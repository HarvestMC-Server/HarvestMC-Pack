from lib import *
from animals import eyes, blush


def face_tex(skin, iris, female=False, brow="#3a2a1c", mouth=None, freckles=False, stubble=None):
    """15x15 pixel face: eyes with pupil and iris, brows, nose shadow, smile with lips."""
    lip = rgb(mouth or ("#c24a5a" if female else "#9a4f47"))
    dark = (42, 24, 22)
    brow_c = rgb(brow)
    iris_c = rgb(iris)
    skin_c = rgb(skin)
    shade = tuple(max(0, int(v * 0.82)) for v in skin_c)

    def fn(d, c, img):
        cw = c.pw / 15.0
        ch = c.ph / 15.0

        def px(col, row, color, alpha=255):
            d.rectangle([int(col * cw), int(row * ch), max(int(col * cw), int((col + 1) * cw) - 1), max(int(row * ch), int((row + 1) * ch) - 1)], fill=tuple(color) + (alpha,))

        if stubble:
            sc = rgb(stubble)
            blend = tuple(int(skin_c[i] * 0.6 + sc[i] * 0.4) for i in range(3))
            for row in range(8, 15):
                for col in range(2, 13):
                    px(col, row, blend)
        for ex in (4, 10):
            px(ex - 1, 4, (250, 250, 250)); px(ex, 4, dark); px(ex + 1, 4, (250, 250, 250))
            px(ex - 1, 5, (250, 250, 250)); px(ex, 5, iris_c); px(ex + 1, 5, (250, 250, 250))
            px(ex - 1, 3 if female else 2, brow_c); px(ex, 3 if female else 2, brow_c); px(ex + 1, 3 if female else 2, brow_c)
            if not female:
                px(ex - 1, 3, brow_c, 150)
                px(ex + 1, 3, brow_c, 150)
            else:
                px(ex - 1, 3, dark); px(ex + 1, 3, dark)
        px(7, 7, shade)
        px(6, 8, shade)
        px(8, 8, shade)
        if female:
            for col in (3, 4, 10, 11):
                px(col, 8, (233, 128, 122), 130)
            px(6, 10, lip); px(7, 10, lip); px(8, 10, lip)
            px(5, 11, lip); px(6, 11, lip); px(7, 11, (240, 160, 170)); px(8, 11, lip); px(9, 11, lip)
            px(4, 10, dark, 120); px(10, 10, dark, 120)
        else:
            for col in range(5, 10):
                px(col, 10, dark)
            px(4, 9, dark, 110); px(10, 9, dark, 110)
            px(6, 11, lip); px(7, 11, lip); px(8, 11, lip)
        if freckles:
            for col, row in ((3, 7), (5, 7), (9, 7), (11, 7), (4, 8), (10, 8), (7, 6)):
                px(col, row, (168, 106, 72), 170)
    return P(paint(skin, noise=4), ov_draw(fn))


def legs(m, g, pants, boots, boot_h=3.2, tall=False):
    w = 1.6 if g == "f" else 1.9
    for s in (-1, 1):
        m.box((s * 2 - w, 3, -2.2), (s * 2 + w, 10.5, 2.2), pants, skip=())
        m.box((s * 2 - w - 0.1, 0, -2.6), (s * 2 + w + 0.1, boot_h + (3.0 if tall else 0), 3), boots, skip=())
        m.box((s * 2 - w - 0.15, 0, -3), (s * 2 + w + 0.15, 1.2, 3.1), paint("#2b1d12"), skip=())


def torso(m, g, shirt_front, shirt_back, shirt_side, belt=None, bulk=0.0):
    if g == "f":
        half = 3.5 + bulk
        m.box((-half, 13.0, -2.3), (half, 22, 2.3), {"north": shirt_front, "south": shirt_back, "east": shirt_side, "west": shirt_side, "all": shirt_side}, skip=())
        m.box((-half + 0.5, 10.5, -2.1), (half - 0.5, 13.0, 2.1), shirt_side, skip=())
    else:
        half = 4.0 + bulk
        m.box((-half, 10.5, -2.4), (half, 22, 2.4), {"north": shirt_front, "south": shirt_back, "east": shirt_side, "west": shirt_side, "all": shirt_side}, skip=())
    if belt:
        w = 3.7 if g == "f" else 4.3 + bulk
        m.box((-w, 9.6, -2.7), (w, 11.0, 2.7), belt, skip=())


def arms(m, g, sleeve, skin_mat, glove=None, cuff=None):
    for s in (-1, 1):
        m.box((s * 5.4 - 1.6, 11.8, -2.0), (s * 5.4 + 1.6, 21.8, 2.0), sleeve, rot=("x", -22.5, (s * 5.4, 21.2, 0)) if s > 0 else None, skip=())
        hand = glove if glove is not None else skin_mat
        m.box((s * 5.4 - 1.5, 9.8, -2.9 if s > 0 else -1.9), (s * 5.4 + 1.5, 11.8, -0.9 if s > 0 else 2.1), hand, skip=())
        if cuff:
            m.box((s * 5.4 - 1.7, 11.6, -2.2), (s * 5.4 + 1.7, 12.6, 2.2), cuff, skip=())


def head(m, skin, face_n, nose=True, lip=None, lip_w=1.2):
    m.box((-3.75, 22, -3.75), (3.75, 29.5, 3.75), {"north": face_n, "all": paint(skin, noise=4)}, skip=())
    m.box((-0.9, 24.2, -4.7), (0.9, 26.4, -3.9), paint(skin, noise=3), skip=())
    m.box((-1.8, 19.6, -1.8), (1.8, 22.2, 1.8), paint(skin, noise=3), skip=())
    m.box((-4.25, 24.0, -0.8), (-3.75, 26.8, 1.2), paint(skin, noise=3), skip=())
    m.box((3.75, 24.0, -0.8), (4.25, 26.8, 1.2), paint(skin, noise=3), skip=())
    if lip:
        m.box((-lip_w, 22.9, -4.0), (lip_w, 23.7, -3.75), paint(lip, noise=2), skip=())
        m.box((-lip_w * 0.8, 23.7, -3.95), (lip_w * 0.8, 24.1, -3.75), paint(lip, noise=2), skip=())


def hair(m, style, color, dark=None):
    h = fur(color, dark, 3, 0.62, 5)
    m.box((-3.95, 28.0, -3.95), (3.95, 29.9, 3.95), h, skip=())
    m.box((-3.95, 26.0, 2.8), (3.95, 29.9, 4.0), h, skip=())
    m.box((-3.95, 25.2 if style != "long" else 24.0, -2.0), (-3.7, 29.9, 4.0), h, skip=())
    m.box((3.7, 25.2 if style != "long" else 24.0, -2.0), (3.95, 29.9, 4.0), h, skip=())
    m.box((-3.95, 27.2, -4.1), (3.95, 29.9, -3.7), h, skip=())
    m.box((-3.95, 27.2, -4.1), (-2.4, 28.2, -3.7), h, skip=())
    if style == "long":
        m.box((-3.95, 19.5, 2.8), (3.95, 25.0, 4.4), h, skip=())
        m.box((-3.6, 14.5, 2.4), (3.6, 19.5, 4.0), h, skip=())
    elif style == "ponytail":
        m.box((-0.8, 27.0, 3.9), (0.8, 28.6, 5.0), paint("#c0392b"), skip=())
        m.box((-1.3, 20.0, 4.6), (1.3, 27.0, 6.4), h, skip=())
    elif style == "bun":
        m.box((-1.9, 29.6, 0.6), (1.9, 31.9, 4.0), h, skip=())
        m.box((-2.0, 29.4, 0.4), (2.0, 30.0, 4.2), paint("#c0392b"), skip=())
    elif style == "braids":
        for s in (-1, 1):
            m.box((s * 3.9 - 0.8, 19.5, 0.4), (s * 3.9 + 0.8, 26.0, 2.2), h, skip=())
            m.box((s * 3.9 - 0.7, 14.5, 0.5), (s * 3.9 + 0.7, 19.5, 2.1), h, skip=())
            m.box((s * 3.9 - 0.9, 14.0, 0.3), (s * 3.9 + 0.9, 15.2, 2.3), paint("#f2c230"), skip=())
    elif style == "short":
        pass


def beard(m, color, full=True):
    b = fur(color, None, 3, 0.6, 5)
    m.box((-3.4, 22.2, -4.4), (3.4, 23.2, -3.5), b, skip=())
    m.box((-3.4, 23.2, -4.4), (-1.5, 25.0, -3.5), b, skip=())
    m.box((1.5, 23.2, -4.4), (3.4, 25.0, -3.5), b, skip=())
    if full:
        m.box((-3.8, 24.0, -3.3), (-3.3, 27.5, 2.0), b, skip=())
        m.box((3.3, 24.0, -3.3), (3.8, 27.5, 2.0), b, skip=())


def mustache(m, color, wide=3.4):
    m.box((-wide / 2, 24.2, -4.4), (wide / 2, 25.1, -3.7), fur(color, None, 3, 0.6, 5), skip=())


def finalize_pose(m):
    return m


def farmer():
    m = Model("npc_farmer", 106)
    skin = "#f1c9a5"
    gingham = plaid("#f6f1e2", "#e8d9a8", 1.2)
    denim = P(cloth("#4a6fa5", 1, 5), ov_stripe("#385783", 0.5, 0.3, True))
    boot = paint("#3f6b32", noise=3)
    legs(m, "f", denim, boot)
    torso(m, "f", P(gingham, ov_rect("#4a6fa5", 1.0, 0.0, 1.0, 9.0), ov_rect("#4a6fa5", 5.5, 0.0, 1.0, 9.0), ov_rect("#4a6fa5", 1.8, 3.0, 3.4, 5.0)), gingham, gingham, belt=paint("#7a5230"))
    m.box((-2.4, 11.0, -2.45), (2.4, 17.0, -2.25), P(denim, ov_rect("#385783", 0.6, 0.6, 3.6, 3.0), ov_rect("#d6a238", 0.4, 0.2, 0.5, 0.5), ov_rect("#d6a238", 4.9, 0.2, 0.5, 0.5)), skip=())
    for s in (-1, 1):
        m.box((s * 2.3 - 0.35, 17.0, -2.5), (s * 2.3 + 0.35, 22.0, 2.5), denim, skip=())
    arms(m, "f", gingham, paint(skin, noise=3))
    head(m, skin, face_tex(skin, "#3a7bb5", True, "#8a5a2c", freckles=True), True, "#c24a5a", 1.3)
    hair(m, "braids", "#e0b050", "#c89a3c")
    m.box((-6.8, 28.2, -6.8), (6.8, 29.2, 6.8), P(straw(), ov_frame("#b9964a", 0.4)), skip=())
    m.box((-4.2, 29.2, -4.2), (4.2, 31.8, 4.2), straw(), skip=())
    m.box((-4.3, 29.2, -4.3), (4.3, 30.2, 4.3), paint("#c0392b", noise=3), skip=())
    m.box((4.6, 8.6, -4.6), (7.4, 12.6, -1.4), planks("#a8825a", 1.4, True), skip=())
    m.box((4.6, 12.6, -3.2), (7.4, 14.2, -2.8), planks("#8a6038", 1.4), skip=())
    for k in range(3):
        m.box((5.0 + k * 0.9, 12.4, -3.8 + k * 0.5), (5.8 + k * 0.9, 13.6, -2.8 + k * 0.5), paint(["#e8453c", "#f2862a", "#7ee05a"][k], noise=5), skip=())
    return m


def rancher():
    m = Model("npc_rancher", 107)
    skin = "#c98f66"
    plaidr = plaid("#9b2f24", "#c04a3a", 1.5)
    jeans = P(cloth("#2f4a7a", 1, 5), ov_stripe("#243a62", 0.5, 0.3, True), ov_rect("#c8b078", 0.3, 0.0, 0.7, 10.0))
    boot = paint("#6b4a2a", noise=4)
    legs(m, "m", jeans, boot, 3.2, tall=True)
    torso(m, "m", plaidr, plaidr, plaidr, belt=P(paint("#4d3220"), ov_rect("#d9a83a", 3.4, 0.2, 2.6, 1.0)))
    leather = paint("#7a4a28", noise=5)
    m.box((-4.2, 12.0, -2.6), (-0.6, 21.0, -2.2), leather, skip=())
    m.box((0.6, 12.0, -2.6), (4.2, 21.0, -2.2), leather, skip=())
    m.box((-4.2, 12.0, 2.2), (4.2, 21.0, 2.6), leather, skip=())
    m.box((-4.1, 17.6, -2.7), (-3.2, 18.6, -2.4), metal("#d9a83a"), skip=())
    arms(m, "m", plaidr, paint(skin, noise=3), cuff=paint("#7a4a28"))
    head(m, skin, face_tex(skin, "#5a3a22", False, "#3a2412", stubble="#3a2a1c"), True, "#8a4a42", 1.1)
    hair(m, "short", "#4a3320", "#33241a")
    mustache(m, "#4a3320", 3.6)
    m.box((-3.4, 20.2, -3.0), (3.4, 22.6, 3.0), paint("#c0392b", noise=4), skip=())
    m.box((-0.8, 20.0, -3.4), (0.8, 22.2, -2.8), paint("#c0392b", noise=4), skip=())
    hat = planks("#a8825a", 1.2, True, 0.8, 0.04)
    m.box((-6.8, 28.3, -6.2), (6.8, 29.3, 6.2), P(hat, ov_frame("#6b4a2a", 0.4)), skip=())
    m.box((-7.6, 29.0, -5.6), (-5.4, 30.0, 5.6), hat, rot=("z", 22.5), skip=())
    m.box((5.4, 29.0, -5.6), (7.6, 30.0, 5.6), hat, rot=("z", -22.5), skip=())
    m.box((-3.9, 29.3, -3.9), (3.9, 31.7, 3.9), hat, skip=())
    m.box((-4.0, 29.3, -4.0), (4.0, 30.4, 4.0), paint("#4d3220", noise=3), skip=())
    m.box((-1.6, 31.6, -3.8), (1.6, 32.0, 3.8), hat, skip=())
    m.box((4.8, 8.2, -3.4), (7.2, 13.6, -1.0), paint("#c8b078", noise=6), skip=())
    m.box((4.9, 8.4, -3.5), (7.1, 9.0, -0.9), paint("#a8905c", noise=5), skip=())
    m.box((4.9, 10.2, -3.5), (7.1, 10.8, -0.9), paint("#a8905c", noise=5), skip=())
    return m


def builder():
    m = Model("npc_builder", 108)
    skin = "#a8724a"
    tee = paint("#8d9298", noise=4)
    vest = P(paint("#e8791c", noise=4), ov_stripe("#e8eef2", 0.45, 0.9, False), ov_stripe("#e8eef2", 0.72, 0.9, False))
    cargo = P(cloth("#5c6068", 1, 5), ov_rect("#4a4d54", 0.2, 3.0, 3.4, 2.6), ov_rect("#4a4d54", 3.6, 3.0, 3.4, 2.6))
    boot = paint("#5a4a30", noise=3)
    legs(m, "m", cargo, boot, 3.6)
    torso(m, "m", P(tee, ov_stripe("#e8eef2", 0.5, 0.9, False)), tee, tee, belt=P(paint("#4d3220"), ov_rect("#8f9399", 3.4, 0.2, 1.8, 1.0)), bulk=0.4)
    m.box((-4.5, 12.0, -2.7), (-0.5, 21.6, -2.4), vest, skip=())
    m.box((0.5, 12.0, -2.7), (4.5, 21.6, -2.4), vest, skip=())
    m.box((-4.5, 12.0, 2.4), (4.5, 21.6, 2.7), vest, skip=())
    for s in (-1, 1):
        m.box((s * 3.4 - 0.6, 12.0, -2.8), (s * 3.4 + 0.6, 21.6, -2.4), paint("#e8eef2", noise=2), skip=())
    m.box((-4.5, 8.6, -3.0), (-2.4, 10.4, -2.6), paint("#5a4a30"), skip=())
    m.box((2.4, 8.6, -3.0), (4.5, 10.4, -2.6), paint("#5a4a30"), skip=())
    arms(m, "m", tee, paint(skin, noise=3), glove=paint("#d9c27a", noise=4))
    head(m, skin, face_tex(skin, "#2a1d12", False, "#1f160d", stubble="#2a1d12"), True, "#7a3a34", 1.1)
    hair(m, "short", "#2a1d12", "#1f160d")
    beard(m, "#2a1d12", True)
    hat = paint("#f2c230", noise=4)
    m.box((-4.3, 28.6, -4.3), (4.3, 31.6, 4.3), hat, skip=())
    m.box((-4.5, 28.4, -6.0), (4.5, 29.2, -3.8), hat, skip=())
    m.box((-0.7, 31.6, -4.0), (0.7, 32.0, 4.0), hat, skip=())
    m.box((-4.4, 29.6, -4.4), (4.4, 30.2, 4.4), paint("#e8791c", noise=3), skip=())
    m.box((5.3, 4.0, -3.6), (6.1, 17.0, -2.8), planks("#8a6038", 1.4, True), skip=())
    m.box((4.0, 16.6, -4.0), (7.6, 19.0, -2.4), metal("#8f9399"), skip=())
    return m


def mechanic():
    m = Model("npc_mechanic", 109)
    skin = "#8a5a3c"
    blue = P(cloth("#2f5fa8", 1, 5), ov_stripe("#244a85", 0.5, 0.3, True))
    smudge = P(blue, ov_rect("#1a1a1a", 1.0, 2.0, 1.6, 0.9, 150), ov_rect("#1a1a1a", 4.0, 5.0, 1.4, 0.8, 130))
    boot = paint("#2a2d33", noise=3)
    legs(m, "f", smudge, boot, 3.4)
    torso(m, "f", P(blue, ov_rect("#e8b81a", 2.2, 3.4, 3.0, 0.5), ov_rect("#244a85", 1.2, 5.0, 1.6, 1.8)), blue, blue, belt=paint("#4d3220"))
    for s in (-1, 1):
        m.box((s * 1.4 - 0.5, 15.0, -2.6), (s * 1.4 + 0.5, 17.2, -2.3), metal("#c9962f"), skip=())
    arms(m, "f", blue, paint(skin, noise=3), glove=paint("#3a3d42", noise=3), cuff=paint("#244a85"))
    head(m, skin, face_tex(skin, "#2a1d12", True, "#1f160d", mouth="#8a3a48", freckles=False), True, "#b8465a", 1.3)
    hair(m, "ponytail", "#1f160d", "#15100a")
    band = paint("#c0392b", noise=4)
    m.box((-3.95, 27.4, -3.95), (3.95, 28.6, 3.95), band, skip=())
    m.box((-3.95, 27.4, -4.0), (3.95, 28.6, -3.7), P(band, ov_dots("#f4f0e6", 3, 1)), skip=())
    m.box((-1.4, 28.0, 3.9), (1.4, 29.4, 5.2), band, skip=())
    m.box((-3.6, 29.0, -3.0), (3.6, 30.6, 0.0), metal("#8d9399"), skip=())
    m.box((-2.8, 29.4, -3.6), (-0.8, 30.8, -2.8), glass("#9fd4ee", 160), skip=())
    m.box((0.8, 29.4, -3.6), (2.8, 30.8, -2.8), glass("#9fd4ee", 160), skip=())
    m.box((5.1, 6.0, -3.6), (5.9, 16.0, -3.0), metal("#8f9399"), skip=())
    m.box((4.5, 16.0, -3.9), (6.5, 18.2, -2.7), metal("#b9bdc3"), skip=())
    m.box((4.9, 17.2, -3.5), (6.1, 17.8, -3.1), metal("#2a2d33"), skip=())
    return m


def pilot():
    m = Model("npc_pilot", 110)
    skin = "#e0ac84"
    leather = P(paint("#7a4a28", noise=6), ov_stripe("#5a3a1e", 0.5, 0.3, True))
    khaki = P(cloth("#b8a47c", 1, 5), ov_stripe("#a08c64", 0.5, 0.3, True))
    boot = paint("#2a1d12", noise=3)
    legs(m, "m", khaki, boot, 3.4, tall=True)
    torso(m, "m", P(leather, ov_rect("#c9962f", 1.6, 1.0, 0.6, 0.6), ov_rect("#c9962f", 5.8, 1.0, 0.6, 0.6)), leather, leather, belt=paint("#3a2412"))
    fluff = fur("#f4efe2", "#dcd6c4", 3, 0.6, 5)
    m.box((-4.4, 20.4, -2.8), (4.4, 22.6, 2.8), fluff, skip=())
    m.box((-4.3, 9.8, -2.7), (4.3, 10.8, 2.7), leather, skip=())
    arms(m, "m", leather, paint(skin, noise=3), glove=paint("#3a2412", noise=3), cuff=fluff)
    head(m, skin, face_tex(skin, "#3a7bb5", False, "#4a3320", stubble="#4a3320"), True, "#a85a4a", 1.1)
    hair(m, "short", "#5a4028", "#46321e")
    mustache(m, "#5a4028", 3.2)
    scarf = paint("#f4f0e6", noise=3)
    m.box((-3.6, 20.2, -3.3), (3.6, 22.4, 3.3), scarf, skip=())
    m.box((1.2, 11.0, -3.6), (3.6, 20.4, -2.9), scarf, skip=())
    cap = paint("#6b4a2a", noise=4)
    m.box((-4.1, 27.4, -4.1), (4.1, 30.2, 4.1), cap, skip=())
    m.box((-4.3, 23.8, -2.6), (-3.7, 28.0, 1.8), cap, skip=())
    m.box((3.7, 23.8, -2.6), (4.3, 28.0, 1.8), cap, skip=())
    m.box((-4.0, 28.9, -4.5), (4.0, 31.0, -3.6), metal("#2a2d33"), skip=())
    m.box((-3.4, 29.3, -4.9), (-0.3, 30.7, -4.4), glass("#9fd4ee", 170), skip=())
    m.box((0.3, 29.3, -4.9), (3.4, 30.7, -4.4), glass("#9fd4ee", 170), skip=())
    m.box((4.6, 9.0, -4.4), (7.0, 17.0, -3.6), planks("#8a6038", 1.5, True), skip=())
    m.box((4.9, 9.4, -4.6), (6.7, 16.4, -4.3), paint("#f4f0e6", noise=3), skip=())
    return m


def conductor():
    m = Model("npc_conductor", 111)
    skin = "#6b452e"
    navy = P(cloth("#1f2a44", 1, 5), ov_stripe("#2f3d5c", 0.5, 0.3, True))
    jacket = P(navy, ov_rect("#d6a238", 1.0, 1.6, 0.6, 0.6), ov_rect("#d6a238", 1.0, 3.4, 0.6, 0.6), ov_rect("#d6a238", 1.0, 5.2, 0.6, 0.6),
               ov_rect("#d6a238", 5.9, 1.6, 0.6, 0.6), ov_rect("#d6a238", 5.9, 3.4, 0.6, 0.6), ov_rect("#d6a238", 5.9, 5.2, 0.6, 0.6))
    boot = paint("#16140f", noise=3)
    legs(m, "f", paint("#2a2d33", noise=3), boot, 3.0)
    torso(m, "f", jacket, navy, navy, belt=P(paint("#16140f"), ov_rect("#d6a238", 3.2, 0.2, 1.6, 1.0)))
    m.box((-5.0, 6.0, -3.0), (5.0, 11.0, 3.0), navy, skip=())
    m.box((-5.2, 10.2, -3.1), (5.2, 11.0, 3.1), paint("#d6a238", noise=3), skip=())
    m.box((-1.6, 18.0, -2.5), (1.6, 22.0, -2.2), paint("#f4f0e6", noise=3), skip=())
    m.box((-0.2, 12.5, -2.5), (0.2, 17.5, -2.3), metal("#d6a238"), skip=())
    arms(m, "f", navy, paint(skin, noise=3), glove=paint("#f4f0e6", noise=3), cuff=paint("#d6a238"))
    head(m, skin, face_tex(skin, "#2a1d12", True, "#1f160d", mouth="#7a2a3a"), True, "#a83a52", 1.3)
    hair(m, "bun", "#1f160d", "#15100a")
    cap = paint("#1f2a44", noise=3)
    m.box((-4.1, 28.2, -4.1), (4.1, 30.8, 4.1), cap, skip=())
    m.box((-4.2, 28.2, -4.2), (4.2, 29.0, 4.2), paint("#d6a238", noise=3), skip=())
    m.box((-3.8, 28.4, -5.2), (3.8, 29.0, -3.9), cap, skip=())
    m.box((-0.9, 29.2, -4.4), (0.9, 30.4, -4.1), metal("#d6a238"), skip=())
    m.box((5.4, 2.0, -3.6), (6.0, 24.0, -3.0), planks("#8a6038", 1.4, True), skip=())
    m.box((5.5, 18.0, -8.4), (5.9, 23.4, -3.2), P(paint("#2f9e44", noise=4), ov_stripe("#f4f0e6", 0.5, 0.8, True)), skip=())
    return m


def all_npcs():
    return [farmer(), rancher(), builder(), mechanic(), pilot(), conductor()]
