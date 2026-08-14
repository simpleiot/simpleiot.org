+++
title = "Provision a device with a directory of files"
description = "Simple IoT instances can now configure themselves from YAML files: applied at start-up, re-applied when they change, idempotent, and checkable in CI."
date = 2026-08-15
[taxonomies]
tags = ["provisioning", "release"]
+++

Building one device by hand in a UI is fine. Building the fiftieth unit of a
product that way is how configuration drift is born: every unit slightly
different, nobody sure which one is right, and the knowledge of how to set one
up living in someone's head.

Simple IoT 0.22 addresses this with provisioning: an instance configures itself
from a directory of YAML files, applied at start-up and whenever a file changes.
A unit built from an image comes up configured, with no import step and no
operator involvement.

## A file that reads as configuration

One format now describes a tree of nodes, and `siot export`, `siot import`, and
provisioning all use it. The node type is the key and each point type is a key
of its own, so a file reads as configuration rather than as a serialized data
structure:

```yaml
apiVersion: 1
nodes:
  - group:
      description: Sensors
      children:
        - modbus:
            description: Modbus sensors
            port: /dev/ttyS1
            baud: 9600
```

There are no node IDs in a file. Nodes are matched by description, which is what
makes applying a file idempotent: it creates what is missing, sends only the
points that differ, and does nothing when the tree already agrees. Applying the
same file twice does what applying it once did, so a configuration-management
tool can drop a file in place without checking state first. A `nodeID` point
names the node it refers to by description too, so a rule can point at a
variable without either of them knowing a UUID, even across files.

Because an export uses the same format, the workflow I actually use is: build
the configuration in the UI on a bench unit, `siot export`, and ship the result
as a provisioning file.

## Two ways files arrive

Files come from a directory on disk (`SIOT_PROVISIONING_DIR`, defaulting to
`<SIOT_DATA>/provisioning` when it exists, so an image can ship the directory
and say nothing else), applied in lexical order with the familiar `10-`, `20-`
prefixes. Files can also be uploaded through the UI as `file` nodes, which is
how a unit whose filesystem you cannot reach gets configured. Disk applies
first, uploads layer on top.

A `provisioning` node under the root records what was applied, with a checksum
per file and the last error if one failed. Provisioning describes what should
exist, and does not own what it made: removing a file removes its status, and
the nodes it created stay. A `delete` list is how a file removes nodes, and it
is as safe to apply repeatedly as everything else.

## Checkable before it ships

`siot provision -dir ./provisioning` prints what a directory of files would do
to a running instance without applying any of it, and `-check` only parses them,
which needs no instance at all. That second form is built for CI: a build can
fail on a bad configuration file before an image is ever flashed.

Configuration as reviewable, diffable, testable files is a practice the rest of
the software world settled on years ago. Embedded devices deserve the same
treatment, and the description-matching rules have some subtlety worth reading;
the details are in the
[configuration documentation](https://docs.simpleiot.org/docs/user/configuration.html).

If you provision fleets today, with SIOT or anything else, I'd like to know what
this format cannot express yet. Tell me on the
[forum](https://community.tmpdir.org/c/simple-iot/5).
