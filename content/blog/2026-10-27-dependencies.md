+++
title = "Some dependencies make your life easier"
description = "Updating the NATS Go client brings more reliable recovery from dropped connections."
date = 2026-11-03
[taxonomies]
tags = ["sync", "nats"]
+++

Some dependencies cause pain when updated, and others quietly improve a system.
I noticed this in the Simple IoT changelog after a recent Go dependency update.

- **Sync and the store recover more reliably from dropped connections.** The
  NATS Go client 1.55.0 fixes deadlocks, leaks, and stalls in reconnect, drain,
  and ordered consumers, so a device on a flaky link reconnects and resumes
  cleanly.

Handling all the edge conditions of a flaky network link is indeed one of the
hard parts of IIoT systems, and it is nice when dependencies do some of this
work for us. The [NATS.io](https://nats.io/) dependencies in the Simple IoT
system are stable and are always improving. I've not encountered any problems
and update without hesitation when there are new versions available.

Simple IoT stands on the shoulders of giants to provide a reliable real-time
system for device manufacturers who want rich, real-time interaction with remote
systems.
