# Character Sheet Template (written spec)

Fill from the chosen reference frames. This spec is the prompt backbone for every later generation.
Keep it factual — describe what is actually in the frames, not an idealization.

## Header
- **Name / handle:**
- **Source:** <reference video/photos>  ·  built from real frames  ·  **no facial alteration**
- **Visual sheet:** <montage png>

## Canonical reference frames (lock geometry to these)
| Angle | Frame | File |
|-------|-------|------|
| Frontal (primary) | | |
| Three-quarter | | |
| Profile | | |
| Full body — look 1 | | |
| Full body — look 2 | | |

## Face spec
- **Identity:** age range, ethnicity, sex
- **Face shape:** (oval / heart / round / square; jaw + chin)
- **Skin:** tone, finish, texture
- **Eyes:** shape, colour, lid type, tilt
- **Brows:** shape, thickness, colour
- **Nose:** bridge, tip
- **Lips:** fullness, cupid's bow, tint
- **Cheeks:** cheekbone height, blush
- **Hair:** colour + style per look
- **Makeup:** overall look
- **Wardrobe:** per look
- **Eyewear / product worn:** exact description
- **Expression:** default demeanour

## Face-lock prompt fragment (paste into generations)
> [age] [ethnicity] [sex], [face shape] with [jaw/chin], [skin], [eyes], [brows], [nose], [lips],
> [cheeks], [makeup]. **Keep identity and facial geometry identical to the frontal reference frame;
> do not distort the face.**

## Worked example — Minnie × OWNDAYS
- Early-20s East-Asian woman; soft oval-heart face, tapered jaw, rounded chin; warm-fair dewy skin;
  almond dark-brown low-lid eyes, subtle upturn; straight-soft dark brows; slim straight nose,
  rounded tip; full rosy-nude lips, soft cupid's bow; high soft cheekbones; black-brown hair
  (Look 1 slicked low bun / Look 2 long straight); clean monochrome-rose glam.
- Product: OWNDAYS rimless silver-wire frame; variants = rose-tinted lens (source) and
  fully clear colorless lens (generated).
- Anchors used: frontal frame 110, 3-4 frame 100, profile frame 120, full-body frames 075/165.
