from PIL import Image, ImageDraw, ImageFont

REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
BLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def F(b, s): return ImageFont.truetype(BLD if b else REG, s)

INK=(22,24,28); SUB=(120,125,135); LINE=(208,212,220); BG=(245,245,243)
CARD=(255,255,255); ACC=(196,72,52); CHIP=(34,36,42)

W,H = 2260, 1740
cv = Image.new("RGB",(W,H),BG); d = ImageDraw.Draw(cv)
M = 60

# ---------- Header ----------
d.text((M,46), "MINNIE × OWNDAYS", font=F(True,72), fill=INK)
d.text((M,130), "PRODUCT MODELLING FILM  ·  CREATIVE DIRECTOR GRID SHEET", font=F(True,28), fill=SUB)

brief = [
    ("PRODUCT","OWNDAYS rimless silver-wire frame · clear lens"),
    ("TALENT","Minnie (identity-locked from ref.mp4)"),
    ("FORMAT","9:16 vertical · ~15s · fast-paced cuts"),
    ("LOOK","Studio cyclorama · chocolate-brown tailoring"),
    ("GRADE","Clean neutral 5600K · soft beauty key · subtle teal floor"),
    ("AUDIO","Minimal pulse + glass/fabric foley · light bass"),
]
bx = M; by = 190
for i,(k,v) in enumerate(brief):
    col = i % 3; row = i//3
    x = M + col*((W-2*M)//3); y = by + row*54
    d.text((x,y), k, font=F(True,20), fill=ACC)
    d.text((x+150,y), v, font=F(False,20), fill=INK)
d.line([(M,by+120),(W-M,by+120)], fill=LINE, width=2)

# ---------- Track banners ----------
ty = by+140
d.text((M,ty), "TRACK A — MARKETING STUDIO · PRO VIRTUAL TRY-ON", font=F(True,24), fill=CHIP)
d.text((M,ty+34), "Avatar (Minnie) + Product (frame) → auto try-on ad.  One-click, social-ready.  Lock identity, let the engine pose.", font=F(False,21), fill=SUB)
d.text((M+1300,ty), "TRACK B — CINEMA STUDIO 3.0 · FAST MODELLING FILM", font=F(True,24), fill=CHIP)
d.text((M+1300,ty+34), "8 image-to-video shots from our hero stills,\ncut fast. Hook → turns → detail → walk → end-card.", font=F(False,21), fill=SUB)
d.line([(M,ty+92),(W-M,ty+92)], fill=LINE, width=2)

# ---------- Storyboard cells ----------
SRC = "/Users/manvendrakumar/Desktop/Minnie Product Video"
def load(p): return Image.open(p).convert("RGB")
def fcrop(im, fr):
    w,h = im.size; l,t,r,b = fr
    return im.crop((int(l*w),int(t*h),int(r*w),int(b*h)))

shots = [
 dict(src="Minnie_clear_glasses_portrait.png", fr=(0.20,0.26,0.80,0.60),
      n="01 · HOOK", tc="0.0–1.8s", typ="ECU / MACRO", cam="rack focus, static",
      act="Clear lens snaps into focus — silver wire catches a light glint on the bridge."),
 dict(src="Minnie_clear_glasses_portrait.png", fr=None,
      n="02 · REVEAL", tc="1.8–3.6s", typ="MCU · 85mm", cam="slow dolly in",
      act="Minnie lifts chin to camera, fingers leaving the temple. Eyes settle."),
 dict(src="Product /2.png", fr=(0.05,0.12,0.95,0.92),
      n="03 · DETAIL", tc="3.6–5.2s", typ="ECU · macro", cam="side tracking glint",
      act="Rimless edge + hinge detail — light travels the wire. Pure product beauty."),
 dict(src="Minnie_fullbody_clear_glasses.png", fr=(0.06,0.04,0.94,0.96),
      n="04 · STANCE", tc="5.2–7.4s", typ="MWS · 35mm", cam="slow orbit left",
      act="Full body — oversized blazer, weight-shift pose. Confident, editorial."),
 dict(src="Minnie_clear_glasses_portrait.png", fr=(0.16,0.30,0.84,0.58),
      n="05 · GAZE", tc="7.4–9.0s", typ="CU · 100mm", cam="static, shallow DoF",
      act="Eyes through clear lens — a blink, a micro-smile. Lens reads invisible."),
 dict(src="Minnie_fullbody_clear_glasses.png", fr=(0.10,0.10,0.90,0.85),
      n="06 · WALK", tc="9.0–11.4s", typ="MWS · 50mm", cam="tracking, fast",
      act="Strides toward camera, blazer in motion. Energy beat — the fast cut."),
 dict(src="Product /1.png", fr=(0.06,0.14,0.94,0.86),
      n="07 · HERO", tc="11.4–13.2s", typ="ECU · macro", cam="slow orbit",
      act="The frame alone, floating on grey — silver glint, weightless rimless form."),
 dict(src="Product /1.png", fr=(0.0,0.0,1.0,1.0),
      n="08 · END CARD", tc="13.2–15.0s", typ="WS · clean", cam="pull back, static",
      act="Product centered, negative space top — OWNDAYS logo + clear-lens line."),
]

cols=4; cell_w=480; img_h=560; lab_h=170; gap=18
gx0 = M; gy0 = ty+108
for i,s in enumerate(shots):
    c = i%cols; r = i//cols
    x = gx0 + c*(cell_w+gap); y = gy0 + r*(img_h+lab_h+gap)
    im = load(f"{SRC}/{s['src']}")
    if s["fr"]: im = fcrop(im, s["fr"])
    sc = max(cell_w/im.width, img_h/im.height)
    im = im.resize((int(im.width*sc), int(im.height*sc)))
    im = im.crop(((im.width-cell_w)//2,(im.height-img_h)//2,(im.width+cell_w)//2,(im.height+img_h)//2))
    cv.paste(im,(x,y))
    # label card
    d.rectangle([x,y+img_h,x+cell_w,y+img_h+lab_h], fill=CARD, outline=LINE, width=2)
    # shot number chip
    d.rectangle([x,y,x+196,y+34], fill=CHIP)
    d.text((x+10,y+7), s["n"], font=F(True,19), fill=(255,255,255))
    d.text((x+cell_w-86,y+8), s["tc"], font=F(True,18), fill=(255,255,255))
    d.rectangle([x+cell_w-92,y,x+cell_w,y+30], fill=ACC)
    d.text((x+cell_w-86,y+6), s["tc"], font=F(True,17), fill=(255,255,255))
    # label text
    ly = y+img_h+12
    d.text((x+14,ly), s["typ"], font=F(True,21), fill=INK)
    d.text((x+14,ly+30), s["cam"], font=F(False,19), fill=ACC)
    # wrap action
    words=s["act"].split(); cur=""; lines=[]
    for w in words:
        t=(cur+" "+w).strip()
        if d.textbbox((0,0),t,font=F(False,19))[2] > cell_w-28: lines.append(cur); cur=w
        else: cur=t
    lines.append(cur)
    yy=ly+62
    for ln in lines[:4]:
        d.text((x+14,yy), ln, font=F(False,19), fill=SUB); yy+=24

# ---------- Footer: director's note ----------
fy = gy0 + 2*(img_h+lab_h+gap) + 6
d.line([(M,fy),(W-M,fy)], fill=LINE, width=2)
d.text((M,fy+14), "DIRECTOR'S NOTE", font=F(True,24), fill=INK)
notes = [
 ("SIGNATURE MOMENT","Shot 01 hook + Shot 05 gaze — spend best credits here; the clear lens must read as truly invisible."),
 ("GENERATE FIRST","Shot 04 (full-body orbit) as the anchor — confirms wardrobe + identity hold under motion before the rest."),
 ("WATCH FOR","Lens staying colourless (no rose tint creeping back); silver wire not melting; face identity locked across cuts."),
 ("IF IT FAILS","Add 'fully transparent colorless optical lens, no tint' + 'identity identical to reference' and regen that shot only."),
]
ny=fy+52
for k,v in notes:
    d.text((M,ny), k, font=F(True,20), fill=ACC)
    d.text((M+230,ny), v, font=F(False,20), fill=INK); ny+=38

cv.save(f"{SRC}/Minnie_director_grid_sheet.png")
print("saved", cv.size)
