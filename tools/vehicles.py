from lib import *

STEEL = "#6d7076"
DARK = "#2a2c30"
CHROME = "#c9ced6"
YELLOW = "#f2b134"


def tractor(name, k, body, trim, cab, dual, seed, label, body_c=None):
    m = Model(name, seed)
    m.k = k
    K = lambda v: v * k
    steel = metal(STEEL)
    dark = metal(DARK)
    bodyp = body if callable(body) else paint(body, noise=4)
    bc = body_c or body
    trimp = paint(trim, noise=4)
    rw, rf = K(8), K(5)
    rax, fax = K(7), K(-10)

    m.box((K(-4.5), K(4), K(-12)), (K(4.5), K(8), K(11)), dark)
    m.box((K(-4.5), K(8), K(1)), (K(4.5), K(11), K(11)), P(bodyp, ov_dots(tint(bc, 0.7), 5, 1)))
    m.box((K(-5), K(8), K(-13)), (K(5), K(14.5), K(-1)), {"east": P(bodyp, ov_shadow(0.25), ov_text(label, trim, 7)), "west": P(bodyp, ov_shadow(0.25), ov_text(label, trim, 7)), "all": bodyp})
    m.box((K(-4), K(14.5), K(-12.2)), (K(4), K(16.2), K(-2)), {"up": P(trimp, ov_vents("#1d1d1d", 5, 1.2)), "all": trimp})
    m.box((K(-4.2), K(8.8), K(-13.7)), (K(4.2), K(14), K(-13)), {"north": grille(CHROME, "#1b1b1b", 5), "all": steel}, skip=("down", "up"))
    for s in (-1, 1):
        m.box((K(s * 3.6 - 1.3), K(10.4), K(-14.3)), (K(s * 3.6 + 1.3), K(12.8), K(-13)), {"north": light("#fff0b0"), "all": paint(CHROME)})
        m.box((K(s * 4.3 - 0.6), K(7.2), K(-13.8)), (K(s * 4.3 + 0.6), K(8.2), K(-13)), light("#ffb347"))
    if cab:
        m.box((K(-6.5), K(5.5), K(-15.2)), (K(6.5), K(8.8), K(-13.7)), P(hazard(YELLOW, "#1e1e1e", 3), ov_shadow(0.2)))
    m.box((K(2.2), K(14.5), K(-8)), (K(3.4), K(24), K(-6.8)), dark, skip=())
    m.box((K(1.9), K(24), K(-8.3)), (K(3.7), K(24.7), K(-6.5)), steel, skip=())
    m.box((K(-3.5), K(14.5), K(-7.6)), (K(-2), K(18.5), K(-6.1)), metal(CHROME), skip=())
    for s in (-1, 1):
        m.box((K(s * 7.9 - 2.9), K(16.4), K(2)), (K(s * 7.9 + 2.9), K(17.5), K(12.2)), P(bodyp, ov_shadow(0.3)))
        m.box((K(s * 5.4 - 0.9), K(7), K(3)), (K(s * 5.4 + 0.9), K(7.8), K(8)), diamond())
        m.box((K(s * 8.6 - 0.5), K(17.5), K(11)), (K(s * 8.6 + 0.5), K(19.2), K(11.8)), light("#ff3b30"))
        wheel(m, K(s * 7.9), rw, rax, rw, K(5), "#2a2b2f", trim, "#8d9096")
        wheel(m, K(s * 6.5), rf, fax, rf, K(3.2), "#2a2b2f", trim, "#8d9096")
        m.box((K(s * 5.5 - 0.5), K(7), K(rax - 0.6)), (K(s * 7.4 + 0.5), K(9), K(rax + 0.6)), steel)
        m.box((K(s * 4.5 - 0.4), K(4.4), K(fax - 0.6)), (K(s * 6.5 + 0.4), K(5.8), K(fax + 0.6)), steel)
        if dual:
            wheel(m, K(s * 13.1), rw, rax, rw, K(4.4), "#2a2b2f", trim, "#8d9096")
            m.box((K(s * 7.4), K(7.4), K(rax - 0.8)), (K(s * 11), K(8.6), K(rax + 0.8)), steel)
    m.box((K(-1.6), K(5), K(11)), (K(1.6), K(7), K(18)), steel)
    m.box((K(-0.4), K(7), K(15)), (K(0.4), K(9), K(16)), steel)
    m.box((K(-1), K(8.4), K(11)), (K(1), K(10.4), K(13.6)), paint(YELLOW))
    seatm = cloth("#1c1c1c")
    m.box((K(-2.4), K(11.5), K(5.5)), (K(2.4), K(13.2), K(9)), seatm)
    m.box((K(-2.4), K(13.2), K(8.4)), (K(2.4), K(19), K(9.4)), seatm)
    m.p("steer")
    m.box((K(-0.5), K(11.5), K(2.6)), (K(0.5), K(15.6), K(3.4)), steel, rot=("x", 22.5))
    ring = metal("#1a1a1a")
    m.box((K(-2.2), K(15.3), K(1.6)), (K(2.2), K(15.9), K(2.2)), ring, skip=())
    m.box((K(-2.2), K(15.3), K(3.8)), (K(2.2), K(15.9), K(4.4)), ring, skip=())
    m.box((K(-2.2), K(15.3), K(2.2)), (K(-1.6), K(15.9), K(3.8)), ring, skip=())
    m.box((K(1.6), K(15.3), K(2.2)), (K(2.2), K(15.9), K(3.8)), ring, skip=())
    m.p("body")
    if cab:
        m.box((K(-4.6), K(10.5), K(1.4)), (K(4.6), K(11.5), K(10.4)), dark)
        for sx in (-1, 1):
            for z in (1.4, 9.4):
                m.box((K(sx * 4.4 - 0.5), K(11.5), K(z)), (K(sx * 4.4 + 0.5), K(28), K(z + 1)), bodyp, skip=())
            m.box((K(sx * 4.9 - 0.2), K(11.5), K(2.2)), (K(sx * 4.9 + 0.2), K(14.2), K(9.8)), P(bodyp, ov_frame(tint(bc, 0.6), 0.5)))
            m.box((K(sx * 4.7 - 0.2), K(14.2), K(2.4)), (K(sx * 4.7 + 0.2), K(27.8), K(9.6)), glass("#a8dcf0", 105))
            m.box((K(sx * 5.2 - 0.2), K(21.5), K(2.2)), (K(sx * 5.2 + 0.2), K(23), K(3.4)), metal("#222"))
            m.box((K(sx * 7.2 - 0.3), K(21.8), K(1.6)), (K(sx * 7.2 + 0.3), K(26), K(2.8)), paint("#1b1d20"))
            m.box((K(sx * 5.2), K(23), K(1.9)), (K(sx * 7.2), K(23.6), K(2.2)), steel)
        m.box((K(-4.2), K(14), K(1.5)), (K(4.2), K(27.8), K(1.9)), glass("#a8dcf0", 100))
        m.box((K(-4.2), K(14), K(9.9)), (K(4.2), K(27.8), K(10.3)), glass("#a8dcf0", 100))
        m.box((K(-6), K(28), K(0.2)), (K(6), K(29.4), K(11.6)), {"up": P(bodyp, ov_vents("#222", 3, 2.5)), "all": bodyp}, skip=())
        for x in (-4, -1.3, 1.3, 4):
            m.box((K(x - 0.6), K(29.4), K(0.6)), (K(x + 0.6), K(30.4), K(1.6)), light("#fff3c4"))
    else:
        for sx in (-1, 1):
            m.box((K(sx * 4 - 0.55), K(11), K(9)), (K(sx * 4 + 0.55), K(25), K(10.1)), trimp, skip=())
        m.box((K(-4.6), K(24), K(8.8)), (K(4.6), K(25.2), K(10.3)), trimp, skip=())
        m.box((K(-2), K(25.2), K(9.1)), (K(2), K(26), K(10)), light("#fff3c4"))
    return m


def attach_tiller():
    m = Model("attachment_tiller", 31)
    steel = metal(STEEL)
    dark = metal(DARK)
    orange = paint("#d4631b", noise=4)
    m.box((-12, 8, -2.5), (12, 10.5, 1.5), P(orange, ov_text("TILL", "#f4e3c1", 6)))
    m.box((-2.5, 10.5, -1.5), (2.5, 15, 0.5), dark)
    m.box((-1, 15, -0.5), (1, 17, 1), steel)
    for s in (-1, 1):
        m.box((s * 8.5 - 0.7, 8.5, -9), (s * 8.5 + 0.7, 10, -1.5), steel)
        m.box((s * 12 - 0.6, 3, -2.5), (s * 12 + 0.6, 10, 3.5), orange)
    m.p("rotor")
    cyl_x(m, 0, 4.5, 1, 1.1, 24, metal("#55585e"))
    for i in range(-5, 6):
        x = i * 2.1
        oct_prism(m, "x", x, 4.5, 1, 3.4, 0.5, metal("#7b7e84"))
        m.box((x - 0.35, 0.4, 0.4), (x + 0.35, 3.2, 1.6), steel, rot=("x", 22.5 if i % 2 else -22.5, (x, 4.5, 1)), skip=())
        m.box((x - 0.35, 4.5 + 2.2, -0.3), (x + 0.35, 4.5 + 4.6, 0.8), steel, rot=("x", -22.5 if i % 2 else 22.5, (x, 4.5, 1)), skip=())
    m.p("body")
    m.box((-12.6, 5.4, 3.4), (12.6, 11.2, 4.2), P(orange, ov_stripe("#2a2a2a", 0.5, 0.6, False)), rot=("x", -22.5, (0, 5.4, 3.4)))
    m.box((-12.5, 9.2, -2.6), (12.5, 9.6, 3.6), steel)
    m.box((-1.4, 2, 5), (1.4, 5, 8), diamond())
    m.box((-0.5, 0.5, 6), (0.5, 3, 7), steel)
    return m


def attach_seeder():
    m = Model("attachment_seeder", 41)
    steel = metal(STEEL)
    dark = metal(DARK)
    green = paint("#4a9a3a", noise=4)
    yellow = paint(YELLOW, noise=4)
    m.box((-12.5, 7.5, -1), (12.5, 9.5, 1), dark)
    m.box((-12, 8.4, -9), (-11, 9.4, -1), steel)
    m.box((11, 8.4, -9), (12, 9.4, -1), steel)
    m.box((-1, 9.5, -4), (1, 12.5, 0), steel)
    for i in range(4):
        x = -9 + i * 6
        m.box((x - 2.2, 9.5, -2.2), (x + 2.2, 12.5, 2.2), P(green, ov_frame("#2d6a22", 0.6)))
        m.box((x - 3, 12.5, -3), (x + 3, 17, 3), P(yellow, ov_dots("#a97a1a", 4, 1)))
        m.box((x - 3.3, 17, -3.3), (x + 3.3, 18, 3.3), paint("#7c5a14"), skip=())
        m.box((x - 1, 18, -1), (x + 1, 18.8, 1), steel)
        m.box((x - 0.5, 3, -0.5), (x + 0.5, 9.5, 0.5), paint("#3a3a3a"), skip=())
        m.box((x - 0.9, 1, -2), (x + 0.9, 3.5, 0.5), steel, rot=("x", 22.5, (x, 3, 0)))
        m.box((x - 0.4, 3, 0.8), (x + 0.4, 7.5, 1.3), paint("#2a2a2a"), skip=())
    for s in (-1, 1):
        wheel(m, s * 13.2, 3.2, 2.5, 3.2, 1.8, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
        m.box((s * 12.4 - 0.4, 3.2, 1.8), (s * 12.4 + 0.4, 9, 3.2), steel)
    m.box((-1.5, 6, 1), (1.5, 8, 7), steel)
    return m


def attach_harvester():
    m = Model("attachment_harvester", 51)
    steel = metal(STEEL)
    dark = metal(DARK)
    red = paint("#b8312a", noise=4)
    yellow = paint(YELLOW, noise=4)
    m.box((-13, 3, -12), (13, 5.2, -8), P(red, ov_text("HMC", "#f4e3c1", 9)))
    m.box((-13, 5.2, -12.4), (13, 12, -11.4), red)
    for s in (-1, 1):
        m.box((s * 13 - 0.6, 3, -12.4), (s * 13 + 0.6, 14, -2), P(red, ov_shadow(0.2)))
    m.box((-13, 12, -12.4), (13, 13.2, -11), yellow)
    m.box((-13, 5.2, -11.4), (13, 6.6, -2), metal("#9aa0a6"))
    for i in range(-12, 13, 2):
        m.box((i - 0.8, 1.4, -15), (i + 0.8, 3, -12), steel, rot=("x", 0))
        m.box((i - 0.35, 1.9, -17), (i + 0.35, 2.6, -15), metal("#d7dbe0"))
    m.p("reel")
    cyl_x(m, 0, 11.5, -14, 0.7, 26, metal("#55585e"))
    for i in range(-5, 6):
        x = i * 2.3
        oct_prism(m, "x", x, 11.5, -14, 3.6, 0.5, metal("#7b7e84"))
    for a in range(4):
        ang = a * 45 + 22.5
        rad = math.radians(ang)
        yy = 11.5 + math.sin(rad) * 3.4
        zz = -14 + math.cos(rad) * 3.4
        m.box((-12.5, yy - 0.4, zz - 0.4), (12.5, yy + 0.4, zz + 0.4), metal("#cfd3d8"), skip=())
    m.p("body")
    m.box((-4, 5.2, -2), (4, 13, 3.5), P(red, ov_shadow(0.2)))
    m.box((-6, 8, 3.5), (6, 16, 9), P(red, ov_frame("#7c1f1b", 0.7), ov_text("BIN", "#f4e3c1", 6)))
    m.box((-6.4, 16, 3.1), (6.4, 17, 9.4), yellow, skip=())
    m.box((-4.5, 4, 8.5), (4.5, 8, 11), dark)
    m.box((-2, 5.5, 11), (2, 7.5, 13), steel)
    for s in (-1, 1):
        wheel(m, s * 7.2, 2.6, 6, 2.6, 2, "#2a2b2f", "#e8b81a", "#8d9096", lug=False)
    m.box((-1, 13, -3), (1, 15, -2), light("#ffb347"))
    return m


def attach_sprayer():
    m = Model("attachment_sprayer", 61)
    steel = metal(STEEL)
    dark = metal(DARK)
    tank = P(paint("#e9e4d2", noise=3), ov_stripe("#2f6fbf", 0.5, 2.2, False))
    cyl_x(m, 0, 11, 2, 5.4, 14, {"all": tank, "east": paint("#d8d2bd"), "west": paint("#d8d2bd")})
    m.box((-1.4, 15.8, 0.6), (1.4, 17.6, 3.4), metal("#2f6fbf"), skip=())
    m.box((-1, 17.6, 1), (1, 18.2, 3), steel, skip=())
    m.box((-5.6, 5, -1), (5.6, 6.4, 5), dark)
    m.box((-4, 6.4, -1.2), (-2.8, 10, 5.2), steel)
    m.box((2.8, 6.4, -1.2), (4, 10, 5.2), steel)
    m.box((-0.6, 6.4, -6), (0.6, 8, -1), steel)
    m.box((-1.6, 8, 5), (1.6, 12, 5.8), P(paint("#d8d2bd"), ov_text("L", "#2f6fbf", 5)))
    m.box((-24, 6.2, 7.2), (24, 7.2, 8.4), P(steel, ov_stripe("#3a3d42", 0.5, 0.4, False)), skip=())
    for s in (-1, 1):
        m.box((s * 1 - 0.3 + (0 if s > 0 else -0.0), 7.2, 5.2), (s * 1 + 0.3, 8.6, 8), steel)
        m.box((s * 12 - 0.3, 7, 7.2), (s * 12 + 0.3, 12.6, 8.4), steel, rot=("z", 22.5 * s, (s * 12, 7, 7.8)))
        for i in range(2, 10):
            x = s * i * 2.4
            m.box((x - 0.4, 4.2, 7.3), (x + 0.4, 6.2, 8.3), paint("#2f6fbf"), skip=())
            m.box((x - 0.25, 3.4, 7.5), (x + 0.25, 4.2, 8.1), steel, skip=())
        m.box((s * 23.2 - 0.5, 4, 7), (s * 23.2 + 0.5, 8.2, 8.6), paint(YELLOW))
        wheel(m, s * 7, 2.4, 3, 2.4, 1.6, "#2a2b2f", "#cccccc", "#8d9096", lug=False)
    m.box((-0.3, 12.5, -6), (0.3, 13.1, 2), paint("#222"), skip=())
    return m


def train_loco():
    m = Model("train_locomotive", 71)
    steel = metal("#55585e")
    dark = metal("#202226")
    black = P(metal("#26282c"), ov_dots("#3c3f44", 6, 2))
    red = paint("#a82a24", noise=4)
    brass = metal("#c9962f")
    cyl_z(m, 0, 11.5, -8, 5.8, 26, {"all": P(metal("#2f3237"), ov_stripe("#c9962f", 0.35, 0.7, False), ov_stripe("#c9962f", 0.75, 0.7, False)), "north": black, "south": black})
    cyl_z(m, 0, 11.5, -19.2, 5.9, 3, {"all": black, "north": P(paint("#1d1f22"), ov_draw(lambda d, c, i: d.ellipse([c.pw * 0.2, c.ph * 0.2, c.pw * 0.8, c.ph * 0.8], fill=(120, 124, 130, 255))))})
    m.box((-1.4, 12.6, -20.7), (1.4, 14.4, -19.5), light("#fff3b0"))
    m.box((-1.8, 17.2, -17), (1.8, 19.8, -14.6), P(metal("#d7bf72"), ov_frame("#8a6c1f", 0.5)))
    m.box((-1.3, 17.6, -17.6), (1.3, 19.2, -17), light("#fff3b0"))
    cyl_y(m, 0, 16.8, -15.6, 1.9, 6, black)
    m.box((-2.6, 22.8, -17.4), (2.6, 23.8, -13.8), black, skip=())
    cyl_y(m, 0, 17, -9, 2.5, 2.8, metal("#c9962f"))
    cyl_y(m, 0, 17.2, -4, 1.7, 2, brass)
    m.box((-0.5, 19, -4.5), (0.5, 21.5, -3.5), brass, skip=())
    m.box((-6.4, 4.8, -13), (6.4, 5.8, 4), dark)
    for s in (-1, 1):
        m.box((s * 6.6 - 0.5, 5.8, -13), (s * 6.6 + 0.5, 6.8, 4), steel)
        m.box((s * 6.6 - 0.5, 6.8, -13), (s * 6.6 + 0.5, 7.4, 4), brass)
        m.box((s * 6.6 - 0.35, 9, -19), (s * 6.6 + 0.35, 10, -3), brass)
        cyl_z(m, s * 6.4, 8.2, -16, 1.5, 6, steel)
        m.box((s * 6.4 - 0.5, 8, -13), (s * 6.4 + 0.5, 8.9, -9), steel)
        for z in (-9, -1.5, 6):
            wheel(m, s * 7.6, 5.4, z, 5.4, 1.2, "#25272b", "#c0392b", "#b8bcc2", lug=False)
        m.box((s * 8.5 - 0.3, 5.1, -9.6), (s * 8.5 + 0.3, 5.9, 6.6), steel)
        wheel(m, s * 7, 2.8, -17, 2.8, 1.2, "#25272b", "#b8bcc2", "#8d9096", lug=False)
    m.box((-4.5, 3.2, -22.2), (4.5, 6.2, -20.4), P(steel, ov_vents("#16171a", 4, 0.8)), rot=("x", 22.5, (0, 4.5, -21.3)))
    m.box((-4.5, 6, 5), (4.5, 7.2, 22), dark)
    m.box((-6.4, 7.2, 5), (-5.8, 20.2, 21.4), planks("#8a2f26", 2.5, True), skip=())
    m.box((5.8, 7.2, 5), (6.4, 20.2, 21.4), planks("#8a2f26", 2.5, True), skip=())
    for s in (-1, 1):
        m.box((s * 6.1 - 0.2, 12, 8), (s * 6.1 + 0.2, 17, 14), glass("#a8dcf0", 110))
    m.box((-6.4, 7.2, 21), (6.4, 17, 21.8), planks("#8a2f26", 2.5, True))
    m.box((-6.4, 7.2, 4.4), (6.4, 20.2, 5.2), P(red, ov_shadow(0.2)))
    m.box((-3, 11, 4.2), (3, 17, 4.5), glass("#a8dcf0", 110))
    m.box((-7.6, 20.2, 3.4), (7.6, 21.8, 23), P(paint("#2b2d31", noise=3), ov_vents("#16171a", 4, 2)), skip=())
    m.box((-3.5, 7.2, 14), (3.5, 9.6, 21), black)
    m.box((-0.6, 9.6, 16), (0.6, 12.6, 18), steel)
    m.box((-2, 7.2, 10), (2, 8.4, 13), planks("#6b4a2a", 2))
    return m


def train_wagon():
    m = Model("train_wagon", 81)
    steel = metal("#55585e")
    dark = metal("#202226")
    wood = planks("#8a3b2b", 2.5, True)
    m.box((-6.6, 4.2, -21), (6.6, 5.6, 21), dark)
    m.box((-6.8, 5.6, -20.4), (6.8, 6.4, 20.4), planks("#4a3320", 3))
    m.box((-6.4, 6.4, -20), (6.4, 19.5, -19.2), P(planks("#8a3b2b", 2.5, True), ov_text("HMC", "#f1dca0", 9)))
    m.box((-6.4, 6.4, 19.2), (6.4, 19.5, 20), wood)
    for s in (-1, 1):
        m.box((s * 6 - 0.4, 6.4, -19.2), (s * 6 + 0.4, 19.5, 19.2), P(wood, ov_stripe("#4d1f16", 0.5, 0.5, False)), skip=())
        m.box((s * 6.5 - 0.35, 6.4, -20.2), (s * 6.5 + 0.35, 19.7, -19.4), steel)
        m.box((s * 6.5 - 0.35, 6.4, 19.4), (s * 6.5 + 0.35, 19.7, 20.2), steel)
        for z in (-12, -4, 4, 12):
            m.box((s * 6.4 - 0.25, 6.4, z - 0.4), (s * 6.4 + 0.25, 19.4, z + 0.4), paint("#3a2418"))
        m.box((s * 6.5 - 0.3, 6.4, -6), (s * 6.5 + 0.3, 19, 6), paint("#1b1410", noise=3), skip=())
    for s, nm in ((1, "door_e"), (-1, "door_w")):
        m.p(nm)
        m.box((s * 7.0, 7, -5.6), (s * 7.5, 18.6, 5.6), P(planks("#a6492f", 2.5, True), ov_frame("#3a2418", 0.7)), skip=())
        m.box((s * 7.0, 18.6, -6.6), (s * 7.5, 19.2, 6.6), steel, skip=())
        m.box((s * 7.5, 12, 4), (s * 8, 14, 5), steel)
    m.p("body")
    m.box((-6.5, 19.5, -20.2), (6.5, 20.4, 20.2), planks("#3a2418", 3), skip=())
    for s in (-1, 1):
        m.box((s * 3.4 - 3.7, 20.2, -20.4), (s * 3.4 + 3.7, 21.8, 20.4), planks("#4b4b50", 3), rot=("z", 22.5 * s, (s * 6.6, 20.2, 0)), skip=())
    m.box((-0.8, 22.6, -20.4), (0.8, 23.2, 20.4), steel, skip=())
    for z in (-21, 21):
        s = 1 if z > 0 else -1
        m.box((-0.8, 5.4, z), (0.8, 7.4, z + 1.8 * s), steel, skip=())
        m.box((-2.6, 5, z + 1.4 * s), (2.6, 7, z + 2.4 * s), dark)
        m.box((-0.4, 6.4, z + 2.4 * s), (0.4, 6.8, z + 3 * s), steel, skip=())
        m.box((6.2, 6.4, z - 0.6 * s), (7.3, 17.4, z + 0.2 * s), steel, skip=())
    for bz in (-13, 13):
        m.box((-5.4, 3.4, bz - 3.6), (5.4, 4.6, bz + 3.6), dark)
        for s in (-1, 1):
            m.box((s * 4.4 - 0.4, 3.4, bz - 3.4), (s * 4.4 + 0.4, 5, bz + 3.4), steel)
            for dz in (-2.4, 2.4):
                wheel(m, s * 5.4, 3, bz + dz, 3, 1.1, "#25272b", "#b8bcc2", "#8d9096", lug=False)
    return m


def cargo_crate():
    m = Model("cargo_crate", 91)
    wood = planks("#a9794a", 3)
    frame = planks("#6e4a2a", 1.6)
    steel = metal("#6a6e75")
    m.box((-9, 0, -7), (9, 11, 7), {"north": P(wood, ov_text("HARVEST", "#2d1c10", 7)), "all": wood})
    for x in (-9, 7.8):
        for z in (-7, 5.8):
            m.box((x, 0, z), (x + 1.2, 11.4, z + 1.2), frame, skip=())
    for y in (0, 10.2):
        m.box((-9.2, y, -7.2), (9.2, y + 1.2, 7.2), frame, skip=())
    m.box((-8.6, 5, -7.5), (8.6, 6.3, -7), frame, skip=())
    for s in (-1, 1):
        m.box((s * 8.1 - 1, 9.6, -7.6), (s * 8.1 + 1, 11.6, -6.6), steel, skip=())
        m.box((s * 8.1 - 1, -0.2, -7.6), (s * 8.1 + 1, 1.8, -6.6), steel, skip=())
    m.p("lid")
    m.box((-8.2, 11, -6.2), (8.2, 11.6, 6.2), frame, skip=())
    m.p("body")
    for i in range(7):
        x = -7 + i * 2.35
        m.box((x - 0.35, 11.6, -3 + (i % 3) * 0.8), (x + 0.35, 17.2 - (i % 2) * 1.4, -2.2 + (i % 3) * 0.8), paint("#e0b94a"), skip=())
        m.box((x - 0.6, 15.6 - (i % 2) * 1.4, -3.2 + (i % 3) * 0.8), (x + 0.6, 18.4 - (i % 2) * 1.4, -1.8 + (i % 3) * 0.8), paint("#c9962f"), skip=())
    m.box((-6, 11.6, 2), (-1, 14.6, 6), P(burlap(), ov_stripe("#7a6238", 0.5, 0.8, True)))
    m.box((-4.2, 14.6, 3), (-2.8, 15.6, 5), burlap("#a38757"), skip=())
    m.box((11, 0, -4), (17, 7, 3), P(burlap(), ov_stripe("#7a6238", 0.5, 0.8, True)))
    m.box((13, 7, -1.8), (15, 8.4, 0.8), burlap("#a38757"), skip=())
    m.box((-17, 0, -3), (-11, 2, 3), planks("#4a3320", 2), skip=())
    m.box((-16, 2, -2), (-12, 9, 2), P(paint("#8c7a5a"), ov_text("$", "#2b1f10", 9)), skip=())
    m.box((-16.4, 9, -2.4), (-11.6, 9.8, 2.4), steel, skip=())
    return m


TRACTORS = [
    ("tractor_small", dict(k=0.8, body="#c23b2e", trim="#e8d8b0", cab=False, dual=False, seed=11, label="HM-1")),
    ("tractor_medium", dict(k=0.95, body="#3f8f3a", trim="#f2c230", cab=True, dual=False, seed=12, label="HM-5")),
    ("tractor_large", dict(k=1.05, body="#2f5fa8", trim="#e8e8ea", cab=True, dual=True, seed=13, label="HM-9")),
]


def all_models():
    out = []
    for name, kw in TRACTORS:
        out.append(tractor(name, **kw))
    import attach2
    out += attach2.all_attachments() + [train_wagon(), cargo_crate()]
    return out
