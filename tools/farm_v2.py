"""Farm buildings v2: chicken coop (+ yard), windmill (+ sails part) and bakery, their ruins and
construction stages, plus a few flat item icons.

Standalone on purpose: build.py no longer matches the live pack, so this script never rebuilds the
whole pack. It only writes the models listed in MODELS / ICONS into an overlay folder that has the
same assets/harvestmc/... layout as the pack:

    python farm_v2.py <out pack folder>          (default: ../pack_v2)

The per-model pipeline mirrors build.py main(): finalize -> snap alpha to 0/255 -> atlas png ->
model json (textures, elements, display) -> item definition -> construction stages -> cull faces.
build.py's helpers (display_for, stage_models, cull_faces, item_def, write_json) are loaded from its
source with ast, without running its module-level main().

All buildings face north (front / door at -Z), floor at y=0, footprint centred on x=0, z=0 in model
coordinates (Model.box adds +8 on x/z). World size = model units / 16 * scale.
"""
import ast
import json
import math
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from PIL import Image, ImageDraw  # noqa: E402
from lib import *  # noqa: E402,F401
from lib import DENSITY, Model, P, paint, planks, light, glass, straw, burlap, cloth, metal, rgb, tint, lerp, clamp, cyl_y, oct_prism, vnoise  # noqa: E402
from bld import TRIM, mesh  # noqa: E402
from cosmetics import bricks  # noqa: E402
import icons  # noqa: E402


# --------------------------------------------------------------------------------------------
# build.py helpers, loaded without executing build.py's main()
# --------------------------------------------------------------------------------------------

def load_build_helpers(assets):
    src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {"write", "write_json", "item_def", "display_for", "cull_faces", "stage_models"}
    names = {"NS", "OPP", "AX", "STATS", "STAGES", "AXES"}
    keep = []
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name in funcs:
            keep.append(node)
        elif isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id in names for t in node.targets):
            keep.append(node)
    ns = {"os": os, "json": json, "math": math, "ASSETS": assets}
    exec(compile(ast.Module(body=keep, type_ignores=[]), os.path.join(HERE, "build.py"), "exec"), ns)
    return ns


# --------------------------------------------------------------------------------------------
# Model with optional higher-resolution faces
# --------------------------------------------------------------------------------------------

class M(Model):
    def box(self, a, b, mat, rot=None, skip=("down",), label="", hd=1):
        n0 = len(self.reqs)
        el = super().box(a, b, mat, rot, skip, label)
        if hd != 1:
            for i in range(n0, len(self.reqs)):
                idx, f, pw, ph, w, h, painter = self.reqs[i]
                self.reqs[i] = (idx, f, max(1, int(round(w * DENSITY * hd))), max(1, int(round(h * DENSITY * hd))), w, h, painter)
        return el

    def mark(self):
        return len(self.els)


# --------------------------------------------------------------------------------------------
# Materials
# --------------------------------------------------------------------------------------------

def _ppu(ctx):
    return ctx.pw / ctx.w if ctx.w > 1e-6 else DENSITY


def bnb(color, board=2.3):
    """Board and batten: wide vertical boards, narrow battens with a highlight and a shadow."""
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        bw = max(3, int(round(board * _ppu(ctx))))
        for y in range(ctx.ph):
            g = 1 + 0.07 * (1 - 2 * (y + 0.5) / ctx.ph)
            for x in range(ctx.pw):
                i, t = divmod(x, bw)
                pr = random.Random(i * 7919 + 13)
                k = g * (1 + pr.uniform(-0.06, 0.06))
                k += math.sin(y * 0.8 + i * 2.3 + pr.random() * 6) * 0.03 + ctx.rng.uniform(-0.035, 0.035)
                if t == 0:
                    k *= 1.18
                elif t == 1:
                    k *= 0.68
                px[x, y] = (clamp(c[0] * k), clamp(c[1] * k), clamp(c[2] * k), 255)
        return img

    return f


def shingles(color, row=1.5, tab=1.9, down="bottom", moss=None):
    """Staggered shingle courses; `down` says which image edge is downhill (shadow side of a course)."""
    c = rgb(color)
    mc = rgb(moss) if moss else None

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        rh = max(2, int(round(row * DENSITY)))
        tw = max(3, int(round(tab * DENSITY)))
        for y in range(ctx.ph):
            yy = y if down == "bottom" else ctx.ph - 1 - y
            r, t = divmod(yy, rh)
            off = (tw // 2) if r % 2 else 0
            for x in range(ctx.pw):
                idx, u = divmod(x + off + r * 3, tw)
                pr = random.Random(r * 977 + idx * 31 + 7)
                k = 1 + pr.uniform(-0.12, 0.10)
                col = c
                if mc and pr.random() < 0.12:
                    col = lerp(c, mc, 0.55)
                if t == rh - 1:
                    k *= 0.6
                elif t == 0:
                    k *= 1.12
                if u == tw - 1:
                    k *= 0.78
                n = ctx.rng.uniform(-4, 4)
                px[x, y] = (clamp(col[0] * k + n), clamp(col[1] * k + n), clamp(col[2] * k + n), 255)
        return img

    return f


def fieldstone(color="#9a958c", mortar="#5c574f", rh=1.9, bw=3.0):
    """Irregular coursed stone: varying stone widths, per-stone tint, darker rounded corners."""
    c, mo = rgb(color), rgb(mortar)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        rhp = max(3, int(round(rh * DENSITY)))
        for y in range(ctx.ph):
            row, ty = divmod(y, rhp)
            rr = random.Random(row * 131 + 5)
            edges = [0]
            while edges[-1] < ctx.pw + 8:
                edges.append(edges[-1] + max(3, int(rr.uniform(0.6, 1.5) * bw * DENSITY)))
            shift = rr.randint(0, 5)
            for x in range(ctx.pw):
                xx = x + shift
                j = 0
                while edges[j + 1] <= xx:
                    j += 1
                tx = xx - edges[j]
                wpx = edges[j + 1] - edges[j]
                if ty == rhp - 1 or tx == wpx - 1:
                    col, k = mo, 1.0
                else:
                    pr = random.Random(row * 733 + j * 17)
                    base = lerp(c, (c[0] * 0.8, c[1] * 0.86, c[2] * 0.95), pr.random() * 0.8)
                    col = base
                    k = 1 + pr.uniform(-0.1, 0.1)
                    corner = (tx in (0, wpx - 2)) and (ty in (0, rhp - 2))
                    if corner:
                        k *= 0.78
                    elif ty == 0:
                        k *= 1.12
                n = ctx.rng.uniform(-5, 5)
                px[x, y] = (clamp(col[0] * k + n), clamp(col[1] * k + n), clamp(col[2] * k + n), 255)
        return img

    return f


def plaster(color="#efe2c4"):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        vn = vnoise(ctx.pw, ctx.ph, 5, random.Random(ctx.pw * 3 + ctx.ph))
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                k = 0.94 + 0.1 * vn[y][x] + ctx.rng.uniform(-0.025, 0.025)
                px[x, y] = (clamp(c[0] * k), clamp(c[1] * k), clamp(c[2] * k), 255)
        return img

    return f


def halftimber(wall="#efe2c4", timber="#5a3b24", t=0.75, bay=4.6, braces=True):
    """Plaster panel with a dark timber frame drawn on: sill, plate, posts every `bay`, mid rail, corner braces."""
    base = plaster(wall)
    tc = rgb(timber)

    def f(ctx):
        img = base(ctx)
        d = ImageDraw.Draw(img)
        s = _ppu(ctx)
        sy = ctx.ph / ctx.h if ctx.h > 1e-6 else DENSITY
        tw = max(1, int(round(t * s)))
        th = max(1, int(round(t * sy)))
        W, H = ctx.pw, ctx.ph
        col = tc + (255,)
        n = max(1, int(round(ctx.w / bay)))
        xs = [int(round(i * (W - tw) / n)) for i in range(n + 1)]
        for x in xs:
            d.rectangle([x, 0, x + tw - 1, H - 1], fill=col)
        d.rectangle([0, 0, W - 1, th - 1], fill=col)
        d.rectangle([0, H - th, W - 1, H - 1], fill=col)
        if ctx.h > 3.0:
            ym = int(H * 0.55)
            d.rectangle([0, ym, W - 1, ym + th - 1], fill=col)
        if braces and n >= 2:
            for (a, b, flip) in ((xs[0] + tw, xs[1], False), (xs[-2] + tw, xs[-1], True)):
                if flip:
                    d.line([(a, th), (b, H - th)], fill=col, width=max(1, tw))
                else:
                    d.line([(b, th), (a, H - th)], fill=col, width=max(1, tw))
        px = img.load()
        for y in range(H):
            for x in range(W):
                r, g, b_, a_ = px[x, y]
                if (r, g, b_) == tc:
                    k = 1 + ctx.rng.uniform(-0.08, 0.08)
                    px[x, y] = (clamp(r * k), clamp(g * k), clamp(b_ * k), 255)
        return img

    return f


def dirt(color="#8a6a44"):
    c = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        v1 = vnoise(ctx.pw, ctx.ph, 3, random.Random(ctx.pw * 7 + 1))
        v2 = vnoise(ctx.pw, ctx.ph, 7, random.Random(ctx.ph * 5 + 3))
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                t = v1[y][x] * 0.5 + v2[y][x] * 0.5
                k = 0.84 + 0.3 * t + ctx.rng.uniform(-0.05, 0.05)
                col = c
                if v2[y][x] > 0.72:
                    col = lerp(c, (214, 186, 98), 0.55)
                elif ctx.rng.random() < 0.03:
                    col = (150, 140, 126)
                px[x, y] = (clamp(col[0] * k), clamp(col[1] * k), clamp(col[2] * k), 255)
        return img

    return f


def ov_mask(fn):
    """Cutout: pixels where fn(face, u, v, w, h) is False become transparent (u from image left, v from top, in units)."""
    def f(img, ctx):
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                u = (x + 0.5) / ctx.pw * ctx.w
                v = (y + 0.5) / ctx.ph * ctx.h
                if not fn(ctx.face, u, v, ctx.w, ctx.h):
                    px[x, y] = (0, 0, 0, 0)

    return f


def tri_keep(face, u, v, w, h):
    return abs(u - w / 2) <= (v / h) * (w / 2) + 0.02


def jag_fn(seed, lo=0.35, hi=0.95, n=9):
    r = random.Random(seed)
    pts = [r.uniform(lo, hi) for _ in range(n + 1)]
    for i in range(1, n, 3):
        pts[i] = max(lo, pts[i] - 0.25)

    def prof(t):
        x = max(0.0, min(0.9999, t)) * n
        i = int(x)
        fr = x - i
        return pts[i] * (1 - fr) + pts[i + 1] * fr

    def keep(face, u, v, w, h):
        return (h - v) / h <= prof(u / w)

    return keep


def hole_fn(cu, cv, ru, rv, seed, flip_v=False):
    """Irregular hole (False inside) centred at fractions (cu, cv) of the face, radii in units."""
    r = random.Random(seed)
    k = [r.uniform(-0.3, 0.3) for _ in range(7)]

    def keep(face, u, v, w, h):
        if flip_v:
            v = h - v
        du = (u - cu * w) / ru
        dv = (v - cv * h) / rv
        a = math.atan2(dv, du)
        rad = 1 + sum(k[i] * math.sin((i + 2) * a + i) for i in range(len(k))) * 0.5
        return du * du + dv * dv > rad * rad

    return keep


def sprite(draw):
    """Transparent face with a pixel-art drawing; draw(d, W, H, ctx)."""
    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph), (0, 0, 0, 0))
        draw(ImageDraw.Draw(img), ctx.pw, ctx.ph, ctx)
        return img

    return f


def logs_end(bark="#5a3b24", wood="#c9a06a"):
    b, w_ = rgb(bark), rgb(wood)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        cx, cy = ctx.pw / 2, ctx.ph / 2
        R = min(cx, cy)
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                r = math.hypot(x + 0.5 - cx, y + 0.5 - cy) / R
                if r > 0.82:
                    col, k = b, 1.0
                else:
                    col = w_
                    k = 1.0 - (0.14 if int(r * 5) % 2 else 0)
                n = ctx.rng.uniform(-4, 4)
                px[x, y] = (clamp(col[0] * k + n), clamp(col[1] * k + n), clamp(col[2] * k + n), 255)
        return img

    return f


STONE = fieldstone()
STONE_D = fieldstone("#7f7b74", "#4b4842")
WOOD = planks("#8a6038", 1.4)
WOOD_D = planks("#5e3f26", 1.2)
WOOD_V = planks("#8a6038", 1.4, True)
DARK = paint("#231a13", noise=3, grad=0.02, bevel=0.05)
WHITE = paint(TRIM, noise=3)
IRON = metal("#3b3b40")
GOLD = metal("#c9962f")
STRAW = straw("#e0c060")
SHUTTER = "#3f6b4a"


# --------------------------------------------------------------------------------------------
# Building helpers
# --------------------------------------------------------------------------------------------

def slab(m, face, a0, a1, y0, y1, c_out, t, mat, skip=(), hd=1):
    if face == "n":
        return m.box((a0, y0, c_out - t), (a1, y1, c_out), mat, skip=skip, hd=hd)
    if face == "s":
        return m.box((a0, y0, c_out), (a1, y1, c_out + t), mat, skip=skip, hd=hd)
    if face == "e":
        return m.box((c_out, y0, a0), (c_out + t, y1, a1), mat, skip=skip, hd=hd)
    return m.box((c_out - t, y0, a0), (c_out, y1, a1), mat, skip=skip, hd=hd)


def win(m, face, cx, cy, c_out, w, h, lit=False, trim=TRIM, shutter=None, sw=1.2, panes=(2, 2), sill=True, glow="#ffcf6a"):
    """Small window: pane with mullions, trim frame, optional shutters and sill. Returns element count."""
    n0 = m.mark()
    fr = paint(trim, noise=3)
    pane = paint(glow if lit else "#34506b", noise=5, grad=0.25)
    ovs = []
    for i in range(1, panes[0]):
        ovs.append(ov_stripe(trim, i / panes[0], 0.45, True))
    for i in range(1, panes[1]):
        ovs.append(ov_stripe(trim, i / panes[1], 0.45, False))
    if not lit:
        ovs.append(ov_draw(lambda d, c, i: d.line([(1, c.ph - 2), (c.pw // 2, 1)], fill=(120, 160, 196, 255))))
    slab(m, face, cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, c_out, 0.12, P(pane, *ovs), hd=1)
    b = 0.55
    t = 0.38
    slab(m, face, cx - w / 2 - b, cx + w / 2 + b, cy + h / 2, cy + h / 2 + b, c_out, t, fr)
    slab(m, face, cx - w / 2 - b, cx - w / 2, cy - h / 2, cy + h / 2, c_out, t, fr)
    slab(m, face, cx + w / 2, cx + w / 2 + b, cy - h / 2, cy + h / 2, c_out, t, fr)
    if sill:
        slab(m, face, cx - w / 2 - b - 0.25, cx + w / 2 + b + 0.25, cy - h / 2 - b, cy - h / 2, c_out, t + 0.3, fr)
    else:
        slab(m, face, cx - w / 2 - b, cx + w / 2 + b, cy - h / 2 - b, cy - h / 2, c_out, t, fr)
    if shutter:
        sh = P(planks(shutter, 1.0, True, 0.72, 0.05), ov_stripe(tint(shutter, 0.7), 0.3, 0.4, False), ov_stripe(tint(shutter, 0.7), 0.7, 0.4, False))
        slab(m, face, cx - w / 2 - b - sw, cx - w / 2 - b, cy - h / 2 - b, cy + h / 2 + b, c_out, 0.3, sh)
        slab(m, face, cx + w / 2 + b, cx + w / 2 + b + sw, cy - h / 2 - b, cy + h / 2 + b, c_out, 0.3, sh)
    return m.mark() - n0


def flowerbox(m, face, cx, y_top, c_out, w, seed=1):
    cols = ["#e8453c", "#f7d34a", "#f08ab4", "#f4f0e6", "#9b6fd6", "#ff8c3a"]
    slab(m, face, cx - w / 2, cx + w / 2, y_top - 1.3, y_top, c_out, 1.2, planks("#6b4a2a", 1.0))
    slab(m, face, cx - w / 2 + 0.2, cx + w / 2 - 0.2, y_top, y_top + 0.6, c_out - (0.2 if face in "nw" else -0.2), 0.8, paint("#3f7a34", noise=10), skip=())
    n = max(2, int(w // 1.3))
    r = random.Random(seed)
    for i in range(n):
        a = cx - w / 2 + 0.35 + i * (w - 0.7) / max(1, n - 1) - 0.4
        slab(m, face, a, a + 0.8, y_top + 0.4, y_top + 1.2 + r.uniform(0, 0.4), c_out - (0.35 if face in "nw" else -0.35), 0.6, paint(cols[(i + seed) % len(cols)], noise=8), skip=())


def roof45x(m, x0, x1, zc, hs, ye, ov, t, mat_n, mat_s, mat_under, ridge_mat, cap=True, ext=0.45, parts=("n", "s"), hole=None):
    """45-degree gable roof, ridge along X. Walls at z = zc +- hs, wall top ye. The roof underside meets
    the wall tops exactly. Returns the ridge top height."""
    c = math.sqrt(0.5)
    run = hs + ov
    L = run / c + ext
    for s in (-1, 1):
        if ("n" if s < 0 else "s") not in parts:
            continue
        mid = run / 2
        yc = ye + hs - mid + (t / 2) / c
        zmid = zc + s * mid
        zmid -= s * (ext / 2) * c
        yc += (ext / 2) * c
        mat = {"up": mat_n if s < 0 else mat_s, "down": mat_under, "all": mat_under}
        if hole:
            mat["up"] = P(mat["up"], ov_mask(hole_fn(*hole)))
            mat["down"] = P(mat_under, ov_mask(hole_fn(*hole, flip_v=True)))
        m.box((x0, yc - t / 2, zmid - L / 2), (x1, yc + t / 2, zmid + L / 2), mat, rot=("x", 45 * (-s), (0, yc, zmid)), skip=())
    top = ye + hs + t / c
    if cap:
        a = 0.85
        m.box((x0 - 0.15, top - 0.35 - a, zc - a), (x1 + 0.15, top - 0.35 + a, zc + a), ridge_mat, rot=("x", 45, (0, top - 0.35, zc)), skip=())
    return top


def barge45x(m, x, zc, hs, ye, ov, t, mat, side):
    """White barge boards along both slopes at the gable end x (side=-1 west end, +1 east end)."""
    c = math.sqrt(0.5)
    run = hs + ov
    L = run / c + 0.3
    tt = t + 0.35
    for s in (-1, 1):
        mid = run / 2
        yc = ye + hs - mid + (t / 2) / c + 0.12
        zmid = zc + s * mid
        x0, x1 = (x - 0.45, x + 0.05) if side < 0 else (x - 0.05, x + 0.45)
        m.box((x0, yc - tt / 2, zmid - L / 2), (x1, yc + tt / 2, zmid + L / 2), mat, rot=("x", 45 * (-s), (x, yc, zmid)), skip=())


def gable_tri_x(m, x_face, side, zc, hs, ye, mat, thick=0.6, hd=1, mask_extra=None):
    """Triangular gable end (cutout) on the end wall plane at x_face, from ye up to ye + hs."""
    keep = tri_keep if mask_extra is None else (lambda f, u, v, w, h: tri_keep(f, u, v, w, h) and mask_extra(f, u, v, w, h))
    tex = P(mat, ov_mask(keep))
    x0, x1 = (x_face, x_face + thick) if side < 0 else (x_face - thick, x_face)
    m.box((x0, ye, zc - hs), (x1, ye + hs, zc + hs), {"east": tex, "west": tex, "all": tex}, skip=("up", "down", "north", "south"), hd=hd)


def oct_ring(m, cy, a, h, t, mat, y0=None):
    """Octagonal ring of 8 rails (apothem a) at height cy, rail height h and thickness t."""
    s = 2 * a * math.tan(math.radians(22.5)) + 0.25
    for k in range(4):
        pass
    m.box((-s / 2, cy - h / 2, -a - t / 2), (s / 2, cy + h / 2, -a + t / 2), mat, skip=())
    m.box((-s / 2, cy - h / 2, a - t / 2), (s / 2, cy + h / 2, a + t / 2), mat, skip=())
    m.box((-a - t / 2, cy - h / 2, -s / 2), (-a + t / 2, cy + h / 2, s / 2), mat, skip=())
    m.box((a - t / 2, cy - h / 2, -s / 2), (a + t / 2, cy + h / 2, s / 2), mat, skip=())
    for sx in (-1, 1):
        for sz in (-1, 1):
            d = a * math.sqrt(0.5)
            px_, pz_ = sx * d, sz * d
            ang = 45 if sx * sz < 0 else -45
            m.box((px_ - s / 2, cy - h / 2, pz_ - t / 2), (px_ + s / 2, cy + h / 2, pz_ + t / 2), mat, rot=("y", ang, (px_, cy, pz_)), skip=())


def oct_corners(a):
    R = a / math.cos(math.radians(22.5))
    return [(R * math.sin(math.radians(22.5 + 45 * i)), -R * math.cos(math.radians(22.5 + 45 * i))) for i in range(8)]


def sack(m, x, z, h=2.6, w=2.0, col="#d8c9a3", stripe="#8a6a3a", lean=None):
    mat = P(burlap(col), ov_stripe(stripe, 0.5, 0.5, False))
    rot = None
    if lean:
        rot = (lean[0], lean[1], (x, 0, z))
    m.box((x - w / 2, 0, z - w * 0.4), (x + w / 2, h, z + w * 0.4), {"up": burlap(tint(col, 0.95)), "all": mat}, rot=rot)
    m.box((x - w * 0.22, h, z - w * 0.18), (x + w * 0.22, h + 0.55, z + w * 0.18), burlap(tint(col, 0.88)), rot=rot, skip=())


def rubble(m, cx, cz, n, spread, seed, mats, hmax=1.1):
    r = random.Random(seed)
    for i in range(n):
        x = cx + r.uniform(-spread, spread)
        z = cz + r.uniform(-spread * 0.7, spread * 0.7)
        w = r.uniform(0.7, 1.6)
        d = r.uniform(0.6, 1.4)
        h = r.uniform(0.4, hmax)
        rot = None
        if r.random() < 0.5:
            rot = ("y", r.choice((22.5, -22.5, 45)), (x, 0, z))
        m.box((x - w / 2, 0, z - d / 2), (x + w / 2, h, z + d / 2), mats[i % len(mats)], rot=rot)


def plank_debris(m, pts, seed, mats):
    """Loose boards: list of (x, z, length, axis, angle) lying on the ground or leaning."""
    r = random.Random(seed)
    for i, (x, z, L, ax, ang, y) in enumerate(pts):
        w = r.uniform(0.7, 1.0)
        t = 0.3
        mat = mats[i % len(mats)]
        if ax == "y":
            m.box((x - L / 2, y, z - w / 2), (x + L / 2, y + t, z + w / 2), mat, rot=("y", ang, (x, y, z)), skip=())
        elif ax == "z":
            m.box((x - L / 2, y, z - w / 2), (x + L / 2, y + t, z + w / 2), mat, rot=("z", ang, (x, y, z)), skip=())
        else:
            m.box((x - w / 2, y, z - L / 2), (x + w / 2, y + t, z + L / 2), mat, rot=("x", ang, (x, y, z)), skip=())


# --------------------------------------------------------------------------------------------
# Chicken coop
# --------------------------------------------------------------------------------------------

COOP = dict(HX0=-11.2, HX1=8.6, HZ0=-4.4, HZ1=8.4, FL=2.4, YE=10.0, POP_X=-0.9)


def rooster_draw(d, W, H, ctx):
    col = (201, 150, 47, 255)
    dk = (120, 84, 22, 255)
    sx = W / 20.0
    sy = H / 16.0

    def P_(pts):
        return [(x * sx, y * sy) for x, y in pts]

    # arrow (bottom)
    d.rectangle([0, int(13.2 * sy), W - 1, int(14.4 * sy)], fill=dk)
    d.polygon(P_([(0, 13.8), (2.6, 11.6), (2.6, 16.0)]), fill=dk)
    d.polygon(P_([(20, 13.8), (17.2, 11.2), (18.4, 13.8), (17.2, 16.0)]), fill=dk)
    # legs
    d.line(P_([(9.0, 10.5), (8.4, 13.4)]), fill=dk, width=max(1, int(sx * 0.9)))
    d.line(P_([(11.0, 10.5), (11.4, 13.4)]), fill=dk, width=max(1, int(sx * 0.9)))
    # tail
    d.polygon(P_([(5.5, 8.5), (2.0, 2.0), (4.5, 3.0), (3.6, 0.6), (6.6, 2.6), (7.4, 0.8), (8.6, 4.6), (9.0, 8.0)]), fill=col)
    # body
    d.ellipse(P_([(5.0, 5.2), (14.0, 11.2)]), fill=col)
    # neck + head
    d.polygon(P_([(11.5, 7.0), (12.6, 3.4), (14.8, 3.0), (14.6, 7.6)]), fill=col)
    d.ellipse(P_([(12.2, 1.6), (15.6, 4.6)]), fill=col)
    # comb, beak, wattle
    d.polygon(P_([(12.6, 2.0), (12.9, 0.4), (13.7, 1.2), (14.2, 0.0), (14.8, 1.0), (15.2, 1.9)]), fill=(196, 58, 40, 255))
    d.polygon(P_([(15.4, 2.6), (17.4, 3.2), (15.4, 3.8)]), fill=dk)
    d.ellipse(P_([(14.6, 3.8), (15.6, 5.2)]), fill=(196, 58, 40, 255))
    d.point((int(14.4 * sx), int(2.7 * sy)), fill=(30, 20, 10, 255))


def coop(state="normal"):
    """state: normal | broken"""
    broken = state == "broken"
    name = "coop_t1" + ("_broken" if broken else "")
    m = M(name, 9101 + (7 if broken else 0))
    C = COOP
    HX0, HX1, HZ0, HZ1, FL, YE = C["HX0"], C["HX1"], C["HZ0"], C["HZ1"], C["FL"], C["YE"]
    zc = (HZ0 + HZ1) / 2
    hs = (HZ1 - HZ0) / 2
    red_c = "#a8432f"
    red = bnb(red_c)
    trim = WHITE
    roof_c = "#4f4b52"
    under = planks("#7a5638", 1.2)

    # --- footings, skirt, sill ------------------------------------------------------------
    for x in (HX0 + 0.9, (HX0 + HX1) / 2, HX1 - 0.9):
        for z in (HZ0 + 0.9, HZ1 - 0.9):
            m.box((x - 1.1, 0, z - 1.1), (x + 1.1, FL - 0.6, z + 1.1), STONE)
    lattice = P(paint("#2c2119", noise=3), ov_draw(lambda d, c, i: [d.line([(k, 0), (k + c.ph, c.ph)], fill=(176, 150, 112, 255)) for k in range(-c.ph, c.pw, 6)] + [d.line([(k, c.ph), (k + c.ph, 0)], fill=(176, 150, 112, 255)) for k in range(-c.ph, c.pw, 6)]))
    m.box((HX0 + 0.35, 0, HZ0 + 0.35), (HX1 - 0.35, FL - 0.6, HZ1 - 0.35), {"north": lattice, "south": lattice, "east": lattice, "west": lattice, "all": DARK}, skip=("down", "up"), hd=2)
    m.box((HX0 - 0.15, FL - 0.7, HZ0 - 0.15), (HX1 + 0.15, FL, HZ1 + 0.15), {"up": STRAW, "all": WOOD_D}, skip=("down",))

    # --- walls ------------------------------------------------------------------------------
    if not broken:
        m.box((HX0, FL, HZ0), (HX1, YE, HZ1), {"up": DARK, "all": red}, skip=("down",))
    else:
        jn = jag_fn(11, 0.45, 1.0)
        js = jag_fn(12, 0.7, 1.0)
        je = jag_fn(13, 0.3, 0.85)
        mat = {"north": P(red, ov_mask(jn)), "south": P(red, ov_mask(js)), "east": P(red, ov_mask(je)), "west": red}
        m.box((HX0, FL, HZ0), (HX1, YE, HZ1), mat, skip=("down", "up"))
        inner = planks("#4a3322", 1.4, True, 0.7, 0.05)
        imat = {"north": P(inner, ov_mask(js)), "south": P(inner, ov_mask(jn)), "east": inner, "west": P(inner, ov_mask(je))}
        i0 = 0.35
        m.box((HX0 + i0, FL, HZ0 + i0), (HX1 - i0, YE - 0.1, HZ0 + i0 + 0.1), {"south": P(inner, ov_mask(jn)), "all": inner}, skip=("down", "up", "north", "east", "west"))
        m.box((HX0 + i0, FL, HZ1 - i0 - 0.1), (HX1 - i0, YE - 0.1, HZ1 - i0), {"north": P(inner, ov_mask(js)), "all": inner}, skip=("down", "up", "south", "east", "west"))
        m.box((HX1 - i0 - 0.1, FL, HZ0 + i0), (HX1 - i0, YE - 0.1, HZ1 - i0), {"west": P(inner, ov_mask(je)), "all": inner}, skip=("down", "up", "north", "south", "east"))
        m.box((HX0 + i0, FL, HZ0 + i0), (HX0 + i0 + 0.1, YE - 0.1, HZ1 - i0), inner, skip=("down", "up", "north", "south", "west"))
        m.box((HX0 + i0, FL, HZ0 + i0), (HX1 - i0, FL + 0.25, HZ1 - i0), STRAW, skip=("down",))

    # corner boards and bands
    cb = 0.85
    for (x0, x1) in ((HX0 - 0.22, HX0 + cb), (HX1 - cb, HX1 + 0.22)):
        for (z0, z1) in ((HZ0 - 0.22, HZ0 + cb), (HZ1 - cb, HZ1 + 0.22)):
            ytop = YE
            if broken and (x0 > 0 and z0 < 0):
                ytop = YE - 3.2
            m.box((x0, FL, z0), (x1, ytop, z1), trim, skip=("down",))
    m.box((HX0 - 0.12, FL, HZ0 - 0.12), (HX1 + 0.12, FL + 0.6, HZ1 + 0.12), trim, skip=("down", "up"))
    if not broken:
        for z0, z1 in ((HZ0 - 0.12, HZ0 + 0.5), (HZ1 - 0.5, HZ1 + 0.12)):
            m.box((HX0, YE - 0.6, z0), (HX1, YE, z1), trim, skip=("down", "up"))

    # --- front: pop door + ramp, windows ----------------------------------------------------
    px_ = C["POP_X"]
    slab(m, "n", px_ - 1.3, px_ + 1.3, FL + 0.6, FL + 3.4, HZ0, 0.14, DARK)
    slab(m, "n", px_ - 1.85, px_ - 1.3, FL + 0.6, FL + 3.95, HZ0, 0.32, trim)
    slab(m, "n", px_ + 1.3, px_ + 1.85, FL + 0.6, FL + 3.95, HZ0, 0.32, trim)
    slab(m, "n", px_ - 1.85, px_ + 1.85, FL + 3.4, FL + 3.95, HZ0, 0.32, trim)
    if not broken:
        door = P(planks("#8a6038", 0.9, True, 0.7, 0.05), ov_stripe("#5e3f26", 0.5, 0.45, False))
        slab(m, "n", px_ - 1.4, px_ + 1.4, FL + 4.05, FL + 6.8, HZ0, 0.45, door)
        for sx in (-1, 1):
            slab(m, "n", px_ + sx * 1.6 - 0.18, px_ + sx * 1.6 + 0.18, FL + 3.95, FL + 7.1, HZ0, 0.6, WOOD_D)
        slab(m, "n", px_ - 0.15, px_ + 0.15, FL + 6.8, FL + 7.6, HZ0 - 0.25, 0.15, IRON)
    # ramp with cleats
    yh = FL - 0.15
    Lr = yh / math.sin(math.radians(22.5)) + 0.5
    rw = 2.5
    ramp_mat = planks("#9a6c40", 1.0, False, 0.7, 0.06)
    if not broken:
        org = (px_, yh, HZ0 - 0.05)
        m.box((px_ - rw / 2, yh - 0.35, HZ0 - 0.05 - Lr), (px_ + rw / 2, yh, HZ0 - 0.05), ramp_mat, rot=("x", 22.5, org), skip=())
        for k in range(5):
            zz = HZ0 - 0.05 - 0.8 - k * 1.15
            m.box((px_ - rw / 2 + 0.15, yh, zz - 0.2), (px_ + rw / 2 - 0.15, yh + 0.28, zz + 0.2), WOOD_D, rot=("x", 22.5, org), skip=())
    else:
        m.box((px_ - rw / 2 - 1.5, 0, -8.7 - Lr / 2 + 2.5), (px_ + rw / 2 - 1.5, 0.35, -8.7 + Lr / 2 + 0.8), ramp_mat, rot=("y", 22.5, (px_ - 1.5, 0, -7.0)), skip=())
    # windows
    if not broken:
        win(m, "n", -7.0, FL + 4.6, HZ0, 2.2, 2.4, False, TRIM, SHUTTER, sw=1.05)
        win(m, "n", 4.4, FL + 4.6, HZ0, 2.2, 2.4, False, TRIM, SHUTTER, sw=1.05)
        flowerbox(m, "n", 4.4, FL + 2.85, HZ0, 3.0, seed=2)
    else:
        win(m, "n", -7.0, FL + 4.6, HZ0, 2.2, 2.4, False, TRIM, None)
        slab(m, "n", -9.7, -8.5, FL + 1.0, FL + 5.6, HZ0, 0.3, planks(SHUTTER, 1.0, True))
    win(m, "s", (HX0 + HX1) / 2 - 2, FL + 4.6, HZ1, 2.2, 2.4, False, TRIM, SHUTTER if not broken else None, sw=1.05)

    # --- west end: people door with steps ---------------------------------------------------
    dz = zc + 0.5
    slab(m, "w", dz - 1.7, dz + 1.7, FL + 0.2, FL + 6.2, HX0, 0.2, P(planks("#7a5230", 1.1, True, 0.7, 0.05), ov_draw(lambda d, c, i: (d.line([(1, c.ph - 2), (c.pw - 2, c.ph // 2 + 1)], fill=(70, 46, 28, 255), width=2), d.rectangle([0, c.ph // 2 - 1, c.pw - 1, c.ph // 2], fill=(70, 46, 28, 255)), d.rectangle([0, 1, c.pw - 1, 2], fill=(70, 46, 28, 255)), d.rectangle([0, c.ph - 3, c.pw - 1, c.ph - 2], fill=(70, 46, 28, 255))))))
    slab(m, "w", dz - 2.25, dz - 1.7, FL, FL + 6.75, HX0, 0.4, trim)
    slab(m, "w", dz + 1.7, dz + 2.25, FL, FL + 6.75, HX0, 0.4, trim)
    slab(m, "w", dz - 2.25, dz + 2.25, FL + 6.2, FL + 6.75, HX0, 0.4, trim)
    slab(m, "w", dz + 0.9, dz + 1.3, FL + 2.9, FL + 3.3, HX0 - 0.2, 0.3, GOLD)
    m.box((HX0 - 2.4, 0, dz - 1.9), (HX0 - 0.15, 0.9, dz + 1.9), STONE_D)
    m.box((HX0 - 1.3, 0.9, dz - 1.9), (HX0 - 0.15, 1.8, dz + 1.9), STONE_D, skip=("down",))
    if not broken:
        win(m, "w", zc - 3.3, FL + 4.6, HX0, 1.8, 2.2, False, TRIM, None)

    # --- nest boxes (east) --------------------------------------------------------------------
    nb_d = 3.2
    nb_lo = FL + 0.9
    nb_hi = FL + 4.0
    lid_rise = nb_d * math.tan(math.radians(22.5))
    nb_z0, nb_z1 = zc - 3.9, zc + 3.9
    nb_top = nb_hi + lid_rise

    def nb_keep(face, u, v, w, h):
        hb = h - v
        if face == "east":
            return hb <= (nb_hi - nb_lo)
        if face == "north":
            xo = w - u
        elif face == "south":
            xo = u
        else:
            return True
        return hb <= (nb_top - nb_lo) - xo * math.tan(math.radians(22.5)) + 0.05

    nbm = P(bnb(red_c, 1.6), ov_mask(nb_keep))
    m.box((HX1, nb_lo, nb_z0), (HX1 + nb_d, nb_top, nb_z1), {"north": nbm, "south": nbm, "east": P(bnb(red_c, 1.6), ov_mask(nb_keep)), "all": red}, skip=("up", "west"))
    m.box((HX1, nb_lo - 0.5, nb_z0 - 0.1), (HX1 + nb_d + 0.1, nb_lo, nb_z1 + 0.1), trim, skip=())
    lid = {"up": shingles(roof_c, 1.2, 1.5, "bottom"), "all": WOOD}
    if not broken:
        m.box((HX1 - 0.1, nb_top, nb_z0 - 0.35), (HX1 + nb_d + 0.8, nb_top + 0.45, nb_z1 + 0.35), lid, rot=("z", 22.5, (HX1, nb_top, zc)), skip=())
        for zz in (nb_z0 + 1.6, nb_z1 - 1.6):
            m.box((HX1 + 0.2, nb_top + 0.42, zz - 0.3), (HX1 + 1.8, nb_top + 0.6, zz + 0.3), IRON, rot=("z", 22.5, (HX1, nb_top, zc)), skip=())
    else:
        m.box((HX1 - 0.1, nb_top, nb_z0 - 0.35), (HX1 + nb_d + 0.8, nb_top + 0.45, nb_z1 + 0.35), lid, rot=("z", -45, (HX1, nb_top, zc)), skip=())
        for k in range(3):
            m.box((HX1 + 0.6, nb_lo + 0.2, nb_z0 + 0.6 + k * 2.5), (HX1 + 2.6, nb_lo + 0.9, nb_z0 + 2.3 + k * 2.5), STRAW, skip=())
        m.box((HX1 + 1.2, nb_lo + 0.9, nb_z0 + 1.0), (HX1 + 2.0, nb_lo + 1.9, nb_z0 + 1.8), paint("#f4f0e6", noise=3), skip=())
    for zz in (nb_z0 + 0.9, nb_z1 - 0.9):
        m.box((HX1 + 0.4, nb_lo - 2.6, zz - 0.3), (HX1 + 3.0, nb_lo - 2.0, zz + 0.3), WOOD_D, rot=("z", -45, (HX1 + 0.4, nb_lo - 2.6, zz)), skip=())

    # --- roof -----------------------------------------------------------------------------------
    ov, fov, t = 1.25, 1.0, 0.7
    rx0, rx1 = HX0 - fov, HX1 + fov
    shn = shingles(roof_c, 1.5, 1.9, "top", moss="#6b7a4a")
    shs = shingles(roof_c, 1.5, 1.9, "bottom", moss="#6b7a4a")
    ridge = planks("#3a363c", 1.0)
    if not broken:
        top = roof45x(m, rx0, rx1, zc, hs, YE, ov, t, shn, shs, under, ridge)
        gtri = bnb(red_c)
        gable_tri_x(m, HX0, -1, zc, hs, YE, gtri)
        gable_tri_x(m, HX1, 1, zc, hs, YE, gtri)
        for side, xf in ((-1, rx0), (1, rx1)):
            barge45x(m, xf, zc, hs, YE, ov, t, trim, side)
        for side, xf in ((-1, HX0), (1, HX1)):
            yv = YE + 2.6
            a = 1.25
            x0, x1 = (xf - 0.25, xf) if side < 0 else (xf, xf + 0.25)
            m.box((x0, yv - a, zc - a), (x1, yv + a, zc + a), trim, rot=("x", 45, (xf, yv, zc)), skip=())
            x0, x1 = (xf - 0.35, xf - 0.25) if side < 0 else (xf + 0.25, xf + 0.35)
            m.box((x0, yv - 0.8, zc - 0.8), (x1, yv + 0.8, zc + 0.8), DARK, rot=("x", 45, (xf, yv, zc)), skip=())
        # weathervane on the ridge
        vx = -3.4
        vy = top + 0.2
        m.box((vx - 0.7, vy - 0.4, zc - 0.7), (vx + 0.7, vy + 0.5, zc + 0.7), IRON, skip=())
        m.box((vx - 0.16, vy + 0.5, zc - 0.16), (vx + 0.16, vy + 4.2, zc + 0.16), IRON, skip=())
        m.box((vx - 1.7, vy + 2.0, zc - 0.1), (vx + 1.7, vy + 2.22, zc + 0.1), IRON, skip=())
        m.box((vx - 0.1, vy + 2.0, zc - 1.7), (vx + 0.1, vy + 2.22, zc + 1.7), IRON, skip=())
        m.box((vx - 0.32, vy + 2.75, zc - 0.32), (vx + 0.32, vy + 3.35, zc + 0.32), GOLD, skip=())
        rs = sprite(rooster_draw)
        m.box((vx - 2.3, vy + 4.1, zc - 0.08), (vx + 2.3, vy + 7.8, zc + 0.08), {"north": rs, "south": rs, "all": rs}, skip=("up", "down", "east", "west"), hd=4)
    else:
        # south slope kept, north slope blown off, east gable torn
        top = roof45x(m, rx0, rx1 - 4.5, zc, hs, YE, ov, t, shn, shs, under, ridge, cap=False, parts=("s",), hole=(0.62, 0.45, 3.2, 2.6, 71))
        m.box((rx0 - 0.1, top - 1.2, zc - 0.6), (rx1 - 7.0, top - 0.2, zc + 0.6), ridge, skip=())
        gable_tri_x(m, HX0, -1, zc, hs, YE, bnb(red_c), mask_extra=jag_fn(21, 0.4, 1.0))
        barge45x(m, rx0, zc, hs, YE, ov, t, trim, -1)
        c = math.sqrt(0.5)
        for xr in (HX0 + 3.0, -1.0, 3.0, HX1 - 1.2):
            run = hs
            L = run / c
            yc = YE + hs / 2 + 0.2
            m.box((xr - 0.3, yc - 0.3, zc - hs / 2 - L / 2), (xr + 0.3, yc + 0.3, zc - hs / 2 + L / 2), WOOD_D, rot=("x", 45, (xr, yc, zc - hs / 2)), skip=())
        # torn north slope lying in front, propped on the ramp side
        m.box((-11.6, 0.4, -10.6), (-2.4, 1.1, -5.4), {"up": shn, "all": under}, rot=("z", 22.5, (-7.0, 0.7, -8.0)), skip=())
        m.box((3.2, 0, -10.2), (9.4, 0.6, -6.6), {"up": shn, "all": under}, rot=("y", -22.5, (6.3, 0.3, -8.4)), skip=())
        # fallen weathervane
        m.box((8.0, 0.1, 6.0), (12.0, 0.4, 6.4), IRON, rot=("y", 22.5, (10.0, 0.2, 6.2)), skip=())
        rs = sprite(rooster_draw)
        m.box((9.4, 0.0, 7.9), (13.2, 0.25, 10.9), {"up": rs, "all": rs}, skip=("north", "south", "east", "west", "down"), hd=4)
        plank_debris(m, [(-5.0, -8.6, 5.0, "y", 22.5, 0.0), (5.2, 9.5, 4.4, "y", -45, 0.0), (-12.0, 4.0, 4.2, "y", 45, 0.0),
                         (2.0, -7.0, 3.6, "y", -22.5, 0.6), (11.4, -2.0, 4.0, "y", 22.5, 0.0), (-8.6, 9.4, 3.4, "y", 0, 0.0),
                         (-1.0, 1.0, 6.0, "z", 22.5, YE - 2.2)], 5, [WOOD, bnb(red_c), WOOD_D, WHITE])
        rubble(m, 0, -7.4, 5, 7.5, 17, [STONE, paint("#4f4b52", noise=6), WOOD_D], 0.8)
        rubble(m, 10.5, 3.0, 3, 1.6, 18, [STONE_D, WOOD], 0.7)

    # --- straw, hay bale, egg basket --------------------------------------------------------------
    r = random.Random(4)
    for i in range(5):
        x = px_ + r.uniform(-3.4, 3.4)
        z = -10.0 + r.uniform(0.2, 2.6)
        m.box((x - 0.9, 0, z - 0.5), (x + 0.9, 0.22, z + 0.5), STRAW, rot=("y", r.choice((22.5, -22.5, 0.0)), (x, 0, z)) if i % 2 else None)
    bale = {"north": P(straw("#d8b850"), ov_stripe("#8a6a3a", 0.3, 0.4, True), ov_stripe("#8a6a3a", 0.7, 0.4, True)), "south": P(straw("#d8b850"), ov_stripe("#8a6a3a", 0.3, 0.4, True), ov_stripe("#8a6a3a", 0.7, 0.4, True)), "up": P(straw("#e0c060"), ov_stripe("#8a6a3a", 0.3, 0.4, False), ov_stripe("#8a6a3a", 0.7, 0.4, False)), "all": straw("#d0b04a")}
    if not broken:
        m.box((-13.0, 0, -9.3), (-9.6, 2.2, -7.1), bale)
        m.box((-12.6, 2.2, -8.8), (-10.2, 3.2, -7.2), {"up": STRAW, "all": straw("#d0b04a")}, rot=("y", 22.5, (-11.4, 2.2, -8.0)))
        bx, bz = 3.6, -8.4
        m.box((bx - 1.2, 0, bz - 0.9), (bx + 1.2, 1.2, bz + 0.9), {"up": P(paint("#5a3b24", noise=3), ov_frame("#9a6c40", 0.5)), "all": P(cloth("#b0844a", 1, 8), ov_stripe("#7a5230", 0.5, 0.5, False))}, skip=("down",))
        for k, (ex, ez) in enumerate(((-0.5, -0.2), (0.4, 0.3), (0.0, -0.1))):
            m.box((bx + ex - 0.35, 1.0, bz + ez - 0.3), (bx + ex + 0.35, 1.75 - k * 0.08, bz + ez + 0.3), paint("#f4efe2" if k != 1 else "#d9b48a", noise=3), skip=("down",))
        m.box((bx - 1.25, 1.2, bz - 0.1), (bx + 1.25, 2.6, bz + 0.1), WOOD_D, skip=("down",)) if False else None
    else:
        m.box((-13.0, 0, -9.3), (-9.6, 2.0, -7.1), bale, rot=("y", 22.5, (-11.3, 0, -8.2)))
    return m


def coop_yard():
    """Fenced dirt yard placed in front of the coop (separate part). Origin = yard centre, floor y=0.
    About 8 x 5 blocks at the coop scale (4.8): 26.6 x 16.6 model units. The back (+Z) side faces the
    coop and has an opening where the coop ramp comes down."""
    m = M("coop_yard", 9150)
    X0, X1, Z0, Z1 = -13.3, 13.3, -8.3, 8.3
    H = 3.4
    post_m = planks("#7a5230", 0.9, True, 0.7, 0.05)
    rail = planks("#9a6c40", 1.2)
    wire = mesh("#b8bec4", 0.9)
    m.box((X0 + 0.2, 0, Z0 + 0.2), (X1 - 0.2, 0.22, Z1 - 0.2), dirt(), skip=("down",))
    gate_c, gate_w = 5.5, 4.4

    def run(x0, z0, x1, z1, gaps=()):
        L = math.hypot(x1 - x0, z1 - z0)
        n = max(1, int(round(L / 4.4)))
        for i in range(n + 1):
            t = i / n
            post_x = x0 + (x1 - x0) * t
            post_z = z0 + (z1 - z0) * t
            m.box((post_x - 0.4, 0, post_z - 0.4), (post_x + 0.4, H + 0.35, post_z + 0.4), {"up": paint("#5e3f26"), "all": post_m}, skip=("down",))
        segs = [(0.0, 1.0)]
        for g0, g1 in gaps:
            new = []
            for a, b in segs:
                if g1 <= a or g0 >= b:
                    new.append((a, b))
                else:
                    if g0 > a:
                        new.append((a, g0))
                    if g1 < b:
                        new.append((g1, b))
            segs = new
        for a, b in segs:
            ax, az = x0 + (x1 - x0) * a, z0 + (z1 - z0) * a
            bx, bz = x0 + (x1 - x0) * b, z0 + (z1 - z0) * b
            xa, xb = sorted((ax, bx))
            za, zb = sorted((az, bz))
            m.box((xa - 0.15, H - 0.45, za - 0.15), (xb + 0.15, H, zb + 0.15), rail, skip=())
            m.box((xa - 0.15, 0.25, za - 0.15), (xb + 0.15, 0.65, zb + 0.15), rail, skip=())
            if xb - xa > zb - za:
                m.box((xa, 0.65, za - 0.02), (xb, H - 0.45, za + 0.02), wire, skip=("up", "down", "east", "west"))
            else:
                m.box((xa - 0.02, 0.65, za), (xa + 0.02, H - 0.45, zb), wire, skip=("up", "down", "north", "south"))

    L = X1 - X0
    run(X0, Z0, X1, Z0, gaps=(((gate_c - gate_w / 2 - X0) / L, (gate_c + gate_w / 2 - X0) / L),))
    run(X0, Z0, X0, Z1)
    run(X1, Z0, X1, Z1)
    pop = COOP["POP_X"]
    run(X0, Z1, X1, Z1, gaps=(((pop - 2.4 - X0) / L, (pop + 2.4 - X0) / L),))
    # gate (closed, framed with a diagonal brace)
    g0, g1 = gate_c - gate_w / 2 + 0.45, gate_c + gate_w / 2 - 0.45
    gate = P(planks("#9a6c40", 0.9, True, 0.7, 0.05), ov_draw(lambda d, c, i: (d.rectangle([0, 0, c.pw - 1, c.ph - 1], outline=(94, 63, 38, 255), width=2), d.line([(1, c.ph - 2), (c.pw - 2, 1)], fill=(94, 63, 38, 255), width=2))))
    m.box((g0, 0.5, Z0 - 0.2), (g1, H - 0.3, Z0 + 0.2), {"north": gate, "south": gate, "all": planks("#9a6c40", 0.9)}, skip=())
    m.box((g1 - 0.9, H * 0.55, Z0 - 0.45), (g1 - 0.3, H * 0.55 + 0.4, Z0 - 0.2), IRON, skip=())
    # feeder trough and waterer
    tx, tz = -7.0, -2.0
    m.box((tx - 2.6, 0.2, tz - 0.9), (tx + 2.6, 1.3, tz + 0.9), {"up": P(paint("#5a3b24"), ov_rect("#d8b850", 0.4, 0.4, 4.4, 1.0)), "all": planks("#8a6038", 1.0)})
    for sx in (-1, 1):
        m.box((tx + sx * 2.6 - 0.25, 0.2, tz - 1.1), (tx + sx * 2.6 + 0.25, 1.6, tz + 1.1), WOOD_D)
    wx, wz = 8.6, 1.6
    cyl_y(m, wx, 0.2, wz, 1.4, 0.45, {"all": metal("#9aa0a6"), "up": paint("#5d8fb8", noise=4)})
    cyl_y(m, wx, 0.65, wz, 0.8, 2.0, {"all": metal("#b5bbc1")})
    m.box((wx - 0.35, 2.65, wz - 0.35), (wx + 0.35, 3.05, wz + 0.35), metal("#6d7076"), skip=())
    r = random.Random(9)
    for i in range(6):
        x, z = r.uniform(-11, 11), r.uniform(-6.5, 6.5)
        m.box((x - 0.8, 0.22, z - 0.5), (x + 0.8, 0.38, z + 0.5), STRAW, rot=("y", r.choice((22.5, -22.5, 45, 0.0)), (x, 0.22, z)) if i % 2 else None)
    for x, z in ((-1.5, -5.0), (2.4, -4.2), (0.6, 3.8)):
        m.box((x - 0.15, 0.22, z - 0.15), (x + 0.15, 0.32, z + 0.15), paint("#f4efe2"), skip=("down",))
    return m


# --------------------------------------------------------------------------------------------
# Windmill (tower) + sails part
# --------------------------------------------------------------------------------------------

MILL = dict(HUB_Y=24.2, HUB_Z=-11.4, SAIL_R=14.3, DOOR_Z=-7.6)


def oct_layer(m, y0, a, h, side, top=None):
    cyl_y(m, 0, y0, 0, a, h, {"up": top or side, "down": side, "all": side})


def transposed(painter):
    """Paint with width/height swapped, then transpose (rows become columns)."""
    from lib import Ctx

    def f(ctx):
        img = painter(Ctx(ctx.ph, ctx.pw, ctx.h, ctx.w, ctx.face, ctx.rng))
        return img.transpose(Image.TRANSPOSE)

    return f


def roof45z(m, z0, z1, xc, hs, ye, t, ov, mat_w, mat_e, mat_under, ridge_mat, ext=0.45, parts=("w", "e")):
    """45-degree gable roof with the ridge along Z (walls at x = xc +- hs, top ye)."""
    c = math.sqrt(0.5)
    run = hs + ov
    L = run / c + ext
    for s in (-1, 1):
        if ("w" if s < 0 else "e") not in parts:
            continue
        mid = run / 2
        yc = ye + hs - mid + (t / 2) / c + (ext / 2) * c
        xmid = xc + s * mid - s * (ext / 2) * c
        mat = {"up": mat_w if s < 0 else mat_e, "down": mat_under, "all": mat_under}
        m.box((xmid - L / 2, yc - t / 2, z0), (xmid + L / 2, yc + t / 2, z1), mat, rot=("z", 45 * s, (xmid, yc, (z0 + z1) / 2)), skip=())
    top = ye + hs + t / c
    if ridge_mat is not None:
        a = 0.8
        m.box((xc - a, top - 0.35 - a, z0 - 0.15), (xc + a, top - 0.35 + a, z1 + 0.15), ridge_mat, rot=("z", 45, (xc, top - 0.35, (z0 + z1) / 2)), skip=())
    return top


def barge45z(m, z, xc, hs, ye, t, ov, mat, side):
    c = math.sqrt(0.5)
    run = hs + ov
    L = run / c + 0.3
    tt = t + 0.35
    for s in (-1, 1):
        mid = run / 2
        yc = ye + hs - mid + (t / 2) / c + 0.12
        xmid = xc + s * mid
        z0, z1 = (z - 0.45, z + 0.05) if side < 0 else (z - 0.05, z + 0.45)
        m.box((xmid - L / 2, yc - tt / 2, z0), (xmid + L / 2, yc + tt / 2, z1), mat, rot=("z", 45 * s, (xmid, yc, z)), skip=())


def mill(state="normal"):
    """state: normal | on | broken. Slim tapered tower (stone base, brick upper), wooden gallery,
    boat-shaped (gabled) cap with the windshaft coming out of its front gable."""
    on = state == "on"
    broken = state == "broken"
    name = "mill_t1" + {"normal": "", "on": "_on", "broken": "_broken"}[state]
    m = M(name, 9200 + {"normal": 0, "on": 1, "broken": 2}[state])
    stone = fieldstone("#a19a8e", "#5f584e", 1.8, 2.8)
    stone_d = fieldstone("#857e73", "#4d473f", 1.8, 2.8)
    brick = bricks("#b3613f", "#6e3a26", 1.3, 2.6)
    band = paint("#e6dfcf", noise=4, bevel=0.2)
    deck = planks("#9a6c40", 1.1)
    rail = planks("#efe6d2", 0.8)
    curb = planks("#5e3f26", 1.0)
    roof_w = transposed(shingles("#4b3f3a", 1.3, 1.7, "top", moss="#6b7a4a"))
    roof_e = transposed(shingles("#4b3f3a", 1.3, 1.7, "bottom", moss="#6b7a4a"))
    under = planks("#7a5638", 1.0)
    capwall = planks("#efe6d2", 1.0, True, 0.75, 0.05)
    dz = MILL["DOOR_Z"]

    # tower: plinth, stone base, brick upper in three tapering stages with white string courses
    oct_layer(m, 0, 8.2, 1.0, stone_d)
    oct_layer(m, 1.0, 7.6, 7.4, stone)
    oct_layer(m, 8.4, 6.9, 5.8, brick, band)
    oct_layer(m, 14.2, 7.15, 0.5, band)
    if not broken:
        oct_layer(m, 14.7, 6.4, 4.3, brick, band)
        oct_layer(m, 19.0, 6.65, 0.5, band)
        oct_layer(m, 19.5, 5.9, 1.9, brick)
        oct_layer(m, 21.4, 6.3, 0.7, curb)
    else:
        jag = jag_fn(31, 0.15, 1.0, 7)
        cyl_y(m, 0, 14.7, 0, 6.4, 4.3, {"up": P(paint("#3a2c22"), ov_mask(lambda *a: False)), "down": brick, "all": P(brick, ov_mask(jag))})
        cyl_y(m, 0, 14.7, 0, 5.7, 0.6, {"up": P(planks("#5e3f26", 1.0), ov_rect("#2a1f17", 2, 2, 4, 3)), "all": paint("#3a2c22")})

    # gallery (stage): deck, brackets, white railing
    ga = 9.9
    gy = 8.4
    if not broken:
        cyl_y(m, 0, gy, 0, ga, 0.6, {"up": deck, "all": curb})
    else:
        k = 0.4142 * ga
        m.box((-ga, gy, -k), (ga, gy + 0.6, k), {"up": deck, "all": curb}, skip=())
        m.box((-k, gy, 0), (k, gy + 0.6, ga), {"up": deck, "all": curb}, skip=())
    for (sx, sz) in ((0, -1), (0, 1), (-1, 0), (1, 0)):
        if broken and sz < 0:
            continue
        L = 2.8
        if sz:
            z = sz * (7.6 + 0.99)
            m.box((-0.3, gy - 1.3, z - L / 2), (0.3, gy - 0.7, z + L / 2), curb, rot=("x", 45 * sz, (0, gy - 1.0, z)), skip=())
        else:
            x = sx * (7.6 + 0.99)
            m.box((x - L / 2, gy - 1.3, -0.3), (x + L / 2, gy - 0.7, 0.3), curb, rot=("z", -45 * sx, (x, gy - 1.0, 0)), skip=())
    ra = ga - 0.35
    for i, (x, z) in enumerate(oct_corners(ra)):
        if broken and i in (0, 7, 6):
            continue
        m.box((x - 0.25, gy + 0.6, z - 0.25), (x + 0.25, gy + 3.0, z + 0.25), rail, skip=())
    if not broken:
        oct_ring(m, gy + 2.85, ra, 0.35, 0.3, rail)
        oct_ring(m, gy + 1.75, ra, 0.25, 0.2, rail)
    else:
        m.box((-ra - 0.15, gy + 2.7, -3.0), (-ra + 0.15, gy + 3.0, 4.0), rail, skip=())
        m.box((-4.0, gy + 2.7, ra - 0.15), (4.0, gy + 3.0, ra + 0.15), rail, skip=())
        m.box((ra - 0.15, gy + 1.6, -4.0), (ra + 0.15, gy + 1.9, 4.0), rail, rot=("x", 22.5, (ra, gy + 1.7, 0)), skip=())
        k = 0.4142 * ga
        m.box((-k, gy - 0.6, -ga), (k, gy, -7.4), {"up": deck, "all": curb}, rot=("x", -22.5, (0, gy, -7.6)), skip=())

    # cap: boat-shaped gable roof, ridge front-to-back; sails hang on the front gable
    hy, hz = MILL["HUB_Y"], MILL["HUB_Z"]
    cw, cz0, cz1 = 5.0, -6.2, 6.0
    cy0, cye = 22.1, 23.1
    if not broken:
        m.box((-cw, cy0, cz0), (cw, cye, cz1), {"up": DARK, "all": curb}, skip=())
        top = roof45z(m, cz0 - 0.9, cz1 + 0.9, 0, cw, cye, 0.7, 0.9, roof_w, roof_e, under, planks("#3a2c24", 1.0))
        tri = P(capwall, ov_mask(tri_keep))
        m.box((-cw, cye, cz0), (cw, cye + cw, cz0 + 0.5), {"north": tri, "south": tri, "all": tri}, skip=("up", "down", "east", "west"))
        m.box((-cw, cye, cz1 - 0.5), (cw, cye + cw, cz1), {"north": tri, "south": tri, "all": tri}, skip=("up", "down", "east", "west"))
        for zf, side in ((cz0 - 0.9, -1), (cz1 + 0.9, 1)):
            barge45z(m, zf, 0, cw, cye, 0.7, 0.9, WHITE, side)
        # finial on the ridge, small rear window
        m.box((-0.2, top - 0.2, cz1 - 1.0), (0.2, top + 0.6, cz1 - 0.6), GOLD, skip=())
        m.box((-0.45, top + 0.5, cz1 - 1.05), (0.45, top + 1.0, cz1 - 0.55), GOLD, skip=())
        win(m, "s", 0, cye + 1.6, cz1, 1.2, 1.4, on, TRIM, None, panes=(1, 1), sill=False)
        # windshaft bearing block on the front gable + shaft out to the hub
        slab(m, "n", -1.4, 1.4, hy - 1.4, hy + 1.4, cz0, 0.5, curb)
        cyl_z(m, 0, hy, (cz0 - 0.5 + hz + 0.9) / 2, 0.7, (cz0 - 0.5) - (hz + 0.9), {"all": metal("#4a4a4f")})
    else:
        # cap blown off: roof panels and the cap frame lying behind the tower
        cx, cz = -8.6, 7.4
        m.box((cx - 3.2, 0, cz - 4.4), (cx + 3.4, 0.7, cz + 4.4), {"up": roof_e, "all": under}, rot=("x", 22.5, (cx, 0.3, cz)), skip=())
        m.box((cx + 3.0, 0, cz - 4.0), (cx + 8.4, 0.7, cz + 4.0), {"up": roof_w, "all": under}, rot=("y", 22.5, (cx + 5.5, 0.3, cz)), skip=())
        m.box((cx - 1.0, 0, cz - 5.6), (cx + 0.2, 1.0, cz + 4.6), planks("#3a2c24", 1.0), rot=("y", -22.5, (cx, 0, cz)))
        tri = P(capwall, ov_mask(jag_fn(35, 0.4, 1.0, 5)))
        m.box((cx + 1.6, 0.7, cz - 6.6), (cx + 6.6, 1.1, cz - 3.2), {"up": tri, "all": capwall}, rot=("y", 45, (cx + 4.0, 0.9, cz - 4.9)), skip=())
        # broken sail arm across the ground at the front-right
        ax, az = 6.0, -4.6
        st = planks("#5e3f26", 1.0)
        lat = planks("#efe6d2", 0.8)
        m.box((ax - 0.45, 0, az - 7.4), (ax + 0.45, 0.8, az + 6.0), st, rot=("y", 22.5, (ax, 0, az)))
        m.box((ax + 0.45, 0.1, az - 6.0), (ax + 3.8, 0.25, az + 4.0), P(cloth("#efe6cf", 2, 4), ov_mask(jag_fn(33, 0.3, 1.0, 6))), rot=("y", 22.5, (ax, 0, az)), skip=())
        for k in range(4):
            zz = az - 5.5 + k * 3.0
            m.box((ax + 0.45, 0.25, zz - 0.2), (ax + 4.0, 0.6, zz + 0.2), lat, rot=("y", 22.5, (ax, 0, az)), skip=())
        m.box((ax + 3.6, 0.25, az - 6.0), (ax + 4.0, 0.6, az + 3.0), lat, rot=("y", 22.5, (ax, 0, az)), skip=())
        rubble(m, -3.0, -10.4, 6, 4.6, 41, [stone, brick, band], 1.0)
        rubble(m, 9.6, 4.0, 5, 2.4, 42, [brick, stone_d], 1.1)
        rubble(m, -10.0, -3.0, 4, 1.8, 43, [brick, curb], 0.9)
        plank_debris(m, [(-6.0, -11.0, 4.0, "y", 22.5, 0.0), (10.4, -7.0, 3.6, "y", -45, 0.0), (2.6, 10.8, 4.4, "y", 0, 0.0),
                         (-11.0, 1.6, 3.6, "y", 45, 0.0)], 7, [deck, rail, curb])

    # front door with stone surround and step
    dw, dh = 1.9, 6.2
    slab(m, "n", -dw - 0.8, -dw, 1.0, dh + 1.7, dz, 0.5, stone_d)
    slab(m, "n", dw, dw + 0.8, 1.0, dh + 1.7, dz, 0.5, stone_d)
    slab(m, "n", -dw - 0.8, dw + 0.8, dh + 1.0, dh + 1.8, dz, 0.55, stone_d)
    m.box((-dw - 1.1, 0, dz - 2.0), (dw + 1.1, 1.0, dz), stone_d)
    door = P(planks("#6b4a2a", 1.0, True, 0.7, 0.05), ov_stripe("#3e2a1a", 0.22, 0.45, False), ov_stripe("#3e2a1a", 0.75, 0.45, False))
    if on:
        slab(m, "n", -dw, dw, 1.0, dh + 1.0, dz + 0.6, 0.1, light("#ffcf7a"))
        slab(m, "n", -dw + 0.3, dw - 0.3, 1.0, 1.4, dz + 0.5, 0.3, paint("#f4efe2", noise=3))
        m.box((-dw - 0.4, 1.0, dz - 3.4), (-dw, dh + 1.0, dz), {"east": door, "west": door, "all": planks("#6b4a2a", 1.0, True)}, skip=())
    elif broken:
        slab(m, "n", -dw, dw, 1.0, dh + 1.0, dz + 0.5, 0.1, DARK)
        m.box((-dw, 1.0, dz - 0.5), (dw, dh + 1.0, dz - 0.1), door, rot=("z", 22.5, (dw, 1.0, dz)), skip=())
    else:
        slab(m, "n", -dw, dw, 1.0, dh + 1.0, dz, 0.25, door)
        slab(m, "n", dw - 1.0, dw - 0.6, 4.0, 4.6, dz - 0.25, 0.25, IRON)
    # lantern beside the door
    slab(m, "n", dw + 1.1, dw + 1.4, 5.4, 6.4, dz, 0.8, IRON)
    m.box((dw + 0.85, 4.4, dz - 1.1), (dw + 1.65, 5.4, dz - 0.3), {"all": light("#ffd36a") if on else glass("#e8d8a0", 200), "up": IRON}, skip=())

    # windows (north one sits between the sail sweep and the tower)
    if not broken:
        win(m, "n", 0, 16.9, -6.4, 1.5, 2.3, on, TRIM, None, panes=(1, 2))
        win(m, "e", 0, 11.6, 6.9, 1.7, 2.5, on, TRIM, "#5e3f26", sw=0.9)
        win(m, "w", 0, 11.6, -6.9, 1.7, 2.5, on, TRIM, "#5e3f26", sw=0.9)
        win(m, "s", 0, 16.9, 6.4, 1.5, 2.3, on, TRIM, None, panes=(1, 2))
        win(m, "e", 1.2, 4.8, 7.6, 1.5, 2.1, on, TRIM, None)
        win(m, "s", 0, 4.8, 7.6, 1.5, 2.1, on, TRIM, None)
    else:
        win(m, "e", 0, 11.6, 6.9, 1.7, 2.5, False, TRIM, None)
        win(m, "w", 0, 11.6, -6.9, 1.7, 2.5, False, TRIM, None)
        slab(m, "e", 1.6, 3.2, 9.0, 13.4, 6.9, 0.3, planks("#5e3f26", 1.0, True))

    # flour sacks, crate by the door
    if not broken:
        sack(m, -4.2, -9.6, 2.6, 2.0)
        sack(m, -6.3, -9.0, 2.4, 2.0, lean=("z", -22.5))
        sack(m, -5.0, -11.4, 2.2, 1.9, col="#e6dcc0", lean=("y", 22.5))
        bx_, bz_ = 5.0, -9.6
        cyl_y(m, bx_, 0, bz_, 1.25, 2.8, {"up": P(planks("#8a6038", 0.7), ov_frame("#3e2a1a", 0.3)), "all": planks("#9a6c40", 0.8, True, 0.7, 0.06)})
        for yy in (0.5, 2.0):
            cyl_y(m, bx_, yy, bz_, 1.32, 0.3, {"all": IRON})
        sack(m, 7.2, -8.6, 1.8, 1.7, col="#e6dcc0", lean=("y", 22.5))
    else:
        sack(m, -4.2, -9.6, 2.0, 2.0, lean=("x", 45))
        sack(m, 5.0, -9.8, 2.2, 2.0, lean=("z", -45))
        m.box((-8.0, 0, -8.6), (-5.0, 0.4, -6.0), paint("#ece6d8", noise=6), skip=("down",))
    if on:
        flour = paint("#f6f2e8", noise=4, bevel=0.05)
        r = random.Random(77)
        for (x, z, w, h) in ((0.0, -9.0, 3.2, 0.25), (-1.6, -10.2, 1.6, 0.18), (1.8, -10.4, 1.4, 0.16), (-3.2, -10.8, 1.2, 0.3)):
            m.box((x - w / 2, 0, z - w * 0.35), (x + w / 2, h, z + w * 0.35), flour, skip=("down",))
        for i in range(7):
            x = r.uniform(-2.4, 2.4)
            y = r.uniform(1.6, 6.8)
            z = dz - 0.6 - r.uniform(0.2, 2.6)
            s = r.uniform(0.35, 0.7)
            m.box((x - s / 2, y - s / 2, z - s / 2), (x + s / 2, y + s / 2, z + s / 2), flour, rot=("y", 45, (x, y, z)) if i % 2 else None, skip=())
        m.box((-7.2, 0, -9.4), (-5.4, 0.4, -7.8), flour, skip=("down",))
    return m


def mill_sails():
    """Four common sails (lattice + canvas) in an X pose, built around the hub at (0, 8, 0) so the
    game can spin the part about Z with pivot [0, 8, 0]. Sails face north (-Z)."""
    m = M("mill_sails", 9250)
    R = MILL["SAIL_R"]
    stock = planks("#5e3f26", 1.0)
    lat = planks("#efe6d2", 0.8)
    canvas = P(cloth("#efe6cf", 2, 4), ov_stripe("#ddd2b6", 0.33, 0.35, True), ov_stripe("#ddd2b6", 0.66, 0.35, True))
    lead = planks("#8a6038", 0.9)
    hub = (0.0, 8.0, 0.0)

    def arm(down, ang):
        def bx(a, b, mat, skip=()):
            (x0, y0, z0), (x1, y1, z1) = a, b
            if down:
                x0, x1 = -x1, -x0
                y0, y1 = 16 - y1, 16 - y0
            m.box((x0, y0, z0), (x1, y1, z1), mat, rot=("z", ang, hub), skip=skip)

        y_in, y_out = 8 + 3.4, 8 + R - 0.4
        bx((-0.45, 8 + 0.8, -0.55), (0.45, 8 + R, 0.35), stock)
        bx((0.45, y_in, 0.15), (4.1, y_out, 0.25), canvas)
        bx((3.9, y_in, -0.35), (4.35, y_out, 0.15), lat)
        bx((0.45, y_out - 0.4, -0.3), (3.9, y_out, 0.15), lat)
        bx((0.45, y_in, -0.3), (3.9, y_in + 0.4, 0.15), lat)
        n = 5
        for k in range(1, n + 1):
            yy = y_in + 0.4 + k * (y_out - y_in - 0.8) / (n + 1)
            bx((0.45, yy - 0.16, -0.3), (3.9, yy + 0.16, 0.1), lat)
        bx((-1.35, y_in + 1.2, -0.25), (-0.45, y_out, 0.05), lead)

    arm(False, 45)
    arm(False, -45)
    arm(True, 45)
    arm(True, -45)
    # hub boss and cross clamps
    cyl_z(m, 0, 8, -0.1, 1.5, 2.0, {"all": metal("#4a4a4f"), "north": metal("#5c5c62")})
    m.box((-0.7, 7.3, -1.45), (0.7, 8.7, -1.1), GOLD, skip=())
    for ang in (45, -45):
        m.box((-0.6, 5.6, -1.0), (0.6, 10.4, -0.6), IRON, rot=("z", ang, hub), skip=())
    return m


# --------------------------------------------------------------------------------------------
# Bakery
# --------------------------------------------------------------------------------------------

BAK = dict(BX0=-14.0, BX1=6.4, BZ0=-6.6, BZ1=7.8, GF=7.4, YE=11.8, JET=0.7, OVEN=(10.8, -2.4), CHIM=(6.4, 9.6, 1.6, 5.2))


def bread_draw(d, W, H, ctx):
    d.rectangle([0, 0, W - 1, H - 1], fill=(236, 224, 196, 255))
    d.rectangle([0, 0, W - 1, H - 1], outline=(94, 63, 38, 255), width=2)
    cx, cy = W / 2, H / 2 + 1
    rx, ry = W * 0.36, H * 0.26
    d.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], fill=(168, 101, 42, 255))
    d.ellipse([cx - rx + 1, cy - ry, cx + rx - 1, cy + ry - 2], fill=(212, 137, 58, 255))
    d.ellipse([cx - rx * 0.6, cy - ry * 0.9, cx + rx * 0.2, cy - ry * 0.1], fill=(232, 168, 90, 255))
    for k in (-0.5, 0.0, 0.5):
        x = cx + k * rx
        d.line([(x + 2, cy - ry * 0.7), (x - 2, cy + ry * 0.5)], fill=(138, 74, 28, 255), width=1)


def scallop_keep(face, u, v, w, h):
    per = 1.3
    t = (u % per) / per
    edge = h * (0.55 + 0.45 * math.sin(t * math.pi))
    return v <= edge


def bakery(state="normal"):
    on = state == "on"
    broken = state == "broken"
    name = "bakery_t1" + {"normal": "", "on": "_on", "broken": "_broken"}[state]
    m = M(name, 9300 + {"normal": 0, "on": 1, "broken": 2}[state])
    B = BAK
    BX0, BX1, BZ0, BZ1, GF, YE, J = B["BX0"], B["BX1"], B["BZ0"], B["BZ1"], B["GF"], B["YE"], B["JET"]
    stone = fieldstone("#b3a58e", "#6e624f", 1.8, 2.9)
    stone_d = fieldstone("#8f8472", "#5a5042", 1.8, 2.9)
    ht = halftimber("#f1e4c6", "#5a3b24", 0.75, 4.4)
    tile_n = shingles("#b65a36", 1.3, 1.6, "top", moss="#7a7a4a")
    tile_s = shingles("#b65a36", 1.3, 1.6, "bottom", moss="#7a7a4a")
    under = planks("#7a5638", 1.2)
    timber = planks("#5a3b24", 1.2)
    brick = bricks("#a8503a", "#5a2a20", 1.3, 2.6)
    clay = bricks("#c07a52", "#7a4a30", 1.1, 2.2)
    trim = WHITE
    UZ0 = BZ0 - J
    zc = (UZ0 + BZ1) / 2
    hs = (BZ1 - UZ0) / 2

    # ground floor: stone with plinth
    m.box((BX0 - 0.35, 0, BZ0 - 0.35), (BX1 + 0.35, 0.9, BZ1 + 0.35), stone_d)
    m.box((BX0, 0.9, BZ0), (BX1, GF, BZ1), stone, skip=("down",))
    # jetty beam + joist ends
    m.box((BX0 - 0.1, GF - 0.1, UZ0 - 0.1), (BX1 + 0.1, GF + 0.6, BZ0 + 0.6), timber, skip=())
    for x in (-11.6, -7.2, -2.8, 1.6, 5.2):
        m.box((x - 0.35, GF - 0.75, UZ0 + 0.1), (x + 0.35, GF - 0.1, BZ0 + 0.4), timber, skip=())
    # upper storey
    if not broken:
        m.box((BX0, GF + 0.6, UZ0), (BX1, YE, BZ1), {"up": DARK, "all": ht}, skip=("down",))
    else:
        jn = jag_fn(51, 0.25, 1.0, 8)
        je = jag_fn(52, 0.5, 1.0, 6)
        mat = {"north": P(ht, ov_mask(jn)), "east": P(ht, ov_mask(je)), "south": ht, "west": ht}
        m.box((BX0, GF + 0.6, UZ0), (BX1, YE, BZ1), mat, skip=("down", "up"))
        inner = planks("#4a3322", 1.3, True, 0.7, 0.05)
        i0 = 0.35
        m.box((BX0 + i0, GF + 0.6, UZ0 + i0), (BX1 - i0, YE - 0.1, UZ0 + i0 + 0.1), {"south": P(inner, ov_mask(jag_fn(53, 0.6, 1.0))), "all": inner}, skip=("down", "up", "north", "east", "west"))
        m.box((BX0 + i0, GF + 0.6, BZ1 - i0 - 0.1), (BX1 - i0, YE - 0.1, BZ1 - i0), {"north": P(inner, ov_mask(jn)), "all": inner}, skip=("down", "up", "south", "east", "west"))
        m.box((BX1 - i0 - 0.1, GF + 0.6, UZ0 + i0), (BX1 - i0, YE - 0.1, BZ1 - i0), {"west": inner, "all": inner}, skip=("down", "up", "north", "south", "east"))
        m.box((BX0 + i0, GF + 0.6, UZ0 + i0), (BX0 + i0 + 0.1, YE - 0.1, BZ1 - i0), {"east": P(inner, ov_mask(je)), "all": inner}, skip=("down", "up", "north", "south", "west"))
        m.box((BX0 + i0, GF + 0.6, UZ0 + i0), (BX1 - i0, GF + 0.8, BZ1 - i0), planks("#7a5638", 1.2), skip=("down",))
    # corner posts on the upper storey
    for x0, x1 in ((BX0 - 0.2, BX0 + 0.6), (BX1 - 0.6, BX1 + 0.2)):
        for z0, z1 in ((UZ0 - 0.2, UZ0 + 0.6), (BZ1 - 0.6, BZ1 + 0.2)):
            m.box((x0, GF + 0.6, z0), (x1, YE, z1), timber, skip=("down",))

    # roof
    ov, fov, t = 1.3, 1.1, 0.75
    rx0, rx1 = BX0 - fov, BX1 + fov
    ridge = planks("#6e3a26", 1.0)
    if not broken:
        top = roof45x(m, rx0, rx1, zc, hs, YE, ov, t, tile_n, tile_s, under, ridge)
        gable_tri_x(m, BX0, -1, zc, hs, YE, halftimber("#f1e4c6", "#5a3b24", 0.75, 4.0, braces=False))
        gable_tri_x(m, BX1, 1, zc, hs, YE, halftimber("#f1e4c6", "#5a3b24", 0.75, 4.0, braces=False))
        for side, xf in ((-1, rx0), (1, rx1)):
            barge45x(m, xf, zc, hs, YE, ov, t, timber, side)
        # front dormer with a round-topped window
        dx = -8.2
        dzf = UZ0 + 0.5
        dyb, dyt = YE + 1.2, YE + 4.9
        m.box((dx - 2.0, dyb, dzf), (dx + 2.0, dyt, -1.6), plaster("#f1e4c6"), skip=("down", "up"))
        win(m, "n", dx, YE + 3.3, dzf, 1.7, 1.7, on, TRIM, None, panes=(2, 2), sill=False)
        c45 = math.sqrt(0.5)
        drun = 2.0 + 0.45
        dL = drun / c45 + 0.35
        dzm = (dzf - 0.7 + 0.0) / 2
        dlen = 0.0 - (dzf - 0.7)
        for s in (-1, 1):
            cxs = dx + s * drun / 2 - s * 0.12
            cys = dyt + 2.0 - drun / 2 + (t / 2) / c45 + 0.12
            m.box((cxs - dL / 2, cys - t / 2, dzm - dlen / 2), (cxs + dL / 2, cys + t / 2, dzm + dlen / 2), {"up": shingles("#b65a36", 1.3, 1.6, "bottom"), "all": under}, rot=("z", 45 * s, (cxs, cys, dzm)), skip=())
        dtop = dyt + 2.0 + t / c45
        m.box((dx - 0.6, dtop - 0.9, dzf - 0.8), (dx + 0.6, dtop + 0.3, 0.0), ridge, rot=("z", 45, (dx, dtop - 0.3, 0)), skip=())
        m.box((dx - 2.0, dyt, dzf), (dx + 2.0, dyt + 2.0, dzf + 0.5), P(plaster("#f1e4c6"), ov_mask(tri_keep)), skip=("up", "down", "east", "west", "south"))
    else:
        top = roof45x(m, rx0, rx1, zc, hs, YE, ov, t, tile_n, tile_s, under, ridge, cap=False, parts=("s",), hole=(0.66, 0.42, 4.2, 3.2, 72))
        gable_tri_x(m, BX0, -1, zc, hs, YE, halftimber("#f1e4c6", "#5a3b24", 0.75, 4.0, braces=False))
        gable_tri_x(m, BX1, 1, zc, hs, YE, halftimber("#f1e4c6", "#5a3b24", 0.75, 4.0, braces=False), mask_extra=jag_fn(54, 0.3, 0.9))
        barge45x(m, rx0, zc, hs, YE, ov, t, timber, -1)
        m.box((rx0, top - 1.3, zc - 0.5), (rx1 - 6.0, top - 0.3, zc + 0.5), ridge, skip=())
        c = math.sqrt(0.5)
        L = hs / c
        for xr in (-12.4, -8.0, -3.6, 0.8):
            yc = YE + hs / 2 + 0.25
            m.box((xr - 0.3, yc - 0.3, zc - hs / 2 - L / 2), (xr + 0.3, yc + 0.3, zc - hs / 2 + L / 2), timber, rot=("x", 45, (xr, yc, zc - hs / 2)), skip=())
        # one rafter snapped and hanging
        m.box((4.8, YE - 5.0, UZ0 - 0.4), (5.4, YE + 0.3, UZ0 + 0.2), timber, rot=("x", 22.5, (5.1, YE, UZ0)), skip=())
        # tiles slid off onto the ground in front and at the side
        m.box((-12.6, 0, -11.4), (-5.2, 0.6, -8.6), {"up": tile_s, "all": under}, rot=("y", 22.5, (-8.9, 0, -10.0)), skip=("down",))
        m.box((8.0, 0.0, 6.4), (13.8, 0.6, 10.4), {"up": tile_s, "all": under}, rot=("x", 22.5, (10.9, 0.3, 8.4)), skip=())
        rubble(m, -2.0, -10.0, 7, 8.0, 61, [clay, stone, brick, timber], 0.9)
        rubble(m, 9.0, 9.0, 4, 2.4, 62, [brick, stone], 1.0)
        plank_debris(m, [(2.0, -11.0, 4.6, "y", -22.5, 0.0), (-13.4, 5.0, 4.0, "y", 45, 0.0), (12.6, -8.6, 3.6, "y", 22.5, 0.0),
                         (-6.0, 10.0, 4.4, "y", 0, 0.0)], 8, [timber, WOOD, under])

    # chimney (external stack on the east gable)
    cx0, cx1, cz0, cz1 = B["CHIM"]
    ch_top = 22.6 if not broken else 13.6
    m.box((BX1, 0, cz0 - 0.4), (cx1 + 0.4, 7.4, cz1 + 0.4), brick)
    m.box((BX1, 7.4, cz0 - 0.4), (cx1 + 0.4, 8.0, cz1 + 0.4), stone_d, skip=())
    if not broken:
        m.box((BX1 - 0.4, 8.0, cz0), (cx1, ch_top, cz1), brick, skip=())
        m.box((BX1 - 0.8, ch_top, cz0 - 0.4), (cx1 + 0.4, ch_top + 0.7, cz1 + 0.4), stone_d, skip=())
        ccx, ccz = (BX1 + cx1) / 2, (cz0 + cz1) / 2
        for k, dzp in enumerate((-0.85, 0.85)):
            cyl_y(m, ccx, ch_top + 0.7, ccz + dzp, 0.6, 1.4 - k * 0.35, {"all": paint("#b8643a", noise=5), "up": light("#ff8a2a") if on else paint("#1d1612")})
    else:
        jag = jag_fn(55, 0.3, 1.0, 5)
        m.box((BX1 - 0.4, 8.0, cz0), (cx1, ch_top, cz1), {"north": P(brick, ov_mask(jag)), "south": P(brick, ov_mask(jag)), "east": P(brick, ov_mask(jag_fn(56, 0.4, 1.0, 4))), "all": brick}, skip=("up", "down"))
        m.box((BX1 - 0.2, 8.0, cz0 + 0.2), (cx1 - 0.2, ch_top - 2.6, cz1 - 0.2), {"up": paint("#1d1612"), "all": brick}, skip=("down",))
        rubble(m, 12.4, 4.6, 6, 2.4, 63, [brick, stone_d], 1.2)

    # bread oven: stone plinth + brick dome, mouth facing north
    ox, oz = B["OVEN"]
    m.box((BX1, 0, oz - 4.2), (ox + 4.3, 2.6, oz + 4.0), {"up": stone_d, "all": stone_d})
    if not broken:
        for (y0, a, h) in ((2.6, 3.8, 1.8), (4.4, 3.2, 1.2), (5.6, 2.3, 0.9), (6.5, 1.2, 0.6)):
            cyl_y(m, ox, y0, oz, a, h, {"all": clay})
    else:
        for (y0, a, h) in ((2.6, 3.8, 1.8),):
            cyl_y(m, ox, y0, oz, a, h, {"all": P(clay, ov_mask(jag_fn(57, 0.45, 1.0, 5))), "up": paint("#2a1c14")})
        rubble(m, ox, oz, 5, 2.6, 64, [clay], 0.9)
    mz = oz - 3.8
    mouth = light("#ff7a1c") if on else paint("#1b1511")
    slab(m, "n", ox - 1.2, ox + 1.2, 2.7, 4.5, mz, 0.15, mouth)
    slab(m, "n", ox - 1.75, ox - 1.2, 2.6, 4.6, mz, 0.45, brick)
    slab(m, "n", ox + 1.2, ox + 1.75, 2.6, 4.6, mz, 0.45, brick)
    slab(m, "n", ox - 1.75, ox + 1.75, 4.5, 5.1, mz, 0.45, brick)
    m.box((ox - 1.9, 2.1, mz - 1.4), (ox + 1.9, 2.6, mz), stone_d, skip=())
    if on:
        for k, (ex, ey) in enumerate(((-0.6, 2.85), (0.2, 3.1), (0.7, 2.85))):
            m.box((ox + ex - 0.3, ey - 0.25, mz + 0.0), (ox + ex + 0.3, ey + 0.25, mz + 0.4), light("#ffd27a"), skip=())
    # peel leaning on the oven
    if not broken:
        m.box((ox + 2.4, 0, mz - 0.6), (ox + 2.7, 7.0, mz - 0.3), planks("#a9794a", 0.6, True), rot=("z", -22.5, (ox + 2.55, 0, mz)), skip=())
        m.box((ox + 1.6, 0, mz - 0.7), (ox + 3.4, 1.8, mz - 0.4), planks("#c9a06a", 0.8, True), rot=("z", -22.5, (ox + 2.55, 0, mz)), skip=())
    # wood pile behind the oven
    le = logs_end()
    bark = planks("#5a3b24", 0.8)
    if not broken:
        for i, (lx, ly) in enumerate(((11.0, 0), (12.6, 0), (14.2, 0), (11.8, 1.5), (13.4, 1.5), (12.6, 3.0))):
            m.box((lx - 0.75, ly, 2.4), (lx + 0.75, ly + 1.5, 7.2), {"north": le, "south": le, "all": bark}, skip=() if ly else ("down",))
    else:
        for i, (lx, lz, ang) in enumerate(((11.6, 3.6, 22.5), (13.8, 6.4, -45), (10.4, 9.6, 45))):
            m.box((lx - 0.75, 0, lz - 2.4), (lx + 0.75, 1.5, lz + 2.4), {"north": le, "south": le, "all": bark}, rot=("y", ang, (lx, 0, lz)))

    # --- front facade ---------------------------------------------------------------------
    # display bay window with loaves
    bx0, bx1 = -12.6, -3.8
    by0, by1 = 0.9, 6.2
    bz = BZ0 - 1.3
    m.box((bx0 - 0.3, by0, bz - 0.2), (bx1 + 0.3, by0 + 1.5, BZ0), {"up": WOOD, "all": P(planks("#6b4a2a", 1.0, True), ov_frame("#3e2a1a", 0.4))})
    m.box((bx0 - 0.3, by1 - 0.6, bz - 0.25), (bx1 + 0.3, by1, BZ0), {"all": P(paint("#3f6b4a", noise=3), ov_frame("#2a4a33", 0.3))}, skip=())
    for x in (bx0, (bx0 + bx1) / 2, bx1):
        m.box((x - 0.3, by0 + 1.5, bz - 0.2), (x + 0.3, by1 - 0.6, bz + 0.3), paint("#3f6b4a", noise=3), skip=())
    back = light("#ffd890") if on else P(planks("#4a3322", 1.0, True), ov_shadow(0.3))
    slab(m, "n", bx0, bx1, by0 + 1.5, by1 - 0.6, BZ0, 0.1, back)
    if not broken:
        slab(m, "n", bx0 + 0.3, bx1 - 0.3, by0 + 1.5, by1 - 0.6, bz + 0.05, 0.05, glass("#cfe6f2", 120))
    m.box((bx0 + 0.3, by0 + 2.9, bz + 0.5), (bx1 - 0.3, by0 + 3.1, BZ0 - 0.1), planks("#a9794a", 0.8), skip=())
    loaf = {"up": P(paint("#d4893a", noise=6), ov_stripe("#8a4a1c", 0.3, 0.4, True), ov_stripe("#8a4a1c", 0.6, 0.4, True)), "all": paint("#b8702e", noise=6)}
    if not broken:
        for k, x in enumerate((-11.6, -9.6, -7.4, -5.2)):
            m.box((x - 0.8, by0 + 1.5, bz + 0.6), (x + 0.8, by0 + 2.4, BZ0 - 0.3), loaf, skip=("down",))
            if k % 2 == 0:
                m.box((x + 0.2, by0 + 3.1, bz + 0.7), (x + 1.6, by0 + 3.8, BZ0 - 0.4), {"up": paint("#e0a050", noise=6), "all": paint("#c07a30", noise=6)}, skip=("down",))
            else:
                cyl_y(m, x + 0.9, by0 + 3.1, (bz + BZ0) / 2, 0.55, 0.9, {"all": paint("#c98a3a", noise=6)}) if k == 1 else None
    # awning
    aw_y = GF - 0.25
    aw_L = 3.9
    stripes = P(paint("#c0392b", noise=3), *[ov_stripe("#f4f0e6", (i + 0.5) / 10, 0.9, False) for i in range(0, 10, 2)])
    stripes_v = P(paint("#c0392b", noise=3), *[ov_stripe("#f4f0e6", (i + 0.5) / 10, 0.9, True) for i in range(0, 10, 2)])
    if not broken:
        m.box((bx0 - 0.7, aw_y - 0.25, BZ0 - aw_L), (bx1 + 0.7, aw_y, BZ0), {"up": stripes_v, "down": stripes_v, "all": stripes}, rot=("x", 22.5, (0, aw_y, BZ0)), skip=())
        vz = BZ0 - aw_L * math.cos(math.radians(22.5))
        vy = aw_y - aw_L * math.sin(math.radians(22.5))
        val = P(stripes_v, ov_mask(scallop_keep))
        m.box((bx0 - 0.7, vy - 1.0, vz - 0.12), (bx1 + 0.7, vy, vz), {"north": val, "south": val, "all": val}, skip=("up", "down", "east", "west"), hd=2)
    else:
        m.box((bx0 - 0.7, aw_y - 0.25, BZ0 - aw_L), (bx1 + 0.7, aw_y, BZ0), {"up": stripes_v, "down": stripes_v, "all": stripes}, rot=("x", -45, (0, aw_y, BZ0)), skip=())
        m.box((bx0 - 0.2, 0, BZ0 - 3.2), (bx0 + 0.6, 0.3, BZ0 - 0.4), paint("#2a2a2e"), rot=("y", 22.5, (bx0, 0, BZ0 - 1.8)), skip=())
        for x, z in ((-9.0, -8.4), (-6.0, -9.2), (-10.6, -9.6)):
            m.box((x - 0.5, 0, z - 0.4), (x + 0.5, 0.15, z + 0.4), paint("#cfe6f2", noise=10), rot=("y", 45, (x, 0, z)), skip=("down",))
    # flower pots either side of the door step
    if not broken:
        for k, px_ in enumerate((-2.7, 4.3)):
            cyl_y(m, px_, 0, BZ0 - 1.1, 0.7, 1.1, {"all": paint("#b8643a", noise=5), "up": paint("#4a3220", noise=8)})
            m.box((px_ - 0.55, 1.1, BZ0 - 1.65), (px_ + 0.55, 2.1, BZ0 - 0.55), paint("#3f7a34", noise=10), skip=("down",))
            m.box((px_ - 0.3, 2.1, BZ0 - 1.4), (px_ + 0.3, 2.6, BZ0 - 0.8), paint(("#e8453c", "#f7d34a")[k], noise=6), skip=("down",))

    # door with glazed top, transom, lantern, step
    dx0, dx1 = -0.9, 2.5
    dcx = (dx0 + dx1) / 2
    door_m = P(paint("#2f5a6a", noise=4), ov_frame("#20404c", 0.4), ov_rect("#20404c", 0.9, 3.8, 1.6, 1.6))
    slab(m, "n", dx0, dx1, 0.9, 6.6, BZ0, 0.2, door_m)
    slab(m, "n", dx0 + 0.6, dx1 - 0.6, 3.6, 5.8, BZ0 - 0.2, 0.08, paint("#ffcf6a" if on else "#34506b", noise=5))
    slab(m, "n", dx1 - 0.9, dx1 - 0.55, 3.0, 3.4, BZ0 - 0.2, 0.3, GOLD)
    slab(m, "n", dx0 - 0.6, dx0, 0.9, 7.2, BZ0, 0.45, timber)
    slab(m, "n", dx1, dx1 + 0.6, 0.9, 7.2, BZ0, 0.45, timber)
    slab(m, "n", dx0 - 0.6, dx1 + 0.6, 6.6, 7.2, BZ0, 0.45, timber)
    m.box((dx0 - 0.9, 0, BZ0 - 1.6), (dx1 + 0.9, 0.9, BZ0), stone_d)
    lx = dx1 + 1.6
    slab(m, "n", lx - 0.15, lx + 0.15, 5.0, 6.2, BZ0, 0.9, IRON)
    m.box((lx - 0.45, 4.0, BZ0 - 1.2), (lx + 0.45, 5.0, BZ0 - 0.4), {"all": light("#ffd36a") if on else glass("#e8d8a0", 200), "up": IRON}, skip=())
    m.box((lx - 0.55, 5.0, BZ0 - 1.3), (lx + 0.55, 5.3, BZ0 - 0.3), IRON, skip=())

    # hanging sign on an iron bracket
    sx_ = 4.4
    if not broken:
        m.box((sx_ - 0.15, GF + 1.6, UZ0 - 3.8), (sx_ + 0.15, GF + 1.9, UZ0), IRON, skip=())
        m.box((sx_ - 0.12, GF + 0.4, UZ0 - 0.9), (sx_ + 0.12, GF + 1.6, UZ0 - 0.6), IRON, rot=("x", 45, (sx_, GF + 1.6, UZ0)), skip=())
        sg = sprite(bread_draw)
        m.box((sx_ - 0.2, GF - 1.4, UZ0 - 3.6), (sx_ + 0.2, GF + 1.25, UZ0 - 0.4), {"east": sg, "west": sg, "all": planks("#6b4a2a", 0.8)}, skip=(), hd=3)
        for zz in (UZ0 - 3.3, UZ0 - 0.7):
            m.box((sx_ - 0.06, GF + 1.25, zz - 0.06), (sx_ + 0.06, GF + 1.6, zz + 0.06), IRON, skip=())
    else:
        sg = sprite(bread_draw)
        m.box((sx_ + 0.6, 0, -10.6), (sx_ + 3.8, 0.4, -7.9), {"up": sg, "all": planks("#6b4a2a", 0.8)}, rot=("y", 22.5, (sx_ + 2.2, 0, -9.2)), hd=3)

    # upper-floor windows with flower boxes
    fz = UZ0
    for k, wx in enumerate((-11.2, -5.2, 1.4)):
        if broken and k == 1:
            continue
        win(m, "n", wx, 9.75, fz, 2.0, 2.4, on, TRIM, "#3f6b4a" if k != 2 else None, sw=0.9)
        if not broken:
            flowerbox(m, "n", wx, 8.0, fz, 3.4, seed=k)
    win(m, "e", -3.6, 9.75, BX1, 2.0, 2.4, on, TRIM, "#3f6b4a", sw=0.9)
    if not broken:
        flowerbox(m, "e", -3.6, 8.0, BX1, 3.4, seed=5)
    win(m, "w", 0.6, 9.75, BX0, 2.0, 2.4, on, TRIM, "#3f6b4a", sw=0.9)
    win(m, "w", -2.0, 4.2, BX0, 2.2, 2.6, on, TRIM, None)
    win(m, "s", -9.0, 9.75, BZ1, 2.0, 2.4, on, TRIM, None)
    win(m, "s", -1.0, 4.2, BZ1, 2.2, 2.6, on, TRIM, None)
    # back door
    slab(m, "s", -7.4, -4.6, 0.9, 6.4, BZ1, 0.2, P(planks("#6b4a2a", 1.0, True), ov_frame("#3e2a1a", 0.4)))
    slab(m, "s", -7.9, -4.1, 6.4, 6.9, BZ1, 0.4, timber)
    if broken:
        rubble(m, -9.0, 9.6, 3, 2.0, 65, [stone, clay], 0.8)
    return m


# --------------------------------------------------------------------------------------------
# Item icons (32 x 32, same Canvas pipeline as icons.py)
# --------------------------------------------------------------------------------------------

def icon_dough():
    c = icons.Canvas()
    c.ellipse(1.5, 20.5, 30.5, 29.5, "#f3eee2")
    c.ellipse(3.0, 21.5, 29.0, 28.5, "#fbf8f0")
    c.ellipse(4.5, 9.0, 27.5, 27.0, "#d9c49a")
    c.ellipse(5.0, 8.5, 27.0, 25.5, "#ecdcb6")
    c.ellipse(7.0, 9.5, 21.0, 19.0, "#f6ead0")
    c.ellipse(9.5, 11.0, 15.5, 15.0, "#fffaf0")
    c.line((17.0, 14.0), (21.5, 18.5), 1.0, "#d6c296")
    c.line((15.5, 16.5), (19.0, 20.5), 0.8, "#dcc9a0")
    for (x, y, r) in ((8.0, 23.5, 0.8), (24.0, 22.5, 0.9), (13.0, 25.0, 0.7), (20.0, 25.2, 0.8), (26.5, 26.0, 0.7), (5.0, 26.0, 0.6)):
        c.ellipse(x - r, y - r, x + r, y + r, "#ffffff")
    return c.finish(21, outline="#5a4630", light=1.06, dark=0.88, noise=3)


def icon_material_wood():
    c = icons.Canvas()
    planks_ = (
        (3.0, 21.0, 26.5, 26.0, "#9a6c40", "#c9a06a"),
        (5.0, 16.0, 28.5, 21.0, "#b07a46", "#dcb07a"),
        (2.5, 11.0, 25.5, 16.0, "#8a5e36", "#c09060"),
        (6.0, 6.0, 27.0, 11.0, "#a87440", "#d8aa72"),
    )
    for x0, y0, x1, y1, col, end in planks_:
        c.rect(x0, y0, x1, y1, "#4a3220")
        c.rect(x0 + 0.6, y0 + 0.6, x1 - 2.6, y1 - 0.6, col)
        c.rect(x0 + 0.6, y0 + 0.6, x1 - 2.6, y0 + 1.6, tint(col, 1.15))
        c.line((x0 + 3, y0 + 3), (x0 + 9, y0 + 3), 0.6, tint(col, 0.8))
        c.line((x0 + 12, y0 + 2.6), (x1 - 6, y0 + 2.6), 0.6, tint(col, 0.82))
        c.rect(x1 - 2.4, y0 + 0.6, x1 - 0.6, y1 - 0.6, end)
        c.rect(x1 - 1.8, y0 + 2.0, x1 - 1.2, y0 + 3.0, tint(end, 0.8))
    for x in (10.0, 20.0):
        c.rect(x, 5.0, x + 1.6, 26.5, "#d8c080")
        c.rect(x + 0.4, 5.0, x + 0.9, 26.5, "#efe0a8")
    c.ellipse(13.0, 1.0, 18.0, 6.0, "#d8c080")
    c.ellipse(14.2, 2.2, 16.8, 4.8, "#8a6a3a")
    c.line((15.5, 5.5), (12.5, 8.5), 0.9, "#d8c080")
    c.line((15.5, 5.5), (18.5, 8.5), 0.9, "#d8c080")
    return c.finish(22)


def icon_material_stone():
    c = icons.Canvas()
    stones = (
        (2.5, 17.5, 14.5, 28.5, "#8e9196"),
        (12.0, 18.5, 28.0, 29.5, "#7d8085"),
        (19.5, 11.5, 30.0, 22.5, "#9a9a92"),
        (6.5, 9.5, 19.5, 21.0, "#a6a9ae"),
        (12.5, 3.0, 23.5, 13.5, "#8a8e96"),
    )
    for x0, y0, x1, y1, col in stones:
        c.ellipse(x0 - 0.7, y0 - 0.7, x1 + 0.7, y1 + 0.7, "#3c3e42")
        c.ellipse(x0, y0, x1, y1, col)
        c.ellipse(x0 + 1.5, y0 + 1.0, x0 + (x1 - x0) * 0.62, y0 + (y1 - y0) * 0.5, tint(col, 1.18))
        c.ellipse(x0 + (x1 - x0) * 0.45, y0 + (y1 - y0) * 0.55, x1 - 1.0, y1 - 1.0, tint(col, 0.85))
    c.line((9, 22), (11, 25), 0.7, "#5e6166")
    c.line((24, 15), (26, 18), 0.7, "#5e6166")
    c.line((16, 6), (18, 9), 0.6, "#5e6166")
    c.ellipse(22.0, 24.0, 24.0, 25.6, "#6e8a4a")
    return c.finish(23)


ICONS = {"dough": icon_dough, "material_wood": icon_material_wood, "material_stone": icon_material_stone}


# --------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------

STYLES = {"coop_t1": "sweep_z", "mill_t1": "sweep_z_rev", "mill_t1_on": "sweep_z_rev", "bakery_t1": "sweep_x_rev", "bakery_t1_on": "sweep_x_rev"}


def all_models():
    return [coop(), coop("broken"), coop_yard(),
            mill(), mill("on"), mill("broken"), mill_sails(),
            bakery(), bakery("on"), bakery("broken")]


def emit(B, assets, m, written):
    NS = B["NS"]
    atlas, els = m.finalize()
    apx = atlas.load()
    for yy in range(atlas.height):
        for xx in range(atlas.width):
            r_, g_, b_, a_ = apx[xx, yy]
            if a_ not in (0, 255):
                apx[xx, yy] = (r_, g_, b_, 255) if a_ >= 128 else (0, 0, 0, 0)
    tex_dir = os.path.join(assets, "textures", "item")
    os.makedirs(tex_dir, exist_ok=True)
    atlas.save(os.path.join(tex_dir, f"{m.name}.png"))
    written.append(f"textures/item/{m.name}.png")
    disp = B["display_for"](m)
    tex = {"0": f"{NS}:item/{m.name}", "particle": f"{NS}:item/{m.name}"}
    B["write_json"](os.path.join(assets, "models", "item", f"{m.name}.json"), {"textures": tex, "elements": els, "display": disp})
    B["write_json"](os.path.join(assets, "items", f"{m.name}.json"), B["item_def"](m.name))
    written += [f"models/item/{m.name}.json", f"items/{m.name}.json"]
    if m.name in STYLES:
        B["stage_models"](m.name, els, tex, STYLES[m.name])
        for k in range(1, B["STAGES"]):
            written += [f"models/item/{m.name}__b{k}.json", f"items/{m.name}__b{k}.json"]
    B["cull_faces"](els, ["body"] * len(els))
    print(f"{m.name:22s} els={len(els):4d} atlas={atlas.width} zfix={getattr(m, 'zfixed', 0)}")


def emit_icon(B, assets, name, fn, written):
    NS = B["NS"]
    img = fn()
    tex_dir = os.path.join(assets, "textures", "item")
    os.makedirs(tex_dir, exist_ok=True)
    img.save(os.path.join(tex_dir, f"{name}.png"))
    B["write_json"](os.path.join(assets, "models", "item", f"{name}.json"), {"parent": "minecraft:item/generated", "textures": {"layer0": f"{NS}:item/{name}"}})
    B["write_json"](os.path.join(assets, "items", f"{name}.json"), B["item_def"](name))
    written += [f"textures/item/{name}.png", f"models/item/{name}.json", f"items/{name}.json"]


def main():
    out = os.path.abspath(sys.argv[1]) if len(sys.argv) > 1 else os.path.join(HERE, "..", "pack_v2")
    only = set(sys.argv[2:])
    assets = os.path.join(out, "assets", "harvestmc")
    B = load_build_helpers(assets)
    written = []
    for m in all_models():
        if only and m.name not in only:
            continue
        emit(B, assets, m, written)
    for name, fn in ICONS.items():
        if only and name not in only:
            continue
        emit_icon(B, assets, name, fn, written)
    print("files", len(written))


if __name__ == "__main__":
    main()
