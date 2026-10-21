"""Prepare generated media for one story (copies into the story, never touches inbox).

    python3 kit/prep_media.py --story stories/ST02 --img TL-04_knife,SK-09_resort-facade --vid VID-04_yousef --vo ST02
    python3 kit/prep_media.py --story stories/ST02 --img all            # every image in inbox/img

- images: generated on a flat paper colour → levels-lifted so the paper becomes white and
  `mix-blend-mode:multiply` melts them into the composition paper. PP-* (torn strips, tape, ticket) are keyed
  from #FF00FF instead; PP-01 (texture) is copied as is.
- clips: scaled to 1080x1920 (portrait) or 1920x1080 (landscape), 30 fps, short GOP for seeking, no audio.
- VO: loudnorm -16 LUFS, 48 kHz (inbox/vo/stories/<ID>.wav or inbox/vo/youtube/<ID>.wav).
Paper colour of the generated images: --paper F3EFE4 (default; sample PP-01 / a corner pixel when unsure).
"""
import argparse, glob, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ap = argparse.ArgumentParser()
ap.add_argument("--story", required=True)
ap.add_argument("--img", default="")
ap.add_argument("--vid", default="")
ap.add_argument("--vo", default="")
ap.add_argument("--paper", default="F3EFE4")
a = ap.parse_args()
S = a.story if os.path.isabs(a.story) else os.path.join(ROOT, a.story)
for d in ("img", "vid", "audio"):
    os.makedirs(f"{S}/assets/{d}", exist_ok=True)


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


def ids(spec, folder, ext):
    if spec == "all":
        return [os.path.splitext(os.path.basename(p))[0] for p in sorted(glob.glob(f"{ROOT}/inbox/{folder}/*.{ext}"))]
    return [x for x in spec.split(",") if x]


r, g, b = (int(a.paper[i:i + 2], 16) / 255 for i in (0, 2, 4))
LIFT = f"colorlevels=rimax={r - 0.008:.3f}:gimax={g - 0.008:.3f}:bimax={b - 0.008:.3f}"

for i in ids(a.img, "img", "png"):
    src, dst = f"{ROOT}/inbox/img/{i}.png", f"{S}/assets/img/{i}.png"
    if i.startswith("PP-01"):
        ff("-i", src, dst)
    elif i.startswith("PP-"):
        ff("-i", src, "-vf", "colorkey=0xFF00FF:0.32:0.08,despill=type=blue:mix=0.4", dst)
    else:
        ff("-i", src, "-vf", LIFT, dst)
    print("img", i)

for i in ids(a.vid, "vid", "mp4"):
    src = f"{ROOT}/inbox/vid/{i}.mp4"
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height",
                                    "-of", "csv=p=0", src], capture_output=True, text=True).stdout.strip().split(","))
    size = "1080:1920" if h > w else "1920:1080"
    ff("-i", src, "-vf", f"scale={size}:force_original_aspect_ratio=increase:flags=lanczos,crop={size},fps=30",
       "-an", "-c:v", "libx264", "-crf", "16", "-pix_fmt", "yuv420p", "-g", "15", f"{S}/assets/vid/{i}.mp4")
    print("vid", i)

for i in ids(a.vo, "vo/stories", "wav"):
    src = next((p for p in (f"{ROOT}/inbox/vo/stories/{i}.wav", f"{ROOT}/inbox/vo/youtube/{i}.wav") if os.path.exists(p)), None)
    if not src:
        print("missing VO", i)
        continue
    ff("-i", src, "-af", "loudnorm=I=-16:TP=-1.5:LRA=11", "-ar", "48000", f"{S}/assets/audio/{i}.wav")
    print("vo", i)
