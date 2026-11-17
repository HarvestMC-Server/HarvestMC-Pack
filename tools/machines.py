import math
from lib import *
from bld import slab, post
from attach2 import hitch, hose, hydraulic

STEEL = "#6d7076"
YELLOW = "#f2b134"


def farm_buggy():
    m = Model("machine_buggy", 801)
    red = paint("#c4372b", noise=4)
    redf = P(red, ov_shadow(0.25))
    dark = metal("#26282c")
    steel = metal(STEEL)
    seatm = cloth("#1b1b1b")
    for s in (-1, 1):
        wheel(m, s * 7.2, 4.1, -8.6, 4.1, 4.4, "#26272b", "#d8d8dc", "#8d9096")
        wheel(m, s * 7.2, 4.1, 8.4, 4.1, 4.6, "#26272b", "#d8d8dc", "#8d9096")
    m.box((-3.6, 5.0, -13.0), (3.6, 7.2, 12.0), dark)
    for s in (-1, 1):
        m.box((s * 5.0 - 0.5, 5.6, -9.0), (s * 5.0 + 0.5, 7.0, 9.0), steel, skip=())
        m.box((s * 7.2 - 0.4, 5.6, -8.6), (s * 7.2 + 0.4, 6.4, 8.4), steel, skip=())
        m.box((s * 8.6 - 0.9, 6.4, -4.0), (s * 8.6 + 0.9, 7.0, 4.0), diamond(), skip=())
        m.box((s * 8.0 - 1.4, 9.0, -11.4), (s * 8.0 + 1.4, 10.0, -5.6), redf)
        m.box((s * 8.0 - 1.4, 9.0, 5.4), (s * 8.0 + 1.4, 10.0, 11.6), redf)
        m.box((s * 4.6 - 0.9, 10.2, -14.0), (s * 4.6 + 0.9, 12.0, -13.0), light("#fff0b0"))
    m.box((-5.8, 7.2, -14.4), (5.8, 11.4, -5.0), P(redf, ov_stripe("#f2f2f2", 0.5, 1.0, True)))
    m.box((-4.6, 8.4, -15.0), (4.6, 10.4, -14.2), grille("#c9ced6", "#1b1b1b", 3), skip=())
    m.box((-5.8, 5.6, -15.8), (5.8, 7.0, -14.2), steel, skip=())
    m.box((-3.4, 11.4, -7.0), (3.4, 14.0, -1.0), P(redf, ov_text("HMC", "#f4f0e6", 6)))
    m.box((-1.0, 14.0, -5.2), (1.0, 14.6, -3.4), metal("#e8b81a"), skip=())
    m.box((-3.0, 8.0, 1.0), (3.0, 10.2, 8.0), seatm)
    m.box((-3.0, 10.2, 7.0), (3.0, 13.6, 8.2), seatm)
    m.box((-5.0, 9.4, 8.4), (5.0, 10.2, 15.0), P(dark, ov_dots("#55585e", 4, 1)))
    for x in (-4.4, 4.4):
        m.box((x - 0.35, 10.2, 8.8), (x + 0.35, 12.4, 9.4), steel, skip=())
        m.box((x - 0.35, 10.2, 14.4), (x + 0.35, 12.4, 15.0), steel, skip=())
    m.box((-4.4, 12.0, 8.6), (4.4, 12.5, 9.2), steel, skip=())
    m.box((-4.4, 12.0, 14.2), (4.4, 12.5, 14.8), steel, skip=())
    m.box((-4.0, 8.0, -13.4), (4.0, 8.8, -8.0), diamond())
    cyl_z(m, 5.2, 8.0, 14.8, 1.0, 5.0, {"all": metal("#9aa0a6")})
    m.box((-1.0, 6.0, 12.0), (1.0, 7.4, 17.0), steel, skip=())
    cyl_y(m, 0, 7.4, 16.6, 0.9, 1.4, {"all": metal("#c9ced6")})
    m.p("steer")
    m.box((-0.5, 11.4, -4.2), (0.5, 14.0, -3.4), steel, skip=())
    m.box((-5.0, 13.6, -4.4), (5.0, 14.4, -3.4), dark, skip=())
    for s in (-1, 1):
        m.box((s * 5.0 - 0.5, 13.2, -4.6), (s * 5.0 + 1.2, 14.8, -3.2), metal("#c9962f"), skip=())
        m.box((s * 3.6 - 0.8, 14.4, -4.0), (s * 3.6 + 0.8, 15.2, -3.4), light("#fff0b0"), skip=())
    m.p("body")
    return m


def combine():
    m = Model("machine_combine", 802)
    green = paint("#3f8f3a", noise=4)
    greenf = P(green, ov_shadow(0.2))
    yellow = paint(YELLOW, noise=4)
    dark = metal("#26282c")
    steel = metal(STEEL)
    for s in (-1, 1):
        wheel(m, s * 11.0, 8.0, -2.0, 8.0, 6.6, "#26272b", YELLOW, "#8d9096")
        wheel(m, s * 8.8, 5.2, 16.0, 5.2, 4.2, "#26272b", YELLOW, "#8d9096")
        m.box((s * 8.8 - 0.5, 4.0, 14.5), (s * 8.8 + 0.5, 12.0, 17.5), steel, skip=())
    m.box((-5.4, 6.0, -10.0), (5.4, 14.0, 19.0), dark)
    m.box((-9.0, 12.0, -12.0), (9.0, 20.0, 14.0), P(greenf, ov_dots("#2a6a26", 6, 1)))
    m.box((-9.4, 19.4, -12.4), (9.4, 20.4, 14.4), yellow, skip=())
    for s in (-1, 1):
        m.box((s * 9.0 - 0.4, 12.0, -12.0), (s * 9.0 + 0.4, 20.0, 14.0), P(greenf, ov_stripe(YELLOW, 0.5, 0.6, False)), skip=())
        m.box((s * 9.2 - 0.4, 9.0, -6.0), (s * 9.2 + 0.4, 12.0, 4.0), greenf, skip=())
    m.box((-7.0, 20.4, -12.0), (7.0, 29.2, -2.0), P(green, ov_frame("#2a6a26", 0.6)))
    for s in (-1, 1):
        slab(m, "e" if s > 0 else "w", -9.4, -2.6, 22.0, 28.0, 7.0 * s, 0.4, glass("#a8dcf0", 100), skip=())
    slab(m, "n", -6.2, 6.2, 22.0, 28.4, -12.0, 0.4, glass("#a8dcf0", 100), skip=())
    slab(m, "s", -6.2, 6.2, 22.0, 28.4, -2.0, 0.4, glass("#a8dcf0", 100), skip=())
    m.box((-7.8, 29.2, -13.0), (7.8, 30.4, -1.0), P(paint("#e8e8ea", noise=3), ov_vents("#7b8188", 3, 2.0)), skip=())
    for x in (-5.0, -1.7, 1.7, 5.0):
        m.box((x - 0.6, 30.4, -12.4), (x + 0.6, 31.4, -11.4), light("#fff3c4"), skip=())
    m.box((-2.4, 22.0, -5.0), (2.4, 25.4, -3.6), seat_c(), skip=())
    m.box((-2.4, 23.0, -4.0), (2.4, 28.0, -2.8), seat_c(), skip=())
    m.box((-8.0, 20.4, 0.0), (8.0, 27.0, 14.0), P(paint("#5a6b4a", noise=3), ov_frame("#2a6a26", 0.8)))
    m.box((-8.4, 26.6, -0.4), (8.4, 28.0, 14.4), yellow, rot=("x", 0), skip=())
    m.box((-6.0, 27.0, 2.0), (6.0, 28.4, 12.0), paint("#d6b04a", noise=8), skip=())
    cyl_z(m, 10.4, 28.6, 3.0, 1.6, 16.0, {"all": metal("#a8aeb4")})
    m.box((9.4, 24.0, -1.0), (11.4, 29.4, 1.0), steel, skip=())
    m.box((-7.0, 14.0, 14.0), (7.0, 22.0, 22.0), P(greenf, ov_vents("#1f4a18", 4, 1.2)))
    cyl_y(m, 5.6, 22.0, 18.0, 1.2, 8.0, {"all": metal("#40454d")})
    m.box((4.4, 30.0, 17.0), (6.8, 30.8, 19.0), steel, skip=())
    m.box((-9.4, 6.0, 12.0), (9.4, 7.4, 23.0), dark, skip=())
    m.box((-7.0, 8.0, -14.0), (7.0, 15.0, -11.0), P(greenf, ov_frame("#2a6a26", 0.6)))
    m.box((-14.0, 3.6, -23.8), (14.0, 6.0, -21.0), P(paint("#3f8f3a", noise=4), ov_stripe(YELLOW, 0.5, 0.5, False)))
    m.box((-14.0, 6.0, -23.0), (14.0, 11.6, -21.6), P(green, ov_dots("#2a6a26", 6, 1)))
    for s in (-1, 1):
        m.box((s * 14.0 - 0.7, 3.6, -23.8), (s * 14.0 + 0.7, 14.0, -13.0), greenf, skip=())
        m.box((s * 14.0 - 0.5, 13.6, -23.9), (s * 14.0 + 0.5, 14.8, -13.0), yellow, skip=())
    m.box((-14.0, 6.0, -21.6), (14.0, 8.6, -13.4), metal("#9aa0a6"))
    for i in range(-13, 14):
        x = i * 1.0
        m.box((x - 0.3, 2.6, -23.9), (x + 0.3, 3.8, -23.0), metal("#d7dbe0"), skip=())
    m.p("reel")
    cyl_x(m, 0, 13.0, -19.2, 0.8, 27, metal("#55585e"))
    for i in range(-6, 7):
        oct_prism(m, "x", i * 2.1, 13.0, -19.2, 3.9, 0.55, metal("#7b8188"))
    for a in range(6):
        rad = math.radians(a * 60)
        yy = 13.0 + math.sin(rad) * 3.7
        zz = -19.2 + math.cos(rad) * 3.7
        m.box((-13.0, yy - 0.45, zz - 0.45), (13.0, yy + 0.45, zz + 0.45), metal("#cfd3d8"), skip=())
    m.p("body")
    hydraulic(m, -5.0, 8.0, -14.0, 14.0, -19.2)
    hydraulic(m, 5.0, 8.0, -14.0, 14.0, -19.2)
    return m


def seat_c():
    return cloth("#1c1c1c")


def farm_truck():
    m = Model("machine_truck", 803)
    blue = paint("#2f5fa8", noise=4)
    bluef = P(blue, ov_shadow(0.22))
    white = paint("#e9eef2", noise=3)
    dark = metal("#26282c")
    steel = metal(STEEL)
    for s in (-1, 1):
        wheel(m, s * 7.8, 4.6, -11.4, 4.6, 3.4, "#26272b", "#d8d8dc", "#8d9096", lug=False)
        wheel(m, s * 7.8, 4.6, 11.0, 4.6, 3.4, "#26272b", "#d8d8dc", "#8d9096", lug=False)
    m.box((-4.6, 5.4, -18.0), (4.6, 8.0, 19.0), dark)
    for s in (-1, 1):
        m.box((s * 6.2 - 0.6, 6.4, -18.0), (s * 6.2 + 0.6, 8.0, 19.0), steel, skip=())
        m.box((s * 7.8 - 0.3, 6.6, -11.4), (s * 7.8 + 0.3, 7.4, -11.0), steel, skip=()) if False else None
    m.box((-7.8, 8.0, -17.4), (7.8, 14.4, -8.2), P(bluef, ov_vents("#1d3a66", 3, 1.0)))
    m.box((-6.6, 8.6, -18.0), (6.6, 12.4, -17.4), grille("#c9ced6", "#1b1b1b", 4), skip=())
    m.box((-7.8, 5.8, -19.2), (7.8, 8.0, -17.4), P(metal("#c9ced6"), ov_stripe("#2a2d33", 0.5, 0.4, False)), skip=())
    for s in (-1, 1):
        m.box((s * 6.0 - 1.4, 10.0, -18.2), (s * 6.0 + 1.4, 12.0, -17.4), light("#fff0b0"), skip=())
        m.box((s * 8.4 - 0.4, 14.0, -9.0), (s * 8.4 + 0.4, 17.6, -7.6), paint("#1b1d20"), skip=())
    m.box((-7.8, 8.0, -8.2), (7.8, 20.0, 2.0), P(bluef, ov_frame("#1d3a66", 0.6)))
    m.box((-7.2, 19.6, -9.0), (7.2, 21.0, 3.0), white)
    for s in (-1, 1):
        slab(m, "e" if s > 0 else "w", -6.6, 0.8, 14.0, 19.2, 7.8 * s, 0.4, glass("#a8dcf0", 100), skip=())
        m.box((s * 7.8 - 0.2, 8.0, -7.4), (s * 7.8 + 0.2, 13.6, 1.4), P(blue, ov_frame("#1d3a66", 0.5)), skip=()) if False else None
        m.box((s * 8.0 - 0.3, 11.0, -5.0), (s * 8.0 + 0.3, 11.8, -3.6), metal("#c9962f"), skip=())
    slab(m, "n", -6.6, 6.6, 14.0, 19.4, -8.2, 0.4, glass("#a8dcf0", 100), skip=())
    slab(m, "s", -6.6, 6.6, 14.0, 19.4, 2.0, 0.4, glass("#a8dcf0", 100), skip=())
    m.box((-2.4, 9.0, -3.0), (2.4, 12.0, -0.6), seat_c(), skip=())
    m.box((-2.4, 12.0, -0.8), (2.4, 17.0, 0.4), seat_c(), skip=())
    m.box((-7.8, 8.0, 2.0), (7.8, 9.0, 19.0), planks("#4a3320", 3))
    m.box((-7.8, 9.0, 2.0), (-6.8, 14.0, 19.0), P(bluef, ov_stripe(YELLOW, 0.5, 0.5, False)))
    m.box((6.8, 9.0, 2.0), (7.8, 14.0, 19.0), P(bluef, ov_stripe(YELLOW, 0.5, 0.5, False)))
    m.box((-7.8, 9.0, 18.0), (7.8, 14.0, 19.0), P(bluef, ov_text("HMC", "#f4f0e6", 8)))
    m.box((-7.8, 9.0, 2.0), (7.8, 13.0, 3.0), bluef)
    for s in (-1, 1):
        m.box((s * 6.6 - 1.4, 9.0, 8.4), (s * 6.6 + 1.4, 11.6, 13.0), dark, skip=())
    for i in range(3):
        m.box((-5.4 + i * 3.8, 9.0, 4.0), (-2.2 + i * 3.8, 12.6, 8.4), P(straw("#dcc05a"), ov_stripe("#6b4a2a", 0.3, 0.4, True), ov_stripe("#6b4a2a", 0.7, 0.4, True)), skip=())
    m.box((-5.4, 9.0, 14.0), (-0.8, 13.4, 17.6), planks("#a9794a", 1.4), skip=())
    m.box((1.0, 9.0, 14.4), (5.4, 12.0, 17.8), planks("#a9794a", 1.4), skip=())
    m.box((-7.8, 5.8, 19.0), (7.8, 8.0, 20.4), metal("#c9ced6"), skip=())
    for s in (-1, 1):
        m.box((s * 6.0 - 1.0, 8.4, 19.0), (s * 6.0 + 1.0, 9.6, 19.6), light("#ff3b30"), skip=())
    cyl_y(m, 8.4, 8.0, -3.4, 1.0, 14.0, {"all": metal("#40454d")})
    cyl_y(m, 8.4, 22.0, -3.4, 1.4, 1.2, {"all": metal("#40454d")})
    m.box((-1.0, 6.0, 20.0), (1.0, 7.4, 24.0), steel, skip=())
    m.p("steer")
    m.box((-1.8, 12.6, -5.4), (1.8, 13.2, -4.2), dark, skip=())
    m.p("body")
    return m


def attach_plow():
    m = Model("attachment_plow", 811)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    blue = paint("#2f5fa8", noise=4)
    hitch(m, 7.0, 4.0, -13.0, -2.0, "#4a4d52")
    m.box((-2.0, 8.0, -4.0), (2.0, 13.0, 0.0), steel)
    m.box((-1.2, 13.0, -3.2), (1.2, 16.0, -0.8), dark)
    m.box((-10.0, 9.0, -1.4), (10.0, 11.4, 1.4), P(blue, ov_text("PLOW-3", "#f4e3c1", 6)), rot=("y", 22.5))
    m.box((-1.2, 8.2, -2.0), (1.2, 11.6, 2.0), steel)
    for i in range(3):
        x = -8.0 + i * 8.0
        z = -7.0 + i * 6.0
        m.box((x - 0.8, 3.0, z - 0.6), (x + 0.8, 9.2, z + 0.6), dark, skip=())
        m.box((x - 1.6, 0.8, z - 2.0), (x + 4.4, 5.0, z + 2.6), P(metal("#cfd3d8"), ov_stripe("#8f959c", 0.5, 0.4, False)), rot=("y", 22.5), skip=())
        m.box((x - 0.6, 0.0, z - 3.8), (x + 0.6, 1.8, z - 0.6), metal("#e8eaed"), skip=())
        m.box((x - 0.4, 9.0, z - 1.0), (x + 0.4, 12.0, z - 0.4), steel, skip=())
    cyl_y(m, -4.0, 5.0, -10.0, 3.0, 0.8, {"all": metal("#9aa0a6")})
    m.box((-4.4, 3.0, -10.4), (-3.6, 9.0, -9.6), steel, skip=())
    for s in (1,):
        wheel(m, 12.0, 3.2, 4.0, 3.2, 1.8, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
        m.box((11.6, 3.2, 3.0), (12.4, 10.0, 5.0), steel, skip=())
    m.box((-9.0, 10.8, 3.4), (12.0, 11.8, 4.6), steel, skip=())
    hydraulic(m, 0.0, 9.0, -3.0, 15.0, -7.0)
    return m


def attach_mower():
    m = Model("attachment_mower", 812)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    orange = paint("#d4631b", noise=4)
    hitch(m, 8.0, 5.0, -13.0, -2.0, "#4a4d52")
    m.box((-14.0, 4.0, -4.0), (14.0, 8.0, 5.0), P(orange, ov_text("MOW", "#f4e3c1", 6)))
    m.box((-14.4, 7.6, -4.4), (14.4, 8.6, 5.4), P(orange, ov_stripe("#2a2d33", 0.5, 0.4, False)), skip=())
    m.box((-14.0, 2.4, 5.0), (14.0, 4.2, 6.4), P(dark, ov_vents("#55585e", 2, 0.5)), skip=())
    for s in (-1, 1):
        m.box((s * 14.0 - 0.5, 2.6, -4.0), (s * 14.0 + 0.5, 8.0, 5.0), steel, skip=())
        m.box((s * 12.0 - 1.4, 0.6, -4.2), (s * 12.0 + 1.4, 2.6, 5.4), steel, skip=())
    for i, x in enumerate((-9.0, 0.0, 9.0)):
        m.p(f"disc_{i + 1}")
        oct_prism(m, "y", x, 1.0, 0.5, 4.2, 1.2, metal("#cfd3d8"))
        m.box((x - 4.4, 1.0, -0.2), (x + 4.4, 1.5, 1.0), metal("#e8eaed"), skip=())
        m.box((x - 0.6, 1.5, -0.1), (x + 0.6, 2.6, 1.1), steel, skip=())
        m.p("body")
    for x in (-9.0, 0.0, 9.0):
        cyl_y(m, x, 8.6, 0.5, 1.0, 1.4, {"all": metal("#9aa0a6")})
    m.box((-6.0, 8.6, -3.8), (6.0, 11.0, -1.0), dark)
    m.box((-14.0, 2.2, -4.6), (14.0, 3.4, -4.0), hazard(YELLOW, "#1e1e1e", 2), skip=())
    for i in range(7):
        m.box((-13.0 + i * 4.2, 2.4, 6.4), (-12.0 + i * 4.2, 4.0, 7.0), steel, skip=())
    for s in (-1, 1):
        wheel(m, s * 15.0, 2.6, 0.6, 2.6, 1.4, "#2a2b2f", "#cccccc", "#8d9096", lug=False)
        m.box((s * 14.4 - 0.4, 2.6, -0.4), (s * 14.4 + 0.4, 8.0, 1.6), steel, skip=())
    hydraulic(m, -6.0, 8.0, -3.0, 14.0, -9.0)
    return m


def attach_spreader():
    m = Model("attachment_spreader", 813)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    green = paint("#4a9a3a", noise=4)
    hitch(m, 5.0, 3.0, -9.0, -1.0, "#4a4d52")
    m.box((-7.0, 8.0, -4.0), (7.0, 14.0, 6.0), P(green, ov_stripe(YELLOW, 0.5, 0.6, False)))
    m.box((-9.0, 13.0, -6.0), (9.0, 14.4, 8.0), P(green, ov_frame("#2d6a22", 0.6)), skip=())
    m.box((-8.4, 14.4, -5.4), (8.4, 19.6, 7.4), P(paint("#e3d9b8", noise=4), ov_text("FERT", "#2d6a22", 6)))
    m.box((-8.8, 19.6, -5.8), (8.8, 20.8, 7.8), green, skip=())
    m.box((-6.0, 20.8, -4.0), (6.0, 21.4, 6.0), P(dark, ov_dots("#55585e", 4, 1)), skip=())
    m.box((-1.4, 8.0, 6.0), (1.4, 12.0, 9.0), steel, skip=())
    for i, s in enumerate((-1, 1)):
        m.p(f"spinner_{'l' if s < 0 else 'r'}")
        oct_prism(m, "y", s * 5.0, 7.4, 10.0, 3.8, 0.8, metal("#cfd3d8"))
        for k in range(4):
            a = k * 90
            r = 3.4
            m.box((s * 5.0 - 0.4, 7.4, 10.0 - r), (s * 5.0 + 0.4, 8.4, 10.0 + r), metal("#e8eaed"), rot=("y", 0) if k % 2 == 0 else None, skip=())
        m.p("body")
        m.box((s * 5.0 - 0.5, 7.4, 8.8), (s * 5.0 + 0.5, 9.0, 10.2), steel, skip=()) if False else None
        wheel(m, s * 9.4, 3.6, 2.0, 3.6, 2.0, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
        m.box((s * 8.6 - 0.4, 3.6, 1.0), (s * 8.6 + 0.4, 10.0, 3.0), steel, skip=())
    m.box((-6.0, 3.0, -2.0), (6.0, 4.6, 0.0), steel, skip=())
    m.box((-2.0, 6.0, 7.0), (2.0, 8.0, 10.0), dark)
    hose(m, [(0, 9.0, -1.0), (0, 9.0, 6.0)], t=0.4)
    return m


def attach_baler():
    m = Model("attachment_baler", 814)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    red = paint("#b8312a", noise=4)
    redf = P(red, ov_shadow(0.2))
    hitch(m, 6.0, 4.0, -15.0, -4.0, "#4a4d52")
    m.box((-9.0, 6.0, -8.0), (9.0, 8.4, 14.0), dark)
    for s in (-1, 1):
        m.box((s * 9.0 - 0.7, 8.0, -8.0), (s * 9.0 + 0.7, 22.0, 14.0), P(redf, ov_stripe("#f4f0e6", 0.5, 0.6, False)))
    cyl_x(m, 0, 15.0, 3.0, 8.0, 17.0, {"all": P(straw("#dcc05a"), ov_stripe("#7a5a1a", 0.5, 0.5, True)), "east": straw("#c9a940"), "west": straw("#c9a940")})
    cyl_x(m, 0, 15.0, 3.0, 8.4, 19.0, {"all": red}) if False else None
    for s in (-1, 1):
        cyl_x(m, s * 9.4, 15.0, 3.0, 1.4, 1.0, {"all": metal("#c9962f")})
    m.box((-9.0, 22.0, -8.0), (9.0, 23.4, 14.0), redf, skip=())
    m.box((-9.4, 23.0, 8.0), (9.4, 31.0, 14.4), P(redf, ov_frame("#7c1f1b", 0.7)), rot=("x", -22.5, (0, 23.0, 12.0)))
    m.box((-5.0, 8.0, 14.0), (5.0, 21.0, 15.0), P(redf, ov_text("BALE", "#f4e3c1", 6)))
    m.box((-6.0, 22.2, -2.0), (6.0, 24.0, 6.0), yellow_box(), skip=())
    m.p("pickup")
    cyl_x(m, 0, 4.0, -11.0, 1.0, 17, metal("#55585e"))
    for i in range(-5, 6):
        oct_prism(m, "x", i * 1.5, 4.0, -11.0, 2.6, 0.5, metal("#7b8188"))
    for a in range(4):
        rad = math.radians(a * 90)
        yy = 4.0 + math.sin(rad) * 2.8
        zz = -11.0 + math.cos(rad) * 2.8
        for i in range(-5, 6, 2):
            m.box((i * 1.5 - 0.2, yy - 1.4, zz - 0.2), (i * 1.5 + 0.2, yy + 1.4, zz + 0.2), metal("#e8eaed"), skip=())
    m.p("body")
    m.box((-8.0, 1.6, -13.6), (8.0, 2.4, -12.0), steel, skip=()) if False else None
    for s in (-1, 1):
        wheel(m, s * 11.8, 4.0, 5.0, 4.0, 2.4, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
        m.box((s * 10.6 - 0.5, 4.0, 4.0), (s * 10.6 + 0.5, 10.0, 6.0), steel, skip=())
    hydraulic(m, -6.0, 10.0, -6.0, 18.0, -12.0)
    hydraulic(m, 6.0, 10.0, -6.0, 18.0, -12.0)
    return m


def yellow_box():
    return metal(YELLOW)


def attach_trailer():
    m = Model("attachment_trailer", 815)
    steel = metal(STEEL)
    dark = metal("#2a2d33")
    green = paint("#3f8f3a", noise=4)
    greenf = P(green, ov_shadow(0.2))
    hitch(m, 4.0, 3.0, -17.0, -8.0, "#4a4d52")
    m.box((-1.0, 4.0, -17.0), (1.0, 5.4, -8.0), steel, skip=())
    m.box((-8.0, 5.0, -10.0), (8.0, 7.0, 18.0), dark)
    m.box((-9.0, 7.0, -10.4), (9.0, 8.2, 18.4), planks("#4a3320", 3))
    for s in (-1, 1):
        m.box((s * 9.0 - 0.5, 8.0, -10.4), (s * 9.0 + 0.5, 17.0, 18.4), P(greenf, ov_stripe(YELLOW, 0.8, 0.6, False)))
        m.box((s * 9.4 - 0.4, 7.0, -10.6), (s * 9.4 + 0.4, 18.0, -10.0), steel, skip=())
        m.box((s * 9.4 - 0.4, 7.0, 18.0), (s * 9.4 + 0.4, 18.0, 18.6), steel, skip=())
    m.box((-9.0, 8.0, -10.4), (9.0, 17.0, -9.4), greenf)
    m.box((-9.0, 8.0, 17.4), (9.0, 17.0, 18.4), P(greenf, ov_text("HMC", "#f4e3c1", 8)))
    rng = __import__("random").Random(5)
    m.box((-8.0, 8.2, -9.0), (8.0, 11.6, 17.0), P(paint("#d8b84a", noise=10), ov_dots("#a98a20", 3, 1)), skip=())
    for i in range(10):
        x = rng.uniform(-7, 7)
        z = rng.uniform(-8, 16)
        m.box((x - 1.2, 11.6, z - 1.2), (x + 1.2, 11.6 + rng.uniform(0.6, 1.8), z + 1.2), paint("#e0c04e", noise=10), skip=())
    for bz in (2.0, 12.0):
        for s in (-1, 1):
            wheel(m, s * 10.8, 4.6, bz, 4.6, 3.2, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
            m.box((s * 9.4 - 0.5, 4.6, bz - 1.0), (s * 9.4 + 0.5, 6.0, bz + 1.0), steel, skip=())
    m.box((-8.0, 4.4, 10.0), (8.0, 5.4, 12.0), dark, skip=()) if False else None
    for s in (-1, 1):
        m.box((s * 8.0 - 1.0, 8.4, 18.4), (s * 8.0 + 1.0, 9.6, 19.0), light("#ff3b30"), skip=())
    return m


def all_machines():
    return [farm_buggy(), combine(), farm_truck(), attach_plow(), attach_mower(), attach_spreader(), attach_baler(), attach_trailer()]
