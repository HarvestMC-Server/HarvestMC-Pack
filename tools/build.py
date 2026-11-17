import base64
import hashlib
import io
import json
import math
import os
import shutil
import sys
import zipfile
from PIL import Image

sys.path.insert(0, os.path.dirname(__file__))
import vehicles
import animals
import icons
import cosmetics
import bld_models
import bld_parts
import trainx2
import machines
import planes
import babies
from rig import rig_for

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PACK = os.path.join(ROOT, "resourcepack")
NS = "harvestmc"
ASSETS = os.path.join(PACK, "assets", NS)
FADES = set()


def write(path, data, mode="w"):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, mode) as f:
        f.write(data)


def write_json(path, obj):
    write(path, json.dumps(obj, indent=2))


def item_def(model_id):
    return {"model": {"type": "minecraft:model", "model": f"{NS}:item/{model_id}"}}


def display_for(m):
    (x0, x1), (y0, y1), (z0, z1) = m.extents()
    ex, ey, ez = x1 - x0, y1 - y0, z1 - z0
    diag = math.hypot(ex, ez)
    fit = max(ey * 0.866 + diag * 0.5, (ex + ez) * 0.707)
    s = round(min(1.6, 15.0 / fit), 3)
    ymid = (y0 + y1) / 2
    ty = round(max(-40, min(40, (8 - ymid) * s)), 3)
    return {
        "gui": {"rotation": [30, 225, 0], "translation": [0, ty, 0], "scale": [s, s, s]},
        "ground": {"rotation": [0, 0, 0], "translation": [0, 3, 0], "scale": [s * 0.5] * 3},
        "fixed": {"rotation": [0, 180, 0], "translation": [0, ty * 0.6, 0], "scale": [s * 0.8] * 3},
        "thirdperson_righthand": {"rotation": [75, 45, 0], "translation": [0, 2.5, 0], "scale": [s * 0.5] * 3},
        "firstperson_righthand": {"rotation": [0, 45, 0], "translation": [0, 2, 0], "scale": [s * 0.5] * 3},
    }


def data_uri(img):
    buf = io.BytesIO()
    img.save(buf, "PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


OPP = {"north": "south", "south": "north", "east": "west", "west": "east", "up": "down", "down": "up"}
AX = {"north": (2, -1), "south": (2, 1), "west": (0, -1), "east": (0, 1), "down": (1, -1), "up": (1, 1)}
STATS = {"before": 0, "after": 0}


def cull_faces(els, labels):
    n = len(els)
    STATS["before"] += sum(len(e["faces"]) for e in els)
    for i in range(n):
        A = els[i]
        if "rotation" in A:
            continue
        for j in range(n):
            if i == j:
                continue
            B = els[j]
            if "rotation" in B or labels[i] != labels[j]:
                continue
            for d in list(A["faces"].keys()):
                ax, sg = AX[d]
                o = OPP[d]
                if o not in B["faces"]:
                    continue
                pa = A["to"][ax] if sg > 0 else A["from"][ax]
                pb = B["from"][ax] if sg > 0 else B["to"][ax]
                if abs(pa - pb) > 0.002:
                    continue
                ok = True
                for k in range(3):
                    if k == ax:
                        continue
                    if A["from"][k] < B["from"][k] - 0.002 or A["to"][k] > B["to"][k] + 0.002:
                        ok = False
                        break
                if ok:
                    del A["faces"][d]
    STATS["after"] += sum(len(e["faces"]) for e in els)


def shift_part(els, idx, pivot):
    import copy
    px, py, pz = pivot
    out = []
    for i in idx:
        e = copy.deepcopy(els[i])
        e["from"] = [round(e["from"][0] - px, 3), round(e["from"][1] - py + 8, 3), round(e["from"][2] - pz, 3)]
        e["to"] = [round(e["to"][0] - px, 3), round(e["to"][1] - py + 8, 3), round(e["to"][2] - pz, 3)]
        if "rotation" in e:
            o = e["rotation"]["origin"]
            e["rotation"]["origin"] = [round(o[0] - px, 3), round(o[1] - py + 8, 3), round(o[2] - pz, 3)]
        for v in e["from"] + e["to"]:
            assert -16 <= v <= 32, ("part range", v)
        out.append(e)
    return out


HINGES = [("part_door_house", "part_door_house__hinge", (-3.5, 0.0, 0.0)), ("part_door_barn", "part_door_barn__hl", (-3.6, 0.0, 0.0)), ("part_door_barn", "part_door_barn__hr", (3.6, 0.0, 0.0)), ("part_hatch", "part_hatch__hinge", (0.0, 0.0, 0.0)), ("part_vent", "part_vent__hinge", (0.0, 6.0, 0.0))]


def hinge_variants():
    import copy
    for src, dst, (px, py, pz) in HINGES:
        mj = json.load(open(os.path.join(ASSETS, "models", "item", f"{src}.json")))
        els = []
        for e in mj["elements"]:
            e = copy.deepcopy(e)
            e["from"] = [round(e["from"][0] - px, 3), round(e["from"][1] - py + 8, 3), round(e["from"][2] - pz, 3)]
            e["to"] = [round(e["to"][0] - px, 3), round(e["to"][1] - py + 8, 3), round(e["to"][2] - pz, 3)]
            if "rotation" in e:
                o = e["rotation"]["origin"]
                e["rotation"]["origin"] = [round(o[0] - px, 3), round(o[1] - py + 8, 3), round(o[2] - pz, 3)]
            els.append(e)
        write_json(os.path.join(ASSETS, "models", "item", f"{dst}.json"), {"textures": mj["textures"], "elements": els})
        write_json(os.path.join(ASSETS, "items", f"{dst}.json"), item_def(dst))


def main():
    if os.path.isdir(PACK):
        shutil.rmtree(PACK)
    models = vehicles.all_models() + animals.all_models() + cosmetics.all_models() + bld_models.all_buildings() + bld_parts.all_parts() + trainx2.all_trainx() + machines.all_machines() + planes.all_planes() + babies.all_babies()
    preview = {"models": [], "icons": []}
    rig_json = {}
    tex_dir = os.path.join(ASSETS, "textures", "item")
    os.makedirs(tex_dir, exist_ok=True)
    for m in models:
        atlas, els = m.finalize()
        apx = atlas.load()
        for yy in range(atlas.height):
            for xx in range(atlas.width):
                r_, g_, b_, a_ = apx[xx, yy]
                if a_ not in (0, 255):
                    apx[xx, yy] = (r_, g_, b_, 255) if a_ >= 128 else (0, 0, 0, 0)
        atlas.save(os.path.join(tex_dir, f"{m.name}.png"))
        ids = [(m.name, atlas)]
        if m.name in FADES:
            for i in (1, 2, 3):
                fa = atlas.copy()
                px = fa.load()
                for y in range(fa.height):
                    for x in range(fa.width):
                        r, g, b, a = px[x, y]
                        px[x, y] = (r, g, b, int(a * 0.25 * i))
                fa.save(os.path.join(tex_dir, f"{m.name}_f{i}.png"))
                ids.append((f"{m.name}_f{i}", fa))
        disp = display_for(m)
        for mid, _ in ids:
            write_json(os.path.join(ASSETS, "models", "item", f"{mid}.json"), {
                "textures": {"0": f"{NS}:item/{mid}", "particle": f"{NS}:item/{mid}"},
                "elements": els,
                "display": disp,
            })
            write_json(os.path.join(ASSETS, "items", f"{mid}.json"), item_def(mid))
        rg = rig_for(m)
        lab = [None] * len(els)
        if rg:
            for part_, info_ in rg.items():
                for i_ in info_["elements"]:
                    lab[i_] = part_
        else:
            lab = ["body"] * len(els)
        cull_faces(els, lab)
        if rg:
            rig_json[m.name] = {"parts": {}}
            for part, info in rg.items():
                pid = f"{m.name}__{part}"
                rig_json[m.name]["parts"][part] = {k: v for k, v in info.items() if k != "elements"}
                rig_json[m.name]["parts"][part]["model"] = pid
                rig_json[m.name]["parts"][part]["centered"] = part != "body"
                for mid, _ in ids:
                    sub = shift_part(els, info["elements"], info["pivot"]) if part != "body" else [els[i] for i in info["elements"]]
                    write_json(os.path.join(ASSETS, "models", "item", f"{mid}__{part}.json"), {
                        "textures": {"0": f"{NS}:item/{mid}", "particle": f"{NS}:item/{mid}"},
                        "elements": sub,
                    })
                    write_json(os.path.join(ASSETS, "items", f"{mid}__{part}.json"), item_def(f"{mid}__{part}"))
        preview["models"].append({
            "name": m.name,
            "size": atlas.width,
            "elements": els,
            "atlas": data_uri(atlas),
            "fades": m.name in FADES,
            "count": len(els),
        })
    for name, fn in icons.ICONS.items():
        img = fn()
        img.save(os.path.join(tex_dir, f"{name}.png"))
        parent = "minecraft:item/handheld" if name in icons.HANDHELD else "minecraft:item/generated"
        write_json(os.path.join(ASSETS, "models", "item", f"{name}.json"), {"parent": parent, "textures": {"layer0": f"{NS}:item/{name}"}})
        write_json(os.path.join(ASSETS, "items", f"{name}.json"), item_def(name))
        preview["icons"].append({"name": name, "png": data_uri(img.resize((256, 256), Image.NEAREST))})
    hinge_variants()
    write_json(os.path.join(ROOT, "src", "main", "resources", "rig.json"), rig_json)
    write_json(os.path.join(PACK, "pack.mcmeta"), {"pack": {"pack_format": 46, "description": "HarvestMC custom models and textures"}})
    icons.ICONS["icon_coin"]().resize((64, 64), Image.NEAREST).save(os.path.join(PACK, "pack.png"))

    out_dir = os.path.join(ROOT, "src", "main", "resources", "pack")
    os.makedirs(out_dir, exist_ok=True)
    zpath = os.path.join(out_dir, "HarvestMC-Pack.zip")
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(PACK):
            for f in sorted(files):
                full = os.path.join(base, f)
                z.write(full, os.path.relpath(full, PACK).replace("\\", "/"))
    sha = hashlib.sha1(open(zpath, "rb").read()).hexdigest()
    write(os.path.join(ROOT, "resourcepack.sha1"), sha)
    os.makedirs(os.path.join(ROOT, "preview"), exist_ok=True)
    write(os.path.join(ROOT, "preview", "data.json"), json.dumps(preview))
    print("faces", STATS)
    print("models", len(models), "icons", len(icons.ICONS), "zip", os.path.getsize(zpath), "sha1", sha)


main()
