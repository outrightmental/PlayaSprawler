# Firmware

* `sim/psbus_sim.py` — the behavioural reference for every node type. `python sim/psbus_sim.py --check`
  runs the scripted hot-swap scenario on a deterministic in-process bus and asserts the timing rules;
  `--transport udp` runs a single node on real multicast for bench work.
* `schemas/psbus-message.schema.json` — JSON Schema for every PS-Bus v1 message.

Production targets (not yet written): an MCU with a hardware 100BASE-TX PHY per node, FOC motor
controller in the wheel module, zenoh-pico or a hand-rolled UDP loop. The simulator's node classes
are the spec those ports must match (`docs/06`).
