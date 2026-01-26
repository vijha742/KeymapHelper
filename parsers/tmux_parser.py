#!/usr/bin/env python3
"""Parser for tmux configuration files"""

import re
import os

def parse_tmux_config(config_path):
    """
    Parse tmux config file and extract keybindings
    Returns list of dicts with keys: key, description, category
    """
    config_path = os.path.expanduser(config_path)
    
    if not os.path.exists(config_path):
        return []
    
    keymaps = []
    
    # Category mapping based on common tmux commands
    categories = {
        'split-window': 'Panes',
        'select-pane': 'Navigation',
        'select-window': 'Windows',
        'new-window': 'Windows',
        'kill-pane': 'Panes',
        'kill-window': 'Windows',
        'resize-pane': 'Panes',
        'copy-mode': 'Copy Mode',
        'paste-buffer': 'Copy Mode',
        'source-file': 'Configuration',
        'display': 'Information',
    }
    
    with open(config_path, 'r') as f:
        lines = f.readlines()
    
    # Track prefix key
    prefix = 'C-b'
    
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Extract prefix key
        if 'set-option -g prefix' in line or 'set -g prefix' in line:
            match = re.search(r'prefix\s+(\S+)', line)
            if match:
                prefix = match.group(1)
        
        # Parse bind and bind-key
        if line.startswith('bind') or line.startswith('bind-key'):
            # Handle various bind formats
            # bind key command
            # bind -n key command (no prefix)
            # bind -r key command (repeatable)
            # bind-key -T copy-mode-vi key command
            
            # Split carefully to handle quoted strings
            parts = line.split(None, 1)
            if len(parts) < 2:
                continue
            
            rest = parts[1]
            
            # Check for flags
            flags = []
            no_prefix = False
            key_table = None
            
            while rest.startswith('-'):
                flag_match = re.match(r'-(\w+)\s+(.+)', rest)
                if flag_match:
                    flag = flag_match.group(1)
                    rest = flag_match.group(2)
                    flags.append(flag)
                    
                    if flag == 'n':
                        no_prefix = True
                    elif flag == 'T':
                        # Extract key table
                        table_match = re.match(r'(\S+)\s+(.+)', rest)
                        if table_match:
                            key_table = table_match.group(1)
                            rest = table_match.group(2)
                else:
                    break
            
            # Extract key and command
            key_cmd_match = re.match(r'([^\s]+)\s+(.+)', rest)
            if not key_cmd_match:
                continue
            
            key = key_cmd_match.group(1)
            command = key_cmd_match.group(2)
            
            # Format the key binding
            if key_table:
                key_display = f"[{key_table}] {key}"
            elif no_prefix:
                key_display = key
            else:
                key_display = f"{prefix} {key}"
            
            # Determine category
            category = 'Other'
            for keyword, cat in categories.items():
                if keyword in command:
                    category = cat
                    break
            
            # Extract description from command or comment
            description = command
            
            # Try to make description more readable
            if 'split-window -h' in command:
                description = 'Split pane horizontally'
            elif 'split-window -v' in command:
                description = 'Split pane vertically'
            elif 'select-pane -L' in command:
                description = 'Select left pane'
            elif 'select-pane -R' in command:
                description = 'Select right pane'
            elif 'select-pane -U' in command:
                description = 'Select upper pane'
            elif 'select-pane -D' in command:
                description = 'Select lower pane'
            elif 'source-file' in command:
                description = 'Reload config'
            elif 'copy-selection' in command:
                description = 'Copy selection'
            elif 'begin-selection' in command:
                description = 'Begin selection'
            
            # Truncate long descriptions
            if len(description) > 60:
                description = description[:57] + '...'
            
            keymaps.append({
                'key': key_display,
                'description': description,
                'category': category
            })
    
    # Add common default tmux keybindings that might not be in config
    default_keymaps = [
        {'key': f'{prefix} c', 'description': 'Create new window', 'category': 'Windows'},
        {'key': f'{prefix} n', 'description': 'Next window', 'category': 'Windows'},
        {'key': f'{prefix} p', 'description': 'Previous window', 'category': 'Windows'},
        {'key': f'{prefix} d', 'description': 'Detach from session', 'category': 'Session'},
        {'key': f'{prefix} z', 'description': 'Toggle pane zoom', 'category': 'Panes'},
        {'key': f'{prefix} [', 'description': 'Enter copy mode', 'category': 'Copy Mode'},
        {'key': f'{prefix} ]', 'description': 'Paste buffer', 'category': 'Copy Mode'},
        {'key': f'{prefix} ,', 'description': 'Rename current window', 'category': 'Windows'},
        {'key': f'{prefix} $', 'description': 'Rename session', 'category': 'Session'},
        {'key': f'{prefix} &', 'description': 'Kill current window', 'category': 'Windows'},
        {'key': f'{prefix} x', 'description': 'Kill current pane', 'category': 'Panes'},
        {'key': f'{prefix} ?', 'description': 'List all keybindings', 'category': 'Help'},
    ]
    
    # Only add defaults that aren't already present
    existing_keys = {km['key'] for km in keymaps}
    for default in default_keymaps:
        if default['key'] not in existing_keys:
            keymaps.append(default)
    
    return keymaps


if __name__ == '__main__':
    # Test the parser
    keymaps = parse_tmux_config('~/.tmux.conf')
    for km in keymaps[:15]:
        print(f"{km['category']:20} {km['key']:25} {km['description']}")
