import copy
import json
import math
import os
import sys
import numpy as np
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
import render as R

M = R.load_models()


def place(name, off, rot=None, sy=None, sy_pivot=None):
    els, atlas = M[name]
    out = []
    for e in els:
        e = copy.deepcopy(e)
        for k in ("from", "to"):
            e[k] = [e[k][0] + off[0], e[k][1] + off[1], e[k][2] + off[2]]
        if "rotation" in e:
            o = e["rotation"]["origin"]
            e["rotation"]["origin"] = [o[0] + off[0], o[1] + off[1], o[2] + off[2]]
        if sy is not None:
            for k in ("from", "to"):
                e[k][1] = sy_pivot + (e[k][1] - sy_pivot) * sy
        if rot and "rotation" not in e:
            axis, ang, piv = rot
            e["rotation"] = {"axis": axis, "angle": ang, "origin": [piv[0] + off[0] + 8, piv[1] + off[1], piv[2] + off[2] + 8] if False else [off[0] + piv[0] + 8, off[1] + piv[1], off[2] + piv[2] + 8]}
        out.append(e)
    return out, atlas


def render_multi(groups, yaw, pitch, scale, size, center):
    layer = None
    return R.render_groups(groups, yaw, pitch, scale, size, center)


def build_scene(kind, t):
    base = {"barn": "barn", "mill": "mill", "garage": "garage", "greenhouse": "greenhouse", "silo": "silo", "farm": "farmhouse_t2"}[kind]
    groups = [(M[base][0], M[base][1])]
    if kind == "barn":
        a = 105 * t
        groups.append(place("part_door_barn", (-3.6, 3, -17.7), ("y", a, (-3.6, 0, 0))))
        groups.append(place("part_door_barn", (3.6, 3, -17.7), ("y", -a, (3.6, 0, 0))))
    elif kind == "mill":
        groups.append(place("deco_windmill_blades", (0, 11.5, -13.2), ("z", 360 * t * 0.25, (0, 8, 0))))
    elif kind == "garage":
        sy = 1 - 0.88 * t
        groups.append(place("part_door_garage", (0, 2, -16.4), None, sy, 16.0))
    elif kind == "greenhouse":
        a = 55 * t
        groups.append(place("part_vent", (-8, 6.5, -14.4), ("x", a, (0, 6, 0))))
        groups.append(place("part_vent", (8, 6.5, -14.4), ("x", a, (0, 6, 0))))
    elif kind == "silo":
        groups.append(place("part_gauge", (0, 5 + 14.5 * t, -10.1)))
    elif kind == "farm":
        groups.append(place("part_door_house", (0, 2, -13.5), ("y", 100 * t, (-3.5, 0, 0))))
    return groups


if __name__ == "__main__":
    kinds = ["barn", "mill", "garage", "greenhouse", "silo", "farm"]
    cell = 360
    frames = []
    N = 14
    ts = [i / (N - 1) for i in range(N)] + [1 - i / (N - 1) for i in range(1, N - 1)]
    for t in ts:
        im = Image.new("RGBA", (3 * cell, 2 * cell), (46, 54, 36, 255))
        for i, k in enumerate(kinds):
            g = build_scene(k, t if k != "mill" else (t * 4 % 1.0))
            els0 = g[0][0]
            lo = np.array([1e9] * 3)
            hi = np.array([-1e9] * 3)
            for e in els0:
                lo = np.minimum(lo, e["from"])
                hi = np.maximum(hi, e["to"])
            ctr = (lo + hi) / 2
            ctr[1] = min(ctr[1], 15)
            sc = cell / 62.0
            r = R.render_groups(g, 35, 24, sc, (cell, cell), ctr)
            im.alpha_composite(r, ((i % 3) * cell, (i // 3) * cell))
        frames.append(im.convert("RGB").quantize(128))
    frames[0].save("preview/animations.gif", save_all=True, append_images=frames[1:], duration=70, loop=0)
    print(len(frames))
