# GitHub Copilot Instructions for baladengale.github.io

## Project Overview

This is a simple static personal website for Bala Dengale (Lead System Engineer at Visa Worldwide). The site is hosted on GitHub Pages and consists of hand-crafted HTML files with a clean, modern CSS design inspired by minimal portfolio sites.

## Repository Structure

```
./
├── index.html              # Homepage with hero section
├── about.html              # About page
├── assets/                 # Static assets
│   └── css/
│       └── styles.css      # Main stylesheet
├── blog/                   # Legacy build system (not in use)
└── .github/
    └── workflows/          # GitHub Actions workflows
```

## Site Architecture

This is a **simple static website** with:
- Hand-written HTML files (no build step required)
- Single CSS file for styling (`assets/css/styles.css`)
- External blog hosted at https://baladengale.blogspot.com/
- GitHub Pages deployment from repository root

## Coding Conventions

### File Structure

- **HTML files**: Hand-written, located in repository root
- **CSS**: Single file at `assets/css/styles.css`
- **No build process**: Edit HTML/CSS directly

### HTML Structure

- Semantic HTML5 elements
- Clean, minimal markup
- Consistent class naming conventions
- All pages share common header/footer structure

### CSS Organization

- CSS custom properties (variables) for theming
- Mobile-first responsive design
- Class-based selectors (avoid IDs for styling)
- Organized by component/section

### Design Principles

- **Minimalist aesthetic**: Clean typography, ample whitespace
- **Responsive**: Works on all screen sizes
- **Fast loading**: No frameworks, minimal dependencies
- **Accessible**: Semantic HTML, proper contrast ratios

## Dependencies

This is a dependency-free static website:
- **No build tools required**
- **No Node.js/npm needed** for production
- Pure HTML, CSS, and optional JavaScript

The `blog/` directory contains a legacy Markdown-based build system that is no longer in active use.

## Testing

This is a static site. When making changes:

1. Open HTML files directly in a browser to verify rendering
2. Check responsive design at different screen sizes
3. Validate HTML using W3C validator if needed
4. Test all navigation links work correctly

## Common Tasks

### Adding/Updating Content

1. Edit the HTML file directly (`index.html`, `about.html`, etc.)
2. Modify content within the `<main>` section
3. Keep header/footer consistent across pages
4. Test in browser

### Modifying Site Styling

1. Edit `assets/css/styles.css`
2. Use CSS custom properties (variables) defined in `:root`
3. Test responsive behavior with browser dev tools
4. Keep changes minimal and maintainable

### Adding a New Page

1. Create new HTML file in repository root
2. Copy structure from existing page (`index.html`)
3. Update navigation in header/footer of all pages
4. Add content in the `<main>` section
5. Test all navigation links

## GitHub Pages Deployment

The site is deployed to GitHub Pages from the repository root. HTML files in the root directory are served directly. No build process is required for deployment.

## Best Practices

1. **Keep it simple** - hand-edit HTML/CSS directly, no build complexity
2. **Test across devices** - verify responsive design works properly
3. **Maintain consistency** - keep header/footer/nav structure uniform across pages
4. **Follow existing code style** - match indentation and formatting
5. **Validate HTML/CSS** - use W3C validators to catch errors
6. **Optimize for speed** - minimize CSS, avoid unnecessary dependencies
7. **Keep navigation updated** - ensure all internal links work correctly

## Security Considerations

- Keep external links using `target="_blank"` with `rel="noopener"` for security
- Validate all user-facing content
- Keep dependencies minimal (currently none for production)

## Getting Help

- Project documentation: See this file and README files
- Report issues on GitHub Issues
- For questions about design: Reference the minimal, typography-focused approach

## Notes for Copilot

- When generating content, maintain the existing simple HTML structure
- Prefer minimal changes that preserve the clean, modern aesthetic
- Test generated HTML for proper structure and CSS class usage
- Respect the existing design patterns and navigation structure
- Keep external blog reference to https://baladengale.blogspot.com/
