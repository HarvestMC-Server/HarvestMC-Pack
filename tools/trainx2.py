import random
from lib import *
from bld import siding, corrug, slab, post, shingle
from trainx import train_coach, part_coach_door


RAIL_TOP = 3.7
GAUGE = 5.4


def gravel(color="#8a8d92"):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        v = vnoise(ctx.pw, ctx.ph, 2, ctx.rng)
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                k = 0.62 + v[y][x] * 0.7
                n = ctx.rng.uniform(-9, 9)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


def track_rails(m, z0, z1):
    steel = metal("#8f959c")
    dark = metal("#5a5f66")
    for s in (-1, 1):
        x = s * GAUGE
        m.box((x - 1.2, 2.4, z0), (x + 1.2, 2.8, z1), dark, skip=())
        m.box((x - 0.4, 2.8, z0), (x + 0.4, 3.2, z1), dark, skip=())
        m.box((x - 0.85, 3.2, z0), (x + 0.85, RAIL_TOP, z1), steel, skip=())


def ties(m, z0, z1, step=3.0):
    z = z0 + 1.5
    i = 0
    while z + 0.75 <= z1:
        tone = ("#6b4a2a", "#5e4126", "#745230")[i % 3]
        m.box((-7.2, 1.4, z - 0.75), (7.2, 2.4, z + 0.75), planks(tone, 1.5, True, 0.72, 0.06), skip=())
        for s in (-1, 1):
            m.box((s * GAUGE - 1.5, 2.4, z - 0.6), (s * GAUGE + 1.5, 2.55, z + 0.6), metal("#40454d"), skip=())
        z += step
        i += 1


def track_straight():
    m = Model("track_straight", 710)
    m.box((-8.5, 0, -24), (8.5, 1.0, 24), {"all": gravel("#7c8086")}, skip=("down",))
    m.box((-7.2, 1.0, -24), (7.2, 1.7, 24), {"all": gravel("#90949a")}, skip=())
    ties(m, -24, 24)
    track_rails(m, -24, 24)
    return m


def track_end():
    m = Model("track_end", 711)
    m.box((-8.5, 0, -24), (8.5, 1.0, 21), {"all": gravel("#7c8086")}, skip=("down",))
    m.box((-7.2, 1.0, -24), (7.2, 1.7, 20), {"all": gravel("#90949a")}, skip=())
    ties(m, -24, 20)
    track_rails(m, -24, 15)
    stripes = P(paint("#d6332a", noise=3), ov_stripe("#f4f0e6", 0.17, 1.4, True), ov_stripe("#f4f0e6", 0.5, 1.4, True), ov_stripe("#f4f0e6", 0.83, 1.4, True))
    m.box((-7.8, 4.4, 15.6), (7.8, 7.4, 17.0), stripes, skip=())
    for s in (-1, 1):
        post(m, s * 7.0, 16.3, 1.8, 10.5, 1.6, planks("#5e4126", 1.4, True))
        m.box((s * GAUGE - 1.0, 3.6, 12.4), (s * GAUGE + 1.0, 5.6, 15.6), metal("#2a2d33"), skip=())
        cyl_z(m, s * GAUGE, 4.6, 11.6, 1.5, 1.6, {"all": metal("#c9962f")})
    m.box((-7.8, 9.4, 15.4), (7.8, 10.8, 17.2), planks("#5e4126", 1.4), skip=())
    m.box((-1.2, 10.8, 15.8), (1.2, 12.6, 16.8), light("#ff3b30"), skip=())
    return m


def station_shelter():
    m = Model("station_shelter", 712)
    wood = planks("#7a5230", 1.6)
    woodl = planks("#a9794a", 1.6)
    roof = shingle("#5a4a3a")
    m.box((-7, 0, -20), (7, 1.2, 20), planks("#b8a98a", 2.0, False, 0.8, 0.05))
    m.box((6.4, 0, -20.4), (7.4, 1.6, 20.4), paint("#e8b81a", noise=3), skip=())
    for z in (-18, -6, 6, 18):
        for x in (-5.6, 5.6):
            post(m, x, z, 1.2, 15, 1.4, wood)
    m.box((-7, 14.6, -20.4), (7, 15.8, 20.4), wood)
    for s in (-1, 1):
        m.box((s * 3.8 - 3.9, 15.4, -21), (s * 3.8 + 3.9, 16.3, 21), roof, rot=("z", 22.5 * s, (s * 3.8, 15.8, 0)), skip=())
    m.box((-0.8, 17.0, -21), (0.8, 17.8, 21), paint("#40454d"), skip=())
    sign = P(paint("#2f5a42", noise=3), ov_text("HARVEST", "#f2c94c", 8), ov_frame("#e9dfc4", 0.5))
    m.box((-6, 8.4, 0.0), (-5.0, 12.6, 9.6), {"east": sign, "west": sign, "all": paint("#2f5a42")}, skip=())
    for z in (-13.0, 10.0):
        m.box((-6.8, 1.2, z - 3), (-4.4, 2.8, z + 3), woodl, skip=())
        m.box((-6.8, 2.8, z - 3), (-6.2, 6.4, z + 3), woodl, skip=())
        for dz in (-3, 3):
            m.box((-6.8, 1.2, z + dz - 0.3), (-4.4, 2.2, z + dz + 0.3), wood, skip=())
    cyl_x(m, 0.0, 12.4, -19.6, 1.6, 0.6, {"all": paint("#f4f0e6")})
    m.box((-0.2, 11.2, -19.9), (0.2, 12.4, -19.3), paint("#2a2d33"), skip=())
    m.box((-2.8, 1.2, 14.4), (2.8, 2.4, 18.4), planks("#8a6038", 1.2), skip=())
    for i in range(3):
        m.box((-2.4 + i * 1.7, 2.4, 14.8 + (i % 2) * 0.8), (-0.9 + i * 1.7, 4.4, 17.6), planks("#c9a96a", 1.2), skip=())
    m.box((3.0, 1.2, -17.8), (5.0, 3.2, -15.6), paint("#6b4423"), skip=())
    cyl_y(m, 4.0, 3.2, -16.7, 1.0, 0.6, {"all": paint("#3f8f3a", noise=8)})
    for z in (-12, -2, 8):
        m.box((5.2, 12.0, z - 0.6), (6.4, 13.8, z + 0.6), light("#ffd36a"), skip=())
        m.box((5.4, 13.8, z - 0.3), (6.2, 14.6, z + 0.3), metal("#2a2d33"), skip=())
    return m


def station_signal():
    m = Model("station_signal", 713)
    iron = metal("#2a2d33")
    m.box((-2.2, 0, -2.2), (2.2, 1.6, 2.2), paint("#8c8f94", noise=4))
    m.box((-0.7, 1.6, -0.7), (0.7, 20.0, 0.7), iron, skip=())
    for y in range(3, 16, 2):
        m.box((-1.4, y, -0.2), (1.4, y + 0.35, 0.2), iron, skip=())
    m.box((-1.8, 17.0, -1.6), (1.8, 21.4, 1.6), P(paint("#1d1f23", noise=3), ov_frame("#55585e", 0.4)), skip=())
    m.box((-1.0, 19.2, -1.9), (1.0, 20.8, -1.6), light("#e8453c"), skip=())
    m.box((-1.0, 17.4, -1.9), (1.0, 19.0, -1.6), light("#4cd964"), skip=())
    m.box((-0.8, 21.4, -0.8), (0.8, 22.4, 0.8), iron, skip=())
    m.box((0.6, 15.2, -1.4), (1.6, 17.0, -0.2), metal("#55585e"), skip=())
    return m


def part_signal_arm():
    m = Model("part_signal_arm", 714)
    stripes = P(paint("#d6332a", noise=3), ov_stripe("#f4f0e6", 0.3, 1.2, True), ov_stripe("#f4f0e6", 0.7, 1.2, True))
    m.box((0.0, 7.3, -0.3), (8.4, 8.9, 0.3), {"north": stripes, "south": stripes, "all": paint("#d6332a")}, skip=())
    m.box((-0.8, 7.4, -0.6), (0.8, 8.8, 0.6), metal("#c9962f"), skip=())
    m.box((6.8, 7.5, -0.5), (8.4, 8.7, 0.5), paint("#f4f0e6"), skip=())
    return m


def train_tender():
    m = Model("train_tender", 715)
    green = planks("#2f5a42", 2.4, True, 0.74, 0.05)
    dark = metal("#202226")
    steel = metal("#55585e")
    side = P(green, ov_stripe("#d6a238", 0.45, 0.5, False), ov_text("HMC 07", "#d6a238", 8))
    m.box((-5.0, 4.4, -17), (5.0, 7.0, 17), dark)
    m.box((-6.2, 7.0, -17.4), (6.2, 8.2, 17.4), planks("#4a3320", 3))
    m.box((-6.2, 8.2, -17), (6.2, 15.4, 17), {"east": side, "west": side, "all": green})
    m.box((-6.5, 14.6, -17.3), (6.5, 15.6, 17.3), paint("#c9962f", noise=3), skip=())
    rng = random.Random(33)
    m.box((-5.2, 15.4, -15), (5.2, 17.0, 11), paint("#1b1b1f", noise=8), skip=())
    for i in range(14):
        x = rng.uniform(-4.4, 4.4)
        z = rng.uniform(-14, 10)
        h = rng.uniform(0.6, 1.6)
        m.box((x - 0.9, 17.0, z - 0.9), (x + 0.9, 17.0 + h, z + 0.9), paint("#26262b", noise=10), skip=())
    cyl_y(m, 0, 15.4, 14.0, 2.4, 1.2, {"all": metal("#c9962f")})
    cyl_y(m, 0, 16.6, 14.0, 1.8, 0.5, {"all": metal("#e0b13a")})
    for zz, s in ((-17.2, -1), (17.2, 1)):
        m.box((-5.4, 5.6, zz + (0 if s > 0 else -2.4)), (5.4, 7.0, zz + (2.4 if s > 0 else 0)), dark, skip=())
        for x in (-4.6, 4.6):
            m.box((x - 0.9, 8.0, zz + (0.3 if s > 0 else -1.5)), (x + 0.9, 10.4, zz + (1.5 if s > 0 else -0.3)), steel, skip=())
            cyl_z(m, x, 9.2, zz + (2.0 if s > 0 else -2.0), 1.2, 1.0, {"all": metal("#c9962f")})
        m.box((-0.8, 5.8, zz + (0 if s > 0 else -2.6)), (0.8, 7.2, zz + (2.6 if s > 0 else 0)), steel, skip=())
    for s in (-1, 1):
        m.box((s * 6.2 - 0.3, 15.4, 4.5), (s * 6.2 + 0.3, 19.4, 5.1), steel, skip=())
    for bz in (-8.5, 8.5):
        m.box((-5.4, 2.6, bz - 3.0), (5.4, 3.6, bz + 3.0), dark)
        for s in (-1, 1):
            for dz in (-2.0, 2.0):
                wheel(m, s * GAUGE, 2.8, bz + dz, 2.8, 1.1, "#25272b", "#b8bcc2", "#8d9096", lug=False)
    return m


def train_loco2():
    m = Model("train_locomotive", 71)
    green = P(paint("#1f4a36", noise=4), ov_stripe("#d6a238", 0.5, 0.35, True))
    black = P(metal("#26282c"), ov_dots("#3c3f44", 6, 2))
    dark = metal("#202226")
    steel = metal("#55585e")
    brass = metal("#c9962f")
    copper = metal("#b8643a")
    wood = planks("#4a3320", 1.6)
    for z in (-8.5, -1.0, 6.5):
        for s in (-1, 1):
            wheel(m, s * GAUGE, 5.6, z, 5.6, 1.4, "#25272b", "#a8342b", "#b8bcc2", lug=False)
    for z in (-17.0, 14.5):
        for s in (-1, 1):
            wheel(m, s * GAUGE, 3.0, z, 3.0, 1.2, "#25272b", "#b8bcc2", "#8d9096", lug=False)
    m.box((-4.3, 4.0, -21), (4.3, 8.6, 19), dark)
    for s in (-1, 1):
        m.p("rods_l" if s < 0 else "rods_r")
        m.box((s * 6.5 - 0.3, 5.3, -8.5), (s * 6.5 + 0.3, 5.9, 6.5), steel, skip=())
        m.p("main_rod_l" if s < 0 else "main_rod_r")
        m.box((s * 6.6 - 0.3, 6.6, -15.2), (s * 6.6 + 0.3, 7.2, -8.5), steel, skip=())
        m.p("body")
        m.box((s * 7.2 - 1.3, 6.8, -18.2), (s * 7.2 + 1.3, 10.6, -11.4), black)
        m.box((s * 7.2 - 1.4, 7.4, -19.0), (s * 7.2 + 1.4, 10.0, -18.2), brass, skip=())
        m.p("main_rod_l" if s < 0 else "main_rod_r")
        m.box((s * 7.6 - 0.35, 7.8, -11.4), (s * 7.6 + 0.35, 8.4, -8.4), steel, skip=())
        m.p("body")
        m.box((s * 7.0 - 0.3, 11.4, -19.4), (s * 7.0 + 0.3, 12.0, 5.4), steel, skip=())
        m.box((s * 6.0 - 1.2, 11.4, -17), (s * 6.0 + 1.2, 12.0, 6.2), wood, skip=())
        for z in (-16.0, -9.0, -2.0, 4.0):
            m.box((s * 6.4 - 0.3, 12.0, z - 0.3), (s * 6.4 + 0.3, 14.4, z + 0.3), steel, skip=())
        m.box((s * 6.4 - 0.2, 14.0, -16.0), (s * 6.4 + 0.2, 14.5, 4.3), steel, skip=())
        m.box((s * 5.4 - 0.35, 13.4, -17.0), (s * 5.4 + 0.35, 13.9, 1.0), copper, skip=())
    cyl_z(m, 0, 16.4, -9.0, 5.0, 25.0, {"all": green})
    for z in (-15.5, -7.0, 0.5):
        cyl_z(m, 0, 16.4, z, 5.2, 0.9, {"all": brass})
    door = P(paint("#1d1f23"), ov_draw(lambda d, c, i: (d.ellipse([c.pw * 0.12, c.ph * 0.12, c.pw * 0.88, c.ph * 0.88], outline=(150, 154, 160, 255), width=2), d.ellipse([c.pw * 0.44, c.ph * 0.44, c.pw * 0.56, c.ph * 0.56], fill=(201, 150, 47, 255)))))
    cyl_z(m, 0, 16.4, -20.4, 5.2, 4.0, {"all": black, "north": door})
    m.box((-1.4, 21.0, -22.0), (1.4, 24.0, -19.4), P(brass, ov_frame("#8a6c1f", 0.4)), skip=())
    m.box((-1.0, 21.4, -22.4), (1.0, 23.6, -22.0), light("#fff3b0"), skip=())
    m.box((-2.0, 23.8, -22.6), (2.0, 24.6, -19.0), black, skip=())
    cyl_y(m, 0, 20.6, -17.6, 1.7, 4.0, {"all": black})
    cyl_y(m, 0, 24.4, -17.6, 2.4, 1.6, {"all": black})
    cyl_y(m, 0, 25.8, -17.6, 2.9, 0.9, {"all": dark})
    cyl_y(m, 0, 21.0, -9.0, 2.5, 3.4, {"all": brass})
    cyl_y(m, 0, 24.2, -9.0, 2.8, 0.7, {"all": brass})
    cyl_y(m, 0, 21.0, -2.0, 2.1, 2.6, {"all": green})
    cyl_y(m, 0, 23.4, -2.0, 2.4, 0.6, {"all": brass})
    cyl_y(m, 0, 21.0, 3.0, 0.9, 3.4, {"all": brass})
    m.box((-0.5, 24.4, 2.5), (0.5, 25.0, 3.5), brass, skip=())
    m.box((-0.8, 21.0, -13.0), (0.8, 23.4, -11.4), brass, skip=())
    m.box((-1.4, 23.0, -13.4), (1.4, 24.2, -11.0), brass, skip=())
    m.box((-0.2, 20.8, -14.0), (0.2, 23.6, -10.4), steel, skip=())
    m.box((-6.4, 11.4, 5.2), (6.4, 12.4, 22.6), wood, skip=())
    pr = P(paint("#1f4a36", noise=4), ov_stripe("#d6a238", 0.5, 0.35, False))
    side = P(pr, ov_text("HM 07", "#f2d27a", 6))
    for s in (-1, 1):
        face = "e" if s > 0 else "w"
        m.box((s * 6.1 - 0.4, 12.4, 5.4), (s * 6.1 + 0.4, 17.6, 22.0), {"east": side, "west": side, "all": pr}, skip=())
        for z0, z1 in ((5.4, 6.9), (13.0, 14.0), (20.5, 22.0)):
            m.box((s * 6.1 - 0.45, 17.6, z0), (s * 6.1 + 0.45, 26.4, z1), green, skip=())
        slab(m, face, 6.9, 13.0, 18.2, 25.0, 6.5 * s, 0.3, glass("#9fc4de", 150), skip=())
        slab(m, face, 14.0, 20.5, 18.2, 25.0, 6.5 * s, 0.3, glass("#9fc4de", 150), skip=())
        slab(m, face, 6.9, 20.5, 25.0, 26.4, 6.5 * s, 0.5, paint("#1f4a36"), skip=())
    m.box((-6.0, 12.4, 5.2), (6.0, 26.4, 6.2), paint("#1d1f23", noise=3), skip=())
    glow = P(paint("#241a12", noise=3), ov_draw(lambda d, c, i: (d.ellipse([c.pw * 0.25, c.ph * 0.35, c.pw * 0.75, c.ph * 0.95], fill=(255, 130, 40, 255)), d.ellipse([c.pw * 0.38, c.ph * 0.55, c.pw * 0.62, c.ph * 0.9], fill=(255, 220, 120, 255)))))
    m.box((-2.8, 14.4, 6.2), (2.8, 20.0, 7.0), glow, skip=())
    for x in (-3.4, 3.4):
        cyl_z(m, x, 22.4, 6.9, 0.9, 0.7, {"all": P(paint("#f4f0e6"), ov_frame("#c9962f", 0.3))})
    for x in (-1.6, 1.0):
        m.box((x, 12.4, 7.4), (x + 0.5, 17.2, 7.9), steel, skip=())
    m.box((3.0, 12.4, 12.0), (5.0, 14.4, 14.0), planks("#6b4a2a", 1.0), skip=())
    dr = shingle("#2a2d33")
    for s in (-1, 1):
        m.box((s * 3.6 - 4.2, 26.6, 4.6), (s * 3.6 + 4.2, 27.4, 22.8), dr, rot=("z", 22.5 * s, (s * 3.6, 27.0, 0)), skip=())
    m.box((-1.2, 27.6, 4.6), (1.2, 28.2, 22.8), metal("#40454d"), skip=())
    m.box((-1.6, 28.0, 10), (1.6, 29.4, 14), metal("#7b8188"), skip=())
    m.box((-7.6, 8.6, -22.8), (7.6, 11.0, -21.4), P(paint("#a8342b", noise=3), ov_dots("#f4f0e6", 6, 1)), skip=())
    for s in (-1, 1):
        cyl_z(m, s * 4.0, 9.8, -23.0, 1.5, 1.6, {"all": metal("#c9ccd1")})
        m.box((s * 6.6 - 0.5, 10.4, -22.0), (s * 6.6 + 0.5, 11.6, -21.4), light("#ffb347"), skip=())
    m.box((-5.4, 1.6, -24.0), (5.4, 2.4, -22.4), metal("#3a3d42"), rot=("x", -22.5, (0, 2.0, -22.4)), skip=())
    for i in range(7):
        m.box((-5.2 + i * 1.74, 1.8, -23.6), (-4.6 + i * 1.74, 7.8, -22.6), metal("#3a3d42"), skip=())
    m.box((-0.8, 5.6, 19.0), (0.8, 7.0, 23.4), steel, skip=())
    cab_down = 3.0
    for e in m.els:
        cz = (e["from"][2] + e["to"][2]) / 2 - 8
        if cz > 4.8 and e["from"][1] >= 11.3:
            e["from"][1] = round(e["from"][1] - cab_down, 3)
            e["to"][1] = round(e["to"][1] - cab_down, 3)
            if "rotation" in e:
                e["rotation"]["origin"][1] = round(e["rotation"]["origin"][1] - cab_down, 3)
    for s in (-1, 1):
        m.box((s * 6.6 - 0.6, 8.6, 4.6), (s * 6.6 + 0.6, 9.6, 5.8), metal("#55585e"), skip=())
        m.box((s * 6.6 - 1.2, 6.6, 3.8), (s * 6.6 + 1.2, 7.4, 6.2), planks("#4a3320", 1.4), skip=())
    return m


def all_trainx():
    return [train_coach(), part_coach_door(), train_loco2(), train_tender(), track_straight(), track_end(), station_shelter(), station_signal(), part_signal_arm()]
