#!/usr/bin/env python3
"""Parser for i3 window manager config files"""

import re
import os
from pathlib import Path

def parse_i3_config(config_path):
    """
    Parse i3 config file and extract keybindings
    Returns list of dicts with keys: key, description, category
    """
    config_path = os.path.expanduser(config_path)
    
    if not os.path.exists(config_path):
        return []
    
    keymaps = []
    categories = {
        'exec': 'Applications',
        'kill': 'Window Management',
        'split': 'Layouts',
        'focus': 'Navigation',
        'move': 'Window Movement',
        'resize': 'Resize',
        'workspace': 'Workspaces',
        'floating': 'Floating',
        'fullscreen': 'Fullscreen',
        'layout': 'Layouts',
        'reload': 'System',
        'restart': 'System',
        'exit': 'System',
        'mode': 'Modes',
    }
    
    with open(config_path, 'r') as f:
        lines = f.readlines()
    
    # Track the mod key
    mod_key = '$mod'
    
    for line in lines:
        line = line.strip()
        
        # Skip comments and empty lines
        if not line or line.startswith('#'):
            continue
        
        # Extract mod key definition
        if line.startswith('set $mod'):
            mod_parts = line.split()
            if len(mod_parts) >= 3:
                mod_value = mod_parts[2]
                if mod_value == 'Mod4':
                    mod_key = 'Super'
                elif mod_value == 'Mod1':
                    mod_key = 'Alt'
        
        # Parse bindsym
        if line.startswith('bindsym'):
            match = re.match(r'bindsym\s+(\S+)\s+(.+)', line)
            if match:
                key_combo = match.group(1)
                command = match.group(2).strip()
                
                # Replace $mod with actual key name
                key_combo = key_combo.replace('$mod', mod_key)
                
                # Determine category based on command
                category = 'Other'
                for keyword, cat in categories.items():
                    if keyword in command.lower():
                        category = cat
                        break
                
                # Clean up command for description
                # Remove leading 'exec' and '--no-startup-id'
                description = command
                description = re.sub(r'^exec\s+(--no-startup-id\s+)?', '', description)
                description = re.sub(r'^--no-startup-id\s+', '', description)
                
                # Truncate long commands
                if len(description) > 60:
                    description = description[:57] + '...'
                
                keymaps.append({
                    'key': key_combo,
                    'description': description,
                    'category': category
                })
    
    return keymaps


if __name__ == '__main__':
    # Test the parser
    keymaps = parse_i3_config('~/dotfiles/i3/config')
    for km in keymaps[:10]:
        print(f"{km['category']:20} {km['key']:25} {km['description']}")
