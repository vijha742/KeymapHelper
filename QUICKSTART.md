# Keymap Helper - Quick Start

## Installation Complete!

Your keymap helper is ready to use at:
`~/Documents/Vikas/KeymapHelper`

## Usage

### From tmux (Recommended)
```
C-a K       (Ctrl+A, then Shift+K)
```

### From command line
```bash
cd ~/Documents/Vikas/KeymapHelper
./keymap-helper.sh
```

## What's Included

**14 Utilities Ready to Use:**

**Your Configs (Auto-Parsed):**
- i3 Window Manager (35 keybindings)
- tmux (26 keybindings)
- Neovim (22 keybindings)
- Alacritty

**Built-in Cheatsheets:**
- Bash/Readline shortcuts
- fzf keybindings
- Git commands
- LazyGit, LazyDocker
- Docker commands
- htop, btop
- less, make

## Navigation

1. **Select utility** → Type to search → Enter
2. **View keymaps** → Type `/` to search → ESC to go back
3. **Quit** → Press `q` or ESC

## Examples

**Find bash word delete shortcut:**
1. C-a K
2. Select "Bash Shell"
3. Type `/delete word`
4. See: Ctrl+W, Alt+D, Alt+Backspace

**Check tmux split commands:**
1. C-a K
2. Select "tmux"
3. Type `/split`
4. See: C-a | (horizontal), C-a - (vertical)

## Customization

**Enable/disable utilities:**
Edit `config.yaml`

**Add custom keymaps:**
Edit `data/keymaps.yaml`

**Configs auto-refresh:**
Changes to i3/tmux/nvim configs are picked up automatically

## Testing

Run the test suite:
```bash
./test.sh
```

## Need Help?

See README.md for full documentation
See USAGE_EXAMPLES.md for detailed examples

## First Time Setup

If tmux binding doesn't work:
```bash
tmux source-file ~/.tmux.conf
```

Then try `C-a K` again!
