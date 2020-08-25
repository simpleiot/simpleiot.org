#!/bin/sh

# need to make a function that replaces the following links
# in markdown files:
# ![gw](gw.jpg)
# with
# ![gw](/img/projects/gw.jpg)
# but not include links like:
# ![conn](https://www.wiredwatts.com/img/products/m/pt3c6km3-1_m.jpg)

siot_projects="go hw fw"

siot_find_md_files() {
  for p in $siot_projects; do
    for f in "docs/$p/"*.md; do
      ret="${ret} ${f}"
    done
  done
  echo "$ret"
}

siot_update_image_links() {
  file=$1
  project=$(echo "$1" | sed 's/docs\/\(.*\)\/.*/\1/')
  echo "project: $project"
  # FIXME this is still replacing all links, even external
  sed -i "s/\(!\[.*\]\)(\(.*\))/\1(\/img\/projects\/${project}\/\2)/g" "$file"
}

siot_update_docs() {
  echo "updating docs"
  img_dest=static/img/projects
  rm -rf docs/go docs/hw docs/fw "img_dest"
  for project in $siot_projects; do
    src=projects/$project/docs
    dest=docs/$project
    mkdir "$dest"
    mkdir -p "$img_dest/$project"
    cp "$src"/*.md "$dest/"
    cp "$src"/*.png "$img_dest/$project"
    cp "$src"/*.jpg "$img_dest/$project"
  done

  md_files=$(siot_find_md_files)
  echo "updating links in files $md_files"
  for f in $md_files; do
    echo "processing $f"
    siot_update_image_links "$f"
  done
}
