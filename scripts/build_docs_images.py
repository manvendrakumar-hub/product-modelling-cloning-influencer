"""Generate likeness-free README graphics (banner, pipeline diagram, character-sheet mock)."""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(HERE, "docs"); os.makedirs(DOCS, exist_ok=True)
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
BLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def F(b, s): return ImageFont.truetype(BLD if b else REG, s)

BG=(22,24,28); PANEL=(31,34,40); LINE=(54,58,66); INK=(238,238,236)
SUB=(150,156,166); AMBER=(206,124,72); TEAL=(90,170,160)
def ctext(d,cx,y,t,f,fill):
    b=d.textbbox((0,0),t,font=f); d.text((cx-(b[2]-b[0])/2,y),t,font=f,fill=fill)

# ---------- 1. BANNER ----------
W,H=1280,448
im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
for y in range(H):  # vertical gradient
    t=y/H; d.line([(0,y),(W,y)],fill=(int(22+t*8),int(24+t*8),int(28+t*10)))
d.rectangle([0,0,W,6],fill=AMBER)
ctext(d,W/2,96,"PRODUCT MODELLING",F(True,76),INK)
ctext(d,W/2,182,"CLONING AN INFLUENCER",F(True,40),AMBER)
ctext(d,W/2,256,"reference video  →  character sheet  →  identity-locked stills  →  product videos",F(False,24),SUB)
# pill chips
chips=["Claude Skill","grid-review QA","Nano Banana · Kling · Cinema","tooling only — no likeness media"]
fx=F(True,20); xs=[]; tot=0
for c in chips:
    w=d.textbbox((0,0),c,font=fx)[2]+40; xs.append(w); tot+=w+14
x=(W-tot)/2; y=330
for c,w in zip(chips,xs):
    d.rounded_rectangle([x,y,x+w,y+44],radius=22,fill=PANEL,outline=LINE,width=1)
    ctext(d,x+w/2,y+11,c,fx,INK if c!=chips[-1] else TEAL); x+=w+14
im.save(f"{DOCS}/banner.png"); print("banner")

# ---------- 2. PIPELINE ----------
W,H=1400,820
im=Image.new("RGB",(W,H),BG); d=ImageDraw.Draw(im)
d.text((48,40),"THE PIPELINE",font=F(True,40),fill=INK)
d.text((48,92),"Eight steps. Anchor every generation to real frames — never distort the face.",font=F(False,22),fill=SUB)
steps=[("01","Extract frames","bundled ffmpeg, no install"),
       ("02","Pick hero frame","clean frontal / 3-4 / profile"),
       ("03","Character sheet","written spec + real-frame montage"),
       ("04","Identity-locked stills","face sheet · turnaround · variants"),
       ("05","Virtual try-on","avatar drives wardrobe + product"),
       ("06","Cinematic shots","image-to-video per beat"),
       ("07","Posing video","body + finger-level hand motion"),
       ("08","Fast-cut + QA","local edit · frame-by-frame check")]
cols=4; cw=312; ch=270; gx=48; gy=150; gap=24
for i,(n,t,s) in enumerate(steps):
    r,c=divmod(i,cols); x=gx+c*(cw+gap); y=gy+r*(ch+gap)
    d.rounded_rectangle([x,y,x+cw,y+ch],radius=18,fill=PANEL,outline=LINE,width=2)
    d.rounded_rectangle([x,y,x+cw,y+8],radius=4,fill=AMBER if r==0 else TEAL)
    d.text((x+24,y+30),n,font=F(True,46),fill=AMBER if r==0 else TEAL)
    d.text((x+24,y+104),t,font=F(True,27),fill=INK)
    # wrap sub
    words=s.split(); cur=""; ly=y+150
    for wd in words:
        tt=(cur+" "+wd).strip()
        if d.textbbox((0,0),tt,font=F(False,21))[2]>cw-48: d.text((x+24,ly),cur,font=F(False,21),fill=SUB); ly+=28; cur=wd
        else: cur=tt
    d.text((x+24,ly),cur,font=F(False,21),fill=SUB)
    if c<cols-1 and i<len(steps)-1:
        ay=y+ch//2; d.line([(x+cw+4,ay),(x+cw+gap-4,ay)],fill=AMBER,width=3)
im.save(f"{DOCS}/pipeline.png"); print("pipeline")

# ---------- 3. CHARACTER SHEET MOCK (placeholders, no real face) ----------
W,H=1240,760
im=Image.new("RGB",(W,H),(244,244,242)); d=ImageDraw.Draw(im)
INK2=(28,30,34); SUB2=(120,125,135); LN=(208,212,220)
d.text((40,34),"CHARACTER SHEET",font=F(True,44),fill=INK2)
d.text((40,90),"layout mock — silhouettes shown; you bring consented, licensed source media",font=F(False,21),fill=SUB2)
d.line([(40,128),(W-40,128)],fill=LN,width=2)
def silhouette(x,y,w,h,label):
    d.rounded_rectangle([x,y,x+w,y+h],radius=12,fill=(228,229,232),outline=LN,width=2)
    cx=x+w/2; hd=w*0.32
    d.ellipse([cx-hd/2,y+h*0.18,cx+hd/2,y+h*0.18+hd],fill=(196,199,205))   # head
    d.pieslice([cx-w*0.32,y+h*0.46,cx+w*0.32,y+h*1.15],180,360,fill=(196,199,205))  # shoulders
    d.text((x+12,y+h-30),label,font=F(True,18),fill=SUB2)
fx=( W-80-2*24)//3
for i,lab in enumerate(["FRONTAL","THREE-QUARTER","PROFILE"]):
    silhouette(40+i*(fx+24),150,fx,300,lab)
bw=(760-24)//2
for i,lab in enumerate(["LOOK 01 — FULL BODY","LOOK 02 — FULL BODY"]):
    silhouette(40+i*(bw+24),474,bw,250,lab)
# spec panel
px=40+760+24; pw=W-40-px
d.rounded_rectangle([px,150,px+pw,724],radius=14,fill=(255,255,255),outline=LN,width=2)
d.text((px+24,172),"FACE SPEC",font=F(True,26),fill=INK2); d.line([(px+24,212),(px+pw-24,212)],fill=LN,width=2)
rows=["Face shape","Skin","Eyes","Brows","Nose","Lips","Hair","Makeup","Eyewear","Expression"]
yy=232
for r in rows:
    d.text((px+24,yy),r.upper(),font=F(True,18),fill=INK2)
    d.rounded_rectangle([px+150,yy+2,px+pw-24,yy+16],radius=6,fill=(232,233,236))
    yy+=48
im.save(f"{DOCS}/character-sheet-mock.png"); print("mock")
print("done ->", DOCS)
