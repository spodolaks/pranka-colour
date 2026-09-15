# How the page is built

`index.html` is generated, not hand-written. These are the sources.

- `page_shell.html` - the chrome: fonts, the light/dark colour tokens, masthead,
  scope strip, TOC, case-study header block, all the CSS, the contact card,
  footer, and the before/after slider JS.
- `make_page.py` - the content. `ITEM` holds a kicker, a note and the measured
  CIELAB readouts per frame; `GRIDS`, `CASES` and `SECTIONS` decide what appears
  where and in what order. Reads `manifest2.json`, writes `index.html`.
- `build_web2.py` - makes the web-sized images in `img/` from the original and
  retouched masters, and writes `manifest2.json`. Aspect drift decides whether a
  frame becomes a slider (near-identical crop) or a side-by-side pair.
- `build_exports.py`, `rebuild3.py` - the platform export sets (Upwork,
  Freelancer, Fiverr sizes). Not needed for the website.
- `manifest2.json` - per-frame mode and pixel dimensions, consumed by make_page.

To rebuild: run `build_web2.py` first if the image set changed, then
`make_page.py`. Both expect the original folder at the path set at the top of
each file.

For a text-only change - wording, a caption, a colour - edit `make_page.py` or
`page_shell.html` and re-run `make_page.py`. Editing `index.html` directly works
too, but the next rebuild overwrites it.
