import os, shutil
import build_exports as B
from PIL import Image
Image.MAX_IMAGE_PIXELS = None
S = B.SRC
SPECIAL = {}
_load = B.load
def load(kind, n):
    return _load(kind, n)
B.load = load

SEARCH10 = [7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
ICELAND8 = list(range(88, 96))
MASKS16  = [52, 53, 54, 55, 56, 58, 59, 60, 61, 63, 64, 65, 66, 67, 68, 70]

def justified(nums, rows, W, gap=6):
    ims=[load("r",n) for n in nums]; ar=[i.width/i.height for i in ims]
    per=sum(ar)/rows; out=[]; cur=[]; acc=0.0
    for i,a in enumerate(ar):
        cur.append(i); acc+=a
        if acc>=per and len(out)<rows-1: out.append(cur); cur=[]; acc=0.0
    if cur: out.append(cur)
    laid=[]; H=0
    for r in out:
        h=int((W-gap*(len(r)-1))/sum(ar[i] for i in r)); laid.append((r,h)); H+=h+gap
    H-=gap
    c=Image.new("RGB",(W,H),B.BG); y=0
    for r,h in laid:
        x=0
        for k,i in enumerate(r):
            w=W-x if k==len(r)-1 else int(ar[i]*h)
            c.paste(ims[i].resize((max(1,w),max(1,h)),Image.LANCZOS),(x,y)); x+=w+gap
        y+=h+gap
    return c

ITEMS = {
 "01-whole-set-matched": ("SHEETS", [11, 9, 94, 52]),
 "02-colour-casts":      (None,     [50, 99, 45, 73, 109]),
 "03-portraits":         (None,     [21, 106, 96, 6]),
 "04-landscape-drone":   (None,     [75, 3, 71, 103, 25]),
 "05-cleanup-removal":   (None,     [40, 92]),
 "06-bw-selective":      (None,     [89, 67, 27, 80]),
}

B.OUT = OUT = "/home/claude/exports3"
shutil.rmtree(OUT, ignore_errors=True); os.makedirs(OUT)

def build(folder, W, H, cap, gw):
    for item,(sp,nums) in ITEMS.items():
        i=1
        if sp=="SHEETS":
            for name,ns,rows in (("narrative-series",SEARCH10,3),
                                 ("editorial-series-iceland",ICELAND8,3),
                                 ("conceptual-fashion-series",MASKS16,4)):
                B.save(justified(ns,rows,gw), f"{folder}/{item}/{item}-{i:02d}-{name}-contact-sheet.jpg", maxbytes=cap); i+=1
        for n in nums:
            B.save(B.ba_split(n,W,H), f"{folder}/{item}/{item}-{i:02d}-pair-{n}.jpg", maxbytes=cap); i+=1

build("01-upwork", 2000, 1500, 9_000_000, 2000)
build("03-fiverr-portfolio", 1920, 1152, 40_000_000, 1920)
build("04-freelancer", 1800, 1350, 9_000_000, 1800)

W,H = 1280,769; CH = H-round(H*0.165); MB = 4_800_000
G1="02-fiverr-gig-images/gig-1-colour-grading"; G2="02-fiverr-gig-images/gig-2-whole-set-grading"
B.save(B.framed(B.ba_split(47,W,CH,lab_scale=1.5),W,H,
  ["COLOUR GRADING FOR PHOTOGRAPHERS","Exposure, white balance, grade, crop, export"]), f"{G1}/gig1-01-thumbnail.jpg", maxbytes=MB)
B.save(B.framed(B.pair_rows([100,23],W,CH),W,H,
  ["FLAT FILES IN, PUBLISH-READY OUT","Landscape, travel and portrait work"]), f"{G1}/gig1-02-range.jpg", maxbytes=MB)
B.save(B.framed(B.ba_split(40,W,CH,lab_scale=1.5),W,H,
  ["CLEAN-UP INCLUDED","Objects removed and the ground rebuilt underneath"]), f"{G1}/gig1-03-cleanup.jpg", maxbytes=MB)
B.save(B.framed(justified(MASKS16,4,1600),W,H,
  ["ONE GRADE, WHOLE SHOOT","Every frame in the delivery matched to one look"]), f"{G2}/gig2-01-thumbnail.jpg", maxbytes=MB)
B.save(B.framed(justified(ICELAND8,3,1600),W,H,
  ["A LOOK BUILT FOR EACH SHOOT","Preset per project, then every frame checked by hand"]), f"{G2}/gig2-02-second-set.jpg", maxbytes=MB)
B.save(B.framed(B.pair_rows([94,92],W,CH),W,H,
  ["SHOT-TO-SHOT CONSISTENCY","Same trip, same look, frame after frame"]), f"{G2}/gig2-03-consistency.jpg", maxbytes=MB)
print("done")
