"""Update data/videos.json with the videos on the Simple IoT YouTube channel.

The videos page is built from this file rather than YouTube's RSS feed, so
`zola build` needs no network access. Run this when a new video is posted,
then commit the result.

Videos already in the file keep their stored date; only new videos are looked
up individually for their upload date.

Usage:
    python scripts/update-videos.py

Requires yt-dlp.
"""
import json
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "videos.json"


def ytdlp(*args):
    result = subprocess.run(
        ["yt-dlp", "--ignore-config", *args],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.exit(f"yt-dlp failed:\n{result.stderr}")
    return [line.split("\t") for line in result.stdout.splitlines() if line]


def main():
    config = tomllib.loads((ROOT / "config.toml").read_text())
    channel_url = config["extra"]["youtube_url"] + "/videos"

    known = {}
    if OUT.exists():
        known = {v["id"]: v for v in json.loads(OUT.read_text())["videos"]}

    # Channel listing, newest first. Flat mode is fast but has no dates.
    listing = ytdlp(
        "--flat-playlist", "--print", "%(id)s\t%(title)s", channel_url
    )
    if not listing:
        sys.exit("No videos found; leaving data/videos.json unchanged.")

    new_ids = [vid for vid, _ in listing if vid not in known]
    dates = {}
    if new_ids:
        print(f"Looking up dates for {len(new_ids)} new video(s)...")
        urls = [f"https://www.youtube.com/watch?v={vid}" for vid in new_ids]
        for vid, date in ytdlp(
            "--skip-download", "--print", "%(id)s\t%(upload_date)s", *urls
        ):
            dates[vid] = f"{date[:4]}-{date[4:6]}-{date[6:8]}"

    videos = [
        {
            "id": vid,
            "title": title,
            "date": dates.get(vid) or known[vid]["date"],
        }
        for vid, title in listing
    ]

    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps({"videos": videos}, indent=2) + "\n")
    print(f"Wrote {len(videos)} videos to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
