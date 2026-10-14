+++
title = "Real-time edge-to-browser connectivity"
description = "Simple IoT now streams device state from the edge to the browser in real time over NATS, with offline queuing when the connection drops."
date = 2026-10-13
[taxonomies]
tags = ["sync", "ui", "release"]
+++

Have you ever wanted to see the state of your remote devices in real time,
without lag, spinners, or stale check-ins? Simple IoT now has real-time
connectivity from edge to browser based on [NATS](https://nats.io/), which is a
high-performance, lightweight, open-source messaging system. This allows for
rich, efficient interaction with remote devices, where remote state updates
instantly and configuration changes take effect right away.

In the demo below, we have SIOT running on a Raspberry Pi 5 connected to another
SIOT running on a cloud server.

![Demo setup: a Raspberry Pi 5 with a push button and LED syncs to the siot3 server, and a browser connects to both over NATS WebSocket](/images/blog/realtime-edge-to-browser-setup.svg)

The [video demo](https://youtu.be/lqM4MPVNHsc) walks through how this works.

A rule on the server watches a push button on the Pi 5 and then turns on an LED
when the button is pressed. This demonstrates a round trip of data from the Pi 5
switch, to the server, through the rules, and then back to the Pi 5 LED. The LED
lights nearly instantaneously when the button is pressed. The round trip is
barely perceptible, roughly 100 ms.

If the connection drops, NATS JetStream queues data at both ends, and
functionality resumes nearly instantly once the connection returns.

The NATS project is what makes this possible. NATS provides essential bits like
JetStream that allows efficient synchronization between systems, and web client
libraries that push data efficiently to the browser in real time.

SIOT models the entire system as a tree of nodes where each node is a set of
points. Telemetry, IoT data, and configuration are all just points and are
handled the same way. Write a point, and SIOT synchronizes it wherever it needs
to go. This simplicity allows SIOT to efficiently synchronize data from a fleet
of devices to your browser and makes it straightforward to extend with custom
functionality for just about any application.
