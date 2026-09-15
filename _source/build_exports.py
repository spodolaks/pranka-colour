#!/usr/bin/env python3
"""Build the per-platform export set from the retouch examples folder."""
import os, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter
Image.MAX_IMAGE_PIXELS = None

SRC = "/mnt/user-data/uploads/retouch examples"
OUT = "/home/claude/exports"
BG = (17, 17, 18)
INK = (232, 230, 226)
DIM = (150, 148, 144)
ACC = (196, 122, 74)

FB = "/usr/share/fonts/truetype/crosextra/Carlito-Bold.ttf"
FR = "/usr/share/fonts/truetype/crosextra/Carlito-Regular.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def load(kind, n):
    p = f"{SRC}/{'originals/original' if kind == 'b' else 'retouched/retouched'}-{n}.jpg"
    return Image.open(p).convert("RGB")


def cover(im, W, H):
    """Scale + centre-crop to exactly WxH."""
    s = max(W / im.width, H / im.height)
    im = im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)
    x = (im.width - W) // 2
    y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))


def contain(im, W, H):
    s = min(W / im.width, H / im.height)
    return im.resize((max(1, round(im.width * s)), max(1, round(im.height * s))), Image.LANCZOS)


def tracked(d, xy, text, f, fill, track=0):
    x, y = xy
    for ch in text:
        d.text((x, y), ch, font=f, fill=fill)
        x += d.textlength(ch, font=f) + track
    return x


def tracked_w(d, text, f, track=0):
    return sum(d.textlength(ch, font=f) + track for ch in text) - track


def label_bar(canvas, box, text, f, fill=INK, track=1.5):
    d = ImageDraw.Draw(canvas)
    x0, y0, x1, _ = box
    tracked(d, (x0, y0), text, f, fill, track)


def ba_split(n, W, H, gap=None, labels=True, lab_scale=1.0):
    """Before | after, each cover-cropped to half the canvas."""
    gap = gap if gap is not None else max(2, round(W * 0.004))
    half = (W - gap) // 2
    c = Image.new("RGB", (W, H), BG)
    c.paste(cover(load("b", n), half, H), (0, 0))
    c.paste(cover(load("r", n), W - half - gap, H), (half + gap, 0))
    if labels:
        d = ImageDraw.Draw(c)
        fs = max(11, round(H * 0.030 * lab_scale))
        f = font(FB, fs)
        pad = round(H * 0.030)
        for x0, t, col in ((pad, "BEFORE", INK), (half + gap + pad, "AFTER", INK)):
            tw = tracked_w(d, t, f, fs * 0.16)
            d.rectangle([x0 - pad * 0.45, pad - pad * 0.35,
                         x0 + tw + pad * 0.45, pad + fs * 1.35], fill=(12, 12, 13))
            tracked(d, (x0, pad), t, f, col, fs * 0.16)
    return c


def ba_grid(nums, cols, W, H, cell_gap=None):
    """Grid of small before|after pairs."""
    cell_gap = cell_gap if cell_gap is not None else max(3, round(W * 0.006))
    rows = math.ceil(len(nums) / cols)
    cw = (W - cell_gap * (cols - 1)) // cols
    ch = (H - cell_gap * (rows - 1)) // rows
    c = Image.new("RGB", (W, H), BG)
    for i, n in enumerate(nums):
        cell = ba_split(n, cw, ch, gap=max(1, round(cw * 0.006)), labels=False)
        c.paste(cell, ((i % cols) * (cw + cell_gap), (i // cols) * (ch + cell_gap)))
    return c


def hero(n, W, H, side="r"):
    return cover(load(side, n), W, H)


def strip(nums, W, H, vertical=False):
    """Several before|after pairs stacked."""
    gap = max(3, round((H if not vertical else W) * 0.012))
    k = len(nums)
    if vertical:
        ch = (H - gap * (k - 1)) // k
        c = Image.new("RGB", (W, H), BG)
        for i, n in enumerate(nums):
            c.paste(ba_split(n, W, ch, labels=(i == 0), lab_scale=1.6), (0, i * (ch + gap)))
    else:
        cw = (W - gap * (k - 1)) // k
        c = Image.new("RGB", (W, H), BG)
        for i, n in enumerate(nums):
            c.paste(ba_split(n, cw, H, labels=(i == 0)), (i * (cw + gap), 0))
    return c


def caption_block(canvas, lines, pad_ratio=0.055):
    """Solid dark footer band (with a short gradient above it) + headline/subline."""
    W, H = canvas.size
    band = round(H * 0.175)
    feather = round(H * 0.10)
    # feathered lead-in above the band
    grad = Image.new("L", (1, feather))
    for y in range(feather):
        grad.putpixel((0, y), int(252 * (y / feather) ** 1.5))
    grad = grad.resize((W, feather))
    top = H - band - feather
    shade = Image.new("RGB", (W, feather), (9, 9, 10))
    canvas.paste(Image.composite(shade, canvas.crop((0, top, W, top + feather)), grad), (0, top))
    d = ImageDraw.Draw(canvas)
    d.rectangle([0, H - band, W, H], fill=(9, 9, 10))
    d.line([(0, H - band), (W, H - band)], fill=(38, 38, 40), width=max(1, round(H * 0.002)))
    pad = round(W * pad_ratio)
    f1 = font(FB, round(H * 0.060))
    f2 = font(FR, round(H * 0.038))
    y = H - band + round(H * 0.028)
    tracked(d, (pad, y), lines[0], f1, INK, round(H * 0.060) * 0.045)
    if len(lines) > 1:
        d.text((pad, y + round(H * 0.076)), lines[1], font=f2, fill=DIM)


def framed(content, W, H, lines, pad_ratio=0.045):
    """Content on top, solid caption band beneath - nothing important is covered."""
    band = round(H * 0.165)
    c = Image.new("RGB", (W, H), (9, 9, 10))
    c.paste(cover(content, W, H - band), (0, 0))
    d = ImageDraw.Draw(c)
    d.line([(0, H - band), (W, H - band)], fill=(44, 44, 46), width=max(1, round(H * 0.0026)))
    pad = round(W * pad_ratio)
    f1 = font(FB, round(H * 0.058))
    f2 = font(FR, round(H * 0.036))
    y = H - band + round(H * 0.030)
    tracked(d, (pad, y), lines[0], f1, INK, round(H * 0.058) * 0.05)
    if len(lines) > 1:
        d.text((pad, y + round(H * 0.072)), lines[1], font=f2, fill=DIM)
    return c


def after_grid(nums, cols, W, H, cell_gap=None):
    """Grid of graded (after) frames only - shows consistency across a set."""
    cell_gap = cell_gap if cell_gap is not None else max(3, round(W * 0.005))
    rows = math.ceil(len(nums) / cols)
    cw = (W - cell_gap * (cols - 1)) // cols
    ch = (H - cell_gap * (rows - 1)) // rows
    c = Image.new("RGB", (W, H), BG)
    for i, n in enumerate(nums):
        c.paste(cover(load("r", n), cw, ch),
                ((i % cols) * (cw + cell_gap), (i // cols) * (ch + cell_gap)))
    return c


def pair_rows(nums, W, H):
    """Stacked full-width before|after rows, each labelled."""
    gap = max(4, round(H * 0.016))
    k = len(nums)
    rh = (H - gap * (k - 1)) // k
    c = Image.new("RGB", (W, H), BG)
    for i, n in enumerate(nums):
        c.paste(ba_split(n, W, rh, lab_scale=2.4), (0, i * (rh + gap)))
    return c


def save(im, rel, quality=88, maxbytes=None):
    p = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    q = quality
    while True:
        im.save(p, "JPEG", quality=q, subsampling=1, optimize=True, progressive=True)
        if maxbytes is None or os.path.getsize(p) <= maxbytes or q <= 60:
            break
        q -= 6
    print(f"{rel:62s} {im.size[0]}x{im.size[1]}  {os.path.getsize(p)/1024:7.0f} KB")
    return p


# ---------------------------------------------------------------- selections
MASK16 = [52, 53, 54, 55, 56, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 70]
MASK8 = [52, 55, 59, 60, 63, 65, 67, 70]
FOREST8 = [7, 8, 11, 12, 13, 14, 15, 16]

UPWORK = {
 "01-set-consistency": ("GRID16", [67, 60, 55, 69]),
 "02-landscape-travel": (None, [75, 3, 85, 108, 101]),
 "03-portrait-location": (None, [47, 23, 18, 96, 6]),
 "04-black-and-white":  (None, [67, 104, 89, 105, 78]),
 "05-colour-cast-fix":  (None, [100, 107, 82, 45, 99]),
 "06-aerial-drone":     (None, [98, 103, 71, 97, 26]),
}

FIVERR_PORT = {
 "01-set-consistency": ("GRID16", [67, 60, 69]),
 "02-landscape-travel": (None, [75, 3, 85, 101]),
 "03-portrait-location": (None, [47, 23, 96, 6]),
 "04-black-and-white":  (None, [67, 104, 89, 105]),
 "05-colour-cast-fix":  (None, [100, 107, 82, 99]),
 "06-aerial-drone":     (None, [98, 103, 71, 97]),
}

FREELANCER = {
 "01-set-consistency": ("GRID8", [67]),
 "02-landscape-travel": (None, [75, 3]),
 "03-portrait-location": (None, [47, 23]),
 "04-black-and-white":  (None, [67, 104]),
 "05-colour-cast-fix":  (None, [100, 99]),
 "06-aerial-drone":     (None, [98, 103]),
}

PAGE = [75, 3, 100, 104, 85, 47, 23, 67, 46, 99, 12, 18,
        80, 6, 96, 4, 88, 45, 103, 98, 109, 26, 72, 20]


def build_upwork():
    W, H = 2000, 1500
    for item, (special, nums) in UPWORK.items():
        i = 1
        if special == "GRID16":
            save(after_grid(MASK16, 4, W, H), f"01-upwork/{item}/{item}-{i:02d}-set-16-graded-frames.jpg",
                 maxbytes=9_000_000); i += 1
            save(ba_grid(MASK8, 2, W, H), f"01-upwork/{item}/{item}-{i:02d}-before-after-8.jpg",
                 maxbytes=9_000_000); i += 1
        for n in nums:
            save(ba_split(n, W, H), f"01-upwork/{item}/{item}-{i:02d}-pair-{n}.jpg",
                 maxbytes=9_000_000); i += 1


def build_fiverr_portfolio():
    W, H = 1920, 1152
    for item, (special, nums) in FIVERR_PORT.items():
        i = 1
        if special == "GRID16":
            save(after_grid(MASK16, 4, W, H), f"03-fiverr-portfolio/{item}/{item}-{i:02d}-set-16-graded-frames.jpg",
                 maxbytes=40_000_000); i += 1
        for n in nums:
            save(ba_split(n, W, H), f"03-fiverr-portfolio/{item}/{item}-{i:02d}-pair-{n}.jpg",
                 maxbytes=40_000_000); i += 1


def build_freelancer():
    W, H = 1800, 1350
    for item, (special, nums) in FREELANCER.items():
        i = 1
        if special == "GRID8":
            save(after_grid(MASK16, 4, W, H), f"04-freelancer/{item}/{item}-{i:02d}-set-16-graded-frames.jpg",
                 maxbytes=9_000_000); i += 1
        for n in nums:
            save(ba_split(n, W, H), f"04-freelancer/{item}/{item}-{i:02d}-pair-{n}.jpg",
                 maxbytes=9_000_000); i += 1


def build_fiverr_gigs():
    W, H = 1280, 769
    CH = H - round(H * 0.165)          # height of the picture area inside framed()
    MB = 4_800_000
    G1 = "02-fiverr-gig-images/gig-1-retouching"
    G2 = "02-fiverr-gig-images/gig-2-batch-grading"

    # Gig 1 - colour / light / crop retouching
    save(framed(ba_split(47, W, CH, lab_scale=1.5), W, H,
                ["COLOUR, LIGHT & CROP RETOUCHING",
                 "Exposure - white balance - grade - straighten - export"]),
         f"{G1}/gig1-01-thumbnail.jpg", maxbytes=MB)

    save(framed(pair_rows([75, 23], W, CH), W, H,
                ["FLAT FILES IN - PUBLISH-READY OUT",
                 "Landscape, travel and portrait work"]),
         f"{G1}/gig1-02-range.jpg", maxbytes=MB)

    save(framed(ba_split(100, W, CH, lab_scale=1.5), W, H,
                ["COLOUR CASTS REMOVED",
                 "White balance corrected frame by frame"]),
         f"{G1}/gig1-03-cast.jpg", maxbytes=MB)

    # Gig 2 - batch grading
    save(framed(after_grid(MASK16, 4, W, CH), W, H,
                ["ONE GRADE, WHOLE SHOOT",
                 "16 frames from one set - matched to a single look"]),
         f"{G2}/gig2-01-thumbnail.jpg", maxbytes=MB)

    save(framed(pair_rows([60, 52], W, CH), W, H,
                ["SHOT-TO-SHOT CONSISTENCY",
                 "Every frame in the delivery reads as one shoot"]),
         f"{G2}/gig2-02-consistency.jpg", maxbytes=MB)

    save(framed(after_grid(FOREST8 + [10, 9, 1, 17], 4, W, CH), W, H,
                ["A LOOK BUILT FOR EACH SHOOT",
                 "Preset per project, then every frame checked by hand"]),
         f"{G2}/gig2-03-batch.jpg", maxbytes=MB)


def build_web():
    """Matched-aspect before/after files for the portfolio page + a manifest."""
    manifest = []
    LONG = 1500
    for n in PAGE:
        b, r = load("b", n), load("r", n)
        ab, ar = b.width / b.height, r.width / r.height
        drift = abs(ab - ar) / min(ab, ar)
        mode = "slider" if drift < 0.06 else "pair"
        a = (ab + ar) / 2
        if a >= 1:
            W, H = LONG, round(LONG / a)
        else:
            H, W = LONG, round(LONG * a)
        H -= H % 2; W -= W % 2
        save(cover(b, W, H), f"web/p{n}-b.jpg", quality=80, maxbytes=380_000)
        save(cover(r, W, H), f"web/p{n}-a.jpg", quality=80, maxbytes=380_000)
        manifest.append({"n": n, "w": W, "h": H, "mode": mode})
    save(ba_grid(MASK16, 4, 1600, 1000), "web/grid-mask16.jpg", quality=80, maxbytes=600_000)
    save(ba_grid(FOREST8, 4, 1600, 700), "web/grid-forest8.jpg", quality=80, maxbytes=500_000)
    import json
    with open(os.path.join(OUT, "web", "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=1)
    print("\nmanifest:", json.dumps(manifest))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    build_upwork()
    build_fiverr_gigs()
    build_fiverr_portfolio()
    build_freelancer()
    build_web()
