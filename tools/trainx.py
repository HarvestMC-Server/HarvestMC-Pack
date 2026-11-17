from lib import *
from bld import siding, corrug, slab, post


def train_coach():
    m = Model("train_coach", 700)
    green = planks("#2f5a42", 2.4, True, 0.74, 0.05)
    greenb = paint("#2a4f3a", noise=4)
    gold = "#d6a238"
    roof = P(metal("#b8bec4"), ov_vents("#7b8188", 3, 2.0))
    dark = metal("#202226")
    steel = metal("#55585e")
    trim = paint("#e9dfc4", noise=3)
    m.box((-6.6, 3.4, -21), (6.6, 5.2, 21), dark)
    m.box((-6.4, 5.2, -19.6), (6.4, 5.8, 19.6), planks("#4a3320", 3))
    body = {"east": P(green, ov_stripe(gold, 0.46, 0.5, False)), "west": P(green, ov_stripe(gold, 0.46, 0.5, False)), "all": green}
    m.box((-6.2, 5.8, -19.6), (6.2, 17.4, 19.6), body)
    m.box((-6.4, 5.8, -19.8), (6.4, 7.4, 19.8), P(greenb, ov_stripe("#d6a238", 0.9, 0.5, False)), skip=())
    zs_e = (-15.5, -10.0, 10.0, 15.5)
    zs_w = (-15.5, -10.0, 10.0, 15.5)
    warm = P(paint("#ffcf6a", noise=5), ov_stripe("#e9dfc4", 0.5, 0.5, True), ov_rect("#3a2a1c", 0.0, 3.6, 8.0, 0.8))
    for z in zs_e:
        slab(m, "e", z - 2.1, z + 2.1, 9.4, 14.6, 6.2, 0.3, warm, skip=())
        slab(m, "e", z - 2.7, z + 2.7, 14.6, 15.2, 6.2, 0.5, trim, skip=())
        slab(m, "e", z - 2.7, z + 2.7, 8.8, 9.4, 6.2, 0.5, trim, skip=())
    for z in zs_w:
        slab(m, "w", z - 2.1, z + 2.1, 9.4, 14.6, -6.2, 0.3, warm, skip=())
        slab(m, "w", z - 2.7, z + 2.7, 14.6, 15.2, -6.2, 0.5, trim, skip=())
        slab(m, "w", z - 2.7, z + 2.7, 8.8, 9.4, -6.2, 0.5, trim, skip=())
    slab(m, "e", -3.2, 3.2, 5.8, 17.0, 6.2, 0.3, paint("#241a12", noise=3), skip=())
    slab(m, "e", -3.9, -3.2, 5.8, 17.4, 6.2, 0.8, trim, skip=())
    slab(m, "e", 3.2, 3.9, 5.8, 17.4, 6.2, 0.8, trim, skip=())
    slab(m, "e", -3.9, 3.9, 17.0, 17.6, 6.2, 0.8, trim, skip=())
    slab(m, "w", -3.2, 3.2, 5.8, 17.0, -6.2, 0.3, paint("#241a12", noise=3), skip=())
    slab(m, "w", -3.9, -3.2, 5.8, 17.4, -6.2, 0.8, trim, skip=())
    slab(m, "w", 3.2, 3.9, 5.8, 17.4, -6.2, 0.8, trim, skip=())
    slab(m, "w", -3.9, 3.9, 17.0, 17.6, -6.2, 0.8, trim, skip=())
    m.box((-8.4, 3.8, -4.2), (-6.2, 4.6, 4.2), planks("#8a6a48", 1.4), skip=())
    m.box((-7.8, 3.0, -3.2), (-6.2, 3.8, 3.2), planks("#8a6a48", 1.4), skip=())
    m.box((6.2, 3.8, -4.2), (8.4, 4.6, 4.2), planks("#8a6a48", 1.4), skip=())
    m.box((6.2, 3.0, -3.2), (7.8, 3.8, 3.2), planks("#8a6a48", 1.4), skip=())
    for s, nm in ((1, "door_e"), (-1, "door_w")):
        m.p(nm)
        face = P(planks("#2f5a42", 2.4, True, 0.74, 0.05), ov_rect("#ffcf6a", 1.4, 1.6, 3.6, 4.0), ov_frame("#e9dfc4", 0.5))
        m.box((s * 6.75, 5.8, -3.1), (s * 7.35, 17.0, 3.1), {"east": face if s > 0 else paint("#2f5a42"), "west": face if s < 0 else paint("#2f5a42"), "all": paint("#2f5a42", noise=4)}, skip=())
        m.box((s * 7.35, 10.4, 1.6), (s * 7.85, 12.0, 2.2), metal("#c9962f"), skip=())
    m.p("body")
    m.box((-5.0, 17.4, -19.6), (5.0, 18.6, 19.6), roof, skip=())
    for s in (-1, 1):
        m.box((s * 5.5 - 1.6, 17.5, -19.6), (s * 5.5 + 1.6, 18.2, 19.6), roof, rot=("z", 22.5 * s, (s * 5.5, 17.8, 0)), skip=())
    for z in (-10, 0, 10):
        m.box((-1.6, 18.6, z - 1.2), (1.6, 19.6, z + 1.2), metal("#7b8188"), skip=())
    for z, s in ((-1, -1), (1, 1)):
        zz = z * 19.8
        m.box((-6.2, 5.8, zz if z > 0 else zz - 0.2), (6.2, 17.4, zz + 0.2 if z > 0 else zz), P(green, ov_text("HMC", gold, 9)), skip=())
        m.box((-5.4, 4.2, zz), (5.4, 5.2, zz + 2.2 * s), planks("#4a3320", 3), skip=())
        for x in (-5.0, 5.0):
            m.box((x - 0.3, 5.2, zz + (1.6 if s > 0 else -2.2)), (x + 0.3, 9.4, zz + (2.2 if s > 0 else -1.6)), steel, skip=())
        m.box((-5.2, 9.0, zz + (1.6 if s > 0 else -2.2)), (5.2, 9.5, zz + (2.2 if s > 0 else -1.6)), steel, skip=())
        m.box((-0.8, 5.0, zz + (0 if s > 0 else -1.8)), (0.8, 7.0, zz + (1.8 if s > 0 else 0)), steel, skip=())
        m.box((-2.6, 4.6, zz + (1.4 if s > 0 else -2.4)), (2.6, 6.6, zz + (2.4 if s > 0 else -1.4)), dark)
        m.box((-0.5, 13.6, zz + (0 if s > 0 else -0.5)), (0.5, 14.6, zz + (0.5 if s > 0 else 0)), light("#fff3b0"), skip=())
    for bz in (-12.5, 12.5):
        m.box((-5.4, 2.6, bz - 4.0), (5.4, 3.6, bz + 4.0), dark)
        for s in (-1, 1):
            m.box((s * 4.4 - 0.4, 2.6, bz - 3.8), (s * 4.4 + 0.4, 4.2, bz + 3.8), steel)
            for dz in (-2.6, 2.6):
                wheel(m, s * 5.4, 2.6, bz + dz, 2.6, 1.1, "#25272b", "#b8bcc2", "#8d9096", lug=False)
    return m


def part_coach_door():
    m = Model("part_coach_door", 701)
    green = planks("#2f5a42", 2.4, True, 0.74, 0.05)
    face = P(green, ov_rect("#ffcf6a", 1.4, 1.6, 3.6, 4.0), ov_frame("#e9dfc4", 0.5))
    m.box((-0.3, 0, -3.1), (0.3, 11.2, 3.1), {"east": face, "west": P(green, ov_frame("#e9dfc4", 0.5)), "all": green}, skip=())
    m.box((0.3, 4.6, 1.6), (0.8, 6.2, 2.2), metal("#c9962f"), skip=())
    return m


def all_trainx():
    return [train_coach(), part_coach_door()]
