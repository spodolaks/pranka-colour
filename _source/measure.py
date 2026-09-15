#!/usr/bin/env python3
"""Measure the readout chips shown on the portfolio page.

Every number on the page comes from here: computed off the actual original
and retouched files, never from metadata and never estimated.

Pipeline per file: sRGB 8-bit -> linear RGB (the 0.04045 / 2.4 transfer curve)
-> CIE XYZ under D65 -> CIELAB.

  a*        mean a*, the green(-) to magenta(+) axis. Reported before -> after.
  b*        mean b*, the blue(-) to yellow(+) axis.
  chroma    mean hypot(a*, b*), i.e. distance from neutral. Reported as % change,
            so "chroma -36%" means the frame is 36% less saturated overall.
  contrast  standard deviation of L*. Reported as % change. Std dev, not
            max-minus-min, so a single blown highlight cannot fake it.
  L-bar     mean L*, 0 = black, 100 = white. Reported as two absolute values.

Images are downscaled to 900px on the long edge first. That makes it fast and
kills sensor noise, but it does move a number by about a point either way, so
keep the thumbnail size fixed if you want values to stay reproducible.

Aspect chips ("3:2 -> 4:5") are read from the pixel dimensions, not measured.
Chips like "objects removed" are observations, not measurements.

Usage:  python3 measure.py 47 23 96
"""
import sys
import numpy as np
from PIL import Image

SRC = "/mnt/user-data/uploads/retouch examples"   # adjust to wherever the set lives
THUMB = 900

M_RGB2XYZ = np.array([[0.4124564, 0.3575761, 0.1804375],
                      [0.2126729, 0.7151522, 0.0721750],
                      [0.0193339, 0.1191920, 0.9503041]])
D65 = np.array([0.95047, 1.0, 1.08883])


def to_lab(path):
    im = Image.open(path).convert("RGB")
    im.thumbnail((THUMB, THUMB), Image.LANCZOS)
    a = np.asarray(im, dtype=np.float64) / 255.0
    a = np.where(a <= 0.04045, a / 12.92, ((a + 0.055) / 1.055) ** 2.4)
    t = (a @ M_RGB2XYZ.T) / D65
    d = 6 / 29
    f = np.where(t > d ** 3, np.cbrt(t), t / (3 * d * d) + 4 / 29)
    L = 116 * f[..., 1] - 16
    return L, 500 * (f[..., 0] - f[..., 1]), 200 * (f[..., 1] - f[..., 2])


def readouts(n):
    Lb, ab, bb = to_lab(f"{SRC}/originals/original-{n}.jpg")
    La, aa, ba = to_lab(f"{SRC}/retouched/retouched-{n}.jpg")
    cb, ca = np.hypot(ab, bb).mean(), np.hypot(aa, ba).mean()
    return {
        "a*":       "%+.1f → %+.1f" % (ab.mean(), aa.mean()),
        "b*":       "%+.1f → %+.1f" % (bb.mean(), ba.mean()),
        "chroma":   "%+.0f%%" % ((ca / cb - 1) * 100),
        "contrast": "%+.0f%%" % ((La.std() / Lb.std() - 1) * 100),
        "L-bar":    "%.0f → %.0f" % (Lb.mean(), La.mean()),
    }


if __name__ == "__main__":
    for n in (int(x) for x in sys.argv[1:]) or range(1, 110):
        try:
            r = readouts(n)
        except FileNotFoundError:
            continue
        print(n, "  ".join(f"{k} {v}" for k, v in r.items()))
