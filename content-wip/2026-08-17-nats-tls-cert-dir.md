+++
title = "TLS certificates that renew without a restart"
description = "Simple IoT can now serve NATS TLS from a watched certificate directory. Point it at the directory Caddy already keeps fresh and renewals are picked up automatically."
date = 2026-08-17
[taxonomies]
tags = ["security", "release"]
+++

Every certificate story I have from the field ends the same way: the certificate
was fine for 89 days, and then it was not. Publicly trusted certificates now
live 90 days or less, which means renewal is not an annual chore to calendar; it
is a process that has to run without you.

The web side of this problem is solved. Most SIOT cloud deployments already run
Caddy in front of the web UI, and Caddy obtains and renews publicly trusted
certificates entirely on its own. The gap was NATS: SIOT loaded its TLS
certificate from a file once at start-up, so a renewed certificate waited for
the next restart, and devices in the field kept presenting the old one to be
rejected.

## Point SIOT at the directory

The latest SIOT closes that gap with one environment variable.
`SIOT_NATS_TLS_CERT_DIR` points at a directory that some other tool keeps
supplied with certificates:

```bash
SIOT_NATS_TLS_CERT_DIR=/var/lib/caddy/.local/share/caddy/certificates
SIOT_NATS_TLS_NAME=siot.example.com   # if the directory holds several domains
```

SIOT scans the directory recursively for certificate/key pairs and serves the
best one. Caddy's layout works, and so do certbot's, lego's, and a plain
combined PEM file, with no configuration describing which is which. Among the
candidates, the latest expiry wins, which is what selects a renewed certificate
over the one it replaced.

The directory is rescanned once a minute, so a renewal is served to new
connections without a restart, and existing connections keep their session. A
file that does not parse, such as a truncated write caught mid-renewal, is
skipped with a log message while the previous certificate keeps serving.

## Never up in plaintext

Start-up ordering is the detail I care most about here. At boot, SIOT waits
until the directory yields a usable pair before starting NATS. On a fresh
deployment that means SIOT simply waits while Caddy solves its first ACME
challenge, logging what it is waiting for. The alternative, starting in
plaintext because a certificate was not ready yet, is exactly the kind of silent
downgrade that nobody notices until an audit does, so it cannot happen.

Explicit `SIOT_NATS_TLS_CERT` and `SIOT_NATS_TLS_KEY` settings still take
precedence, for deployments that manage certificates their own way.

## The downstream side needs nothing

Because the certificates are publicly trusted, everything that connects verifies
against the system trust store: a downstream sync instance just writes its Sync
node URI with a `tls://` scheme, and the `nats` CLI and Grafana work the same
way. No CA files to distribute to devices, no client configuration to keep in
step with the server.

The [security reference](https://docs.simpleiot.org/docs/ref/security.html) has
the full details, including the one real deployment consideration: Caddy keeps
its storage private to its own user, so SIOT needs read access via a shared
group, an ACL, or Caddy's permissions config. The worked example there covers
all three.

This wraps up the series on this year's changes: the
[JetStream store](/blog/jetstream-store/),
[stream replication](/blog/sync-replication/),
[provisioning](/blog/provisioning/),
[Prometheus scraping](/blog/prometheus-scrape/), and now TLS that maintains
itself. Each one removes something a small team would otherwise have to operate
by hand. If you try them and something does not hold up, the
[forum](https://community.tmpdir.org/c/simple-iot/5) is where I want to hear
about it.
