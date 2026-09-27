# ADR-006 — JSON over UDP multicast for v1, CBOR/zenoh reserved

Status: accepted · 2026-09

**Context.** Messages are tiny (a tread command is ~60 bytes at 50 Hz); readability and tooling matter more than bandwidth on a 100 Mb link with seven nodes.

**Decision.** One JSON object per datagram on 239.77.83.1:7783; schema in `firmware/schemas/`. Heartbeat is implicit in the command stream; presence is the status stream; one node per dock.

**Consequences.** Anyone can debug with `tcpdump` and `jq`. Parsing cost on an MCU is acceptable at these rates. CBOR (same schema, binary) and zenoh-pico are the upgrade path if v2 moves to 10BASE-T1S.

**Rejected.** Protobuf (tooling weight); custom binary (unreadable on the playa at 3 a.m.).
