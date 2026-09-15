#!/usr/bin/env python3
"""Build every web asset the portfolio page needs, from the current masters.

Resolution order for a retouched frame: retouched/masks/, retouched/iceland/,
retouched/'the endless search'/, then the flat retouched/ folder. The subfolders
hold the full-resolution masters; the flat copies are older downsamples of the
same edits, so the subfolders must win.

Writes img/p<N>-b.jpg and p<N>-a.jpg for every frame, the three contact sheets,
and manifest2.json (per-frame mode and pixel dimensions, read by make_page.py).

Frames whose before/after aspect ratios match become sliders; the rest become
side-by-side pairs.
"""
import os, json
from PIL import Image
Image.MAX_IMAGE_PIXELS = None

BASE = "/mnt/user-data/uploads/retouch examples"
OUT  = "/home/claude/site/img"
BG   = (16, 17, 17)
LONG = 1500
os.makedirs(OUT, exist_ok=True)

PAGE = [3, 6, 8, 9, 11, 12, 15, 18, 21, 23, 24, 25, 27, 40, 45, 46, 47, 50, 52, 54,
        56, 59, 65, 67, 69, 71, 72, 73, 75, 80, 89, 92, 94, 96, 99, 100, 103, 104, 106, 109]
MASKS16  = [52, 53, 54, 55, 56, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 70]
SEARCH10 = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
ICELAND8 = [88, 89, 90, 91, 92, 93, 94, 95]


def load(kind, n):
    if kind == "b":
        return Image.open(f"{BASE}/originals/original-{n}.jpg").convert("RGB")
    for sub in ("retouched/masks", "retouched/iceland",
                "retouched/the endless search", "retouched"):
        p = f"{BASE}/{sub}/retouched-{n}.jpg"
        if os.path.exists(p):
            return Image.open(p).convert("RGB")
    raise FileNotFoundError(f"retouched-{n}.jpg")


def cover(im, W, H):
    s = max(W / im.width, H / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def fit(im, long=LONG):
    s = long / max(im.width, im.height)
    return im.resize((max(2, round(im.width * s)), max(2, round(im.height * s))), Image.LANCZOS)


def save(im, rel, q=80, cap=380_000):
    p = os.path.join(OUT, rel)
    while True:
        im.save(p, "JPEG", quality=q, subsampling=1, optimize=True, progressive=True)
        if os.path.getsize(p) <= cap or q <= 58:
            return os.path.getsize(p)
        q -= 6


def sheet(nums, rows_target, W, gap=6):
    """Justified contact sheet: whole frames, equal-height rows, no crop, no dead space."""
    ims = [load("r", n) for n in nums]
    ar = [im.width / im.height for im in ims]
    per_row = sum(ar) / rows_target
    rows, cur, acc = [], [], 0.0
    for i, a in enumerate(ar):
        cur.append(i); acc += a
        if acc >= per_row and len(rows) < rows_target - 1:
            rows.append(cur); cur, acc = [], 0.0
    if cur:
        rows.append(cur)
    laid, H = [], 0
    for r in rows:
        h = int((W - gap * (len(r) - 1)) / sum(ar[i] for i in r))
        laid.append((r, h)); H += h + gap
    c = Image.new("RGB", (W, H - gap), BG)
    y = 0
    for r, h in laid:
        x = 0
        for k, i in enumerate(r):
            w = W - x if k == len(r) - 1 else int(ar[i] * h)
            c.paste(ims[i].resize((max(1, w), max(1, h)), Image.LANCZOS), (x, y))
            x += w + gap
        y += h + gap
    return c


if __name__ == "__main__":
    manifest = []
    for n in PAGE:
        b, r = load("b", n), load("r", n)
        ab, ar = b.width / b.height, r.width / r.height
        if abs(ab - ar) / min(ab, ar) < 0.06:            # same framing -> slider
            a = ar          # the graded frame keeps its own shape; the before is cropped to match
            W, H = (LONG, round(LONG / a)) if a >= 1 else (round(LONG * a), LONG)
            W -= W % 2; H -= H % 2
            save(cover(b, W, H), f"p{n}-b.jpg"); save(cover(r, W, H), f"p{n}-a.jpg")
            manifest.append({"n": n, "mode": "slider", "w": W, "h": H})
        else:                                             # recropped -> side by side
            fb, fr = fit(b), fit(r)
            save(fb, f"p{n}-b.jpg"); save(fr, f"p{n}-a.jpg")
            manifest.append({"n": n, "mode": "pair", "w": fb.width, "h": fb.height,
                             "w2": fr.width, "h2": fr.height})
    for name, nums, rows, cap in (("grid-masks", MASKS16, 4, 620_000),
                                  ("grid-search", SEARCH10, 3, 520_000),
                                  ("grid-iceland", ICELAND8, 3, 560_000)):
        g = sheet(nums, rows, 1600)
        save(g, f"{name}.jpg", cap=cap)
        print(f"{name}.jpg {g.size}")
    json.dump(manifest, open("/home/claude/site/manifest2.json", "w"), indent=1)
    print("frames:", len(manifest), "files:", len(os.listdir(OUT)))
