import math
from lib import *
from bld import slab, post, corrug, shingle
from attach2 import hose

STEEL = "#6d7076"
YEL = "#f2b134"


def wingp(color, n=8, tip=None):
    base = paint(color, noise=3)
    ovs = [ov_stripe(tint(color, 0.78), (i + 0.5) / n, 0.35, True) for i in range(n)]
    if tip:
        ovs.append(ov_stripe(tip, 0.04, 2.0, True))
        ovs.append(ov_stripe(tip, 0.96, 2.0, True))
    return P(base, *ovs)


def prop(m, cx, cy, cz, length=17.0, name="propeller", dark="#26282c"):
    m.p(name)
    m.box((cx - 0.5, cy - length / 2, cz - 0.3), (cx + 0.5, cy + length / 2, cz + 0.3), P(metal("#2a2d33"), ov_stripe("#e8b81a", 0.05, 1.0, False), ov_stripe("#e8b81a", 0.95, 1.0, False)), skip=())
    m.box((cx - length / 2, cy - 0.5, cz - 0.7), (cx + length / 2, cy + 0.5, cz - 0.1), P(metal("#2a2d33"), ov_stripe("#e8b81a", 0.04, 1.0, True), ov_stripe("#e8b81a", 0.96, 1.0, True)), skip=())
    cyl_z(m, cx, cy, cz - 0.9, 1.5, 1.8, {"all": metal("#c9962f")})
    m.p("body")


def plane_duster():
    m = Model("plane_duster", 901)
    yel = paint(YEL, noise=4)
    yelf = P(yel, ov_shadow(0.2))
    red = paint("#c4372b", noise=3)
    dark = metal("#26282c")
    steel = metal(STEEL)
    cyl_z(m, 0, 9.4, -14.2, 4.3, 5.0, {"all": P(metal("#d9d9de"), ov_stripe("#2a2d33", 0.5, 0.6, True)), "north": metal("#2a2d33")})
    for s in (-1, 1):
        cyl_z(m, s * 3.4, 10.0, -14.0, 0.9, 3.0, {"all": metal("#7b8188")})
        m.box((s * 4.4 - 0.4, 8.0, -15.5), (s * 4.4 + 0.4, 8.6, -12.5), metal("#9aa0a6"), skip=())
    prop(m, 0, 9.4, -18.2)
    m.box((-3.8, 6.2, -12.0), (3.8, 12.8, -4.0), yelf)
    m.box((-3.4, 12.8, -10.0), (3.4, 14.8, -3.6), P(red, ov_stripe("#f4f0e6", 0.5, 0.6, False)))
    m.box((-1.4, 14.8, -8.0), (1.4, 15.4, -5.6), metal("#2a2d33"), skip=())
    m.box((-3.2, 6.4, -4.0), (3.2, 12.2, 5.0), yelf)
    m.box((-2.6, 6.6, 5.0), (2.6, 11.6, 11.0), yelf)
    m.box((-1.8, 7.2, 11.0), (1.8, 10.8, 16.0), yelf)
    m.box((-1.0, 7.8, 16.0), (1.0, 10.2, 20.0), yelf)
    m.box((-3.2, 5.4, -6.0), (3.2, 6.4, 6.0), dark, skip=())
    m.box((-2.2, 12.2, -3.4), (2.2, 12.8, 3.2), dark, skip=())
    m.box((-2.0, 7.8, -2.4), (2.0, 10.0, 1.4), cloth("#3a2a1c"), skip=())
    m.box((-2.0, 9.8, 0.6), (2.0, 12.4, 1.6), cloth("#3a2a1c"), skip=())
    m.box((-0.9, 11.4, -0.8), (0.9, 13.0, 0.6), paint("#e8b48a"), skip=())
    m.box((-1.0, 12.0, -1.0), (1.0, 12.8, -0.4), paint("#2a2d33"), skip=())
    m.box((-3.0, 12.8, -3.6), (3.0, 15.0, -3.2), glass("#cfe8f5", 100), skip=())
    m.box((-22.0, 5.0, -5.4), (22.0, 6.0, 1.4), wingp(YEL, 10, "#c4372b"), skip=())
    m.box((-22.0, 14.8, -6.4), (22.0, 15.8, 0.8), wingp(YEL, 10, "#c4372b"), skip=())
    m.box((-22.4, 5.0, -5.4), (-22.0, 15.8, 0.8), paint("#c4372b"), skip=()) if False else None
    for s in (-1, 1):
        for x in (8.0, 17.0):
            for z in (-4.6, -0.6):
                m.box((s * x - 0.35, 6.0, z - 0.35), (s * x + 0.35, 14.8, z + 0.35), steel, skip=())
        for z in (-4.0, -0.4):
            m.box((s * 2.6 - 0.35, 12.2, z - 0.35), (s * 2.6 + 0.35, 14.8, z + 0.35), steel, skip=())
        for k in range(2):
            m.box((s * (8.0 + k * 9.0) - 0.15, 6.0, -2.7), (s * (8.0 + k * 9.0) + 0.15, 14.8, -2.5), metal("#aeb4ba"), rot=("z", 22.5 * s * (1 if k == 0 else -1), (s * (8.0 + k * 9.0), 10.4, -2.6)), skip=())
        m.box((s * 7.0 - 7.0 if s > 0 else -14.0, 4.6, -1.6), (s * 7.0 + 7.0 if s > 0 else 0.0, 5.0, -1.0), metal("#2a2d33"), skip=()) if False else None
        for i in range(5):
            x = s * (3.6 + i * 3.0)
            m.box((x - 0.25, 3.6, -2.4), (x + 0.25, 5.0, -1.8), paint("#c4372b"), skip=())
        m.box((s * 2.4 - 0.4, 3.4, -9.0), (s * 2.4 + 0.4, 6.2, -7.8), steel, skip=())
        m.box((s * 3.6 - 0.35, 2.6, -8.0), (s * 5.0 + 0.35, 6.2, -7.4), steel, rot=("z", 22.5 * s, (s * 4.2, 4.4, -7.7)), skip=())
        wheel(m, s * 5.4, 2.8, -7.0, 2.8, 1.8, "#2a2b2f", "#c4372b", "#b8bcc2", lug=False)
    m.box((-4.0, 3.6, -8.0), (4.0, 4.2, -7.4), steel, skip=())
    m.box((-5.0, 3.6, -2.4), (5.0, 4.0, -1.8), steel, skip=()) if False else None
    m.box((-0.5, 10.0, 15.0), (0.5, 17.0, 19.4), P(red, ov_stripe("#f4f0e6", 0.5, 0.8, False)))
    m.box((-7.0, 9.0, 14.6), (7.0, 9.8, 18.8), wingp(YEL, 4, "#c4372b"), skip=())
    m.box((-0.4, 6.6, 18.6), (0.4, 9.0, 19.8), steel, skip=())
    wheel(m, 0, 1.6, 17.6, 1.6, 1.0, "#2a2b2f", "#b8bcc2", "#8d9096", lug=False)
    m.box((-14.0, 3.6, -1.6), (14.0, 4.2, -1.0), metal("#9aa0a6"), skip=())
    return m


def plane_transport():
    m = Model("plane_transport", 902)
    white = paint("#eef0f2", noise=3)
    whitef = P(white, ov_stripe("#2f5fa8", 0.62, 1.6, False), ov_stripe("#d6a238", 0.7, 0.5, False))
    blue = paint("#2f5fa8", noise=3)
    dark = metal("#26282c")
    steel = metal(STEEL)
    cyl_z(m, 0, 10.0, -1.0, 5.4, 30.0, {"all": whitef, "north": white, "south": white})
    for i, (r, z, h) in enumerate(((4.6, -17.0, 3.0), (3.4, -19.6, 2.4), (2.0, -21.6, 2.0))):
        cyl_z(m, 0, 10.0, z, r, h, {"all": white, "north": white})
    m.box((-0.8, 9.0, -22.4), (0.8, 11.0, -21.6), metal("#2a2d33"), skip=())
    cyl_z(m, 0, 10.0, 17.5, 4.2, 6.0, {"all": whitef})
    cyl_z(m, 0, 10.0, 21.5, 2.6, 4.0, {"all": white})
    for s in (-1, 1):
        face = "e" if s > 0 else "w"
        for z in (-11.0, -6.0, -1.0, 4.0, 9.0):
            slab(m, face, z - 1.6, z + 1.6, 10.6, 13.4, 5.5 * s, 0.4, glass("#a8dcf0", 200), skip=())
        slab(m, face, 12.4, 15.6, 8.0, 14.6, 5.5 * s, 0.5, P(paint("#d8dce0"), ov_frame("#2f5fa8", 0.5)), skip=())
    slab(m, "n", -3.4, 3.4, 11.4, 13.6, -15.4, 0.5, glass("#a8dcf0", 200), skip=())
    m.box((-0.7, 14.6, 16.0), (0.7, 25.0, 23.0), P(blue, ov_stripe("#eef0f2", 0.5, 1.0, False)))
    m.box((-9.0, 16.0, 17.4), (9.0, 17.0, 22.6), wingp("#eef0f2", 4, "#2f5fa8"), skip=())
    m.box((-23.0, 14.8, -8.0), (23.0, 16.0, 0.6), wingp("#eef0f2", 12, "#2f5fa8"), skip=())
    for s in (-1, 1):
        m.box((s * 4.0 - 0.5, 14.2, -4.0), (s * 4.0 + 0.5, 15.0, 0.0), steel, skip=())
        m.box((s * 8.0 - 0.4, 6.2, -2.6), (s * 8.0 + 0.4, 14.8, -1.8), steel, rot=("z", 22.5 * s * -1, (s * 8.0, 10.4, -2.2)), skip=())
        cyl_z(m, s * 10.0, 12.4, -8.0, 2.4, 9.0, {"all": whitef, "north": metal("#2a2d33")})
        m.box((s * 10.0 - 1.0, 13.0, -3.8), (s * 10.0 + 1.0, 14.8, -1.0), steel, skip=())
        m.p("propeller_l" if s < 0 else "propeller_r")
        m.box((s * 10.0 - 0.45, 12.4 - 6.0, -12.9), (s * 10.0 + 0.45, 12.4 + 6.0, -12.3), metal("#2a2d33"), skip=())
        m.box((s * 10.0 - 6.0, 12.4 - 0.45, -13.2), (s * 10.0 + 6.0, 12.4 + 0.45, -12.6), metal("#2a2d33"), skip=())
        cyl_z(m, s * 10.0, 12.4, -13.6, 1.2, 1.4, {"all": metal("#c9962f")})
        m.p("body")
        m.box((s * 5.6 - 0.4, 3.0, 0.6), (s * 5.6 + 0.4, 8.2, 3.4), steel, skip=())
        wheel(m, s * 6.4, 3.2, 2.0, 3.2, 1.8, "#2a2b2f", "#2f5fa8", "#b8bcc2", lug=False)
    m.box((-0.5, 3.0, -14.0), (0.5, 6.4, -12.8), steel, skip=())
    wheel(m, 0, 2.2, -13.4, 2.2, 1.4, "#2a2b2f", "#2f5fa8", "#b8bcc2", lug=False)
    m.box((-3.4, 4.2, -9.0), (3.4, 5.4, 12.0), dark, skip=())
    return m


def plane_cargo():
    m = Model("plane_cargo", 903)
    grey = paint("#8b9486", noise=4)
    greyf = P(grey, ov_stripe("#d6a238", 0.55, 0.5, False), ov_dots("#6f7868", 6, 1))
    dark = metal("#26282c")
    steel = metal(STEEL)
    m.box((-6.8, 5.6, -16.0), (6.8, 17.0, 12.0), {"east": P(greyf, ov_text("CARGO", "#f4f0e6", 8)), "west": P(greyf, ov_text("CARGO", "#f4f0e6", 8)), "all": greyf})
    for i, (hw, y0, y1, z0, z1) in enumerate(((6.0, 6.2, 16.2, -19.0, -16.0), (4.6, 7.4, 15.0, -21.0, -19.0), (3.0, 8.6, 13.8, -22.4, -21.0))):
        m.box((-hw, y0, z0), (hw, y1, z1), greyf, skip=())
    slab(m, "n", -4.6, 4.6, 12.0, 15.0, -19.0, 0.5, glass("#a8dcf0", 100), skip=())
    for s in (-1, 1):
        slab(m, "e" if s > 0 else "w", -17.0, -13.0, 11.6, 14.8, 6.8 * s, 0.4, glass("#a8dcf0", 100), skip=())
    m.box((-6.0, 6.2, 12.0), (6.0, 16.2, 15.0), greyf, skip=())
    m.box((-5.4, 8.0, 15.0), (5.4, 16.0, 18.0), greyf, skip=())
    m.box((-4.6, 7.4, 18.0), (4.6, 16.0, 22.0), P(greyf, ov_frame("#d6a238", 0.6)), rot=("x", 0), skip=())
    m.box((-4.8, 4.0, 12.4), (4.8, 8.6, 21.4), P(grey, ov_stripe("#2a2d33", 0.5, 0.6, False)), rot=("x", -22.5, (0, 8.0, 12.4)), skip=())
    m.box((-0.8, 16.0, 17.0), (0.8, 27.0, 23.0), P(grey, ov_stripe("#d6a238", 0.5, 1.0, False)))
    m.box((-10.0, 26.0, 17.4), (10.0, 27.2, 23.0), wingp("#8b9486", 4, "#d6a238"), skip=())
    m.box((-23.0, 18.0, -10.0), (23.0, 19.4, 0.4), wingp("#8b9486", 12, "#d6a238"), skip=())
    for s in (-1, 1):
        m.box((s * 4.4 - 0.6, 16.8, -6.0), (s * 4.4 + 0.6, 18.2, -2.0), steel, skip=())
        m.box((s * 12.0 - 0.5, 8.0, -4.4), (s * 12.0 + 0.5, 18.0, -3.4), steel, rot=("z", 22.5 * s * -1, (s * 12.0, 13.0, -3.9)), skip=())
        for k, xo in enumerate((9.0, 17.0)):
            cyl_z(m, s * xo, 15.6, -11.0, 2.3, 9.0, {"all": greyf, "north": metal("#2a2d33")})
            m.box((s * xo - 1.0, 16.4, -6.6), (s * xo + 1.0, 18.2, -2.6), steel, skip=())
            nm = f"propeller_{'l' if s < 0 else 'r'}{k + 1}"
            m.p(nm)
            m.box((s * xo - 0.45, 15.6 - 5.5, -15.6), (s * xo + 0.45, 15.6 + 5.5, -15.0), metal("#2a2d33"), skip=())
            m.box((s * xo - 5.5, 15.6 - 0.45, -15.9), (s * xo + 5.5, 15.6 + 0.45, -15.3), metal("#2a2d33"), skip=())
            cyl_z(m, s * xo, 15.6, -16.2, 1.1, 1.4, {"all": metal("#c9962f")})
            m.p("body")
        m.box((s * 8.6 - 1.4, 4.0, -4.0), (s * 8.6 + 1.4, 10.4, 8.0), greyf)
        for z in (-0.4, 5.2):
            wheel(m, s * 8.6, 3.2, z, 3.2, 2.0, "#2a2b2f", "#d6a238", "#b8bcc2", lug=False)
    m.box((-0.5, 3.0, -15.0), (0.5, 6.4, -13.8), steel, skip=())
    wheel(m, 0, 2.4, -14.4, 2.4, 1.6, "#2a2b2f", "#d6a238", "#b8bcc2", lug=False)
    return m


def hangar():
    m = Model("hangar", 910)
    metal_roof = corrug("#9aa4a8")
    wall = corrug("#b9c1c6")
    dark = paint("#1b1d20", noise=3)
    conc = paint("#8c8f94", noise=5)
    m.box((-20.6, 0, -20.0), (20.6, 1.0, 20.0), conc)
    r = 19.0
    cy = 8.0
    segs = ((0, 0.0), (22.5, 1), (45.0, 1), (67.5, 1), (22.5, -1), (45.0, -1), (67.5, -1))
    for phi, s in segs:
        a = math.radians(phi)
        cx = s * r * math.sin(a)
        yy = cy + r * math.cos(a)
        ang = 22.5 * round(phi / 22.5) * s
        if phi == 0:
            m.box((-4.0, yy - 0.6, -20.4), (4.0, yy + 0.6, 20.4), metal_roof, skip=())
        else:
            m.box((cx - 4.4, yy - 0.6, -20.4), (cx + 4.4, yy + 0.6, 20.4), metal_roof, rot=("z", ang, (cx, yy, 0)), skip=())
    for s in (-1, 1):
        m.box((s * 19.8 - 0.6, 1.0, -20.0), (s * 19.8 + 0.6, 9.0, 20.0), wall, skip=())
        for z in range(-18, 19, 6):
            m.box((s * 20.2 - 0.4, 1.0, z - 0.4), (s * 20.2 + 0.4, 11.0, z + 0.4), metal("#6d7076"), skip=())
        for z in (-12, 0, 12):
            slab(m, "e" if s > 0 else "w", z - 2.5, z + 2.5, 5.0, 8.0, 20.4 * s, 0.4, glass("#a8dcf0", 200), skip=())
    for side in (-1, 1):
        zc = side * 19.4
        y = 1.0
        while y < 26.9:
            hw = math.sqrt(max(0.0, r * r - (y + 0.5 - cy) ** 2)) if y > cy else 19.8
            hw = min(19.8, hw) - 0.9
            if hw > 0.4:
                if side < 0 and y < 17.0:
                    for sx in (-1, 1):
                        x0 = 12.0
                        if hw > x0:
                            m.box((min(sx * x0, sx * hw), y, zc - 0.5), (max(sx * x0, sx * hw), y + 1.0, zc + 0.5), wall, skip=())
                else:
                    m.box((-hw, y, zc - 0.5), (hw, y + 1.0, zc + 0.5), wall, skip=())
            y += 1.0
    slab(m, "n", -12.0, 12.0, 1.0, 17.0, -19.9, 0.4, dark, skip=())
    m.box((-12.6, 1.0, -20.8), (-11.8, 17.4, -19.2), metal("#40454d"), skip=())
    m.box((11.8, 1.0, -20.8), (12.6, 17.4, -19.2), metal("#40454d"), skip=())
    m.box((-12.6, 17.0, -20.8), (12.6, 18.2, -19.2), metal("#40454d"), skip=())
    sign = P(paint("#2a2d33"), ov_text("HANGAR", "#f2b134", 9), ov_frame("#f2b134", 0.5))
    m.box((-7.0, 19.0, -20.6), (7.0, 22.6, -20.0), sign, skip=())
    for s in (-1, 1):
        m.box((s * 14.5 - 0.7, 12.0, -21.4), (s * 14.5 + 0.7, 13.6, -20.0), light("#fff0b0"), skip=())
    m.box((-8.0, 1.0, -26.0), (8.0, 1.2, -20.0), conc, skip=()) if False else None
    cyl_y(m, -18.0, 1.0, -17.0, 1.8, 4.0, {"all": paint("#2f5fa8", noise=4)})
    m.box((14.0, 1.0, -18.0), (19.0, 6.0, -15.0), P(planks("#6b4a2a", 1.4), ov_stripe("#3a2a1c", 0.5, 0.5, False)), skip=())
    m.box((-10.0, 1.0, 14.0), (10.0, 1.4, 19.4), P(paint("#4a4d52", noise=4), ov_stripe("#e8b81a", 0.5, 0.4, True)), skip=())
    return m


def part_hangar_door():
    m = Model("part_door_hangar", 911)
    m.box((-6.0, 0, -0.6), (6.0, 16, 0.6), {"north": P(corrug("#c9ccd1"), ov_frame("#40454d", 0.8), ov_stripe("#e8b81a", 0.9, 0.8, False)), "south": corrug("#c9ccd1"), "all": corrug("#c9ccd1")}, skip=())
    m.box((-6.0, 15.2, -0.9), (6.0, 16.0, -0.4), hazard("#e8b81a", "#1e1e1e", 2), skip=())
    return m


def runway():
    m = Model("runway_strip", 912)
    asp = paint("#3a3d42", noise=7)
    m.box((-16.0, 0, -24.0), (16.0, 1.0, 24.0), {"up": P(asp, ov_stripe("#f4f0e6", 0.5, 0.9, True), ov_stripe("#f4f0e6", 0.03, 1.0, True), ov_stripe("#f4f0e6", 0.97, 1.0, True)), "all": asp}, skip=("down",))
    for z in range(-22, 23, 8):
        m.box((-0.45, 1.0, z - 1.6), (0.45, 1.1, z + 1.6), paint("#f4f0e6"), skip=())
    for s in (-1, 1):
        for z in range(-22, 23, 12):
            m.box((s * 14.8 - 0.5, 1.0, z - 0.5), (s * 14.8 + 0.5, 1.8, z + 0.5), light("#ffe28a"), skip=())
    return m


def deco_windsock():
    m = Model("deco_windsock", 913)
    m.box((-2.0, 0, -2.0), (2.0, 1.4, 2.0), paint("#8c8f94", noise=4))
    m.box((-0.5, 1.4, -0.5), (0.5, 20.0, 0.5), metal("#c9ccd1"), skip=())
    cyl_y(m, 0, 19.6, 0, 1.0, 1.2, {"all": metal("#2a2d33")})
    return m


def part_windsock():
    m = Model("part_windsock", 914)
    rings = ((3.6, 0.0), (3.2, 2.6), (2.8, 5.2), (2.4, 7.8), (2.0, 10.4), (1.6, 13.0))
    for i, (r, z) in enumerate(rings):
        col = "#e8453c" if i % 2 == 0 else "#f4f0e6"
        cyl_z(m, 0, 8.0, -z - 1.3, r, 2.6, {"all": paint(col, noise=3)})
    m.box((-0.4, 4.0, 0.2), (0.4, 12.0, 1.0), metal("#c9ccd1"), skip=())
    return m


def all_planes():
    return [plane_duster(), plane_transport(), plane_cargo(), hangar(), part_hangar_door(), runway(), deco_windsock(), part_windsock()]
