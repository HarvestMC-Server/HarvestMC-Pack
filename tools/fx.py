import math
from lib import *


def fx_puff_a():
    m = Model("fx_puff_a", 970)
    a = paint("#dff5cf", noise=10)
    b = paint("#bfe6a2", noise=10)
    c = paint("#f4fbe8", noise=8)
    m.box((-3.4, 5.0, -3.4), (3.4, 11.0, 3.4), a, skip=())
    m.box((-5.2, 6.4, -2.2), (-1.6, 10.2, 2.2), b, skip=())
    m.box((1.6, 5.6, -2.8), (5.4, 9.4, 2.6), c, skip=())
    m.box((-2.2, 9.0, -2.0), (2.6, 12.6, 2.4), c, skip=())
    m.box((-1.8, 3.8, -3.8), (2.2, 7.0, 0.6), b, skip=())
    return m


def fx_puff_b():
    m = Model("fx_puff_b", 971)
    a = paint("#cfeab4", noise=10)
    b = paint("#e8f7d8", noise=10)
    c = paint("#a9d98a", noise=8)
    m.box((-4.0, 6.0, -2.6), (4.0, 10.0, 2.6), a, skip=())
    m.box((-2.6, 4.4, -4.0), (2.6, 8.6, 4.0), b, skip=())
    m.box((-1.4, 8.4, -1.6), (3.4, 12.2, 2.4), c, skip=())
    m.box((-5.4, 5.4, 0.4), (-2.2, 8.4, 3.6), b, skip=())
    m.box((2.4, 6.6, -4.2), (5.6, 9.4, -0.8), a, skip=())
    return m


def fx_mist_a():
    m = Model("fx_mist_a", 974)
    a = paint("#e4f6d6", noise=10)
    b = paint("#c6e8ae", noise=10)
    m.box((-2.2, 6.0, -2.2), (2.2, 10.0, 2.2), a, skip=())
    m.box((-3.4, 6.8, -1.2), (-0.6, 9.4, 1.6), b, skip=())
    m.box((0.8, 7.2, -1.8), (3.6, 9.8, 1.4), b, skip=())
    return m


def fx_mist_b():
    m = Model("fx_mist_b", 975)
    a = paint("#d8f0c4", noise=10)
    b = paint("#f2fbe8", noise=10)
    m.box((-2.6, 6.4, -1.8), (2.0, 9.6, 2.2), a, skip=())
    m.box((-1.2, 8.4, -2.8), (2.6, 11.0, 0.6), b, skip=())
    m.box((-3.2, 5.6, 0.2), (-0.2, 8.4, 3.0), b, skip=())
    return m


def fx_sprout():
    m = Model("fx_sprout", 972)
    leaf = paint("#4fbf3a", noise=6)
    leaf2 = paint("#7ee05a", noise=6)
    bud = paint("#fff3b0", noise=4)
    m.box((-0.4, 0.0, -0.4), (0.4, 5.0, 0.4), leaf, skip=())
    for ang in (0, 90, 180, 270):
        dx = math.cos(math.radians(ang))
        dz = math.sin(math.radians(ang))
        m.box((dx * 1.6 - 0.9, 3.4, dz * 1.6 - 0.9), (dx * 1.6 + 0.9, 4.2, dz * 1.6 + 0.9), leaf2, skip=())
        m.box((dx * 2.8 - 0.8, 4.6, dz * 2.8 - 0.8), (dx * 2.8 + 0.8, 5.4, dz * 2.8 + 0.8), leaf, skip=())
    m.box((-0.8, 5.0, -0.8), (0.8, 6.4, 0.8), bud, skip=())
    return m


def fx_spark():
    m = Model("fx_spark", 973)
    star = light("#fff3b0")
    m.box((-0.3, 3.0, -2.6), (0.3, 13.0, 2.6), star, skip=())
    m.box((-4.6, 7.7, -0.3), (4.6, 8.3, 0.3), star, skip=())
    m.box((-0.3, 7.7, -4.6), (0.3, 8.3, 4.6), star, skip=())
    m.box((-1.2, 6.8, -1.2), (1.2, 9.2, 1.2), light("#ffffff"), skip=())
    return m


def all_fx():
    return [fx_puff_a(), fx_puff_b(), fx_mist_a(), fx_mist_b(), fx_sprout(), fx_spark()]
