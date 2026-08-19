"""Generate the [siot] logo assets in static/images/.

Renders "[siot]" as embedded glyph outlines (no font dependency in the
SVG) using Fira Code Medium, which matches the site's monospace stack,
in orange on black like a terminal.

Outputs:
    siot-logo.svg         wide wordmark (site header)
    siot-logo-square.svg  square wordmark (og:image / social previews)
    siot-icon.svg         square [s] icon (favicons, small sizes)

Usage:
    python scripts/gen-logo.py
    rsvg-convert -w 400 static/images/siot-logo.svg -o static/images/siot-logo.png
    rsvg-convert -w 360 -h 360 static/images/siot-logo-square.svg -o static/images/siot-logo-square.png
    rsvg-convert -w 64 -h 64 static/images/siot-icon.svg -o static/images/favicon.png

Requires fontTools and the Fira Code font (path below).
"""
from pathlib import Path

from fontTools.misc.transform import Transform
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

FONT = "/usr/share/fonts/TTF/FiraCodeNerdFont-Medium.ttf"
TEXT = "[siot]"
ORANGE = "#ff6600"
BG = "#000000"  # $bg-code in sass/main.scss

OUT = Path(__file__).resolve().parent.parent / "static" / "images"

font = TTFont(FONT)
cmap = font.getBestCmap()
glyphs = font.getGlyphSet()

def text_path(text):
    """Combined outline path, y-flipped (font coords -> SVG coords), plus bounds."""
    pen = SVGPathPen(glyphs)
    bpen = BoundsPen(glyphs)
    x = 0
    for ch in text:
        g = glyphs[cmap[ord(ch)]]
        t = Transform(1, 0, 0, -1, x, 0)
        g.draw(TransformPen(pen, t))
        g.draw(TransformPen(bpen, t))
        x += g.width
    return pen.getCommands(), bpen.bounds


def svg(path, width, height, scale, tx, ty, bg=None):
    parts = ['<?xml version="1.0" encoding="UTF-8"?>']
    parts.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" '
        f'width="{width}" height="{height}">'
    )
    if bg:
        parts.append(f'  <rect width="{width}" height="{height}" fill="{bg}"/>')
    parts.append(f'  <g transform="translate({tx:.2f}, {ty:.2f}) scale({scale:.6f})">')
    parts.append(f'    <path d="{path}" fill="{ORANGE}"/>')
    parts.append("  </g>")
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def square(path, bounds, frac):
    """360x360 square with the text scaled to frac of the width, centered."""
    xmin, ymin, xmax, ymax = bounds
    w, h = xmax - xmin, ymax - ymin
    SQ = 360
    s = (SQ * frac) / w
    tx = (SQ - w * s) / 2 - xmin * s
    ty = (SQ - h * s) / 2 - ymin * s
    return svg(path, SQ, SQ, s, tx, ty, bg=BG)


path, bounds = text_path(TEXT)
xmin, ymin, xmax, ymax = bounds
w, h = xmax - xmin, ymax - ymin


# Wide header logo on a background, normalized to 100 px tall.
pad = 0.30 * h
s = 100.0 / (h + 2 * pad)
W = round((w + 2 * pad) * s, 2)
(OUT / "siot-logo.svg").write_text(
    svg(path, W, 100, s, (pad - xmin) * s, (pad - ymin) * s, bg=BG)
)
print(f"wrote siot-logo.svg {W} x 100")

# Square wordmark for og:image / social previews.
(OUT / "siot-logo-square.svg").write_text(square(path, bounds, 0.78))
print("wrote siot-logo-square.svg 360x360")

# [s] icon for favicons — a full wordmark is unreadable at tab size.
ipath, ibounds = text_path("[s]")
(OUT / "siot-icon.svg").write_text(square(ipath, ibounds, 0.72))
print("wrote siot-icon.svg 360x360")
