#!/usr/bin/env python3
"""
Keymap Helper - Main orchestrator
Loads configurations, parses keymaps, and formats for fzf display
"""

import os
import sys
import yaml
from pathlib import Path

# Add parsers directory to path
SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR / 'parsers'))

# Import parsers
from i3_parser import parse_i3_config
from tmux_parser import parse_tmux_config
from neovim_parser import parse_neovim_config
from alacritty_parser import parse_alacritty_config


def load_config():
    """Load configuration from config.yaml"""
    config_path = SCRIPT_DIR / 'config.yaml'
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    return config


def load_static_keymaps():
    """Load static keymaps from data/keymaps.yaml"""
    keymaps_path = SCRIPT_DIR / 'data' / 'keymaps.yaml'
    
    with open(keymaps_path, 'r') as f:
        keymaps = yaml.safe_load(f)
    
    return keymaps


def get_keymaps_for_utility(utility, config, static_keymaps):
    """
    Get keymaps for a specific utility
    Returns list of dicts with keys: key, description, category
    """
    parser_type = utility.get('parser')
    config_path = utility.get('config_path')
    utility_name = utility.get('name')
    
    keymaps = []
    
    if parser_type == 'static':
        # Load from static database
        if utility_name in static_keymaps:
            categories = static_keymaps[utility_name]
            for category_data in categories:
                category_name = category_data.get('category', 'General')
                for keymap in category_data.get('keymaps', []):
                    keymaps.append({
                        'key': keymap['key'],
                        'description': keymap['description'],
                        'category': category_name
                    })
    
    elif parser_type == 'i3':
        keymaps = parse_i3_config(config_path)
    
    elif parser_type == 'tmux':
        keymaps = parse_tmux_config(config_path)
    
    elif parser_type == 'neovim':
        keymaps = parse_neovim_config(config_path)
    
    elif parser_type == 'alacritty':
        keymaps = parse_alacritty_config(config_path)
    
    return keymaps


def format_keymaps_for_fzf(keymaps, separator="━━━"):
    """
    Format keymaps for fzf display with category grouping
    Returns formatted string
    """
    if not keymaps:
        return "No keymaps found"
    
    # Group by category
    by_category = {}
    for km in keymaps:
        category = km.get('category', 'Other')
        if category not in by_category:
            by_category[category] = []
        by_category[category].append(km)
    
    # Format output
    lines = []
    for category in sorted(by_category.keys()):
        # Category header
        lines.append(f"\n{separator} {category} {separator}")
        
        # Keymaps in this category
        for km in by_category[category]:
            key = km['key']
            desc = km['description']
            
            # Format: "KEY                  Description"
            line = f"{key:<30} {desc}"
            lines.append(line)
    
    return '\n'.join(lines)


def list_utilities(config):
    """
    List all enabled utilities for fzf selection
    Returns formatted string
    """
    utilities = config.get('utilities', [])
    enabled = [u for u in utilities if u.get('enabled', True)]
    
    lines = []
    for util in enabled:
        name = util.get('display_name', util.get('name'))
        parser = util.get('parser', 'unknown')
        
        # Format: "display_name (parser_type)"
        line = f"{name:<40} [{parser}]"
        lines.append(line)
    
    return '\n'.join(lines)


def get_utility_by_display_name(display_name, config):
    """Find utility config by display name"""
    utilities = config.get('utilities', [])
    
    for util in utilities:
        util_display = util.get('display_name', util.get('name'))
        if display_name.strip().startswith(util_display):
            return util
    
    return None


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: keymap-helper.py <command> [args]")
        print("Commands:")
        print("  list-utilities    - List all enabled utilities")
        print("  show <utility>    - Show keymaps for utility")
        sys.exit(1)
    
    command = sys.argv[1]
    
    # Load configuration
    config = load_config()
    static_keymaps = load_static_keymaps()
    
    if command == 'list-utilities':
        print(list_utilities(config))
    
    elif command == 'show' and len(sys.argv) >= 3:
        utility_display = ' '.join(sys.argv[2:])
        utility = get_utility_by_display_name(utility_display, config)
        
        if not utility:
            print(f"Utility not found: {utility_display}")
            sys.exit(1)
        
        keymaps = get_keymaps_for_utility(utility, config, static_keymaps)
        
        separator = config.get('display', {}).get('category_separator', '━━━')
        formatted = format_keymaps_for_fzf(keymaps, separator)
        
        print(formatted)
    
    else:
        print(f"Unknown command: {command}")
        sys.exit(1)


if __name__ == '__main__':
    main()
