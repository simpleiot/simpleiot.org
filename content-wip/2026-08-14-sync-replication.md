+++
title = "Sync is now stream replication"
description = "Simple IoT no longer compares hash trees to synchronize instances. Each instance replicates the other's streams, and the stream sequence number is the synchronization state."
date = 2026-08-14
[taxonomies]
tags = ["sync", "release"]
+++

The [previous post](/blog/jetstream-store/) covered moving the Simple IoT store
to NATS JetStream. This one covers the payoff: synchronization between instances
is now stream replication, and the hash tree is gone.

## The old way, and what it cost

SIOT has synchronized cloud and edge instances for years using a Merkle-style
hash tree: hash every node, compare hashes up the tree, and push the subtrees
that differ. It worked, and it got real products through years of field
deployments on connections I would not wish on anyone.

But comparing state is work that grows with the size of the tree, it ran on a
period rather than continuously, and the bookkeeping to keep hashes consistent
across concurrent writes was some of the most delicate code in the project. The
question a sync system has to answer is "what does the other side not have
yet?", and we were reconstructing that answer from scratch on every pass.

A stream already knows the answer. Messages have sequence numbers, so a reader
that remembers its position knows exactly what it has missed. That is the whole
trick.

## One writer per stream

Every instance appends only to its own streams. A device with root `X` writes
everything it produces to its stream; a hub writes configuration for that device
to a separate stream of its own. Sync means each side holds a replica of the
other's stream, driven by durable NATS consumers: a push pump copies the
device's stream up, a pull pump copies the hub's configuration stream down.
Current state on either side is the merge of the two, newest timestamp winning.

Because no instance ever writes remote data into its own streams, points cannot
echo back and forth between instances. There is no loop to suppress, which
removes an entire class of sync bug by construction.

A durable consumer remembers its position across disconnects, so a device that
has been offline for two weeks reconnects and receives exactly the backlog, in
order, with original timestamps. No rescan, no comparison, no sync period to
configure (that setting is gone from the UI, because there is nothing left for
it to mean). Replication is continuous: a write on one side shows up on the
other as fast as the connection carries it.

The pumps move messages in windows of up to 256 so the round trips overlap,
which is what makes a first sync of a long stream practical. A window that fails
is resent as a unit, so each subject always arrives in source order.

## Details that matter in the field

A few behaviors fall out of this design that we used to have to build
deliberately:

- **Pre-provisioning.** Configuration written on the hub before a device ever
  connects simply waits in the hub's stream and arrives on first connect.
- **Clean detach.** Deleting a device on the hub detaches it: the hub stops
  showing it, the device keeps operating standalone, and only the hub can
  restore it. Devices no longer force themselves back into the tree.
- **Gap-free external history.** The database client consumes the streams with
  its own durable consumers, so InfluxDB or VictoriaMetrics receives every
  point, including the backlog after an outage, rather than only what crossed
  the wire while it was listening.
- **Independent retention.** A hub can keep more history of a device's data than
  the device keeps itself, since each instance applies its own retention to the
  streams on its own disk.

When something does look wrong, the new `siot dump` command describes an
instance as it actually is: root ID, tree with IDs, and the replication streams
with their message counts. Comparing dumps from two instances is the quickest
way to tell a replication problem from a configuration one.

The full design is in the
[sync reference](https://docs.simpleiot.org/docs/ref/sync.html) and
[ADR-7](https://docs.simpleiot.org/docs/adr/7-jetstream-store.html). Some limits
are documented there too: nested boundaries (a device that itself syncs devices)
and per-stream authorization are planned, not shipped.

Distributed state machines are where I have spent some of my most humbling
debugging weeks, so I am saying this carefully: this design has fewer places to
be wrong. If you can see one I've missed, the
[forum](https://community.tmpdir.org/c/simple-iot/5) is where I'd like to find
out.
