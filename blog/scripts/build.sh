#!/bin/bash

set -euo pipefail

# Build script for baladengale-markdown-site

# Define directories
CONTENT_DIR="./content"
POSTS_DIR="./posts"
TEMPLATES_DIR="./templates"
OUTPUT_DIR="./output"

# Ensure Node dependencies are installed (npm). This helps when the project contains JS/CSS build steps.
ensure_npm() {
    if command -v npm >/dev/null 2>&1; then
        echo "npm found: $(npm --version)"
        # Prefer clean install if package-lock exists
        if [ -f package-lock.json ]; then
            echo "Running npm ci to install exact dependencies..."
            npm ci
        else
            echo "Running npm install..."
            npm install
        fi
        return 0
    fi

    echo "npm not found. Attempting to install via apt-get..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update || true
        if sudo apt-get install -y npm nodejs; then
            echo "npm/nodejs installed via apt"
            if [ -f package-lock.json ]; then
                npm ci
            else
                npm install
            fi
            return 0
        else
            echo "apt install for npm failed. Continuing without npm."
            return 1
        fi
    else
        echo "apt-get not available; cannot install npm automatically. Continuing without npm."
        return 1
    fi
}

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

# Ensure pandoc is available. Try apt, then a binary tarball fallback.
ensure_pandoc() {
    if command -v pandoc >/dev/null 2>&1; then
        echo "pandoc found: $(pandoc --version | head -n1)"
        return 0
    fi

    echo "pandoc not found. Attempting to install via apt..."
    if command -v apt-get >/dev/null 2>&1; then
        sudo apt-get update || true
        if sudo apt-get install -y pandoc; then
            echo "pandoc installed via apt"
            return 0
        else
            echo "apt install failed or not permitted, will try fallback download"
        fi
    else
        echo "apt-get not available on this system. Trying fallback download..."
    fi

    # Fallback: download a prebuilt pandoc tarball and install the binary.
    PANDOC_VER="3.1.4"
    TMPDIR="/tmp/pandoc-install-$$"
    mkdir -p "$TMPDIR"
    echo "Downloading pandoc $PANDOC_VER to $TMPDIR..."
    wget -q -O "$TMPDIR/pandoc.tar.gz" "https://github.com/jgm/pandoc/releases/download/$PANDOC_VER/pandoc-$PANDOC_VER-linux-amd64.tar.gz"
    tar -xzf "$TMPDIR/pandoc.tar.gz" -C "$TMPDIR"
    if [ -f "$TMPDIR/pandoc-$PANDOC_VER/bin/pandoc" ]; then
        echo "Installing pandoc binary to /usr/local/bin (requires sudo)..."
        sudo cp -f "$TMPDIR/pandoc-$PANDOC_VER/bin/pandoc" /usr/local/bin/
        sudo chmod +x /usr/local/bin/pandoc
        echo "pandoc installed to /usr/local/bin"
        rm -rf "$TMPDIR"
        return 0
    else
        echo "pandoc binary not found in downloaded archive"
        rm -rf "$TMPDIR"
        return 1
    fi
}

# Function to convert markdown to HTML
convert_markdown() {
        local input_file=$1
        local output_file=$2
        if [ ! -f "$input_file" ]; then
                echo "Warning: input file '$input_file' not found. Skipping."
                return 0
        fi
        pandoc "$input_file" -o "$output_file" --template="$TEMPLATES_DIR/layout.html"
}

# Main
if ! ensure_pandoc; then
    echo "Error: pandoc is required but could not be installed. Exiting."
    exit 1
fi

# Convert index.md
convert_markdown "$CONTENT_DIR/index.md" "$OUTPUT_DIR/index.html"

# Convert blog.md
convert_markdown "$CONTENT_DIR/blog.md" "$OUTPUT_DIR/blog.html"

# Convert about.md
convert_markdown "$CONTENT_DIR/about.md" "$OUTPUT_DIR/about.html"

# Convert all blog posts
shopt -s nullglob
for post in "$POSTS_DIR"/*.md; do
        post_name=$(basename "$post" .md)
        convert_markdown "$post" "$OUTPUT_DIR/$post_name.html"
done
shopt -u nullglob

echo "Build completed. Output files are located in the '$OUTPUT_DIR' directory."