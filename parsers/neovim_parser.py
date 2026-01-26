#!/usr/bin/env python3
"""Parser for Neovim Lua configuration files"""

import re
import os
from pathlib import Path

def parse_neovim_config(config_dir):
    """
    Parse neovim lua config directory and extract keybindings
    Returns list of dicts with keys: key, description, category, mode
    """
    config_dir = os.path.expanduser(config_dir)
    
    if not os.path.exists(config_dir):
        return []
    
    keymaps = []
    
    # Find all lua files recursively
    lua_files = []
    for root, dirs, files in os.walk(config_dir):
        for file in files:
            if file.endswith('.lua'):
                lua_files.append(os.path.join(root, file))
    
    for lua_file in lua_files:
        keymaps.extend(parse_lua_file(lua_file))
    
    return keymaps


def parse_lua_file(file_path):
    """Parse a single Lua file for keymaps"""
    keymaps = []
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except Exception as e:
        return keymaps
    
    # Pattern 1: vim.keymap.set('mode', 'key', 'command', { desc = 'description' })
    pattern1 = r"vim\.keymap\.set\s*\(\s*['\"](\w+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*[^,]+,\s*\{[^}]*desc\s*=\s*['\"]([^'\"]+)['\"]"
    
    # Pattern 2: vim.keymap.set('mode', 'key', 'command')
    pattern2 = r"vim\.keymap\.set\s*\(\s*['\"](\w+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]?([^'\")\n]+)['\"]?\s*\)"
    
    # Pattern 3: vim.api.nvim_set_keymap('mode', 'key', 'command', { ... })
    pattern3 = r"vim\.api\.nvim_set_keymap\s*\(\s*['\"](\w+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]"
    
    # Pattern 4: which-key spec format
    pattern4 = r"\{\s*['\"](<leader>\w+)['\"]\s*,\s*group\s*=\s*['\"]([^'\"]+)['\"]"
    
    # Find all matches with descriptions
    for match in re.finditer(pattern1, content, re.MULTILINE):
        mode = match.group(1)
        key = match.group(2)
        description = match.group(3)
        
        category = categorize_keymap(key, description, file_path)
        
        keymaps.append({
            'key': format_key(key, mode),
            'description': description,
            'category': category,
            'mode': mode
        })
    
    # Find matches without explicit descriptions
    for match in re.finditer(pattern2, content, re.MULTILINE):
        mode = match.group(1)
        key = match.group(2)
        command = match.group(3)
        
        # Skip if we already captured this with description
        if any(km['key'] == format_key(key, mode) for km in keymaps):
            continue
        
        category = categorize_keymap(key, command, file_path)
        description = simplify_command(command)
        
        keymaps.append({
            'key': format_key(key, mode),
            'description': description,
            'category': category,
            'mode': mode
        })
    
    # Find vim.api.nvim_set_keymap calls
    for match in re.finditer(pattern3, content, re.MULTILINE):
        mode = match.group(1)
        key = match.group(2)
        command = match.group(3)
        
        # Skip if already captured
        if any(km['key'] == format_key(key, mode) for km in keymaps):
            continue
        
        category = categorize_keymap(key, command, file_path)
        description = simplify_command(command)
        
        keymaps.append({
            'key': format_key(key, mode),
            'description': description,
            'category': category,
            'mode': mode
        })
    
    # Find which-key group definitions
    for match in re.finditer(pattern4, content, re.MULTILINE):
        key = match.group(1)
        group_name = match.group(2)
        
        keymaps.append({
            'key': key,
            'description': f'[Group] {group_name}',
            'category': 'Leader Groups',
            'mode': 'n'
        })
    
    return keymaps


def format_key(key, mode):
    """Format key binding with mode indicator"""
    # Replace common patterns for readability
    key = key.replace('<leader>', 'Space')
    key = key.replace('<C-', 'Ctrl+')
    key = key.replace('<M-', 'Alt+')
    key = key.replace('<S-', 'Shift+')
    key = key.replace('>', '')
    
    # Add mode prefix for non-normal modes
    mode_prefix = ''
    if mode == 'i':
        mode_prefix = '[Insert] '
    elif mode == 'v':
        mode_prefix = '[Visual] '
    elif mode == 't':
        mode_prefix = '[Terminal] '
    elif mode == 'x':
        mode_prefix = '[Visual Block] '
    
    return f"{mode_prefix}{key}"


def categorize_keymap(key, description, file_path):
    """Determine category based on key, description, and file location"""
    desc_lower = description.lower()
    file_lower = file_path.lower()
    
    # Category based on file location
    if 'lsp' in file_lower:
        return 'LSP'
    elif 'telescope' in file_lower or 'fzf' in file_lower:
        return 'Fuzzy Finder'
    elif 'git' in file_lower or 'gitsigns' in file_lower:
        return 'Git'
    elif 'buffer' in file_lower:
        return 'Buffers'
    elif 'copilot' in file_lower:
        return 'AI/Copilot'
    elif 'theme' in file_lower:
        return 'Themes'
    
    # Category based on description
    if any(word in desc_lower for word in ['search', 'find', 'telescope', 'fzf']):
        return 'Search'
    elif any(word in desc_lower for word in ['git', 'diff', 'commit', 'branch']):
        return 'Git'
    elif any(word in desc_lower for word in ['lsp', 'diagnostic', 'definition', 'hover', 'reference']):
        return 'LSP'
    elif any(word in desc_lower for word in ['buffer', 'buf']):
        return 'Buffers'
    elif any(word in desc_lower for word in ['window', 'split', 'focus']):
        return 'Windows'
    elif any(word in desc_lower for word in ['copy', 'paste', 'yank', 'clipboard']):
        return 'Clipboard'
    elif any(word in desc_lower for word in ['terminal']):
        return 'Terminal'
    elif any(word in desc_lower for word in ['format', 'indent']):
        return 'Formatting'
    elif '<leader>' in key or 'Space' in key:
        return 'Leader Commands'
    
    return 'General'


def simplify_command(command):
    """Simplify vim command for display"""
    # Remove <cmd> and <CR> tags
    command = command.replace('<cmd>', '').replace('<CR>', '').replace('<Esc>', '')
    
    # Truncate long commands
    if len(command) > 60:
        command = command[:57] + '...'
    
    return command.strip()


if __name__ == '__main__':
    # Test the parser
    keymaps = parse_neovim_config('~/dotfiles/nvim')
    
    # Group by category
    by_category = {}
    for km in keymaps:
        cat = km['category']
        if cat not in by_category:
            by_category[cat] = []
        by_category[cat].append(km)
    
    # Print sample from each category
    for category, maps in sorted(by_category.items()):
        print(f"\n{category}:")
        for km in maps[:3]:
            print(f"  {km['key']:30} {km['description']}")
