#!/bin/bash
cd "$(dirname "$0")/.."

# Load shared environment variables
if [ -f "GO/.env" ]; then
  set -a
  source "GO/.env"
  set +a
fi

# Run Go file
go run "GO/ten.go"
