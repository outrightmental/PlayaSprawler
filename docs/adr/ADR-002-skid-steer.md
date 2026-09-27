# ADR-002 — Skid steer, no steering mechanism

Status: accepted · 2026-09

**Context.** Four identical modules cannot include steering geometry without becoming non-identical (a steered front module differs from a rear one).

**Decision.** Differential (skid) steering: left tread drives both left wheels, right tread both right wheels. Modules only need to know their side, which the dock tells them.

**Consequences.** Zero-radius turns; scrub on hard playa is harmless at 8 km/h; the turn-rate limiter `|ω|·|v| ≤ 0.25 g` is required in firmware because the geometry allows very fast yaw. Rider training: two treads, like a tracked vehicle.

**Rejected.** Ackermann steering (two module types, a steering column); castor front wheels (non-driven modules, poor sand performance).
