#!/bin/bash

# Get the directory of the script
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Find all .go files in the script directory and its subdirectories
find "$SCRIPT_DIR" -type f -name "*.go" | while read -r go_file; do
    echo "Running $go_file..."
    go install
    go run "$go_file"
done
