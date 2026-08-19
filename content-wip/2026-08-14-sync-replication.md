+++
title = "Sync is now stream replication"
description = "How Simple IoT streams make catch-up sync simple and reliable."
date = 2026-08-14
[taxonomies]
tags = ["sync", "release"]
+++

The [previous post](/blog/jetstream-store/) covered moving the Simple IoT store
to NATS JetStream. This post covers how we use streams to synchronize
offline/catch-up data. There is also a
[demo of offline synchronization](https://www.youtube.com/watch?v=THmQkxWp9fo)
on the Simple IoT YouTube channel.

Offline synchronization provides several key benefits:

- Nothing is lost during network disruptions, which are a fact of life in
  distributed systems, especially edge systems.
- We can take down cloud/upstream services (including databases) at any time and
  no data is lost. This drastically simplifies operations and maintenance if we
  don't have to have always on, highly available infrastructure.

## The old way

In the past, SIOT has synchronized cloud and edge instances using a Merkle-style
hash tree: hash every node, compare hashes up the tree, and push the subtrees
that differ. It worked, but there was a lot of overhead on calculating the
hashes and updating every upstream node every time a point changed.

## The new way

Since the SIOT store is now on JetStream, we already history data available. The
only tricky parts are:

1. How do we handle multiple writers (downstream and upstream)?
2. Where do we draw the stream boundaries.

I originally planned one stream per node, but ended up with streams at the
device boundaries which is simpler and less overhead.

Because both the downstream and upstream can write data, there needs to be a
stream for each writer. Sync means each side holds a replica of the other's
stream, driven by durable NATS consumers: a push pump copies the device's stream
up, a pull pump copies the hub's configuration stream down. Current state on
either side is the merge of the two, newest timestamp winning.

Because no instance ever writes remote data into its own streams, points cannot
echo back and forth between instances. There is no loop to suppress, which
removes an entire class of sync bug by construction.

A durable consumer remembers its position across disconnects, so a device that
has been offline for two weeks reconnects and receives exactly the backlog, in
order, with original timestamps. No rescan, no comparison, no sync period to
configur. Replication is continuous: a write on one side shows up on the other
as fast as the connection carries it.

## SIOT drastically simplifies stream based replication

With SIOT, the developer rarely has to be concerned with the low-level stream
details. SIOT handles all of those details under the hood, and all the developer
needs to do is create nodes, points, and the clients that respond to and send
points. The rest happens automatically.

Distributed systems are hard, especially systems where you can't assume the
connection is solid and all services will be running all the time. With SIOT, a
lot of this complexity is eliminated. Nats JetsStream provides the building
blocks (streams, durable consumers, etc.) and SIOT manages them in a way that is
transparent to the developer.

The full design is in the
[sync reference](https://docs.simpleiot.org/docs/ref/sync.html) and
[ADR-7](https://docs.simpleiot.org/docs/adr/7-jetstream-store.html).
