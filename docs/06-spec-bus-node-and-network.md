# 06 — Bus node and network spec (PS-Bus v1)

## Physical layer

* **Data**: 100BASE-TX over M12 D-coded connectors and cables (IP67). Star topology through the
  8-port unmanaged switch in the B node. Cable lengths ≤ 2 m.
* **Power/ID**: separate M12 A-coded 4-pin: bus +, bus −, ID, spare. SELV 21–29.4 V. Per-port eFuse
  5 A on the B node. ID pin: resistor ladder inside each dock/port.

| ID resistor | Role |
|---|---|
| 1.0 kΩ | FL |
| 2.2 kΩ | FR |
| 4.7 kΩ | RL |
| 10 kΩ | RR |
| 22 kΩ | CL |
| 47 kΩ | CR |
| 100 kΩ | AUX (lights, inputs) |
| open | charger dock |

"Do better than Ethernet": the interface reserves **10BASE-T1S (single-pair Ethernet, multidrop)**
as PS-Bus v2 — one twisted pair, no switch, same IP stack. Until it is proven on the playa, v1 is
plain 100BASE-TX because every MCU, laptop and phone can speak it.

## Transport

UDP multicast `239.77.83.1:7783`, one JSON object per datagram (CBOR reserved for v2). No broker,
no master. The B node's switch just forwards frames. Schema: `firmware/schemas/psbus-message.schema.json`.

Envelope: `{ "t": "<topic>", "ts": <seconds, node clock>, ...payload }`

## Topics

| Topic | Rate | Payload | Publisher |
|---|---|---|---|
| `ctrl/tread/left` · `ctrl/tread/right` | 50 Hz | `v`, `seq`, `src`, `input` | control modules |
| `wheel/<FL|FR|RL|RR>/status` | 10 Hz | `serial`, `v_kmh`, `soc`, `temp_c`, `fault`, `stop` | wheel modules |
| `node/<serial>/hello` | 1 Hz | `kind`, `dock`, `rating`, `fw` | every node |
| `veh/mode` | 10 Hz | `mode` (run/crawl/stop), `rating`, `rider_class` | supervisor |
| `veh/estop` | 10 Hz | `active` | supervisor, any node |
| `light/<n>/cmd` | on change | `on`, `pattern` | anyone |
| `input/<n>/event` | on change | `event` | inputs |
| `veh/log` | on event | text | supervisor |

## Rules

1. **Heartbeat by stream.** Wheels stop 200 ms after the last valid tread command and ramp to zero in 300 ms.
2. **One node per dock.** A `hello` from a new serial on an occupied dock supersedes the old occupant immediately (this is how a hot-swap is recognised without link-state).
3. **Presence = status stream.** The supervisor treats a wheel as present only while its status is < 250 ms old (2.5 frames).
4. **Rating.** `vehicle_rating = min(rating of live nodes ∪ frame rating)`; `crawl` if below rider class.
5. **Malformed = absent.** Bad JSON, out-of-range `v`, stale `seq` are dropped; the timeout does the rest.
6. **Modes.** `run` cap 8 km/h · `crawl` cap 2 km/h · `stop` cap 0.

## B node hardware

8-port 100 Mb unmanaged switch board, supervisor MCU, 6 × (M12 D + M12 A) ports, e-stop mushroom,
charge input (XT60 → bus through a CC/CV limiter), optional extra pack bay. Mass budget 0.55 kg.
If it dies the vehicle stops (rule 1) — it is a swappable unit like everything else.

## Reference implementation

`firmware/sim/psbus_sim.py` is the behavioural reference: the same node classes run against a
deterministic in-process bus (CI) or real UDP multicast (bench). Candidate production stack:
zenoh-pico or a hand-rolled UDP loop on an MCU with a hardware PHY.
