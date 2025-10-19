# baladengale-markdown-site (blog/)

This repository contains a small markdown-based website whose source (content, templates and build script) is located in the `blog/` directory. The generated site is written directly into the repository root (the parent directory of `blog/`) by default.

The site is a simple personal site with a homepage, blog listing and an about page. The repository includes a template, CSS and a tiny build script that converts Markdown to HTML using pandoc.

## Current layout

Top-level repo layout (important parts):

```
./
├── blog/                 # Source: content, templates, scripts
│   ├── content/
│   ├── posts/
│   ├── templates/
│   └── scripts/build.sh  # Build script for the site source
├── (generated HTML files placed directly here by the build script)
└── .git/
```

## Build instructions

All site sources live under `blog/`. The build script is `blog/scripts/build.sh` and it:

- Resolves content/templates relative to the `blog/` directory.
- By default writes generated HTML files directly to the repo root (one level above `blog/`).
- Will attempt to install missing tools automatically:
  - `pandoc`: tries `apt-get` then falls back to downloading a prebuilt tarball and installing the binary to `/usr/local/bin`.
  - `npm`: runs `npm ci` or `npm install` if `npm` is present. If `npm` isn't available it will try `apt-get install` (best-effort).
- Safely re-executes with `bash` if invoked with `sh` so the script's safety flags work across shells.

Typical usage (from repo root):

```bash
chmod +x blog/scripts/build.sh
./blog/scripts/build.sh
```

To override the output directory (for example to build to `/tmp/site-output`):

```bash
OUTPUT_DIR=/tmp/site-output ./blog/scripts/build.sh
```

Notes:
- The script uses `sudo` for system package installs and copying the pandoc binary to `/usr/local/bin` when necessary. Make sure the environment allows `sudo` if you rely on the auto-install behavior.
- If you prefer not to auto-install anything, ensure `pandoc` and `npm` are installed beforehand and the build will proceed without attempting installs.

## Development

- Edit Markdown files in `blog/content/` and `blog/posts/`.
- Edit `blog/templates/layout.html` and `blog/assets/css/styles.css` to change look and feel.

## License

This project is licensed under the MIT License. See the top-level `LICENSE` file for details.

## Acknowledgments

Inspired by the original site design (adapted for Bala Dengale).