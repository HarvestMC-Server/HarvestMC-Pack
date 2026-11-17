# HarvestMC Pack

Resource pack for the HarvestMC Core plugin (Minecraft 1.21.4+, `pack_format` 46) plus the Python generator that builds every model and texture.

- `resourcepack/` is the generated pack (item model definitions, models, textures).
- `tools/` is the generator: `python tools/build.py` rebuilds `resourcepack/`, the zip, `rig.json` (animated model parts) and the SHA-1. Needs Python 3 with Pillow and NumPy.
- Releases (`pack-vN`) hold the zip that servers download. Put the release asset URL and `resourcepack.sha1` in the plugin's `config.yml`.

The generator writes the zip and `rig.json` into the HarvestMC-Core project (`src/main/resources`), so run it from a checkout laid out as `tools/`, `resourcepack/` and the Core `src/` side by side.
