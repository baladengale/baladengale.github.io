# Architecture — bala.dengale

How the site is built, rendered, and deployed. Sibling docs:
[site-spec](site-spec.md) · [guidelines](guidelines.md).

## Repository layout

```
baladengale.github.io/
├── site/                        ← the entire website (deploy root)
│   ├── index.html               ← home (hand-written)
│   ├── workex.html              ← work experience (hand-written)
│   ├── life.html                ← "Beyond the terminal" (hand-written)
│   ├── build.py                 ← blog builder (posts/*.md → blog/*)
│   ├── posts/                   ← blog source of truth (Markdown + front-matter)
│   ├── blog/                    ← GENERATED (post pages, index, posts.json)
│   └── assets/                  ← css/style.css, js/main.js, img/*
├── spec/                        ← this doc suite (site-spec, architecture, guidelines)
├── deploy/                      ← Kubernetes manifests + nginx conf (kind deploys)
├── Dockerfile                   ← python build → nginx serve (container image)
├── .github/workflows/static.yml ← Pages deploy + is-a.dev mirror sync
├── profile/                     ← resume PDF (not part of the site build)
└── photos/                      ← local-only image originals (gitignored)
```

## Rendering pipeline

```
posts/*.md ──build.py──▶ blog/<slug>/index.html   (one page per post)
                        └▶ blog/index.html        (regenerated listing)
                        └▶ blog/posts.json        (manifest for the home feed)
```

`site/build.py` (stdlib-only Python 3) does four things:

1. **`parse_post`** — reads front-matter (`title/subtitle/date/tags/draft`), derives the
   slug from the filename (drops the `yyyy-mm-dd-` prefix), computes reading time.
2. **`render_markdown`** — a minimal Markdown → HTML renderer (headings, code, lists,
   blockquotes, tables, inline bold/italic/code/links/images).
3. **`page` / `post_page`** — wraps output in the shared layout (header/nav/footer/theme).
4. **Writes** the three outputs above; skips drafts and files starting with `_`.

Posts sort newest-first by `date`; the index and `posts.json` reflect that order.

## Data flow

The home page's "Latest from the blog" section fetches `blog/posts.json` at runtime and
renders the 3 newest posts. No backend — the JSON is a static file rebuilt on every deploy.

## Deployment

### GitHub Pages (primary)

`push main` → `.github/workflows/static.yml`:

1. **build** — `python3 site/build.py`, then uploads `site/` as the Pages artifact
   (so absolute paths like `/assets`, `/blog`, `/workex.html` resolve at the Pages root).
2. **mirror** — clones [`baladengale-redirect`](https://github.com/baladengale/baladengale-redirect),
   wipes it (keeping `.git` + `CNAME`), copies the built `site/`, and pushes — that repo
   serves `baladengale.is-a.dev`.
3. **deploy** — publishes the artifact to GitHub Pages.

One push → both domains.

### Container (Docker)

`Dockerfile` is multi-stage: `python:3.12-alpine` runs `build.py`, then the static output
is copied into `nginx:1.27-alpine`. Serves on `:8080` with a `/healthz` probe; `deploy/nginx.conf`
adds gzip, pretty URLs (`/blog/<slug>` → `index.html`), and image/cache headers.

### Local Kubernetes (kind)

`deploy/README.md` documents a kind + gateway deployment serving `https://baladengale.internal`
(2-replica Deployment, ClusterIP Service, host annotation routed by kind-infra's AgentGateway).

## Domain routing

| URL | Role |
|---|---|
| `baladengale.com` | canonical (GitHub Pages custom domain, HTTPS) |
| `baladengale.is-a.dev` | full mirror (the `baladengale-redirect` repo) |
| `baladengale.github.io` | redirects to `baladengale.com` (default GitHub behaviour) |
| `baladengale.blogspot.com` | legacy external blog (older posts, linked from Life + one post) |

## Cache-busting

Static assets are versioned with `?v=YYYY.MM.DDx`. The version string lives in the four
source templates — `site/build.py` plus the three hand-written pages (`index.html`,
`workex.html`, `life.html`). Bump all four whenever CSS/JS changes.
