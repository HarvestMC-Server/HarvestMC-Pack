import json
import math
import os
from PIL import Image
from lib import *

GLYPHS = {
    "": ["..##....", "..##.###", "########", "#.######", "########", ".##..##.", "........", "........"],
    "": ["........", ".######.", "##.##.##", "#..##..#", "##.##.##", ".######.", "........", "........"],
    "": ["...#....", "..##.#..", ".#.#.##.", "..##.#..", ".#.#.##.", "..##.#..", "...#....", "...#...."],
    "": ["..####..", ".######.", ".##..##.", ".##..##.", "..####..", "...##...", "...#....", "........"],
    "": ["...##...", "..####..", ".######.", ".######.", ".######.", "########", "...##...", "........"],
    "": ["...#....", "..###...", ".#####..", "#######.", ".#####..", "..###...", "...#....", "........"],
}

TONES = {"#": (255, 255, 255, 255), "+": (222, 222, 222, 255)}


def glyph_sheet():
    keys = list(GLYPHS)
    img = Image.new("RGBA", (8 * len(keys), 8), (0, 0, 0, 0))
    px = img.load()
    for i, k in enumerate(keys):
        for y, row in enumerate(GLYPHS[k]):
            for x, ch in enumerate(row):
                if ch == "#":
                    px[i * 8 + x, y] = TONES["#"] if y < 4 else TONES["+"]
    return img, "".join(keys)


def overlay_cinema(size=256):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    px = img.load()
    bar = int(size * 0.115)
    soft = int(size * 0.06)
    for y in range(size):
        edge = min(y, size - 1 - y)
        for x in range(size):
            a = 0.0
            if edge < bar:
                a = 1.0
            elif edge < bar + soft:
                a = 1.0 - (edge - bar) / soft
            dx = (x - size / 2) / (size / 2)
            dy = (y - size / 2) / (size / 2)
            r = math.sqrt(dx * dx + dy * dy)
            vig = max(0.0, (r - 0.78) / 0.7) ** 1.6 * 0.55
            a = min(1.0, a + vig * (1.0 - a))
            px[x, y] = (6, 5, 4, int(a * 255))
    return img


def write_assets(assets):
    sheet, chars = glyph_sheet()
    tex = os.path.join(assets, "textures", "font")
    os.makedirs(tex, exist_ok=True)
    sheet.save(os.path.join(tex, "cutscene.png"))
    font = {"providers": [{"type": "bitmap", "file": "harvestmc:font/cutscene.png", "ascent": 7, "height": 8, "chars": [chars]}]}
    fdir = os.path.join(os.path.dirname(os.path.dirname(assets)), "assets", "minecraft", "font")
    os.makedirs(fdir, exist_ok=True)
    with open(os.path.join(fdir, "default.json"), "w") as f:
        json.dump(font, f, indent=2)
    mdir = os.path.join(assets, "textures", "misc")
    os.makedirs(mdir, exist_ok=True)
    overlay_cinema().save(os.path.join(mdir, "cinema.png"))
    idir = os.path.join(assets, "items")
    os.makedirs(idir, exist_ok=True)
    with open(os.path.join(idir, "cutscene_overlay.json"), "w") as f:
        json.dump({"model": {"type": "minecraft:empty"}}, f, indent=2)


def station_sign():
    m = Model("cutscene_sign", 960)
    wood = planks("#4a3320", 3)
    gold = metal("#c9962f")
    dark = metal("#202226")
    board = paint("#1f3a2c", noise=4)
    face = P(board, ov_frame("#d6a238", 0.7), ov_text("NEXT STOP", "#f4e3c1", 8), ov_stripe("#d6a238", 0.78, 0.4, False))
    for s in (-1, 1):
        m.box((s * 11.0 - 0.9, 0, -0.9), (s * 11.0 + 0.9, 21.0, 0.9), wood)
        m.box((s * 11.0 - 1.8, 0, -1.8), (s * 11.0 + 1.8, 1.4, 1.8), dark, skip=())
        m.box((s * 14.0 - 0.5, 14.0, -0.5), (s * 14.0 + 0.5, 15.2, 0.5), dark, skip=())
        m.box((s * 14.0 - 1.1, 11.2, -1.1), (s * 14.0 + 1.1, 14.0, 1.1), light("#ffe9a0"), skip=())
        m.box((s * 14.0 - 1.4, 10.6, -1.4), (s * 14.0 + 1.4, 11.2, 1.4), dark, skip=())
    m.box((-13.0, 13.0, -1.2), (13.0, 21.6, 1.2), {"north": face, "south": face, "all": board}, skip=())
    m.box((-13.6, 21.6, -1.6), (13.6, 22.6, 1.6), gold, skip=())
    m.box((-13.6, 12.2, -1.6), (13.6, 13.0, 1.6), gold, skip=())
    m.box((-12.0, 22.6, -1.0), (12.0, 23.4, 1.0), dark, skip=())
    return m


def platform_lamp():
    m = Model("cutscene_lamp", 961)
    dark = metal("#202226")
    gold = metal("#c9962f")
    m.box((-2.2, 0, -2.2), (2.2, 1.6, 2.2), dark)
    m.box((-1.4, 1.6, -1.4), (1.4, 3.2, 1.4), gold, skip=())
    m.box((-0.6, 3.2, -0.6), (0.6, 22.0, 0.6), dark, skip=())
    m.box((-0.6, 22.0, -0.6), (4.4, 22.8, 0.6), dark, skip=())
    m.box((3.0, 17.4, -1.6), (5.8, 21.6, 1.6), light("#ffe9a0"), skip=())
    m.box((2.6, 21.6, -2.0), (6.2, 22.6, 2.0), gold, skip=())
    m.box((2.6, 16.6, -2.0), (6.2, 17.4, 2.0), gold, skip=())
    return m


def luggage_cart():
    m = Model("cutscene_cart", 962)
    wood = planks("#8a6a48", 1.4)
    dark = metal("#2a2d33")
    crate = P(planks("#a8825a", 1.6), ov_frame("#4a3320", 0.6))
    sack = paint("#c9ad72", noise=8)
    m.box((-6.0, 3.0, -9.0), (6.0, 4.4, 9.0), wood)
    for s in (-1, 1):
        m.box((s * 6.0 - 0.3, 4.4, -9.0), (s * 6.0 + 0.3, 7.0, 9.0), dark, skip=())
        for z in (-6.0, 6.0):
            wheel(m, s * 6.8, 2.2, z, 2.2, 1.0, "#25272b", "#b8bcc2", "#8d9096", lug=False)
    m.box((-6.0, 4.4, -9.3), (6.0, 7.0, -8.7), dark, skip=())
    m.box((-0.5, 4.0, 9.0), (0.5, 5.0, 16.0), dark, skip=())
    m.box((-5.2, 4.4, -7.8), (-0.4, 9.6, -2.6), crate)
    m.box((0.6, 4.4, -7.8), (5.4, 8.4, -3.0), crate)
    m.box((-4.8, 4.4, 0.2), (-0.8, 7.6, 4.2), sack)
    m.box((0.2, 4.4, 1.0), (4.8, 8.0, 5.6), sack)
    m.box((-4.0, 9.6, -6.8), (-1.2, 12.0, -3.6), crate)
    return m


def all_cutscene():
    return [station_sign(), platform_lamp(), luggage_cart()]
