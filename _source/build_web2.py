#!/usr/bin/env python3
"""v2 web assets: pairs + after-only project grids."""
import os, math, json
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

SRC = "/mnt/user-data/uploads/retouch examples"
OUT = "/home/claude/site/img"
BG = (16, 17, 17)
os.makedirs(OUT, exist_ok=True)

# where the retouched master lives for each frame
SPECIAL = {55: "retouched/masks/retouched-55.jpg",
           60: "retouched/masks/retouched-60.jpg"}


def load(kind, n):
    if kind == "r" and n in SPECIAL:
        return Image.open(f"{SRC}/{SPECIAL[n]}").convert("RGB")
    sub = "originals/original" if kind == "b" else "retouched/retouched"
    return Image.open(f"{SRC}/{sub}-{n}.jpg").convert("RGB")


def cover(im, W, H):
    s = max(W / im.width, H / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    x = (im.width - W) // 2; y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def save(im, rel, q=80, cap=380_000):
    p = os.path.join(OUT, rel)
    while True:
        im.save(p, "JPEG", quality=q, subsampling=1, optimize=True, progressive=True)
        if os.path.getsize(p) <= cap or q <= 58:
            break
        q -= 6
    return os.path.getsize(p)


def after_grid(nums, rows_target, W, gap=6):
    """Justified contact sheet: whole frames, equal-height rows, no crop, no dead space."""
    ims = [load("r", n) for n in nums]
    ar = [im.width / im.height for im in ims]
    total = sum(ar)
    per_row = total / rows_target
    rows, cur, acc = [], [], 0.0
    for i, a in enumerate(ar):
        cur.append(i); acc += a
        if acc >= per_row and len(rows) < rows_target - 1:
            rows.append(cur); cur, acc = [], 0.0
    if cur:
        rows.append(cur)
    laid, H = [], 0
    for r in rows:
        avail = W - gap * (len(r) - 1)
        h = int(avail / sum(ar[i] for i in r))
        laid.append((r, h)); H += h + gap
    H -= gap
    c = Image.new("RGB", (W, H), BG)
    y = 0
    for r, h in laid:
        x = 0
        for k, i in enumerate(r):
            w = W - x if k == len(r) - 1 else int(ar[i] * h)
            c.paste(ims[i].resize((max(1, w), max(1, h)), Image.LANCZOS), (x, y))
            x += w + gap
        y += h + gap
    return c


PAGE = [100, 99, 45, 109, 72, 75, 3, 103, 104, 40,
        47, 23, 18, 96, 6, 88, 1, 80, 46, 20,
        60, 55, 67, 12, 15]

LONG = 1500
manifest = []
for n in PAGE:
    b, r = load("b", n), load("r", n)
    ab, ar = b.width / b.height, r.width / r.height
    drift = abs(ab - ar) / min(ab, ar)
    mode = "slider" if drift < 0.06 else "pair"
    if mode == "slider":
        a = (ab + ar) / 2
        W, H = (LONG, round(LONG / a)) if a >= 1 else (round(LONG * a), LONG)
        W -= W % 2; H -= H % 2
        save(cover(b, W, H), f"p{n}-b.jpg"); save(cover(r, W, H), f"p{n}-a.jpg")
        manifest.append({"n": n, "mode": mode, "w": W, "h": H})
    else:
        def fit(im):
            s = LONG / max(im.width, im.height)
            return im.resize((max(2, round(im.width * s)), max(2, round(im.height * s))), Image.LANCZOS)
        fb, fr = fit(b), fit(r)
        save(fb, f"p{n}-b.jpg"); save(fr, f"p{n}-a.jpg")
        manifest.append({"n": n, "mode": mode,
                         "w": fb.width, "h": fb.height, "w2": fr.width, "h2": fr.height})

MASKS16 = [52, 53, 54, 55, 56, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 70]
SEARCH10 = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
gm = after_grid(MASKS16, 4, 1600); save(gm, "grid-masks.jpg", cap=620_000)
gs = after_grid(SEARCH10, 3, 1600); save(gs, "grid-search.jpg", cap=520_000)

print("GRID", gm.size, gs.size)

for f in ("p4-a.jpg p4-b.jpg p98-a.jpg p98-b.jpg p85-a.jpg p85-b.jpg "
          "p26-a.jpg p26-b.jpg grid-mask16.jpg grid-forest8.jpg").split():
    p = os.path.join(OUT, f)
    if os.path.exists(p):
        os.remove(p)

json.dump(manifest, open("/home/claude/site/manifest2.json", "w"), indent=1)
print(json.dumps(manifest))
print("files:", len(os.listdir(OUT)))
