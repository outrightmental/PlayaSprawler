"""
Playa Sprawler — single source of truth for design parameters.

Every analysis script, the CAD generator and the site read from here.
Change a number here, re-run `python run_all.py`, and the derived numbers
(member forces, safety factors, range, mass margin, turn-speed limits)
update everywhere.

Units: millimetres, kilograms, newtons, seconds — unless a name says otherwise.
Coordinate frame: x forward, y left, z up. Ground plane z = 0.
"""

PROJECT = "Playa Sprawler"
VERSION = "0.1.0"
G = 9.81

# ---------------------------------------------------------------------------
# 1. Rating classes — the "safety DNA". A vehicle's rating is the minimum
#    rating of every load-path part installed on it.
# ---------------------------------------------------------------------------
RATING_CLASSES = {"PS-100": 100.0, "PS-125": 125.0, "PS-150": 150.0}  # payload kg (rider + carried gear)
DEFAULT_CLASS = "PS-125"

# ---------------------------------------------------------------------------
# 2. Hard external constraints (verified Sept 2026, see docs/sources.md)
# ---------------------------------------------------------------------------
BAG_LINEAR_IN_MAX = 62.0          # Burner Express: length + width + depth per luggage item
BAG_MASS_MAX_LB = 50.0            # Burner Express: per luggage item
BAG_MASS_MAX_KG = BAG_MASS_MAX_LB * 0.45359237
BAG_OUTER_MM = (660.0, 450.0, 450.0)     # chosen duffel, 61.4 linear inches
BAG_WALL_MM = 10.0                       # padding/fabric allowance per side
V_MAX_KMH = 8.0                   # Black Rock City vehicle speed limit is 5 mph

# ---------------------------------------------------------------------------
# 3. Wheel module
# ---------------------------------------------------------------------------
TIRE_SPEC = "16 x 3.0 (ISO 76-305), folding bead, tubeless-ready"
WHEEL_OD_MM = 457.0               # inflated
WHEEL_OD_DEFLATED_MM = 400.0      # packed (tires deflated for transport)
TIRE_WIDTH_MM = 76.0
WHEEL_R_MM = WHEEL_OD_MM / 2
CARRIER_THICKNESS_MM = 45.0       # inboard 'brick': battery + controller + node
CARRIER_GAP_MM = 5.0
OUTBOARD_NUT_MM = 9.0
MODULE_WIDTH_MM = CARRIER_THICKNESS_MM + CARRIER_GAP_MM + TIRE_WIDTH_MM + OUTBOARD_NUT_MM  # 135
DOCK_Z_MM = 300.0                 # top face of the module rail above ground
AXLE_DIAM_MM = 12.0               # typical mini geared hub motor axle (M12 with flats)
AXLE_FLAT_MM = 10.0               # across flats
AXLE_CANTILEVER_MM = 45.0         # wheel centre plane -> near edge of the torque clamp
AXLE_YIELD_MPA = 785.0            # 40Cr Q&T hub-motor axle steel — MUST be verified per motor by test
MOTOR = {
    "type": "mini geared hub motor, no-clutch (regen-capable) variant preferred",
    "nominal_W": 250.0, "peak_W": 500.0,
    "torque_rated_Nm": 20.0, "torque_peak_Nm": 35.0,
    "mass_kg": 1.90,
}
BATTERY = {
    "config": "7s1p 18650, 3.4 Ah",
    "v_nom": 25.2, "v_max": 29.4, "v_min": 21.0,
    "wh": 85.7, "usable_frac": 0.85, "mass_kg": 0.41,
    "discharge_A_max": 15.0,
}
POWER_BUS_V_NOM = 25.2            # the vehicle power bus runs at pack voltage (SELV)
POWER_BUS_PORT_A_MAX = 5.0        # per-port eFuse limit; traction current never crosses a dock

# ---------------------------------------------------------------------------
# 4. Frame geometry (mm). Two side hubs joined by the front seat rail;
#    four legs down to the wheel-module docks; two rear poles up to the
#    backrest tips; tension cords close the truss.
# ---------------------------------------------------------------------------
HUB_Y = 180.0;  HUB_Z = 450.0
DOCK_X = 330.0; DOCK_Y = 280.0            # dock centre; the wheel plane sits further outboard
FRONT_TIP = (60.0, 180.0, 600.0)
REAR_TIP = (-340.0, 230.0, 800.0)
WHEEL_PLANE_Y = DOCK_Y + CARRIER_THICKNESS_MM / 2 + CARRIER_GAP_MM + TIRE_WIDTH_MM / 2  # 345.5
TRACK_MM = 2 * WHEEL_PLANE_Y
WHEELBASE_MM = 2 * DOCK_X
SEAT_PAN_Z_MM = 530.0             # sling low point (estimate; fabric-dependent)

SEAT_SAG_MM = 150.0               # sling low point below the tip-to-tip chord

def frame_nodes():
    """Node coordinates. Suffix L/R = left(+y)/right(-y); F/R prefix on docks = front/rear.
    SEAT_L/R are the sling low points where the seated weight is applied."""
    n = {}
    for s, sy in (("L", 1), ("R", -1)):
        n[f"HUB_{s}"] = (0.0, sy * HUB_Y, HUB_Z)
        n[f"DOCK_F{s}"] = (DOCK_X, sy * DOCK_Y, DOCK_Z_MM)
        n[f"DOCK_R{s}"] = (-DOCK_X, sy * DOCK_Y, DOCK_Z_MM)
        n[f"FTIP_{s}"] = (FRONT_TIP[0], sy * FRONT_TIP[1], FRONT_TIP[2])
        n[f"RTIP_{s}"] = (REAR_TIP[0], sy * REAR_TIP[1], REAR_TIP[2])
        mx = (FRONT_TIP[0] + REAR_TIP[0]) / 2
        my = sy * (FRONT_TIP[1] + REAR_TIP[1]) / 2
        mz = (FRONT_TIP[2] + REAR_TIP[2]) / 2 - SEAT_SAG_MM
        n[f"SEAT_{s}"] = (mx, my, mz)
    return n

def frame_members():
    """(name, node_a, node_b, kind). kind: 'tube' (compression/tension), 'cord' (tension only),
    'fabric' (seat canvas edge, tension only)."""
    m = [
        ("SEAT_RAIL", "HUB_L", "HUB_R", "tube"),          # front seat rail / crossbar
        ("CTRL_RAIL", "DOCK_FL", "DOCK_FR", "tube"),      # front control rail (pedals/levers mount here)
        ("TOP_RAIL", "RTIP_L", "RTIP_R", "tube"),         # backrest top rail / push handle
        ("SEAT_CROSS", "SEAT_L", "SEAT_R", "fabric"),     # canvas transverse tension
        ("SEAT_FRONT_EDGE", "FTIP_L", "FTIP_R", "fabric"),  # canvas front edge between the two front posts
        ("REAR_CORD", "DOCK_RL", "DOCK_RR", "cord"),
        ("XF_1", "DOCK_FL", "HUB_R", "cord"), ("XF_2", "DOCK_FR", "HUB_L", "cord"),
        ("XR_1", "DOCK_RL", "HUB_R", "cord"), ("XR_2", "DOCK_RR", "HUB_L", "cord"),
    ]
    for s, o in (("L", "R"), ("R", "L")):
        m += [
            (f"LEG_F{s}", f"HUB_{s}", f"DOCK_F{s}", "tube"),
            (f"LEG_R{s}", f"HUB_{s}", f"DOCK_R{s}", "tube"),
            (f"POLE_{s}", f"HUB_{s}", f"RTIP_{s}", "tube"),
            (f"POST_{s}", f"HUB_{s}", f"FTIP_{s}", "tube"),          # short front seat post
            (f"SIDE_CORD_{s}", f"DOCK_F{s}", f"DOCK_R{s}", "cord"),
            (f"FORESTAY_{s}", f"FTIP_{s}", f"DOCK_F{s}", "cord"),     # holds the front post against the sling pull
            (f"AFTSTAY_{s}", f"FTIP_{s}", f"DOCK_R{s}", "cord"),      # braces the front post laterally, runs outboard of the seat
            (f"BACKSTAY_{s}", f"RTIP_{s}", f"DOCK_R{o}", "cord"),     # crossed: also braces the backrest laterally
            (f"SIDE_STRAP_{s}", f"FTIP_{s}", f"RTIP_{s}", "fabric"),  # straight webbing along the seat side edge
            (f"SLING_F{s}", f"FTIP_{s}", f"SEAT_{s}", "fabric"),
            (f"SLING_R{s}", f"SEAT_{s}", f"RTIP_{s}", "fabric"),
        ]
    return m

# ---------------------------------------------------------------------------
# 5. Materials
# ---------------------------------------------------------------------------
TUBE = {
    "spec": "roll-wrapped carbon fibre tube, 25 mm OD x 22 mm ID (1.5 mm wall)",
    "od": 25.0, "id": 22.0,
    "E_MPa": 80_000.0,            # conservative axial modulus for mixed-layup roll-wrapped tube
    "sigma_ult_MPa": 450.0,       # conservative flexural/compressive ultimate; verify by 3-point bend test
    "density_g_cc": 1.55,
}
CORD = {
    "spec": "5 mm Dyneema SK78 single braid; spliced eyes preferred, knots allowed with the 0.5 knockdown below",
    "mbl_N": 18_000.0, "knot_knockdown": 0.5, "E_MPa": 40_000.0, "area_mm2": 19.6,
}
FABRIC = {
    "spec": "1000D nylon Cordura or 600D polyester canvas, UV-stable; edges reinforced with 25 mm tubular webbing",
    "edge_strength_N": 6_000.0,   # webbing-reinforced edge, sewn; verify by pull test
    "E_MPa": 1_500.0, "area_mm2": 40.0,   # effective edge stiffness (webbing + fabric)
}
PRINT = {
    "spec": "PA12-CF / PAHT-CF / PET-CF, 100% infill in load regions, annealed where the material calls for it",
    "sigma_ult_datasheet_MPa": 80.0,
    "knockdown": 0.5,             # anisotropy, layer adhesion, moisture, printer variance
    "density_g_cc": 1.20,
}
SF = {"tube": 2.0, "cord": 3.0, "fabric": 3.0, "print": 1.5, "axle": 1.5}   # applied on top of the knockdowns above

# ---------------------------------------------------------------------------
# 6. Load cases (multiples of payload weight W = payload_kg * g unless noted)
# ---------------------------------------------------------------------------
LOAD_CASES = {
    "LC1": {"name": "Static seated", "vert": 1.0, "lat": 0.0, "back": 0.0, "kind": "deflection"},
    "LC2": {"name": "Dynamic vertical (bump/drop)", "vert": 2.5, "lat": 0.0, "back": 0.0, "kind": "ultimate"},
    "LC3": {"name": "Lateral skid / turn", "vert": 1.0, "lat": 0.6, "back": 0.0, "kind": "ultimate"},
    "LC5": {"name": "Backrest lean", "vert": 1.0, "lat": 0.0, "back": 0.5, "kind": "ultimate"},
}
PROOF_FACTOR = 1.5                # every load-path part is proof-loaded to 1.5 x static before marking
SLING_SAG_RATIO = 0.33            # seat fabric sag / chord; sets the horizontal pull on the tips
FRONT_SHARE = 0.45                # share of seated weight on the front tips (rest on rear tips)

# ---------------------------------------------------------------------------
# 7. Mass budget targets (kg). The one-bag pack is the binding constraint.
# ---------------------------------------------------------------------------
MASS_BUDGET = {
    "Wheel module (x4)": 4 * 4.35,
    "Frame tubes (carbon)": 0.74,
    "Joiners (printed) + hardware": 0.90,
    "Cords + tensioners": 0.15,
    "Seat canvas": 0.70,
    "Control modules (x2)": 2 * 0.30,
    "Bus node (switch + supervisor + power)": 0.55,
    "Harness (M12 data + power)": 0.65,
    "Bag": 0.80,
}
WHEEL_MODULE_BREAKDOWN = {
    "hub motor": MOTOR["mass_kg"], "rim + spokes": 0.62, "tire (tubeless) + sealant": 0.80,
    "battery pack": BATTERY["mass_kg"], "controller + node board": 0.15,
    "carrier (printed + Al torque plates)": 0.35, "connectors + fasteners": 0.10,
}

# ---------------------------------------------------------------------------
# 8. Performance model inputs
# ---------------------------------------------------------------------------
CRR = {"playa, hard": 0.02, "playa, soft/dusty": 0.06, "beach, wet firm": 0.05, "beach, dry loose": 0.20}
GRADE_MAX = 0.10
DRIVE_EFF = 0.70
AUX_W = 10.0
A_LAT_MAX_G = 0.25                # turn-rate limiter target (half the geometric tipping threshold)
ACCEL_MAX_G = 0.25
DECEL_MAX_G = 0.30
RIDER_CG_ABOVE_SEAT_MM = 250.0
VEHICLE_CG_Z_MM = 300.0
SAND_PRESSURE_DRY_KPA = 40.0      # target ground pressure for dry loose sand (beach wheelchairs use 20-30)
COMMS_TIMEOUT_MS = 200            # wheel module stops if no valid tread command within this window
STOP_RAMP_MS = 300
