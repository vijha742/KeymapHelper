#!/usr/bin/env bash
# Keymap Helper - Shell entry script
# This script is called by tmux and provides the fzf interface

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HELPER_SCRIPT="$SCRIPT_DIR/keymap-helper.py"

# Colors for fzf
export FZF_DEFAULT_OPTS="
  --height=100%
  --layout=reverse
  --border=rounded
  --margin=1
  --padding=1
  --color=dark
  --color=fg:-1,bg:-1,hl:#7aa2f7
  --color=fg+:#c0caf5,bg+:#292e42,hl+:#7dcfff
  --color=info:#7dcfff,prompt:#7dcfff,pointer:#7dcfff
  --color=marker:#9ece6a,spinner:#9ece6a,header:#9ece6a
  --bind='ctrl-/:toggle-preview'
"

show_utility_keymaps() {
    local utility="$1"
    
    # Get keymaps and display with fzf
    "$HELPER_SCRIPT" show "$utility" | fzf \
        --ansi \
        --header="Keymaps for $utility | Press / to search, ESC to go back, q to quit" \
        --header-first \
        --no-sort \
        --bind='enter:abort' \
        --bind='esc:abort' \
        --bind='q:abort' \
        --prompt="Search keymap: " \
        --preview-window=hidden
}

main() {
    # Check if Python is available
    if ! command -v python3 &> /dev/null; then
        echo "Error: Python 3 is required but not found"
        exit 1
    fi
    
    # Check if fzf is available
    if ! command -v fzf &> /dev/null; then
        echo "Error: fzf is required but not found"
        echo "Install with: git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf && ~/.fzf/install"
        exit 1
    fi
    
    # Main loop - show utilities list
    while true; do
        # Select utility
        selected_utility=$("$HELPER_SCRIPT" list-utilities | fzf \
            --ansi \
            --header="Select a utility to view keymaps | Press / to search, ESC or q to quit" \
            --header-first \
            --prompt="Select utility: " \
            --preview-window=hidden)
        
        # Check if user cancelled
        if [ -z "$selected_utility" ]; then
            break
        fi
        
        # Show keymaps for selected utility
        show_utility_keymaps "$selected_utility"
    done
}

main
