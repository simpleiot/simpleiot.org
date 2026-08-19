# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

The public website for [Simple IoT](https://github.com/simpleiot/simpleiot)
(simpleiot.org), a static site built with [Zola](https://www.getzola.org/). It
is a git submodule of the parent repo at `/scratch/simpleiot/siot` (gitdir lives
in `../.git/modules/simpleiot.org`).

The project documentation is a separate site (docs.simpleiot.org) generated
from the `docs/` directory of the main simpleiot repository — doc content does
not live here.

## Commands

```sh
zola serve    # dev server at http://127.0.0.1:1111 with live reload
zola build    # build to public/ (gitignored)
zola check    # validate internal/external links and templates
```

`source envsetup.sh` provides `siot_web_serve` / `siot_web_build` /
`siot_web_check` wrappers plus `siot_web_deploy`, which builds and rsyncs
`public/` to `bec-systems.com:/srv/http/siot/website/`. Do not deploy unless
asked.

There is no package manager, test suite, or external theme — Zola is the only
dependency. Prettier config (80 cols, `proseWrap: always`) applies to markdown.

## Architecture

Standard Zola layout; the non-obvious parts:

- **`config.toml` `[extra]`** holds every external URL used by the site
  (GitHub, docs, forum, YouTube, newsletter, godoc, contact email). Templates
  reference these as `config.extra.*` — add/change links there, not inline in
  templates.
- **Landing page**: `content/_index.md` is frontmatter only; all landing-page
  content is authored directly in `templates/index.html` (hero, feature
  sections, quickstart). The quickstart code shown there comes from
  `static/snippets/`.
- **Videos page**: `templates/videos.html` fetches the Simple IoT YouTube
  channel's RSS feed via `load_data()` at build time (channel ID from
  `config.extra.youtube_channel_id`). New videos appear only on rebuild, and
  building requires network access; the template degrades gracefully
  (`required=false`) when the feed is unavailable.
- **Styling**: single SCSS bundle at `sass/main.scss`, compiled by Zola. Custom
  dark theme (orange `#ff6600` accent on near-black slate, from the sIoT logo);
  all colors are SCSS variables at the top of the file.
- **Logo**: `scripts/gen-logo.py` regenerates the logo SVGs in `static/images/`
  from Fira Code glyph outlines (fontTools): the `[siot]` wordmark (wide for
  the header, square for og:image) and a `[s]` icon for favicons. Its
  docstring has the `rsvg-convert` commands for the PNG/favicon derivatives.
- **Blog**: `content/blog/`, filenames prefixed `YYYY-MM-DD-slug.md`, TOML
  frontmatter with `date` and `[taxonomies] tags`. The `tags` taxonomy and the
  blog section both generate Atom feeds.
- **Queued posts**: `content-wip/` holds finished posts scheduled for future
  dates. Zola only scans `content/`, so nothing there builds or reaches the
  Atom feed. Publishing a post means moving its file into `content/blog/` on
  (or after) the date in its frontmatter, then building and deploying.
