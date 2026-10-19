"""PORT THE MH3U ARMOR VIEWER'S APP CODE INTO THE HD VIEWER (Phase 1.5 of C:\\Coding Repos\\VIEWER-BASE-PLAN.md).

    python dev/port-from-3u.py            # copy + anchor-replace from ..\\MH3U-Armor-Viewer's working tree
    python dev/port-from-3u.py --check    # list what a port would change, write nothing

The HD viewer is the 3U viewer on the Wii U version's models and textures (wiiu_build_armor.py builds its data). Its app
code is the 3U viewer's, so a change made there is ported here by re-running this: the 3U files are copied, then every
HD difference is applied as an anchor replace that must match exactly once (a 3U edit that moves an anchor stops the
port instead of silently dropping an HD difference). The shared base itself (docs/base) is not copied from 3U: it is
pulled from upstream with dev/sync-base.py --pull.

The HD differences: the title, the Links modal's rows (the 3DS viewer linked, this one "you are here"), the About text
and credits (the Wii U models and textures, the GX2 tiling reference), the storage prefix (-hd) (3U's game.js reads the old shared backdrop key once, keyed off the prefix), the save / capture / set file names, and the Wii U's own colour board and Skin Tone strip
(notes/armor.md "Wii U colours"): the board image and region, the 0-99 slider, a 3DS-board pixel or 3DS skin index in an
older save kept as its RGB.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
HD = os.path.dirname(HERE)
U3 = os.path.join(os.path.dirname(HD), 'MH3U-Armor-Viewer')

# the 3U viewer's own files that the HD viewer takes (data files are built for the HD viewer by wiiu_build_armor.py)
COPY = ['docs/index.html', 'docs/app.js', 'docs/game.js', 'docs/adapter.js', 'docs/render/piece.js',
        'docs/guild-card-titles.json']
# the render copies the base replaced (3U deleted them in Phase 1.3)
DELETE = ['docs/render/' + n + '.js' for n in
          ('assets', 'fx', 'grid', 'lens', 'material', 'materials-db', 'pose', 'skeleton', 'stage')]

R = {}
R['docs/index.html'] = [
    ('<title>MH3U Armor Viewer</title>', '<title>MH3U Armor Viewer HD</title>'),
    ('<h1>MH3U Armor Viewer</h1>', '<h1>MH3U Armor Viewer HD</h1>'),
    # the Links modal: 3U's lists every MH3U app in the hub's order with its own row "you are here" and HD's a link; HD
    # swaps the two (3U's row becomes the link, HD's the "you are here" one), keeping each row's text as 3U has it
    ('''      <li class="current">
        <span class="app-name">Armor Viewer <span class="app-here">you are here</span></span>
        <span class="app-desc">Renders a hunter in 3D with every MH3U armor piece swappable, so you can mix and match a set.</span>
      </li>
      <li>
        <a href="https://armoredraven17.github.io/mh3u-armor-viewer-hd/" target="_blank" rel="noopener">Armor Viewer HD</a>
        <span class="app-desc">The Armor Viewer with the Wii U version's models and textures.</span>
      </li>
''', '''      <li>
        <a href="https://armoredraven17.github.io/mh3u-armor-viewer/" target="_blank" rel="noopener">Armor Viewer</a>
        <span class="app-desc">Renders a hunter in 3D with every MH3U armor piece swappable, so you can mix and match a set.</span>
      </li>
      <li class="current">
        <span class="app-name">Armor Viewer HD <span class="app-here">you are here</span></span>
        <span class="app-desc">The Armor Viewer with the Wii U version's models and textures.</span>
      </li>
'''),
    ("with the game's own models, textures and names. Not affiliated",
     "with the Wii U version's own models and textures, and the game's own names and motion lists. "
     "Not affiliated"),
    ('''        <span class="app-desc">Converted MT Framework <code>.mod</code> meshes to glTF and <code>.tex</code> textures to DDS.</span></li>
''', '''        <span class="app-desc">Converted MT Framework <code>.mod</code> meshes to glTF and <code>.lmt</code> motion lists to animation (the motion lists from the 3DS version, whose skeletons are the same).</span></li>
      <li><span class="app-name">AMD's address library</span> &mdash; as ported to Python by AboodXD
        <span class="app-desc">The reference for undoing the Wii U's GX2 texture tiling; the build uses its own reduced version of that path.</span></li>
'''),
]
R['docs/game.js'] = [
    ("  storagePrefix: 'mh3u-armor-viewer',\n",
     "  // -hd: the HD viewer keeps its own settings, apart from the 3DS viewer's on the same origin\n"
     "  storagePrefix: 'mh3u-armor-viewer-hd',\n"),
    ("  setFileName: 'mh3u-armor-set.json',\n  setFileLabel: 'MH3U armor set',\n",
     "  setFileName: 'mh3u-armor-hd-set.json',\n  setFileLabel: 'MH3U armor set',\n"),
    # THE WII U'S COLOUR BOARD AND SKIN STRIP (notes/armor.md "Wii U colours"; wiiu_build_armor.py wiiu_colour_data)
    ('''  // the game's colour board (GUI\\Texture\\lobby\\td_color), at the bottom of the Pigment modal's first tab: its 178 x 53
  // pixels, [0, 0] to [177, 52] inclusive (armor.json colors.board)
  pigmentBoard: { image: 'boards/mh3u-td_color.png', region: [0, 0, 177, 52] },
''', '''  // the game's colour board, the WII U's: GUI\\Texture\\startmenu\\st_menu_03 (the 3DS's td_color is another texture,
  // another layout; the Wii U presets' x, y land on this one, 23 of 24 exact), at the bottom of the Pigment modal's first
  // tab: its 408 x 124 pixels, [1, 1] to [408, 124] inclusive (armor.json colors.board). The image is this app's own
  // (docs/ui, built by wiiu_build_armor.py), reached from base/ -- the base hosts the 3DS board only.
  pigmentBoard: { image: '../ui/st_menu_03.png', region: [1, 1, 408, 124] },
'''),
    ('''    { kind: 'strip', input: 'skinTone', label: 'Skin Tone', min: 0, max: 189, step: 1, default: 189, rgb: true,
      title: "The game's skin tone slider: each step is one texel of the game's own skin strip" },
''', '''    // the Wii U's Skin Tone slider: 0-99 (0x268aec4), starting at 99 (0x2687c18), each step the texel 1 + trunc(412 * s /
    // 100) of row 132 of st_menu_03 (0x268ac04; armor.json colors.skin.strip). The 3DS's runs 0-189 over another texture.
    // rgb: the Wii U save holds the skin as packed RGB too (+0x73e0, written by 0x268ae74; Raven's "mi" holds a 3DS tone).
    { kind: 'strip', input: 'skinTone', label: 'Skin Tone', min: 0, max: 99, step: 1, default: 99, rgb: true,
      title: "The game's skin tone slider: each step is the texel the Wii U version reads from its own skin strip" },
'''),
    ('''  // rest, READ; notes/armor.md "Colour and pigment NAMES"). Each preset IS a pixel of the colour board (armor.json
  // colors.presets: [R, G, B, x, y]).
''', '''  // rest, READ; notes/armor.md "Colour and pigment NAMES"; the Wii U's StMenu_eng.gmd has the same strings there, its
  // label code not traced). Each preset IS a pixel of the colour board (armor.json colors.presets: [R, G, B, x, y]).
'''),
    ('''  // GUILD INFO: the Guild Card title words (build_guild_titles.py, notes/armor.md "Guild Card titles"), eight to a page
  // (0x45b7f0), and the name tag (`tag`, below). No hrBands: the 3DS tag takes no rank colour (it is the layout's one
  // colour), so there is no Hunter Rank row.
''', '''  // GUILD INFO: the Guild Card title words (build_guild_titles.py, notes/armor.md "Guild Card titles"; built from the Wii
  // U's CardTitle / CardEdit text the file is identical), eight to a page (3DS 0x45b7f0; Wii U 0x26399ec, the same slots
  // 6..13 test), and the name tag (`tag`, below) in the Wii U's RANK COLOURS (Raven, 2026-10-19: "Rank colours, as Wii
  // U"; notes/armor.md "Wii U gathering-hall name tag"): 0x2607b60 colours the tag's text by 0x26061e8(member u16 +0x28)
  // -- hrBands below, READ (ABGR words; the order READ from the skin chip). That +0x28 is the Hunter Rank is INFERRED:
  // the same lobby message (0x2213938) sends the sender's HR (save +0x5a20, the "HR %3d" its list prints) beside each
  // relayed member's +0x28; the bands end at 999, the HR cap; 0xffff is the fallback. Its writer is not found. When
  // +0x28 is 0xffff the game uses the player's slot colour (0x20296b8) -- logged, not offered.
'''),
    ('''      // the layout's text Color, read: both text objects of npc_statusicon.gui point into its vector pool at
      // (255, 255, 255, 255); no code on either path sets another colour, and none reads a rank
      colour: '#ffffff',
''', '''      // no colour: the Wii U colours the tag by rank band (hrBands, above), not the 3DS layout's white
'''),
    ('''    titlePage: 8,
''', '''    titlePage: 8,
    // 0x26061e8's bands (unsigned compares: <=2, <=5, <=7, <=99, <=998, else), the game's colours. The labels are the
    // VIEWER's, not game text (the game gives the bands none): each band's range, in GU's style -- Raven can rename them
    hrBands: [
      { hr: 1,   max: 2,   color: '#f0f0f0', label: 'HR 1–2' },
      { hr: 3,   max: 5,   color: '#ffff50', label: 'HR 3–5' },
      { hr: 6,   max: 7,   color: '#ffa461', label: 'HR 6–7' },
      { hr: 8,   max: 99,  color: '#ff435d', label: 'HR 8–99' },
      { hr: 100, max: 998, color: '#ff84ff', label: 'HR 100–998' },
      { hr: 999, max: 999, color: '#57ffff', label: 'HR 999' },
    ],
'''),
    ('''      // the <ICON> font's weapon glyphs, <ICON 00> .. <ICON 12> in 14 px cells (build_plate_icons.py: font_icon.gii /
      // .gfd / font_icon_00_GSM_NOMIP.tex)
      icons: 'ui/plate-icons.png?v=20261019', iconCell: 14,
''', '''      // the Wii U's own <ICON> font: weapon glyphs <ICON 00> .. <ICON 12> in 32 px cells (MH3U-Extract/
      // wiiu_build_plate_icons.py: its font_icon.gii / .gfd / font_icon_00_GSM_NOMIP.tex, 512 x 128 RGBA; the 3DS's are
      // 14 px). The Wii U has no glyph at <ICON 05> (the 3DS a second gun); class 5 is drawn as 6, so 05 is never used.
      // The Wii U layout names GUI/font/font_jpn as its font, not the 3DS layout's GUI/dfont/Dfont_net
      icons: 'ui/plate-icons.png?v=20261019hd', iconCell: 32,
'''),
]
R['docs/adapter.js'] = [
    ("// Then the base adds the game's colour board (game.pigmentBoard).",
     "// HD: the Wii U's own -- its presets are RPX 0x10114a88 (the same 24 colours; the pigment page's 0x21c4120 takes records\n"
     "// 12..23 for every mode but the hair's 0..11), its 44 colours 0x1000d83c (byte-identical), its board st_menu_03. No\n"
     "// other Wii U colour reaches a pick (the record block 0x101149a0 is read only by unreferenced code; notes/armor.md).\n"
     "// Then the base adds the game's colour board (game.pigmentBoard)."),
]
R['docs/app.js'] = [
    ('// The MH3U Armor Viewer. One figure:', '// The MH3U Armor Viewer HD: the MH3U Armor Viewer\'s code (ported by dev/port-from-3u.py) on the Wii U version\'s\n'
     '// models and textures (C:\\MH3U-Extract\\wiiu_build_armor.py; the tables, mount, stances and motion lists are the 3DS\n'
     '// build\'s). One figure:'),
    ("const LS_KEY = 'mh3u-armor-viewer';", "const LS_KEY = 'mh3u-armor-viewer-hd';"),
    ("const CHAIN_KEY_OLD = 'mh3u-armor-viewer-chain';", "const CHAIN_KEY_OLD = 'mh3u-armor-viewer-hd-chain';"),
    ("  return 'MH3U ' + who + ' ' + new Date()", "  return 'MH3U HD ' + who + ' ' + new Date()"),
    ("  return { app: 'MH3U Armor Viewer', version: 2,", "  return { app: 'MH3U Armor Viewer HD', version: 2,"),
    ("(d.app === 'MH3U Armor Viewer' || ", "(d.app === 'MH3U Armor Viewer HD' || d.app === 'MH3U Armor Viewer' || "),
    # THE WII U'S COLOURS. A board pixel { x, y } is only ever an older save's, picked on the 3DS board this viewer used
    # before it took the Wii U's: it reads from that board (armor.json colors.legacyBoard), so its colour is kept.
    ('''const boardImg = new Image();
await new Promise((ok, bad) => { boardImg.onload = ok; boardImg.onerror = bad; boardImg.src = C.board.png; });
const boardData = (() => {
  const cv = document.createElement('canvas'); cv.width = C.board.w; cv.height = C.board.h;
  const cx = cv.getContext('2d'); cx.drawImage(boardImg, 0, 0);
  return cx.getImageData(0, 0, C.board.w, C.board.h).data;
})();
const boardRGB = (x, y) => { const i = (y * C.board.w + x) * 4; return [boardData[i], boardData[i + 1], boardData[i + 2]]; };
''', '''// HD: those older saves picked on the 3DS board (td_color), which this viewer drew before it took the Wii U's colours
// (st_menu_03, armor.json colors.board), so the pixel is read from that one (colors.legacyBoard).
const LB = C.legacyBoard || C.board;
const boardImg = new Image();
await new Promise((ok, bad) => { boardImg.onload = ok; boardImg.onerror = bad; boardImg.src = LB.png; });
const boardData = (() => {
  const cv = document.createElement('canvas'); cv.width = LB.w; cv.height = LB.h;
  const cx = cv.getContext('2d'); cx.drawImage(boardImg, 0, 0);
  return cx.getImageData(0, 0, LB.w, LB.h).data;
})();
const boardRGB = (x, y) => { const i = (y * LB.w + x) * 4; return [boardData[i], boardData[i + 1], boardData[i + 2]]; };
'''),
    ("// The starting colours are the game's own new hunter's (the new-save routine 0x99b128, READ 2026-10-19; notes/armor.md\n",
     "// The starting colours are the game's own new hunter's (HD: the WII U's new-save routine 0x216d0e0..0x216d420 writes the\n"
     "// same four words -- hair +0x1c 0x7a431eff (4 branches), skin +0x73e0 0xffffffff (white = the Wii U strip's 99, the\n"
     "// slider's start 0x2687c18), clothing +0x5768 0x8ba150ff, features +0x73e8 / +0x73ec 0xffffff00; READ 2026-10-19). The\n"
     "// 3DS's: the new-save routine 0x99b128, READ 2026-10-19; notes/armor.md\n"),
    # A hunter saved on the 3DS's Skin Tone scale (this viewer before the port, session v2 / set version 1, or a set from
    # the 3DS viewer) holds an index into the 3DS's 190-texel strip, which names no step of the Wii U's: it is kept as
    # that texel's RGB (armor.json colors.legacySkin), as the game keeps a carried-over character's skin (Raven's Wii U
    # save "mi" holds 3DS strip texel 188).
    ("const state = clone(DEFAULTS);\n",
     "// HD: a hunter whose skin is an index on the 3DS's strip (see the session and applySet below) keeps that texel's RGB\n"
     "const skin3ds = h => h && typeof h === 'object' && Number.isInteger(h.skin) && h.skin >= 0 && C.legacySkin\n"
     "  ? Object.assign({}, h, { skin: rgbHex(C.legacySkin[Math.min(h.skin, C.legacySkin.length - 1)]) }) : h;\n"
     "const state = clone(DEFAULTS);\n"),
    ("if (SAVED) Object.assign(state, hunterOf(SAVED));",
     "if (SAVED) Object.assign(state, hunterOf(SAVED.v === 3 ? SAVED : skin3ds(SAVED)));"),
    ("  Object.assign(state, hunterOf(d.hunter));",
     # only a set that IS on the 3DS scale converts: the 3DS viewer's, or this viewer's own before the port (version 1); a
     # set with no app (Reset, New, a slot's fresh hunter) is this viewer's own, on the Wii U scale
     "  Object.assign(state, hunterOf(d.app === 'MH3U Armor Viewer' || (d.app === 'MH3U Armor Viewer HD' && !(d.version >= 2))\n"
     "    ? skin3ds(d.hunter) : d.hunter));"),
]


def read(p):
    with open(p, 'r', encoding='utf-8', newline='') as f:
        return f.read().replace('\r\n', '\n')


def port():
    out = {}
    for rel in COPY:
        t = read(os.path.join(U3, rel))
        for rep in R.get(rel, []):
            a, b = rep[0], rep[1]
            if len(rep) > 2 and rep[2] == 'last':
                i = t.rfind(a)
                if i < 0:
                    sys.exit('%s: anchor not found: %r' % (rel, a[:60]))
                t = t[:i] + b + t[i + len(a):]
                continue
            n = t.count(a)
            if n != 1:
                sys.exit('%s: anchor found %d times (want 1): %r' % (rel, n, a[:60]))
            t = t.replace(a, b)
        out[rel] = t
    return out


def main():
    check = '--check' in sys.argv
    out = port()
    for rel, t in out.items():
        p = os.path.join(HD, rel)
        old = read(p) if os.path.exists(p) else None
        if old == t:
            continue
        print(('would write ' if check else 'write ') + rel)
        if not check:
            os.makedirs(os.path.dirname(p), exist_ok=True)
            with open(p, 'w', encoding='utf-8', newline='\n') as f:
                f.write(t)
    for rel in DELETE:
        p = os.path.join(HD, rel)
        if os.path.exists(p):
            print(('would delete ' if check else 'delete ') + rel)
            if not check:
                os.remove(p)


if __name__ == '__main__':
    main()
