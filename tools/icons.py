import math
import random
from PIL import Image, ImageDraw, ImageFilter
from lib import rgb, clamp, tint, lerp

S = 32
SS = 8


class Canvas:
    def __init__(self):
        self.img = Image.new("RGBA", (S * SS, S * SS), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.img)

    def poly(self, pts, fill):
        self.d.polygon([(x * SS, y * SS) for x, y in pts], fill=rgb(fill) + (255,))

    def line(self, a, b, width, fill):
        self.d.line([(a[0] * SS, a[1] * SS), (b[0] * SS, b[1] * SS)], fill=rgb(fill) + (255,), width=int(width * SS))

    def rect(self, x0, y0, x1, y1, fill):
        self.d.rectangle([x0 * SS, y0 * SS, x1 * SS - 1, y1 * SS - 1], fill=rgb(fill) + (255,))

    def ellipse(self, x0, y0, x1, y1, fill):
        self.d.ellipse([x0 * SS, y0 * SS, x1 * SS - 1, y1 * SS - 1], fill=rgb(fill) + (255,))

    def layer(self):
        return Canvas()

    def comp(self, other):
        self.img.alpha_composite(other.img)
        self.d = ImageDraw.Draw(self.img)

    def finish(self, seed=0, outline="#1d1a17", light=1.18, dark=0.78, noise=5):
        small = self.img.resize((S, S), Image.BOX)
        px = small.load()
        for y in range(S):
            for x in range(S):
                r, g, b, a = px[x, y]
                px[x, y] = (r, g, b, 255 if a >= 110 else 0)
        rng = random.Random(seed)
        out = Image.new("RGBA", (S, S), (0, 0, 0, 0))
        op = out.load()

        def opaque(x, y):
            return 0 <= x < S and 0 <= y < S and px[x, y][3] > 0

        for y in range(S):
            for x in range(S):
                if px[x, y][3] > 0:
                    r, g, b, a = px[x, y]
                    k = 1.0
                    if not opaque(x - 1, y) or not opaque(x, y - 1):
                        k = light
                    elif not opaque(x + 1, y) or not opaque(x, y + 1):
                        k = dark
                    n = rng.uniform(-noise, noise)
                    op[x, y] = (clamp(r * k + n), clamp(g * k + n), clamp(b * k + n), 255)
        oc = rgb(outline)
        for y in range(S):
            for x in range(S):
                if px[x, y][3] == 0 and any(opaque(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    op[x, y] = oc + (255,)
        return out


def grad_poly(c, pts, c1, c2, vertical=True):
    pass


def hoe():
    c = Canvas()
    c.line((5, 28), (23, 10), 2.6, "#7a5230")
    c.line((5.8, 27.2), (22.2, 10.8), 1.0, "#9a6b3f")
    c.line((4.6, 29.2), (8, 25.6), 2.8, "#3b2a1c")
    c.poly([(17, 9), (21.5, 4.5), (28, 4), (29.5, 7), (25, 9.5), (22, 13.5)], "#8e9196")
    c.poly([(19, 8.5), (22, 5.5), (27.5, 5.2), (24.5, 8.2)], "#b2b5ba")
    c.poly([(20, 11), (22.5, 12.5), (21.5, 14.5), (18, 12.5)], "#6c6f74")
    c.line((20.5, 12), (23.5, 9), 1.4, "#4f4a44")
    c.line((20, 9.4), (22.4, 7), 0.8, "#c9ccd0")
    return c.finish(1)


def sickle():
    c = Canvas()
    c.line((7, 29), (13, 18), 2.8, "#7a5230")
    c.line((7.8, 28.4), (12.8, 19), 1.0, "#a06f40")
    c.line((6.2, 30), (8.6, 25.4), 3.0, "#3b2a1c")
    c.line((12.5, 18.4), (14.2, 16), 3.2, "#8a8d91")
    outer, inner, shine = [], [], []
    n = 16
    for i in range(n + 1):
        t = i / n
        th = math.radians(168 - 140 * t)
        th_t = 3.9 * (1 - t) ** 0.55 + 0.2
        cx, cy = 21, 19
        outer.append((cx + 12 * math.cos(th), cy - 12 * math.sin(th)))
        inner.append((cx + (12 - th_t) * math.cos(th), cy - (12 - th_t) * math.sin(th)))
        shine.append((cx + (12 - th_t * 0.25) * math.cos(th), cy - (12 - th_t * 0.25) * math.sin(th)))
    c.poly(outer + inner[::-1], "#9a9da2")
    c.poly(outer + shine[::-1], "#d3d6db")
    return c.finish(2)


def seed_pouch():
    c = Canvas()
    c.poly([(8, 12), (24, 12), (27, 28), (5, 28)], "#a9794a")
    c.poly([(8.5, 12.5), (14, 12.5), (13, 28), (5.6, 28)], "#c08d5b")
    c.poly([(11, 8), (21, 8), (24, 12), (8, 12)], "#8f6439")
    c.ellipse(8.5, 6, 23.5, 11, "#7a5230")
    c.rect(9, 11, 23, 13, "#5a3d22")
    c.line((9, 12), (23, 12), 1.0, "#d9a83a")
    c.ellipse(14.5, 11, 17.5, 14, "#d9a83a")
    c.line((16, 13.5), (13, 17), 0.8, "#d9a83a")
    c.line((16, 13.5), (19, 17), 0.8, "#d9a83a")
    for i, (x, y) in enumerate(((11, 3), (14, 1.6), (17, 2.6), (20, 1.8), (13, 4.6), (19, 4.4), (16, 3.4))):
        c.ellipse(x - 1, y - 0.5, x + 1, y + 0.9, "#e3c565" if i % 2 else "#c9962f")
    c.poly([(9, 20), (23, 20), (24, 22), (8.4, 22)], "#6b4423")
    c.rect(14.5, 18.5, 17.5, 23.5, "#d9a83a")
    return c.finish(3)


def watering_can():
    c = Canvas()
    c.poly([(7, 13), (21, 13), (22, 27), (6, 27)], "#4f7fb8")
    c.poly([(8, 14), (12, 14), (11.5, 26), (7, 26)], "#7ba7d8")
    c.rect(6, 12, 22, 14, "#6c9bd2")
    c.rect(5.5, 25.5, 22.5, 28, "#37608f")
    c.line((20, 17), (28, 7), 2.0, "#4f7fb8")
    c.line((20.2, 16.4), (27.4, 7.4), 0.8, "#7ba7d8")
    c.poly([(26, 4), (31, 7), (30, 9.5), (25, 7)], "#8e9196")
    for i in range(4):
        c.rect(27.2 + i * 0.5, 9.6 + i * 0.8, 28.0 + i * 0.5, 11.2 + i * 0.8, "#6fb4ee")
    c.poly([(7, 13), (7.5, 8), (10, 6), (14, 6), (17, 8)], "#4f7fb8")
    c.line((7.5, 12.5), (9, 6.8), 1.6, "#8a5a30")
    c.line((9, 6.8), (15, 6), 1.6, "#8a5a30")
    c.ellipse(11, 14.5, 17, 20.5, "#d9a83a")
    c.ellipse(12.2, 15.7, 15.8, 19.3, "#f2cf6a")
    c.line((14, 16), (14, 19), 0.6, "#8a6a1c")
    return c.finish(4)


def icon_expand():
    c = Canvas()
    c.poly([(3, 10), (17, 5), (30, 11), (16, 18)], "#6bbf4a")
    c.poly([(3, 10), (16, 18), (16, 24), (3, 16)], "#8a5a30")
    c.poly([(16, 18), (30, 11), (30, 17), (16, 24)], "#6e4524")
    for i in range(4):
        t = i / 4
        x0, y0 = 5 + 3 * i, 11 + 1.8 * i - 0.1
        c.line((x0 + 1, y0 - 1.5), (x0 + 13, y0 - 6.4 + 0), 0.7, "#3f8f3a")
    c.line((3, 10), (17, 5), 0.8, "#c9962f")
    c.line((17, 5), (30, 11), 0.8, "#c9962f")
    c.poly([(23, 3), (30, 3), (30, 10), (28, 8), (25, 11), (22.5, 8.5), (25.5, 5.5), (23, 3)], "#f2b134")
    return c.finish(5)


def icon_tasks():
    c = Canvas()
    c.rect(6, 4, 26, 29, "#8a5a30")
    c.rect(7.5, 6, 24.5, 28, "#f1e6c8")
    c.rect(11, 2, 21, 7, "#8e9196")
    c.ellipse(14.5, 3, 17.5, 6, "#2d2f33")
    for i in range(3):
        y = 10 + i * 6
        c.rect(9.5, y, 12.5, y + 3, "#d9cfae")
        c.line((9.8, y + 1.6), (11, y + 2.8), 0.7, "#3f9a3a")
        c.line((11, y + 2.8), (13.4, y - 0.8), 0.7, "#3f9a3a")
        c.rect(14.5, y + 1, 22.5, y + 2.2, "#7a6a4a")
    return c.finish(6)


def icon_market():
    c = Canvas()
    c.rect(4, 21, 28, 29, "#8a5a30")
    c.rect(5, 22, 27, 28, "#a9794a")
    c.line((4, 25), (28, 25), 0.7, "#6e4524")
    for i, h in enumerate((6, 9, 12, 16)):
        c.rect(6 + i * 5.5, 20 - h, 10.5 + i * 5.5, 21, "#6bbf4a" if i < 3 else "#f2b134")
    c.line((6, 13), (12, 10), 0.8, "#3f8f3a")
    c.line((12, 10), (17, 8), 0.8, "#3f8f3a")
    c.poly([(21, 3), (27, 3), (27, 9), (25, 7), (21, 11), (19.5, 9.5), (23.5, 5.5)], "#f2b134")
    return c.finish(7)


def icon_livestock():
    c = Canvas()
    c.poly([(4, 15), (16, 5), (28, 15), (28, 29), (4, 29)], "#b8312a")
    c.poly([(2, 16), (16, 3.5), (30, 16), (28, 17), (16, 6.5), (4, 17)], "#e8e8e4")
    c.rect(10, 17, 22, 29, "#f1ede0")
    c.rect(11.2, 18.2, 20.8, 28, "#b8312a")
    c.line((11.2, 18.2), (20.8, 28), 1.0, "#f1ede0")
    c.line((20.8, 18.2), (11.2, 28), 1.0, "#f1ede0")
    c.rect(13.5, 10.5, 18.5, 14.5, "#f1ede0")
    c.rect(14.3, 11.3, 17.7, 13.7, "#2d2f33")
    c.rect(4, 28, 28, 30, "#5f4a2e")
    return c.finish(8)


def icon_coin():
    c = Canvas()
    c.ellipse(3, 3, 29, 29, "#d9a01e")
    c.ellipse(5, 5, 27, 27, "#f2c94c")
    c.ellipse(7.5, 7.5, 24.5, 24.5, "#e0a81f")
    c.line((16, 22), (16, 10), 1.2, "#8a5a10")
    for i in range(3):
        y = 12 + i * 3.2
        c.poly([(16, y), (11.5, y - 3), (11.5, y - 1), (16, y + 1.6)], "#8a5a10")
        c.poly([(16, y), (20.5, y - 3), (20.5, y - 1), (16, y + 1.6)], "#8a5a10")
    c.poly([(16, 6.4), (14.6, 9.6), (17.4, 9.6)], "#8a5a10")
    c.poly([(7, 12), (9.5, 7.5), (13, 6), (10.5, 9.5)], "#fff0b0")
    return c.finish(9)


def icon_cosmetics():
    c = Canvas()
    c.ellipse(3, 15, 29, 25, "#c9a24a")
    c.ellipse(4.5, 15.5, 27.5, 22.5, "#e3c565")
    c.poly([(9, 18), (10, 9), (13, 6), (19, 6), (22, 9), (23, 18)], "#e3c565")
    c.poly([(10, 9), (13, 6), (19, 6), (22, 9), (20, 10.5), (12, 10.5)], "#f1d98a")
    c.poly([(9, 16.5), (23, 16.5), (23.4, 19), (8.6, 19)], "#b3322a")
    c.ellipse(15, 14.4, 17.6, 17, "#f2b134")
    for (x, y, r) in ((5, 7, 2.4), (27, 5, 2.0), (26, 27, 1.8)):
        c.poly([(x, y - r * 1.6), (x + r * 0.5, y - r * 0.5), (x + r * 1.6, y), (x + r * 0.5, y + r * 0.5), (x, y + r * 1.6), (x - r * 0.5, y + r * 0.5), (x - r * 1.6, y), (x - r * 0.5, y - r * 0.5)], "#fff0b0")
    return c.finish(10)


def item_flour():
    c = Canvas()
    c.poly([(7, 10), (25, 10), (27, 28), (5, 28)], "#efe6cf")
    c.poly([(8, 10.5), (13, 10.5), (12, 28), (5.8, 28)], "#faf4e2")
    c.poly([(9, 5), (23, 5), (25, 10), (7, 10)], "#d8cdb0")
    c.rect(8, 9, 24, 11, "#b89a58")
    c.ellipse(11, 14, 21, 24, "#c9b87a")
    c.line((16, 22.5), (16, 15), 0.8, "#8a6a1c")
    for k in range(3):
        y = 16 + k * 2.2
        c.poly([(16, y), (13, y - 2), (13, y - 0.6), (16, y + 1.2)], "#8a6a1c")
        c.poly([(16, y), (19, y - 2), (19, y - 0.6), (16, y + 1.2)], "#8a6a1c")
    return c.finish(11)


def item_loaf():
    c = Canvas()
    c.ellipse(3, 9, 29, 26, "#a8652a")
    c.ellipse(4.5, 9.5, 27.5, 23.5, "#d4893a")
    c.ellipse(7, 11, 20, 18, "#e8a85a")
    for x in (9, 14, 19, 24):
        c.line((x, 12), (x - 2.4, 20), 1.2, "#8a4a1c")
    c.rect(4, 24, 28, 27, "#7a4416")
    return c.finish(12)


def icon_buildings():
    c = Canvas()
    c.rect(5, 15, 27, 29, "#f2eee2")
    c.rect(5, 26, 27, 29, "#8c8f94")
    c.poly([(2, 16), (16, 4), (30, 16), (27, 17), (16, 8), (5, 17)], "#a63a2c")
    c.poly([(7, 15), (16, 7), (25, 15)], "#d6584a")
    c.rect(13, 20, 19, 29, "#7a5230")
    c.rect(7, 18, 11, 22, "#7ba7d8")
    c.rect(21, 18, 25, 22, "#7ba7d8")
    c.rect(22, 5, 25, 12, "#a8503a")
    c.line((24, 25), (30, 19), 1.3, "#7a5230")
    c.rect(27, 16, 31, 20, "#8e9196")
    return c.finish(13)


ICONS = {
    "stone_hoe": hoe,
    "stone_sickle": sickle,
    "stone_seed_pouch": seed_pouch,
    "stone_watering_can": watering_can,
    "icon_expand": icon_expand,
    "icon_tasks": icon_tasks,
    "icon_market": icon_market,
    "icon_livestock": icon_livestock,
    "icon_coin": icon_coin,
    "icon_cosmetics": icon_cosmetics,
    "item_flour": item_flour,
    "item_loaf": item_loaf,
    "icon_buildings": icon_buildings,
}

HANDHELD = {"stone_hoe", "stone_sickle", "stone_watering_can"}
