#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Detect OS
OS="$(uname)"

# Find all .go files in the script directory and its subdirectories
find "$SCRIPT_DIR" -type f -name "*.go" | while read -r go_file; do
    echo "Opening new terminal for $go_file..."

    if [[ "$OS" == "Darwin" ]]; then
        # MacOS: Open in new Terminal window
        osascript -e "tell application \"Terminal\" to do script \"cd '$SCRIPT_DIR'; go run '$go_file'\""

    elif [[ "$OS" == "Linux" ]]; then
        # Linux: Open in a new terminal (adjust for your terminal)
        gnome-terminal -- bash -c "go run \"$go_file\"; exec bash"
        # Alternative:
        # x-terminal-emulator -e bash -c "go run \"$go_file\"; exec bash"

    elif [[ "$OS" == "MINGW64_NT"* || "$OS" == "MSYS_NT"* ]]; then
        # Windows (Git Bash): Use start command to open new cmd.exe window
        cmd.exe /c start "Go Run" bash -c "go run \"$go_file\"; exec bash"

    else
        echo "Unsupported OS: $OS"
    fi
done
