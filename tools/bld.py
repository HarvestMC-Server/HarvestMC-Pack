import math
from lib import *
from cosmetics import bricks

TRIM = "#f2eee2"
DARKW = "#2a1d14"


def siding(c="#f2eee2", plank=1.6):
    return planks(c, plank, False, 0.78, 0.05)


def batten(c, bat="#f2eee2"):
    return P(planks(c, 2.4, True, 0.74, 0.05), ov_dots(tint(bat, 0.9), 12, 0))


def shingle(c, rh=2.0, bw=3.0):
    return bricks(c, tint(c, 0.5), rh, bw)


def corrug(c, w=1.0):
    col = rgb(c)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph))
        px = img.load()
        p = max(2, int(w * 3 * DENSITY / 2))
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                t = x % (p * 2)
                k = 1.14 if t < p // 2 + 1 else 1.0 if t < p else 0.84 if t < p + p // 2 + 1 else 0.94
                n = ctx.rng.uniform(-3, 3)
                px[x, y] = (clamp(col[0] * k + n), clamp(col[1] * k + n), clamp(col[2] * k + n), 255)
        return img

    return f


def mesh(color="#9aa0a6", step=2.0, alpha=255):
    col = rgb(color)

    def f(ctx):
        img = Image.new("RGBA", (ctx.pw, ctx.ph), (0, 0, 0, 0))
        px = img.load()
        s = max(2, int(step * DENSITY))
        for y in range(ctx.ph):
            for x in range(ctx.pw):
                if x % s == 0 or y % s == 0:
                    px[x, y] = col + (alpha,)
        return img

    return f


def slab(m, face, a0, a1, y0, y1, c_out, t, mat, skip=()):
    if face == "n":
        return m.box((a0, y0, c_out - t), (a1, y1, c_out), mat, skip=skip)
    if face == "s":
        return m.box((a0, y0, c_out), (a1, y1, c_out + t), mat, skip=skip)
    if face == "e":
        return m.box((c_out, y0, a0), (c_out + t, y1, a1), mat, skip=skip)
    return m.box((c_out - t, y0, a0), (c_out, y1, a1), mat, skip=skip)


def window(m, face, cx, cy, c_out, w, h, lit=False, trim=TRIM, shutter=None, box=None):
    fr = paint(trim, noise=3)
    t = 0.5
    bar = 0.7
    slab(m, face, cx - w / 2, cx + w / 2, cy - h / 2, cy + h / 2, c_out, 0.25, P(paint("#ffcf6a" if lit else "#3b5a78", noise=5), ov_stripe(trim, 0.5, 0.5, True), ov_stripe(trim, 0.5, 0.5, False)), skip=())
    slab(m, face, cx - w / 2 - bar, cx + w / 2 + bar, cy + h / 2, cy + h / 2 + bar, c_out, t, fr, skip=())
    slab(m, face, cx - w / 2 - bar, cx + w / 2 + bar, cy - h / 2 - bar, cy - h / 2, c_out, t, fr, skip=())
    slab(m, face, cx - w / 2 - bar, cx - w / 2, cy - h / 2, cy + h / 2, c_out, t, fr, skip=())
    slab(m, face, cx + w / 2, cx + w / 2 + bar, cy - h / 2, cy + h / 2, c_out, t, fr, skip=())
    if shutter:
        sh = planks(shutter, 1.2, True, 0.7, 0.05)
        slab(m, face, cx - w / 2 - bar - 2.2, cx - w / 2 - bar, cy - h / 2 - bar, cy + h / 2 + bar, c_out, 0.5, sh, skip=())
        slab(m, face, cx + w / 2 + bar, cx + w / 2 + bar + 2.2, cy - h / 2 - bar, cy + h / 2 + bar, c_out, 0.5, sh, skip=())
    if box:
        slab(m, face, cx - w / 2 - 0.6, cx + w / 2 + 0.6, cy - h / 2 - bar - 1.8, cy - h / 2 - bar, c_out, 1.4, planks("#6b4a2a", 1.0), skip=())
        cols = ["#e8453c", "#f7d34a", "#f08ab4", "#f4f0e6", "#9b6fd6"]
        n = int((w + 1.2) // 1.6)
        for i in range(n):
            a = cx - w / 2 - 0.4 + i * 1.6
            fl = paint(cols[i % 5], noise=6)
            slab(m, face, a, a + 1.0, cy - h / 2 - bar, cy - h / 2 - bar + 1.4, c_out + (1.1 if face in "se" else -1.1 + 0.0), 0.6, fl, skip=())


def gable(m, W, D, ye, roof, gmat, ov=1.5, fov=1.5, thick=1.0, ridge="z", ridge_mat=None, deg=22.5, fill=True, wall_t=1.0):
    half = W / 2 + ov
    rise = half * math.tan(math.radians(deg))
    L = half / math.cos(math.radians(deg))
    span_len = D + 2 * fov

    def mk(s0, y0, l0, s1, y1, l1, mat, rot=None, skip=()):
        if ridge == "z":
            m.box((s0, y0, l0), (s1, y1, l1), mat, rot=rot, skip=skip)
        else:
            m.box((l0, y0, s0), (l1, y1, s1), mat, rot=rot, skip=skip)

    for s in (-1, 1):
        cs_ = s * half / 2
        cy = ye + rise / 2
        axis = "z" if ridge == "z" else "x"
        ang = 22.5 * s * (1 if ridge == "z" else -1)
        if deg == 45:
            ang = 45 * s * (1 if ridge == "z" else -1)
        if ridge == "z":
            mk(cs_ - L / 2, cy - thick / 2, -span_len / 2, cs_ + L / 2, cy + thick / 2, span_len / 2, roof, rot=(axis, ang, (cs_, cy, 0)))
        else:
            mk(cs_ - L / 2, cy - thick / 2, -span_len / 2, cs_ + L / 2, cy + thick / 2, span_len / 2, roof, rot=(axis, ang, (0, cy, cs_)))
    mk(-1.3, ye + rise - 0.2, -span_len / 2, 1.3, ye + rise + 0.7, span_len / 2, ridge_mat or roof, skip=())
    if fill:
        n = max(4, int(rise / 0.55))
        step = rise / n
        for side in (-1, 1):
            pos = side * (D / 2 - wall_t / 2)
            for k in range(n):
                y0 = ye + k * step
                hw = min(W / 2, half * (1 - (y0 + step - ye) / rise) - 0.9)
                if hw <= 0.3:
                    continue
                mk(-hw, y0, pos - wall_t / 2, hw, y0 + step + 0.02, pos + wall_t / 2, gmat, skip=())
    return rise


def oct_layers(m, layers, mat_for, cx=0, cz=0):
    y = layers[0][0]
    for (y0, r, h, key) in layers:
        cyl_y(m, cx, y0, cz, r, h, mat_for(key))


def beam(m, a, b, t, mat, rot=None):
    m.box((a[0] - t / 2, a[1], a[2] - t / 2), (b[0] + t / 2, b[1], b[2] + t / 2), mat, rot=rot, skip=())


def post(m, x, z, y0, y1, t, mat):
    m.box((x - t / 2, y0, z - t / 2), (x + t / 2, y1, z + t / 2), mat, skip=())


def fence_run(m, x0, z0, x1, z1, y0, y1, mat_post, mat_rail, step=6):
    import math as mm
    L = mm.hypot(x1 - x0, z1 - z0)
    n = max(1, int(round(L / step)))
    for i in range(n + 1):
        px = x0 + (x1 - x0) * i / n
        pz = z0 + (z1 - z0) * i / n
        post(m, px, pz, y0, y1, 0.8, mat_post)
    xa, xb = sorted((x0, x1))
    za, zb = sorted((z0, z1))
    for yy in (y0 + (y1 - y0) * 0.35, y0 + (y1 - y0) * 0.75):
        m.box((xa - 0.2, yy - 0.3, za - 0.2), (xb + 0.2, yy + 0.3, zb + 0.2), mat_rail, skip=())
