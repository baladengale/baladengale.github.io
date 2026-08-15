---
title: Your Post Title Here
subtitle: A one-line subtitle that hooks the reader (optional)
date: 2026-08-15
tags: ai, kubernetes, experiments
draft: true
---

<!--
  ============================================================
  STANDARD BLOG POST TEMPLATE — "AI and I"
  ============================================================
  HOW TO USE
  1. Copy this file to:  posts/<yyyy-mm-dd>-<slug>.md
  2. Fill the front-matter above:
       title     - shown on the post, blog list and home page
       subtitle  - optional italic strapline under the title
       date      - YYYY-MM-DD (posts are sorted newest first)
       tags      - comma-separated, rendered as chips
       draft     - true hides the post from the build entirely
  3. Delete this comment block and write your content below.
  4. Run:  python3 build.py   (from the site/ directory)

  RICH CONTENT SUPPORTED (all optional):
    # .. ####        headings (h2+ auto-linked in the Contents box)
    **bold**  *italic*  `inline code`
    [links](https://...)   ![images](/assets/img/foo.png)
    - bullet lists   1. numbered lists
    > blockquotes for pull-quotes
    Tables:
      | Col A | Col B |
      |-------|-------|
      | 1     | 2     |
    Fenced code with language hint:
      ```python
      print("hello")
      ```
    ---  horizontal rule
-->

Write your opening paragraph here. One or two sentences that set up
why this post exists and what the reader will walk away with.

## First section

Body text. Use **bold** for key claims, `code` for tool names, and
links for sources.

> A pull-quote or key insight works well as a blockquote.

### Sub-section

Lists are fine too:

- Point one
- Point two
- Point three

## Code example

```python
def hello(kind: str = "cluster") -> str:
    return f"hello, {kind}"

print(hello("kubernetes"))
```

## Data

| Tool   | Verdict | Notes                  |
|--------|---------|------------------------|
| Tool A | ✅ use   | free tier, solid API   |
| Tool B | ⚠️ maybe | paid, but polished     |
| Tool C | ❌ skip  | 72% annual drag        |

---

*Thanks for reading — ping me at dengalebr@gmail.com to discuss.*
