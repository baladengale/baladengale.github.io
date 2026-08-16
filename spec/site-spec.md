# Site Spec — bala.dengale

The authoritative description of what the site *is* and how it should look and behave.
Design and content changes should preserve the properties below. Sibling docs:
[architecture](architecture.md) · [guidelines](guidelines.md).

## Identity

- **Brand**: `bala.dengale` — tagline "Agentic AI · Kubernetes · Platform Engineering".
- **Owner**: Bala Dengale — Lead Systems Engineer & Platform Architect, Visa.
- **Voice**: first person, hands-on, honest. War stories over vendor decks.

## Pages

| Page | Path (source) | Purpose |
|---|---|---|
| Home | `/` — `site/index.html` | hero, agentic-AI flagship, skills grid, latest 3 posts |
| Work | `/workex.html` — `site/workex.html` | work-experience timeline + certifications |
| Life | `/life.html` — `site/life.html` | "Beyond the terminal" — family, hobbies, gallery |
| Blog index | `/blog/` — generated | "The Human in the Loop" — all posts, newest first |
| Post | `/blog/<slug>/` — generated | single blog post |

## Tech stack

- Hand-rolled HTML/CSS/JS. No frameworks, no npm, no client-side build step.
- Blog builder is dependency-free Python 3 (`site/build.py`, stdlib only).

## Theming

- Dark by default; light via the ☀️/🌙 toggle. Choice persisted in `localStorage`
  and applied pre-paint by an inline `<script>` (no flash-of-wrong-theme).
- All colors are CSS custom properties: `:root` = dark, `:root[data-theme="light"]` = light.

| Role | Dark | Light |
|---|---|---|
| background | `#0d1117` | `#f6f8fa` |
| surface / card | `#161f2b` | `#ffffff` |
| border | `#263241` | `#d8dee4` |
| accent (blue) | `#58b6ff` | `#0969da` |
| accent-2 (teal) | `#7ee0c3` | `#1a7f72` |
| accent-warm | `#ffb86b` | `#b35900` |

## Responsive

- Breakpoints: `768px` (primary — hamburger nav below, full nav above) and `640px` (refinement).
- 28px mobile gutters; card borders/shadows preserved at every viewport.
- Respects `prefers-reduced-motion`.

## Typography

- System sans for prose, mono for accents/tags/eyebrows; serif reserved for post-body flourishes.

## Blog engine

- Source of truth: `site/posts/*.md` (front-matter + Markdown).
- Front-matter fields: `title`, `subtitle` (optional), `date` (`YYYY-MM-DD`, newest-first sort),
  `tags` (comma-separated → chips), `draft` (`true` hides the post from the build).
- Filename `<yyyy-mm-dd>-<slug>.md` → URL `/blog/<slug>/`; keep the filename date == the `date:` field.
- Auto-generated per post: Contents box (needs ≥3 `##` h2s), reading time (~200 wpm),
  tag chips, excerpt (first paragraph, ~200 chars).
- `blog/posts.json` is the manifest the home page reads for "Latest from the blog".
- Markdown supported: headings, fenced code (+ language hint), inline code, bold/italic,
  links, images, ordered/unordered lists, blockquotes, pipe tables, horizontal rules.

## Accessibility & motion

- Semantic HTML5; real `<button>` elements for toggles; `aria-*` on the nav toggle.
- `prefers-reduced-motion` disables non-essential animation.
