siot_update_docs() {
  rm -rf docs/go docs/hw docs/fw
  cp -a simpleiot/docs docs/go
  cp -a hardware/docs docs/hw
  cp -a firmware/docs docs/hw
}
