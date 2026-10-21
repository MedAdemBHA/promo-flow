"""Key the green screen out of inbox/devices/*.png, measure the 4 screen corners, write kit/devices.json.

    python3 kit/prep_devices.py            # needs ffmpeg on PATH (no PIL needed)

For each DEV-xx_<kind>-green.png:
  - finds the chroma-green pixels, takes the 4 extreme corners (min/max of x+y and x−y) = screen quad
  - crops the device (bounding box of non-background pixels + margin)
  - keys the green (colorkey + despill) and lifts the background to white (for multiply blending)
  - writes assets/dev/<kind>_c.png (2x) and devices.json {kind: {crop, quad, screen}}
"""
import json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = f"{ROOT}/inbox/devices"
OUT = f"{ROOT}/kit/assets/dev"
os.makedirs(OUT, exist_ok=True)
KINDS = {"DEV-01_laptop-green": ("laptop", 1700), "DEV-02_phone-green": ("phone", 374), "DEV-03_hand-phone-green": ("hand", 374),
         "DEV-04_laptop-phone-green": ("duo", 1700), "DEV-04_hand-phone-green-f": ("hand_f", 374)}


def raw(path):
    w, h = map(int, subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=width,height", "-of", "csv=p=0", path],
                                   capture_output=True, text=True).stdout.strip().split(","))
    data = subprocess.run(["ffmpeg", "-v", "error", "-i", path, "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
    return w, h, data


def measure(path):
    w, h, d = raw(path)
    best = {"tl": (1e9, None), "br": (-1e9, None), "tr": (-1e9, None), "bl": (1e9, None)}
    xs, ys = [], []
    for y in range(0, h, 2):
        row = y * w * 3
        for x in range(0, w, 2):
            r, g, b = d[row + x * 3], d[row + x * 3 + 1], d[row + x * 3 + 2]
            if g > 180 and r < 110 and b < 110:
                s, t = x + y, x - y
                if s < best["tl"][0]: best["tl"] = (s, (x, y))
                if s > best["br"][0]: best["br"] = (s, (x, y))
                if t > best["tr"][0]: best["tr"] = (t, (x, y))
                if t < best["bl"][0]: best["bl"] = (t, (x, y))
            if (r + g + b) < 600:   # non-background pixel → device bbox
                xs.append(x); ys.append(y)
    quad = [best[k][1] for k in ("tl", "tr", "br", "bl")]
    m = 20
    crop = (max(0, min(xs) - m), max(0, min(ys) - m), min(w, max(xs) + m) - max(0, min(xs) - m), min(h, max(ys) + m) - max(0, min(ys) - m))
    return w, h, quad, crop


def main():
    out = {}
    for name, (kind, sw) in KINDS.items():
        p = f"{SRC}/{name}.png"
        if not os.path.exists(p):
            print("missing", p); continue
        w, h, quad, crop = measure(p)
        # normalise to 1024-wide space like the reference kit
        k = 1024 / w
        quad_n = [(round(x * k), round(y * k)) for x, y in quad]
        crop_n = tuple(round(v * k) for v in crop)
        qw = ((quad_n[1][0] - quad_n[0][0]) + (quad_n[2][0] - quad_n[3][0])) / 2
        qh = ((quad_n[3][1] - quad_n[0][1]) + (quad_n[2][1] - quad_n[1][1])) / 2
        out[kind] = dict(crop=crop_n, quad=quad_n, screen=(sw, round(sw * qh / qw)))
        x0, y0, cw, ch = crop
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", p, "-vf",
                        f"crop={cw}:{ch}:{x0}:{y0},scale={round(cw * k * 2)}:{round(ch * k * 2)}:flags=lanczos,format=rgba,"
                        "colorkey=0x00FF00:0.32:0.08,despill=type=green,curves=all='0/0 0.5/0.47 0.80/0.93 0.88/1 1/1'",
                        f"{OUT}/{kind}_c.png"], check=True)
        print(kind, "quad", quad_n, "crop", crop_n, "screen", out[kind]["screen"])
    json.dump(out, open(f"{ROOT}/kit/devices.json", "w"), indent=1)


if __name__ == "__main__":
    main()
