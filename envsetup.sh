#!/bin/bash

# Build and deploy script for the Simple IoT website
# Usage: source envsetup.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEPLOY_TARGET="bec-systems.com:/srv/http/siot/website/"

siot_web_deploy() {
	echo "Building site with Zola..."
	cd "$SCRIPT_DIR" || return 1
	zola build || return 1
	echo "Deploying to $DEPLOY_TARGET..."
	rsync -avz --delete public/ "$DEPLOY_TARGET"
}

siot_web_serve() {
	echo "Starting Zola development server..."
	cd "$SCRIPT_DIR" || return 1
	zola serve
}

siot_web_build() {
	echo "Building site with Zola..."
	cd "$SCRIPT_DIR" || return 1
	zola build
}

siot_web_videos() {
	echo "Updating data/videos.json from YouTube..."
	cd "$SCRIPT_DIR" || return 1
	python3 scripts/update-videos.py
}

siot_web_check() {
	echo "Checking links and templates..."
	cd "$SCRIPT_DIR" || return 1
	zola check
}

echo "Simple IoT website environment loaded."
echo "Available commands:"
echo "  siot_web_deploy - Build and deploy to $DEPLOY_TARGET"
echo "  siot_web_serve  - Start local development server"
echo "  siot_web_build  - Build the site into public/"
echo "  siot_web_videos - Update the videos list from YouTube"
echo "  siot_web_check  - Validate links and templates"
