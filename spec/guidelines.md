# Guidelines — bala.dengale

High-level rules to keep the site consistent. Follow these on every change. Sibling docs:
[site-spec](site-spec.md) · [architecture](architecture.md).

## Writing a blog post

Start from the template — [site/posts/_TEMPLATE.md](../site/posts/_TEMPLATE.md) carries the
full voice, structure, and formatting conventions. Quick loop:

```bash
cp site/posts/_TEMPLATE.md site/posts/$(date +%F)-my-post-slug.md
# edit front-matter + Markdown body; set draft: false when ready
cd site && python3 build.py && python3 -m http.server   # → http://localhost:8000
git add site/posts site/blog && git commit -m "blog: my post title" && git push
```

Rules that keep posts consistent:

- **Voice**: first person, hands-on, honest. War stories > vendor decks.
- **Hook**: open with why the post exists and what the reader walks away with.
- **Structure**: 3–6 `##` sections max — h2s auto-build the Contents box (needs ≥3).
- **Rhythm**: short paragraphs (2–4 lines). One idea per paragraph.
- **Emphasis**: `**bold**` for key claims, `` `code` `` for tools/commands,
  `>` blockquotes for pull-quotes, `---` before the sign-off.
- **Close**: end with the italic sign-off line (see the template).

## Editing an existing page

- Pages are hand-written HTML: `site/index.html`, `site/workex.html`, `site/life.html`.
- Edit inside `<main>`; keep the shared header/footer/nav identical across pages.
- Use the CSS custom properties (`var(--accent)`, etc.) — never hard-code colors.

## Adding a new page

1. Copy `site/life.html` (or the smallest page) as a skeleton.
2. Add the nav entry in **`site/build.py` → `nav()`** (it renders the nav for all pages),
   and mirror the link in the three hand-written pages' own nav markup.
3. Add the page to the deploy path — no other wiring needed (static hosting).

## Images

- **Curated images** live in `site/assets/img/` (deployed). Use `/assets/img/...` paths.
- **Raw originals** live in `photos/` — gitignored, never committed.
- Compress/resize before adding; keep gallery images small.

## Cache-busting

- Bump `?v=YYYY.MM.DDx` in all four source templates — `site/build.py`, `index.html`,
  `workex.html`, `life.html` — whenever CSS or JS changes, then rebuild the blog.

## Commit & deploy

- Commit both the source **and** the regenerated `blog/` output.
- Push to `main` → GitHub Actions deploys to `baladengale.com` **and** mirrors to
  `baladengale.is-a.dev` in one go.

## Do / Don't

| Do | Don't |
|---|---|
| Rebuild the blog after any `posts/` change | Hand-edit anything under `blog/` (it's generated) |
| Edit CSS via `:root` tokens | Hard-code colors or sizes inline |
| Keep one idea per paragraph | Commit raw originals from `photos/` |
| Bump `?v=` on asset changes | Add frameworks / npm / build tooling |
| Match the existing page's structure | Drift the nav across pages |
