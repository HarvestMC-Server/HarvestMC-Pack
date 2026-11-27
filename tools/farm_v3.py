"""Farm v3: wooden and iron axe / pickaxe, the material_metal icon and two extra crow flight frames.

Standalone like farm_v2.py: it never rebuilds the whole pack, it only writes the models listed below
into an overlay folder with the pack's assets/harvestmc/... layout:

    python farm_v3.py <out pack folder> --base <live pack folder or zip> [name ...]

    <out pack folder>   default ../pack_v3
    --base              the live pack (a folder holding assets/harvestmc, or the release zip). Needed for
                        the crow frames, which reuse the live crow_flap_up model and texture, and used to
                        check that the tool display blocks still match the live stone tools.
    name ...            only write these models / icons

Tools: the stone axe and stone pickaxe are not in this generator any more (they only exist in the live
pack), so the handle elements and display blocks below are copied from the live stone_axe /
stone_pickaxe. The heads are new. Coordinates here are absolute model coordinates (the JSON from/to);
the helper converts them for Model.box, which adds +8 on x/z and negates the rotation angle.

Crow frames: built from the live crow_flap_up elements (same body boxes, UVs and texture), so the body
does not move when the game swaps frames. Only the wings (and, for the glide, the body tilt and a
fanned tail) change. All rotations are single-axis multiples of 22.5 degrees.
"""
import ast
import copy
import io
import json
import math
import os
import random
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from PIL import Image  # noqa: E402
from lib import Model, rgb, tint, lerp, clamp  # noqa: E402
import icons  # noqa: E402


# --------------------------------------------------------------------------------------------
# build.py helpers, loaded without executing build.py's main() (same approach as farm_v2.py)
# --------------------------------------------------------------------------------------------

def load_build_helpers(assets):
    src = open(os.path.join(HERE, "build.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    funcs = {"write", "write_json", "item_def", "display_for", "cull_faces"}
    names = {"NS", "OPP", "AX", "STATS"}
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
# Live pack access (folder or zip)
# --------------------------------------------------------------------------------------------

class Base:
    def __init__(self, path):
        self.path = path
        self.zip = zipfile.ZipFile(path) if path and path.lower().endswith(".zip") else None

    def _read(self, rel):
        rel = "assets/harvestmc/" + rel
        if self.zip:
            return self.zip.read(rel)
        with open(os.path.join(self.path, *rel.split("/")), "rb") as f:
            return f.read()

    def model(self, name):
        return json.loads(self._read(f"models/item/{name}.json"))

    def texture(self, name):
        return Image.open(io.BytesIO(self._read(f"textures/item/{name}.png"))).convert("RGBA")


# --------------------------------------------------------------------------------------------
# Tool materials (painters take a lib.Ctx and return a pw x ph RGBA image)
# --------------------------------------------------------------------------------------------

def _img(ctx):
    return Image.new("RGBA", (ctx.pw, ctx.ph))


def grain(color, dark=0.8, noise=4, ring=3):
    """Wood with the grain along the longer side of the face, dark grain lines, bevelled edges."""
    c = rgb(color)

    def f(ctx):
        img = _img(ctx)
        px = img.load()
        along_y = ctx.ph >= ctx.pw
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                a, b = (x, y) if along_y else (y, x)
                k = 1 + 0.05 * math.sin(b * 0.5 + a * 2.3)
                if (a * 2 + int(b * 0.18 + math.sin(a * 1.7) * 1.5)) % ring == 0:
                    k *= dark
                if ctx.pw > 2 and ctx.ph > 2:
                    if x == 0 or y == 0:
                        k *= 1.08
                    elif x == ctx.pw - 1 or y == ctx.ph - 1:
                        k *= 0.86
                n = ctx.rng.uniform(-noise, noise)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


def plank_head(color, board=1.5, groove=0.62):
    """Plank wood: boards across the short side, grooves between them, grain along the boards."""
    c = rgb(color)

    def f(ctx):
        img = _img(ctx)
        px = img.load()
        pl = max(2, int(round(board * 2)))
        along_y = ctx.ph >= ctx.pw
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                a, b = (x, y) if along_y else (y, x)
                idx = a // pl
                pr = random.Random(idx * 131 + ctx.pw * 7 + ctx.ph)
                k = 1 + pr.uniform(-0.1, 0.1) + 0.05 * math.sin(b * 0.6 + idx * 2.1)
                if a % pl == pl - 1:
                    k *= groove
                elif a % pl == 0:
                    k *= 1.1
                if (b + idx * 3) % 7 == 0 and a % pl != pl - 1:
                    k *= 0.86
                n = ctx.rng.uniform(-3, 3)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


def twine(color="#d9c07a"):
    """Twisted twine: alternating diagonal strands."""
    c = rgb(color)

    def f(ctx):
        img = _img(ctx)
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                k = 1.1 if (x + y) % 2 == 0 else 0.8
                if (x - y) % 4 == 0:
                    k *= 0.86
                n = ctx.rng.uniform(-4, 4)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


STEEL_BANDS = ((0.0, "#dfe6ee"), (0.16, "#ffffff"), (0.3, "#cdd6e0"), (0.52, "#a6b2c0"), (0.66, "#6d7987"), (0.8, "#8e9aa8"), (1.0, "#b7c2ce"))


def _bands(stops, t):
    for (t0, c0), (t1, c1) in zip(stops, stops[1:]):
        if t <= t1:
            return lerp(c0, c1, (t - t0) / (t1 - t0) if t1 > t0 else 0)
    return rgb(stops[-1][1])


def steel(stops=STEEL_BANDS):
    """Polished steel: chrome-like diagonal reflection bands (white highlight, dark band), bright rims.
    Faces too small for the bands get one tone by direction (tops bright, bottoms dark)."""

    def f(ctx):
        img = _img(ctx)
        px = img.load()
        small = ctx.pw <= 2 or ctx.ph <= 2
        flat = {"up": 0.2, "down": 0.66, "north": 0.4, "south": 0.4, "east": 0.3, "west": 0.52}[ctx.face]
        span = ctx.ph + 0.5 * ctx.pw
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                t = flat if small else (y + 0.5 + 0.5 * (ctx.pw - 1 - x)) / span
                col = _bands(stops, t)
                if not small:
                    if x == 0 or y == 0:
                        col = lerp(col, "#ffffff", 0.35)
                    elif x == ctx.pw - 1 or y == ctx.ph - 1:
                        col = lerp(col, "#5d6875", 0.35)
                n = ctx.rng.uniform(-2, 2)
                px[x, y] = (clamp(col[0] + n), clamp(col[1] + n), clamp(col[2] + n), 255)
        return img

    return f


def dark_steel(color="#4d5560"):
    c = rgb(color)

    def f(ctx):
        img = _img(ctx)
        px = img.load()
        for y in range(ctx.ph):
            g = 1.12 - 0.24 * (y + 0.5) / ctx.ph
            for x in range(ctx.pw):
                k = g
                if ctx.pw > 2 and ctx.ph > 2 and (x == 0 or y == 0):
                    k *= 1.25
                n = ctx.rng.uniform(-3, 3)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


def leather(color="#6b4226"):
    """Leather strip wound diagonally round the grip, dark seams between the turns."""
    c = rgb(color)

    def f(ctx):
        img = _img(ctx)
        px = img.load()
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                v = (y + x // 2) % 3
                k = 0.55 if v == 0 else 1.16 if v == 1 else 0.98
                n = ctx.rng.uniform(-4, 4)
                px[x, y] = (clamp(c[0] * k + n), clamp(c[1] * k + n), clamp(c[2] * k + n), 255)
        return img

    return f


# Handle woods: the stone tools use a mid brown (#845b31 average). Wood tier is lighter (birch-like).
HANDLE_WOOD = grain("#c9a26a", dark=0.84)
HANDLE_STONE = grain("#8c6236", dark=0.78)
HEAD_WOOD = plank_head("#93603a")
HEAD_WOOD_END = grain("#b98a58", dark=0.8)
TWINE = twine()
STEEL = steel()
STEEL_D = dark_steel()
LEATHER = leather()


# --------------------------------------------------------------------------------------------
# Model helper in absolute (JSON) coordinates
# --------------------------------------------------------------------------------------------

ALLOWED = (-45.0, -22.5, 0.0, 22.5, 45.0)


class Tool(Model):
    def bx(self, lo, hi, mat, axis=None, angle=0.0, origin=None, label=""):
        """Box from absolute from/to. angle is the JSON angle (right-handed, as Minecraft applies it)."""
        a = (lo[0] - 8, lo[1], lo[2] - 8)
        b = (hi[0] - 8, hi[1], hi[2] - 8)
        rot = None
        if axis and angle:
            assert angle in ALLOWED, angle
            o = origin or [(lo[i] + hi[i]) / 2 for i in range(3)]
            rot = (axis, -angle, (o[0] - 8, o[1], o[2] - 8))
        return self.box(a, b, mat, rot=rot, skip=(), label=label)

    def bar(self, p, q, thick, depth, mat, zc=8.0, overlap=0.5, label=""):
        """Bar in the x/y plane from point p to point q (centreline), any multiple of 22.5 degrees."""
        dx, dy = q[0] - p[0], q[1] - p[1]
        L = math.hypot(dx, dy) + overlap
        ang = math.degrees(math.atan2(dy, dx))
        ang = round(ang / 22.5) * 22.5
        while ang > 90:
            ang -= 180
        while ang <= -90:
            ang += 180
        cx, cy = (p[0] + q[0]) / 2, (p[1] + q[1]) / 2
        if abs(ang) > 45:  # long axis along y, turned the rest of the way
            ang = ang - 90 if ang > 0 else ang + 90
            w, h = thick, L
        else:
            w, h = L, thick
        lo = (cx - w / 2, cy - h / 2, zc - depth / 2)
        hi = (cx + w / 2, cy + h / 2, zc + depth / 2)
        return self.bx(lo, hi, mat, "z" if ang else None, ang, (cx, cy, zc), label)


# The live stone tools' handle (three boxes making a rounded rod) and display blocks, copied verbatim.
HANDLE = (
    ((7.15, -8.0, 7.15), (8.85, 17.0, 8.85)),
    ((6.95, -7.8, 7.7), (9.05, 16.8, 8.3)),
    ((7.7, -7.83, 6.95), (8.3, 16.83, 9.05)),
)

_HELD = {
    "ground": {"rotation": [0, 0, 0], "translation": [0, 2, 0], "scale": [0.5, 0.5, 0.5]},
    "fixed": {"rotation": [0, 180, 0], "translation": [0, 0, 0], "scale": [0.5, 0.5, 0.5]},
    "thirdperson_righthand": {"rotation": [0, 90, 10], "translation": [0, 4, 0.5], "scale": [0.85, 0.85, 0.85]},
    "firstperson_righthand": {"rotation": [0, 90, -20], "translation": [1.13, 3.2, 1.13], "scale": [0.68, 0.68, 0.68]},
}
AXE_DISPLAY = {"gui": {"rotation": [8, 24, 0], "translation": [-0.151, 0.441, 0], "scale": [0.465, 0.465, 0.465]}, **_HELD}
PICK_DISPLAY = {"gui": {"rotation": [8, 24, 0], "translation": [-0.0, 0.689, 0], "scale": [0.481, 0.481, 0.481]}, **_HELD}
DISPLAY_SOURCE = {"wooden_axe": "stone_axe", "iron_axe": "stone_axe", "wooden_pickaxe": "stone_pickaxe", "iron_pickaxe": "stone_pickaxe"}


def handle(m, mat):
    for lo, hi in HANDLE:
        m.bx(lo, hi, mat, label="handle")


def leather_grip(m):
    m.bx((6.82, -7.3, 6.82), (9.18, 2.4, 9.18), LEATHER, label="grip")
    m.bx((6.7, 2.4, 6.7), (9.3, 2.9, 9.3), STEEL_D, label="grip_band")
    m.bx((6.7, -7.96, 6.7), (9.3, -7.3, 9.3), STEEL_D, label="pommel")


# --------------------------------------------------------------------------------------------
# Axes (blade towards -x, poll towards +x, like stone_axe)
# --------------------------------------------------------------------------------------------

def wooden_axe():
    m = Tool("wooden_axe", 301)
    m.display = AXE_DISPLAY
    handle(m, HANDLE_WOOD)
    # carved plank head, a chunky blunt wedge
    m.bx((6.5, 12.0, 6.45), (9.7, 20.0, 9.55), HEAD_WOOD, label="socket")
    m.bx((4.8, 11.6, 6.85), (6.5, 20.4, 9.15), HEAD_WOOD, label="cheek")
    m.bx((3.0, 10.8, 7.1), (4.8, 21.2, 8.9), HEAD_WOOD, label="blade")
    m.bx((1.6, 10.2, 7.3), (3.0, 21.8, 8.7), HEAD_WOOD, label="blade2")
    m.bx((1.0, 10.5, 7.45), (1.6, 21.5, 8.55), HEAD_WOOD_END, label="edge")
    m.bx((9.7, 13.6, 6.85), (12.4, 18.4, 9.15), HEAD_WOOD, label="poll")
    m.bx((12.4, 14.3, 7.15), (14.2, 17.7, 8.85), HEAD_WOOD_END, label="poll2")
    # twine lashing: two wraps round the head, a cross over each face, a wrap round the handle below
    m.bx((6.3, 12.7, 6.25), (9.9, 13.5, 9.75), TWINE, label="wrap_lo")
    m.bx((6.3, 18.5, 6.25), (9.9, 19.3, 9.75), TWINE, label="wrap_hi")
    m.bx((6.0, 15.75, 6.3), (10.2, 16.35, 9.7), TWINE, "z", 45.0, (8.1, 16.05, 8.0), label="cross_a")
    m.bx((6.0, 15.75, 6.3), (10.2, 16.35, 9.7), TWINE, "z", -45.0, (8.1, 16.05, 8.0), label="cross_b")
    m.bx((6.8, 10.7, 6.8), (9.2, 11.5, 9.2), TWINE, label="wrap_handle")
    return m


def iron_axe():
    m = Tool("iron_axe", 302)
    m.display = AXE_DISPLAY
    handle(m, HANDLE_STONE)
    leather_grip(m)
    # forged eye with darker collars
    m.bx((6.6, 12.7, 6.55), (9.4, 19.3, 9.45), STEEL, label="eye")
    m.bx((6.4, 12.0, 6.35), (9.6, 12.7, 9.65), STEEL_D, label="collar_lo")
    m.bx((6.4, 19.3, 6.35), (9.6, 20.0, 9.65), STEEL_D, label="collar_hi")
    # slim bearded blade, darker cutting edge
    m.bx((5.0, 12.9, 7.05), (6.6, 19.1, 8.95), STEEL, label="cheek")
    m.bx((3.4, 11.6, 7.3), (5.0, 20.4, 8.7), STEEL, label="blade")
    m.bx((2.2, 10.0, 7.48), (3.4, 21.9, 8.52), STEEL, label="blade2")
    m.bx((1.8, 9.4, 7.6), (2.2, 22.4, 8.4), STEEL, label="blade3")
    m.bx((1.0, 9.6, 7.7), (1.8, 22.2, 8.3), STEEL_D, label="edge")
    # square hammer poll
    m.bx((9.4, 14.3, 6.95), (12.0, 17.7, 9.05), STEEL, label="poll")
    m.bx((12.0, 13.9, 6.75), (13.4, 18.1, 9.25), STEEL, label="poll_face")
    m.bx((13.4, 14.2, 7.0), (13.8, 17.8, 9.0), STEEL_D, label="poll_strike")
    # rivets on both faces of the eye
    for z0, z1 in ((6.45, 6.55), (9.45, 9.55)):
        m.bx((7.55, 15.55, z0), (8.45, 16.45, z1), STEEL_D, label="rivet")
    return m


# --------------------------------------------------------------------------------------------
# Pickaxes (arms curve down on both sides of the handle, like stone_pickaxe, but each segment
# follows the arc: 0, 22.5, 45 and 67.5 degrees)
# --------------------------------------------------------------------------------------------

def arc_points(x0, y0, segs):
    pts = [(x0, y0)]
    for ang, L in segs:
        a = math.radians(ang)
        x, y = pts[-1]
        pts.append((x + L * math.cos(a), y - L * math.sin(a)))
    return pts


PICK_ARC = ((0.0, 3.6), (22.5, 4.4), (45.0, 4.2), (67.5, 2.4))
PICK_Y = 18.7


def pick_arms(m, sizes, mats, tip=None):
    pts = arc_points(2.0, PICK_Y, PICK_ARC)
    for side in (-1, 1):
        for i in range(len(PICK_ARC)):
            (ax, ay), (bx_, by) = pts[i], pts[i + 1]
            th, dp = sizes[i]
            m.bar((8 + side * ax, ay), (8 + side * bx_, by), th, dp, mats[i], label=f"arm{i}")
        if tip:
            (ax, ay), (bx_, by) = pts[-2], pts[-1]
            ux, uy = bx_ - ax, by - ay
            n = math.hypot(ux, uy)
            L, th, dp, mat = tip
            ex, ey = bx_ + ux / n * L, by + uy / n * L
            m.bar((8 + side * (bx_ - ux / n * 0.4), by - uy / n * 0.4), (8 + side * ex, ey), th, dp, mat, overlap=0.0, label="tip")


def wooden_pickaxe():
    m = Tool("wooden_pickaxe", 303)
    m.display = PICK_DISPLAY
    handle(m, HANDLE_WOOD)
    m.bx((5.7, 16.6, 6.4), (10.3, 20.6, 9.6), HEAD_WOOD, label="hub")
    pick_arms(m, ((3.0, 2.5), (2.7, 2.3), (2.4, 2.1), (2.1, 1.9)), (HEAD_WOOD, HEAD_WOOD, HEAD_WOOD, HEAD_WOOD_END))
    # twine: loops over the hub on both sides of the handle, a wrap round the handle under it
    m.bx((6.2, 16.3, 6.2), (6.95, 20.9, 9.8), TWINE, label="loop_l")
    m.bx((9.05, 16.3, 6.2), (9.8, 20.9, 9.8), TWINE, label="loop_r")
    m.bx((6.8, 15.0, 6.8), (9.2, 15.9, 9.2), TWINE, label="wrap_handle")
    return m


def iron_pickaxe():
    m = Tool("iron_pickaxe", 304)
    m.display = PICK_DISPLAY
    handle(m, HANDLE_STONE)
    leather_grip(m)
    m.bx((5.8, 16.9, 6.5), (10.2, 20.4, 9.5), STEEL, label="hub")
    m.bx((6.5, 16.2, 6.4), (9.5, 16.9, 9.6), STEEL_D, label="collar")
    pick_arms(m, ((2.8, 2.2), (2.3, 2.0), (1.8, 1.7), (1.3, 1.4)), (STEEL, STEEL, STEEL, STEEL), tip=(1.3, 0.8, 1.0, STEEL_D))
    for z0, z1 in ((6.4, 6.5), (9.5, 9.6)):
        m.bx((7.55, 18.2, z0), (8.45, 19.1, z1), STEEL_D, label="rivet")
    return m


TOOLS = (wooden_axe, iron_axe, wooden_pickaxe, iron_pickaxe)


# --------------------------------------------------------------------------------------------
# Icon: material_metal (32 x 32, same Canvas pipeline as icons.py / farm_v2 icons)
# --------------------------------------------------------------------------------------------

INGOT_OUTLINE = "#2b2f35"


def _ingot(c, x, y, w, h, d, sl=2.0):
    """Ingot seen from the front and a little above: top face, sloped front face, right end.
    A dark rim is drawn first so stacked ingots stay separate (finish() only outlines the silhouette)."""
    k = d * 0.9
    sil = [(x, y + d + h), (x + w, y + d + h), (x + w + k - 0.4, y + h * 0.7), (x + w - sl + k, y), (x + sl + k, y), (x + sl, y + d)]
    c.poly(sil, INGOT_OUTLINE)
    c.d.line([(px * icons.SS, py * icons.SS) for px, py in sil + sil[:1]], fill=rgb(INGOT_OUTLINE) + (255,), width=int(1.3 * icons.SS), joint="curve")
    # front face (trapezoid, wider at the bottom)
    c.poly([(x, y + d + h), (x + w, y + d + h), (x + w - sl, y + d), (x + sl, y + d)], "#b3bbc5")
    # right end face
    c.poly([(x + w, y + d + h), (x + w - sl, y + d), (x + w - sl + k, y), (x + w + k - 0.4, y + h * 0.7)], "#7b8490")
    # top face
    c.poly([(x + sl, y + d), (x + w - sl, y + d), (x + w - sl + k, y), (x + sl + k, y)], "#e6ebf0")
    # shine along the top edge, a glint on the front, a shadow line at the base
    c.line((x + sl + 0.8, y + d - 0.8), (x + w - sl - 1.2, y + d - 0.8), 0.9, "#ffffff")
    c.line((x + sl + 0.2, y + d + 1.3), (x + sl + 3.6, y + d + 1.3), 0.8, "#dde3ea")
    c.line((x + 0.8, y + d + h - 0.6), (x + w - 0.8, y + d + h - 0.6), 0.9, "#8d96a1")


def icon_material_metal():
    c = icons.Canvas()
    _ingot(c, 1.5, 18.0, 15.0, 6.0, 3.6)
    _ingot(c, 13.0, 20.0, 15.0, 6.0, 3.6)
    _ingot(c, 7.0, 9.5, 15.0, 6.0, 3.6)
    # sparkle
    c.rect(27.0, 2.0, 28.0, 9.0, "#eef6ff")
    c.rect(24.0, 5.0, 31.0, 6.0, "#eef6ff")
    c.rect(27.0, 5.0, 28.0, 6.0, "#ffffff")
    return c.finish(24, outline=INGOT_OUTLINE, light=1.08, dark=0.86, noise=3)


ICONS = {"material_metal": icon_material_metal}


# --------------------------------------------------------------------------------------------
# Crow frames, derived from the live crow_flap_up
# --------------------------------------------------------------------------------------------

CROW_SRC = "crow_flap_up"
CROW_BODY_ORIGIN = [8.0, 5.8, 8.1]  # centre of the body box (5.4..10.6, 3.6..8.0, 4.6..11.6)


def _crow_parts(src):
    els = src["elements"]
    wings = [i for i, e in enumerate(els) if e.get("rotation", {}).get("axis") == "z"]
    tail = max(range(len(els)), key=lambda i: els[i]["to"][2] if i not in wings else -1e9)
    return els, wings, tail


def crow_flap_mid(src):
    """Wings level: halfway between flap_up (+50 deg tip up) and flap_down (35 deg tip down), on the 22.5 grid."""
    els, wings, _ = _crow_parts(src)
    out = copy.deepcopy(els)
    for i in wings:
        del out[i]["rotation"]
    return out


def crow_glide(src):
    """Wings spread flat and swept back 22.5 deg, tail fanned, whole body pitched 22.5 deg nose down."""
    els, wings, tail = _crow_parts(src)
    out = []
    tilt = {"angle": -22.5, "axis": "x", "origin": list(CROW_BODY_ORIGIN)}
    for i, e in enumerate(els):
        e = copy.deepcopy(e)
        if i in wings:
            root_x = e["rotation"]["origin"][0]
            left = e["from"][0] < root_x - 0.01
            e["rotation"] = {"angle": 22.5 if left else -22.5, "axis": "y", "origin": e["rotation"]["origin"]}
            out.append(e)
            continue
        if i == tail:
            faces = e["faces"]
            fan = (
                ((6.1, 4.3, 11.4), (9.9, 5.9, 14.2)),
                ((5.1, 4.6, 14.0), (10.9, 5.6, 16.4)),
                ((4.3, 4.8, 16.2), (11.7, 5.4, 18.0)),
            )
            for k, (lo, hi) in enumerate(fan):
                out.append({"name": f"tail{k}", "from": list(lo), "to": list(hi), "faces": copy.deepcopy(faces), "rotation": dict(tilt, origin=list(CROW_BODY_ORIGIN))})
            continue
        e["rotation"] = dict(tilt, origin=list(CROW_BODY_ORIGIN))
        out.append(e)
    return out


CROW_FRAMES = {"crow_flap_mid": crow_flap_mid, "crow_glide": crow_glide}


# --------------------------------------------------------------------------------------------
# Checks
# --------------------------------------------------------------------------------------------

def check_elements(name, els):
    for e in els:
        for v in e["from"] + e["to"]:
            assert -16 <= v <= 32, (name, e.get("name"), v)
        r = e.get("rotation")
        if r:
            assert r["axis"] in ("x", "y", "z"), (name, r)
            assert float(r["angle"]) in ALLOWED, (name, e.get("name"), r["angle"])
            for v in r["origin"]:
                assert -16 <= v <= 32, (name, "origin", v)


def check_handle(name, els):
    got = [(tuple(e["from"]), tuple(e["to"])) for e in els[:3]]
    assert got == [(lo, hi) for lo, hi in HANDLE], (name, "handle moved", got)


# --------------------------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------------------------

def snap_alpha(img):
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a not in (0, 255):
                px[x, y] = (r, g, b, 255) if a >= 128 else (0, 0, 0, 0)
    return img


def emit_tool(B, assets, m, written, base):
    NS = B["NS"]
    atlas, els = m.finalize()
    snap_alpha(atlas)
    check_elements(m.name, els)
    check_handle(m.name, els)
    if base:
        live = base.model(DISPLAY_SOURCE[m.name])["display"]
        assert live == m.display, (m.name, "display differs from live", DISPLAY_SOURCE[m.name])
    tex_dir = os.path.join(assets, "textures", "item")
    os.makedirs(tex_dir, exist_ok=True)
    atlas.save(os.path.join(tex_dir, f"{m.name}.png"))
    tex = {"0": f"{NS}:item/{m.name}", "particle": f"{NS}:item/{m.name}"}
    B["write_json"](os.path.join(assets, "models", "item", f"{m.name}.json"), {"textures": tex, "elements": els, "display": m.display})
    B["write_json"](os.path.join(assets, "items", f"{m.name}.json"), B["item_def"](m.name))
    written += [f"textures/item/{m.name}.png", f"models/item/{m.name}.json", f"items/{m.name}.json"]
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
    print(f"{name:22s} icon {img.width}x{img.height}")


def emit_crow(B, assets, name, fn, written, base):
    NS = B["NS"]
    src = base.model(CROW_SRC)
    els = fn(src)
    check_elements(name, els)
    tex_dir = os.path.join(assets, "textures", "item")
    os.makedirs(tex_dir, exist_ok=True)
    base.texture(CROW_SRC).save(os.path.join(tex_dir, f"{name}.png"))
    tex = {"0": f"{NS}:item/{name}", "particle": f"{NS}:item/{name}"}
    B["write_json"](os.path.join(assets, "models", "item", f"{name}.json"), {"textures": tex, "elements": els, "display": copy.deepcopy(src["display"])})
    B["write_json"](os.path.join(assets, "items", f"{name}.json"), B["item_def"](name))
    written += [f"textures/item/{name}.png", f"models/item/{name}.json", f"items/{name}.json"]
    print(f"{name:22s} els={len(els):4d} (from {CROW_SRC})")


def main():
    args = sys.argv[1:]
    base_path = None
    if "--base" in args:
        i = args.index("--base")
        base_path = os.path.abspath(args[i + 1])
        del args[i:i + 2]
    out = os.path.abspath(args[0]) if args else os.path.join(HERE, "..", "pack_v3")
    only = set(args[1:])
    base = Base(base_path) if base_path else None
    assets = os.path.join(out, "assets", "harvestmc")
    B = load_build_helpers(assets)
    written = []
    for fn in TOOLS:
        m = fn()
        if only and m.name not in only:
            continue
        emit_tool(B, assets, m, written, base)
    for name, fn in ICONS.items():
        if only and name not in only:
            continue
        emit_icon(B, assets, name, fn, written)
    for name, fn in CROW_FRAMES.items():
        if only and name not in only:
            continue
        if not base:
            print(f"{name:22s} skipped: needs --base <live pack> for {CROW_SRC}")
            continue
        emit_crow(B, assets, name, fn, written, base)
    print("files", len(written))


if __name__ == "__main__":
    main()
