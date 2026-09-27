#!/usr/bin/env python3
"""
PS-Bus reference simulator.

Models the Playa Sprawler control network exactly as the spec describes it
(docs/06-spec-bus-node-and-network.md):

  * every node is a UDP multicast pub/sub peer (239.77.83.1:7783, JSON);
  * a node learns its ROLE from the dock it is plugged into (geographic
    addressing: the dock's ID pin says FL/FR/RL/RR/CL/CR), never from config;
  * wheel nodes stop within COMMS_TIMEOUT_MS of the last valid tread command;
  * the supervisor (B node) computes the vehicle rating = min(part ratings)
    and forces `crawl` mode when it is below the rider class;
  * any control input (lever, pedal, sip-puff...) publishes the same
    normalised tread message, so inputs are interchangeable.

Two transports share the same node code:
  --transport inproc  deterministic simulated clock; runs the scripted
                      hot-swap scenario and self-checks (used by CI);
  --transport udp     real multicast on the host network, real time; run one
                      process per node (e.g. on a bench with real nodes).

    python psbus_sim.py                      # scripted demo, prints a timeline
    python psbus_sim.py --check              # demo + assertions (exit 1 on fail)
    python psbus_sim.py --transport udp --node wheel --serial W-0001
    python psbus_sim.py --transport udp --node control --serial C-0001 --input pedal
    python psbus_sim.py --transport udp --node supervisor --rider-class PS-125
"""
import argparse, json, math, socket, struct, sys, time, itertools
from collections import defaultdict

MCAST_GRP, MCAST_PORT = "239.77.83.1", 7783
COMMS_TIMEOUT_S = 0.200          # wheel stops if no valid tread command inside this window
RAMP_DOWN_S = 0.300              # decel ramp to zero on timeout / estop
CTRL_HZ, STATUS_HZ, HELLO_HZ = 50, 10, 1
CLASS_KG = {"PS-100": 100, "PS-125": 125, "PS-150": 150}
MODE_CAP_KMH = {"run": 8.0, "crawl": 2.0, "stop": 0.0}
DOCK_ROLES = {"FL": "left", "RL": "left", "FR": "right", "RR": "right", "CL": "left", "CR": "right"}


# ----------------------------------------------------------------------------- transports
class InprocBus:
    """Deterministic in-process bus with a simulated clock."""
    def __init__(self):
        self.now = 0.0
        self.subs = []
        self.log = []

    def publish(self, topic, payload):
        msg = {"t": topic, "ts": round(self.now, 4), **payload}
        self.log.append(msg)
        for pattern, cb in list(self.subs):
            if topic_match(pattern, topic):
                cb(msg)

    def subscribe(self, pattern, cb):
        self.subs.append((pattern, cb))

    def unsubscribe_all(self, owner_cbs):
        self.subs = [(p, cb) for (p, cb) in self.subs if cb not in owner_cbs]

    def time(self):
        return self.now


class UdpBus:
    """Real UDP multicast transport; every node runs as its own process."""
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(("", MCAST_PORT))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY))
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        self.sock.setblocking(False)
        self.subs = []

    def publish(self, topic, payload):
        msg = {"t": topic, "ts": round(time.time(), 4), **payload}
        self.sock.sendto(json.dumps(msg).encode(), (MCAST_GRP, MCAST_PORT))

    def subscribe(self, pattern, cb):
        self.subs.append((pattern, cb))

    def pump(self):
        while True:
            try:
                data, _ = self.sock.recvfrom(4096)
            except BlockingIOError:
                return
            try:
                msg = json.loads(data.decode())
            except ValueError:
                continue
            for pattern, cb in self.subs:
                if topic_match(pattern, msg.get("t", "")):
                    cb(msg)

    def time(self):
        return time.time()


def topic_match(pattern, topic):
    p, t = pattern.split("/"), topic.split("/")
    if len(p) != len(t):
        return False
    return all(a in ("+", b) for a, b in zip(p, t))


# ----------------------------------------------------------------------------- nodes
class Node:
    def __init__(self, bus, serial, rating, kind):
        self.bus, self.serial, self.rating, self.kind = bus, serial, rating, kind
        self.next_hello = 0.0
        self.dock = None
        self.alive = False              # a node does nothing until it is plugged into a dock
        self.cbs = []

    def sub(self, pattern, cb):
        self.cbs.append(cb)
        self.bus.subscribe(pattern, cb)

    def plug(self, dock):
        """Read the dock ID pin. Everything the node does follows from this."""
        self.dock = dock
        self.alive = True

    def unplug(self):
        self.alive = False
        self.dock = None
        if isinstance(self.bus, InprocBus):
            self.bus.unsubscribe_all(self.cbs)
        self.cbs = []

    def hello(self):
        self.bus.publish(f"node/{self.serial}/hello", {"kind": self.kind, "dock": self.dock, "rating": self.rating, "fw": "0.1.0"})

    def tick(self, now):
        if not self.alive:
            return
        if now >= self.next_hello:
            self.hello()
            self.next_hello = now + 1.0 / HELLO_HZ


class WheelNode(Node):
    """One wheel module. Motor sign is inverted on the left side so 'forward' means forward everywhere."""
    def __init__(self, bus, serial, rating="PS-125"):
        super().__init__(bus, serial, rating, "wheel")
        self.cmd, self.cmd_ts, self.seq_seen = 0.0, -1e9, -1
        self.v_kmh, self.mode, self.estop = 0.0, "stop", False
        self.next_status = 0.0
        self.last_stop_reason = None

    def plug(self, dock):
        super().plug(dock)
        self.side = DOCK_ROLES[dock]
        self.sub(f"ctrl/tread/{self.side}", self.on_cmd)
        self.sub("veh/mode", lambda m: setattr(self, "mode", m["mode"]))
        self.sub("veh/estop", lambda m: setattr(self, "estop", bool(m["active"])))
        self.cmd_ts = -1e9

    def on_cmd(self, m):
        if not self.alive or m.get("seq", 0) <= self.seq_seen and m.get("seq", 0) != 0:
            return
        v = m.get("v")
        if not isinstance(v, (int, float)) or not -1.0 <= v <= 1.0:
            return                              # malformed -> ignored, timeout will catch it
        self.seq_seen, self.cmd, self.cmd_ts = m.get("seq", 0), float(v), m["ts"]

    def tick(self, now):
        super().tick(now)
        if not self.alive:
            return
        cap = MODE_CAP_KMH.get(self.mode, 0.0)
        timed_out = (now - self.cmd_ts) > COMMS_TIMEOUT_S
        if self.estop or timed_out or cap == 0.0:
            target = 0.0
            self.last_stop_reason = "estop" if self.estop else ("timeout" if timed_out else "mode")
        else:
            target = self.cmd * cap
            self.last_stop_reason = None
        # rate limit: full-scale ramp in RAMP_DOWN_S (decel) / 0.5 s (accel)
        dt = 1.0 / CTRL_HZ
        step = 8.0 * dt / (RAMP_DOWN_S if abs(target) < abs(self.v_kmh) else 0.5)
        self.v_kmh += max(-step, min(step, target - self.v_kmh))
        if abs(self.v_kmh) < 1e-3:
            self.v_kmh = 0.0
        if now >= self.next_status:
            self.bus.publish(f"wheel/{self.dock}/status", {"serial": self.serial, "v_kmh": round(self.v_kmh, 2), "soc": 0.9,
                                                           "temp_c": 41, "fault": None, "stop": self.last_stop_reason})
            self.next_status = now + 1.0 / STATUS_HZ


class ControlNode(Node):
    """One control module. `input_fn(now) -> [-1, 1]` stands in for a lever, pedal, joystick, sip-puff..."""
    def __init__(self, bus, serial, input_kind, input_fn, rating="PS-150"):
        super().__init__(bus, serial, rating, "control")
        self.input_kind, self.input_fn = input_kind, input_fn
        self.seq = itertools.count(1)
        self.next_cmd = 0.0

    def plug(self, dock):
        super().plug(dock)
        self.side = DOCK_ROLES[dock]

    def tick(self, now):
        super().tick(now)
        if not self.alive:
            return
        if now >= self.next_cmd:
            v = max(-1.0, min(1.0, self.input_fn(now)))
            self.bus.publish(f"ctrl/tread/{self.side}", {"v": round(v, 3), "seq": next(self.seq), "src": self.serial, "input": self.input_kind})
            self.next_cmd = now + 1.0 / CTRL_HZ


class Supervisor(Node):
    """The B node. Owns veh/mode and veh/estop; nothing else needs to be configured."""
    def __init__(self, bus, rider_class="PS-125", rating="PS-150"):
        super().__init__(bus, "B-0001", rating, "supervisor")
        self.rider_class = rider_class
        self.parts = {}                 # serial -> (kind, dock, rating, last_seen)
        self.status_seen = {}           # dock -> last status ts
        self.mode, self.estop = "stop", False
        self.events = []
        self.alive = True
        self.sub("node/+/hello", self.on_hello)
        self.sub("wheel/+/status", lambda m: self.status_seen.__setitem__(m["t"].split("/")[1], m["ts"]))

    def on_hello(self, m):
        serial = m["t"].split("/")[1]
        # one node per dock: a hello from a new serial on an occupied dock supersedes the old occupant
        for other, (k, d, r, ts) in list(self.parts.items()):
            if d == m["dock"] and other != serial:
                del self.parts[other]
        self.parts[serial] = (m["kind"], m["dock"], m["rating"], m["ts"])

    def vehicle_rating(self, now):
        live = [r for (k, d, r, ts) in self.parts.values() if now - ts <= 2.5 / HELLO_HZ]
        return min(live, key=lambda r: CLASS_KG[r]) if live else None

    def tick(self, now):
        super().tick(now)
        wheels = {d for (k, d, r, ts) in self.parts.values() if k == "wheel" and now - ts <= 2.5 / HELLO_HZ}
        # a wheel is present iff its status stream is alive (2.5 frames at STATUS_HZ = 250 ms)
        wheels_ok = {"FL", "FR", "RL", "RR"} <= wheels and all(now - self.status_seen.get(d, -1e9) <= 2.5 / STATUS_HZ for d in ("FL", "FR", "RL", "RR"))
        rating = self.vehicle_rating(now)
        if not wheels_ok or rating is None:
            new_mode = "stop"
        elif CLASS_KG[rating] < CLASS_KG[self.rider_class]:
            new_mode = "crawl"
        else:
            new_mode = "run"
        if new_mode != self.mode:
            self.events.append((now, f"mode {self.mode} -> {new_mode} (wheels {sorted(wheels)}, vehicle rating {rating}, rider {self.rider_class})"))
            self.mode = new_mode
        self.bus.publish("veh/mode", {"mode": self.mode, "rating": rating, "rider_class": self.rider_class})
        self.bus.publish("veh/estop", {"active": self.estop})


# ----------------------------------------------------------------------------- scripted scenario
def scenario(check=False, quiet=False):
    bus = InprocBus()
    left_in = lambda now: 0.0 if now < 1.0 else min(1.0, (now - 1.0) / 1.5) * 0.8
    right_in = lambda now: 0.0 if now < 1.0 else min(1.0, (now - 1.0) / 1.5) * 0.8
    sup = Supervisor(bus, rider_class="PS-125")
    cl = ControlNode(bus, "C-0007", "lever", left_in)      # rider uses a lever on the left...
    cr = ControlNode(bus, "C-0011", "pedal", right_in)     # ...and a pedal on the right: same messages
    wheels = {d: WheelNode(bus, f"W-{i:04d}") for i, d in enumerate(("FL", "FR", "RL", "RR"), 1)}
    spare_low = WheelNode(bus, "W-0999", rating="PS-100")  # a lower-rated module from another vehicle
    spare_ok = WheelNode(bus, "W-0042", rating="PS-125")
    for d, w in wheels.items():
        w.plug(d)
    cl.plug("CL"); cr.plug("CR")
    timeline = []
    def log(now, msg):
        timeline.append((now, msg))
        if not quiet:
            print(f"{now:6.2f}s  {msg}")

    nodes = [sup, cl, cr, *wheels.values(), spare_low, spare_ok]
    dt = 1.0 / CTRL_HZ
    steps = int(9.0 / dt)
    marks = {}
    for i in range(steps):
        now = round(i * dt, 4)
        bus.now = now
        # --- scripted events
        if i == 0: log(now, "boot: 4 wheel modules + lever (CL) + pedal (CR) + supervisor; rider class PS-125")
        if abs(now - 3.00) < 1e-6:
            log(now, "HOT-SWAP 1: wheel RR (W-0004) pulled out while rolling"); wheels["RR"].unplug()
        if abs(now - 3.60) < 1e-6:
            log(now, "HOT-SWAP 1: spare W-0999 (rated PS-100) pushed into dock RR; it reads the dock ID and becomes RR"); spare_low.plug("RR"); wheels["RR"] = spare_low
        if abs(now - 5.00) < 1e-6:
            log(now, "HOT-SWAP 2: W-0999 replaced by W-0042 (rated PS-125)"); spare_low.unplug(); spare_ok.plug("RR"); wheels["RR"] = spare_ok
        if abs(now - 6.50) < 1e-6:
            log(now, "FAULT: left control cable unplugged (CL goes silent)"); cl.unplug()
        if abs(now - 7.50) < 1e-6:
            log(now, "left control re-plugged into dock CL"); cl.plug("CL")
        for n in nodes:
            n.tick(now)
        # --- observations
        vL = (wheels["FL"].v_kmh + wheels["RL"].v_kmh) / 2
        vR = (wheels["FR"].v_kmh + wheels["RR"].v_kmh) / 2 if wheels["RR"].alive else wheels["FR"].v_kmh
        if now == 2.50: marks["v_run"] = (vL, vR); log(now, f"rolling: left {vL:.1f} km/h, right {vR:.1f} km/h, mode {sup.mode}")
        if now == 3.30 and "stop_after_pull" not in marks:
            marks["stop_after_pull"] = (sup.mode, wheels["FR"].v_kmh); log(now, f"0.30 s after pull: mode {sup.mode}, FR {wheels['FR'].v_kmh:.1f} km/h")
        if now == 4.80: marks["crawl"] = (sup.mode, vR); log(now, f"with PS-100 module: mode {sup.mode}, right side {vR:.1f} km/h (cap {MODE_CAP_KMH[sup.mode]} km/h)")
        if now == 6.40: marks["run2"] = (sup.mode, vR); log(now, f"with PS-125 module: mode {sup.mode}, right side {vR:.1f} km/h")
        if 6.5 < now < 7.5 and "left_stopped" not in marks and wheels["FL"].v_kmh == 0.0:
            marks["left_stopped"] = now - 6.5; log(now, f"left wheels at 0 km/h {now - 6.5:.2f} s after the cable fault (timeout {COMMS_TIMEOUT_S*1000:.0f} ms + ramp {RAMP_DOWN_S*1000:.0f} ms)")
        if now == 8.90: marks["end"] = (sup.mode, vL, vR); log(now, f"end: mode {sup.mode}, left {vL:.1f} km/h, right {vR:.1f} km/h")
    for t, e in sup.events:
        if not quiet:
            print(f"{t:6.2f}s  supervisor: {e}")
    if check:
        ok = True
        def expect(cond, msg):
            nonlocal ok
            print(("PASS " if cond else "FAIL ") + msg)
            ok = ok and cond
        expect(marks["v_run"][0] > 5 and abs(marks["v_run"][0] - marks["v_run"][1]) < 0.1, "lever and pedal produce identical drive on both sides")
        expect(marks["stop_after_pull"][0] == "stop", "vehicle enters stop mode when a wheel module is pulled")
        expect(marks["crawl"][0] == "crawl" and marks["crawl"][1] <= MODE_CAP_KMH["crawl"] + 0.05, "a PS-100 part on a PS-125 rider forces crawl mode")
        expect(marks["run2"][0] == "run", "run mode returns once every part meets the rider class")
        expect("left_stopped" in marks and marks["left_stopped"] <= COMMS_TIMEOUT_S + RAMP_DOWN_S + 0.03, "left side stops within timeout + ramp after cable fault")
        expect(marks["end"][0] == "run" and marks["end"][1] > 5, "vehicle recovers after the control is re-plugged")
        print("ALL CHECKS PASSED" if ok else "CHECKS FAILED")
        return 0 if ok else 1
    return 0


# ----------------------------------------------------------------------------- real-network node
def run_udp(args):
    bus = UdpBus()
    if args.node == "wheel":
        n = WheelNode(bus, args.serial, args.rating); n.plug(args.dock)
    elif args.node == "control":
        fn = lambda now: math.sin(now) * 0.5      # replace with a real ADC read
        n = ControlNode(bus, args.serial, args.input, fn, args.rating); n.plug(args.dock)
    else:
        n = Supervisor(bus, args.rider_class)
    print(f"{args.node} {n.serial} on dock {n.dock} — joined {MCAST_GRP}:{MCAST_PORT}")
    while True:
        bus.pump(); n.tick(bus.time()); time.sleep(0.005)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--transport", choices=["inproc", "udp"], default="inproc")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--quiet", action="store_true")
    ap.add_argument("--node", choices=["wheel", "control", "supervisor"], default="wheel")
    ap.add_argument("--serial", default="W-0001")
    ap.add_argument("--dock", default="FL")
    ap.add_argument("--input", default="lever")
    ap.add_argument("--rating", default="PS-125")
    ap.add_argument("--rider-class", default="PS-125")
    a = ap.parse_args()
    if a.transport == "udp":
        run_udp(a)
    else:
        sys.exit(scenario(check=a.check, quiet=a.quiet))
