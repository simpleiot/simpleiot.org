+++
title = "GPIO, IIO, and Shelly device improvments"
description = "A roundup of what has landed in Simple IoT since the MQTT release, mostly around reading real hardware."
date = 2026-09-02
[taxonomies]
tags = ["release"]
+++

The [MQTT post](/blog/mqtt/) covered the 0.25 release. Several things have
landed since then, mostly around reading real hardware.

- **Read a switch or drive a relay from a GPIO line.** A `gpio` node reads or
  drives one line on a Linux GPIO character device, so a rule can watch a float
  switch and run a pump. Set the chip to `sim` to develop rules before the
  hardware exists. See the
  [GPIO client](https://docs.simpleiot.org/docs/user/gpio.html).
- **Analog IO through the Linux IIO subsystem.** An `iio` node reads ADCs, DACs,
  and the sensors the kernel presents the same way: accelerometers, pressure,
  humidity, light. Name the device and its channels are detected and added as
  children, each publishing a reading in volts, amps, or degrees Celsius. See
  the [IIO documentation](https://docs.simpleiot.org/docs/user/iio.html).
- **Shelly devices are more discoverable and efficient.** A Shelly Gen2 or later
  device answers with its own component list, so any such device works,
  including models released after this one. Status now arrives over a WebSocket
  instead of polling, so a relay switched at the wall shows up right away. See
  the [Shelly documentation](https://docs.simpleiot.org/docs/user/shelly.html).
- **Mirroring a hardware node now creates a view of it**, so only the instance
  where the node actually lives talks to the device, and a value set on the
  mirror travels back down to the hardware. See
  [primary and mirror edges](https://docs.simpleiot.org/docs/ref/data.html#primary-and-mirror-edges).
- **User passwords are stored hashed.** The store, sync streams, and exports
  carry only a bcrypt hash. Existing passwords convert the next time each user
  signs in.

## Upgrading

Node replies over NATS now use the binary point encoding instead of protobuf.
This is an incompatible wire change, so instances and devices that sync with
each other need to be upgraded together. The
[changelog](https://github.com/simpleiot/simpleiot/blob/master/CHANGELOG.md) has
the full list of changes.
