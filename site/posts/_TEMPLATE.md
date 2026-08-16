---
title: Your Post Title Here
subtitle: A one-line subtitle that hooks the reader (optional)
date: 2026-08-16
tags: ai, kubernetes, experiments
draft: true
---

<!--
  ============================================================
  BLOG POST TEMPLATE — "The Human in the Loop"
  ============================================================
  HOW TO USE
  1. Copy this file to:  posts/<yyyy-mm-dd>-<slug>.md
       e.g.  posts/2026-08-16-my-agents-in-prod.md
       The <slug> becomes the URL (/blog/<slug>/); keep the filename
       date equal to the date: field below (they sort/route together).
  2. Fill the front-matter above:
       title     - shown on the post, blog list and home page
       subtitle  - optional italic strapline under the title
       date      - YYYY-MM-DD (posts sort newest first)
       tags      - comma-separated, rendered as chips
       draft     - true hides the post from the build entirely
  3. Delete this comment block and write your content below.
  4. Preview:  cd site && python3 build.py && python3 -m http.server
  5. Publish:  commit + push to main (both domains deploy automatically)

  WRITING GUIDELINES (keep the blog consistent)
  - Voice: first person, hands-on, honest. War stories > vendor decks.
  - Hook: open with why this post exists and what the reader walks away with.
  - Structure: 3-6 "##" sections max; h2s auto-build the Contents box.
  - Rhythm: short paragraphs (2-4 lines). One idea per paragraph.
  - Emphasis: **bold** for key claims, `code` for tools/commands,
    > blockquotes for pull-quotes, --- before the sign-off.
  - Close: end with the italic sign-off line (see bottom of this file).

  MARKDOWN SUPPORTED (all optional)
    # .. ####        headings          **bold**  *italic*  `inline code`
    [links](https://...)  ![images](/assets/img/foo.png)
    - bullets   1. numbered   > quotes   --- rule
    | Tables | work |      ```python  fenced code with language hint  ```
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
