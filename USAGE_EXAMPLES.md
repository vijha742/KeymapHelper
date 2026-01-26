# Keymap Helper - Usage Examples

## Quick Start

Press `C-a K` in tmux to launch the keymap helper!

## Example Outputs

### 1. Utility Selection Screen (Level 1)

When you first launch the tool, you'll see:

```
Select utility: _
> i3 Window Manager                        [i3]
  tmux                                     [tmux]
  Alacritty Terminal                       [alacritty]
  Neovim                                   [neovim]
  Bash Shell                               [static]
  fzf - Fuzzy Finder                       [static]
  Git                                      [static]
  LazyGit                                  [static]
  Docker CLI                               [static]
  LazyDocker                               [static]
  htop                                     [static]
  btop                                     [static]
  less                                     [static]
  GNU Make                                 [static]

Select a utility to view keymaps | Press / to search, ESC or q to quit
```

Type to fuzzy search: `git` will show only Git and LazyGit

### 2. Keymap Display Screen (Level 2)

After selecting "Bash Shell", you'll see:

```
━━━ Navigation ━━━
Ctrl+A                         Move to beginning of line
Ctrl+E                         Move to end of line
Ctrl+B / Left                  Move back one character
Ctrl+F / Right                 Move forward one character
Alt+B                          Move back one word
Alt+F                          Move forward one word

━━━ Editing ━━━
Ctrl+D                         Delete character under cursor
Ctrl+H / Backspace             Delete character before cursor
Ctrl+W                         Delete word before cursor
Ctrl+U                         Delete from cursor to beginning of line
Ctrl+K                         Delete from cursor to end of line
Ctrl+Y                         Paste last deleted text

━━━ History ━━━
Ctrl+R                         Reverse search history
Ctrl+G                         Escape from history search
Ctrl+P / Up                    Previous command in history
Ctrl+N / Down                  Next command in history

━━━ Control ━━━
Ctrl+L                         Clear screen
Ctrl+C                         Cancel current command
Ctrl+Z                         Suspend current process

Keymaps for Bash Shell | Press / to search, ESC to go back, q to quit
```

Type `/reverse` to instantly jump to "Reverse search history"

### 3. Your Custom i3 Keybindings

After selecting "i3 Window Manager":

```
━━━ Applications ━━━
Super+Return                   alacritty
Super+e                        nemo
Super+b                        ~/Downloads/zen/zen
Super+d                        rofi -show drun -theme tokyonight.rasi

━━━ Navigation ━━━
Super+Left                     focus left
Super+Down                     focus down
Super+Up                       focus up
Super+Right                    focus right

━━━ Workspaces ━━━
Super+1                        workspace number $ws1
Super+2                        workspace number $ws2
...

━━━ Window Management ━━━
Super+w                        kill
Super+Shift+c                  reload
Super+Shift+r                  restart
```

### 4. Your Custom Neovim Keymaps

After selecting "Neovim":

```
━━━ LSP ━━━
Spaceq                         Open diagnostic [Q]uickfix list

━━━ Fuzzy Finder ━━━
Spacesh                        [S]earch [H]elp
Spacesk                        [S]earch [K]eymaps
Ctrl+p                         [S]earch [F]iles
Spacess                        [S]earch [S]elect Telescope
Spacesg                        [S]earch by [G]rep

━━━ Windows ━━━
Ctrl+h                         Move focus to the left window
Ctrl+l                         Move focus to the right window
Ctrl+j                         Move focus to the lower window
Ctrl+k                         Move focus to the upper window

━━━ Clipboard ━━━
Spacey                         Copy to system clipboard
Spacep                         Paste from system clipboard

━━━ Themes ━━━
Spacetn                        Next Theme
Spacetp                        Previous Theme
Spacetc                        Pick Theme (Telescope)
```

### 5. Git Commands Quick Reference

After selecting "Git":

```
━━━ Basic Commands ━━━
git status                     Show working tree status
git add <file>                 Add file to staging
git add .                      Add all changes to staging
git commit -m                  Commit staged changes
git push                       Push commits to remote
git pull                       Fetch and merge from remote

━━━ Branching ━━━
git branch                     List branches
git checkout <branch>          Switch to branch
git checkout -b <name>         Create and switch to branch
git merge <branch>             Merge branch into current

━━━ History & Inspection ━━━
git log                        Show commit history
git log --oneline              Compact commit history
git diff                       Show unstaged changes
git diff --staged              Show staged changes
```

## Search Examples

### Scenario: "I know there's a bash shortcut to delete a word, but I forgot it"

1. Press `C-a K`
2. Select "Bash Shell"
3. Type `/delete word`
4. Results instantly filter to show:
   - `Ctrl+W` - Delete word before cursor
   - `Alt+D` - Delete word after cursor
   - `Alt+Backspace` - Delete word before cursor

### Scenario: "How do I split tmux panes again?"

1. Press `C-a K`
2. Select "tmux"
3. Type `/split`
4. See:
   - `C-a |` - Split pane horizontally
   - `C-a -` - Split pane vertically

### Scenario: "What was that nvim keymap for searching files?"

1. Press `C-a K`
2. Select "Neovim"
3. Type `/search file` or just `/file`
4. See: `Ctrl+p` - [S]earch [F]iles

## Tips

- The search is fuzzy and searches BOTH the key and description
- You can search "ctrl word" to find all Ctrl+something that deal with words
- Press ESC once to go back to utility list, twice to quit
- Categories are visual separators and help organize large keymaps
- The tool reads your actual config files, so it's always in sync

## Common Workflows

### Learning a new tool
Browse through the keymaps without searching to discover features

### Refreshing your memory
Quick search when you vaguely remember a feature but forgot the key

### Comparing similar tools
Switch between lazygit and git to see command differences

### Documenting your setup
The parsed keymaps show exactly what you've configured
