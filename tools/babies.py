from lib import *
from animals import eyes, nostrils, blush, DPINK


def chick():
    m = Model("livestock_chicken_baby", 951)
    down = fur("#f7de52", "#eab93a", 3, 0.66, 5)
    pale = fur("#fbeaa0", None, 3, 0.7, 4)
    orange = paint("#f08a2c", noise=3)
    m.box((-2.7, 3.4, -2.8), (2.7, 8.0, 3.2), down)
    m.box((-2.1, 3.2, -2.2), (2.1, 3.8, 2.6), pale, skip=())
    m.p("head")
    head_e = P(down, eyes([2.6], 2.6, 1.3, white="#ffffff", iris="#14110f"))
    head_w = P(down, eyes([0.4], 2.6, 1.3, white="#ffffff", iris="#14110f"))
    m.box((-2.5, 7.4, -5.0), (2.5, 12.2, -0.2), {"east": head_e, "west": head_w, "all": down}, skip=())
    m.box((-0.8, 9.2, -6.4), (0.8, 10.4, -5.0), orange, skip=())
    m.box((-0.6, 8.4, -5.6), (0.6, 9.2, -5.0), paint("#e8453c"), skip=())
    for i, dx in enumerate((-0.9, 0.0, 0.9)):
        m.box((dx - 0.3, 12.2, -3.4 + i * 0.4), (dx + 0.3, 13.2 - (i % 2) * 0.4, -2.6 + i * 0.4), pale, skip=())
    for s in (-1, 1):
        m.p("wing_l" if s < 0 else "wing_r")
        m.box((s * 3.0 - 0.4, 4.0, -1.4), (s * 3.0 + 0.4, 7.2, 2.4), paint("#eab93a", noise=5), skip=())
    for s in (-1, 1):
        m.p("leg_l" if s < 0 else "leg_r")
        m.box((s * 1.1 - 0.3, 0.6, -0.3), (s * 1.1 + 0.3, 3.4, 0.3), orange, skip=())
        for dx in (-0.5, 0.0, 0.5):
            m.box((s * 1.1 + dx - 0.2, 0.0, -1.4), (s * 1.1 + dx + 0.2, 0.6, 0.3), orange, skip=())
    m.p("tail")
    m.box((-0.9, 5.4, 3.2), (0.9, 7.6, 4.4), down, skip=())
    m.p("body")
    return m


def calf():
    m = Model("livestock_cow_baby", 952)
    brown = fur("#b9824f", "#f2e8d8", 6, 0.63, 4)
    brown2 = fur("#a8743f", "#f2e8d8", 5, 0.7, 4)
    cream = paint("#f2e8d8", noise=4)
    pink = paint("#f2a7b2", noise=4)
    dark = paint("#3a2a1c", noise=3)
    m.box((-3.6, 5.6, -5.0), (3.6, 12.0, 6.0), brown)
    m.box((-3.0, 5.2, -4.0), (3.0, 6.0, 5.0), cream, skip=())
    m.p("head")
    face_n = P(brown2, ov_rect("#f2e8d8", 2.2, 0.0, 1.6, 5.0), eyes([0.5, 4.5], 2.2, 1.5, iris="#2a1d14"))
    m.box((-3.0, 9.0, -11.0), (3.0, 14.8, -5.4), {"north": face_n, "all": brown2}, skip=())
    m.box((-2.2, 9.2, -12.6), (2.2, 11.8, -11.0), P(pink, nostrils([0.6, 2.8], 0.9, 0.9, 0.9, "#7a3a47")), skip=())
    for s in (-1, 1):
        m.box((s * 2.2 - 0.5, 14.8, -8.6), (s * 2.2 + 0.5, 15.8, -7.6), cream, skip=())
        m.box((s * 3.0, 12.6, -9.4), (s * 6.0, 14.0, -7.2), {"up": P(dark, ov_rect(DPINK, 0.4, 0.3, 2.0, 0.6, 130)), "all": dark}, rot=("z", 22.5 * s, (s * 3.0, 13.2, -8.3)), skip=())
    for sx in (-1, 1):
        for z in (-3.4, 4.6):
            m.p(f"leg_{'f' if z < 0 else 'b'}{'l' if sx < 0 else 'r'}")
            m.box((sx * 2.4 - 1.1, 1.4, z - 1.1), (sx * 2.4 + 1.1, 5.8, z + 1.1), brown, skip=())
            m.box((sx * 2.4 - 1.15, 0.0, z - 1.15), (sx * 2.4 + 1.15, 1.6, z + 1.15), dark, skip=())
    m.p("tail")
    m.box((-0.4, 6.0, 6.0), (0.4, 11.4, 6.8), brown, skip=())
    m.box((-0.8, 4.4, 5.8), (0.8, 6.6, 7.4), dark, skip=())
    m.p("body")
    return m


def piglet():
    m = Model("livestock_pig_baby", 953)
    skin = fur("#f8bcc8", "#f0a3b2", 4, 0.68, 4)
    stripe = P(skin, ov_stripe("#e89aab", 0.25, 0.5, False), ov_stripe("#e89aab", 0.55, 0.5, False), ov_stripe("#e89aab", 0.8, 0.5, False))
    pink = paint("#fbd0d8", noise=3)
    m.box((-3.0, 3.6, -4.4), (3.0, 9.2, 4.8), stripe)
    m.p("head")
    face_n = P(skin, eyes([0.4, 4.2], 1.6, 1.3, iris="#241616"), blush([0.2, 4.6], 3.0, 1.2, 1.0))
    m.box((-2.8, 5.4, -9.0), (2.8, 10.6, -4.4), {"north": face_n, "all": skin}, skip=())
    m.box((-1.8, 5.8, -10.6), (1.8, 8.6, -9.0), P(pink, nostrils([0.5, 2.2], 0.8, 0.8, 0.8, "#7a3a47")), skip=())
    for s in (-1, 1):
        m.box((s * 2.6 - 0.3, 10.6, -7.8), (s * 2.6 + 1.9, 12.6, -5.8), P(pink, ov_rect(DPINK, 0.3, 0.4, 1.2, 1.2, 140)), rot=("z", 22.5 * s, (s * 2.6, 10.6, -6.8)), skip=())
    for sx in (-1, 1):
        for z in (-3.0, 3.4):
            m.p(f"leg_{'f' if z < 0 else 'b'}{'l' if sx < 0 else 'r'}")
            m.box((sx * 2.2 - 1.1, 0.8, z - 1.1), (sx * 2.2 + 1.1, 3.8, z + 1.1), skin, skip=())
            m.box((sx * 2.2 - 1.15, 0.0, z - 1.15), (sx * 2.2 + 1.15, 0.9, z + 1.15), paint("#8a5a64", noise=2), skip=())
    m.p("tail")
    for k in range(3):
        m.box((-0.3, 6.6 + k * 0.8, 4.8 + (k % 2) * 0.7), (0.3, 7.4 + k * 0.8, 5.6 + (k % 2) * 0.7), skin, skip=())
    m.p("body")
    return m


def lamb():
    m = Model("livestock_sheep_baby", 954)
    wl = curly("#f8f0e0", "#d8cdb5", 2.4)
    wl2 = curly("#f3ead8", "#d0c4aa", 2.0)
    face = fur("#e9d3b8", None, 4, 0.7, 4)
    leg = paint("#cdb497", noise=3)
    m.box((-3.2, 5.4, -4.4), (3.2, 10.6, 5.0), paint("#e9d8c0", noise=4))
    m.box((-3.9, 5.8, -4.6), (3.9, 10.6, 5.2), wl, skip=())
    m.box((-3.2, 5.2, -5.2), (3.2, 10.8, 5.8), wl2, skip=())
    m.p("head")
    face_n = P(face, eyes([0.4, 3.4], 2.5, 1.4, white="#ffffff", iris="#14110f"), nostrils([1.8, 2.7], 4.0, 0.5, 0.6, "#a8826a"))
    m.box((-2.4, 8.2, -9.4), (2.4, 13.2, -4.8), {"north": face_n, "all": face}, skip=())
    m.box((-1.6, 8.0, -10.4), (1.6, 10.6, -9.4), paint("#f0a3b0", noise=3), skip=())
    m.box((-2.6, 13.0, -8.6), (2.6, 14.6, -5.6), wl, skip=())
    for s in (-1, 1):
        m.box((s * 2.4, 11.0, -8.2), (s * 5.2, 12.2, -6.4), {"up": P(paint("#f0a3b0"), ov_rect("#d98494", 0.6, 0.3, 1.8, 0.5, 140)), "all": paint("#f0a3b0")}, rot=("z", 22.5 * s, (s * 2.4, 11.6, -7.3)), skip=())
    for sx in (-1, 1):
        for z in (-3.0, 3.8):
            m.p(f"leg_{'f' if z < 0 else 'b'}{'l' if sx < 0 else 'r'}")
            m.box((sx * 2.4 - 1.0, 1.4, z - 1.0), (sx * 2.4 + 1.0, 5.6, z + 1.0), leg, skip=())
            m.box((sx * 2.4 - 1.05, 0.0, z - 1.05), (sx * 2.4 + 1.05, 1.5, z + 1.05), paint("#3a3028"), skip=())
    m.p("tail")
    m.box((-1.0, 6.2, 5.8), (1.0, 9.6, 7.4), wl, skip=())
    m.p("body")
    return m


def all_babies():
    return [chick(), calf(), piglet(), lamb()]
