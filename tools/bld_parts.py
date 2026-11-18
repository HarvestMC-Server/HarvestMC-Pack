import math
import random
from lib import *
from bld import *
from cosmetics import bricks


def part_door_house():
    m = Model("part_door_house", 610)
    w = planks("#7a5230", 1.6, True, 0.7, 0.06)
    m.box((-3.5, 0, -0.5), (3.5, 11, 0.5), {"north": P(w, ov_frame("#4a3220", 0.5), ov_rect("#4a3220", 1.2, 1.2, 4.6, 0.4), ov_rect("#4a3220", 1.2, 12.0, 4.6, 0.4)), "south": P(w, ov_frame("#4a3220", 0.5)), "all": w}, skip=())
    m.box((-1.9, 6.2, -0.7), (1.9, 9.4, -0.4), glass("#9fc4de", 215), skip=())
    m.box((2.2, 5.0, -0.9), (3.0, 5.8, -0.4), metal("#c9962f"), skip=())
    return m


def part_door_barn():
    m = Model("part_door_barn", 611)
    red = planks("#a63a2c", 1.8, True, 0.72, 0.05)

    def xbrace(d, c, i):
        for a in ((0, 0, c.pw, c.ph), (c.pw, 0, 0, c.ph)):
            d.line(a, fill=(242, 238, 226, 255), width=2)
        d.rectangle([0, 0, c.pw - 1, c.ph - 1], outline=(242, 238, 226, 255), width=2)

    face = P(red, ov_draw(xbrace))
    m.box((-3.6, 0, -0.6), (3.6, 14, 0.6), {"north": face, "south": face, "all": red}, skip=())
    m.box((1.8, 6.0, -1.0), (2.8, 8.4, -0.6), metal("#40454d"), skip=())
    return m


def part_hatch():
    m = Model("part_hatch", 612)
    w = planks("#8a6038", 1.2, True, 0.7, 0.06)
    m.box((-3, 0, -0.4), (3, 5, 0.4), {"north": P(w, ov_frame("#f2eee2", 0.5)), "all": w}, skip=())
    m.box((-0.5, 3.6, -0.7), (0.5, 4.4, -0.4), metal("#c9962f"), skip=())
    return m


def part_door_garage():
    m = Model("part_door_garage", 613)
    slat = planks("#c9ccd1", 2.8, False, 0.7, 0.03)
    face = P(slat, ov_rect("#2a2d33", 2.0, 9.0, 20.0, 0.4), ov_rect("#9fc4de", 3.0, 3.0, 4.2, 2.6, 170), ov_rect("#9fc4de", 9.8, 3.0, 4.2, 2.6, 170), ov_rect("#9fc4de", 16.6, 3.0, 4.2, 2.6, 170), ov_rect("#2a2d33", 0, 27.2, 24.0, 0.8))
    m.box((-12, 0, -0.5), (12, 14, 0.5), {"north": face, "south": slat, "all": slat}, skip=())
    m.box((-0.8, 3.0, -0.9), (0.8, 4.0, -0.5), metal("#40454d"), skip=())
    m.box((-12, 0, -0.9), (12, 0.8, -0.5), metal("#40454d"), skip=())
    return m


def part_vent():
    m = Model("part_vent", 614)
    wh = paint(TRIM, noise=3)
    m.box((-6, 0, -0.3), (6, 6, 0.3), {"north": P(glass("#b6dcf0", 110), ov_vents("#f2eee2", 5, 0.8)), "south": glass("#b6dcf0", 110), "all": wh}, skip=())
    m.box((-6.2, 0, -0.5), (6.2, 0.6, 0.5), wh, skip=())
    m.box((-6.2, 5.4, -0.5), (6.2, 6.0, 0.5), wh, skip=())
    m.box((-6.2, 0, -0.5), (-5.6, 6, 0.5), wh, skip=())
    m.box((5.6, 0, -0.5), (6.2, 6, 0.5), wh, skip=())
    return m


def part_valve():
    m = Model("part_valve", 615)
    red = paint("#c0392b", noise=4)
    cyl_z(m, 0, 8, 0, 2.7, 0.7, {"all": red})
    cyl_z(m, 0, 8, 0, 1.6, 0.9, {"all": metal("#9aa0a6")})
    m.box((-2.9, 7.7, -0.3), (2.9, 8.3, 0.3), red, skip=())
    m.box((-0.3, 5.1, -0.3), (0.3, 10.9, 0.3), red, skip=())
    m.box((-0.6, 7.4, -0.9), (0.6, 8.6, 0.0), metal("#55585e"), skip=())
    return m


def part_gauge():
    m = Model("part_gauge", 616)
    m.box((-1.0, 0, -0.4), (1.0, 1.4, 0.4), P(paint("#d6332a", noise=4), ov_stripe("#f4f0e6", 0.5, 0.5, False)), skip=())
    m.box((1.0, 0.3, -0.3), (1.9, 1.1, 0.3), paint("#d6332a"), skip=())
    return m


def part_weathervane():
    m = Model("part_weathervane", 617)
    iron = metal("#2a2d33")
    gold = metal("#c9962f")
    m.box((-0.3, 0, -0.3), (0.3, 4.2, 0.3), iron, skip=())
    m.box((-2.4, 2.4, -0.2), (2.4, 2.8, 0.2), iron, skip=())
    m.box((-0.2, 2.4, -2.4), (0.2, 2.8, 2.4), iron, skip=())
    for (x, z) in ((2.6, 0), (-2.6, 0), (0, 2.6), (0, -2.6)):
        m.box((x - 0.3, 2.3, z - 0.3), (x + 0.3, 3.0, z + 0.3), gold, skip=())
    m.box((-0.2, 4.4, -4.6), (0.2, 4.9, 4.2), iron, skip=())
    m.box((-0.8, 4.4, -5.6), (0.8, 4.9, -4.2), iron, rot=("y", 45), skip=())
    m.box((-0.15, 3.8, 3.4), (0.15, 7.0, 5.4), iron, skip=())
    m.box((-0.5, 4.9, -1.2), (0.5, 7.0, 1.4), gold, skip=())
    m.box((-0.4, 7.0, -1.8), (0.4, 8.6, -0.6), gold, skip=())
    m.box((-0.2, 8.6, -2.2), (0.2, 9.4, -1.4), paint("#d6332a"), skip=())
    m.box((-0.2, 7.0, -2.4), (0.2, 7.6, -1.8), paint("#f0b82a"), skip=())
    m.box((-0.2, 7.0, 1.4), (0.2, 8.8, 2.8), gold, rot=("x", 22.5, (0, 7.0, 1.4)), skip=())
    return m


def site(name, W, D, H, seed):
    m = Model(name, seed)
    wood = planks("#a9794a", 1.4)
    wood2 = planks("#8a6038", 1.4, True)
    conc = paint("#9a9ea4", noise=6)
    m.box((-W / 2, 0, -D / 2), (W / 2, 1.0, D / 2), conc)
    m.box((-W / 2 + 1, 1.0, -D / 2 + 1), (W / 2 - 1, 1.4, D / 2 - 1), paint("#7a7e84", noise=6), skip=())
    for sx in (-1, 1):
        for sz in (-1, 1):
            post(m, sx * (W / 2 - 1.5), sz * (D / 2 - 1.5), 1.0, H, 1.2, wood2)
    for y in (H * 0.45, H - 0.8):
        for s in (-1, 1):
            m.box((-W / 2 + 1, y, s * (D / 2 - 1.5) - 0.5), (W / 2 - 1, y + 0.8, s * (D / 2 - 1.5) + 0.5), wood, skip=())
            m.box((s * (W / 2 - 1.5) - 0.5, y, -D / 2 + 1), (s * (W / 2 - 1.5) + 0.5, y + 0.8, D / 2 - 1), wood, skip=())
    span = W - 3.0
    hgt = H * 0.45 - 1.0
    for s in (-1, 1):
        m.box((-span / 2, 1.2, s * (D / 2 - 1.5) - 0.3), (span / 2, 1.2 + hgt * 1.3, s * (D / 2 - 1.5) + 0.3), wood, rot=("z", 45, (0, 1.2 + hgt * 0.65, s * (D / 2 - 1.5))), skip=()) if False else None
    for s in (-1, 1):
        for sgn in (-1, 1):
            zc = s * (D / 2 - 1.5)
            x0 = sgn * (W / 4)
            m.box((x0 - 0.35, 1.4, zc - 0.35), (x0 + 0.35, 1.4 + (W / 2 - 3) * 1.1, zc + 0.35), wood, rot=("z", 45 * sgn, (x0, 1.4 + (W / 2 - 3) * 0.55, zc)), skip=())
    pl = planks("#b8905a", 1.8)
    for k in range(3):
        m.box((-W / 2 + 3, H * 0.45 + 0.8, -D / 2 + 3 + k * (D - 6) / 3), (W / 2 - 3, H * 0.45 + 1.4, -D / 2 + 3 + (k + 0.9) * (D - 6) / 3), pl, skip=())
    hz = hazard("#e8b81a", "#1e1e1e", 2)
    m.box((-W / 2 + 1, 4.0, -D / 2 - 0.6), (W / 2 - 1, 6.4, -D / 2 - 0.1), hz, skip=())
    for x in (-W / 2 + 1, 0, W / 2 - 1):
        post(m, x, -D / 2 - 0.4, 1.0, 6.4, 0.7, wood2)
    sw = min(W - 6.0, 26.0) / 2.0
    wording = "UNDER\nCONSTRUCTION" if W >= 30 else "BUILD SITE"
    sh = 7.5 if W >= 30 else 4.0
    m.box((-sw, 7.0, -D / 2 - 0.6), (sw, 7.0 + sh, -D / 2 - 0.1), P(paint("#e8b81a", noise=3), ov_frame("#1e1e1e", 0.4), ov_text(wording, "#1e1e1e", 7)), skip=())
    for i in range(3):
        m.box((W / 2 - 8 + (i % 2) * 0.6, 1.0 + i * 1.6, 3.0 + (i % 2) * 0.4), (W / 2 - 2, 2.4 + i * 1.6, 9.0), planks("#c9a96a", 1.2), skip=())
    m.box((-W / 2 + 2, 1.0, 2), (-W / 2 + 8, 4.2, 7.6), bricks("#a8503a", "#5a2a20", 1.2, 2.4), skip=())
    for i in range(3):
        m.box((-W / 2 + 2.4 + i * 1.6, 1.0, -8), (-W / 2 + 3.8 + i * 1.6, 3.0, -4.4), P(burlap("#d8d0bc"), ov_stripe("#9a9078", 0.5, 0.6, True)), skip=())
    wx, wz = 4, 6
    m.box((wx - 2.4, 2.6, wz - 3.0), (wx + 2.4, 4.4, wz + 2.0), metal("#c9962f"), skip=())
    cyl_x(m, wx, 2.0, wz - 3.4, 1.6, 0.9, {"all": paint("#1f1f20", noise=4)})
    m.box((wx - 2.2, 2.4, wz + 2.0), (wx - 1.8, 3.2, wz + 5.4), metal("#40454d"), skip=())
    m.box((wx + 1.8, 2.4, wz + 2.0), (wx + 2.2, 3.2, wz + 5.4), metal("#40454d"), skip=())
    post(m, 0, D / 2 - 3, 1.0, H - 0.8, 0.9, wood2) if False else None
    cyl_y(m, 3.0, H - 0.2, D / 2 - 1.5, 1.6, 0.6, {"all": paint("#f2c230", noise=3)})
    cyl_y(m, 3.0, H + 0.3, D / 2 - 1.5, 1.1, 0.9, {"all": paint("#f2c230", noise=3)})
    for s in range(4):
        m.box((-W / 2 + 3 + s * 0.0, H * 0.45 + 1.4, -D / 2 + 3 + 0.0), (-W / 2 + 3.5, H * 0.45 + 1.8 + s * 0.4, -D / 2 + 3.5), wood, skip=()) if False else None
    for y in range(2, int(H * 0.45), 2):
        m.box((W / 2 - 1.6, y, -3.0), (W / 2 - 1.0, y + 0.4, 3.0), wood, skip=())
    return m


def part_turbine():
    m = Model("part_turbine", 617)
    steel = metal("#b8bec4")
    red = paint("#c0392b", noise=4)
    dark = metal("#2a2d33")
    m.box((-0.35, 4.6, -0.35), (0.35, 7.2, 0.35), dark, skip=())
    cyl_y(m, 0, 6.8, 0, 1.2, 2.4, {"all": red})
    m.box((-3.8, 7.3, -0.45), (3.8, 8.7, 0.45), steel, rot=("x", 22.5), skip=())
    m.box((-0.45, 7.3, -3.8), (0.45, 8.7, 3.8), steel, rot=("z", 22.5), skip=())
    m.box((-3.0, 7.9, -0.4), (3.0, 8.5, 0.4), steel, rot=("y", 45), skip=())
    m.box((-3.0, 7.9, -0.4), (3.0, 8.5, 0.4), steel, rot=("y", -45), skip=())
    m.box((-1.1, 9.2, -1.1), (1.1, 9.8, 1.1), red, skip=())
    m.box((-0.3, 9.8, -0.3), (0.3, 11.2, 0.3), dark, skip=())
    return m


def all_parts():
    return [part_door_house(), part_door_barn(), part_hatch(), part_door_garage(), part_vent(), part_valve(), part_gauge(), part_turbine(), part_weathervane(),
            site("build_site_s", 24, 24, 14, 620), site("build_site_m", 36, 30, 16, 621), site("build_site_l", 44, 36, 20, 622)]
