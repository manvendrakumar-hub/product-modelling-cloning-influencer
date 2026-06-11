import subprocess, imageio_ffmpeg
FF = imageio_ffmpeg.get_ffmpeg_exe()
SRC = "/Users/manvendrakumar/Desktop/Minnie Product Video"

# (file, start_sec, zoom, face_bias)  each cut = 0.5s
# zoom 1.0 = full frame; <1 = punch-in. face_bias shifts crop up for face shots.
cuts = [
 ("s1_hook",    0.2, 1.00, False),  # 1  hook face
 ("s1_hook",    1.6, 0.55, True),   # 2  ZOOM to eyes/lens
 ("s4_walk",    0.3, 1.00, False),  # 3  full-body blazer reveal
 ("s3_detail",  0.4, 1.00, False),  # 4  product detail
 ("s2_reveal",  1.2, 0.85, True),   # 5  chin-lift gaze
 ("s4_walk",    1.4, 0.70, False),  # 6  body punch-in (pose)
 ("s1_hook",    2.6, 0.45, True),   # 7  macro eyes
 ("s3_detail",  1.6, 0.60, False),  # 8  product hinge zoom
 ("s4_walk",    2.2, 1.00, False),  # 9  full body stance
 ("s2_reveal",  2.4, 0.80, True),   # 10 hand near temple
 ("s1_hook",    3.0, 0.95, False),  # 11 face front
 ("s4_walk",    0.9, 0.65, False),  # 12 body pose punch-in
 ("s3_detail",  2.6, 1.00, False),  # 13 product rotate
 ("s2_reveal",  3.2, 0.55, True),   # 14 soft-smile ECU
 ("s4_walk",    3.0, 1.00, False),  # 15 step toward camera
 ("s1_hook",    0.9, 0.70, True),   # 16 face 3/4-ish
 ("s3_detail",  0.9, 0.50, False),  # 17 macro glint
 ("s4_walk",    1.9, 0.85, False),  # 18 body
 ("s3_detail",  3.2, 1.00, False),  # 19 product hero
 ("s5_endcard", 2.2, 1.00, False),  # 20 END CARD
]

SW, SH = 720, 1280          # source 9:16
OW, OH = 1080, 1920         # output 9:16
DUR = 0.5

inputs = []
for f, st, z, fb in cuts:
    inputs += ["-ss", f"{st:.2f}", "-t", f"{DUR}", "-i", f"{SRC}/clips/{f}.mp4"]

filt = []
labels = []
for i, (f, st, z, fb) in enumerate(cuts):
    cw = int(SW * z) // 2 * 2
    ch = int(SH * z) // 2 * 2
    x = (SW - cw) // 2
    y = int((SH - ch) * (0.28 if fb else 0.5))
    filt.append(
        f"[{i}:v]crop={cw}:{ch}:{x}:{y},scale={OW}:{OH}:flags=lanczos,"
        f"setsar=1,fps=24,format=yuv420p[v{i}]"
    )
    labels.append(f"[v{i}]")
filt.append("".join(labels) + f"concat=n={len(cuts)}:v=1:a=0[out]")

cmd = [FF, "-y", "-hide_banner", "-loglevel", "error", *inputs,
       "-filter_complex", ";".join(filt),
       "-map", "[out]", "-c:v", "libx264", "-pix_fmt", "yuv420p",
       "-crf", "18", "-preset", "medium",
       f"{SRC}/Minnie_OWNDAYS_fastreel_20cuts.mp4"]
print("running ffmpeg with", len(cuts), "cuts...")
import os
out = f"{SRC}/Minnie_OWNDAYS_fastreel_20cuts.mp4"
print("inputs:", len(inputs), "filters:", len(filt))
r = subprocess.run(cmd, capture_output=True, text=True)
print("rc", r.returncode, "exists", os.path.exists(out), "size", os.path.getsize(out) if os.path.exists(out) else 0)
print("STDOUT:\n", r.stdout[-1500:])
print("STDERR:\n", r.stderr[-3000:])
