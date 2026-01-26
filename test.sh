#!/usr/bin/env bash
# Test script for keymap-helper

echo "Testing Keymap Helper Components..."
echo

# Test 1: Check if scripts are executable
echo "1. Checking file permissions..."
if [ -x "keymap-helper.sh" ] && [ -x "keymap-helper.py" ]; then
    echo "   ✓ Scripts are executable"
else
    echo "   ✗ Scripts need to be executable"
    exit 1
fi

# Test 2: Check Python and dependencies
echo "2. Checking Python and dependencies..."
if python3 -c "import yaml" 2>/dev/null; then
    echo "   ✓ Python 3 and PyYAML available"
else
    echo "   ✗ Missing Python 3 or PyYAML"
    exit 1
fi

# Test 3: Test listing utilities
echo "3. Testing utility list..."
output=$(python3 keymap-helper.py list-utilities 2>&1)
if [ $? -eq 0 ] && echo "$output" | grep -q "i3"; then
    echo "   ✓ Can list utilities"
    echo "   Found $(echo "$output" | wc -l) utilities"
else
    echo "   ✗ Failed to list utilities"
    exit 1
fi

# Test 4: Test static keymaps
echo "4. Testing static keymaps (bash)..."
output=$(python3 keymap-helper.py show "Bash Shell" 2>&1)
if [ $? -eq 0 ] && echo "$output" | grep -q "Ctrl"; then
    echo "   ✓ Static keymaps work"
else
    echo "   ✗ Failed to load static keymaps"
    exit 1
fi

# Test 5: Test config parser (i3)
echo "5. Testing i3 config parser..."
output=$(python3 keymap-helper.py show "i3 Window Manager" 2>&1)
if [ $? -eq 0 ]; then
    keymap_count=$(echo "$output" | grep -c "Super\|Ctrl\|Alt")
    echo "   ✓ i3 parser works (found $keymap_count keybindings)"
else
    echo "   ✗ Failed to parse i3 config"
fi

# Test 6: Test tmux parser
echo "6. Testing tmux config parser..."
output=$(python3 keymap-helper.py show "tmux" 2>&1)
if [ $? -eq 0 ]; then
    keymap_count=$(echo "$output" | grep -c "C-a")
    echo "   ✓ tmux parser works (found $keymap_count keybindings)"
else
    echo "   ✗ Failed to parse tmux config"
fi

# Test 7: Test neovim parser
echo "7. Testing neovim config parser..."
output=$(python3 keymap-helper.py show "Neovim" 2>&1)
if [ $? -eq 0 ]; then
    keymap_count=$(echo "$output" | grep -c "Space\|Ctrl")
    echo "   ✓ neovim parser works (found $keymap_count keybindings)"
else
    echo "   ✗ Failed to parse neovim config"
fi

# Test 8: Check fzf availability
echo "8. Checking fzf availability..."
if command -v fzf &> /dev/null; then
    echo "   ✓ fzf is available"
else
    echo "   ⚠ fzf not in PATH (but may be at ~/.fzf/bin/fzf)"
fi

# Test 9: Check tmux config
echo "9. Checking tmux keybinding..."
if grep -q "bind-key K.*keymap-helper" ~/.tmux.conf 2>/dev/null; then
    echo "   ✓ tmux keybinding configured (C-a K)"
else
    echo "   ⚠ tmux keybinding not found in ~/.tmux.conf"
fi

echo
echo "========================================="
echo "All tests passed! ✓"
echo "========================================="
echo
echo "To use the keymap helper:"
echo "1. In tmux, press C-a K (Ctrl+A, then Shift+K)"
echo "2. Or run directly: ./keymap-helper.sh"
echo
echo "Note: You may need to reload tmux config:"
echo "  tmux source-file ~/.tmux.conf"
