import math
import random
import zlib
from PIL import Image, ImageDraw, ImageFont

DENSITY = 2
FACES = ("north", "south", "east", "west", "up", "down")


def clamp(v):
    return 0 if v < 0 else 255 if v > 255 else int(v)


def rgb(h):
    if not isinstance(h, str):
        return tuple(h[:3])
    h = h.lstrip("#")
    if len(h) == 3:
        h = "".join(ch * 2 for ch in h)
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def tint(c, f):
    return tuple(clamp(x * f) for x in rgb(c))


def lerp(a, b, t):
    a, b = rgb(a), rgb(b)
    return tuple(clamp(a[i] + (b[i] - a[i]) * t) for i in range(3))


class Ctx:
    def __init__(self, pw, ph, w, h, face, rng):
        self.pw, self.ph, self.w, self.h, self.face, self.rng = pw, ph, w, h, face, rng

    def X(self, v):
        return int(round(v * DENSITY))


def vnoise(pw, ph, cell, rng):
    gw, gh = pw // cell + 3, ph // cell + 3
    g = [[rng.random() for _ in range(gw)] for _ in range(gh)]
    out = [[0.0] * pw for _ in range(ph)]
    for y in range(ph):
        fy = y / cell
        iy = int(fy)
        ty = fy - iy
        for x in range(pw):
            fx = x / cell
            ix = int(fx)
            tx = fx - ix
            a = g[iy][ix] * (1 - tx) + g[iy][ix + 1] * tx
            b = g[iy + 1][ix] * (1 - tx) + g[iy + 1][ix + 1] * tx
            out[y][x] = a * (1 - ty) + b * ty
    return out


def paint(color, noise=6, grad=0.12, bevel=0.14, alpha=255):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        for y in range(ctx.ph):
            g = 1 + grad * (1 - 2 * (y + 0.5) / ctx.ph)
            for x in range(ctx.pw):
                n = ctx.rng.uniform(-noise, noise)
                k = g
                if ctx.pw > 3 and ctx.ph > 3:
                    if x == 0 or y == 0:
                        k *= 1 + bevel
                    elif x == ctx.pw - 1 or y == ctx.ph - 1:
                        k *= 1 - bevel
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), alpha)
        return img

    return f


def metal(color, streak=5, **kw):
    base = paint(color, **kw)

    def f(ctx):
        img = base(ctx)
        px = img.load()
        for y in range(ctx.ph):
            o = ctx.rng.uniform(-streak, streak)
            for x in range(ctx.pw):
                r, g, b, a = px[x, y]
                px[x, y] = (clamp(r + o), clamp(g + o), clamp(b + o), a)
        return img

    return f


def planks(color, plank=3, vertical=False, dark=0.55, vary=0.12):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        pl = max(2, int(plank * DENSITY))
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                a, b = (x, y) if vertical else (y, x)
                idx = a // pl
                pr = random.Random(idx * 977 + ctx.pw)
                k = 1 + pr.uniform(-vary, vary)
                grain = math.sin(b * 0.55 + idx * 1.7 + pr.random() * 6) * 0.045 + ctx.rng.uniform(-0.03, 0.03)
                k += grain
                if a % pl == pl - 1:
                    k *= dark
                elif a % pl == 0:
                    k *= 1.08
                px[x, y] = (clamp(c[0] * k), clamp(c[1] * k), clamp(c[2] * k), 255)
        return img

    return f


def rubber(color="#232323"):
    return paint(color, noise=4, grad=0.05, bevel=0.1)


def lugs(color="#1c1c1c", period=3.0):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        p = max(3, int(period * DENSITY))
        mid = ctx.pw / 2
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                v = (y + int(abs(x - mid))) % p
                k = 0.62 if v < p * 0.4 else 1.08
                n = ctx.rng.uniform(-3, 3)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


def wheel_side(tire="#202020", rim="#d6a21f", hub="#8a8a8a", bolt="#2b2b2b", rimr=0.66, hubr=0.3):
    t, r, h, b = rgb(tire), rgb(rim), rgb(hub), rgb(bolt)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        R = ctx.h / 2 if ctx.h > ctx.w else ctx.w / 2
        R = max(ctx.w, ctx.h) / 2
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                dx = (x + 0.5) / DENSITY - ctx.w / 2
                dy = (y + 0.5) / DENSITY - ctx.h / 2
                rr = math.hypot(dx, dy) / R
                ang = math.atan2(dy, dx)
                n = ctx.rng.uniform(-3, 3)
                if rr < hubr:
                    col = h
                    k = 1.1 - rr
                    if rr > hubr * 0.45 and abs(math.sin(ang * 4)) > 0.93:
                        col = b
                        k = 1.0
                    elif rr < hubr * 0.3:
                        col = b
                        k = 1.0
                elif rr < rimr:
                    col = r
                    k = 1.15 - 0.45 * (rr - hubr) / (rimr - hubr)
                    if abs(rr - (hubr + rimr) / 2) < 0.03:
                        k *= 0.7
                else:
                    col = t
                    k = 1.0 + (0.15 if (rr - rimr) < 0.05 else 0)
                    if abs((rr - rimr) / (1 - rimr) - 0.5) < 0.09:
                        k *= 1.25
                px[x, y] = (clamp(col[0] * k + n), clamp(col[1] * k + n), clamp(col[2] * k + n), 255)
        return img

    return f


def glass(color="#9fd4ee", alpha=120):
    c = rgb(color)
    solid = alpha >= 180

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph), (0, 0, 0, 0))
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                edge = x in (0, ctx.pw - 1) or y in (0, ctx.ph - 1)
                d = (x + y * 0.6) % 14
                glint = d < 1.6
                if edge:
                    px[x, y] = (clamp(c[0] * 0.5), clamp(c[1] * 0.5), clamp(c[2] * 0.5), 255)
                elif solid:
                    k = 1.0 - 0.18 * (y / max(1, ctx.ph))
                    if glint:
                        k = 1.28
                    px[x, y] = (clamp(c[0] * k * 0.85), clamp(c[1] * k * 0.9), clamp(c[2] * k), 255)
                elif glint:
                    px[x, y] = (clamp(c[0] * 1.2), clamp(c[1] * 1.2), clamp(c[2] * 1.25), 255)
        return img

    return f


def light(color="#ffe9a0"):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                dx = (x + 0.5) / ctx.pw - 0.5
                dy = (y + 0.5) / ctx.ph - 0.5
                k = 1.15 - 0.9 * math.hypot(dx, dy)
                px[x, y] = (clamp(c[0] * k + 25), clamp(c[1] * k + 25), clamp(c[2] * k + 10), 255)
        return img

    return f


def diamond(color="#6e7075"):
    base = paint(color, noise=3)

    def f(ctx):
        img = base(ctx)
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                if (x + y) % 4 == 0 or (x - y) % 4 == 0:
                    r, g, b, a = px[x, y]
                    k = 1.22 if (x + y) % 8 < 4 else 0.82
                    px[x, y] = (clamp(r * k), clamp(g * k), clamp(b * k), a)
        return img

    return f


def hazard(c1="#e8b81a", c2="#1e1e1e", period=3):
    a, b = rgb(c1), rgb(c2)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        p = period * DENSITY
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                c = a if ((x + y) // p) % 2 == 0 else b
                n = ctx.rng.uniform(-3, 3)
                px[x, y] = (clamp(c[0] + n), clamp(c[1] + n), clamp(c[2] + n), 255)
        return img

    return f


def cloth(color, weave=2, noise=5):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                k = 1.06 if (x // weave + y // weave) % 2 == 0 else 0.94
                n = ctx.rng.uniform(-noise, noise)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


def plaid(c1, c2, size=2.0):
    a, b = rgb(c1), rgb(c2)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        s = max(2, int(size * DENSITY))
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                vx = (x // s) % 2
                vy = (y // s) % 2
                if vx and vy:
                    c = tint(a, 0.7)
                elif vx or vy:
                    c = lerp(a, b, 0.5)
                else:
                    c = b
                n = ctx.rng.uniform(-4, 4)
                px[x, y] = (clamp(c[0] + n), clamp(c[1] + n), clamp(c[2] + n), 255)
        return img

    return f


def fur(base, spot=None, cell=4, thr=0.55, noise=5, spot_noise=4):
    cb = rgb(base)
    cs = rgb(spot) if spot else None

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        vn = vnoise(ctx.pw, ctx.ph, max(2, cell * DENSITY // 2), random.Random(ctx.pw * 31 + ctx.ph * 7 + zlib.crc32(ctx.face.encode()) % 997 + 11)) if spot else None
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                c = cb
                if spot and vn[y][x] > thr:
                    c = cs
                n = ctx.rng.uniform(-noise, noise)
                px[x, y] = (clamp(c[0] + n), clamp(c[1] + n), clamp(c[2] + n), 255)
        return img

    return f


def wool(color="#f3efe4", dark="#cfc8b6"):
    a, b = rgb(color), rgb(dark)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        v1 = vnoise(ctx.pw, ctx.ph, 2, ctx.rng)
        v2 = vnoise(ctx.pw, ctx.ph, 4, ctx.rng)
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                t = v1[y][x] * 0.6 + v2[y][x] * 0.4
                c = lerp(b, a, min(1, max(0, (t - 0.25) * 1.9)))
                px[x, y] = (c[0], c[1], c[2], 255)
        return img

    return f


def curly(light="#f6f2e6", dark="#bdb49c", cell=3.0, noise=3):
    a, b = rgb(light), rgb(dark)

    def f(ctx):
        c = max(3, int(cell * DENSITY))
        gw, gh = ctx.pw // c + 3, ctx.ph // c + 3
        pts = {}
        for gy in range(-1, gh):
            for gx in range(-1, gw):
                pts[(gx, gy)] = (gx * c + ctx.rng.uniform(0.15, 0.85) * c, gy * c + ctx.rng.uniform(0.15, 0.85) * c)
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                gx, gy = x // c, y // c
                best = 1e9
                for oy in (-1, 0, 1):
                    for ox in (-1, 0, 1):
                        p = pts[(gx + ox, gy + oy)]
                        d = math.hypot(x + 0.5 - p[0], y + 0.5 - p[1])
                        if d < best:
                            best = d
                t = min(1.0, best / (c * 0.78))
                k = 1.0 - t ** 1.15
                col = lerp(b, a, k)
                if t < 0.28:
                    col = lerp(col, (255, 255, 255), 0.35)
                n = ctx.rng.uniform(-noise, noise)
                px[x, y] = (clamp(col[0] + n), clamp(col[1] + n), clamp(col[2] + n), 255)
        return img

    return f


def feathers(base="#f6f2ea", dark="#d9d1c0"):
    a, b = rgb(base), rgb(dark)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                row = y // 2
                xx = x + (row % 2) * 1
                k = (xx % 3 == 2) or (y % 2 == 1 and (xx % 3 == 1))
                c = lerp(a, b, 0.55 if k else 0.0)
                n = ctx.rng.uniform(-4, 4)
                px[x, y] = (clamp(c[0] + n), clamp(c[1] + n), clamp(c[2] + n), 255)
        return img

    return f


def burlap(color="#b69a68"):
    return cloth(color, weave=1, noise=9)


def straw(color="#e3c565"):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                k = 1.0 + 0.1 * math.sin(x * 1.3 + (y // 2) * 2.1) + ctx.rng.uniform(-0.06, 0.06)
                if (x + y) % 5 == 0:
                    k *= 0.8
                px[x, y] = (clamp(c[0] * k), clamp(c[1] * k), clamp(c[2] * k), 255)
        return img

    return f


def grille(frame="#bcbcbc", slat="#1b1b1b", slats=5):
    fr, sl = rgb(frame), rgb(slat)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                edge = x < 2 or y < 2 or x >= ctx.pw - 2 or y >= ctx.ph - 2
                if edge:
                    c = fr
                else:
                    inner = (y - 2) / max(1, ctx.ph - 4)
                    c = sl if int(inner * slats * 2) % 2 == 0 else lerp(fr, sl, 0.55)
                n = ctx.rng.uniform(-3, 3)
                px[x, y] = (clamp(c[0] + n), clamp(c[1] + n), clamp(c[2] + n), 255)
        return img

    return f


def P(base, *ovs):
    def f(ctx):
        img = base(ctx)
        for ov in ovs:
            ov(img, ctx)
        return img

    return f


def ov_stripe(color, pos=0.5, width=1.5, vertical=True):
    c = rgb(color)

    def f(img, ctx):
        px = img.load()
        wpx = max(1, int(width * DENSITY))
        if vertical:
            x0 = int(pos * ctx.pw - wpx / 2)
            for x in range(max(0, x0), min(ctx.pw, x0 + wpx)):
                for y in range(ctx.ph):
                    px[x, y] = (c[0], c[1], c[2], 255)
        else:
            y0 = int(pos * ctx.ph - wpx / 2)
            for y in range(max(0, y0), min(ctx.ph, y0 + wpx)):
                for x in range(ctx.pw):
                    px[x, y] = (c[0], c[1], c[2], 255)

    return f


def ov_rect(color, x, y, w, h, alpha=255):
    c = rgb(color)

    def f(img, ctx):
        d = ImageDraw.Draw(img)
        d.rectangle([ctx.X(x), ctx.X(y), ctx.X(x + w) - 1, ctx.X(y + h) - 1], fill=c + (alpha,))

    return f


def ov_frame(color, t=1.0):
    c = rgb(color)

    def f(img, ctx):
        d = ImageDraw.Draw(img)
        n = max(1, int(t * DENSITY))
        for i in range(n):
            d.rectangle([i, i, ctx.pw - 1 - i, ctx.ph - 1 - i], outline=c + (255,))

    return f


def ov_vents(color="#1d1d1d", n=4, margin=1.5):
    c = rgb(color)

    def f(img, ctx):
        d = ImageDraw.Draw(img)
        m = ctx.X(margin)
        span = ctx.ph - 2 * m
        for i in range(n):
            y = m + int(span * (i + 0.5) / n)
            d.line([m, y, ctx.pw - 1 - m, y], fill=c + (255,))
            if DENSITY > 1:
                d.line([m, y + 1, ctx.pw - 1 - m, y + 1], fill=c + (255,))

    return f


def ov_dots(color, step=4, margin=1):
    c = rgb(color)

    def f(img, ctx):
        px = img.load()
        s = ctx.X(step)
        m = ctx.X(margin)
        for y in range(m, ctx.ph - m + 1, max(1, s)):
            for x in range(m, ctx.pw - m + 1, max(1, s)):
                if x < ctx.pw and y < ctx.ph:
                    px[x, y] = c + (255,)

    return f


FONT_3X5 = {
    "A": "010101111101101", "B": "110101110101110", "C": "011100100100011", "D": "110101101101110", "E": "111100110100111",
    "F": "111100110100100", "G": "011100101101011", "H": "101101111101101", "I": "111010010010111", "J": "001001001101010",
    "K": "101101110101101", "L": "100100100100111", "M": "101111111101101", "N": "110101101101101", "O": "010101101101010",
    "P": "110101110100100", "Q": "010101101111011", "R": "110101110101101", "S": "011100010001110", "T": "111010010010010",
    "U": "101101101101111", "V": "101101101101010", "W": "101101111111101", "X": "101101010101101", "Y": "101101010010010",
    "Z": "111001010100111", "0": "111101101101111", "1": "010110010010111", "2": "110001010100111", "3": "110001010001110",
    "4": "101101111001001", "5": "111100110001110", "6": "011100110101010", "7": "111001010010010", "8": "010101010101010",
    "9": "010101011001110", "-": "000000111000000", ".": "000000000000010", "!": "010010010000010", ":": "000010000010000", " ": "000000000000000",
}


def pixel_text(layer_px, lines, pw, ph, scale):
    rows = len(lines)
    block_h = rows * 5 * scale + (rows - 1) * scale
    y0 = (ph - block_h) // 2
    for r, line in enumerate(lines):
        line = line.upper()
        width = len(line) * 4 * scale - scale
        x0 = (pw - width) // 2
        for i, ch in enumerate(line):
            glyph = FONT_3X5.get(ch, FONT_3X5[" "])
            for gy in range(5):
                for gx in range(3):
                    if glyph[gy * 3 + gx] == "1":
                        for dy in range(scale):
                            for dx in range(scale):
                                xx = x0 + i * 4 * scale + gx * scale + dx
                                yy = y0 + r * 6 * scale + gy * scale + dy
                                if 0 <= xx < pw and 0 <= yy < ph:
                                    layer_px[xx, yy] = 255


def ov_text(txt, color="#f0f0f0", size=7, x=None, y=None, alpha=255):
    c = rgb(color)
    lines = txt.split("\n")

    def f(img, ctx):
        layer = Image.new("L", (ctx.pw, ctx.ph), 0)
        longest = max(len(l) for l in lines)
        need_w = longest * 4 - 1
        need_h = len(lines) * 6 - 1
        scale = min((ctx.pw - 2) // need_w, (ctx.ph - 2) // need_h)
        if x is None and y is None and scale >= 1:
            pixel_text(layer.load(), lines, ctx.pw, ctx.ph, scale)
        else:
            font = ImageFont.load_default(size=size)
            d = ImageDraw.Draw(layer)
            bb = d.textbbox((0, 0), txt, font=font)
            tw, th = bb[2] - bb[0], bb[3] - bb[1]
            tx = (ctx.pw - tw) // 2 - bb[0] if x is None else ctx.X(x)
            ty = (ctx.ph - th) // 2 - bb[1] if y is None else ctx.X(y)
            d.text((tx, ty), txt, font=font, fill=255)
        px = img.load()
        lp = layer.load()
        for yy in range(ctx.ph):
            for xx in range(ctx.pw):
                if lp[xx, yy] > 110:
                    px[xx, yy] = c + (alpha,)

    return f


def ov_draw(fn):
    def f(img, ctx):
        fn(ImageDraw.Draw(img), ctx, img)

    return f


def ov_shadow(strength=0.35):
    def f(img, ctx):
        px = img.load()
        for y in range(ctx.ph):
            k = 1 - strength * max(0, (y / ctx.ph - 0.65) / 0.35)
            for x in range(ctx.pw):
                r, g, b, a = px[x, y]
                px[x, y] = (clamp(r * k), clamp(g * k), clamp(b * k), a)

    return f


def pack_rects(sizes, W):
    order = sorted(range(len(sizes)), key=lambda i: -sizes[i][1])
    pos = {}
    x = y = row_h = 0
    for i in order:
        w, h = sizes[i]
        if w > W:
            return None
        if x + w > W:
            x = 0
            y += row_h
            row_h = 0
        pos[i] = (x, y)
        x += w
        row_h = max(row_h, h)
    return pos, y + row_h


class Model:
    def __init__(self, name, seed=1):
        self.name = name
        self.seed = seed
        self.els = []
        self.reqs = []
        self.parts = []
        self.cur = "body"
        self.wheel_groups = []
        self.k = 1.0

    def p(self, name):
        self.cur = name

    def box(self, a, b, mat, rot=None, skip=("down",), label=""):
        x0, y0, z0 = a
        x1, y1, z1 = b
        if x1 < x0:
            x0, x1 = x1, x0
        if y1 < y0:
            y0, y1 = y1, y0
        if z1 < z0:
            z0, z1 = z1, z0
        dx, dy, dz = x1 - x0, y1 - y0, z1 - z0
        idx = len(self.els)
        el = {
            "name": label or f"b{idx}",
            "from": [round(x0 + 8, 3), round(y0, 3), round(z0 + 8, 3)],
            "to": [round(x1 + 8, 3), round(y1, 3), round(z1 + 8, 3)],
            "faces": {},
        }
        if rot:
            axis, ang = rot[0], rot[1]
            origin = rot[2] if len(rot) > 2 else ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2)
            el["rotation"] = {"angle": -ang, "axis": axis, "origin": [round(origin[0] + 8, 3), round(origin[1], 3), round(origin[2] + 8, 3)]}
        dims = {"north": (dx, dy), "south": (dx, dy), "east": (dz, dy), "west": (dz, dy), "up": (dx, dz), "down": (dx, dz)}
        for f in FACES:
            if f in skip:
                continue
            painter = self._pick(mat, f)
            w, h = dims[f]
            pw = max(1, int(round(w * DENSITY)))
            ph = max(1, int(round(h * DENSITY)))
            self.reqs.append((idx, f, pw, ph, w, h, painter))
        self.els.append(el)
        self.parts.append(self.cur)
        return el

    def _pick(self, mat, f):
        if callable(mat):
            return mat
        if f in mat:
            return mat[f]
        if f in ("north", "south", "east", "west") and "sides" in mat:
            return mat["sides"]
        if f in ("up", "down") and "caps" in mat:
            return mat["caps"]
        return mat["all"]

    def finalize(self):
        sizes = [(r[2] + 2, r[3] + 2) for r in self.reqs]
        W = 64
        while True:
            res = pack_rects(sizes, W)
            if res and res[1] <= W:
                break
            W *= 2
        pos, _ = res
        atlas = Image.new("RGBA", (W, W), (0, 0, 0, 0))
        for i, (idx, f, pw, ph, w, h, painter) in enumerate(self.reqs):
            rng = random.Random(zlib.crc32(f"{self.name}{idx}{f}".encode()))
            img = painter(Ctx(pw, ph, w, h, f, rng))
            x, y = pos[i]
            atlas.paste(img, (x + 1, y + 1))
            atlas.paste(img.crop((0, 0, pw, 1)), (x + 1, y))
            atlas.paste(img.crop((0, ph - 1, pw, ph)), (x + 1, y + ph + 1))
            atlas.paste(img.crop((0, 0, 1, ph)), (x, y + 1))
            atlas.paste(img.crop((pw - 1, 0, pw, ph)), (x + pw + 1, y + 1))
            self.els[idx]["faces"][f] = {
                "uv": [round((x + 1) / W * 16, 5), round((y + 1) / W * 16, 5), round((x + 1 + pw) / W * 16, 5), round((y + 1 + ph) / W * 16, 5)],
                "texture": "#0",
            }
        for el in self.els:
            for v in el["from"] + el["to"]:
                assert -16 <= v <= 32, (self.name, el["name"], v)
        self.atlas = atlas
        self.zfix()
        return atlas, self.els

    def zfix(self, eps=0.03):
        n = len(self.els)
        info = []
        for e in self.els:
            info.append(None if "rotation" in e else (e["from"], e["to"]))
        axes = {"north": (2, -1), "south": (2, 1), "west": (0, -1), "east": (0, 1), "down": (1, -1), "up": (1, 1)}
        fixed = 0
        for i in range(n):
            if info[i] is None:
                continue
            for j in range(i + 1, n):
                if info[j] is None:
                    continue
                A, B = self.els[i], self.els[j]
                for d, (ax, sg) in axes.items():
                    if d not in A["faces"] or d not in B["faces"]:
                        continue
                    pa = A["to"][ax] if sg > 0 else A["from"][ax]
                    pb = B["to"][ax] if sg > 0 else B["from"][ax]
                    if abs(pa - pb) > 0.002:
                        continue
                    o = [k for k in range(3) if k != ax]
                    ov = 1.0
                    for k in o:
                        lo = max(A["from"][k], B["from"][k])
                        hi = min(A["to"][k], B["to"][k])
                        if hi - lo <= 0.01:
                            ov = 0
                            break
                        ov *= hi - lo
                    if ov <= 0:
                        continue
                    areaA = 1.0
                    areaB = 1.0
                    for k in o:
                        areaA *= A["to"][k] - A["from"][k]
                        areaB *= B["to"][k] - B["from"][k]
                    tgt = B if areaB <= areaA else A
                    key = "to" if sg > 0 else "from"
                    tgt[key][ax] = round(tgt[key][ax] + sg * eps, 3)
                    fixed += 1
        self.zfixed = fixed

    def extents(self):
        xs = [e["from"][0] for e in self.els] + [e["to"][0] for e in self.els]
        ys = [e["from"][1] for e in self.els] + [e["to"][1] for e in self.els]
        zs = [e["from"][2] for e in self.els] + [e["to"][2] for e in self.els]
        return (min(xs), max(xs)), (min(ys), max(ys)), (min(zs), max(zs))


def oct_prism(m, axis, cx, cy, cz, r, length, mat):
    k = 0.4142 * r
    for i, (a, b, rot) in enumerate(((r, k, 0), (k, r, 0), (r, k, 45), (k, r, 45))):
        L = length - 0.03 * i
        if axis == "x":
            lo, hi = (cx - L / 2, cy - a, cz - b), (cx + L / 2, cy + a, cz + b)
        elif axis == "z":
            lo, hi = (cx - b, cy - a, cz - L / 2), (cx + b, cy + a, cz + L / 2)
        else:
            lo, hi = (cx - a, cy - L / 2, cz - b), (cx + a, cy + L / 2, cz + b)
        m.box(lo, hi, mat, rot=(axis, rot, (cx, cy, cz)) if rot else None, skip=())


def wheel(m, cx, cy, cz, r, w, tire="#202020", rim="#d6a21f", hub="#8a8a8a", lug=True):
    mat = {"east": wheel_side(tire, rim, hub), "west": wheel_side(tire, rim, hub), "all": lugs(tire) if lug else rubber(tire)}
    start = len(m.els)
    oct_prism(m, "x", cx, cy, cz, r, w, mat)
    m.wheel_groups.append(((cx, cy, cz, r), start, len(m.els)))


def cyl_x(m, cx, cy, cz, r, length, mat):
    oct_prism(m, "x", cx, cy, cz, r, length, mat)


def cyl_z(m, cx, cy, cz, r, length, mat):
    oct_prism(m, "z", cx, cy, cz, r, length, mat)


def cyl_y(m, cx, cy, cz, r, height, mat):
    oct_prism(m, "y", cx, cy + height / 2, cz, r, height, mat)
