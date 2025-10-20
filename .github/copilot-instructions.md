# GitHub Copilot Instructions for baladengale.github.io

## Project Overview

This is a personal website/blog for Bala Dengale built using a custom Markdown-to-HTML build system. The site is hosted on GitHub Pages and uses Pandoc for converting Markdown content to HTML.

## Repository Structure

```
./
├── blog/                    # Source code and content
│   ├── content/            # Markdown content for main pages (index, about, blog)
│   ├── posts/              # Blog post Markdown files (YYYY-MM-DD-title.md format)
│   ├── templates/          # HTML templates and Markdown snippets
│   │   ├── layout.html     # Main HTML layout template
│   │   ├── header.md       # Header Markdown snippet
│   │   └── footer.md       # Footer Markdown snippet
│   ├── assets/             # CSS, images, and other static assets
│   ├── scripts/
│   │   ├── build.sh        # Main build script
│   │   ├── server.js       # Local development server
│   │   └── static.js       # Static site server
│   └── package.json        # Node.js dependencies
├── *.html                  # Generated HTML files (build output)
├── assets/                 # Copied assets from blog/assets
└── .github/
    └── workflows/          # GitHub Actions workflows
```

## Build System

### Building the Site

The build process converts Markdown files to HTML using Pandoc:

```bash
# From repository root:
./blog/scripts/build.sh
```

Or using npm:

```bash
cd blog/
npm run build
```

### Build Script Behavior

- **Location**: `blog/scripts/build.sh`
- **Input**: Markdown files in `blog/content/` and `blog/posts/`
- **Output**: HTML files written to repository root (parent of `blog/`)
- **Template**: Uses `blog/templates/layout.html` for HTML structure
- **Dependencies**: Auto-installs `pandoc` and npm packages if missing
- **Environment**: Can override output directory with `OUTPUT_DIR` environment variable

### Development Server

```bash
cd blog/
npm start
```

Runs an Express server for local development. Note: The `package.json` references `server.js`, but the actual file is located at `blog/scripts/server.js`.

## Coding Conventions

### File Naming

- **Blog posts**: Use `YYYY-MM-DD-title.md` format in `blog/posts/`
- **Content pages**: Use lowercase with dashes (e.g., `about.md`)
- **Generated HTML**: Matches source Markdown filename with `.html` extension

### Markdown Content

- Use standard Markdown syntax
- Blog posts should include frontmatter-style metadata at the top
- Keep line lengths reasonable for readability
- Use proper heading hierarchy (h1 -> h2 -> h3)

### HTML Templates

- Main template: `blog/templates/layout.html`
- Uses Pandoc variables for content injection
- Maintain consistent HTML structure and classes
- CSS classes are defined in `blog/assets/css/styles.css`

### Bash Scripts

- Use strict error handling: `set -euo pipefail`
- Re-exec with bash if invoked with sh (for pipefail support)
- Make scripts location-agnostic (use `$SCRIPT_DIR` patterns)
- Document environment variables and defaults
- Provide clear error messages

### CSS

- Main stylesheet: `blog/assets/css/styles.css`
- Follow existing naming conventions
- Use class-based selectors
- Maintain responsive design principles

## Dependencies

### System Dependencies

- **Pandoc**: Required for Markdown to HTML conversion
- **Node.js & npm**: For dependency management and dev server
- **Bash**: For build scripts

### npm Dependencies

See `blog/package.json`:
- `express`: Development server
- `ejs`, `markdown-it`, `markdown`: Markdown processing
- `nodemon`: Development hot-reload (dev dependency)

## Testing

Currently, this is a static site generator without automated tests. When making changes:

1. Run the build script to ensure it completes without errors
2. Check generated HTML files for correctness
3. Verify the local server runs (`npm start`)
4. Manually review the rendered pages in a browser

## Common Tasks

### Adding a New Blog Post

1. Create a new Markdown file in `blog/posts/` with format `YYYY-MM-DD-title.md`
2. Add post metadata (title, date, excerpt)
3. Write content in Markdown
4. Run build script to generate HTML
5. Verify the post appears in `blog.html`

### Modifying Site Styling

1. Edit `blog/assets/css/styles.css`
2. Run build script to copy assets
3. Test changes locally with the dev server

### Updating Page Layout

1. Modify `blog/templates/layout.html`
2. Run build script to regenerate all HTML files
3. Verify changes across all pages

### Modifying Build Process

1. Edit `blog/scripts/build.sh`
2. Test with various scenarios (fresh build, missing dependencies)
3. Ensure script is idempotent and handles errors gracefully

## GitHub Pages Deployment

The site is deployed to GitHub Pages from the repository root. Generated HTML files should be committed to the repository. The `.github/workflows/static.yml` workflow may handle deployment automation.

## Best Practices

1. **Never modify generated HTML files directly** - always edit source Markdown files
2. **Test the build script** after any changes to templates or scripts
3. **Keep dependencies up to date** but test thoroughly
4. **Maintain backward compatibility** in the build process
5. **Document any new environment variables** in this file
6. **Follow existing code style** in scripts and HTML/CSS
7. **Validate Markdown** before committing
8. **Check file permissions** on shell scripts (should be executable)

## Security Considerations

- The build script uses `sudo` for system package installation
- Only run the build script in trusted environments
- Review any new dependencies for security vulnerabilities
- Keep npm packages updated for security patches

## Getting Help

- Project README: `blog/README.md`
- Build script documentation: See comments in `blog/scripts/build.sh`
- Report issues on GitHub Issues

## Notes for Copilot

- When generating Markdown content, follow the existing post structure
- Shell scripts should handle both local and CI environments
- Prefer minimal changes to the build system
- Test generated HTML for proper structure and CSS class usage
- Respect the existing template variable patterns used by Pandoc
