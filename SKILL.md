---
name: product-modelling-cloning-influencer
description: >-
  End-to-end pipeline to CLONE a real influencer / model from a reference video or photos
  and produce product-modelling videos (eyewear, apparel, accessories) — without distorting
  the person's face. Covers: frame extraction, building a character sheet, generating
  ultrarealistic identity-locked stills (face sheet + full-body turnaround + wardrobe / product
  variants), Marketing Studio Pro Virtual Try-On, Cinema Studio multi-shot films, Kling posing
  videos, and local fast-cut montage editing — all QA'd frame-by-frame. Use whenever the user
  wants to: clone a model/influencer, build a character/reference sheet, make a product modelling
  or try-on video, generate an avatar that wears a product, create posing / fashion reels, or
  turn a reference clip into new branded video. Trigger on: "clone this model", "character sheet",
  "virtual try-on", "product modelling video", "make her wear X", "posing video", "fast-cut reel",
  "replicate this video", or any influencer-style product video built from a real person's likeness.
---

# Product Modelling — Cloning an Influencer
## Reference video / photos → character sheet → identity-locked stills → product videos

You clone a real person's likeness and use it to model a product across stills and videos,
**without distorting the face**. Every visual claim is verified against frames you actually
extracted and viewed (see `references/` and the companion **grid-review** skill).

Tooling is **zero-install**: Python with `imageio`, `imageio_ffmpeg` (bundles its own ffmpeg —
no system ffmpeg/Homebrew), and `Pillow`. Video/image generation runs through **Higgsfield MCP**.

---

## THE GOLDEN RULE — Do Not Distort The Face

The person is real. Their likeness is the product's credibility. Every generation step must
**anchor to real reference frames** and say so in the prompt
(`identity IDENTICAL to reference, do not distort the face`). When you can avoid AI-inventing
a face at all (montage from real frames, local edit), prefer it. Verify identity on every output.

---

## STEP 0 — Setup (one-time, no admin)

```bash
python3 -c "import imageio, imageio_ffmpeg, PIL" 2>/dev/null && echo OK \
  || pip3 install --user imageio imageio-ffmpeg pillow
```
`imageio_ffmpeg.get_ffmpeg_exe()` returns a full ffmpeg binary (libx264 included) even when
the `ffmpeg` CLI is absent. Use it for ALL extraction, stitching, and encoding.

---

## STEP 1 — Extract & pick the hero frame

Extract frames from the reference video, then pick the clearest **frontal**, **three-quarter**,
and **profile** of the face (and full-body shots for wardrobe).

```python
import imageio_ffmpeg, subprocess
FF = imageio_ffmpeg.get_ffmpeg_exe()
subprocess.run([FF,"-i","ref.mp4","-start_number","1","frames/frame_%05d.png"])
```
Then view a spread of frames (Read tool) and choose: large, sharp, near-frontal, both eyes
visible, neutral expression. Note the frame numbers — they become your canonical anchors.

---

## STEP 2 — Build the character sheet

Two deliverables:
1. **Written spec** (`references/character-sheet-template.md`) — face shape, skin, eyes, brows,
   nose, lips, cheeks, hair, makeup, wardrobe, eyewear, expression + a **face-lock prompt fragment**
   + a **canonical reference frames** table (which frame = which angle).
2. **Visual montage sheet** — a labelled contact sheet built from the REAL frames (zero distortion).
   Use `scripts/build_sheet.py` as the template (crops frontal/3-4/profile + full-body looks,
   draws labels + a spec panel).

This written spec is reused as the prompt backbone for every later generation.

---

## STEP 3 — Generate ultrarealistic identity-locked stills

Higgsfield `generate_image`. **Upload the real reference frames first** (see uploads in
`references/gotchas-and-uploads.md`) and pass them as `medias[].role="image"`.

- **Model:** `nano_banana_pro` (Google "Nano Banana Pro"). NOTE: the platform routes Pro requests
  to engine `nano_banana_2` in the job record — output is genuine 4K, this is expected.
  `soul_2` is the alternative purpose-built character model.
- **Resolution** `4k`, aspect `16:9` for sheets / `4:5`/`9:16` for portraits.
- Generate, in order: **face sheet** (front / 3-4L / 3-4R / profile / up-tilt / down),
  **full-body turnaround** (front / 3-4 / side / back), then **variants** (no-glasses,
  alternate wardrobe, product variant e.g. clear vs tinted lens).
- Every prompt ends with: *"Keep identity and facial geometry identical to the reference; do not
  distort the face."* Reuse the written face spec verbatim.

**Product-variant trick:** to change one attribute (e.g. tinted → clear lens) keep the frame refs,
keep identity language, and state the change emphatically: *"the SAME frame BUT fully clear
transparent colorless lenses, no tint."*

---

## STEP 4 — Marketing Studio · Pro Virtual Try-On (one-click ad)

`show_marketing_studio` presets include **Pro Virtual Try On** (`slug: virtual_try_on`).
Flow:
1. `show_marketing_studio action=create type=avatar` from a clean image of the person.
2. `show_marketing_studio action=create type=product` from the product shots.
3. `generate_video model=marketing_studio_video mode=virtual_try_on aspect_ratio=9:16
   resolution=1080p generate_audio=true product_ids=[...] avatars=[{id,type:'custom'}]`.

**KEY LEARNING — wardrobe is driven by the AVATAR image, not the prompt.** MS auto-rewrites your
prompt (you'll see `enhanced_prompt`) and will invent clothing if the avatar has none. To control
wardrobe (e.g. "put her in the brown blazer"), create the avatar from an image where she already
wears it. To replicate an approved video's motion in new clothes: reuse the same prompt + product,
swap to a wardrobe-correct avatar.

---

## STEP 5 — Cinema Studio · multi-shot film

`cinematic_studio_3_0` (most advanced) or `cinematic_studio_video_v2` (genre control). Image-to-video,
one clip per storyboard shot from your hero stills (`medias[].role="start_image"`), 9:16, dur 4–15.
No audio param (silent — add music in edit). Then **stitch locally** (Step 7). Build a
**director grid sheet** first to plan shots — see `scripts/build_director_grid.py`
(storyboard cells from real stills + camera direction + Director's Note, in the seedance format).

---

## STEP 6 — Posing videos · Kling 3.0

For active **body posing + finger-level hand gestures**, `kling3_0` is the best engine
(`mode`: std/pro/4k, `sound` on/off, dur 3–15, `medias[].role="start_image"`). Start from the
**full-body** still for body poses, prompt a **mix framing** (open full-body → push to 3/4 for
hand-to-face/adjust-glasses gestures). Use the **posing-phrase library**
(`references/posing-prompt-library.md`). For "fast-paced": prompt *rapid succession of poses,
snappy rhythm, fast push-in/whip-pan* (Kling renders continuous motion, not hard cuts — for true
hard cuts, edit locally in Step 7).

---

## STEP 7 — Local fast-cut montage / editing

Hard-cut editing, punch-in "zoom" reframes, and concatenation are done locally with the bundled
ffmpeg — **zero credits, full control**. `scripts/build_reel.py` is the template: define a list of
`(clip, start, zoom, face_bias)` cuts (~0.5s each), crop+scale each to 1080×1920, concat. This is
also the reliable fallback when a single-gen montage engine refuses (e.g. Seedance NSFW block):
generate clean takes, then cut down to a 20-shot reel locally.

---

## STEP 8 — QA every output (always)

Use the **grid-review** skill: sample ~every 0.5s into a labelled contact sheet, view it, and run
the failure checklist — **identity drift, wardrobe drift, lens tint creeping back, warped product,
hand/finger artifacts, text legibility**. State which file you inspected. Remind the user you can
only judge **stills** — they must **playback-check motion + audio**.

---

## ENGINES, GOTCHAS, LIBRARIES — read the references

- `references/engine-catalog.md` — Higgsfield image+video model IDs, params, when to use each.
- `references/gotchas-and-uploads.md` — the upload flow, the Expect:100-continue stall fix,
  NSFW false-positives, preset-recommendation notices, `get_cost`, "GPT 2.0 doesn't exist".
- `references/posing-prompt-library.md` — researched fashion posing + hand-gesture phrases.
- `references/character-sheet-template.md` — the written character-sheet format + face-lock fragment.
- `scripts/` — `build_sheet.py`, `build_director_grid.py`, `build_reel.py` (reusable templates).

---

## DECISION FLOW

```
Have a real person to clone?
  → Extract frames → pick hero → character sheet → identity-locked stills (always first)
Goal = quick branded try-on ad?        → Marketing Studio Pro VTO (avatar drives wardrobe)
Goal = cinematic multi-shot product film? → Cinema Studio 3.0 per-shot + local stitch
Goal = model posing / hand motion?      → Kling 3.0 (4k), posing-phrase library
Goal = punchy fast-cut reel?            → local ffmpeg montage from clean takes
Always: QA with grid-review. Never distort the face. Show plan + grid sheet before burning credits.
```

## OPERATING PRINCIPLES (learned on the job)
1. **Show the plan + a creative grid sheet BEFORE spending credits.** Get a go/scope decision.
2. **Never distort the face** — anchor every gen to real frames; prefer real-frame edits when possible.
3. **Verify, don't assume** — grid every render; report what you actually saw, flag motion as unchecked.
4. **Pick the engine for the job** — try-on→Marketing Studio, posing→Kling, film→Cinema, edit→local.
5. **Be honest about failures** — NSFW blocks, wardrobe overrides, model routing — surface them.
