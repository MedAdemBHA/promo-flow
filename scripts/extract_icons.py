r"""Extract an app's REAL icons as static SVG files — icons in the video are never drawn or generated.

Run from the promo repo; every source is optional, combine what the app uses:

    python3 kit/extract_icons.py --out ui/icons/web \
        --tsx-exports <app>/src/components/svgs/index.tsx   # many `export function Name(...) { return <svg/> }` in one file
    python3 kit/extract_icons.py --out ui/icons/mobile \
        --tsx-dir "<app>/src/assets/icons/*.tsx"            # one component per file (file name = icon name)
    python3 kit/extract_icons.py --out ui/icons/admin \
        --svg-dir "<app>/src/assets/svg/*.svg" \            # plain .svg files, copied
        --iconify solar:star-linear,mdi:check \             # Iconify ids the app uses (fetched from api.iconify.design)
        --mui <app>/node_modules:Add,Close,MoreHoriz         # @mui/icons-material names (paths read from the esm build)

The JSX → SVG converter handles {...props}, style={{}}, template-literal attributes, `{cond && (` wrappers,
width/height/color expressions, camelCase SVG attributes and JSX comments.
Open ui/icons/<surface>/ in a browser (or a gallery page) to check every icon renders.
"""
import argparse, glob, os, re, shutil, subprocess

ATTR = {"strokeWidth": "stroke-width", "strokeLinecap": "stroke-linecap", "strokeLinejoin": "stroke-linejoin", "strokeMiterlimit": "stroke-miterlimit",
        "strokeOpacity": "stroke-opacity", "strokeDasharray": "stroke-dasharray", "fillRule": "fill-rule", "clipRule": "clip-rule", "clipPath": "clip-path",
        "fillOpacity": "fill-opacity", "stopColor": "stop-color", "stopOpacity": "stop-opacity", "xmlnsXlink": "xmlns:xlink", "xlinkHref": "xlink:href",
        "className": "class"}


def jsx_to_svg(block, default_color="currentColor"):
    block = re.sub(r"\{\s*\.\.\.\w+\s*\}", "", block)                     # {...props}
    block = re.sub(r"\s[\w:-]+=\{`[^`]*`\}", "", block)                      # template-literal attrs (clipPath={`url(#${id})`})
    block = re.sub(r"\{\s*[\w.!]+\s*&&\s*\(", "", block)                    # {cond && (  → keep the element
    block = re.sub(r"\)\s*\}", "", block)
    block = re.sub(r"style=\{\{([^}]*)\}\}", lambda m: 'style="' + "; ".join(                # style={{ mixBlendMode: 'color' }}
        re.sub(r"([A-Z])", lambda c: "-" + c.group(1).lower(), k.strip()) + ": " + v.strip().strip("'\"")
        for k, v in (kv.split(":", 1) for kv in m.group(1).split(",") if ":" in kv)) + '"', block)
    vb = re.search(r'viewBox="([\d.\s-]+)"', block)
    w = h = None
    if vb:
        _, _, w, h = vb.group(1).split()
    block = re.sub(r"\bwidth=\{[^}]*\}", f'width="{w}"', block)
    block = re.sub(r"\bheight=\{[^}]*\}", f'height="{h}"', block)
    block = re.sub(r"=\{\s*color\s*\}", f'="{default_color}"', block)
    block = re.sub(r"=\{\s*([\d.]+)\s*\}", r'="\1"', block)               # numeric expressions
    block = re.sub(r'=\{\s*"([^"]*)"\s*\}', r'="\1"', block)              # {"..."}
    block = re.sub(r"=\{[^}]*\}", '="currentColor"', block)              # any other expression → currentColor
    for k, v in ATTR.items():
        block = re.sub(rf"\b{k}=", f"{v}=", block)
    block = re.sub(r"\{/\*.*?\*/\}", "", block, flags=re.S)               # JSX comments
    if "xmlns=" not in block:
        block = block.replace("<svg", '<svg xmlns="http://www.w3.org/2000/svg"', 1)
    return re.sub(r"\n\s*\n", "\n", block).strip() + "\n"



def write(out, name, svg):
    os.makedirs(out, exist_ok=True)
    open(os.path.join(out, name.replace(" ", "_") + ".svg"), "w").write(svg)


def tsx_exports(path, out):
    src, n = open(path).read(), 0
    for m in re.finditer(r"export (?:default )?function (\w+)\(([^)]*)\)\s*\{(.*?)\n\}", src, flags=re.S):
        color = re.search(r'color\s*=\s*"([^"]+)"', m.group(2))
        svg = re.search(r"<svg.*?</svg>", m.group(3), flags=re.S)
        if svg:
            write(out, m.group(1), jsx_to_svg(svg.group(0), color.group(1) if color else "currentColor")); n += 1
    return n


def tsx_dir(pattern, out):
    n = 0
    for p in sorted(glob.glob(pattern)):
        for k, m in enumerate(re.finditer(r"<svg.*?</svg>", open(p).read(), flags=re.S)):
            write(out, os.path.splitext(os.path.basename(p))[0] + (f"_{k}" if k else ""), jsx_to_svg(m.group(0))); n += 1
    return n


def svg_dir(pattern, out):
    os.makedirs(out, exist_ok=True)
    files = sorted(glob.glob(pattern))
    for f in files:
        shutil.copy(f, os.path.join(out, os.path.basename(f).replace(" ", "_")))
    return len(files)


def iconify(ids, out):
    n = 0
    for full in ids.split(","):
        prefix, name = full.split(":", 1)
        r = subprocess.run(["curl", "-sf", f"https://api.iconify.design/{prefix}/{name}.svg"], capture_output=True, text=True)
        if r.returncode == 0 and r.stdout.startswith("<svg"):
            write(out, f"{prefix}-{name}", r.stdout); n += 1
        else:
            print("  not found:", full)
    return n


def mui(spec, out):
    modules, names = spec.split(":", 1)
    n = 0
    for ic in names.split(","):
        f = f"{modules}/@mui/icons-material/esm/{ic}.js"
        ds = re.findall(r'd:\s*"([^"]+)"', open(f).read()) if os.path.exists(f) else []
        if ds:
            write(out, f"mui-{ic}", '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor">'
                  + "".join(f'<path d="{d}"/>' for d in ds) + "</svg>\n"); n += 1
        else:
            print("  not found:", ic)
    return n


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Extract an app's real icons as SVG files.")
    ap.add_argument("--out", required=True, help="output folder, e.g. ui/icons/web")
    ap.add_argument("--tsx-exports", help="one .tsx file exporting many icon components")
    ap.add_argument("--tsx-dir", help='glob of .tsx files, one icon per file (quote it)')
    ap.add_argument("--svg-dir", help='glob of .svg files to copy (quote it)')
    ap.add_argument("--iconify", help="comma list of prefix:name Iconify ids")
    ap.add_argument("--mui", help="<node_modules path>:Name,Name")
    a = ap.parse_args()
    for flag, fn in (("tsx_exports", tsx_exports), ("tsx_dir", tsx_dir), ("svg_dir", svg_dir), ("iconify", iconify), ("mui", mui)):
        v = getattr(a, flag)
        if v:
            print(f"{flag.replace('_', '-')}: {fn(v, a.out)} icons → {a.out}")
