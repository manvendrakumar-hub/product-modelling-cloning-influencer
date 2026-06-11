# Higgsfield Engine Catalog — what to use for each job

Query live with `models_explore(action='list'|'search'|'recommend')`. IDs/params below are the
ones used in the Minnie × OWNDAYS build (June 2026) and may evolve.

## IMAGE models (`generate_image`)
| Model ID | Use it for | Key params |
|---|---|---|
| `nano_banana_pro` | **Default for identity-locked stills, 4K, text/diagrams.** Routes to engine `nano_banana_2` in the job record — expected, output is true 4K. | `resolution` 1k/2k/4k; `medias[].role=image` (multi-ref ok) |
| `nano_banana_2` | Fast next-gen, image-to-image | `resolution` 1k/2k/4k |
| `soul_2` / `soul_v2` | Purpose-built realistic **character / portrait / UGC**; takes max 1 ref; optional trained `soul_id` | `quality` 1.5k/2k |
| `nano_banana` | Budget realistic | — |
| `kling_omni_image` | Versatile photoreal | `resolution` 1k/2k |

- Aspect ratios: 1:1, 3:2, 2:3, 4:3, 3:4, 4:5, 5:4, 9:16, 16:9, 21:9.
- For a character **face sheet** use 16:9 4k; for portraits 4:5 / 9:16.
- Multiple reference images improve identity but **don't over-stack** (degrades fidelity) — 2–3 is plenty.

## VIDEO models (`generate_video`)
| Model ID | Use it for | Notes |
|---|---|---|
| `marketing_studio_video` | **One-click product ads & Virtual Try-On.** | `mode=virtual_try_on` (Pro VTO) or `ugc_virtual_try_on`; pass `avatars=[{id,type:'custom'|'preset'}]` + `product_ids=[...]`; auto-enhances prompt; **avatar image controls wardrobe**; hooks/settings only for UGC/Tutorial/Unboxing/Product Review/UGC-VTO (NOT Pro VTO). dur 4–15. |
| `cinematic_studio_3_0` | **Cinema-grade single shot**, image-to-video | roles image/start_image/end_image; dur 4–15; **no audio param (silent)** |
| `cinematic_studio_video_v2` | Cinema with `genre` + `mode` pro/std | dur 3–12 |
| `kling3_0` | **Posing, finger-level hands, multi-shot, audio** | `mode` std/pro/4k; `sound` on/off; roles start_image/end_image; dur 3–15. Best for deliberate model posing. |
| `kling2_6` | Cinematic motion, physics | `sound` bool; dur 5/10 |
| `seedance_2_0` | Reference-driven identity, smart cuts, genre, audio | dur 4–15. **WARNING: aggressive NSFW filter** — false-positives on midriff/crop-top refs blocked our runs twice. |
| `veo3_1` / `veo3` | Ultra-real cinematic | start_image; veo3_1 dur 4/6/8 only |
| `wan2_7` | Synced audio, character-consistent | — |
| `higgsfield_preset` | Preset-routed i2v (viral templates) | needs `preset_id` from `presets_show` |

## Marketing Studio presets (`show_marketing_studio action=presets`)
UGC · Tutorial · Unboxing · Hyper Motion · Product Review · TV Spot · Wild Card ·
UGC Virtual Try On (`ugc_virtual_try_on`) · **Pro Virtual Try On (`virtual_try_on`)**.

## Engine-by-goal cheat sheet
- Identity stills / character sheet imagery → `nano_banana_pro`.
- Quick branded try-on ad → `marketing_studio_video` + `virtual_try_on` (wardrobe via avatar).
- Cinematic product beats to stitch → `cinematic_studio_3_0` (silent) + local edit.
- Model posing + hands → `kling3_0` (4k).
- Avoid `seedance_2_0` for figure/fashion if the reference shows skin — NSFW false-positives.
