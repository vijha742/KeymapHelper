# Keymap Helper

A TUI tool to quickly lookup keymaps and shortcuts for your most-used developer tools.

## Features

- Two-level fuzzy search interface powered by fzf
- Parses config files dynamically (i3, tmux, neovim, alacritty)
- Comprehensive built-in keymaps for common CLI tools
- Organized by categories for easy navigation
- Integrated with tmux for quick access (C-a + K)

## Installation

The tool is already set up in `~/Documents/Vikas/KeymapHelper`

### Dependencies

- Python 3.6+
- PyYAML (already installed)
- fzf (already installed at ~/.fzf/bin/fzf)

## Usage

### Quick Access from tmux

Press `C-a K` (Ctrl+A, then Shift+K) while in tmux to open the keymap helper in a popup.

### Manual Usage

```bash
cd ~/Documents/Vikas/KeymapHelper
./keymap-helper.sh
```

### Navigation

1. **First screen:** Select a utility (i3, tmux, neovim, bash, git, etc.)
   - Type `/` followed by search term to filter
   - Use arrow keys or j/k to navigate
   - Press Enter to select

2. **Second screen:** View keymaps for selected utility
   - Type `/` to search across both keybindings and descriptions
   - Categories are automatically grouped
   - Press ESC to go back, q to quit

## Included Utilities

### Config-based (auto-parsed):
- **i3** - Window manager keybindings from your config
- **tmux** - Terminal multiplexer keybindings
- **neovim** - Your custom keymaps from Lua configs
- **alacritty** - Terminal emulator keybindings

### Built-in keymaps:
- **bash** - Readline shortcuts
- **fzf** - Fuzzy finder keybindings
- **git** - Common git commands
- **lazygit** - TUI git client
- **docker** - Docker CLI commands
- **lazydocker** - Docker TUI
- **htop/btop** - System monitors
- **less** - File viewer
- **make** - Build tool

## Customization

### Add/Remove Utilities

Edit `config.yaml` to enable/disable utilities:

```yaml
utilities:
  - name: "bash"
    display_name: "Bash Shell"
    parser: "static"
    enabled: true  # Set to false to disable
```

### Add Custom Keymaps

For static utilities, edit `data/keymaps.yaml`:

```yaml
your_tool:
  - category: "Navigation"
    keymaps:
      - key: "Ctrl+N"
        description: "Go to next item"
```

### Refresh Parsed Configs

The tool parses your config files each time it runs, so any changes to your i3, tmux, or neovim configs will be automatically picked up on next launch.

## Project Structure

```
KeymapHelper/
├── keymap-helper.sh          # Shell entry script with fzf UI
├── keymap-helper.py          # Python orchestrator
├── config.yaml               # User configuration
├── data/
│   └── keymaps.yaml          # Static keymaps database
└── parsers/
    ├── i3_parser.py          # Parse i3 config
    ├── tmux_parser.py        # Parse tmux config
    ├── neovim_parser.py      # Parse neovim Lua configs
    └── alacritty_parser.py   # Parse alacritty config
```

## Tmux Integration

The tool is bound to `C-a K` in your tmux config. To change the binding, edit `~/.tmux.conf`:

```tmux
# Change K to another key if desired
bind-key K display-popup -E -w 90% -h 90% "cd ~/Documents/Vikas/KeymapHelper && ./keymap-helper.sh"
```

Then reload tmux config:
```bash
tmux source-file ~/.tmux.conf
```

## Troubleshooting

### Tool doesn't launch from tmux
1. Make sure scripts are executable: `chmod +x keymap-helper.sh keymap-helper.py`
2. Reload tmux config: `tmux source-file ~/.tmux.conf`
3. Check Python is available: `python3 --version`
4. Check fzf is available: `fzf --version`

### No keymaps shown for a config-based tool
1. Check the config path in `config.yaml` is correct
2. Make sure the config file exists
3. Run manually to see errors: `python3 keymap-helper.py show "Tool Name"`

### Want to test parsers individually
```bash
python3 parsers/i3_parser.py
python3 parsers/tmux_parser.py
python3 parsers/neovim_parser.py
```

## Contributing Your Own Parsers

To add a parser for a new config-based tool:

1. Create `parsers/your_tool_parser.py`
2. Implement `parse_your_tool_config(config_path)` function
3. Return list of dicts: `[{'key': '...', 'description': '...', 'category': '...'}]`
4. Add tool to `config.yaml`
5. Import parser in `keymap-helper.py`

## Tips

- Use the fuzzy search liberally - you can search for both keys and descriptions
- The tool is especially useful when you remember "there's a shortcut for X" but forgot the key
- Category headers are not selectable - they're just visual separators
- For neovim, the tool parses your custom keymaps; default vim keybindings are not included

## Future Enhancements

Possible additions:
- Export keymaps to cheatsheet (PDF/HTML)
- Add more tools (ripgrep, fd, bat, etc.)
- Custom keymap notes/annotations
- Keymap conflicts detection
- Web-based UI option
