import math
import random
from lib import *
from bld import *
from cosmetics import bricks

STONE = bricks("#8c8f94", "#4d4f53", 2.0, 4.0)
WOOD = planks("#7a5230", 1.6)
WOODL = planks("#a9794a", 1.8)
DARKINT = paint("#241a12", noise=3)


def farmhouse(tier, lit):
    name = f"farmhouse_t{tier}" + ("_lit" if lit else "")
    m = Model(name, 500 + tier * 2 + (1 if lit else 0))
    W, D, H = {1: (28, 22, 12), 2: (34, 26, 13), 3: (40, 28, 18)}[tier]
    wall_c = {1: "#f2eee2", 2: "#ecd9b0", 3: "#cfdfe8"}[tier]
    trim_c = {1: "#3f7a4a", 2: "#7a3a2a", 3: "#3a4a5a"}[tier]
    roof_c = {1: "#8a3b2b", 2: "#4b5563", 3: "#2f5a52"}[tier]
    fh = 2.0
    ye = fh + H
    m.box((-W / 2 - 0.6, 0, -D / 2 - 0.6), (W / 2 + 0.6, fh, D / 2 + 0.6), STONE)
    m.box((-W / 2, fh, -D / 2), (W / 2, ye, D / 2), siding(wall_c))
    trim = paint(trim_c, noise=3)
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.box((sx * W / 2 - (0 if sx < 0 else 1.2) + (-0.3 if sx < 0 else 0.0), fh, sz * D / 2 - (0 if sz < 0 else 1.2) + (-0.3 if sz < 0 else 0.0)), (sx * W / 2 + (1.5 if sx < 0 else 0.3), ye, sz * D / 2 + (1.5 if sz < 0 else 0.3)), trim, skip=())
    m.box((-W / 2 - 0.3, ye - 0.8, -D / 2 - 0.3), (W / 2 + 0.3, ye, D / 2 + 0.3), trim, skip=())
    m.box((-W / 2 - 0.3, fh, -D / 2 - 0.3), (W / 2 + 0.3, fh + 0.9, D / 2 + 0.3), trim, skip=())
    zf = -D / 2
    slab(m, "n", -3.5, 3.5, fh, fh + 11, zf, 0.3, DARKINT, skip=())
    slab(m, "n", -4.5, -3.5, fh, fh + 11.8, zf, 0.7, paint(TRIM), skip=())
    slab(m, "n", 3.5, 4.5, fh, fh + 11.8, zf, 0.7, paint(TRIM), skip=())
    slab(m, "n", -4.5, 4.5, fh + 11, fh + 12, zf, 0.7, paint(TRIM), skip=())
    porch_d = 6.0
    m.box((-8, 0, zf - porch_d), (8, fh, zf), planks("#a9794a", 1.6), skip=())
    m.box((-5, 0, zf - porch_d - 2), (5, 1.0, zf - porch_d), STONE, skip=())
    for sx in (-1, 1):
        post(m, sx * 7.2, zf - porch_d + 0.8, fh, fh + 11, 1.2, paint(TRIM))
    m.box((-9, fh + 11, zf - porch_d - 0.5), (9, fh + 12, zf + 0.2), planks("#a9794a", 1.4), rot=("x", 22.5, (0, fh + 11.5, zf - porch_d)), skip=())
    m.box((-8.4, fh + 11.8, zf - porch_d - 0.4), (8.4, fh + 12.4, zf - porch_d + 0.2), shingle(roof_c), skip=())
    wl = [(-W / 2 + 6, "n"), (W / 2 - 6, "n")]
    for (x, f) in wl:
        window(m, "n", x, fh + 7, zf, 4.0, 5.0, lit, TRIM, trim_c, True)
    for z in (-D / 2 + 6, D / 2 - 6):
        window(m, "e", z, fh + 7, W / 2, 4.0, 5.0, lit, TRIM, trim_c)
        window(m, "w", z, fh + 7, -W / 2, 4.0, 5.0, lit, TRIM, trim_c)
    window(m, "s", 0, fh + 7, D / 2, 4.0, 5.0, lit, TRIM, trim_c)
    if tier >= 3:
        for (x, f) in wl:
            window(m, "n", x, fh + 14.5, zf, 4.0, 4.6, lit, TRIM, trim_c)
        window(m, "n", 0, fh + 14.5, zf, 4.0, 4.6, lit, TRIM, trim_c)
        m.box((-6, fh + 11.6, zf - 5.4), (6, fh + 12.2, zf), planks("#a9794a", 1.4), skip=())
        for x in range(-6, 7, 2):
            post(m, x, zf - 5.2, fh + 12.2, fh + 15, 0.5, paint(TRIM))
        m.box((-6.2, fh + 15, zf - 5.6), (6.2, fh + 15.6, zf - 4.8), paint(TRIM), skip=())
    cw = 3.2
    cx = -W / 2 + 6
    cz = D / 4
    rise = (W / 2 + 1.5) * math.tan(math.radians(22.5))
    top = ye + rise + (3.0 if tier < 3 else 1.6)
    m.box((cx - cw / 2, ye - 1.0, cz - cw / 2), (cx + cw / 2, top, cz + cw / 2), bricks("#a8503a", "#5a2a20", 1.6, 3.2), skip=())
    m.box((cx - cw / 2 - 0.4, top, cz - cw / 2 - 0.4), (cx + cw / 2 + 0.4, top + 0.9, cz + cw / 2 + 0.4), STONE, skip=())
    gable(m, W, D, ye, shingle(roof_c), siding(wall_c))
    if tier >= 2:
        dz = -D / 4
        for dx in ((0,) if tier == 2 else (-8, 8)):
            m.box((dx - 3, ye + 1.0, zf + 1.0 + 0.0), (dx + 3, ye + 5.6, zf + 5.0), siding(wall_c), skip=())
            window(m, "n", dx, ye + 3.4, zf + 1.0, 2.6, 2.8, lit, TRIM, None)
            m.box((dx - 3.6, ye + 5.0, zf + 0.6), (dx, ye + 6.2, zf + 5.6), shingle(roof_c), rot=("z", -22.5, (dx - 1.8, ye + 5.6, zf + 3.0)), skip=())
            m.box((dx, ye + 5.0, zf + 0.6), (dx + 3.6, ye + 6.2, zf + 5.6), shingle(roof_c), rot=("z", 22.5, (dx + 1.8, ye + 5.6, zf + 3.0)), skip=())
    m.box((W / 2 - 1, fh, -3), (W / 2 + 4, fh + 9, 3), siding(wall_c)) if tier == 3 else None
    for sx in (-1, 1):
        m.box((sx * 12 - 0.6, 0, zf - porch_d - 3.2), (sx * 12 + 0.6, 4.0, zf - porch_d - 2.0), planks("#6b4a2a", 1.0), skip=())
    m.box((-0.5, fh + 12.6, zf - 0.9), (0.5, fh + 14.0, zf), light("#ffd36a") if lit else paint("#55585e"), skip=())
    m.box((W / 2 - 4.5, 0, zf - 4.4), (W / 2 - 1.5, 4.0, zf - 3.2), paint("#c0392b", noise=3), skip=())
    m.box((W / 2 - 3.2, 0, zf - 3.6), (W / 2 - 2.8, 3.0, zf - 3.2), planks("#6b4a2a", 1.0), skip=())
    return m


def barn():
    m = Model("barn", 520)
    W, D, ye = 40, 34, 16
    red = batten("#a63a2c")
    wh = paint(TRIM, noise=3)
    m.box((-W / 2 - 0.6, 0, -D / 2 - 0.6), (W / 2 + 0.6, 3, D / 2 + 0.6), paint("#8c8f94", noise=4))
    m.box((-W / 2, 3, -D / 2), (W / 2, ye, D / 2), red)
    zf = -D / 2
    slab(m, "n", -7.2, 7.2, 3, 17, zf - 0.0, 0.3, DARKINT, skip=())
    m.box((-7.6, 3, zf - 0.6), (-7.0, 17.2, zf + 0.1), wh, skip=())
    m.box((7.0, 3, zf - 0.6), (7.6, 17.2, zf + 0.1), wh, skip=())
    m.box((-7.6, 16.6, zf - 0.6), (7.6, 17.4, zf + 0.1), wh, skip=())
    m.box((-5, 3, zf + 0.3), (5, 3.8, zf + 9), planks("#6b4a2a", 1.6), skip=())
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.box((sx * W / 2 - (0.8 if sx > 0 else 0) - (0 if sx > 0 else -0.0), 3, sz * D / 2 - (0.8 if sz > 0 else 0)), (sx * W / 2 + (0 if sx > 0 else 0.8), ye + 0.4, sz * D / 2 + (0 if sz > 0 else 0.8)), wh, skip=())
    m.box((-W / 2 - 0.3, 3, -D / 2 - 0.3), (W / 2 + 0.3, 4.0, D / 2 + 0.3), wh, skip=())
    m.box((-W / 2 - 0.3, ye - 0.6, -D / 2 - 0.3), (W / 2 + 0.3, ye + 0.4, D / 2 + 0.3), wh, skip=())
    for x in (-14, 14):
        slab(m, "n", x - 2.5, x + 2.5, 8, 14, zf, 0.4, glass("#9fc4de", 215), skip=())
        slab(m, "n", x - 3.1, x + 3.1, 14, 14.8, zf, 0.7, wh, skip=())
        slab(m, "n", x - 3.1, x + 3.1, 7.2, 8, zf, 0.7, wh, skip=())
        slab(m, "n", x - 3.1, x - 2.5, 8, 14, zf, 0.7, wh, skip=())
        slab(m, "n", x + 2.5, x + 3.1, 8, 14, zf, 0.7, wh, skip=())
    for z in (-8, 8):
        for side, xo in (("e", W / 2), ("w", -W / 2)):
            slab(m, side, z - 2.5, z + 2.5, 8, 13, xo, 0.4, glass("#9fc4de", 215), skip=())
            slab(m, side, z - 3.1, z + 3.1, 13, 13.8, xo, 0.7, wh, skip=())
            slab(m, side, z - 3.1, z + 3.1, 7.2, 8, xo, 0.7, wh, skip=())
    prof = lambda y: (W / 2 - (y - ye)) if y < ye + 6 else (W / 2 - 6 - (y - ye - 6) / math.tan(math.radians(22.5)))
    roof = corrug("#5a606a")
    for s in (-1, 1):
        m.box((s * 17 - 4.4, ye + 3.0 - 0.5, -D / 2 - 1.5), (s * 17 + 4.4, ye + 3.0 + 0.5, D / 2 + 1.5), roof, rot=("z", 45 * s, (s * 17, ye + 3.0, 0)), skip=())
        m.box((s * 7 - 7.6, ye + 6 + 2.9 - 0.5, -D / 2 - 1.5), (s * 7 + 7.6, ye + 6 + 2.9 + 0.5, D / 2 + 1.5), roof, rot=("z", 22.5 * s, (s * 7, ye + 6 + 2.9, 0)), skip=())
    top = ye + 6 + 14 * math.tan(math.radians(22.5))
    m.box((-1.4, top - 0.2, -D / 2 - 1.5), (1.4, top + 0.8, D / 2 + 1.5), paint("#40454d"), skip=())
    for side in (-1, 1):
        pz = side * (D / 2 - 0.5)
        y = ye
        while y < top - 0.4:
            hw = prof(y + 1.0) - 1.0
            if hw > 0.3:
                m.box((-hw, y, pz - 0.5), (hw, y + 1.0, pz + 0.5), red, skip=())
            y += 1.0
    slab(m, "n", -3.2, 3.2, 18.6, 25.0, zf, 0.4, DARKINT, skip=())
    slab(m, "n", -3.8, 3.8, 24.6, 25.6, zf, 0.8, wh, skip=())
    slab(m, "n", -3.8, -3.2, 18.6, 24.6, zf, 0.8, wh, skip=())
    slab(m, "n", 3.2, 3.8, 18.6, 24.6, zf, 0.8, wh, skip=())
    m.box((-2.6, 18.6, zf + 0.5), (2.6, 21.8, zf + 4.5), straw("#dcc05a"), skip=())
    m.box((-0.5, 25.6, zf - 4.0), (0.5, 26.6, zf + 0.8), WOOD, skip=())
    m.box((-0.3, 20.0, zf - 3.2), (0.3, 25.6, zf - 2.6), paint("#3a3a3e"), skip=())
    m.box((-1.0, 19.4, zf - 3.6), (1.0, 20.2, zf - 2.2), metal("#55585e"), skip=())
    m.box((-3, top + 0.7, -3), (3, top + 2.7, 3), planks("#f2eee2", 1.0, True), skip=())
    for sx in (-1, 1):
        slab(m, "n", sx * 1.5 - 0.7, sx * 1.5 + 0.7, top + 1.0, top + 2.4, -3, 0.3, DARKINT, skip=())
    m.box((-3.8, top + 2.7, -3.8), (3.8, top + 3.4, 3.8), roof, skip=())
    m.box((-2.4, top + 3.4, -2.4), (2.4, top + 4.0, 2.4), roof, skip=())
    return m


def silo():
    m = Model("silo", 530)
    metalc = corrug("#aeb4ba")
    band = metal("#55585e")
    cyl_y(m, 0, 0, 0, 10.5, 2.0, {"all": paint("#8c8f94", noise=4)})
    cyl_y(m, 0, 2.0, 0, 9.0, 8.0, {"all": metalc})
    cyl_y(m, 0, 10.0, 0, 9.0, 8.0, {"all": corrug("#b8bec4")})
    cyl_y(m, 0, 18.0, 0, 9.0, 6.0, {"all": metalc})
    for y in (2.0, 6.0, 10.0, 14.0, 18.0, 23.0):
        cyl_y(m, 0, y, 0, 9.25, 0.6, {"all": band})
    for i, (y, r, h) in enumerate(((24.0, 9.0, 1.6), (25.6, 7.4, 1.6), (27.2, 5.2, 1.4), (28.6, 2.8, 1.2))):
        cyl_y(m, 0, y, 0, r, h, {"all": corrug("#8d949b")})
    cyl_y(m, 0, 29.8, 0, 1.4, 1.0, {"all": metal("#40454d")})
    m.box((-0.3, 30.8, -0.3), (0.3, 32.0, 0.3), metal("#40454d"), skip=())
    slab(m, "n", -2.0, 2.0, 4.0, 21.0, -9.0, 0.5, paint("#1d1f23", noise=3), skip=())
    slab(m, "n", -1.4, 1.4, 4.5, 20.5, -9.0, 0.7, glass("#9fc4de", 150), skip=())
    for yy in range(5, 21, 3):
        slab(m, "n", 1.0, 2.0, yy, yy + 0.4, -9.0, 1.0, paint("#f2eee2"), skip=())
    slab(m, "n", -2.4, -2.0, 4.0, 21.0, -9.0, 0.9, paint("#40454d"), skip=())
    slab(m, "n", 2.0, 2.4, 4.0, 21.0, -9.0, 0.9, paint("#40454d"), skip=())
    for z in (-1, 1):
        pass
    for x in (-3.0, 3.0):
        m.box((x - 0.4, 2.0, -11.0), (x + 0.4, 24.0, -10.3), band, skip=())
    for y in range(3, 24, 2):
        m.box((-3.0, y, -11.0), (3.0, y + 0.4, -10.3), band, skip=())
    m.box((11.0, 0, -1.4), (13.4, 20.0, 1.4), metal("#7b8188"), skip=())
    m.box((5.0, 18.0, -1.4), (13.4, 20.6, 1.4), metal("#7b8188"), rot=("z", -22.5, (11.0, 19.0, 0)), skip=())
    m.box((9.0, 21.0, -1.2), (11.0, 25.0, 1.2), metal("#7b8188"), skip=())
    slab(m, "e", -1.6, 1.6, 2.0, 7.0, 9.0, 0.8, {"all": planks("#6b4a2a", 1.0, True)}, skip=())
    m.box((9.6, 0, -2.2), (14.0, 2.0, 2.2), paint("#8c8f94", noise=4), skip=())
    m.box((9.8, 2.0, -1.0), (12.4, 3.6, 1.0), metal("#40454d"), skip=())
    m.box((-6.0, 0, 11.0), (6.0, 1.0, 14.0), paint("#8c8f94", noise=4), skip=())
    for i in range(3):
        m.box((-5 + i * 3.6, 1.0, 11.4), (-2.6 + i * 3.6, 4.2, 13.6), P(burlap(), ov_stripe("#7a6238", 0.5, 0.8, True)), skip=())
    return m


def coop():
    m = Model("coop", 540)
    red = planks("#b0463a", 1.6, True, 0.72, 0.05)
    wh = paint(TRIM, noise=3)
    wood = planks("#8a6038", 1.6)
    for sx in (-1, 1):
        for sz in (0, 1):
            post(m, sx * 8, 0.0 + sz * 9.0, 0, 5, 1.2, wood)
    m.box((-9.5, 4.2, -2.4), (9.5, 5.2, 10.4), planks("#a9794a", 1.4), skip=())
    m.box((-9, 5.2, -2), (9, 13, 10), red)
    for sx in (-1, 1):
        for sz in (-1, 1):
            m.box((sx * 9 - 0.6, 5.2, (-2 if sz < 0 else 9.2) - 0.0), (sx * 9 + 0.6, 13, (-1.2 if sz < 0 else 10) - 0.0), wh, skip=())
    slab(m, "n", -3, 3, 5.2, 10.5, -2, 0.3, DARKINT, skip=())
    slab(m, "n", -3.6, -3, 5.2, 10.8, -2, 0.7, wh, skip=())
    slab(m, "n", 3, 3.6, 5.2, 10.8, -2, 0.7, wh, skip=())
    slab(m, "n", -3.6, 3.6, 10.5, 11.1, -2, 0.7, wh, skip=())
    window(m, "n", -6.4, 9.4, -2, 2.0, 2.4, False, TRIM, None)
    window(m, "w", 4, 9.4, -9, 2.4, 2.4, False, TRIM, None)
    for sx, face in ((1, "e"), (-1, "w")):
        pass
    gable(m, 18, 12, 13, shingle("#40454d"), planks("#b0463a", 1.6, True), ov=1.4, fov=1.4)
    for i in range(3):
        x0 = 9.5
        m.box((x0, 5.4, 0.4 + i * 3.2), (x0 + 3.2, 8.6, 3.2 + i * 3.2), planks("#8a6038", 1.4), skip=())
        m.box((x0 - 0.2, 8.4, 0.2 + i * 3.2), (x0 + 3.4, 9.0, 3.4 + i * 3.2), planks("#6b4a2a", 1.2), rot=("z", -22.5, (x0 - 0.2, 8.6, 0)), skip=())
        m.box((x0 + 0.4, 6.0, 0.8 + i * 3.2 + 0.4), (x0 + 3.0, 6.8, 2.8 + i * 3.2), straw(), skip=())
        m.box((x0 + 1.0, 6.8, 1.2 + i * 3.2), (x0 + 2.2, 7.8, 2.4 + i * 3.2), paint("#f4f0e6", noise=3), skip=())
    m.box((-2.5, 4.2, -14), (2.5, 5.0, -2), planks("#a9794a", 1.4), rot=("x", -22.5, (0, 5.0, -2)), skip=())
    for i in range(5):
        m.box((-2.5, 4.4 - i * 0.8, -3.0 - i * 2.2), (2.5, 4.9 - i * 0.8, -2.6 - i * 2.2), planks("#6b4a2a", 1.0), skip=())
    wire = mesh("#a5abb2", 2.0)
    x0, x1, z0, z1 = -14, 14, -22, -3
    for x in (x0, x1):
        for z in (z0, (z0 + z1) / 2, z1):
            post(m, x, z, 0, 8, 0.9, wood)
    for z in (z0, z1):
        for x in (-7, 0, 7):
            post(m, x, z, 0, 8, 0.9, wood)
    m.box((x0, 0.5, z0 - 0.1), (x1, 7.5, z0 + 0.1), wire, skip=())
    m.box((x0 - 0.1, 0.5, z0), (x0 + 0.1, 7.5, z1), wire, skip=())
    m.box((x1 - 0.1, 0.5, z0), (x1 + 0.1, 7.5, z1), wire, skip=())
    m.box((x0, 0.5, z1 - 0.1), (-4, 7.5, z1 + 0.1), wire, skip=())
    m.box((4, 0.5, z1 - 0.1), (x1, 7.5, z1 + 0.1), wire, skip=())
    m.box((x0, 7.5, z0 - 0.3), (x1, 8.2, z0 + 0.3), wood, skip=())
    m.box((x0 - 0.3, 7.5, z0), (x0 + 0.3, 8.2, z1), wood, skip=())
    m.box((x1 - 0.3, 7.5, z0), (x1 + 0.3, 8.2, z1), wood, skip=())
    m.box((x0, 0.0, z0), (x1, 0.3, z1), paint("#9a7a4a", noise=8), skip=())
    m.box((7, 0.3, -17), (13, 2.8, -14), planks("#8a6038", 1.2), skip=())
    m.box((7.4, 2.8, -16.6), (12.6, 3.0, -14.4), paint("#3a7bb5", noise=4), skip=())
    cyl_y(m, -9, 0.3, -12, 2.0, 2.2, {"all": metal("#9aa0a6")})
    m.box((-9.2, 2.5, -12.2), (-8.8, 4.6, -11.8), metal("#9aa0a6"), skip=())
    for i in range(6):
        m.box((-12 + (i % 3) * 3.2, 0.3, -9 - (i // 3) * 3.0), (-10.5 + (i % 3) * 3.2, 0.8, -7.8 - (i // 3) * 3.0), straw("#dcc05a"), skip=())
    m.box((-1, 4.4, 10.6), (1, 12, 11.2), planks("#f2eee2", 1.0, True), skip=())
    return m


def mill():
    m = Model("mill", 550)
    plaster = paint("#efe8d8", noise=4)
    wood = planks("#7a5230", 1.6)
    roof = shingle("#4a3a30")
    cyl_y(m, 0, 0, 0, 11.6, 6.0, {"all": STONE})
    cyl_y(m, 0, 6.0, 0, 10.2, 6.0, {"all": plaster})
    cyl_y(m, 0, 12.0, 0, 8.8, 5.0, {"all": plaster})
    cyl_y(m, 0, 17.0, 0, 7.6, 3.0, {"all": wood})
    for y, r in ((5.6, 10.6), (11.6, 9.2), (16.6, 8.0)):
        cyl_y(m, 0, y, 0, r, 0.9, {"all": wood})
    for y, r, h in ((20.0, 8.6, 1.4), (21.4, 7.2, 1.8), (23.2, 5.6, 1.8), (25.0, 4.0, 1.8), (26.8, 2.6, 1.8), (28.6, 1.4, 1.6)):
        cyl_y(m, 0, y, 0, r, h, {"all": roof})
    m.box((-0.5, 30.2, -0.5), (0.5, 32.0, 0.5), metal("#c9962f"), skip=())
    zf = -11.6
    slab(m, "n", -3.0, 3.0, 0, 9.0, zf, 0.5, DARKINT, skip=())
    slab(m, "n", -3.8, -3.0, 0, 9.8, zf, 1.0, STONE, skip=())
    slab(m, "n", 3.0, 3.8, 0, 9.8, zf, 1.0, STONE, skip=())
    slab(m, "n", -3.8, 3.8, 9.0, 10.0, zf, 1.0, STONE, skip=())
    m.box((-6, 0, zf - 4), (6, 1.0, zf), paint("#8c8f94", noise=4), skip=())
    m.box((-2.4, 1.0, zf - 2), (2.4, 2.0, zf), paint("#8c8f94", noise=4), skip=())
    slab(m, "n", -2.2, 2.2, 6.2, 6.8, zf - 0.2, 0.2, paint("#f2eee2"), skip=())
    m.box((-1.4, 16.2, -11.2), (1.4, 21.6, -6.4), wood, skip=())
    m.box((-1.0, 18.4, -12.6), (1.0, 20.6, -10.8), metal("#55585e"), skip=())
    for a in (-1, 1):
        window(m, "n", a * 4.4, 14.5, -8.2, 1.8, 2.8, False, TRIM, None)
    window(m, "e", 0, 9.0, 10.2, 2.0, 3.0, False, TRIM, "#7a5230")
    window(m, "w", 0, 9.0, -10.2, 2.0, 3.0, False, TRIM, "#7a5230")
    for i in range(3):
        m.box((8 + i * 0.0, i * 3.2, 7 - i * 0.0), (11, 3.2 + i * 3.2, 11), wood, skip=()) if False else None
    for i in range(3):
        m.box((-14.0 + i * 3.6, 0, 4.0), (-11.2 + i * 3.6, 4.0, 7.2), P(burlap(), ov_stripe("#7a6238", 0.5, 0.8, True)), skip=())
    cyl_y(m, 14, 0.2, -2, 3.6, 1.2, {"all": paint("#9a9ea4", noise=6)})
    cyl_y(m, 14, 1.4, -2, 1.4, 0.5, {"all": metal("#55585e")})
    cyl_y(m, 0, 11.2, 0, 11.0, 0.5, {"all": wood}) if False else None
    for ang in range(8):
        a = math.radians(ang * 45 + 22.5)
        x = math.cos(a) * 8.3
        z = math.sin(a) * 8.3
        post(m, x, z, 20.0, 22.0, 0.5, wood) if False else None
    return m


def bakery(lit):
    name = "bakery" + ("_on" if lit else "")
    m = Model(name, 560 + (1 if lit else 0))
    W, D, ye = 32, 24, 14
    brick = bricks("#a8503a", "#5a2a20", 1.6, 3.2)
    m.box((-W / 2 - 0.5, 0, -D / 2 - 0.5), (W / 2 + 0.5, 2, D / 2 + 0.5), STONE)
    m.box((-W / 2, 2, -D / 2), (W / 2, ye, D / 2), brick)
    wh = paint(TRIM, noise=3)
    for sx in (-1, 1):
        for sz in (-1, 1):
            post(m, sx * (W / 2 - 0.3), sz * (D / 2 - 0.3), 2, ye, 1.4, paint("#c9b99a", noise=4))
    m.box((-W / 2 - 0.3, ye - 0.9, -D / 2 - 0.3), (W / 2 + 0.3, ye, D / 2 + 0.3), paint("#c9b99a", noise=4), skip=())
    zf = -D / 2
    slab(m, "n", -12, -2, 5.0, 11.5, zf, 0.3, P(paint("#ffcf6a" if lit else "#3b5a78", noise=5), ov_stripe(TRIM, 0.5, 0.4, True), ov_stripe(TRIM, 0.33, 0.4, False)), skip=())
    slab(m, "n", -12.8, -2, 11.5, 12.3, zf, 0.6, wh, skip=())
    slab(m, "n", -12.8, -2, 4.2, 5.0, zf, 0.6, wh, skip=())
    slab(m, "n", -12.8, -12, 4.2, 12.3, zf, 0.6, wh, skip=())
    slab(m, "n", -2.8, -2, 4.2, 12.3, zf, 0.6, wh, skip=())
    m.box((-13, 2, zf - 2.2), (-1.5, 5, zf), planks("#8a6038", 1.4), skip=())
    for i in range(3):
        m.box((-11.4 + i * 3.4, 5.0, zf - 1.6), (-9.2 + i * 3.4, 6.2, zf - 0.4), paint("#c98a3a", noise=7), skip=())
    slab(m, "n", 3, 9, 2, 11, zf, 0.4, planks("#6b4a2a", 1.4, True), skip=())
    slab(m, "n", 2.4, 3, 2, 11.6, zf, 0.8, wh, skip=())
    slab(m, "n", 9, 9.6, 2, 11.6, zf, 0.8, wh, skip=())
    slab(m, "n", 2.4, 9.6, 11, 11.6, zf, 0.8, wh, skip=())
    slab(m, "n", 4.4, 7.6, 6.5, 9.6, zf - 0.3, 0.3, glass("#9fc4de", 200), skip=())
    stripes = P(paint("#c0392b", noise=3), ov_stripe("#f4f0e6", 0.17, 1.2, True), ov_stripe("#f4f0e6", 0.5, 1.2, True), ov_stripe("#f4f0e6", 0.83, 1.2, True))
    m.box((-14.5, 11.8, zf - 6), (-0.5, 12.6, zf + 0.4), stripes, rot=("x", 22.5, (-7.5, 12.6, zf + 0.4)), skip=())
    for i in range(8):
        m.box((-14.2 + i * 1.95, 9.2, zf - 5.6), (-12.7 + i * 1.95, 10.4, zf - 5.0), paint("#c0392b" if i % 2 == 0 else "#f4f0e6", noise=3), skip=()) if False else None
    for sx in (-14, -1):
        post(m, sx, zf - 5.4, 2, 10.2, 0.6, wood_post())
    m.box((15.0, 9.0, zf - 0.5), (15.0 + 0.6, 12.0, zf + 5.0), wood_post(), skip=()) if False else None
    m.box((W / 2 + 0.2, 13.0, zf + 3), (W / 2 + 4.6, 14.0, zf + 4), metal("#3a3a3e"), skip=())
    sign = P(planks("#8a6038", 1.4), ov_draw(lambda d, c, i: (d.ellipse([c.X(1.6), c.X(1.2), c.pw - c.X(1.6) - 1, c.ph - c.X(1.2) - 1], fill=(222, 164, 80, 255)), d.line([c.X(3.0), c.X(2.4), c.pw - c.X(3.0), c.ph - c.X(2.4)], fill=(160, 100, 40, 255)), d.line([c.X(4.2), c.X(1.8), c.pw - c.X(2.0), c.ph - c.X(3.4)], fill=(160, 100, 40, 255)))))
    m.box((W / 2 + 0.2, 8.0, zf + 2.2), (W / 2 + 0.8, 13.0, zf + 5.6), {"east": sign, "west": sign, "all": planks("#8a6038", 1.4)}, skip=())
    gable(m, D, W, ye, shingle("#b8613a"), brick, ov=1.6, fov=1.6, ridge="x")
    cx, cz = 8, 6
    top = ye + 12 + 4
    m.box((cx - 2, ye - 1, cz - 2), (cx + 2, top, cz + 2), bricks("#8a4430", "#4a2218", 1.6, 3.2), skip=())
    m.box((cx - 2.6, top, cz - 2.6), (cx + 2.6, top + 1.0, cz + 2.6), STONE, skip=())
    if lit:
        m.box((cx - 1.2, top + 1.0, cz - 1.2), (cx + 1.2, top + 1.4, cz + 1.2), light("#ff8a2a"), skip=())
    ox, oz = W / 2 - 0.8, 4.0
    cyl_y(m, ox + 4, 0, oz, 4.4, 3.0, {"all": paint("#b89a6a", noise=6)})
    cyl_y(m, ox + 4, 3.0, oz, 3.4, 1.6, {"all": paint("#b89a6a", noise=6)})
    cyl_y(m, ox + 4, 4.6, oz, 2.0, 1.2, {"all": paint("#b89a6a", noise=6)})
    m.box((ox + 4 - 1.6, 0.8, oz - 5.0), (ox + 4 + 1.6, 3.2, oz - 3.6), light("#ff7a1c") if lit else paint("#1b1511"), skip=())
    for i in range(4):
        m.box((W / 2 + 0.6 + i * 0.1, 0, -6 + i * 1.6), (W / 2 + 2.6, 1.3, -5.0 + i * 1.6), planks("#8a6038", 1.0, True), skip=()) if False else None
    for i in range(3):
        m.box((-W / 2 - 4.0, 0, 3.0 + i * 3.2), (-W / 2 - 0.4, 4.0, 5.8 + i * 3.2), P(burlap("#e8e0cc"), ov_stripe("#c9b99a", 0.5, 0.8, True)), skip=())
    return m


def wood_post():
    return planks("#6b4a2a", 1.0, True)


def greenhouse():
    m = Model("greenhouse", 570)
    W, D = 40, 28
    wh = paint(TRIM, noise=3)
    gl = glass("#b6dcf0", 95)
    m.box((-W / 2 - 0.6, 0, -D / 2 - 0.6), (W / 2 + 0.6, 3, D / 2 + 0.6), STONE)
    ye = 13.0
    for z in (-D / 2, D / 2 - 0.4):
        m.box((-W / 2, 3, z), (W / 2, ye, z + 0.4), gl, skip=())
    for x in (-W / 2, W / 2 - 0.4):
        m.box((x, 3, -D / 2), (x + 0.4, ye, D / 2), gl, skip=())
    for x in range(-20, 21, 4):
        post(m, x, -D / 2 + 0.2, 3, ye, 0.9, wh)
        post(m, x, D / 2 - 0.2, 3, ye, 0.9, wh)
    for z in range(-14, 15, 4):
        post(m, -W / 2 + 0.2, z, 3, ye, 0.9, wh)
        post(m, W / 2 - 0.2, z, 3, ye, 0.9, wh)
    for y in (3, 8, ye - 0.8):
        m.box((-W / 2 - 0.2, y, -D / 2 - 0.2), (W / 2 + 0.2, y + 0.8, -D / 2 + 0.6), wh, skip=())
        m.box((-W / 2 - 0.2, y, D / 2 - 0.6), (W / 2 + 0.2, y + 0.8, D / 2 + 0.2), wh, skip=())
        m.box((-W / 2 - 0.2, y, -D / 2), (-W / 2 + 0.6, y + 0.8, D / 2), wh, skip=())
        m.box((W / 2 - 0.6, y, -D / 2), (W / 2 + 0.2, y + 0.8, D / 2), wh, skip=())
    deg = 22.5
    half = D / 2 + 0.8
    rise = half * math.tan(math.radians(deg))
    L = half / math.cos(math.radians(deg))
    for s in (-1, 1):
        cs_ = s * half / 2
        cy = ye + rise / 2
        m.box((-W / 2 - 0.6, cy - 0.3, cs_ - L / 2), (W / 2 + 0.6, cy + 0.3, cs_ + L / 2), gl, rot=("x", -22.5 * s, (0, cy, cs_)), skip=())
    for x in range(-20, 21, 4):
        for s in (-1, 1):
            cs_ = s * half / 2
            cy = ye + rise / 2
            m.box((x - 0.35, cy - 0.6, cs_ - L / 2), (x + 0.35, cy + 0.6, cs_ + L / 2), wh, rot=("x", -22.5 * s, (x, cy, cs_)), skip=())
    m.box((-W / 2 - 0.6, ye + rise - 0.2, -1.0), (W / 2 + 0.6, ye + rise + 0.8, 1.0), wh, skip=())
    n = int((ye + rise - ye) / 1.4)
    for side in (-1, 1):
        x = side * (W / 2 - 0.2)
        for k in range(n):
            w = (D / 2) * (1 - (k + 0.5) / n) * 2 - 0.4
            y0 = ye + k * rise / n
            m.box((x - 0.2, y0, -w / 2), (x + 0.2, y0 + rise / n + 0.05, w / 2), gl, skip=())
    zf = -D / 2
    slab(m, "n", 14.2, 19.2, 3, 11.6, zf - 0.2, 0.6, DARKINT, skip=())
    slab(m, "n", 14.8, 18.6, 3, 11, zf - 0.8, 0.3, glass("#9fc4de", 90), skip=())
    m.box((-W / 2 + 1, 3, -D / 2 + 1), (W / 2 - 1, 3.4, D / 2 - 1), paint("#8a6a48", noise=7))
    m.box((-4, 3.4, -D / 2 + 1), (4, 3.7, D / 2 - 1), planks("#c9b99a", 2.0, True), skip=())
    cols = ["#e8453c", "#f7d34a", "#f08ab4", "#f4f0e6", "#9b6fd6"]
    rng = random.Random(77)
    for side in (-1, 1):
        for row in range(2):
            x0 = side * (8 + row * 7.5)
            m.box((x0 - 2.2, 3.4, -11.5), (x0 + 2.2, 6.0, 11.5), planks("#8a6038", 1.4), skip=())
            m.box((x0 - 1.8, 6.0, -11.1), (x0 + 1.8, 6.5, 11.1), paint("#4a3220", noise=8), skip=())
            for i in range(9):
                z = -10 + i * 2.5
                h = rng.uniform(2.5, 6.5)
                m.box((x0 - 0.25, 6.5, z - 0.25), (x0 + 0.25, 6.5 + h, z + 0.25), paint("#3f8f3a", noise=6), skip=())
                c = cols[(i + row * 2 + (side > 0)) % 5]
                m.box((x0 - 0.9, 6.5 + h - 0.2, z - 0.9), (x0 + 0.9, 6.5 + h + 1.4, z + 0.9), paint(c, noise=6), skip=())
                m.box((x0 - 1.4, 6.8 + h * 0.4, z - 0.3), (x0 + 1.4, 7.3 + h * 0.4, z + 0.3), paint("#2f6a22", noise=6), skip=())
    m.box((-1.4, 12.4, -D / 2 + 3), (1.4, 13.6, -D / 2 + 5), metal("#9aa0a6"), skip=())
    cyl_y(m, -17.5, 3.4, 11, 1.8, 2.2, {"all": paint("#b8643a", noise=5)})
    return m


def water_tower():
    m = Model("water_tower", 580)
    wood = planks("#7a5230", 1.6)
    iron = metal("#40454d")
    for sx in (-1, 1):
        for sz in (-1, 1):
            post(m, sx * 5, sz * 5, 0, 14, 1.4, wood)
    for y0 in (2.0, 8.0):
        for s in (-1, 1):
            m.box((-5.7, y0, s * 5 - 0.4), (5.7, y0 + 0.8, s * 5 + 0.4), wood, skip=())
            m.box((s * 5 - 0.4, y0, -5.7), (s * 5 + 0.4, y0 + 0.8, 5.7), wood, skip=())
    for s in (-1, 1):
        m.box((-5, 2.4, s * 5 - 0.35), (5, 9.2, s * 5 + 0.35), wood, rot=("z", 45, (0, 5.8, s * 5)), skip=())
        m.box((-5, 2.4, s * 5 - 0.35), (5, 9.2, s * 5 + 0.35), wood, rot=("z", -45, (0, 5.8, s * 5)), skip=())
        m.box((s * 5 - 0.35, 2.4, -5), (s * 5 + 0.35, 9.2, 5), wood, rot=("x", 45, (s * 5, 5.8, 0)), skip=())
        m.box((s * 5 - 0.35, 2.4, -5), (s * 5 + 0.35, 9.2, 5), wood, rot=("x", -45, (s * 5, 5.8, 0)), skip=())
    m.box((-6.2, 14, -6.2), (6.2, 15, 6.2), wood, skip=())
    cyl_y(m, 0, 15, 0, 7.6, 9.0, {"all": planks("#8a6038", 1.2, True, 0.7, 0.06)})
    for y in (15.4, 19.0, 23.0):
        cyl_y(m, 0, y, 0, 7.8, 0.7, {"all": iron})
    cyl_y(m, 0, 12.6, 0, 3.6, 1.4, {"all": iron})
    cyl_y(m, 0, 13.8, 0, 5.4, 1.2, {"all": iron})
    for y, r, h in ((24.0, 8.6, 1.0), (25.0, 6.6, 1.6), (26.6, 4.4, 1.6), (28.2, 2.4, 1.6)):
        cyl_y(m, 0, y, 0, r, h, {"all": shingle("#3a5a52")})
    m.box((-0.4, 29.8, -0.4), (0.4, 31.6, 0.4), iron, skip=())
    post(m, 0, 0, 4.6, 12.6, 1.0, iron)
    m.box((-0.5, 4.2, -6.4), (0.5, 5.0, 0.4), iron, skip=())
    m.box((-0.6, 3.4, -6.8), (0.6, 4.6, -5.6), iron, skip=())
    m.box((-4.5, 0, -12), (4.5, 2.6, -6.5), planks("#8a6038", 1.4), skip=())
    m.box((-4.0, 2.6, -11.6), (4.0, 2.9, -7.0), paint("#3a7bb5", noise=5), skip=())
    for y in range(3, 14, 2):
        m.box((-6.0, y, 6.2), (-4.6, y + 0.4, 7.0), iron, skip=())
    for x in (-5.8, -4.8):
        m.box((x - 0.2, 2.0, 6.2), (x + 0.2, 14.6, 7.0), iron, skip=())
    m.box((-1.0, 14.0, -7.8), (1.0, 14.6, -6.2), iron, skip=())
    return m


def garage():
    m = Model("garage", 590)
    W, D, ye = 36, 30, 14
    wall = corrug("#7d8a86")
    trim = paint("#40454d", noise=3)
    m.box((-W / 2 - 0.6, 0, -D / 2 - 0.6), (W / 2 + 0.6, 2, D / 2 + 0.6), paint("#8c8f94", noise=4))
    m.box((-W / 2, 2, -D / 2), (W / 2, ye, D / 2), wall)
    zf = -D / 2
    slab(m, "n", -12.4, 12.4, 2, 15.2, zf, 0.3, DARKINT, skip=())
    m.box((-12.4, 2, zf + 0.2), (12.4, 2.2, zf + 22), paint("#4a4d52", noise=4), skip=("down",))
    m.box((-11.9, 2.2, zf + 21), (11.9, 7, zf + 22), planks("#6b4a2a", 1.0), skip=())
    for sx in (-1, 1):
        m.box((sx * 10 - 1.2, 2.2, zf + 18), (sx * 10 + 1.2, 12, zf + 21), paint("#3a3a3e", noise=4), skip=())
        for yy in (4, 7, 10):
            m.box((sx * 10 - 3.0, yy, zf + 20.4), (sx * 10 + 3.0, yy + 0.6, zf + 21.2), paint("#c9962f", noise=4), skip=())
    slab(m, "n", -13.2, -12.4, 2, 16.0, zf, 0.9, trim, skip=())
    slab(m, "n", 12.4, 13.2, 2, 16.0, zf, 0.9, trim, skip=())
    slab(m, "n", -13.2, 13.2, 15.2, 16.0, zf, 0.9, trim, skip=())
    slab(m, "n", -13.2, 13.2, 2, 3.0, zf, 1.0, hazard("#e8b81a", "#1e1e1e", 2), skip=())
    sign = P(paint("#2a2d33"), ov_text("GARAGE", "#f2b134", 6))
    slab(m, "n", -6, 6, 16.4, 19.4, zf - 0.2, 0.6, sign, skip=())
    for sx in (-1, 1):
        m.box((sx * 8 - 0.7, 19.0, zf - 1.8), (sx * 8 + 0.7, 19.8, zf - 0.2), trim, skip=())
        m.box((sx * 8 - 0.6, 18.2, zf - 1.7), (sx * 8 + 0.6, 19.0, zf - 0.5), light("#fff0b0"), skip=())
    for z in (-6, 6):
        for xo, face in ((W / 2, "e"), (-W / 2, "w")):
            slab(m, face, z - 3, z + 3, 8.5, 11.5, xo, 0.4, glass("#9fc4de", 200), skip=())
            slab(m, face, z - 3.6, z + 3.6, 11.5, 12.1, xo, 0.8, trim, skip=())
            slab(m, face, z - 3.6, z + 3.6, 7.9, 8.5, xo, 0.8, trim, skip=())
    roof = corrug("#5a606a")
    rise = gable(m, W, D, ye, roof, wall, ov=1.4, fov=1.4, wall_t=1.0)
    m.box((-6, ye + rise + 0.6, -D / 4 - 3), (6, ye + rise + 1.6, -D / 4 + 3), glass("#9fc4de", 140), skip=())
    post(m, 8, D / 4, ye + rise, ye + rise + 5, 1.0, metal("#40454d"))
    cyl_y(m, 8, ye + rise + 5, D / 4, 1.2, 0.8, {"all": metal("#40454d")})
    for i in range(3):
        cyl_y(m, W / 2 + 3, i * 2.2, -4, 2.4, 2.2, {"all": paint("#1f1f20", noise=4), "up": paint("#2e2e30")})
    cyl_y(m, W / 2 + 3, 6.6, -4, 1.3, 0.8, {"all": paint("#1f1f20", noise=4)})
    for i in range(2):
        cyl_y(m, -W / 2 - 3, 0, -9 + i * 5, 1.9, 5.0, {"all": paint("#2f5fa8" if i == 0 else "#a8342b", noise=4)})
        cyl_y(m, -W / 2 - 3, 5.0, -9 + i * 5, 1.9, 0.6, {"all": metal("#9aa0a6")})
    return m


def all_buildings():
    out = []
    for t in (1, 2, 3):
        for lit in (False, True):
            out.append(farmhouse(t, lit))
    out += [barn(), silo(), coop(), mill(), bakery(False), bakery(True), greenhouse(), water_tower(), garage()]
    return out
