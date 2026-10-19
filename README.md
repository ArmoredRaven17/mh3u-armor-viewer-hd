# MH3U Armor Viewer HD

A fan-made 3D viewer for Monster Hunter 3 Ultimate armour and weapons, built from the **Wii U**
version's models and textures. Same app as the
[MH3U Armor Viewer](https://armoredraven17.github.io/mh3u-armor-viewer/) (3DS data), copied from it
on 2026-10-17 so it looks and works the same. It's kept as its own repository so it has its own size
budget.

**Not published yet.**

## What is different from the 3DS data

For the hunter and the weapons, the Wii U disc carries the same models at the same texture sizes as
the 3DS cart (unlike the monsters, whose Wii U textures are up to eight times larger). What differs
is how the textures are stored:

- **Alpha:** the 3DS stores transparency in 4 bits (16 levels); the Wii U textures (BC3) carry about
  220 levels. Hair, fur, fringes and other cut-out edges blend smoothly instead of in steps.
- **Colour:** a different block compression (BC1 / BC3 instead of ETC1), on average about 6 / 255
  away from the 3DS texels.
- **Weapons:** 21 of the cart's 574 weapon archives are not on the Wii U disc. No weapon in the
  game's tables draws their models (the 3DS app lists them as unused too), so no weapon is lost.
- **Colour board and Skin Tone:** the Wii U picks hair, clothing and feature colours on its own,
  larger colour board, and its Skin Tone slider runs 0-99 over its own skin strip (the 3DS: 0-189).
  The twelve preset colours, the 44 armour pigments and the armour and weapon tables are the same.
  The viewer uses the Wii U's board, preset spots and slider.

## Running it

No build step. Serve `docs/` with any static file server:

    python dev/serve.py 5596

## Contents

    docs/index.html      the page: the shared viewer base's markup (docs/base, pulled from the MHGU
                         Armor Viewer by dev/sync-base.py)
    docs/app.js          the app's logic, docs/game.js its rules, docs/adapter.js its data for the
                         base -- all ported from the MH3U Armor Viewer by dev/port-from-3u.py
    docs/armor.json      the game's armour tables, every player model, the clothing drawn under an
                         empty slot, per helm the hair and face parts it leaves, the colour choices
                         and the motion lists; `_about` says where each comes from
    docs/materials.json  each material's base texture, blend state and colour type
    docs/weapons.json    the game's weapon tables and every weapon model
    docs/mount.json      how the game hangs each weapon part on the hunter
    docs/stances/        per class, every weapon clip and the weapon's placement on every frame
    docs/models/         armour, clothing, face, hair and weapon meshes (.glb), from the Wii U disc
    docs/poses/<g>/      the motion lists, animations only (shared with the 3DS app)
    docs/tex/            textures from the Wii U disc, deduplicated by content hash
    docs/render/         the render core

## Where the data comes from

The scripts live beside this repository in `C:\MH3U-Extract` and read the Wii U disc (US,
`WUP-P-AHDE`). The disc is decrypted locally. Keys and decrypted files are never part of this
repository.

    wiiu_player_extract.py   the player and weapon archives (big-endian ARC) into wiiu/arcx/
    wiiu_convert_armor.py    convert_armor.py / convert_weapons.py on the Wii U files; textures
                             through wiiu_tex.py (GX2 untiling)
    wiiu_build_armor.py      build_armor.py / build_weapons.py on that conversion

What comes from where:

- Wii U: models, mesh tables and textures.
- 3DS: each material's render state and colour type (the 3DS `.mrl` of the same model, after checking
  it names the same textures), and the game's tables (armour, weapons, colours, mount, stances) from the
  3DS executable. The Wii U executable is not read for them.
- Shared: the motion lists, after checking each gender's skeleton is the same on both.

The data has to stay under 900 MB so the published app stays under GitHub Pages' 1 GB limit.

## Credits

See NOTICE.md, and the About dialog in the app.

Monster Hunter 3 Ultimate is © CAPCOM CO., LTD. This is an unofficial fan project and is not
affiliated with or endorsed by Capcom.
