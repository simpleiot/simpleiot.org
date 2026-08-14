+++
title = "The store is now a stream"
description = "Simple IoT now stores all application data in NATS JetStream. Points are already messages, so the store captures them instead of translating them into rows, and history comes along for free."
date = 2026-08-13
[taxonomies]
tags = ["store", "release"]
+++

Simple IoT 0.23 replaces the SQLite store with
[NATS JetStream](https://docs.nats.io/nats-concepts/jetstream). This is the
biggest architectural change in the project's history, and it is the first of a
series of posts on what we've been building this year. This one covers the store
itself; the next covers what it does for synchronization.

## Two shapes of the same data

SIOT has always been a NATS application. Every component, whether a Modbus
client, a rule, or the UI, communicates by publishing points as messages. The
store's job was to catch those messages and keep them.

For years it did that by translating each point into rows in SQLite (and before
that, Bolt and Genji). SQLite served us well, and I would still reach for it in
plenty of applications. But it meant we maintained two shapes of the same data:
the message in flight and the row at rest, with translation code in between, and
a Merkle-style hash tree bolted on top so two instances could figure out how
their rows differed.

The real problem was never the database. It was that we were translating between
two data models when one of them already did everything we needed.

## Points are already messages

A JetStream stream is an append-only log of messages with sequence numbers and
per-subject indexing. That shape matches IoT data unusually well:

- **Persisting a point means capturing it.** The same message that moves between
  components lands in a stream. No translation layer, no second data model.
- **History is the natural byproduct.** A stream retains every point written to
  a subject, so time-series history lives in the same place as current state.
  The current value of a point is simply the last message on its subject.
- **Sequence numbers replace the hash tree.** Streams are ordered, so another
  instance can replicate one and know exactly what it has and has not seen. More
  on this in the next post.
- **It is already there.** JetStream runs inside the NATS server every SIOT
  instance ships, on cloud machines and small edge devices alike. There is no
  separate database process to install or operate.

Reads never touch JetStream directly. The store keeps the merged current state
in in-memory caches, populated from the subject tips at startup, so queries stay
fast.

## Retention that understands configuration

Retention is per subject: each point type on each node keeps its own most recent
20,000 messages by default. Per-subject limits have a property that time- or
size-based retention cannot give you: configuration points, written a handful of
times, are effectively kept forever, while a sensor reporting every minute wraps
after about two weeks. Current state is always preserved.

The default works out to about four months of history for 10-minute data,
bounded on disk even for a device nobody visits. A device with little flash can
lower it with `SIOT_STORE_MAX_MSGS_PER_SUBJECT`.

## Compression pays exactly where it matters

Streams are compressed with S2 by default. Point data compresses unusually well,
because the same type repeats in every message, keys come from a small set, and
timestamps march forward. In our testing, a store of 100,000 scraped points went
from 33.4 MB to 11.7 MB. A small store gives up nothing, and compression starts
paying exactly where disk begins to matter.

## Migrating

Existing SQLite databases migrate with `siot export` on v0.22.0 followed by
`siot import` on 0.23. The full design analysis is recorded in
[ADR-7](https://docs.simpleiot.org/docs/adr/7-jetstream-store.html), and the
[store reference](https://docs.simpleiot.org/docs/ref/store.html) covers
retention, compression, and durability tuning in detail.

This is the kind of simplification that feels right. Stay tuned for how
synchronization works, and how streams simplify so many things.
