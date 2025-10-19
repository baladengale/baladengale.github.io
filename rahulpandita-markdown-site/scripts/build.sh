#!/bin/bash

# Build script for rahulpandita-markdown-site

# Define directories
CONTENT_DIR="./content"
POSTS_DIR="./posts"
TEMPLATES_DIR="./templates"
OUTPUT_DIR="./output"

# Create output directory if it doesn't exist
mkdir -p $OUTPUT_DIR

# Function to convert markdown to HTML
convert_markdown() {
    local input_file=$1
    local output_file=$2
    pandoc "$input_file" -o "$output_file" --template="$TEMPLATES_DIR/layout.html"
}

# Convert index.md
convert_markdown "$CONTENT_DIR/index.md" "$OUTPUT_DIR/index.html"

# Convert blog.md
convert_markdown "$CONTENT_DIR/blog.md" "$OUTPUT_DIR/blog.html"

# Convert about.md
convert_markdown "$CONTENT_DIR/about.md" "$OUTPUT_DIR/about.html"

# Convert all blog posts
for post in "$POSTS_DIR"/*.md; do
    post_name=$(basename "$post" .md)
    convert_markdown "$post" "$OUTPUT_DIR/$post_name.html"
done

echo "Build completed. Output files are located in the '$OUTPUT_DIR' directory."