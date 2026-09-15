import ast, json, os, re, math
import numpy as np
from PIL import Image
Image.MAX_IMAGE_PIXELS=None
BASE="/mnt/user-data/uploads/retouch examples"
O=f"{BASE}/originals"; R=f"{BASE}/retouched"
def ret(n):
    for p in (f"{R}/masks/retouched-{n}.jpg", f"{R}/iceland/retouched-{n}.jpg",
              f"{R}/the endless search/retouched-{n}.jpg", f"{R}/retouched-{n}.jpg"):
        if os.path.exists(p): return p
def lab(p):
    im=Image.open(p).convert("RGB"); im.thumbnail((900,900),Image.LANCZOS)
    a=np.asarray(im,dtype=np.float64)/255.0
    a=np.where(a<=0.04045,a/12.92,((a+0.055)/1.055)**2.4)
    M=np.array([[0.4124564,0.3575761,0.1804375],[0.2126729,0.7151522,0.0721750],[0.0193339,0.1191920,0.9503041]])
    t=(a@M.T)/np.array([0.95047,1.0,1.08883]); d=6/29
    f=np.where(t>d**3,np.cbrt(t),t/(3*d*d)+4/29)
    return 116*f[...,1]-16, 500*(f[...,0]-f[...,1]), 200*(f[...,1]-f[...,2])
def stats(n):
    pb,pa=f"{O}/original-{n}.jpg", ret(n)
    Lb,ab,bb=lab(pb); La,aa,ba=lab(pa)
    cb,ca=np.hypot(ab,bb),np.hypot(aa,ba)
    wb,hb=Image.open(pb).size; wa,ha=Image.open(pa).size
    return dict(a_b=ab.mean(),a_a=aa.mean(),b_b=bb.mean(),b_a=ba.mean(),
        chroma=(ca.mean()/cb.mean()-1)*100, c95_after=float(np.percentile(ca,95)),
        cmean_after=float(ca.mean()),
        contrast=(La.std()/Lb.std()-1)*100, L_b=Lb.mean(), L_a=La.mean(),
        ar_b=wb/hb, ar_a=wa/ha, wh_b=(wb,hb), wh_a=(wa,ha))
def num(s):
    s=s.replace("−","-").replace("+","")
    m=re.findall(r'-?\d+\.?\d*', s)
    return [float(x) for x in m]
def ar_val(tok):
    tok=tok.strip()
    if ":" in tok:
        a,b=tok.split(":"); return float(a)/float(b)
    return float(tok)
src=open("make_page.py",encoding="utf-8").read()
ITEM=None
for node in ast.parse(src).body:
    if isinstance(node,ast.Assign) and getattr(node.targets[0],'id','')=="ITEM":
        ITEM=ast.literal_eval(node.value)
bad=[]
for n,(kick,note,reads) in sorted(ITEM.items()):
    try: S=stats(n)
    except Exception as e: bad.append((n,"FILE",str(e))); continue
    for r in reads:
        t=r.replace("−","-").replace("→","->").replace("̄","")
        if t.startswith("a*") or t.startswith("b*"):
            ch=t[0]; v=num(t)
            got=(S[f"{ch}_b"],S[f"{ch}_a"])
            if len(v)>=2 and (abs(v[0]-got[0])>0.35 or abs(v[1]-got[1])>0.35):
                bad.append((n,r,f"measured {got[0]:+.1f} -> {got[1]:+.1f}"))
        elif t.startswith("chroma"):
            v=num(t)
            if v and abs(v[0]-S["chroma"])>2.0: bad.append((n,r,f"measured {S['chroma']:+.0f}%"))
        elif t.startswith("contrast"):
            v=num(t)
            if v and abs(v[0]-S["contrast"])>2.0: bad.append((n,r,f"measured {S['contrast']:+.0f}%"))
        elif t.startswith("L "):
            v=num(t)
            if len(v)>=2 and (abs(v[0]-S["L_b"])>1.5 or abs(v[1]-S["L_a"])>1.5):
                bad.append((n,r,f"measured {S['L_b']:.0f} -> {S['L_a']:.0f}"))
        elif t=="no crop":
            if abs(S["ar_b"]-S["ar_a"])>0.01: bad.append((n,r,f"aspect {S['ar_b']:.3f} -> {S['ar_a']:.3f}"))
        elif t=="converted to mono":
            if S["c95_after"]>0.5: bad.append((n,r,f"NOT MONO: mean chroma {S['cmean_after']:.2f}, p95 {S['c95_after']:.2f}"))
        elif "->" in t and re.match(r'^[\d.:]+\s*->\s*[\d.:]+$', t):
            a,b=[x.strip() for x in t.split("->")]
            try: va,vb=ar_val(a),ar_val(b)
            except: continue
            if abs(va-S["ar_b"])>0.02 or abs(vb-S["ar_a"])>0.02:
                bad.append((n,r,f"aspect {S['ar_b']:.3f} -> {S['ar_a']:.3f}  {S['wh_b']}->{S['wh_a']}"))
print(f"{len(bad)} problems\n")
for n,chip,why in bad: print(f"  #{n:<4} {chip:<28} {why}")
