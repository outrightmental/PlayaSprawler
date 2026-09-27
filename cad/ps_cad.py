"""
Playa Sprawler — parametric CAD (CadQuery 2.x).

Everything is generated from analysis/ps_params.py:
  * joiners: for every frame node, a printed joiner is grown from the node's
    member directions (socket boss per tube, anchor rod per cord/strap),
    so a geometry change re-generates every joiner consistently;
  * wheel module: hub-motor wheel + inboard carrier brick with the T-rail dock;
  * tubes, cords and the seat sling for the assembly;
  * exports: STEP (machinable/importable), STL (printable), SVG views.

Run:  python ps_cad.py        -> writes ./exports/
"""
import os, sys, math
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "analysis"))
import cadquery as cq
from cadquery import Vector as V
import ps_params as P

OUT = os.path.join(os.path.dirname(__file__), "exports")
os.makedirs(OUT, exist_ok=True)

TUBE_R = P.TUBE["od"] / 2
BORE_R = TUBE_R + 0.15            # printed fit clearance
SOCKET_WALL = 4.0
SOCKET_DEPTH = 50.0
SOCKET_START = 8.0                # socket bottom sits this far from the node point
CORE_R = 21.0
LUG_R = 6.0
LUG_LEN = 22.0
CORD_HOLE_R = 3.0
PIN_R = 2.6                       # M5 cross pin


def unit(a, b):
    v = V(*b) - V(*a)
    return v.normalized(), v.Length


def perp(v):
    ref = V(0, 0, 1) if abs(v.dot(V(0, 0, 1))) < 0.9 else V(1, 0, 0)
    return v.cross(ref).normalized()


def node_members(node):
    return [(m, a, b, k) for (m, a, b, k) in P.frame_members() if node in (a, b)]


def joiner(node, nodes):
    """Printed joiner at a node: core + socket boss per tube + anchor rod per tension member."""
    p = V(*nodes[node])
    body = cq.Solid.makeSphere(CORE_R, p, V(0, 0, 1), -90, 90, 360)
    cuts = []
    for m, a, b, kind in node_members(node):
        other = b if a == node else a
        u, L = unit(nodes[node], nodes[other])
        if kind == "tube":
            boss_len = SOCKET_START + SOCKET_DEPTH + 4
            body = body.fuse(cq.Solid.makeCylinder(TUBE_R + SOCKET_WALL, boss_len, p, u))
            cuts.append(cq.Solid.makeCylinder(BORE_R, SOCKET_DEPTH + 30, p + u * SOCKET_START, u))
            w = perp(u)
            cuts.append(cq.Solid.makeCylinder(PIN_R, 2 * (TUBE_R + SOCKET_WALL) + 4,
                                              p + u * (SOCKET_START + SOCKET_DEPTH - 12) - w * (TUBE_R + SOCKET_WALL + 2), w))
        else:  # cord / fabric anchor: short rod with a cross hole
            body = body.fuse(cq.Solid.makeCylinder(LUG_R, CORE_R + LUG_LEN - 4, p, u))
            w = perp(u)
            cuts.append(cq.Solid.makeCylinder(CORD_HOLE_R, 2 * LUG_R + 4, p + u * (CORE_R + LUG_LEN - 11) - w * (LUG_R + 2), w))
    # docks get the shoe that grips the wheel-module T-rail (rail runs fore-aft, x)
    if node.startswith("DOCK"):
        shoe = cq.Solid.makeBox(90, 44, 34, p + V(-45, -22, -34), V(0, 0, 1))
        body = body.fuse(shoe)
        head = cq.Solid.makeBox(94, 24.6, 8.6, p + V(-47, -12.3, -34), V(0, 0, 1))
        stem = cq.Solid.makeBox(94, 12.6, 14, p + V(-47, -6.3, -26), V(0, 0, 1))
        cuts += [head, stem, cq.Solid.makeCylinder(4.1, 60, p + V(0, 0, -40), V(0, 0, 1))]  # drop-pin bore
    # seat tips get a rounded peg that sits inside the canvas corner pocket
    if node.startswith(("RTIP", "FTIP")):
        peg = cq.Solid.makeCylinder(14, 55, p, V(0, 0, 1)).fuse(cq.Solid.makeSphere(14, p + V(0, 0, 55), V(0, 0, 1), -90, 90, 360))
        body = body.fuse(peg)
    for c in cuts:
        body = body.cut(c)
    return body


def wheel_module(pos, side):
    """pos: dock point (x, y, z). side: +1 left, -1 right. Returns (wheel shapes, carrier)."""
    sy = 1 if side > 0 else -1
    dock = V(*pos)
    axle_z = P.WHEEL_R_MM
    yc = sy * P.WHEEL_PLANE_Y
    center = V(dock.x, yc, axle_z)
    ydir = V(0, 1, 0)
    tire = cq.Solid.makeTorus((P.WHEEL_OD_MM - P.TIRE_WIDTH_MM) / 2, P.TIRE_WIDTH_MM / 2, center, ydir)
    rim = cq.Solid.makeCylinder(152.5, 40, center - ydir * 20, ydir).cut(cq.Solid.makeCylinder(140, 40, center - ydir * 20, ydir))
    motor = cq.Solid.makeCylinder(50, 90, center - ydir * 45, ydir)
    # carrier brick, inboard of the tire, top face = dock plane; the T-rail sits on top
    cx, cy, cz = dock.x, sy * P.DOCK_Y, axle_z
    t = P.CARRIER_THICKNESS_MM
    brick = cq.Solid.makeBox(200, t, (P.DOCK_Z_MM - 16) - (axle_z - 40), V(cx - 100, cy - t / 2, axle_z - 40), V(0, 0, 1))
    brick = brick.fillet(8, [e for e in brick.Edges() if abs(e.tangentAt(0).y) > 0.99])
    stem = cq.Solid.makeBox(120, 12, 8, V(cx - 60, cy - 6, P.DOCK_Z_MM - 16), V(0, 0, 1))
    head = cq.Solid.makeBox(120, 24, 8, V(cx - 60, cy - 12, P.DOCK_Z_MM - 8), V(0, 0, 1))
    carrier = brick.fuse(stem).fuse(head)
    axle = cq.Solid.makeCylinder(P.AXLE_DIAM_MM / 2, P.MODULE_WIDTH_MM + 20, V(cx, min(cy, yc) - 70, axle_z), ydir)
    carrier = carrier.cut(cq.Solid.makeCylinder(P.AXLE_DIAM_MM / 2 + 0.1, t + 2, V(cx, cy - t / 2 - 1, axle_z), ydir))
    # connector ports on the inboard face (M12 data + M12 power/ID)
    for dx in (-45, 45):
        carrier = carrier.cut(cq.Solid.makeCylinder(8.5, 12, V(cx + dx, cy - sy * (t / 2 + 1), axle_z + 45), V(0, sy, 0)))
    return [tire, rim, motor, axle], carrier


def seat(nodes):
    f = nodes["FTIP_L"]; r = nodes["RTIP_L"]; s = nodes["SEAT_L"]
    pts_top = [(f[0], f[2] + 55), (f[0] - 60, f[2] + 20), (s[0] + 40, s[2] + 10), (s[0], s[2]), (s[0] - 60, s[2] + 25), (r[0] + 30, r[2] - 40), (r[0], r[2] + 55)]
    pts_bot = [(x, z - 4) for (x, z) in reversed(pts_top)]
    wp = cq.Workplane("XZ").moveTo(*pts_top[0]).spline(pts_top[1:], includeCurrent=True)
    wp = wp.lineTo(*pts_bot[0]).spline(pts_bot[1:], includeCurrent=True).close()
    width = 2 * P.FRONT_TIP[1] + 60
    return wp.extrude(width / 2, both=True).val()


def assembly():
    nodes = P.frame_nodes()
    parts = {"joiners": [], "tubes": [], "cords": [], "wheels": [], "carriers": [], "seat": None}
    for n in nodes:
        if n.startswith("SEAT"):
            continue
        parts["joiners"].append(joiner(n, nodes))
    for m, a, b, kind in P.frame_members():
        u, L = unit(nodes[a], nodes[b])
        pa, pb = V(*nodes[a]), V(*nodes[b])
        if kind == "tube":
            parts["tubes"].append(cq.Solid.makeCylinder(TUBE_R, L - 2 * SOCKET_START, pa + u * SOCKET_START, u))
        elif kind == "cord":
            parts["cords"].append(cq.Solid.makeCylinder(2.5, L - 2 * CORE_R, pa + u * CORE_R, u))
    for pos_name, side in (("DOCK_FL", 1), ("DOCK_RL", 1), ("DOCK_FR", -1), ("DOCK_RR", -1)):
        w, c = wheel_module(nodes[pos_name], side)
        parts["wheels"] += w
        parts["carriers"].append(c)
    parts["seat"] = seat(nodes)
    return nodes, parts


def tighten_svg(path, margin=12):
    """CadQuery's SVG exporter leaves large margins; recompute the viewBox from the drawn paths."""
    import re
    txt = open(path).read()
    m = re.search(r'scale\(([-\d.e]+),\s*([-\d.e]+)\)\s*translate\(([-\d.e]+),\s*([-\d.e]+)\)', txt)
    if not m:
        return
    sx, sy, tx, ty = map(float, m.groups())
    xs, ys = [], []
    for d in re.findall(r'd="([^"]+)"', txt):
        nums = re.findall(r'[-\d.e]+', d)
        pts = [float(n) for n in nums if n not in ('-', '.', 'e')]
        xs += [sx * (pts[i] + tx) for i in range(0, len(pts) - 1, 2)]
        ys += [sy * (pts[i + 1] + ty) for i in range(0, len(pts) - 1, 2)]
    if not xs:
        return
    x0, x1, y0, y1 = min(xs) - margin, max(xs) + margin, min(ys) - margin, max(ys) + margin
    w, h = x1 - x0, y1 - y0
    txt = re.sub(r'<svg\s+xmlns:svg="[^"]+"\s+xmlns="[^"]+"\s+width="[^"]+"\s+height="[^"]+"\s*>',
                 f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{x0:.1f} {y0:.1f} {w:.1f} {h:.1f}" width="{w:.0f}" height="{h:.0f}">', txt, count=1)
    open(path, 'w').write(txt)


def export_all():
    nodes, parts = assembly()
    # individual printed parts
    for n in nodes:
        if n.startswith("SEAT"):
            continue
        j = joiner(n, nodes)
        # re-centre each joiner at the origin for printing
        j = j.translate(V(*nodes[n]) * -1)
        cq.exporters.export(j, os.path.join(OUT, f"joiner_{n}.step"))
        cq.exporters.export(j, os.path.join(OUT, f"joiner_{n}.stl"), tolerance=0.05, angularTolerance=0.1)
    w, c = wheel_module(nodes["DOCK_FL"], 1)
    c0 = c.translate(V(-nodes["DOCK_FL"][0], -P.DOCK_Y, -P.WHEEL_R_MM))
    cq.exporters.export(c0, os.path.join(OUT, "wheel_module_carrier.step"))
    cq.exporters.export(c0, os.path.join(OUT, "wheel_module_carrier.stl"), tolerance=0.05, angularTolerance=0.1)
    module = cq.Compound.makeCompound(w + [c])
    cq.exporters.export(module, os.path.join(OUT, "wheel_module_assembly.step"))
    # full vehicle
    everything = parts["joiners"] + parts["tubes"] + parts["cords"] + parts["wheels"] + parts["carriers"] + [parts["seat"]]
    assy = cq.Compound.makeCompound(everything)
    cq.exporters.export(assy, os.path.join(OUT, "playa_sprawler_assembly.step"))
    frame_only = cq.Compound.makeCompound(parts["joiners"] + parts["tubes"] + parts["cords"] + [parts["seat"]])
    cq.exporters.export(frame_only, os.path.join(OUT, "frame_and_seat.step"))
    # Orthographic views: rotate the model so the wanted (right, up, camera) frame maps to (x, y, z),
    # then project along z. This sidesteps the exporter's unpredictable up-vector for horizontal views.
    # side: rotate -90 deg about x -> (x, z, -y): screen right = +x (front), up = +z, camera on the right side
    # front: rotate -120 deg about (1,1,1) -> (y, z, x): screen right = +y, up = +z, camera ahead of the vehicle
    views = {"iso": None, "top": ("z", 0), "side": ((1, 0, 0), -90), "front": ((1, 1, 1), -120)}
    for name, rot in views.items():
        shape, d = assy, (2, -2, 3)
        if rot is not None:
            shape, d = assy, (0, 0, 1)
            if rot[1]:
                shape = assy.rotate(V(0, 0, 0), V(*rot[0]), rot[1])
        cq.exporters.export(shape, os.path.join(OUT, f"view_{name}.svg"),
                            opt={"width": 900, "height": 600, "marginLeft": 20, "marginTop": 20, "showAxes": False,
                                 "projectionDir": d, "strokeWidth": 0.6, "strokeColor": (30, 30, 30),
                                 "hiddenColor": (160, 160, 160), "showHidden": False})
        tighten_svg(os.path.join(OUT, f"view_{name}.svg"))
    cq.exporters.export(cq.Compound.makeCompound(w + [c]), os.path.join(OUT, "view_wheel_module.svg"),
                        opt={"width": 600, "height": 500, "showAxes": False, "projectionDir": (2, -2, 3),
                             "strokeWidth": 0.6, "strokeColor": (30, 30, 30), "showHidden": False})
    tighten_svg(os.path.join(OUT, "view_wheel_module.svg"))
    # bill of geometry for the docs
    with open(os.path.join(OUT, "geometry.md"), "w") as f:
        f.write("| Node | x | y | z |\n|---|---|---|---|\n")
        for n, (x, y, z) in nodes.items():
            f.write(f"| {n} | {x:.0f} | {y:.0f} | {z:.0f} |\n")
        f.write("\n| Member | From | To | Kind | Length (mm) |\n|---|---|---|---|---|\n")
        for m, a, b, k in P.frame_members():
            f.write(f"| {m} | {a} | {b} | {k} | {unit(nodes[a], nodes[b])[1]:.0f} |\n")
    print("exported to", OUT)


if __name__ == "__main__":
    export_all()
