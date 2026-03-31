#!/usr/bin/env python3
"""Parser for Alacritty terminal configuration files"""

import os

# Try to import TOML library
try:
    import tomli as tomllib  # For Python < 3.11
    HAS_TOML = True
except ImportError:
    try:
        import tomllib  # For Python >= 3.11
        HAS_TOML = True
    except ImportError:
        HAS_TOML = False

def parse_alacritty_config(config_path):
    """
    Parse alacritty TOML config and extract keybindings
    Returns list of dicts with keys: key, description, category
    """
    config_path = os.path.expanduser(config_path)
    
    if not os.path.exists(config_path):
        return get_default_keymaps()
    
    # If TOML library is not available, return defaults
    if not HAS_TOML:
        return get_default_keymaps()
    
    keymaps = []
    
    try:
        with open(config_path, 'rb') as f:
            config = tomllib.load(f)
    except Exception as e:
        # If TOML parsing fails, return defaults
        return get_default_keymaps()
    
    # Check if keybindings exist in config
    keyboard = config.get('keyboard', {})
    bindings = keyboard.get('bindings', [])
    
    for binding in bindings:
        key = binding.get('key', '')
        mods = binding.get('mods', '')
        action = binding.get('action', '')
        
        # Format key combination
        if mods:
            key_display = f"{mods}+{key}"
        else:
            key_display = key
        
        # Determine category based on action
        category = 'Other'
        if 'Paste' in action or 'Copy' in action:
            category = 'Clipboard'
        elif 'Font' in action:
            category = 'Font Size'
        elif 'Window' in action or 'Fullscreen' in action:
            category = 'Window'
        elif 'Vi' in action or 'Search' in action:
            category = 'Search'
        elif 'Scroll' in action:
            category = 'Scrolling'
        
        keymaps.append({
            'key': key_display,
            'description': action,
            'category': category
        })
    
    # If no keybindings found in config, return defaults
    if not keymaps:
        return get_default_keymaps()
    
    return keymaps


def get_default_keymaps():
    """Return default Alacritty keybindings"""
    return [
        {'key': 'Ctrl+Shift+C', 'description': 'Copy to clipboard', 'category': 'Clipboard'},
        {'key': 'Ctrl+Shift+V', 'description': 'Paste from clipboard', 'category': 'Clipboard'},
        {'key': 'Ctrl++', 'description': 'Increase font size', 'category': 'Font Size'},
        {'key': 'Ctrl+-', 'description': 'Decrease font size', 'category': 'Font Size'},
        {'key': 'Ctrl+0', 'description': 'Reset font size', 'category': 'Font Size'},
        {'key': 'Ctrl+Shift+Space', 'description': 'Enter vi mode', 'category': 'Vi Mode'},
        {'key': 'Ctrl+Shift+F', 'description': 'Search forward', 'category': 'Search'},
        {'key': 'Ctrl+Shift+B', 'description': 'Search backward', 'category': 'Search'},
        {'key': 'Ctrl+Shift+U', 'description': 'Scroll page up', 'category': 'Scrolling'},
        {'key': 'Ctrl+Shift+D', 'description': 'Scroll page down', 'category': 'Scrolling'},
        {'key': 'Ctrl+Shift+Home', 'description': 'Scroll to top', 'category': 'Scrolling'},
        {'key': 'Ctrl+Shift+End', 'description': 'Scroll to bottom', 'category': 'Scrolling'},
    ]


if __name__ == '__main__':
    # Test the parser
    keymaps = parse_alacritty_config('~/dotfiles/alacritty/alacritty.toml')
    for km in keymaps:
        print(f"{km['category']:20} {km['key']:25} {km['description']}")
