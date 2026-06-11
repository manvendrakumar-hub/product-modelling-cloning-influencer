from PIL import Image, ImageDraw, ImageFont

SRC = "frames"
REG = "/System/Library/Fonts/Supplemental/Arial.ttf"
BLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"

def font(b, s):
    return ImageFont.truetype(BLD if b else REG, s)

INK = (24, 26, 30)
SUB = (110, 115, 125)
LINE = (210, 213, 220)
BG = (247, 247, 245)
CARD = (255, 255, 255)

W, H = 2000, 1460
cv = Image.new("RGB", (W, H), BG)
d = ImageDraw.Draw(cv)

M = 64

# ---- Header ----
d.text((M, 56), "MINNIE", font=font(True, 88), fill=INK)
d.text((M, 156), "CHARACTER REFERENCE SHEET", font=font(True, 30), fill=SUB)
d.text((M, 200), "Source: OWNDAYS PHOTOSHADE film  ·  built from real frames  ·  no facial alteration",
        font=font(False, 24), fill=SUB)
d.line([(M, 256), (W - M, 256)], fill=LINE, width=2)

def card(box, img, w, h):
    """paste img into box (x,y,w,h) as a centered cover-fit card with border."""
    x, y = box
    fitted = img.copy()
    # cover fit
    scale = max(w / fitted.width, h / fitted.height)
    fitted = fitted.resize((int(fitted.width * scale), int(fitted.height * scale)))
    left = (fitted.width - w) // 2
    top = (fitted.height - h) // 2
    fitted = fitted.crop((left, top, left + w, top + h))
    cv.paste(fitted, (x, y))
    d.rectangle([x, y, x + w, y + h], outline=LINE, width=2)

def label(x, y, w, text):
    bb = d.textbbox((0, 0), text, font=font(True, 24))
    tw = bb[2] - bb[0]
    d.text((x + (w - tw) / 2, y), text, font=font(True, 24), fill=INK)

def crop(f, box):
    return Image.open(f"{SRC}/frame_{f}.png").crop(box)

# ---- Geometry: left image block + right spec panel ----
fx0 = M
specW = 520
gap = 40
leftW = (W - M) - specW - 30 - M   # = 1318

# ---- Face row : frontal / three-quarter / profile ----
fy = 300
fw = (leftW - 2 * gap) // 3
fh = 536
faces = [
    ("00110", (300, 0, 870, 1010), "FRONTAL"),
    ("00100", (250, 20, 830, 980), "THREE-QUARTER"),
    ("00120", (330, 0, 910, 1020), "PROFILE"),
]
for i, (f, box, lab) in enumerate(faces):
    x = fx0 + i * (fw + gap)
    card((x, fy), crop(f, box), fw, fh)
    label(x, fy + fh + 14, fw, lab)

# ---- Full-body looks ----
by = fy + fh + 70
bw = (leftW - gap) // 2
bh = 470
looks = [
    ("00075", (150, 120, 900, 1900), "LOOK 01 · OVERSIZED BLAZER"),
    ("00165", (250, 150, 850, 1820), "LOOK 02 · PREP UNIFORM"),
]
for i, (f, box, lab) in enumerate(looks):
    x = fx0 + i * (bw + gap)
    card((x, by), crop(f, box), bw, bh)
    label(x, by + bh + 14, bw, lab)

# ---- Spec panel (right column) ----
px = fx0 + leftW + 30
pw = W - M - px
py = fy - 6
pbot = by + bh + 40
d.rectangle([px, py, px + pw, pbot], fill=CARD, outline=LINE, width=2)
ix = px + 30
iy = py + 30
d.text((ix, iy), "FACE SPEC", font=font(True, 30), fill=INK)
d.line([(ix, iy + 42), (px + pw - 30, iy + 42)], fill=LINE, width=2)
iy += 64

spec = [
    ("Identity", "Young East-Asian woman, early 20s"),
    ("Face shape", "Soft oval / heart; gently tapered jaw, rounded chin"),
    ("Skin", "Warm fair, smooth, dewy finish; even tone"),
    ("Eyes", "Almond, dark brown, mono/low lid; subtle upturn"),
    ("Brows", "Straight-to-soft-arch, medium, dark brown"),
    ("Nose", "Straight slim bridge, refined rounded tip"),
    ("Lips", "Full balanced; soft cupid's bow; rosy-nude tint"),
    ("Cheeks", "High soft cheekbones; peach-rose blush draped"),
    ("Hair", "Black-brown; L1 slicked-back low bun; L2 long straight"),
    ("Makeup", "Clean glam; flushed monochrome rose; glossy lip"),
    ("Eyewear", "OWNDAYS rimless, silver wire, rose/pink tint lens"),
    ("Expression", "Calm, neutral-cool, lips slightly parted"),
]
for k, v in spec:
    d.text((ix, iy), k.upper(), font=font(True, 21), fill=INK)
    # wrap value
    words = v.split()
    lines, cur = [], ""
    maxw = pw - 60
    for wd in words:
        t = (cur + " " + wd).strip()
        if d.textbbox((0, 0), t, font=font(False, 21))[2] > maxw:
            lines.append(cur); cur = wd
        else:
            cur = t
    lines.append(cur)
    yy = iy + 26
    for ln in lines:
        d.text((ix, yy), ln, font=font(False, 21), fill=SUB)
        yy += 27
    iy = yy + 12

# ---- Footer ----
d.line([(M, H - 56), (W - M, H - 56)], fill=LINE, width=2)
d.text((M, H - 42), "Reference frames: 110 (frontal) · 100 (3/4) · 120 (profile) · 075 / 165 (wardrobe)   —   keep facial geometry locked to these crops.",
        font=font(False, 22), fill=SUB)

cv.save("Minnie_character_sheet.png")
print("saved", cv.size)
