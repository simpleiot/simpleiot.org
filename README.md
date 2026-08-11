# simpleiot.org

Website for [Simple IoT](https://github.com/simpleiot/simpleiot), built with
[Zola](https://www.getzola.org/).

The project documentation lives separately at
[docs.simpleiot.org](https://docs.simpleiot.org), generated from the `docs/`
directory of the [simpleiot](https://github.com/simpleiot/simpleiot) repository.

## Local development

```sh
zola serve              # http://127.0.0.1:1111, live reload
zola build              # output to public/
zola check              # validate links and templates
```

`source envsetup.sh` provides `siot_web_serve`, `siot_web_build`, and
`siot_web_check` wrappers for the same commands, along with `siot_web_deploy`.

## Layout

- `config.toml` — site config, including the external URLs used across the
  templates
- `content/_index.md` — landing page (renders via `templates/index.html`)
- `content/blog/` — blog posts
- `content/community.md`, `content/videos.md` — standalone pages
- `templates/` — Tera templates (`base.html`, `index.html`, `page.html`,
  `section.html`, `videos.html`)
- `sass/main.scss` — single SCSS bundle, compiled to `main.css`
- `static/images/` — logos
- `static/snippets/` — code shown on the landing page

The videos page reads the Simple IoT YouTube channel feed at build time, so
rebuilding the site picks up new videos. The channel ID is set in `config.toml`.

## Theme

Custom dark theme built around the orange and slate of the sIoT logo. No
external theme dependency. Colors live as SCSS variables at the top of
`sass/main.scss`.

## Deploying

```sh
source envsetup.sh
siot_web_deploy
```

This builds the site and rsyncs `public/` to
`bec-systems.com:/srv/http/siot/website/`, alongside the documentation site at
`/srv/http/siot/docs/`. The build has no runtime dependencies, so any other
static host works equally well.
