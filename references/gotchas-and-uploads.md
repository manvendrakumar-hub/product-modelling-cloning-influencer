# Gotchas & Upload Flow (the hard-won part)

## Uploading local media to Higgsfield
Three steps:
1. `media_upload(files=[{filename, content_type}], method='upload_url')` → returns presigned PUT
   URL + `media_id` + a CDN `url`.
2. `curl -X PUT --data-binary @file '<upload_url>'` to push the bytes.
3. `media_confirm(type='image', media_ids=[...])`.

Then reference by `media_id` in `generate_image`/`generate_video` `medias[].value`, or by the CDN
`url` for avatar/product creation.

### ⚠️ Big-PNG PUT stalls (Expect: 100-continue)
Large PNGs (15–25 MB 4K stills) **hang** on `curl PUT` — the request waits on an HTTP
`100-continue` that never resolves, then times out at 0 bytes. Fixes (use all three):
- **Downscale & convert to JPEG** first (≤1800 px long edge, quality ~92) — refs/avatars/products
  don't need 4K. ~0.2–0.5 MB uploads instantly.
- Add **`-H "Expect:"`** to the curl to disable the 100-continue handshake.
- Add `--max-time 60`.
```bash
curl -sS --max-time 60 -H "Expect:" -X PUT -H "Content-Type: image/jpeg" \
  --data-binary @small.jpg '<upload_url>' -o /dev/null -w "%{http_code}\n"
```
A backgrounded curl that sits at 0 bytes is this stall — kill it and re-PUT the small JPEG.

## NSFW false-positives (Seedance especially)
`seedance_2_0` returns `status:"nsfw"` and blocks the render on benign fashion content when the
**reference image shows midriff / crop-top / skin**, even with modest prompts. Two strikes = stop
retrying that path. Fixes:
- Use a **covered reference** (chest-up / buttoned wardrobe) and say "fully covered, professional".
- **Switch engine** — Kling 3.0 / Cinema Studio 3.0 / Marketing Studio did NOT false-flag.
- Or pivot to a **local edit** from already-clean takes.

## Preset-recommendation notices
`generate_video` may return `{notice:{type:"preset_recommendation", ...}}` instead of starting a
job ("This looks like preset X"). To generate your literal prompt, **re-call with
`declined_preset_id: <that preset id>`**. It may suggest a different preset next — decline again.

## Cost control
- `get_cost:true` on `generate_image`/`generate_video` preflights credits without spending.
- Check `balance`. Image 4K ≈ seconds–tens of seconds; video 60–240s (4K Kling longest).
- **Show the plan + a creative grid sheet and get a go/scope decision before batch-generating.**

## Naming / misc
- "GPT 2.0" / "GPT image" **does not exist** in Higgsfield — clarify; usually they mean Nano Banana
  Pro/2 or Soul 2.0.
- Marketing Studio `enhanced_prompt` shows how MS rewrote your text — read it to see what it locked.
- Job results: poll `job_status(jobId, sync=true)` (server waits ~25s). Download `results.rawUrl`.
- `.skill` files are **zip archives** (SKILL.md + references/...). `unzip` to read them.

## Pacing long renders without spamming polls
Background a `sleep` (`run_in_background:true`), wait for its completion notification, then poll
`job_status` once. Cheaper than repeated sync polls. 4K Kling can take 4–6 min.
