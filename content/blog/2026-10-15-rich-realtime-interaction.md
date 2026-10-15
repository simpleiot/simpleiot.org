+++
title = "Rich, real-time interaction with remote devices"
description = "SIOT puts responsiveness first: current data in the portal, instant control, and rules that act immediately."
date = 2026-10-15
[taxonomies]
tags = ["sync", "ui"]
+++

While recording the
[last demo](https://simpleiot.org/blog/realtime-edge-to-browser/), I had an
insight:

**_SIOT is for people who want rich, real-time interaction with remote
devices._**

While we
[have a path to fairly low](https://docs.simpleiot.org/docs/ref/bandwidth.html#ideas)
data usage, this is not the first priority. The first priority is that when we
see data in the portal, we know it is current. When we turn on a pump remotely,
it turns on instantly. When a condition happens that causes a rule to activate,
it happens immediately, not minutes later when the system gets around to running
that rule. These priorities drive the design and architecture of SIOT. I've
spent too much time with consumer IoT technologies watching spinners spin for
tens of seconds while waiting for my garage door to close, only to be told
"something went wrong." SIOT is something different, designed for industrial
reliability and responsiveness. In that demo, a button press on a Raspberry Pi
travels to the cloud server, through a rule, and back to an LED in about 100 ms.

This focus requires some tradeoffs. You probably can't get this responsiveness
using lambda functions in a hyperscale serverless cloud system. You can't easily
scale it to a bazillion devices, or implement it with a 2 MB/month device
bandwidth budget. But the goal we are working toward is to support thousands of
devices and hundreds of users in real time with a relatively modest cloud server
running SIOT.

This is the vision. It's not for everyone or everything, but if you want a great
user experience for a connected industrial product, SIOT may be the technology
for you.
