+++
title = "Collect Prometheus metrics without opening a port"
description = "The Simple IoT metrics client can scrape a local Prometheus /metrics endpoint and publish the samples as points, so applications keep their endpoints on loopback and still report upstream."
date = 2026-08-16
[taxonomies]
tags = ["metrics", "release"]
+++

Most services already export the numbers you want. Any Go application built with
`client_golang` has a Prometheus `/metrics` endpoint, and so do `node_exporter`,
cAdvisor, and a great deal of other infrastructure. The question is how those
numbers get off the machine.

The usual answer is to run Prometheus or `vmagent` somewhere and have it scrape
each target, which means the scraper needs network reach to every machine, and
every machine needs a port open. For a fleet of edge devices behind cellular
connections and NAT, that reach does not exist. And exposing `/metrics` publicly
describes an application's internals to anyone who asks.

Simple IoT 0.23.3 takes a different path: SIOT is already on the machine, so it
can scrape `127.0.0.1`. The application binds its endpoint to loopback and never
listens on a public interface. No port is opened, no VPN is built, no second
agent is installed, and the readings travel out over the connection SIOT already
holds. Set the metrics node's type to `prometheus`, give it a URI, and the
samples flow.

## Samples become points

A metric name becomes the point type, and its labels become the point key,
sorted so a series keeps the same key from one scrape to the next:

| Sample                                           | Point type             | Point key              |
| ------------------------------------------------ | ---------------------- | ---------------------- |
| `myapp_requests_total{method="post",code="200"}` | `myapp_requests_total` | `code=200,method=post` |
| `myapp_queue_depth`                              | `myapp_queue_depth`    | _(empty)_              |

Once a sample is a point, it is ordinary SIOT data: it shows in the UI, syncs
upstream, lands in local stream history, and can drive rules. Histograms and
summaries need no special handling, since the exposition format has already
flattened them into ordinary samples.

Counters get one extra courtesy. A counter only ever climbs, which makes it
unusable in a rule: "alert when errors increase" needs a rate, not a total. So a
counter also publishes a `_delta` point carrying the change since the previous
scrape, and a rule can act on that directly.

## Querying it like Prometheus data

The database client closes the loop. Each label in a scraped key is written to
the time-series database as its own label, so a scraped series queries the way
the Prometheus series it came from did. In Grafana against VictoriaMetrics,
`histogram_quantile` works on scraped histogram buckets as if Prometheus had
collected them.

There are guardrails worth knowing. A scrape is capped at 3000 series, because
points are current state on a node and a node has a payload budget; a source
bigger than that is better split across several nodes. The details, including
how label characters that a point key cannot hold are handled, are in the
[metrics documentation](https://docs.simpleiot.org/docs/user/metrics.html).

This feature exists because I kept wanting the metrics from my own services on
machines that SIOT already watched, and running a whole Prometheus for three
custom servers was more work than it was worth. If your monitoring setup has a
shape this does not fit, I'd like to hear about it on the
[forum](https://community.tmpdir.org/c/simple-iot/5).
