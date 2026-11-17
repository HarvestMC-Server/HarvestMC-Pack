import math


def box(e):
    f, t = e["from"], e["to"]
    return (f[0] - 8, f[1], f[2] - 8, t[0] - 8, t[1], t[2] - 8)


def sgn(v):
    return -1 if v < 0 else 1 if v > 0 else 0


def classify_cow(e):
    x0, y0, z0, x1, y1, z1 = box(e)
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    w = x1 - x0
    if y1 <= 10.0 and w <= 3.6 and abs(cx) > 1.5 and (abs(cz + 4.6) < 2.2 or abs(cz - 6.4) < 2.2):
        return f"leg_{'f' if cz < 0 else 'b'}{'l' if cx < 0 else 'r'}"
    if cz > 9.3 and abs(cx) < 1.2:
        return "tail"
    if cz < -6.2 and cy > 11:
        return "head"
    return "body"


def classify_pig(e):
    x0, y0, z0, x1, y1, z1 = box(e)
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    w = x1 - x0
    if y1 <= 5.5 and w <= 3.4 and abs(cx) > 1.5:
        return f"leg_{'f' if cz < 0 else 'b'}{'l' if cx < 0 else 'r'}"
    if cz > 7.4 and abs(cx) < 1.0 and 10 <= cy <= 13.5:
        return "tail"
    if cz < -6.0 and y1 > 7:
        return "head"
    return "body"


def classify_sheep(e):
    x0, y0, z0, x1, y1, z1 = box(e)
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    w = x1 - x0
    if y1 <= 8.7 and w <= 3.2 and abs(cx) > 1.5 and (abs(cz + 4.2) < 2.0 or abs(cz - 5.6) < 2.0):
        return f"leg_{'f' if cz < 0 else 'b'}{'l' if cx < 0 else 'r'}"
    if cz > 8.2 and w <= 3.2 and abs(cx) < 1.6:
        return "tail"
    if cz < -7.5 and y1 > 11.5:
        return "head"
    return "body"


def classify_chicken(e):
    x0, y0, z0, x1, y1, z1 = box(e)
    cx, cy, cz = (x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2
    w = x1 - x0
    if y1 <= 4.9 and abs(cx) > 0.6:
        return f"leg_{'l' if cx < 0 else 'r'}"
    if abs(cx) > 2.9 and w <= 1.2 and 5.0 <= cy <= 10.5:
        return f"wing_{'l' if cx < 0 else 'r'}"
    if cz > 4.4 and cy > 8 and abs(cx) < 1.8:
        return "tail"
    if cz < -2.0 and y0 >= 9.9:
        return "head"
    return "body"


def classify_npc(e):
    x0, y0, z0, x1, y1, z1 = box(e)
    cx = (x0 + x1) / 2
    if (x0 >= 3.8 and x1 <= 7.4) or (x1 <= -3.8 and x0 >= -7.4):
        return "arm_r" if cx > 0 else "arm_l"
    if y0 >= 19.4:
        return "head"
    if y1 <= 10.6 and abs(cx) < 4.1:
        return "leg_l" if cx < 0 else "leg_r"
    return "body"


PIVOTS = {
    "livestock_cow": {"head": (0, 14.0, -7.0), "leg_fl": (-3.5, 9.8, -4.6), "leg_fr": (3.5, 9.8, -4.6), "leg_bl": (-3.5, 9.8, 6.4), "leg_br": (3.5, 9.8, 6.4), "tail": (0, 18.0, 9.6)},
    "livestock_pig": {"head": (0, 11.0, -6.3), "leg_fl": (-2.9, 5.4, -4.8), "leg_fr": (2.9, 5.4, -4.8), "leg_bl": (-2.9, 5.4, 5.4), "leg_br": (2.9, 5.4, 5.4), "tail": (0, 13.0, 7.5)},
    "livestock_sheep": {"head": (0, 14.5, -7.0), "leg_fl": (-3.0, 8.6, -4.2), "leg_fr": (3.0, 8.6, -4.2), "leg_bl": (-3.0, 8.6, 5.6), "leg_br": (3.0, 8.6, 5.6), "tail": (0, 14.8, 8.5)},
    "livestock_chicken": {"head": (0, 9.8, -3.2), "leg_l": (-1.4, 4.8, 0), "leg_r": (1.4, 4.8, 0), "wing_l": (-3.0, 10.0, 0.5), "wing_r": (3.0, 10.0, 0.5), "tail": (0, 8.0, 4.4)},
    "npc_old_mcdonald": {"head": (0, 22.0, 0), "arm_l": (-5.6, 21.6, 0), "arm_r": (5.6, 21.6, 0), "leg_l": (-2.0, 10.5, 0), "leg_r": (2.0, 10.5, 0)},
}
CLASSIFIERS = {"livestock_cow": classify_cow, "livestock_pig": classify_pig, "livestock_sheep": classify_sheep, "livestock_chicken": classify_chicken, "npc_old_mcdonald": classify_npc}
ROLES = {"head": "head", "tail": "tail", "arm_l": "arm", "arm_r": "arm"}


def role_of(part):
    if part.startswith("leg"):
        return "leg"
    if part.startswith("wing"):
        return "wing"
    if part.startswith("wheel"):
        return "wheel"
    if part.startswith("axle"):
        return "axle"
    if part.startswith("door"):
        return "door"
    if part.startswith("rods"):
        return "crank"
    if part.startswith("main_rod"):
        return "slide"
    return ROLES.get(part, part.split("_")[0])


def meta(part, pivot, extra=None):
    d = {"pivot": [round(pivot[0], 3), round(pivot[1], 3), round(pivot[2], 3)], "role": role_of(part)}
    if part.endswith("_l") or part[-1:] == "l" and part.startswith("leg") or part.endswith("_w"):
        d["side"] = -1
    elif part.endswith("_r") or part[-1:] == "r" and part.startswith("leg") or part.endswith("_e"):
        d["side"] = 1
    else:
        d["side"] = 0
    if part.startswith("leg_f") or part.startswith("leg_b"):
        d["end"] = -1 if part[4] == "f" else 1
    if extra:
        d.update(extra)
    return d


def rig_for(m):
    name = m.name
    parts = {}
    labels = list(m.parts)
    pivots = {}
    if name in CLASSIFIERS:
        labels = [CLASSIFIERS[name](e) for e in m.els]
        pivots = {k: v for k, v in PIVOTS[name].items()}
        extras = {}
    elif name.startswith("tractor_"):
        k = m.k
        wheels = {}
        for (c, a, b) in m.wheel_groups:
            cx, cy, cz, r = c
            rear = cz > 0
            side = "l" if cx < 0 else "r"
            key = f"wheel_{'rear' if rear else 'front'}_{side}"
            for i in range(a, b):
                labels[i] = key
            if key not in wheels or abs(cx) < abs(wheels[key][0]):
                wheels[key] = (cx, cy, cz, r)
        for key, (cx, cy, cz, r) in wheels.items():
            pivots[key] = (cx, cy, cz)
        pivots["steer"] = (0, 15.6 * k, 3.0 * k)
    elif name.startswith("attachment_"):
        wheels = {}
        for (c, a, b) in m.wheel_groups:
            cx, cy, cz, r = c
            key = f"wheel_{'l' if cx < 0 else 'r'}"
            for i in range(a, b):
                labels[i] = key
            wheels[key] = (cx, cy, cz)
        pivots.update(wheels)
        pivots["rotor"] = (0, 4.5, 1.0)
        pivots["reel"] = (0, 11.5, -14.0)
    elif name in ("train_locomotive", "train_tender", "train_wagon", "train_coach"):
        axles = {}
        for (c, a, b) in m.wheel_groups:
            cx, cy, cz, r = c
            axles.setdefault(round(cz, 2), (cy, r, []))[2].append((a, b))
        if name == "train_wagon":
            pivots.update({"door_e": (7.25, 12.8, 0.0), "door_w": (-7.25, 12.8, 0.0)})
        for i, z in enumerate(sorted(axles)):
            cy, r, rng = axles[z]
            key = f"axle_{i + 1}"
            for (a, b) in rng:
                for j in range(a, b):
                    labels[j] = key
            pivots[key] = (0, cy, z)
        if name == "train_locomotive":
            pivots.update({"rods_l": (-6.5, 5.6, -1.0), "rods_r": (6.5, 5.6, -1.0), "main_rod_l": (-6.6, 6.9, -11.0), "main_rod_r": (6.6, 6.9, -11.0)})
    elif name == "cargo_crate":
        pivots["lid"] = (0, 11.0, 6.2)
    else:
        return None
    for i, e in enumerate(m.els):
        parts.setdefault(labels[i], []).append(i)
    if len(parts) <= 1:
        return None
    out = {}
    for part, idx in parts.items():
        p = pivots.get(part, (0, 0, 0))
        extra = {}
        if part.startswith("axle") or part.startswith("wheel"):
            for (c, a, b) in m.wheel_groups:
                if a <= idx[0] < b or any(a <= j < b for j in idx[:4]):
                    extra["radius"] = c[3]
                    break
        out[part] = {"elements": idx, **meta(part, p, extra)}
    return out
