# How the page is built

`index.html` is generated, not hand-written. These are the sources.

Run order: **build_all.py** (images) -> **make_page.py** (html) -> **audit.py** (check).

- `page_shell.html` - the chrome: fonts, meta and og: tags, favicon, the
  light/dark colour tokens, masthead, scope strip, TOC, case-study header,
  all the CSS, the contact card, footer, and the before/after slider JS.
- `make_page.py` - the content. `ITEM` holds a kicker, a note and the measured
  readout chips per frame; `GRIDS`, `CASES` and `SECTIONS` decide what appears
  where and in what order. Reads `manifest2.json`, writes `index.html`.
- `build_all.py` - builds every image in `img/` plus the three contact sheets,
  and writes `manifest2.json`. **Resolution order matters**: `retouched/masks/`,
  `retouched/iceland/` and `retouched/the endless search/` hold the full-size
  masters; the same frame numbers also exist in the flat `retouched/` folder as
  older, smaller exports of the same edits. The subfolders must win.
- `measure.py` - computes the readout chips (CIELAB) from the files. Every
  number on the page comes from here.
- `audit.py` - re-measures every chip on the page against the files and prints
  anything that disagrees. Should print `0 problems`. Run it after any edit to
  the numbers, and after Maria re-exports anything.
- `build_exports.py`, `rebuild3.py` - the platform export sets (Upwork,
  Freelancer, Fiverr sizes). Not needed for the website.
- `manifest2.json` - per-frame mode and pixel dimensions, consumed by make_page.
- `build_web2.py` - superseded, see the note inside it.

For a text-only change - wording, a caption, a colour - edit `make_page.py` or
`page_shell.html` and re-run `make_page.py`. Editing `index.html` directly works
too, but the next rebuild overwrites it.

## Rules the page depends on

Nothing on the page claims anything that is not measured off the files.
`converted to mono` means mean chroma is effectively zero, not merely low; a
frame that only looks monochrome gets its actual `chroma -NN%`. Aspect chips are
computed from pixel dimensions, never rounded to a tidier ratio.
