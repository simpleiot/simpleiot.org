#!/bin/sh

# need to make a function that replaces the following links
# in markdown files:
# ![gw](gw.jpg)
# with
# ![gw](/img/projects/gw.jpg)
# but not include links like:
# ![conn](https://www.wiredwatts.com/img/products/m/pt3c6km3-1_m.jpg)

siot_projects="go hw fw"

siot_find_images() {
  for p in $siot_projects; do
    for f in "docs/$p/"*.md; do
      echo "processing: $f"
    done
  done
}

siot_update_docs() {
  img_dest=static/img/projects
  rm -rf docs/go docs/hw docs/fw "img_dest"
  for project in $siot_projects; do
    src=projects/$project/docs
    dest=docs/$project
    mkdir "$dest"
    mkdir "$img_dest"
    cp "$src"/*.md "$dest/"
    cp "$src"/*.png "$img_dest"
    cp "$src"/*.jpg "$img_dest"
  done
}
