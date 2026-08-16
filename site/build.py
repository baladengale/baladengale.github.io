#!/usr/bin/env python3
"""
Blog build system for bala.dengale
==================================
Standard, dependency-free pipeline for blog posts.

How to write a new post:
  1. Copy  posts/_TEMPLATE.md  to  posts/<yyyy-mm-dd>-<slug>.md
  2. Fill in the YAML-ish front-matter (title, subtitle, date, tags, draft)
     and write the body in Markdown.
  3. Run:  python3 build.py
     -> site/blog/<slug>/index.html   (the rendered post)
     -> site/blog/index.html          (regenerated listing)
     -> site/blog/posts.json          (manifest used by the home page)

Supported markdown: ATX headings, fenced code blocks, inline code,
bold/italic, links, images, ordered/unordered lists, blockquotes,
pipe tables, horizontal rules and paragraphs.
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent          # .../site
POSTS_DIR = ROOT / "posts"
BLOG_DIR = ROOT / "blog"
TEMPLATE = (POSTS_DIR / "_TEMPLATE.md").read_text()

# ---------------------------------------------------------------------------
# Front-matter parsing (simple KEY: value pairs, 'tags' as comma-separated)
# ---------------------------------------------------------------------------

def parse_post(path: Path):
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    if text.startswith("---"):
        # closing delimiter must be a line that is exactly "---" (so that
        # horizontal rules inside the body don't confuse the split)
        lines = text.split("\n")
        try:
            end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
        except StopIteration:
            end = -1
        if end > 0:
            fm, body = "\n".join(lines[1:end]), "\n".join(lines[end + 1:])
            for line in fm.strip().splitlines():
                if ":" in line:
                    k, v = line.split(":", 1)
                    v = v.strip()
                    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
                        v = v[1:-1]
                    meta[k.strip().lower()] = v
            body = body.lstrip("\n")
    slug = path.stem
    m = re.match(r"^\d{4}-\d{2}-\d{2}-(.+)$", slug)
    if m:
        slug = m.group(1)
    meta.setdefault("title", slug.replace("-", " ").title())
    meta.setdefault("subtitle", "")
    meta.setdefault("date", "")
    meta.setdefault("tags", "")
    meta.setdefault("draft", "false")
    meta["slug"] = slug
    meta["tags_list"] = [t.strip() for t in meta["tags"].split(",") if t.strip()]
    meta["reading_minutes"] = max(1, round(len(body.split()) / 200))
    return meta, body


# ---------------------------------------------------------------------------
# Minimal markdown renderer
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline(s: str) -> str:
    s = esc(s)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", r'<img src="\2" alt="\1">', s)
    s = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", r'<a href="\2" target="_blank" rel="noopener">\1</a>', s)
    s = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"\*([^*]+)\*", r"<em>\1</em>", s)
    return s


def render_markdown(md: str) -> str:
    lines = md.split("\n")
    out, i = [], 0
    while i < len(lines):
        line = lines[i]

        # fenced code block
        if line.startswith("```"):
            lang = line[3:].strip()
            code = []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                code.append(esc(lines[i]))
                i += 1
            cls = f' class="language-{lang}"' if lang else ""
            out.append(f"<pre><code{cls}>\n" + "\n".join(code) + "\n</code></pre>")
            i += 1
            continue

        # horizontal rule
        if re.match(r"^-{3,}$", line.strip()):
            out.append("<hr>")
            i += 1
            continue

        # heading
        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            level = len(m.group(1))
            text = inline(m.group(2))
            hid = re.sub(r"[^a-z0-9]+", "-", m.group(2).lower()).strip("-")
            out.append(f'<h{level} id="{hid}">{text}</h{level}>')
            i += 1
            continue

        # blockquote
        if line.startswith(">"):
            quote = []
            while i < len(lines) and lines[i].startswith(">"):
                quote.append(lines[i].lstrip("> ").rstrip())
                i += 1
            out.append("<blockquote><p>" + inline(" ".join(quote)) + "</p></blockquote>")
            continue

        # table
        if "|" in line and i + 1 < len(lines) and re.match(r"^\s*\|[-\s:|]+\|[-\s:|]*$", lines[i + 1]):
            header = [c.strip() for c in line.strip().strip("|").split("|")]
            i += 2
            rows = []
            while i < len(lines) and "|" in lines[i] and lines[i].strip():
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            thead = "".join(f"<th>{inline(c)}</th>" for c in header)
            tbody = "".join("<tr>" + "".join(f"<td>{inline(c)}</td>" for c in r) + "</tr>" for r in rows)
            out.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        # lists
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+", line)
        if m:
            ordered = m.group(2) != "-" and m.group(2) != "*"
            items = []
            while i < len(lines):
                li = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if not li:
                    if lines[i].strip() and items and lines[i].startswith(("  ", "\t")):
                        items[-1] += " " + lines[i].strip()  # continuation line
                        i += 1
                        continue
                    break
                items.append(li.group(3).strip())
                i += 1
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(f"<li>{inline(it)}</li>" for it in items) + f"</{tag}>")
            continue

        # paragraph
        if line.strip():
            para = [line.strip()]
            i += 1
            while i < len(lines) and lines[i].strip() and not re.match(
                r"^(#{1,4}\s|```|>|\s*([-*]|\d+\.)\s|-{3,}$)", lines[i]
            ) and "|" not in lines[i]:
                para.append(lines[i].strip())
                i += 1
            out.append("<p>" + inline(" ".join(para)) + "</p>")
            continue

        i += 1
    return "\n".join(out)


def build_toc(html: str) -> str:
    heads = re.findall(r'<h2 id="([^"]+)">(.*?)</h2>', html)
    if len(heads) < 3:
        return ""
    items = "".join(f'<li><a href="#{hid}">{txt}</a></li>' for hid, txt in heads)
    return f'<div class="toc"><h4>Contents</h4><ul>{items}</ul></div>'


# ---------------------------------------------------------------------------
# Layout
# ---------------------------------------------------------------------------

def nav(active: str) -> str:
    links = [("Home", "/"), ("Work Experience", "/workex.html"), ("Blog", "/blog/"), ("Life", "/life.html")]
    items = "".join(
        f'<li><a href="{href}"{" class=\"active\"" if label == active else ""}>{label}</a></li>'
        for label, href in links
    )
    return items + """
      <li><a href="https://github.com/baladengale" target="_blank" rel="noopener">GitHub</a></li>
      <li><a href="https://www.linkedin.com/in/baladengale" target="_blank" rel="noopener">LinkedIn</a></li>"""


THEME_SCRIPT = ("<script>document.documentElement.setAttribute('data-theme',"
                "(function(){try{return localStorage.getItem('theme')||'dark'}"
                "catch(e){return 'dark'}})());</script>")


def page(title: str, active: str, body: str, description: str = "") -> str:
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="description" content="{description}">
  <title>{title}</title>
  <link rel="stylesheet" href="/assets/css/style.css?v=2026.08.16c">
  <link rel="icon" href="data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 100'><text y='.9em' font-size='90'>⌘</text></svg>">
  {THEME_SCRIPT}
</head>
<body>
<header class="site-header">
  <nav class="site-nav container">
    <a class="brand" href="/">bala<span>.</span>dengale</a>
    <div class="nav-right">
      <ul>{nav(active)}</ul>
      <button class="theme-toggle" id="theme-toggle" aria-label="Toggle light and dark theme" title="Toggle light / dark">
        <span class="icon-sun">☀️</span><span class="icon-moon">🌙</span>
      </button>
    </div>
  </nav>
</header>
{body}
<footer class="site-footer">
  <div class="container inner">
    <div>© <span class="yr"></span> Bala Dengale · It's just you, me, and the code.</div>
    <div class="links">
      <a href="mailto:dengalebr@gmail.com">dengalebr@gmail.com</a>
      <a href="https://github.com/baladengale" target="_blank" rel="noopener">GitHub</a>
      <a href="https://www.linkedin.com/in/baladengale" target="_blank" rel="noopener">LinkedIn</a>
      <a href="https://www.facebook.com/balasaheb.dengale" target="_blank" rel="noopener">Facebook</a>
    </div>
  </div>
</footer>
<script src="/assets/js/main.js?v=2026.08.16c"></script>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Generators
# ---------------------------------------------------------------------------

def post_page(meta: dict, body_html: str) -> str:
    date_fmt = ""
    if meta["date"]:
        try:
            date_fmt = datetime.strptime(meta["date"], "%Y-%m-%d").strftime("%B %-d, %Y")
        except ValueError:
            date_fmt = meta["date"]
    tags = "".join(f'<span class="tag-sm">{t}</span>' for t in meta["tags_list"])
    body = f"""
<main>
  <article>
    <header class="post-header container">
      <div class="meta">
        <span>{date_fmt}</span><span class="dot" style="color:var(--border)">•</span>
        <span>{meta['reading_minutes']} min read</span><span style="color:var(--border)">•</span>
        <span>Bala Dengale</span>
      </div>
      <h1>{esc(meta['title'])}</h1>
      {f'<p class="subtitle">{esc(meta["subtitle"])}</p>' if meta['subtitle'] else ''}
      <div class="tag-row">{tags}</div>
    </header>
    <div class="article container">
      {build_toc(body_html)}
      {body_html}
    </div>
    <div class="post-footer container">
      <a class="btn btn-ghost" href="/blog/">← All posts</a>
      <a class="btn btn-primary" href="mailto:dengalebr@gmail.com?subject=Re: {meta['title']}">Discuss this post</a>
    </div>
  </article>
</main>"""
    return page(f"{meta['title']} — Bala Dengale", "Blog", body, meta["subtitle"] or meta["title"])


def blog_index_page(posts: list) -> str:
    cards = []
    for p in posts:
        tags = "".join(f'<span class="tag-sm">{t}</span>' for t in p["tags_list"])
        date_fmt = datetime.strptime(p["date"], "%Y-%m-%d").strftime("%b %-d, %Y") if p["date"] else ""
        cards.append(f"""
      <a class="post-card" href="/blog/{p['slug']}/">
        <div class="meta"><span>{date_fmt}</span><span class="dot">•</span><span>{p['reading_minutes']} min read</span><span class="dot">•</span>{tags}</div>
        <h2>{esc(p['title'])}</h2>
        <p class="excerpt">{esc(p['excerpt'])}</p>
      </a>""")
    body = f"""
<main class="container">
  <section class="page-head">
    <h1>AI and I</h1>
    <p>It's just you, me, and the code. My personal experiments with the future of tech —
       migrated from <a href="https://baladengale.blogspot.com">baladengale.blogspot.com</a> and continued here.
       Written by a human; occasionally fact-checked by agents I built.</p>
  </section>
  <section class="post-list">{''.join(cards)}</section>
</main>"""
    return page("Blog — Bala Dengale", "Blog", body, "AI and I — the blog of Bala Dengale")


def main():
    if not POSTS_DIR.exists():
        sys.exit("posts/ directory not found")

    posts = []
    for md_file in sorted(POSTS_DIR.glob("*.md")):
        if md_file.name.startswith("_"):
            continue
        meta, body = parse_post(md_file)
        if meta["draft"].lower() == "true":
            print(f"  skipping draft: {md_file.name}")
            continue
        html = render_markdown(body)
        out_dir = BLOG_DIR / meta["slug"]
        out_dir.mkdir(parents=True, exist_ok=True)
        (out_dir / "index.html").write_text(post_page(meta, html), encoding="utf-8")
        # excerpt: first non-heading, non-list paragraph of the body (joined
        # across wrapped lines), truncated at a word boundary
        para, collecting = [], False
        for l in body.splitlines():
            stripped = l.strip()
            if not stripped:
                if collecting: break
                continue
            if stripped.startswith(("#", ">", "```", "|", "- ", "* ", "1.")):
                if collecting: break
                continue
            collecting = True
            para.append(stripped)
        excerpt = " ".join(para)
        if len(excerpt) > 200:
            cut = excerpt[:200].rsplit(" ", 1)[0]
            excerpt = re.sub(r"[.,;:—-]+$", "", cut) + "…"
        meta["excerpt"] = excerpt
        posts.append(meta)
        print(f"  built: blog/{meta['slug']}/index.html  ({meta['title']})")

    # newest first
    posts.sort(key=lambda p: p["date"], reverse=True)

    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    (BLOG_DIR / "index.html").write_text(blog_index_page(posts), encoding="utf-8")
    (BLOG_DIR / "posts.json").write_text(json.dumps(posts, indent=2), encoding="utf-8")
    print(f"  built: blog/index.html, blog/posts.json  ({len(posts)} posts)")


if __name__ == "__main__":
    print("Building blog…")
    main()
    print("Done.")
