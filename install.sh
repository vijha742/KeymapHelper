#!/usr/bin/env bash
# Keymap Helper - One-liner installation script
# Usage: curl -fsSL https://raw.githubusercontent.com/YOUR_USERNAME/KeymapHelper/main/install.sh | bash

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Installation directory
INSTALL_DIR="$HOME/.keymap-helper"
BIN_DIR="$HOME/.local/bin"

echo -e "${BLUE}╔═══════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║        Keymap Helper Installation Script         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════════╝${NC}"
echo ""

# Check dependencies
echo -e "${YELLOW}→${NC} Checking dependencies..."

if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗${NC} Python 3 is required but not installed"
    echo "  Please install Python 3 and try again"
    exit 1
fi
echo -e "${GREEN}✓${NC} Python 3 found"

if ! command -v git &> /dev/null; then
    echo -e "${RED}✗${NC} Git is required but not installed"
    echo "  Please install Git and try again"
    exit 1
fi
echo -e "${GREEN}✓${NC} Git found"

# Check for fzf
if ! command -v fzf &> /dev/null; then
    echo -e "${YELLOW}!${NC} fzf not found - will install"
    
    # Install fzf
    if [ ! -d "$HOME/.fzf" ]; then
        echo -e "${YELLOW}→${NC} Installing fzf..."
        git clone --depth 1 https://github.com/junegunn/fzf.git ~/.fzf
        ~/.fzf/install --key-bindings --completion --no-update-rc
        echo -e "${GREEN}✓${NC} fzf installed"
    else
        echo -e "${GREEN}✓${NC} fzf already installed at ~/.fzf"
    fi
else
    echo -e "${GREEN}✓${NC} fzf found"
fi

# Check for PyYAML
echo -e "${YELLOW}→${NC} Checking Python dependencies..."
if ! python3 -c "import yaml" &> /dev/null; then
    echo -e "${YELLOW}→${NC} Installing PyYAML..."
    pip3 install --user PyYAML
    echo -e "${GREEN}✓${NC} PyYAML installed"
else
    echo -e "${GREEN}✓${NC} PyYAML found"
fi

echo ""
echo -e "${YELLOW}→${NC} Installing Keymap Helper..."

# Remove old installation if exists
if [ -d "$INSTALL_DIR" ]; then
    echo -e "${YELLOW}!${NC} Removing old installation..."
    rm -rf "$INSTALL_DIR"
fi

# Clone repository
echo -e "${YELLOW}→${NC} Cloning repository..."
git clone https://github.com/YOUR_USERNAME/KeymapHelper.git "$INSTALL_DIR"

# Make scripts executable
chmod +x "$INSTALL_DIR/keymap-helper.sh"
chmod +x "$INSTALL_DIR/keymap-helper.py"

# Create bin directory if it doesn't exist
mkdir -p "$BIN_DIR"

# Create symlink
ln -sf "$INSTALL_DIR/keymap-helper.sh" "$BIN_DIR/keymap"

echo -e "${GREEN}✓${NC} Keymap Helper installed to $INSTALL_DIR"
echo -e "${GREEN}✓${NC} Symlink created at $BIN_DIR/keymap"

echo ""
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Installation complete!${NC}"
echo -e "${BLUE}═══════════════════════════════════════════════════${NC}"
echo ""
echo "Usage:"
echo "  ${GREEN}keymap${NC}          - Launch interactive TUI"
echo "  ${GREEN}keymap --stats${NC}  - Show statistics dashboard"
echo ""
echo "Optional: Add tmux integration"
echo "  Add this to your ~/.tmux.conf:"
echo "  ${YELLOW}bind-key K display-popup -E -w 90% -h 90% \"keymap\"${NC}"
echo ""

# Check if ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$BIN_DIR:"* ]]; then
    echo -e "${YELLOW}⚠ Warning:${NC} $BIN_DIR is not in your PATH"
    echo "  Add this to your ~/.bashrc or ~/.zshrc:"
    echo "  ${YELLOW}export PATH=\"\$HOME/.local/bin:\$PATH\"${NC}"
    echo ""
fi

echo "Run ${GREEN}keymap${NC} to get started!"
