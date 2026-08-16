# GitHub Copilot Instructions for baladengale.github.io

## Project Overview

Personal website + blog of Bala Dengale (Lead Systems Engineer & Platform Architect, Visa).
Agentic AI platforms, large-scale Kubernetes, and enterprise automation. A zero-dependency
static site: hand-written HTML/CSS/JS, with a plain-Markdown blog rendered by a stdlib-only
Python builder. Deploys to GitHub Pages from the `site/` directory.

Canonical docs: [`README.md`](../README.md) and [`spec/`](../spec/) (site-spec, architecture,
guidelines). When those disagree with this file, trust them.

## Repository Structure

```
./
├── site/                        # the entire website (deploy root)
│   ├── index.html               # home
│   ├── workex.html              # work experience
│   ├── life.html                # "Beyond the terminal"
│   ├── build.py                 # blog builder: posts/*.md → blog/*.html + posts.json
│   ├── posts/                   # blog source of truth (_TEMPLATE.md = start here)
│   ├── blog/                    # GENERATED output — do not hand-edit
│   └── assets/                  # css/style.css, js/main.js, img/*
├── spec/                        # site-spec, architecture, guidelines
├── deploy/                      # Kubernetes + nginx for container/kind deploys
├── Dockerfile                   # python build → nginx serve
├── .github/workflows/static.yml # Pages deploy + is-a.dev mirror sync
└── photos/                      # local-only originals (gitignored)
```

## Site Architecture

- **Static site** — no frameworks, no npm, no client-side build step.
- **Styling** — single stylesheet `site/assets/css/style.css`; design tokens as CSS
  custom properties in `:root` (dark) and `:root[data-theme="light"]`.
- **Blog** — `site/posts/*.md` are the source of truth; run `python3 site/build.py`
  to regenerate `site/blog/` (pages, index, `posts.json`). Never edit `blog/` by hand.
- **Deploy** — push to `main` → GitHub Actions builds and deploys `site/` to GitHub Pages,
  and mirrors the built site to the `baladengale-redirect` repo (serves `baladengale.is-a.dev`).

## Coding Conventions

- **HTML**: semantic HTML5, shared header/footer/nav on every page, content in `<main>`.
- **CSS**: use the existing `:root` tokens (`var(--accent)`, `var(--border)`, …); class-based
  selectors; no hard-coded colors; mobile-first; breakpoints at 768px and 640px.
- **JS**: vanilla, in `site/assets/js/main.js` (theme toggle, hamburger nav, lightbox, home feed).
- **Blog markdown**: first person, hands-on; 3–6 `##` sections; short paragraphs. See
  `site/posts/_TEMPLATE.md` for the full voice/format rules.
- **Cache-busting**: bump `?v=YYYY.MM.DDx` in `site/build.py`, `index.html`, `workex.html`,
  `life.html` whenever CSS/JS changes, then rebuild the blog.

## Common Tasks

### Adding a blog post

```bash
cp site/posts/_TEMPLATE.md site/posts/$(date +%F)-my-post-slug.md
# edit front-matter + body; set draft: false when ready
cd site && python3 build.py && python3 -m http.server   # preview at :8000
git add site/posts site/blog && git commit -m "blog: <title>" && git push
```

### Adding / editing a page

- Edit the hand-written HTML in `site/`; add nav entries in `site/build.py` → `nav()`
  and mirror them in the three HTML pages.

### Styling

- Edit `site/assets/css/style.css`; bump the `?v=` version string; rebuild the blog.

## Dependencies

None for production: stdlib Python 3 for the blog build, vanilla HTML/CSS/JS for the site.
No Node.js/npm.

## Best Practices

1. Keep changes minimal and consistent with the existing design.
2. Rebuild the blog (`python3 site/build.py`) after touching anything in `posts/`.
3. External links: `target="_blank" rel="noopener"`.
4. Use semantic HTML and `aria-*` for interactive elements.
5. Respect `prefers-reduced-motion`; keep the dark/light theme via CSS tokens only.
6. Don't hand-edit generated files under `site/blog/`.
