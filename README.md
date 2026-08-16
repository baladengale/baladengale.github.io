# bala.dengale — personal site + blog

Personal website of **Bala Dengale** — Lead Systems Engineer & Platform Architect at Visa.
Agentic AI platforms, large-scale Kubernetes, and enterprise automation — plus the
outdoor life beyond the terminal. Zero-dependency static site; the blog is plain
Markdown rendered by a stdlib-only Python builder.

## Where it lives

| URL | What it is |
|---|---|
| **https://baladengale.com** | Canonical site (GitHub Pages custom domain, HTTPS) |
| **https://baladengale.is-a.dev** | Full mirror, auto-synced on every deploy |
| https://baladengale.github.io | Redirects to `baladengale.com` (default GitHub behaviour) |
| https://baladengale.blogspot.com | Legacy external blog (older posts — linked from Life + one post) |
| http://localhost:8090 | Local preview via Docker (`baladengale-site` image) |

External profiles linked in the nav/footer: [GitHub](https://github.com/baladengale),
[LinkedIn](https://www.linkedin.com/in/baladengale),
[Facebook](https://www.facebook.com/balasaheb.dengale), email `dengalebr@gmail.com`.

## Project structure

```
baladengale.github.io/
├── site/                        ← the entire website (deploy root)
│   ├── index.html               ← home: hero, agentic-AI flagship, skills grid
│   ├── workex.html              ← work experience timeline + certifications
│   ├── life.html                ← "Beyond the terminal": family, hobbies, gallery
│   ├── build.py                 ← blog builder (posts/*.md → blog/*.html + posts.json)
│   ├── posts/                   ← blog posts in Markdown (source of truth)
│   │   └── _TEMPLATE.md         ← 📝 START HERE to write a new post
│   ├── blog/                    ← GENERATED — listing, posts, posts.json (don't hand-edit)
│   └── assets/
│       ├── css/style.css        ← design tokens, layout, dark/light themes
│       ├── js/main.js           ← theme toggle, hamburger nav, lightbox, home feed
│       └── img/                 ← avatar.jpg, family.jpg, gallery/ (curated)
├── spec/                        ← docs: site-spec, architecture, guidelines
├── deploy/                      ← Kubernetes manifests + nginx conf (see deploy/README.md)
├── Dockerfile                   ← build (python) → serve (nginx:alpine), healthcheck
├── .github/workflows/static.yml ← deploy pipeline (Pages + is-a.dev mirror sync)
├── profile/                     ← resume PDF (Bala Dengale 2025) — not part of the site build
└── photos/                      ← local-only originals (gitignored — never committed)
```

## Documentation

- [spec/site-spec.md](spec/site-spec.md) — **what** the site is: pages, theming, typography, blog engine.
- [spec/architecture.md](spec/architecture.md) — **how** it's built, rendered, and deployed.
- [spec/guidelines.md](spec/guidelines.md) — the **rules** to follow on every change.
- [site/posts/_TEMPLATE.md](site/posts/_TEMPLATE.md) — blog post template (the full voice/format guide).

The short version: hand-rolled HTML/CSS/JS, dark-by-default theming via CSS custom
properties (breakpoints at 768px + 640px), and a Markdown blog engine that builds a
Contents box, reading time, tags, and excerpts automatically. Full spec in `spec/site-spec.md`.

## Writing a new blog post

```bash
# 1. Start from the template (keep the filename date == the date: field)
cp site/posts/_TEMPLATE.md site/posts/$(date +%F)-my-post-slug.md

# 2. Write: edit front-matter (title/subtitle/date/tags/draft) + Markdown body
#    (set draft: false when ready to publish)

# 3. Preview locally
cd site && python3 build.py && python3 -m http.server   # → http://localhost:8000

# 4. Publish — commit the .md AND the regenerated blog/ output
git add site/posts site/blog && git commit -m "blog: my post title" && git push
```

Posts appear on `/blog/`, and the newest three show on the home page automatically.
Full writing guidelines live in [spec/guidelines.md](spec/guidelines.md) and the template.

## Running locally (Docker)

```bash
docker build -t baladengale-site .
docker run -d -p 8090:8080 --name bala-site baladengale-site
# → http://localhost:8090   (healthcheck at /healthz)
```

Prefer a local Kubernetes (kind) deploy with gateway routing? See [deploy/README.md](deploy/README.md).

## Conventions

- **Cache-busting**: bump `?v=YYYY.MM.DDx` in all four source templates — `build.py`,
  `index.html`, `workex.html`, `life.html` — when CSS/JS changes, then rebuild the blog.
- Curated images live in `site/assets/img/`; raw originals in `photos/` are gitignored.
- No client-side build step — edit, build blog, commit, push. That's the whole loop.
  See [spec/guidelines.md](spec/guidelines.md) for the rest.
