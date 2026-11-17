import random
from lib import *
import vehicles

STEEL = "#6d7076"


def camo(colors, cell=3):
    cs = [rgb(c) for c in colors]

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        v1 = vnoise(ctx.pw, ctx.ph, max(3, cell * DENSITY), random.Random(ctx.pw * 13 + ctx.ph))
        v2 = vnoise(ctx.pw, ctx.ph, max(2, cell * DENSITY // 2 + 1), random.Random(ctx.pw * 7 + ctx.ph * 3))
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                t = v1[y][x] * 0.7 + v2[y][x] * 0.3
                c = cs[0] if t < 0.38 else cs[1] if t < 0.52 else cs[2] if t < 0.66 else cs[3]
                n = ctx.rng.uniform(-4, 4)
                px[x, y] = (clamp(c[0] + n), clamp(c[1] + n), clamp(c[2] + n), 255)
        return img

    return f


def bricks(color="#8c8f94", mortar="#4d4f53", rh=2.0, bw=4.0):
    c, mo = rgb(color), rgb(mortar)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        rhp, bwp = max(2, int(rh * DENSITY)), max(3, int(bw * DENSITY))
        for y in range(ctx.ph):
            row = y // rhp
            for x in range(ctx.pw):
                xx = x + (bwp // 2 if row % 2 else 0)
                if y % rhp == rhp - 1 or xx % bwp == bwp - 1:
                    col, k = mo, 1.0
                else:
                    pr = random.Random(row * 131 + xx // bwp * 17)
                    col, k = c, 1 + pr.uniform(-0.1, 0.1)
                n = ctx.rng.uniform(-3, 3)
                px[x, y] = (clamp(col[0] * k + n), clamp(col[1] * k + n), clamp(col[2] * k + n), 255)
        return img

    return f


def box_ring(m, hw, hd, y0, y1, t, mat, cz=0.0):
    m.box((-hw, y0, cz - hd), (hw, y1, cz - hd + t), mat, skip=())
    m.box((-hw, y0, cz + hd - t), (hw, y1, cz + hd), mat, skip=())
    m.box((-hw, y0, cz - hd + t), (-hw + t, y1, cz + hd - t), mat, skip=())
    m.box((hw - t, y0, cz - hd + t), (hw, y1, cz + hd - t), mat, skip=())


def hat_straw():
    m = Model("hat_straw", 201)
    s = straw()
    s2 = straw("#cfae4f")
    cyl_y(m, 0, -0.2, 0, 6.9, 0.9, {"all": s, "up": s2})
    cyl_y(m, 0, 0.7, 0, 4.5, 3.4, {"all": s, "up": s2})
    cyl_y(m, 0, 4.1, 0, 3.9, 0.5, {"all": s2})
    cyl_y(m, 0, 0.7, 0, 4.7, 1.1, {"all": P(paint("#b3322a", noise=3), ov_stripe("#7d1f1a", 0.5, 0.5, False))})
    m.box((3.6, 0.9, -1.0), (4.6, 2.9, 0.2), paint("#6b4a2a"), rot=("z", 22.5, (4.1, 0.9, -0.4)), skip=())
    m.box((3.9, 2.4, -0.9), (4.9, 4.4, 0.1), paint("#9a7040"), rot=("z", 22.5, (4.1, 2.4, -0.4)), skip=())
    return m


def hat_cowboy():
    m = Model("hat_cowboy", 202)
    felt = paint("#8a5a32", noise=5)
    felt2 = paint("#7a4c28", noise=5)
    band = paint("#2d1f14", noise=3)
    m.box((-5.6, -0.2, -7.2), (5.6, 0.6, 7.2), {"up": felt, "all": felt2})
    for s in (-1, 1):
        m.box((s * 5.5, 0.0, -6.4), (s * 8.6, 0.8, 6.4), {"up": felt, "all": felt2}, rot=("z", -22.5 * s, (s * 5.5, 0.4, 0)), skip=())
    m.box((-5.0, -0.2, -7.6), (5.0, 0.7, -6.8), felt2, rot=("x", -22.5, (0, 0.3, -6.8)), skip=())
    m.box((-4.2, 0.6, -4.4), (4.2, 3.4, 4.4), felt, skip=())
    m.box((-3.7, 3.4, -4.0), (3.7, 5.6, 4.0), felt, skip=())
    for s in (-1, 1):
        m.box((s * 2.5 - 0.9, 5.6, -3.9), (s * 2.5 + 0.9, 6.6, 3.9), felt, skip=())
    m.box((-1.6, 5.6, -3.9), (1.6, 5.9, 3.9), felt2, skip=())
    m.box((-4.4, 0.6, -4.6), (4.4, 1.7, 4.6), band, skip=())
    m.box((-1.0, 0.7, -4.9), (1.0, 1.6, -4.6), metal("#cfd3d8"), skip=())
    for x in (-3.2, 3.2):
        m.box((x - 0.4, 0.9, -4.75), (x + 0.4, 1.4, -4.55), metal("#cfd3d8"), skip=())
    return m


def hat_flatcap():
    m = Model("hat_flatcap", 203)
    tw = plaid("#55683a", "#7b9150", 1.0)
    tw2 = plaid("#4a5b32", "#6a7e45", 1.0)
    m.box((-4.5, -0.2, -4.6), (4.5, 1.5, 4.6), tw, skip=())
    m.box((-4.7, 1.5, -3.8), (4.7, 2.8, 4.2), tw2, skip=())
    m.box((-3.8, 2.8, -2.8), (3.8, 3.2, 3.2), tw, skip=())
    m.box((-3.8, 0.0, -7.2), (3.8, 0.9, -4.4), paint("#2f3a1e", noise=3), rot=("x", 22.5, (0, 0.4, -4.4)), skip=())
    m.box((-0.5, 3.2, 0.0), (0.5, 3.8, 1.0), paint("#2f3a1e"), skip=())
    return m


def hat_flowercrown():
    m = Model("hat_flowercrown", 204)
    vine = paint("#3f7a2e", noise=7)
    box_ring(m, 4.6, 4.6, -0.5, 0.5, 1.0, vine)
    cols = ["#e8453c", "#f7d34a", "#f4f0e6", "#f08ab4", "#9b6fd6", "#f7d34a", "#e8453c", "#f4f0e6"]
    pos = [(-3.6, -4.8), (0, -5.0), (3.6, -4.8), (5.0, 0), (3.6, 4.8), (0, 5.0), (-3.6, 4.8), (-5.0, 0)]
    for (x, z), c in zip(pos, cols):
        m.box((x - 0.9, -0.5, z - 0.9), (x + 0.9, 1.6, z + 0.9), paint(c, noise=6), skip=())
        m.box((x - 0.4, 0.7, z - 0.4), (x + 0.4, 1.9, z + 0.4), paint("#f7d34a" if c != "#f7d34a" else "#d97a1c"), skip=())
    for i, (x, z) in enumerate([(-1.8, -5.0), (1.8, -5.0), (5.0, -1.8), (5.0, 1.8), (1.8, 5.0), (-1.8, 5.0), (-5.0, 1.8), (-5.0, -1.8)]):
        m.box((x - 0.7, 0.2, z - 0.7), (x + 0.7, 1.2, z + 0.7), paint("#2f6a22", noise=6), skip=())
    return m


def hat_pumpkin():
    m = Model("hat_pumpkin", 205)
    pk = P(paint("#e8821c", noise=5), ov_stripe("#b85e10", 0.25, 0.5, True), ov_stripe("#b85e10", 0.75, 0.5, True))
    pk2 = paint("#f09a2c", noise=5)
    cyl_y(m, 0, -0.2, 0, 4.7, 4.0, {"all": pk, "up": pk2})
    cyl_y(m, 0, 0.0, 0, 5.0, 3.0, {"all": pk})
    cyl_y(m, 0, 3.6, 0, 3.4, 0.8, {"all": pk})
    m.box((-0.8, 4.4, -0.8), (0.8, 6.2, 0.8), paint("#5c7a2a", noise=5), skip=())
    m.box((0.2, 5.6, -0.7), (1.8, 6.6, 0.7), paint("#5c7a2a", noise=5), rot=("z", 22.5, (0.2, 5.6, 0)), skip=())
    m.box((1.0, 3.4, -2.6), (4.2, 3.8, 0.2), paint("#4f9a2a", noise=6), rot=("z", 22.5, (1.0, 3.6, 0)), skip=())
    m.box((-3.8, 2.6, -4.2), (-1.6, 3.2, -3.6), paint("#4f9a2a"), skip=())
    return m


def back_basket():
    m = Model("back_basket", 211)
    wick = P(planks("#b88a4a", 1.0, True), ov_stripe("#8a6230", 0.33, 0.5, False), ov_stripe("#8a6230", 0.66, 0.5, False))
    rim = planks("#8a6230", 1.2)
    leather = paint("#6b4423", noise=4)
    m.box((-4.5, 1.0, 2.4), (4.5, 8.0, 8.6), wick, skip=())
    m.box((-4.8, 7.6, 2.2), (4.8, 8.6, 8.8), rim, skip=())
    for s in (-1, 1):
        m.box((s * 3.2 - 0.6, 0.5, 1.8), (s * 3.2 + 0.6, 12.2, 2.4), leather, skip=())
        m.box((s * 3.2 - 0.6, 0.5, 2.4), (s * 3.2 + 0.6, 1.5, 3.0), leather, skip=())
    for x, c in ((-2.8, "#e0b94a"), (-0.2, "#e0b94a"), (2.6, "#d4a73a")):
        m.box((x - 0.4, 8.0, 4.0), (x + 0.4, 13.4, 4.8), paint(c, noise=5), skip=())
        m.box((x - 0.8, 11.8, 3.8), (x + 0.8, 14.2, 5.0), paint("#c9962f", noise=5), skip=())
    for x, z, c in ((-2.8, 6.4, "#d6332a"), (0.4, 7.0, "#c7281f"), (3.0, 6.2, "#d6332a")):
        m.box((x - 1.2, 8.2, z - 1.2), (x + 1.2, 10.4, z + 1.2), paint(c, noise=6), skip=())
        m.box((x - 0.15, 10.4, z - 0.15), (x + 0.15, 11.2, z + 0.15), paint("#4a3220"), skip=())
    m.box((1.4, 8.2, 3.6), (2.6, 11.8, 4.6), paint("#e8821c", noise=5), skip=())
    m.box((1.0, 11.8, 3.4), (3.0, 13.2, 4.8), paint("#3f9a2a", noise=6), skip=())
    m.box((-4.2, 8.2, 3.4), (-2.6, 10.6, 5.0), paint("#f2c230", noise=5), skip=())
    return m


def back_haybale():
    m = Model("back_haybale", 212)
    hay = P(straw("#dcc05a"), ov_stripe("#6b4a2a", 0.25, 0.5, False), ov_stripe("#6b4a2a", 0.75, 0.5, False))
    leather = paint("#6b4423", noise=4)
    m.box((-4.8, 0.0, 2.4), (4.8, 8.0, 9.0), {"east": straw("#c9a940"), "west": straw("#c9a940"), "all": hay}, skip=())
    for i in range(5):
        x = -3.6 + i * 1.8
        m.box((x - 0.3, 8.0, 3.0 + (i % 2)), (x + 0.3, 9.6 + (i % 3) * 0.6, 3.4 + (i % 2)), straw("#e3c565"), skip=())
    for s in (-1, 1):
        m.box((s * 3.2 - 0.6, 0.5, 1.8), (s * 3.2 + 0.6, 12.2, 2.4), leather, skip=())
    m.box((5.0, -3.0, 4.6), (5.8, 14.0, 5.4), planks("#8a6038", 1.5, True), rot=("z", -22.5, (5.4, 4.0, 5.0)), skip=())
    for dx in (-1.0, 0, 1.0):
        m.box((5.4 + dx - 0.25, 14.0, 4.7), (5.4 + dx + 0.25, 16.6, 5.3), metal("#b9bdc3"), rot=("z", -22.5, (5.4, 4.0, 5.0)), skip=())
    return m


def back_scythe():
    m = Model("back_scythe", 213)
    wood = planks("#8a6038", 1.5, True)
    steel = metal("#c7cbd1")
    leather = paint("#6b4423", noise=4)
    m.box((-0.5, -4.0, 2.4), (0.5, 21.0, 3.4), wood, rot=("z", 22.5, (0.0, 6.0, 2.9)), skip=())
    m.box((-1.4, 6.0, 1.8), (1.4, 7.0, 4.0), leather, skip=())
    pts = [(5.0, 20.8), (2.9, 21.6), (0.7, 21.6), (-1.4, 20.8), (-3.2, 19.4), (-4.6, 17.6)]
    for i, (x, y) in enumerate(pts):
        th = 1.7 - i * 0.2
        m.box((x - 1.9, y - th / 2, 2.3), (x + 1.9, y + th / 2, 3.3), steel, rot=("z", -(8 + i * 10), (x, y, 2.8)), skip=())
    m.box((4.4, 19.8, 2.2), (6.4, 21.6, 3.6), metal("#55585e"), skip=())
    for s in (-1, 1):
        m.box((s * 3.2 - 0.6, 0.5, 1.8), (s * 3.2 + 0.6, 12.2, 2.4), leather, skip=())
    return m


SKINS = {
    "camo": dict(body=camo(["#4b5d2e", "#2f3b1d", "#7a6a3c", "#1f2615"]), body_c="#3d4b26", trim="#c8b88a"),
    "midnight": dict(body="#17181c", trim="#d4a72c"),
    "sunrise": dict(body="#ee7b1c", trim="#ffd25a"),
    "arctic": dict(body="#e9eef2", trim="#4aa3df"),
}
SIZES = [
    ("small", dict(k=0.8, cab=False, dual=False, seed=21, label="HM-1")),
    ("medium", dict(k=0.95, cab=True, dual=False, seed=22, label="HM-5")),
    ("large", dict(k=1.05, cab=True, dual=True, seed=23, label="HM-9")),
]


def tractor_skins():
    out = []
    for si, (skin, sk) in enumerate(SKINS.items()):
        for size, kw in SIZES:
            args = dict(kw)
            args.update(sk)
            args["seed"] = kw["seed"] + si * 10
            out.append(vehicles.tractor(f"tractor_{size}_{skin}", **args))
    return out


ANCHORS = {
    "cow": dict(head=(21.0, -12.2, 6.4), neck=(14.2, -8.6, 7.8, 5.4, 2.8), bow=(0.0, 21.0, -11.6)),
    "pig": dict(head=(14.8, -9.2, 7.2), neck=(10.3, -7.1, 8.2, 2.8, 2.8), bow=(0.0, 14.9, -10.0)),
    "sheep": dict(head=(21.0, -10.4, 6.0), neck=(14.8, -8.2, 8.6, 3.6, 3.4), bow=(0.0, 21.2, -10.2)),
    "chicken": dict(head=(16.4, -3.9, 4.0), neck=(10.6, -3.8, 5.6, 3.8, 1.6), bow=(2.3, 14.2, -3.9)),
}


def acc_sunhat(an, a):
    hy, hz, hw = a["head"]
    k = hw / 6.4
    m = Model(f"acc_sunhat_{an}", 301)
    s, s2 = straw(), straw("#cfae4f")
    cyl_y(m, 0, hy, hz, 6.0 * k + 0.6, 0.8, {"all": s, "up": s2})
    cyl_y(m, 0, hy + 0.7, hz, 3.6 * k + 0.4, 2.8 * k + 0.6, {"all": s, "up": s2})
    cyl_y(m, 0, hy + 0.7, hz, 3.8 * k + 0.4, 0.9, {"all": paint("#e8453c", noise=3)})
    return m


def acc_party(an, a):
    hy, hz, hw = a["head"]
    k = hw / 6.4
    m = Model(f"acc_party_{an}", 302)
    cols = ["#e8453c", "#f7d34a", "#3aa6e8", "#f08ab4", "#7bd45a"]
    r = 3.0 * k + 0.4
    for i in range(5):
        cyl_y(m, 0, hy + i * 1.1 * k, hz, max(0.5, r - i * 0.6 * k), 1.1 * k, {"all": paint(cols[i % 5], noise=4)})
    m.box((-0.5, hy + 5.4 * k, hz - 0.5), (0.5, hy + 6.4 * k, hz + 0.5), metal("#f2c94c"), skip=())
    return m


def acc_bow(an, a):
    bx, by, bz = a["bow"]
    k = 1.0 if an != "chicken" else 0.7
    m = Model(f"acc_bow_{an}", 303)
    red = P(paint("#d6332a", noise=4), ov_dots("#f4f0e6", 3, 1))
    for s in (-1, 1):
        m.box((bx + s * 0.9 * k - (0 if s > 0 else 2.2 * k), by - 1.2 * k, bz - 0.6), (bx + s * 0.9 * k + (2.2 * k if s > 0 else 0), by + 1.2 * k, bz + 0.6), red, skip=())
        m.box((bx + s * 2.6 * k - (0 if s > 0 else 1.0 * k), by - 1.8 * k, bz - 0.5), (bx + s * 2.6 * k + (1.0 * k if s > 0 else 0), by + 1.8 * k, bz + 0.5), red, skip=())
    m.box((bx - 0.9 * k, by - 0.9 * k, bz - 0.8), (bx + 0.9 * k, by + 0.9 * k, bz + 0.8), paint("#a8231b"), skip=())
    return m


def acc_scarf(an, a):
    cy, cz, w, d, h = a["neck"]
    m = Model(f"acc_scarf_{an}", 304)
    st = P(paint("#c0392b", noise=3), ov_stripe("#f4f0e6", 0.2, 0.6, False), ov_stripe("#f4f0e6", 0.55, 0.6, False), ov_stripe("#f4f0e6", 0.9, 0.6, False))
    st2 = P(paint("#c0392b", noise=3), ov_stripe("#f4f0e6", 0.5, 0.8, True))
    m.box((-w / 2, cy - h / 2, cz - d / 2), (w / 2, cy + h / 2, cz + d / 2), {"all": st, "up": st2}, skip=())
    tail_h = h * 2.0
    m.box((w / 2 - 0.4, cy - h / 2 - tail_h, cz - d / 2 - 0.2), (w / 2 + 0.6, cy + h / 2 - 0.3, cz - d / 2 + 1.2), st, skip=())
    for i in range(3):
        m.box((w / 2 - 0.3 + i * 0.3, cy - h / 2 - tail_h - 0.6, cz - d / 2 - 0.1), (w / 2 - 0.1 + i * 0.3, cy - h / 2 - tail_h, cz - d / 2 + 0.1), paint("#f4f0e6"), skip=())
    return m


def accessories():
    out = []
    for an, a in ANCHORS.items():
        for fn in (acc_sunhat, acc_party, acc_bow, acc_scarf):
            out.append(fn(an, a))
    return out


def deco_scarecrow():
    m = Model("deco_scarecrow", 401)
    wood = planks("#8a6038", 1.5, True)
    pl = plaid("#3d6bb0", "#6e9ad6", 1.2)
    den = P(cloth("#4a6a96", 1, 5), ov_rect("#a8342b", 1.0, 1.2, 2.0, 2.0), ov_frame("#2e4668", 0.3))
    hay = straw("#e8c866")
    m.box((-0.9, 0, -0.9), (0.9, 22.0, 0.9), wood, skip=())
    m.box((-11.5, 15.8, -0.8), (11.5, 17.4, 0.8), wood, skip=())
    m.box((-4.5, 9.5, -2.3), (4.5, 19.5, 2.3), P(pl, ov_rect("#b58a3a", 4.4, 2.0, 3.0, 3.0)), skip=())
    m.box((-3.9, 2.4, -2.0), (3.9, 9.6, 2.0), den, skip=())
    for x in (-2.0, 0.0, 2.0):
        m.box((x - 0.5, 0.0, -0.5), (x + 0.5, 2.8, 0.5), hay, rot=("z", 22.5 * (1 if x > 0 else -1 if x < 0 else 0)) if x else None, skip=())
    for s in (-1, 1):
        m.box((s * 4.4, 15.0, -1.8), (s * 10.4, 19.2, 1.8), pl, skip=())
        for j, dy in enumerate((16.2, 17.6, 18.8)):
            m.box((s * 10.4, dy - 0.3, -0.6 + j * 0.5 - 0.5), (s * 12.8, dy + 0.3, -0.6 + j * 0.5 + 0.1), hay, skip=())
    face = P(paint("#c9a867", noise=7), ov_draw(lambda d, c, i: (
        d.rectangle([c.X(1.4), c.X(2.0), c.X(2.6) - 1, c.X(3.2) - 1], fill=(30, 24, 20, 255)),
        d.rectangle([c.X(4.4), c.X(2.0), c.X(5.6) - 1, c.X(3.2) - 1], fill=(30, 24, 20, 255)),
        d.polygon([(c.X(3.4), c.X(3.6)), (c.X(4.0), c.X(3.6)), (c.X(3.7), c.X(4.6))], fill=(168, 90, 48, 255)),
        [d.line([c.X(1.6 + j * 0.9), c.X(5.2 + (0.4 if j in (0, 5) else 0)), c.X(1.6 + j * 0.9), c.X(6.0)], fill=(60, 40, 28, 255)) for j in range(6)],
        d.line([c.X(1.6), c.X(5.2), c.X(6.2), c.X(5.2)], fill=(60, 40, 28, 255)))))
    m.box((-3.6, 19.5, -3.6), (3.6, 26.7, 3.6), {"north": face, "all": burlap("#c9a867")}, skip=())
    cyl_y(m, 0, 26.2, 0, 6.2, 0.8, {"all": straw(), "up": straw("#cfae4f")})
    cyl_y(m, 0, 26.9, 0, 3.6, 3.2, {"all": straw()})
    cyl_y(m, 0, 26.9, 0, 3.8, 1.0, {"all": paint("#8a2f26", noise=3)})
    black = paint("#1b1b1f", noise=3)
    m.box((9.4, 19.2, -1.2), (12.4, 21.6, 1.2), black, skip=())
    m.box((11.4, 21.2, -0.9), (13.4, 23.2, 0.9), black, skip=())
    m.box((13.4, 22.2, -0.4), (14.8, 22.8, 0.4), paint("#f0b82a"), skip=())
    m.box((8.4, 19.4, -0.8), (9.4, 20.4, 0.8), black, rot=("z", 22.5, (9.4, 19.8, 0)), skip=())
    return m


def deco_windmill():
    m = Model("deco_windmill", 402)
    plaster = paint("#efe8d8", noise=4)
    stone = bricks("#8c8f94", "#4d4f53")
    wood = planks("#7a5230", 1.6)
    roof = planks("#4a3320", 1.4)
    cyl_y(m, 0, 0, 0, 8.4, 3.0, {"all": stone})
    cyl_y(m, 0, 3.0, 0, 7.8, 4.0, {"all": plaster})
    cyl_y(m, 0, 7.0, 0, 7.0, 6.0, {"all": plaster})
    cyl_y(m, 0, 13.0, 0, 6.2, 5.0, {"all": plaster})
    cyl_y(m, 0, 18.0, 0, 5.4, 4.0, {"all": plaster})
    for y, r in ((6.6, 7.4), (12.6, 6.6), (17.6, 5.8)):
        cyl_y(m, 0, y, 0, r + 0.15, 0.8, {"all": wood})
    cyl_y(m, 0, 22.0, 0, 6.0, 1.6, {"all": roof})
    cyl_y(m, 0, 23.6, 0, 4.8, 1.4, {"all": roof})
    cyl_y(m, 0, 25.0, 0, 3.4, 1.4, {"all": roof})
    cyl_y(m, 0, 26.4, 0, 1.8, 1.4, {"all": roof})
    m.box((-0.5, 27.8, -0.5), (0.5, 30.4, 0.5), metal("#c9962f"), skip=())
    m.box((-2.0, 0.0, -9.2), (2.0, 6.0, -7.6), {"north": P(wood, ov_stripe("#3a2418", 0.5, 0.5, True), ov_rect("#c9962f", 3.2, 6.0, 0.8, 0.8)), "all": wood}, skip=())
    m.box((-2.4, 6.0, -9.4), (2.4, 6.8, -7.4), wood, skip=())
    for y in (9.5, 15.0):
        m.box((-1.4, y, -8.2), (1.4, y + 2.6, -6.2), {"north": glass("#ffe9a0", 190), "all": wood}, skip=())
    m.box((-1.4, 17.8, -10.4), (1.4, 22.0, -5.6), wood, skip=())
    m.box((-1.0, 19.0, -10.6), (1.0, 21.0, -9.4), metal("#55585e"), skip=())
    for s in (-1, 1):
        m.box((s * 7.6 - 0.4, 0, 3.0), (s * 7.6 + 0.4, 6.0, 4.0), wood, skip=())
    return m


def deco_windmill_blades():
    m = Model("deco_windmill_blades", 403)
    wood = planks("#7a5230", 1.2, True)
    sail = cloth("#efe6cf", 1, 4)
    m.box((-1.3, 6.7, -1.3), (1.3, 9.3, 1.3), metal("#55585e"), skip=())
    for ang in (0, 90, 180, 270):
        pass

    def arm(ax, sx, sy):
        pass

    L, W = 15.0, 4.6
    m.box((-0.5, 8.0 + 1.0, -0.5), (0.5, 8.0 + L, 0.5), wood, skip=())
    m.box((-0.5, 8.0 - L, -0.5), (0.5, 8.0 - 1.0, 0.5), wood, skip=())
    m.box((1.0 - 0.5, 8.0 - 1.0, -0.5), (L, 8.0 - 1.0 + 1.0, 0.5), wood, skip=())
    m.box((-L, 8.0 + 0.0, -0.5), (-1.0, 8.0 + 1.0, 0.5), wood, skip=())
    m.box((0.5, 8.0 + 3.0, -0.3), (0.5 + W, 8.0 + L - 0.5, 0.3), sail, skip=())
    m.box((-0.5 - W, 8.0 - L + 0.5, -0.3), (-0.5, 8.0 - 3.0, 0.3), sail, skip=())
    m.box((3.0, 8.0 - 0.5 - W, -0.3), (L - 0.5, 8.0 - 0.5, 0.3), sail, skip=())
    m.box((-L + 0.5, 8.0 + 0.5, -0.3), (-3.0, 8.0 + 0.5 + W, 0.3), sail, skip=())
    for i in range(1, 5):
        t = 3.0 + i * 2.6
        m.box((0.5, 8.0 + t - 0.2, -0.45), (0.5 + W, 8.0 + t + 0.2, 0.45), wood, skip=())
        m.box((-0.5 - W, 8.0 - t - 0.2, -0.45), (-0.5, 8.0 - t + 0.2, 0.45), wood, skip=())
        m.box((t - 0.2, 8.0 - 0.5 - W, -0.45), (t + 0.2, 8.0 - 0.5, 0.45), wood, skip=())
        m.box((-t - 0.2, 8.0 + 0.5, -0.45), (-t + 0.2, 8.0 + 0.5 + W, 0.45), wood, skip=())
    for rect in ((0.5 + W - 0.4, 8.0 + 3.0, 0.5 + W, 8.0 + L - 0.5), (-0.5 - W, 8.0 - L + 0.5, -0.5 - W + 0.4, 8.0 - 3.0)):
        m.box((rect[0], rect[1], -0.5), (rect[2], rect[3], 0.5), wood, skip=())
    return m


def deco_gnome():
    m = Model("deco_gnome", 404)
    skin = paint("#efb08a", noise=4)
    blue = cloth("#2f5fa8", 1, 5)
    red = cloth("#d6332a", 1, 5)
    white = fur("#f4f4f0", "#dcdcd4", 3, 0.6, 5)
    boot = paint("#4d3220", noise=3)
    for s in (-1, 1):
        m.box((s * 1.6 - 1.4, 0, -2.0), (s * 1.6 + 1.4, 2.6, 2.4), boot, skip=())
        m.box((s * 1.6 - 1.1, 2.6, -1.2), (s * 1.6 + 1.1, 4.6, 1.2), paint("#6b4a2a", noise=3), skip=())
    m.box((-3.4, 4.6, -2.4), (3.4, 9.6, 2.4), {"north": P(blue, ov_rect("#c9962f", 0.0, 3.4, 6.8, 0.8), ov_rect("#f2c94c", 2.8, 3.2, 1.2, 1.2)), "all": blue}, skip=())
    for s in (-1, 1):
        m.box((s * 3.4, 5.4, -1.2), (s * 4.8, 9.0, 1.2), blue, skip=())
        m.box((s * 3.4, 4.4, -1.0), (s * 4.8, 5.6, 1.0), skin, skip=())
    m.box((-3.0, 9.6, -2.8), (3.0, 14.0, 2.8), {"north": P(skin, eyes_g(), ov_rect("#e57f8a", 0.2, 3.2, 1.0, 0.8, 120), ov_rect("#e57f8a", 4.8, 3.2, 1.0, 0.8, 120)), "all": skin}, skip=())
    m.box((-0.9, 10.8, -3.8), (0.9, 12.4, -2.8), paint("#f0a088"), skip=())
    m.box((-3.2, 6.0, -3.6), (3.2, 11.0, -2.5), white, skip=())
    m.box((-2.4, 4.4, -3.4), (2.4, 6.2, -2.7), white, skip=())
    for i, (w, h) in enumerate(((3.4, 1.4), (2.6, 1.4), (1.8, 1.4), (1.0, 1.4), (0.5, 1.2))):
        y = 13.6 + i * 1.4
        m.box((-w, y, -w), (w, y + h, w), red if i % 2 == 0 else paint("#e0453a", noise=4), rot=("z", 0) if False else None, skip=())
    m.box((-3.6, 13.6, -3.6), (3.6, 14.6, 3.6), red, skip=())
    return m


def eyes_g():
    def f(d, ctx, img):
        for x in (1.2, 3.8):
            X0, Y0 = ctx.X(x), ctx.X(1.8)
            d.rectangle([X0, Y0, X0 + 3, Y0 + 3], fill=(24, 24, 28, 255))
    return ov_draw(f)


def deco_haystack():
    m = Model("deco_haystack", 405)
    hay = P(straw("#dcc05a"), ov_stripe("#6b4a2a", 0.3, 0.5, True), ov_stripe("#6b4a2a", 0.7, 0.5, True))
    end = straw("#c9a940")
    m.box((-11.0, 0, -4.0), (-1.0, 6.0, 4.0), {"east": end, "west": end, "all": hay}, skip=())
    m.box((1.0, 0, -4.0), (11.0, 6.0, 4.0), {"east": end, "west": end, "all": hay}, skip=())
    m.box((-5.0, 6.0, -4.0), (5.0, 12.0, 4.0), {"east": end, "west": end, "all": hay}, skip=())
    for i in range(6):
        m.box((-10 + i * 3.6, 6.0, -4.3 + (i % 2) * 8.0), (-8.4 + i * 3.6, 6.4 + (i % 3) * 0.6, -3.7 + (i % 2) * 8.0), straw("#e8c866"), skip=())
    cyl_x(m, 0, 4.0, 11.0, 4.0, 7.0, {"all": hay, "east": end, "west": end})
    m.box((-0.25, 0.0, 8.4), (0.25, 7.0, 8.9), wood_g(), rot=("x", 22.5, (0, 0, 8.4)), skip=())
    for dx in (-0.8, 0, 0.8):
        m.box((dx - 0.2, 7.0, 6.9), (dx + 0.2, 9.4, 7.5), metal("#b9bdc3"), skip=())
    m.box((-1.2, 6.6, 7.0), (1.2, 7.2, 7.5), metal("#8f9399"), skip=())
    return m


def wood_g():
    return planks("#8a6038", 1.5, True)


def deco_flowerbed():
    m = Model("deco_flowerbed", 406)
    wood = planks("#8a6038", 2.0)
    soil = paint("#4a3220", noise=8)
    m.box((-11, 0, -6), (11, 4.0, 6), {"up": soil, "all": wood}, skip=())
    m.box((-10, 3.4, -5), (10, 4.4, 5), soil, skip=())
    rng = random.Random(9)
    cols = ["#e8453c", "#f7d34a", "#f4f0e6", "#f08ab4", "#9b6fd6", "#f2862a"]
    for i in range(-4, 5):
        for j in range(-2, 3):
            x = i * 2.3 + rng.uniform(-0.4, 0.4)
            z = j * 2.1 + rng.uniform(-0.4, 0.4)
            h = rng.uniform(3.0, 6.0)
            c = cols[(i * 3 + j * 5) % len(cols)]
            m.box((x - 0.25, 4.0, z - 0.25), (x + 0.25, 4.0 + h, z + 0.25), paint("#3f8f3a", noise=6), skip=())
            m.box((x - 0.9, 4.0 + h - 0.2, z - 0.9), (x + 0.9, 4.0 + h + 1.4, z + 0.9), paint(c, noise=6), skip=())
            m.box((x - 0.4, 4.0 + h + 0.7, z - 0.4), (x + 0.4, 4.0 + h + 1.7, z + 0.4), paint("#f7d34a" if c != "#f7d34a" else "#d97a1c"), skip=())
            m.box((x + 0.2, 4.0 + h * 0.4, z - 0.6), (x + 1.4, 4.0 + h * 0.4 + 0.5, z + 0.6), paint("#2f6a22", noise=6), skip=())
    for x, z in ((-8.5, 4.8), (8.5, -4.8)):
        m.box((x - 0.4, 4.0, z - 0.4), (x + 0.4, 9.0, z + 0.4), paint("#8f6fd0", noise=6), skip=())
    return m


def deco_well():
    m = Model("deco_well", 407)
    stone = bricks("#8c8f94", "#4d4f53")
    wood = planks("#7a5230", 1.6)
    roof = planks("#4a3320", 1.4)
    water = P(stone, ov_draw(lambda d, c, i: (d.ellipse([c.X(1.6), c.X(1.6), c.pw - c.X(1.6) - 1, c.ph - c.X(1.6) - 1], fill=(30, 36, 44, 255)), d.ellipse([c.X(2.2), c.X(2.2), c.pw - c.X(2.2) - 1, c.ph - c.X(2.2) - 1], fill=(58, 110, 170, 255)))))
    m.box((-6.0, 0, -6.0), (6.0, 6.0, 6.0), {"up": water, "all": stone}, skip=())
    m.box((-6.4, 5.4, -6.4), (6.4, 6.4, -4.4), stone, skip=())
    m.box((-6.4, 5.4, 4.4), (6.4, 6.4, 6.4), stone, skip=())
    m.box((-6.4, 5.4, -4.4), (-4.4, 6.4, 4.4), stone, skip=())
    m.box((4.4, 5.4, -4.4), (6.4, 6.4, 4.4), stone, skip=())
    for s in (-1, 1):
        m.box((s * 5.6 - 0.6, 6.4, -0.6), (s * 5.6 + 0.6, 17.0, 0.6), wood, skip=())
    m.box((-6.4, 16.0, -0.7), (6.4, 17.2, 0.7), wood, skip=())
    for s in (-1, 1):
        m.box((s * 3.4 - 3.6, 17.0, -4.6), (s * 3.4 + 3.6, 17.8, 4.6), roof, rot=("z", 22.5 * s, (s * 6.4 * 0.0, 17.0, 0)), skip=())
    m.box((-0.5, 17.6, -4.8), (0.5, 20.2, 4.8), roof, skip=())
    m.box((-0.12, 9.6, -0.12), (0.12, 16.0, 0.12), paint("#b89c6a", noise=5), skip=())
    m.box((-1.5, 6.6, -1.5), (1.5, 9.8, 1.5), P(planks("#8a6038", 1.0, True), ov_stripe("#55585e", 0.2, 0.7, False), ov_stripe("#55585e", 0.8, 0.7, False)), skip=())
    return m


def all_models():
    out = [hat_straw(), hat_cowboy(), hat_flatcap(), hat_flowercrown(), hat_pumpkin(), back_basket(), back_haybale(), back_scythe()]
    out += tractor_skins()
    out += accessories()
    out += [deco_scarecrow(), deco_windmill(), deco_windmill_blades(), deco_gnome(), deco_haystack(), deco_flowerbed(), deco_well()]
    return out
