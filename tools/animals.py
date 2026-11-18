from lib import *

PINK = "#f0a3b0"
DPINK = "#d98494"


def eyes(xs, y, size=1.2, white="#f7f7f7", pupil="#1b1b1b", iris=None):
    def f(d, ctx, img):
        for x in xs:
            X0, Y0, S = ctx.X(x), ctx.X(y), max(2, ctx.X(size))
            d.rectangle([X0, Y0, X0 + S - 1, Y0 + S - 1], fill=rgb(white) + (255,))
            q = max(1, S // 2)
            ox = X0 + (S - q) // 2
            oy = Y0 + S - q
            d.rectangle([ox, oy, ox + q - 1, oy + q - 1], fill=rgb(iris or pupil) + (255,))

    return ov_draw(f)


def nostrils(xs, y, w=0.8, h=0.8, color="#8a4a58"):
    def f(d, ctx, img):
        for x in xs:
            d.rectangle([ctx.X(x), ctx.X(y), ctx.X(x + w) - 1, ctx.X(y + h) - 1], fill=rgb(color) + (255,))

    return ov_draw(f)


def blush(xs, y, w, h, color="#e57f8a", alpha=110):
    def f(d, ctx, img):
        for x in xs:
            d.rectangle([ctx.X(x), ctx.X(y), ctx.X(x + w) - 1, ctx.X(y + h) - 1], fill=rgb(color) + (alpha,))

    return ov_draw(f)


def cow():
    m = Model("livestock_cow", 101)
    white, black = "#f5f2ea", "#1d1b1c"
    coat = fur(white, black, 7, 0.56, 4)
    coat2 = fur(white, black, 6, 0.6, 4)
    lowleg = paint("#eee8da", noise=4)
    belly = paint("#e6dfce", noise=4)
    dark = paint("#262221", noise=3)
    pink = paint("#f2a7b2", noise=4)
    horn = paint("#efe3c4", noise=3)
    horn_tip = paint("#a89a78", noise=3)
    m.box((-5.2, 9.4, -6.5), (5.2, 18.4, 8.6), coat)
    m.box((-5.7, 9.8, -8.2), (5.7, 18.8, -3.4), coat2)
    m.box((-5.5, 9.6, 4.2), (5.5, 18.6, 9.6), coat)
    m.box((-1.6, 18.6, -6.0), (1.6, 19.4, 8.5), coat2)
    m.box((-4.2, 8.3, -5.4), (4.2, 9.5, 6.4), belly)
    for s in (-1, 1):
        m.box((s * 3.4 - 0.9, 18.6, 5.6), (s * 3.4 + 0.9, 19.4, 8.4), coat2, skip=())
    m.box((-3.5, 12.0, -10.8), (3.5, 19.6, -6.2), coat2)
    m.box((-1.6, 10.0, -9.8), (1.6, 12.4, -7.6), coat2, skip=())
    head_n = P(coat2, ov_rect(black, 0.0, 0.0, 2.6, 3.2), ov_rect("#f2a7b2", 2.7, 3.2, 1.0, 2.0, 120))
    eye_e = P(coat2, eyes([3.0], 1.9, 1.4, iris="#2a1d14"))
    eye_w = P(coat2, ov_rect(black, 0.0, 0.4, 2.6, 3.4), eyes([0.5], 1.9, 1.4, iris="#2a1d14"))
    m.box((-3.2, 15.4, -14.6), (3.2, 20.6, -9.8), {"north": head_n, "east": eye_e, "west": eye_w, "all": coat2}, skip=())
    muz_n = P(pink, nostrils([1.1, 3.8], 1.0, 1.0, 1.0, "#7a3a47"))
    m.box((-2.8, 14.8, -16.6), (2.8, 17.6, -14.2), {"north": muz_n, "all": pink}, skip=())
    m.box((-3.0, 14.0, -13.8), (3.0, 15.8, -10.0), coat2, skip=())
    jaw_n = P(pink, ov_rect("#7a3a47", 0.4, 0.0, 4.0, 0.3))
    m.box((-2.4, 12.6, -15.8), (2.4, 14.8, -11.2), {"north": jaw_n, "up": paint("#d98494"), "all": belly}, skip=())
    for s in (-1, 1):
        m.box((s * 3.4 - 0.8, 20.4, -12.8), (s * 3.4 + 0.8, 21.6, -11.2), horn, skip=())
        m.box((s * 4.1 - 0.5, 21.4, -12.5), (s * 4.1 + 0.5, 23.4, -11.5), horn_tip, rot=("z", 22.5 * s, (s * 4.1, 21.4, -12.0)), skip=())
        m.box((s * 3.2, 18.4, -13.4), (s * 7.0, 19.6, -11.4), {"up": P(dark, ov_rect(DPINK, 0.6, 0.4, 2.8, 0.8, 140)), "all": dark}, rot=("z", 22.5 * s, (s * 3.2, 19.0, -12.4)), skip=())
    for sx in (-1, 1):
        for z in (-4.6, 6.4):
            m.box((sx * 3.5 - 1.7, 5.0, z - 1.6), (sx * 3.5 + 1.7, 9.8, z + 1.6), coat, skip=())
            m.box((sx * 3.5 - 1.2, 1.6, z - 1.2), (sx * 3.5 + 1.2, 5.2, z + 1.2), lowleg, skip=())
            m.box((sx * 3.5 - 1.4, 0, z - 1.4), (sx * 3.5 + 1.4, 1.8, z + 1.4), dark, skip=())
    m.box((-2.2, 7.2, 4.4), (2.2, 9.4, 8.2), P(pink, ov_dots(DPINK, 4, 1)), skip=())
    for sx in (-1, 1):
        for z in (5.2, 7.0):
            m.box((sx * 1.1 - 0.4, 6.0, z - 0.4), (sx * 1.1 + 0.4, 7.4, z + 0.4), pink, skip=())
    m.box((-0.5, 8.8, 9.6), (0.5, 18.4, 10.4), coat2, skip=())
    m.box((-0.9, 6.2, 9.4), (0.9, 9.6, 11.0), dark, skip=())
    collar = P(paint("#6b4423", noise=4), ov_dots("#c9962f", 3, 1))
    m.box((-3.75, 14.0, -10.9), (3.75, 15.4, -5.9), collar, skip=())
    m.box((-0.9, 11.6, -11.3), (0.9, 14.0, -10.1), metal("#e0b13a"), skip=())
    m.box((-0.3, 11.2, -11.0), (0.3, 11.8, -10.4), dark, skip=())
    return m


def pig():
    m = Model("livestock_pig", 102)
    skin = fur(PINK, "#e68f9f", 4, 0.7, 4)
    skinh = fur("#f4adba", None, 4, 0.7, 4)
    pink = paint("#f6b6c1", noise=4)
    dark = paint("#9c5662", noise=3)
    m.box((-4.5, 5.2, -6.5), (4.5, 13.4, 7.5), skin)
    m.box((-3.6, 7.6, -12.2), (3.6, 14.6, -6.2), {"north": P(skinh, eyes([0.5, 5.5], 2.4, 1.2, iris="#241616"), blush([0.3, 5.6], 4.6, 1.2, 1.3), ov_rect("#f08a9a", 1.6, 4.2, 4.0, 2.8, 140)), "all": skinh}, skip=())
    m.box((-2.3, 8.2, -13.8), (2.3, 11.4, -12.2), P(paint("#f9c3cc", noise=3), nostrils([0.8, 2.8], 1.0, 0.9, 0.9, "#7a3a47")))
    m.box((-2.2, 8.2, -12.3), (2.2, 8.8, -12.2), dark, skip=())
    for s in (-1, 1):
        m.box((s * 3.1 - 1.1, 14.4, -9.4), (s * 3.1 + 1.1, 17.4, -7.2), P(pink, ov_rect(DPINK, 0.3, 0.6, 1.6, 1.6, 140)), rot=("z", 22.5 * s, (s * 3.1, 14.4, -8.3)), skip=())
    for sx in (-1, 1):
        for z in (-4.8, 5.4):
            m.box((sx * 2.9 - 1.5, 1.2, z - 1.5), (sx * 2.9 + 1.5, 5.4, z + 1.5), skin, skip=())
            m.box((sx * 2.9 - 1.55, 0, z - 1.55), (sx * 2.9 + 1.55, 1.4, z + 1.55), paint("#4a2f33", noise=2), skip=())
    tail = paint("#e68f9f")
    m.box((-0.4, 10.4, 7.5), (0.4, 11.4, 8.5), tail, skip=())
    m.box((-0.4, 11.4, 8.2), (0.4, 12.4, 9.2), tail, skip=())
    m.box((-0.4, 12.2, 7.6), (0.4, 13.2, 8.6), tail, skip=())
    m.box((-4.55, 6.6, -4), (4.55, 9, 3), P(paint("#e68f9f", noise=4), ov_dots("#cf7a8a", 5, 1)), skip=("down", "up"))
    return m


def sheep():
    m = Model("livestock_sheep", 103)
    wl = curly("#f7f3e8", "#bdb49c", 3.0)
    wl2 = curly("#f2eddf", "#b8ae96", 2.6)
    wl3 = curly("#faf7ee", "#c9c0aa", 3.4)
    face = fur("#34312f", None, 4, 0.7, 4)
    snout = fur("#4a4543", None, 4, 0.7, 4)
    leg = paint("#2b2928", noise=3)
    skin = paint("#cdb9a2", noise=4)
    m.box((-4.0, 8.6, -5.2), (4.0, 15.0, 6.4), skin)
    m.box((-5.2, 8.8, -5.4), (5.2, 16.6, 7.0), wl, skip=())
    m.box((-4.2, 7.8, -5.3), (4.2, 17.6, 6.9), wl2, skip=())
    m.box((-4.2, 8.9, -6.6), (4.2, 16.5, 8.2), wl3, skip=())
    for (x, z, ang) in ((-2.4, -2.6, 45), (2.2, -3.0, 0), (-1.6, 2.2, 22.5), (2.6, 3.4, 45), (0.2, 5.4, 0), (-3.0, 5.6, 22.5)):
        m.box((x - 1.5, 17.4, z - 1.5), (x + 1.5, 18.6, z + 1.5), wl2 if ang else wl3, rot=("y", ang) if ang else None, skip=())
    m.box((-3.9, 12.6, -9.8), (3.9, 18.2, -5.6), wl2, skip=())
    m.box((-3.2, 13.4, -10.4), (3.2, 17.4, -9.6), wl3, skip=())
    face_n = P(face, eyes([0.6, 3.8], 2.9, 1.4, white="#e9e4d6", iris="#14110f"), ov_rect("#4a4543", 1.4, 4.4, 3.0, 1.4))
    m.box((-3.0, 12.2, -13.8), (3.0, 18.6, -8.4), {"north": face_n, "all": face}, skip=())
    m.box((-2.0, 11.8, -15.0), (2.0, 15.4, -13.6), {"north": P(snout, nostrils([0.7, 2.6], 0.7, 0.5, 0.6, "#15110f")), "all": snout}, skip=())
    m.box((-3.4, 18.4, -12.4), (3.4, 21.0, -8.0), wl3, skip=())
    m.box((-2.6, 17.8, -13.1), (2.6, 19.6, -12.2), wl2, skip=())
    for s in (-1, 1):
        m.box((s * 3.0, 14.0, -11.4), (s * 4.0, 17.8, -8.6), wl2, skip=())
        m.box((s * 3.0, 15.8, -12.4), (s * 6.4, 17.0, -10.2), {"up": P(face, ov_rect("#c9a7a0", 0.6, 0.3, 2.4, 0.6, 140)), "all": face}, rot=("z", 22.5 * s, (s * 3.0, 16.4, -11.3)), skip=())
        for z in (-4.2, 5.6):
            m.box((s * 3.0 - 1.5, 4.6, z - 1.5), (s * 3.0 + 1.5, 8.6, z + 1.5), wl2, skip=())
            m.box((s * 3.0 - 1.0, 1.2, z - 1.0), (s * 3.0 + 1.0, 4.8, z + 1.0), leg, skip=())
            m.box((s * 3.0 - 1.15, 0, z - 1.15), (s * 3.0 + 1.15, 1.4, z + 1.15), paint("#141313"), skip=())
    m.box((-1.5, 10.2, 8.4), (1.5, 15.0, 10.8), wl, skip=())
    return m


def chicken():
    m = Model("livestock_chicken", 104)
    f = feathers()
    fd = feathers("#e8dfcc", "#c9bda5")
    red = paint("#d6332a", noise=4)
    yel = paint("#f0b82a", noise=3)
    m.box((-3, 4.6, -4), (3, 11, 4.4), f)
    m.box((-2.4, 6.4, -4.6), (2.4, 10.4, -4), P(f, ov_rect("#fff9ea", 0.4, 0.6, 4, 3, 120)), skip=())
    m.box((-2, 10, -5.6), (2, 15.8, -2.2), {"north": f, "east": P(f, eyes([0.7], 2.2, 1.0)), "west": P(f, eyes([1.7], 2.2, 1.0)), "all": f}, skip=())
    for i, (z, h) in enumerate(((-4.4, 1.6), (-3.4, 2.1), (-2.4, 1.5))):
        m.box((-0.45, 15.8, z), (0.45, 15.8 + h, z + 1), red, skip=())
    m.box((-0.9, 11.6, -7.2), (0.9, 13.4, -5.6), yel, skip=())
    m.box((-0.45, 10.4, -6.2), (0.45, 12.0, -5.6), red, skip=())
    for s in (-1, 1):
        m.box((s * 3.3 - 0.4, 5.8, -2.4), (s * 3.3 + 0.4, 10.2, 3.4), fd, rot=("z", 12 if False else 22.5 * -s, (s * 3.3, 10.2, 0)), skip=())
        m.box((s * 1.4 - 0.35, 0, -0.35), (s * 1.4 + 0.35, 4.8, 0.35), yel, skip=())
        for dx in (-0.7, 0, 0.7):
            m.box((s * 1.4 + dx - 0.25, 0, -2.2), (s * 1.4 + dx + 0.25, 0.7, 0.4), yel, skip=())
    for dx, ang, c in ((0, -22.5, fd), (-1.2, -22.5, f), (1.2, -22.5, f)):
        m.box((dx - 0.6, 8, 4.4), (dx + 0.6, 13.4, 5.4), c, rot=("x", ang, (dx, 8, 4.4)), skip=())
    return m


def npc(name="npc_old_mcdonald", seed=105, shirt=("#a8342b", "#d0584a"), pants=("#355d99", "#2a4a7d"), hair=("#f4f4f0", "#dcdcd4", "#cfcfca"),
        hat_color=None, band="#8a2f26", brim="#b9964a", tool="fork", skin_color="#e8b88d"):
    m = Model(name, seed)
    skin = paint(skin_color, noise=4)
    denim = P(cloth(pants[0], 1, 5), ov_stripe(pants[1], 0.5, 0.3, True))
    plaidr = plaid(shirt[0], shirt[1], 1.5)
    boot = paint("#4d3220", noise=3)
    white = fur(hair[0], hair[1], 3, 0.6, 5)
    gray = fur(hair[2], None, 3, 0.6, 5)
    hat = straw() if hat_color is None else paint(hat_color, noise=4)
    for s in (-1, 1):
        m.box((s * 2 - 1.9, 3, -2.2), (s * 2 + 1.9, 10.5, 2.2), denim, skip=())
        m.box((s * 2 - 2, 0, -2.6), (s * 2 + 2, 3.2, 3), boot, skip=())
        m.box((s * 2 - 2.05, 0, -3), (s * 2 + 2.05, 1.2, 3.1), paint("#2b1d12"), skip=())
    bodyfront = P(plaidr, ov_draw(lambda d, c, i: (d.rectangle([c.X(1.0), c.X(3.0), c.X(7.0) - 1, c.ph], fill=(53, 93, 153, 255)), d.rectangle([c.X(1.0), c.X(0.0), c.X(2.2) - 1, c.X(3.0)], fill=(53, 93, 153, 255)), d.rectangle([c.X(5.8), c.X(0.0), c.X(7.0) - 1, c.X(3.0)], fill=(53, 93, 153, 255)), d.rectangle([c.X(2.6), c.X(6.0), c.X(5.4) - 1, c.X(8.0) - 1], outline=(36, 62, 108, 255)), d.rectangle([c.X(1.0), c.X(2.6), c.X(2.2) - 1, c.X(3.2) - 1], fill=(224, 177, 58, 255)), d.rectangle([c.X(5.8), c.X(2.6), c.X(7.0) - 1, c.X(3.2) - 1], fill=(224, 177, 58, 255)))))
    bodyback = P(plaidr, ov_draw(lambda d, c, i: (d.rectangle([c.X(0.0), c.X(4.2), c.pw, c.ph], fill=(53, 93, 153, 255)), d.line([c.X(1.2), 0, c.X(5.4), c.X(4.4)], fill=(36, 62, 108, 255)), d.line([c.X(6.8), 0, c.X(2.6), c.X(4.4)], fill=(36, 62, 108, 255)))))
    m.box((-4, 10.5, -2.4), (4, 22, 2.4), {"north": bodyfront, "south": bodyback, "east": P(denim, ov_rect(shirt[0], 0, 0, 4.8, 4.0)), "west": P(denim, ov_rect(shirt[0], 0, 0, 4.8, 4.0)), "up": plaidr, "down": denim}, skip=())
    m.box((-4.3, 9.6, -2.7), (4.3, 11.0, 2.7), P(paint("#4d3220"), ov_rect("#d9a83a", 3.2, 0.2, 2.2, 0.9)), skip=())
    for s in (-1, 1):
        m.box((s * 5.6 - 1.7, 11.8, -2), (s * 5.6 + 1.7, 21.8, 2), plaidr, rot=("x", -22.5 if s > 0 else 0, (s * 5.6, 21.2, 0)), skip=())
        m.box((s * 5.6 - 1.6, 9.8, -2.9 if s > 0 else -1.9), (s * 5.6 + 1.6, 11.8, -0.9 if s > 0 else 2.1), skin, skip=())
    if tool == "fork":
        m.box((5.1, 0, -3.9), (5.9, 26.0, -3.1), planks("#8a6038", 1.5, True), skip=())
        m.box((3.9, 24.8, -4.1), (7.1, 26.0, -2.9), metal("#8f9399"), skip=())
        for dx in (-1.2, 0, 1.2):
            m.box((5.5 + dx - 0.3, 26.0, -3.8), (5.5 + dx + 0.3, 29.4, -3.2), metal("#b9bdc3"), skip=())
    elif tool == "board":
        m.box((4.6, 9.0, -4.4), (7.0, 17.0, -3.6), planks("#8a6038", 1.5, True), skip=())
        m.box((4.9, 9.4, -4.6), (6.7, 16.4, -4.3), paint("#f4f0e6", noise=3), skip=())
    elif tool == "wrench":
        m.box((5.1, 6.0, -3.6), (5.9, 16.0, -3.0), metal("#8f9399"), skip=())
        m.box((4.5, 16.0, -3.9), (6.5, 18.2, -2.7), metal("#b9bdc3"), skip=())
    face_n = P(skin, blush([0.6, 5.7], 4.0, 1.2, 1.3, "#e9807a", 120), ov_rect("#cfcfca", 0.8, 0.6, 2.4, 0.7), ov_rect("#cfcfca", 4.3, 0.6, 2.4, 0.7), eyes([1.1, 4.6], 1.7, 1.6, iris="#3a7bb5"))
    m.box((-3.75, 22, -3.75), (3.75, 29.5, 3.75), {"north": face_n, "south": gray, "up": hat, "all": gray}, skip=())
    m.box((-3.5, 19.8, -4.5), (3.5, 24.4, -3.3), {"north": P(white, ov_rect("#dcdcd4", 1.6, 2.6, 3.8, 0.4)), "all": white}, skip=())
    m.box((-3.1, 24.2, -4.6), (3.1, 25.6, -3.7), white, skip=())
    m.box((-0.95, 24.8, -4.9), (0.95, 27.0, -3.9), P(paint("#efa488"), ov_rect("#d98672", 0.2, 1.6, 1.6, 0.5)), skip=())
    m.box((-3.85, 24, -2.8), (-3.4, 28, 2.6), gray, skip=())
    m.box((3.4, 24, -2.8), (3.85, 28, 2.6), gray, skip=())
    m.box((-0.9, 23.2, -4.3), (0.9, 23.9, -3.4), P(paint(shirt[0]), ov_rect(shirt[1], 0.2, 0.2, 1.4, 0.2)), skip=())
    m.box((0.6, 23.4, -6.8), (1.2, 24.0, -4), paint("#e8c35a"), rot=("y", 22.5), skip=())
    m.box((-6.6, 28.4, -6.6), (6.6, 29.5, 6.6), P(hat, ov_frame(brim, 0.4)), skip=())
    m.box((-4.2, 29.5, -4.2), (4.2, 30.4, 4.2), paint(band, noise=3), skip=())
    m.box((-3.9, 30.4, -3.9), (3.9, 32, 3.9), hat, skip=())
    return m


NPC_VARIANTS = (
    ("npc_farmer", 106, dict(shirt=("#3f7a3a", "#5aa050"), pants=("#8a6a42", "#6f5232"), hair=("#d8b45a", "#c29a40", "#cfa84e"), band="#2f5f2a", tool="fork")),
    ("npc_rancher", 107, dict(shirt=("#7a4a2a", "#9a6038"), pants=("#2a2d33", "#1f2227"), hair=("#6b4a2a", "#573a20", "#5e4125"), hat_color="#6b4a2a", band="#2a1d12", brim="#8a6038", tool="board")),
    ("npc_builder", 108, dict(shirt=("#e8791c", "#f2a14a"), pants=("#6d7076", "#55585e"), hair=("#3a2a1c", "#2a1d12", "#33241a"), hat_color="#f2c230", band="#e8791c", brim="#d9a81c", tool="board")),
    ("npc_mechanic", 109, dict(shirt=("#2f5fa8", "#4a7bc4"), pants=("#1f2a44", "#16203a"), hair=("#9aa0a6", "#80868c", "#8d9399"), hat_color="#c0392b", band="#8a2a20", brim="#a8322a", tool="wrench")),
    ("npc_pilot", 110, dict(shirt=("#b8a47c", "#c9b88f"), pants=("#6b4a2a", "#573a20"), hair=("#2a1d12", "#1f160d", "#251a10"), hat_color="#e8eef2", band="#2f5fa8", brim="#c9d2da", tool="board")),
    ("npc_conductor", 111, dict(shirt=("#1f2a44", "#2f3d5c"), pants=("#1f2a44", "#16203a"), hair=("#cfcfca", "#b8b8b2", "#c4c4be"), hat_color="#1f2a44", band="#d6a238", brim="#2f3d5c", tool="none")),
)


def all_models():
    return [cow(), pig(), sheep(), chicken(), npc()] + [npc(n, sd, **kw) for n, sd, kw in NPC_VARIANTS]
