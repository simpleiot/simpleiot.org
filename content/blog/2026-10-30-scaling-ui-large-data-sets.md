+++
title = "Scaling the UI to large data sets"
description = "Simple IoT uses its tree structure to load and watch only the nodes on screen, so a browser can work with very large data sets."
date = 2026-10-30
[taxonomies]
tags = ["ui"]
+++

How do you show thousands of devices in a browser without loading them all?
Pagination loads a page at a time as you scroll. Search loads only the matches.
Simple IoT takes a third approach and follows the structure of the data: the
system is a tree of nodes, so the UI loads a node when you expand it and watches
only the nodes on screen.

The [video demo](https://youtu.be/nTNtVRTNRHQ) shows this with two browser
windows open on one instance. It starts by importing
[`large-tree.yaml`](https://github.com/simpleiot/simpleiot/blob/master/testdata/large-tree.yaml),
a test data set of 1,457 nodes that reaches 50 levels deep:

```sh
siot import < testdata/large-tree.yaml
```

The browser debugger in the right window shows the WebSocket messages arriving
over NATS. When we edit a node in the left window, here is what the right window
receives:

- **Node on screen:** a message arrives right away and the value updates.
- **Node collapsed or never expanded:** no messages arrive.
- **Node expanded again:** the UI fetches it and shows the latest value.

Interest drives the data flow. Expanding a node says you want to see it, so the
UI fetches that node's children and subscribes to the nodes on screen.
Collapsing a node ends those subscriptions. The browser's work follows what you
are viewing, so it stays small even as the tree grows.

The tree does this work for us. Every SIOT system already has this structure, so
the UI needs no separate paging or caching scheme. The
[frontend reference](https://docs.simpleiot.org/docs/ref/frontend.html) covers
the details.

Thoughts, questions, feedback,
[let me know](https://community.tmpdir.org/c/simple-iot/5).
