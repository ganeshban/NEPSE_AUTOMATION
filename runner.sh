#!/bin/bash

INPUT_DIR="GO"
RUNNER_DIR="runner"
mkdir -p "$RUNNER_DIR"
find "$INPUT_DIR" -type f -name "*.go" | while read -r gofile; do
    rel_path="${gofile#$INPUT_DIR/}"       # e.g., foo/bar.go
    name="${rel_path//\//_}"               # e.g., foo_bar.go
    name="${name%.*}"                      # e.g., foo_bar

    runner_script="$RUNNER_DIR/$name.sh"

    cat > "$runner_script" <<EOF
#!/bin/bash
cd "\$(dirname "\$0")/.."

# Load shared environment variables
if [ -f "$INPUT_DIR/.env" ]; then
  set -a
  source "$INPUT_DIR/.env"
  set +a
fi

# Run Go file
go run "$gofile"
EOF

    chmod +x "$runner_script"
done
