"""Generate likeness-free demo assets: docs/demo.gif (fast-cut montage style) + docs/social-preview.png.
Pure shapes/silhouettes — no real person, no brand media."""
import os, subprocess, imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOCS = os.path.join(HERE, "docs"); os.makedirs(DOCS, exist_ok=True)
FF = imageio_ffmpeg.get_ffmpeg_exe()
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
BLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
def F(b, s): return ImageFont.truetype(BLD if b else REG, s)
AMBER=(206,124,72); TEAL=(90,170,160); INK=(34,36,40); GREY=(196,199,205)
def ctext(d,cx,y,t,f,fill):
    b=d.textbbox((0,0),t,font=f); d.text((cx-(b[2]-b[0])/2,y),t,font=f,fill=fill)

W,Hc=540,960
def studio(bg=(236,237,235)):
    im=Image.new("RGB",(W,Hc),bg); d=ImageDraw.Draw(im)
    d.ellipse([-160,Hc-260,W+160,Hc+220],fill=(226,227,228))  # soft floor
    return im,d
def sil(d,cx,cy,s,pose):
    hd=120*s
    d.ellipse([cx-hd/2,cy-hd,cx+hd/2,cy],fill=GREY)                          # head
    d.pieslice([cx-150*s,cy+10*s,cx+150*s,cy+360*s],180,360,fill=GREY)        # shoulders/torso
    if pose=="hip":   d.polygon([(cx+120*s,cy+120*s),(cx+170*s,cy+150*s),(cx+120*s,cy+200*s)],fill=GREY)
    if pose=="cross": d.rounded_rectangle([cx-150*s,cy+150*s,cx+150*s,cy+200*s],radius=20,fill=(186,189,195))
    if pose=="hand":  d.ellipse([cx+40*s,cy-30*s,cx+90*s,cy+20*s],fill=(186,189,195))
def glasses(d,cx,cy,s):
    lw=150*s; lh=78*s; g=(120,124,130)
    for off in (-lw-22*s, 22*s):
        d.rounded_rectangle([cx+off,cy-lh/2,cx+off+lw,cy+lh/2],radius=26*s,outline=g,width=max(3,int(5*s)))
    d.line([(cx-22*s,cy-6*s),(cx+22*s,cy-6*s)],fill=g,width=max(3,int(5*s)))   # bridge
    d.line([(cx-lw-22*s,cy),(cx-lw-70*s,cy-10*s)],fill=g,width=max(3,int(4*s)))
    d.line([(cx+lw+22*s,cy),(cx+lw+70*s,cy-10*s)],fill=g,width=max(3,int(4*s)))

SHOTS=[("FULL BODY","pose"),("PUNCH-IN","zoom"),("POWER POSE","hip"),
       ("PRODUCT","prod"),("MACRO","prodzoom"),("3/4 TURN","turn"),
       ("HAND GESTURE","hand"),("YOUR LOGO","end")]
HOLD=3; fr=0; os.makedirs("/tmp/demoframes",exist_ok=True)
total=len(SHOTS)*HOLD
for i,(label,kind) in enumerate(SHOTS):
    im,d=studio()
    if kind in ("pose","hip","hand"): sil(d,W/2,300,1.0,{"hip":"hip","hand":"hand"}.get(kind,""))
    elif kind=="zoom": sil(d,W/2,470,1.9,"")
    elif kind=="turn": sil(d,W/2+30,300,1.0,"")
    elif kind=="prod": glasses(d,W/2,Hc/2,1.0)
    elif kind=="prodzoom": glasses(d,W/2,Hc/2,1.7)
    elif kind=="end":
        d.rounded_rectangle([W/2-150,Hc/2-70,W/2+150,Hc/2+10],radius=14,outline=(150,154,160),width=3)
        ctext(d,W/2,Hc/2-52,"YOUR LOGO",F(True,34),(120,124,130))
        ctext(d,W/2,Hc/2+40,"clean end card",F(False,22),(150,154,160))
    # chrome: shot label chip, timecode, progress bar, footer
    d.rounded_rectangle([24,24,24+18+ImageDraw.Draw(im).textbbox((0,0),label,font=F(True,26))[2],70],radius=18,fill=AMBER)
    d.text((34,32),label,font=F(True,26),fill=(255,255,255))
    d.text((W-118,30),f"0{i}·{i*0.5:.1f}s",font=F(True,22),fill=(120,124,130))
    d.rectangle([0,Hc-10,W,Hc],fill=(214,216,220))
    d.rectangle([0,Hc-10,int(W*((i*HOLD+HOLD)/total)),Hc],fill=AMBER)
    ctext(d,W/2,Hc-56,"build_reel.py  ·  synthetic demo  ·  no real likeness",F(False,20),(140,144,150))
    for _ in range(HOLD):
        im.save(f"/tmp/demoframes/f{fr:03d}.png"); fr+=1

subprocess.run([FF,"-y","-loglevel","error","-framerate","12","-i","/tmp/demoframes/f%03d.png",
  "-vf","scale=420:-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=64[p];[b][p]paletteuse",
  "-loop","0",f"{DOCS}/demo.gif"])
print("demo.gif", os.path.getsize(f"{DOCS}/demo.gif"))

# ---------- social preview 1280x640 ----------
W2,H2=1280,640; im=Image.new("RGB",(W2,H2),(22,24,28)); d=ImageDraw.Draw(im)
for y in range(H2):
    t=y/H2; d.line([(0,y),(W2,y)],fill=(int(22+t*8),int(24+t*8),int(28+t*10)))
d.rectangle([0,0,W2,8],fill=AMBER)
ctext(d,W2/2,150,"PRODUCT MODELLING",F(True,92),(238,238,236))
ctext(d,W2/2,258,"CLONING AN INFLUENCER",F(True,48),AMBER)
ctext(d,W2/2,348,"clone a model from a reference video  ·  produce product videos",F(False,28),(150,156,166))
ctext(d,W2/2,398,"without distorting the face",F(False,28),(150,156,166))
ctext(d,W2/2,498,"Claude skill  ·  scripts  ·  references      —      tooling only, no likeness media",F(True,24),(90,170,160))
im.save(f"{DOCS}/social-preview.png"); print("social-preview", im.size)
