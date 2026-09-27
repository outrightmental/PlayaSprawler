# ADR-003 — Ethernet-only signalling, UDP multicast, geographic addressing

Status: accepted · 2026-09

**Context.** The brief: only Ethernet (or better) jacks and cables for signals; every device joins a pub/sub pool on a router; power on its own system.

**Decision.** 100BASE-TX over M12 D-coded connectors through an unmanaged switch in the B node; UDP multicast JSON messages, no broker; a separate M12 A-coded power/ID connector whose ID pin tells a node which dock it is in.

**Consequences.** Any laptop can sniff or inject on the bus for diagnostics; nodes are configuration-free; the switch is a single point of failure that fails safe (no messages = stop). 10BASE-T1S single-pair Ethernet is reserved as v2 ("do better").

**Rejected.** CAN (not Ethernet; needs addressing config); PoE (unnecessary with a 25 V bus, heavier ports); a broker (MQTT) — a master that can die.
