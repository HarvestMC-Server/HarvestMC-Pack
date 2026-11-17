import json
import math
import os
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORN = {
    "north": (lambda b: [(b[3], b[4], b[2]), (b[0], b[4], b[2]), (b[0], b[1], b[2]), (b[3], b[1], b[2])], (0, 0, -1)),
    "south": (lambda b: [(b[0], b[4], b[5]), (b[3], b[4], b[5]), (b[3], b[1], b[5]), (b[0], b[1], b[5])], (0, 0, 1)),
    "east": (lambda b: [(b[3], b[4], b[5]), (b[3], b[4], b[2]), (b[3], b[1], b[2]), (b[3], b[1], b[5])], (1, 0, 0)),
    "west": (lambda b: [(b[0], b[4], b[2]), (b[0], b[4], b[5]), (b[0], b[1], b[5]), (b[0], b[1], b[2])], (-1, 0, 0)),
    "up": (lambda b: [(b[0], b[4], b[2]), (b[3], b[4], b[2]), (b[3], b[4], b[5]), (b[0], b[4], b[5])], (0, 1, 0)),
    "down": (lambda b: [(b[0], b[1], b[5]), (b[3], b[1], b[5]), (b[3], b[1], b[2]), (b[0], b[1], b[2])], (0, -1, 0)),
}


def rot_mat(axis, ang):
    a = math.radians(ang)
    c, s = math.cos(a), math.sin(a)
    if axis == "x":
        return np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    if axis == "y":
        return np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])


def render(els, atlas, yaw=35, pitch=24, scale=9.0, size=(560, 560), bg=(0, 0, 0, 0), ss=2, center=None):
    W, H = size[0] * ss, size[1] * ss
    S = scale * ss
    y_, p_ = math.radians(yaw), math.radians(pitch)
    c = np.array([math.sin(y_) * math.cos(p_), math.sin(p_), -math.cos(y_) * math.cos(p_)])
    f = -c
    right = np.cross(f, [0, 1, 0])
    right /= np.linalg.norm(right)
    upv = np.cross(right, f)
    lo = np.array([1e9] * 3)
    hi = np.array([-1e9] * 3)
    for e in els:
        lo = np.minimum(lo, e["from"])
        hi = np.maximum(hi, e["to"])
    center = np.array(center if center is not None else [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2], dtype=float)
    light = np.array([-0.45, 0.8, -0.55])
    light /= np.linalg.norm(light)
    quads = []
    for e in els:
        b = (e["from"][0], e["from"][1], e["from"][2], e["to"][0], e["to"][1], e["to"][2])
        R = None
        org = None
        if "rotation" in e:
            R = rot_mat(e["rotation"]["axis"], e["rotation"]["angle"])
            org = np.array(e["rotation"]["origin"])
        for name, f_ in e["faces"].items():
            fn, n = CORN[name]
            n = np.array(n, float)
            pts = np.array(fn(b), float)
            if R is not None:
                pts = (pts - org) @ R.T + org
                n = R @ n
            if n @ c <= 0.01:
                continue
            quads.append((float(np.mean([p @ c for p in pts])), pts, n, f_["uv"]))
    quads.sort(key=lambda q: q[0])
    canvas = Image.new("RGBA", (W, H), bg)
    aw = atlas.width
    for depth, pts, n, uv in quads:
        sp = []
        for p in pts:
            v = p - center
            sp.append((W / 2 + S * float(v @ right), H / 2 + S * 0.06 * 0 - S * float(v @ upv)))
        TL, TR, BR, BL = sp
        x0, y0 = int(uv[0] / 16 * aw + 0.5), int(uv[1] / 16 * aw + 0.5)
        x1, y1 = int(uv[2] / 16 * aw + 0.5), int(uv[3] / 16 * aw + 0.5)
        pw, ph = max(1, x1 - x0), max(1, y1 - y0)
        tex = atlas.crop((x0, y0, x0 + pw, y0 + ph))
        m = np.array([[TR[0] - TL[0], BL[0] - TL[0]], [TR[1] - TL[1], BL[1] - TL[1]]])
        det = np.linalg.det(m)
        if abs(det) < 1e-3:
            continue
        mi = np.linalg.inv(m)
        a, b_ = mi[0] * pw
        d, e_ = mi[1] * ph
        cc = -(a * TL[0] + b_ * TL[1])
        ff = -(d * TL[0] + e_ * TL[1])
        minx = int(max(0, min(p[0] for p in sp) - 2))
        maxx = int(min(W, max(p[0] for p in sp) + 3))
        miny = int(max(0, min(p[1] for p in sp) - 2))
        maxy = int(min(H, max(p[1] for p in sp) + 3))
        if maxx <= minx or maxy <= miny:
            continue
        ow, oh = maxx - minx, maxy - miny
        ox = cc + a * minx + b_ * miny
        oy = ff + d * minx + e_ * miny
        layer = tex.transform((ow, oh), Image.AFFINE, (a, b_, ox, d, e_, oy), Image.NEAREST)
        k = 0.58 + 0.5 * max(0.0, float(n @ light)) + 0.1 * float(n @ right) * 0
        arr = np.asarray(layer, dtype=np.float32)
        arr[..., :3] = np.clip(arr[..., :3] * k, 0, 255)
        layer = Image.fromarray(arr.astype(np.uint8), "RGBA")
        canvas.alpha_composite(layer, (minx, miny))
    return canvas.resize(size, Image.LANCZOS)


def render_groups(groups, yaw=35, pitch=24, scale=9.0, size=(560, 560), center=None, ss=2):
    W, H = size[0] * ss, size[1] * ss
    S = scale * ss
    y_, p_ = math.radians(yaw), math.radians(pitch)
    c = np.array([math.sin(y_) * math.cos(p_), math.sin(p_), -math.cos(y_) * math.cos(p_)])
    f = -c
    right = np.cross(f, [0, 1, 0])
    right /= np.linalg.norm(right)
    upv = np.cross(right, f)
    center = np.array(center, dtype=float)
    light = np.array([-0.45, 0.8, -0.55])
    light /= np.linalg.norm(light)
    quads = []
    for gi, (els, atlas) in enumerate(groups):
        for e in els:
            b = (e["from"][0], e["from"][1], e["from"][2], e["to"][0], e["to"][1], e["to"][2])
            Rm = None
            org = None
            if "rotation" in e:
                Rm = rot_mat(e["rotation"]["axis"], e["rotation"]["angle"])
                org = np.array(e["rotation"]["origin"])
            for name, f_ in e["faces"].items():
                fn, n = CORN[name]
                n = np.array(n, float)
                pts = np.array(fn(b), float)
                if Rm is not None:
                    pts = (pts - org) @ Rm.T + org
                    n = Rm @ n
                if n @ c <= 0.01:
                    continue
                quads.append((float(np.mean([p @ c for p in pts])), pts, n, f_["uv"], gi))
    quads.sort(key=lambda q: q[0])
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for depth, pts, n, uv, gi in quads:
        atlas = groups[gi][1]
        aw = atlas.width
        sp = []
        for p in pts:
            v = p - center
            sp.append((W / 2 + S * float(v @ right), H / 2 - S * float(v @ upv)))
        TL, TR, BR, BL = sp
        x0, y0 = int(uv[0] / 16 * aw + 0.5), int(uv[1] / 16 * aw + 0.5)
        x1, y1 = int(uv[2] / 16 * aw + 0.5), int(uv[3] / 16 * aw + 0.5)
        pw, ph = max(1, x1 - x0), max(1, y1 - y0)
        tex = atlas.crop((x0, y0, x0 + pw, y0 + ph))
        m = np.array([[TR[0] - TL[0], BL[0] - TL[0]], [TR[1] - TL[1], BL[1] - TL[1]]])
        if abs(np.linalg.det(m)) < 1e-3:
            continue
        mi = np.linalg.inv(m)
        a, b_ = mi[0] * pw
        d, e_ = mi[1] * ph
        cc = -(a * TL[0] + b_ * TL[1])
        ff = -(d * TL[0] + e_ * TL[1])
        minx = int(max(0, min(p[0] for p in sp) - 2))
        maxx = int(min(W, max(p[0] for p in sp) + 3))
        miny = int(max(0, min(p[1] for p in sp) - 2))
        maxy = int(min(H, max(p[1] for p in sp) + 3))
        if maxx <= minx or maxy <= miny:
            continue
        ow, oh = maxx - minx, maxy - miny
        ox = cc + a * minx + b_ * miny
        oy = ff + d * minx + e_ * miny
        layer = tex.transform((ow, oh), Image.AFFINE, (a, b_, ox, d, e_, oy), Image.NEAREST)
        k = 0.58 + 0.5 * max(0.0, float(n @ light))
        arr = np.asarray(layer, dtype=np.float32)
        arr[..., :3] = np.clip(arr[..., :3] * k, 0, 255)
        canvas.alpha_composite(Image.fromarray(arr.astype(np.uint8), "RGBA"), (minx, miny))
    return canvas.resize(size, Image.LANCZOS)


def load_models():
    import base64, io
    data = json.load(open(os.path.join(ROOT, "preview", "data.json")))
    out = {}
    for m in data["models"]:
        out[m["name"]] = (m["elements"], Image.open(io.BytesIO(base64.b64decode(m["atlas"].split(",")[1]))).convert("RGBA"))
    return out


def combo_sheet(pairs, out, cols=4, cell=420, yaw=35, pitch=24, bgc=(46, 54, 36, 255), scale=None):
    models = load_models()
    rows = (len(pairs) + cols - 1) // cols
    im = Image.new("RGBA", (cols * cell, rows * cell), bgc)
    for i, group in enumerate(pairs):
        els, atlas = models[group[0]]
        lo = np.array([1e9] * 3)
        hi = np.array([-1e9] * 3)
        for e in els:
            lo = np.minimum(lo, e["from"])
            hi = np.maximum(hi, e["to"])
        ctr = (lo + hi) / 2
        sc = scale or cell / 44.0
        layer = Image.new("RGBA", (cell, cell), (0, 0, 0, 0))
        for n in group:
            e2, a2 = models[n]
            layer.alpha_composite(render(e2, a2, yaw, pitch, sc, (cell, cell), center=ctr))
        im.alpha_composite(layer, ((i % cols) * cell, (i // cols) * cell))
    im.save(out)


def sheet(names, out, cols=4, cell=300, yaw=35, pitch=24, bgc=(46, 54, 36, 255), scale=None):
    data = json.load(open(os.path.join(ROOT, "preview", "data.json")))
    models = {m["name"]: m for m in data["models"]}
    import base64, io
    rows = (len(names) + cols - 1) // cols
    im = Image.new("RGBA", (cols * cell, rows * cell), bgc)
    for i, n in enumerate(names):
        m = models[n]
        atlas = Image.open(io.BytesIO(base64.b64decode(m["atlas"].split(",")[1]))).convert("RGBA")
        sc = scale or max(2.0, cell / 52.0)
        r = render(m["elements"], atlas, yaw, pitch, sc, (cell, cell))
        im.alpha_composite(r, ((i % cols) * cell, (i // cols) * cell))
    im.save(out)


if __name__ == "__main__":
    import sys
    names = sys.argv[3:]
    sheet(names, sys.argv[1], cols=int(sys.argv[2]), cell=int(os.environ.get("CELL", 420)), yaw=float(os.environ.get("YAW", 35)), pitch=float(os.environ.get("PITCH", 24)))
