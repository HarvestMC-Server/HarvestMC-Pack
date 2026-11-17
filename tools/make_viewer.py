import os
root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
t = open(os.path.join(root, "tools", "viewer_template.html"), encoding="utf-8").read()
d = open(os.path.join(root, "preview", "data.json"), encoding="utf-8").read()
out = t.replace("/*DATA*/null", d)
open(os.path.join(root, "preview", "HarvestMC-Models.html"), "w", encoding="utf-8").write(out)
open(os.path.join(root, "preview", "local.html"), "w", encoding="utf-8").write("<!doctype html><html><head><meta charset=utf-8><meta name=viewport content='width=device-width,initial-scale=1'></head><body>" + out + "</body></html>")
print(len(out))
