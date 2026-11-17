import math
from lib import *
from bld import siding, corrug, slab, post

STEEL = "#6d7076"
YELLOW = "#f2b134"


def hydraulic(m, x, y0, z0, y1, z1, mat=None):
    mat = mat or metal("#2a2d33")
    dy, dz = y1 - y0, z1 - z0
    n = max(2, int(max(abs(dy), abs(dz)) / 1.2))
    for i in range(n):
        t = i / n
        yy = y0 + dy * t
        zz = z0 + dz * t
        m.box((x - 0.35, yy, zz - 0.35), (x + 0.35, yy + 0.7, zz + 0.35), mat, skip=())


def hose(m, pts, mat=None, t=0.35):
    mat = mat or paint("#1d1d20", noise=3)
    for (a, b) in zip(pts, pts[1:]):
        x0, y0, z0 = a
        x1, y1, z1 = b
        m.box((min(x0, x1) - t, min(y0, y1) - t, min(z0, z1) - t), (max(x0, x1) + t, max(y0, y1) + t, max(z0, z1) + t), mat, skip=())


def hitch(m, w=9.0, y=5.0, z0=-12.0, z1=-1.5, color=STEEL):
    steel = metal(color)
    dark = metal("#2a2d33")
    for s in (-1, 1):
        m.box((s * w - 0.8, y, z0), (s * w + 0.8, y + 1.6, z1), steel, skip=())
        m.box((s * w - 1.3, y - 0.4, z0 - 0.8), (s * w + 1.3, y + 2.0, z0 + 0.8), dark, skip=())
        m.box((s * w - 0.45, y + 2.0, z0 - 0.45), (s * w + 0.45, y + 3.2, z0 + 0.45), metal("#c9962f"), skip=())
    m.box((-1.0, y + 7.0, z0 - 0.3), (1.0, y + 8.4, z0 + 2.6), dark, skip=())
    m.box((-0.5, y + 1.6, z0 + 0.4), (0.5, y + 7.2, z0 + 1.2), steel, rot=("x", -22.5, (0, y + 1.6, z0 + 0.8)), skip=())
    m.box((-0.4, y + 3.0, z0 + 0.8), (0.4, y + 3.8, z1 - 3), steel, skip=())


def attach_tiller():
    m = Model("attachment_tiller", 31)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    orange = paint("#d4631b", noise=4)
    orange2 = P(orange, ov_stripe("#2a2a2a", 0.5, 0.5, False))
    hitch(m, 9.0, 5.0, -12.0, -1.5)
    m.box((-12.5, 8.0, -2.5), (12.5, 10.8, 1.8), P(orange, ov_text("TILL-9", "#f4e3c1", 6)))
    m.box((-12.7, 7.8, -2.7), (-12.0, 11.0, 2.0), steel, skip=())
    m.box((12.0, 7.8, -2.7), (12.7, 11.0, 2.0), steel, skip=())
    m.box((-3.4, 10.8, -2.2), (3.4, 16.0, 1.0), P(dark, ov_vents("#55585e", 4, 0.8)))
    m.box((-2.0, 16.0, -1.4), (2.0, 17.4, 0.4), steel)
    m.box((-0.9, 8.6, -9.0), (0.9, 10.2, -2.5), P(paint(YELLOW, noise=3), ov_stripe("#2a2a2a", 0.5, 0.5, False)), skip=())
    m.box((-1.4, 8.2, -10.2), (1.4, 10.6, -9.0), dark, skip=())
    m.box((10.2, 6.6, -2.2), (13.6, 10.4, 2.0), P(steel, ov_dots("#2a2d33", 3, 1)))
    for s in (-1, 1):
        m.box((s * 12.4 - 0.7, 2.0, -3.0), (s * 12.4 + 0.7, 11.0, 4.4), P(orange, ov_stripe("#2a2d33", 0.5, 0.35, True)))
        m.box((s * 12.9 - 0.3, 3.6, -1.0), (s * 12.9 + 0.3, 4.4, 3.0), steel, skip=())
        for z in (-1.8, 3.0):
            m.box((s * 13.0 - 0.3, 6.0, z - 0.3), (s * 13.0 + 0.3, 6.8, z + 0.3), metal("#c9962f"), skip=())
        m.box((s * 12.4 - 0.9, 0.8, -3.2), (s * 12.4 + 0.9, 2.2, 4.6), steel, skip=())
    m.p("rotor")
    cyl_x(m, 0, 4.5, 1, 1.2, 24, metal("#55585e"))
    for i in range(-6, 7):
        x = i * 1.85
        oct_prism(m, "x", x, 4.5, 1, 3.5, 0.45, metal("#7b7e84"))
        for j, (ang, side) in enumerate(((22.5, 1), (-22.5, -1))):
            sgn = 1 if (i + j) % 2 == 0 else -1
            m.box((x - 0.35 + 0.35 * sgn * 0.5, 0.3, 0.2), (x + 0.35 + 0.35 * sgn * 0.5, 3.4, 1.6), steel, rot=("x", ang * (1 if i % 2 else -1), (x, 4.5, 1)), skip=())
            m.box((x - 0.35 + 0.35 * sgn * 0.5, 5.6, -0.4), (x + 0.35 + 0.35 * sgn * 0.5, 8.4, 1.0), steel, rot=("x", -ang * (1 if i % 2 else -1), (x, 4.5, 1)), skip=())
    m.p("body")
    shield = P(orange2, ov_vents("#7a3a10", 4, 1.0))
    m.box((-12.6, 10.6, 3.2), (12.6, 11.6, 4.0), shield, skip=())
    m.box((-12.6, 7.6, 3.6), (12.6, 11.0, 4.2), shield, rot=("x", -22.5, (0, 10.6, 3.6)), skip=())
    m.box((-12.5, 4.6, 5.2), (12.5, 8.4, 5.8), P(orange, ov_stripe("#2a2d33", 0.5, 0.5, False)), rot=("x", -22.5, (0, 8.4, 5.2)), skip=())
    for x in (-10, -4, 4, 10):
        for k in range(4):
            m.box((x - 0.25, 7.4 - k * 1.1, 5.4 + k * 0.9), (x + 0.25, 8.3 - k * 1.1, 6.2 + k * 0.9), steel, skip=())
    m.box((-12.0, 4.0, 5.9), (12.0, 4.5, 6.3), hazard(YELLOW, "#1e1e1e", 2), skip=())
    for s in (-1, 1):
        m.box((s * 9 - 1.0, 6.0, 6.2), (s * 9 + 1.0, 7.6, 6.9), light("#ff3b30"), skip=())
        m.box((s * 6 - 0.8, 9.2, 4.0), (s * 6 + 0.8, 10.4, 4.7), paint("#e8b81a"), skip=())
    m.box((-1.4, 2, 6.8), (1.4, 5, 9.0), diamond())
    m.box((-0.5, 0.5, 7.6), (0.5, 3, 8.4), steel)
    return m


def attach_seeder():
    m = Model("attachment_seeder", 41)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    green = paint("#4a9a3a", noise=4)
    green2 = P(green, ov_frame("#2d6a22", 0.6))
    yellow = paint(YELLOW, noise=4)
    hitch(m, 9.0, 4.0, -13.0, -2.0, "#4a4d52")
    m.box((-13.0, 7.2, -1.4), (13.0, 9.6, 1.4), dark)
    m.box((-13.0, 7.6, 1.4), (13.0, 9.0, 3.0), steel)
    m.box((-1.2, 9.6, -4.4), (1.2, 12.8, 0.4), steel)
    for s in (-1, 1):
        m.box((s * 13 - 0.7, 7.0, -3.6), (s * 13 + 0.7, 10.0, 3.4), yellow, skip=())
    for i in range(4):
        x = -9.0 + i * 6.0
        m.box((x - 2.4, 9.6, -2.4), (x + 2.4, 12.6, 2.4), P(green2, ov_dots("#1f4a18", 4, 1)))
        m.box((x - 3.2, 12.6, -3.2), (x + 3.2, 15.8, 3.2), P(yellow, ov_dots("#a97a1a", 4, 1)))
        m.box((x - 3.5, 15.8, -3.5), (x + 3.5, 17.0, 3.5), P(paint("#7c5a14"), ov_frame("#4a3408", 0.5)), skip=())
        m.box((x - 1.2, 17.0, -1.2), (x + 1.2, 17.9, 1.2), steel, skip=())
        m.box((x + 3.2, 12.8, -1.4), (x + 3.5, 15.2, 1.4), glass("#cfe8f5", 140), skip=())
        m.box((x - 0.3, 17.0, 3.5), (x + 0.3, 18.2, 4.2), metal("#c9962f"), skip=())
        m.box((x - 0.9, 8.6, -1.0), (x + 0.9, 9.6, 1.0), dark, skip=())
        m.box((x - 0.5, 3.8, -0.5), (x + 0.5, 9.0, 0.5), paint("#3a3a3a"), skip=())
        m.box((x - 0.4, 3.0, 0.8), (x + 0.4, 7.5, 1.3), paint("#2a2a2a"), skip=())
        m.box((x - 0.6, 5.6, 1.1), (x + 0.6, 6.4, 3.8), dark, skip=())
        for sd in (-1, 1):
            m.box((x - 0.2 + sd * 0.9, 1.0, -2.6), (x + 0.2 + sd * 0.9, 4.8, -1.0), metal("#cfd3d8"), rot=("x", 22.5, (x + sd * 0.9, 4.0, -1.8)), skip=())
        m.box((x - 0.9, 0.3, -2.2), (x + 0.9, 3.0, 0.2), steel, rot=("x", 22.5, (x, 3.0, -1.0)), skip=())
        m.box((x - 0.5, 0.4, 2.2), (x + 0.5, 2.8, 4.2), steel, rot=("x", -22.5, (x, 2.8, 3.0)), skip=())
        m.box((x - 0.5, 2.8, 4.2), (x + 0.5, 3.6, 6.4), steel, skip=())
        hose(m, [(x, 12.6, 0.0), (x, 9.0, 0.0)], t=0.3)
    for s in (-1, 1):
        for k in range(6):
            hx = s * (13 + k * 1.6)
            m.box((hx - 0.2, 8.0 + k * 0.1, -0.6), (hx + 1.4, 8.6 + k * 0.1, 0.6), steel, skip=()) if abs(hx) < 23 else None
        m.box((s * 14 - 0.3, 8.0, 0.0), (s * 22 + 0.3, 8.8, 0.8), P(green, ov_stripe("#f4f0e6", 0.5, 0.5, False)), skip=())
        m.box((s * 22 - 0.5, 6.0, -0.4), (s * 22 + 0.5, 11.0, 1.2), paint(YELLOW), skip=())
        m.box((s * 4 - 0.5, 8.0, -2.0), (s * 4 + 0.5, 9.4, 3.6), metal("#2a2d33"), skip=())
        wheel(m, s * 13.8, 3.4, 1.4, 3.4, 1.9, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
        m.box((s * 12.6 - 0.4, 3.4, 0.6), (s * 12.6 + 0.4, 9.2, 2.2), steel)
    m.box((-1.6, 5.0, -2.4), (1.6, 7.0, 2.8), steel, skip=())
    hydraulic(m, -4.0, 9.6, -3.2, 15.0, -8.8)
    hydraulic(m, 4.0, 9.6, -3.2, 15.0, -8.8)
    m.box((-6.0, 6.4, 3.2), (6.0, 7.4, 4.2), hazard(YELLOW, "#1e1e1e", 2), skip=())
    return m


def attach_harvester():
    m = Model("attachment_harvester", 51)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    red = paint("#b8312a", noise=4)
    redf = P(red, ov_shadow(0.2))
    yellow = paint(YELLOW, noise=4)
    hitch(m, 8.0, 4.0, -4.0, 2.0, "#4a4d52")
    m.box((-13.4, 3.0, -13.0), (13.4, 5.6, -8.0), P(red, ov_text("HARVEST", "#f4e3c1", 6)))
    m.box((-13.4, 5.6, -13.4), (13.4, 12.4, -12.2), P(red, ov_dots("#7c1f1b", 6, 1)))
    for s in (-1, 1):
        m.box((s * 13.4 - 0.7, 3.0, -13.6), (s * 13.4 + 0.7, 15.0, -2.0), redf)
        m.box((s * 13.4 - 0.5, 14.6, -14.6), (s * 13.4 + 0.5, 15.8, -8.0), yellow, skip=())
        m.box((s * 13.4 - 0.9, 5.4, -15.6), (s * 13.4 + 0.9, 13.0, -13.0), P(red, ov_stripe("#f4f0e6", 0.5, 0.6, False)), rot=("x", -22.5, (s * 13.4, 5.4, -13.0)), skip=())
    m.box((-13.4, 12.4, -13.6), (13.4, 13.6, -11.8), yellow, skip=())
    m.box((-13.4, 5.6, -12.2), (13.4, 7.0, -2.0), metal("#9aa0a6"))
    for i in range(-12, 13):
        x = i * 1.1
        m.box((x - 0.4, 1.4, -15.8), (x + 0.4, 3.0, -13.0), steel, skip=())
        m.box((x - 0.5, 1.8, -17.4), (x + 0.5, 2.5, -15.8), metal("#d7dbe0"), skip=())
        if i % 2 == 0:
            m.box((x - 0.3, 3.0, -13.0), (x + 0.3, 4.4, -12.4), dark, skip=())
    m.p("reel")
    cyl_x(m, 0, 11.5, -14, 0.8, 27, metal("#55585e"))
    for i in range(-6, 7):
        x = i * 2.1
        oct_prism(m, "x", x, 11.5, -14, 3.8, 0.55, metal("#7b8188"))
    for a in range(6):
        ang = a * 60
        rad = math.radians(ang)
        yy = 11.5 + math.sin(rad) * 3.6
        zz = -14 + math.cos(rad) * 3.6
        m.box((-13.0, yy - 0.45, zz - 0.45), (13.0, yy + 0.45, zz + 0.45), metal("#cfd3d8"), skip=())
        for i in range(-6, 7, 2):
            x = i * 2.0
            m.box((x - 0.2, yy - 1.4, zz - 0.2), (x + 0.2, yy + 1.4, zz + 0.2), metal("#e8eaed"), skip=())
    m.p("body")
    m.box((-4.6, 5.6, -2.0), (4.6, 14.0, 3.5), redf)
    m.box((-3.6, 6.4, -2.6), (3.6, 9.0, -2.0), P(dark, ov_vents("#55585e", 3, 0.6)), skip=())
    m.box((-7.0, 8.0, 3.5), (7.0, 17.0, 10.0), P(red, ov_frame("#7c1f1b", 0.7), ov_text("BIN", "#f4e3c1", 6)))
    m.box((-7.4, 17.0, 3.1), (7.4, 18.2, 10.4), yellow, skip=())
    m.box((-6.2, 9.6, 10.0), (6.2, 15.8, 10.8), glass("#cfe8f5", 120), skip=())
    for s in (-1, 1):
        m.box((s * 7.6 - 0.4, 9.0, 3.5), (s * 7.6 + 0.4, 16.0, 10.0), steel, skip=())
    m.box((3.0, 17.0, 6.0), (5.2, 24.0, 8.2), metal("#7b8188"), skip=())
    m.box((3.0, 22.6, 6.0), (9.4, 24.0, 8.2), metal("#7b8188"), skip=())
    m.box((8.0, 18.0, 6.2), (9.4, 22.6, 8.0), metal("#9aa0a6"), skip=())
    m.box((-4.5, 4.0, 9.5), (4.5, 8.0, 12.5), dark)
    m.box((-2, 5.5, 12.5), (2, 7.5, 14.5), steel)
    hydraulic(m, -5.0, 6.0, -3.0, 14.0, -9.0)
    hydraulic(m, 5.0, 6.0, -3.0, 14.0, -9.0)
    for s in (-1, 1):
        wheel(m, s * 7.8, 2.8, 6.4, 2.8, 2.0, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
        m.box((s * 7.8 - 0.4, 2.8, 5.4), (s * 7.8 + 0.4, 8.0, 7.4), steel, skip=())
        m.box((s * 11.0 - 0.8, 13.0, -13.8), (s * 11.0 + 0.8, 14.6, -12.6), light("#ffb347"), skip=())
        m.box((s * 6 - 1.0, 17.8, 10.4), (s * 6 + 1.0, 19.0, 11.0), light("#ff3b30"), skip=())
    return m


def attach_sprayer():
    m = Model("attachment_sprayer", 61)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    blue = "#2f6fbf"
    tank = P(paint("#e9e4d2", noise=3), ov_stripe(blue, 0.5, 2.2, False), ov_stripe("#f4f0e6", 0.2, 0.6, False))
    hitch(m, 5.0, 3.0, -7.0, 0.0, "#4a4d52")
    cyl_x(m, 0, 11.4, 2, 5.6, 15, {"all": tank, "east": P(paint("#d8d2bd"), ov_frame("#9aa0a6", 0.6)), "west": P(paint("#d8d2bd"), ov_frame("#9aa0a6", 0.6))})
    for x in (-5.2, 5.2):
        m.box((x - 0.4, 5.6, -2.6), (x + 0.4, 9.2, 6.6), steel, skip=())
    for x in (-3.5, 3.5):
        m.box((x - 1.2, 5.2, -2.8), (x + 1.2, 6.0, 6.8), dark, skip=())
    m.box((-1.6, 16.6, 0.4), (1.6, 18.6, 3.6), P(metal(blue), ov_frame("#1d4a85", 0.5)), skip=())
    m.box((-1.1, 18.6, 0.9), (1.1, 19.2, 3.1), steel, skip=())
    m.box((-0.3, 19.2, 1.7), (0.3, 20.2, 2.3), steel, skip=())
    m.box((5.4, 6.4, -1.0), (6.6, 15.8, 0.2), glass("#cfe8f5", 140), skip=())
    for yy in range(7, 16, 2):
        m.box((5.4, yy, -1.2), (6.9, yy + 0.3, 0.3), paint("#f4f0e6"), skip=())
    m.box((-1.8, 7.6, 5.4), (1.8, 12.8, 6.4), P(paint("#d8d2bd"), ov_text("L", blue, 5)))
    m.box((-5.0, 6.0, -5.4), (5.0, 8.4, -2.4), dark)
    m.box((-1.8, 6.4, -6.4), (1.8, 8.0, -5.4), metal(blue), skip=())
    cyl_x(m, 0, 7.2, -4.0, 1.6, 3.6, {"all": metal("#9aa0a6")})
    m.box((-0.5, 6.4, -4.4), (0.5, 8.2, 0.4), dark, skip=())
    boom = P(steel, ov_stripe("#3a3d42", 0.5, 0.4, False))
    m.box((-23.6, 6.0, 7.2), (23.6, 7.2, 8.4), boom, skip=())
    m.box((-23.6, 8.4, 7.4), (23.6, 8.9, 8.2), boom, skip=())
    for x in range(-22, 23, 4):
        m.box((x - 0.2, 7.2, 7.4), (x + 0.2, 8.4, 8.2), steel, skip=())
    for s in (-1, 1):
        m.box((s * 1.2 - 0.4, 6.4, 5.0), (s * 1.2 + 0.4, 8.6, 8.2), steel, skip=())
        m.box((s * 6 - 0.4, 6.8, 5.8), (s * 6 + 0.4, 9.8, 7.4), steel, rot=("z", 22.5 * s, (s * 6, 6.8, 6.6)), skip=())
        for i in range(1, 11):
            x = s * (i * 2.1 + 0.6)
            m.box((x - 0.4, 4.0, 7.4), (x + 0.4, 6.0, 8.2), P(paint(blue), ov_stripe("#f4f0e6", 0.5, 0.4, False)), skip=())
            m.box((x - 0.25, 3.0, 7.55), (x + 0.25, 4.0, 8.05), metal("#e8eaed"), skip=())
            m.box((x - 0.2, 2.4, 7.6), (x + 0.2, 3.0, 8.0), paint("#e8453c"), skip=()) if i % 3 == 0 else None
        hose(m, [(s * 1.4, 8.8, 4.0), (s * 1.4, 9.2, 7.6), (s * 22.6, 9.2, 7.6)], t=0.3)
        m.box((s * 23.4 - 0.5, 4.0, 7.0), (s * 23.4 + 0.5, 8.8, 8.8), paint(YELLOW), skip=())
        m.box((s * 23.4 - 0.4, 8.8, 7.2), (s * 23.4 + 0.4, 10.6, 8.6), light("#ffb347"), skip=())
        wheel(m, s * 7.2, 2.6, 3.0, 2.6, 1.8, "#2a2b2f", "#cccccc", "#8d9096", lug=False)
        wheel(m, s * 9.4, 2.6, 3.0, 2.6, 1.6, "#2a2b2f", "#cccccc", "#8d9096", lug=False)
        m.box((s * 8.2 - 0.5, 2.6, 2.0), (s * 8.2 + 0.5, 6.0, 4.0), steel, skip=())
    hose(m, [(0, 9.0, -3.0), (0, 9.4, 4.4), (-0.0, 9.4, 7.4)], t=0.4)
    hose(m, [(-3.0, 10.0, -1.0), (-3.0, 6.0, -1.0), (-3.0, 6.0, -3.6)], t=0.3)
    return m


def all_attachments():
    return [attach_tiller(), attach_seeder(), attach_harvester(), attach_sprayer()]
