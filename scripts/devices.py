"""Live-UI device projector — reusable for any promo.

A device = a keyed photo (laptop / phone / hand) + a live HTML UI canvas projected into its screen with an exact
CSS matrix3d (homography from the green-screen corners measured by prep_devices.py → devices.json).

    from devices import *
    html = device("laptop", "lap1", laptop_html, left=20, top=660, width=1040)
    js  += cam("lap1", "laptop", 1040, 20, 660, at=3.0, dur=0.9, z=1.6, ax=900, ay=300)   # push into a UI point
    x, y = at_screen("laptop", 20, 660, 1040, ax=1200, ay=110)                              # tap/ring on a UI point

Conventions (learned the hard way):
- The outer #id keeps any existing tweens (rise/push/swing); camera moves go on #id-cam.
- Devices carry mix-blend-mode:multiply on the OUTER element (never on a transformed child) so the photo's
  light background melts into the paper grid. Two blended devices must NOT overlap (they multiply each other).
- UI classes are namespaced (u-*) and ids prefixed per instance so the video kit css never leaks into the app.
- <video> may never sit inside a timed element: project it at root level with quad_video().
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
DEV = json.load(open(os.path.join(HERE, "devices.json"))) if os.path.exists(os.path.join(HERE, "devices.json")) else {}


# ---------------------------------------------------------------- geometry
def homography(src, dst):
    A, b = [], []
    for (x, y), (u, v) in zip(src, dst):
        A.append([x, y, 1, 0, 0, 0, -u * x, -u * y]); b.append(u)
        A.append([0, 0, 0, x, y, 1, -v * x, -v * y]); b.append(v)
    M = [row[:] + [bb] for row, bb in zip(A, b)]
    for c in range(8):
        p = max(range(c, 8), key=lambda r: abs(M[r][c])); M[c], M[p] = M[p], M[c]
        for r in range(8):
            if r != c:
                f = M[r][c] / M[c][c]; M[r] = [a - f * cc for a, cc in zip(M[r], M[c])]
    h = [M[i][8] / M[i][i] for i in range(8)]
    return [[h[0], h[1], h[2]], [h[3], h[4], h[5]], [h[6], h[7], 1.0]]


def matrix3d(H):
    (a, b, c), (d, e, f), (g, h, i) = H
    return "matrix3d(" + ",".join(f"{v:.9f}" for v in [a, d, 0, g, b, e, 0, h, 0, 0, 1, 0, c, f, 0, i]) + ")"


def geom(kind, width, grow=2.5):
    D = DEV[kind]
    x0, y0, cw, ch = D["crop"]; s = width / cw; q = D["quad"]
    cx = sum(p[0] for p in q) / 4; cy = sum(p[1] for p in q) / 4
    pts = []
    for (x, y) in q:
        dx, dy = x - cx, y - cy; L = (dx * dx + dy * dy) ** 0.5
        pts.append(((x + dx / L * grow - x0) * s, (y + dy / L * grow - y0) * s))
    SW, SH = D["screen"]
    return dict(s=s, w=width, h=ch * s, H=homography([(0, 0), (SW, 0), (SW, SH), (0, SH)], pts), SW=SW, SH=SH)


def screen_pt(kind, width, ax, ay):
    g = geom(kind, width); (a, b, c), (d, e, f), (gg, h, i) = g["H"]; w = gg * ax + h * ay + i
    return ((a * ax + b * ay + c) / w, (d * ax + e * ay + f) / w)


# ---------------------------------------------------------------- html
def device(kind, id_, ui, left, top, width, cls="", style="", fade=False):
    g = geom(kind, width)
    img = f'<img src="assets/dev/{kind}_c.png" alt="" style="position:absolute; left:0; top:0; width:{g["w"]:.1f}px; height:{g["h"]:.1f}px;" />'
    scr = f'<div class="scrq" style="width:{g["SW"]}px; height:{g["SH"]}px; transform:{matrix3d(g["H"])};">{ui}</div>'
    return (f'<div id="{id_}" class="dev3 blend {cls}" style="left:{left}px; top:{top}px; width:{g["w"]:.0f}px; height:{g["h"]:.0f}px; {style}">'
            f'<div id="{id_}-cam" class="dcam{" fade-r" if fade else ""}">{scr}{img}</div></div>')


def cam(id_, kind, width, left, top, at, dur, z, ax, ay, cx=540, cy=900, ease="power2.inOut"):
    px, py = screen_pt(kind, width, ax, ay)
    return f'tl.to("#{id_}-cam", {{ x: {cx - left - px * z:.1f}, y: {cy - top - py * z:.1f}, scale: {z}, duration: {dur}, ease: "{ease}" }}, {at});'


def cam_reset(id_, at, dur=0.6):
    return f'tl.to("#{id_}-cam", {{ x: 0, y: 0, scale: 1, duration: {dur}, ease: "power2.inOut" }}, {at});'


def at_screen(kind, L, T, W, ax, ay, r=48, camv=None):
    px, py = screen_pt(kind, W, ax, ay)
    if camv:
        z, ax0, ay0, cx, cy = camv; qx, qy = screen_pt(kind, W, ax0, ay0)
        return round(cx + (px - qx) * z - r), round(cy + (py - qy) * z - r)
    return round(L + px - r), round(T + py - r)


def quad_video(id_, src, kind, L, T, W, ux, uy, uw, uh, start, dur, mstart, origin, track=12):
    pts = [screen_pt(kind, W, x, y) for x, y in [(ux, uy), (ux + uw, uy), (ux + uw, uy + uh), (ux, uy + uh)]]
    H = homography([(0, 0), (uw, 0), (uw, uh), (0, uh)], [(L + x, T + y) for x, y in pts])
    return (f'<div id="{id_}-w" style="position:absolute; left:0; top:0; width:1080px; height:1920px; transform-origin:{origin[0]:.0f}px {origin[1]:.0f}px; opacity:0;">'
            f'<video id="{id_}" class="clip" src="{src}" muted playsinline data-start="{start}" data-duration="{dur}" data-media-start="{mstart}" data-track-index="{track}" '
            f'style="position:absolute; left:0; top:0; width:{uw}px; height:{uh}px; transform-origin:0 0; transform:{matrix3d(H)}; object-fit:contain; background:#000;"></video></div>')


# ---------------------------------------------------------------- UI isolation
def uclass(html):
    return re.sub(r'\bclass="([^"]*)"', lambda m: 'class="' + " ".join("u-" + c for c in m.group(1).split()) + '"', html)


def pfx(html, p):
    html = re.sub(r'\bid="', f'id="{p}', html)
    return uclass(html.replace("url(#", f"url(#{p}"))


def scope_css(css):
    """Scope an app stylesheet under .app and namespace its classes (u-*)."""
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.S); out, i, n = [], 0, len(css)
    while i < n:
        j = css.find("{", i)
        if j < 0: break
        sel = css[i:j].strip(); depth, k = 1, j + 1
        while depth and k < n:
            depth += {"{": 1, "}": -1}.get(css[k], 0); k += 1
        body = css[j + 1:k - 1]; i = k
        if sel.startswith("@font-face"): out.append(f"{sel} {{{body}}}"); continue
        if sel.startswith("@"): continue
        sels = []
        for s_ in (x.strip() for x in sel.split(",")):
            if s_ in ("html", "body", "#root"): continue
            sels.append(".app" if s_ == ":root" else ".app, .app *" if s_ == "*" else ".app " + re.sub(r"\.([A-Za-z][\w-]*)", r".u-\1", s_))
        if sels: out.append(", ".join(sels) + f" {{{body}}}")
    return "\n".join(out) + DEVICE_CSS


DEVICE_CSS = """
.dev3 { position: absolute; display: block; }
.dcam { position: absolute; inset: 0; transform-origin: 0 0; }
.scrq { position: absolute; left: 0; top: 0; transform-origin: 0 0; overflow: hidden; }
.float-ui { position: absolute; transform-origin: 50% 50%; }
.app { position: relative; }
"""


def grab(html, marker, tag_start=None):
    """The innermost card <div> (class contains "card") that encloses marker."""
    k = html.index(marker)
    starts = [m.start() for m in re.finditer(re.escape(tag_start) if tag_start else r'<div\b[^>]*\bclass="[^"]*\bcard\b', html[:k])]
    i, depth, j = starts[-1], 0, starts[-1]
    pat = re.compile(r"<div\b|</div>")
    while True:
        t = pat.search(html, j); depth += 1 if t.group(0) != "</div>" else -1; j = t.end()
        if depth == 0: return html[i:j]


def float_card(id_, card, w, h, left, top, scale, inner_id=None, style="", mobile=True):
    """Lift a UI card out of the screen: resized to a mobile width, scaled for a phone viewer, shadowed."""
    card = re.sub(r'(style="[^"]*?)\bwidth:\d+px;\s*height:\d+px;', rf'\1width:{w}px; height:{h}px;', card, count=1)
    card = re.sub(r'(style="[^"]*?)\b(right|left):-?\d+(px)?;\s*top:-?\d+(px)?;', r'\1left:0; top:0; overflow:hidden; box-shadow:0 40px 80px -30px rgba(13,17,3,0.35);', card, count=1)
    iid = f' id="{inner_id}"' if inner_id else ""
    return (f'<div id="{id_}" class="float-ui" style="left:{left}px; top:{top}px; width:{w * scale:.0f}px; height:{h * scale:.0f}px; {style}">'
            f'<div{iid} class="app{" mob" if mobile else ""}" style="position:absolute; left:0; top:0; width:{w}px; height:{h}px; transform:scale({scale}); transform-origin:0 0;">{card}</div></div>')


def replace_el(html, id_, new):
    m = re.search(rf'<img id="{re.escape(id_)}"[^>]*/>', html)
    if m: return html[:m.start()] + new + html[m.end():]
    m = re.search(rf'<(div|section)\b[^>]*\bid="{re.escape(id_)}"', html)
    tag, i, depth = m.group(1), m.end(), 1
    pat = re.compile(rf"<{tag}\b|</{tag}>")
    while depth:
        t = pat.search(html, i); depth += 1 if t.group(0) != f"</{tag}>" else -1; i = t.end()
    return html[:m.start()] + new + html[i:]


# ---------------------------------------------------------------- timeline helpers (paste into the page script)
UIJS = r'''
  const $u = (s) => document.querySelector(s);
  function uType(s, text, at, dur) { const el = $u(s); if (!el) return; el.textContent = ""; const o = { p: 0 };
    tl.fromTo(o, { p: 0 }, { p: 1, duration: dur, ease: "none", onUpdate: () => { el.textContent = text.slice(0, Math.ceil(o.p * text.length)); } }, at); }
  function uSet(s, text, at) { const el = $u(s); if (!el) return; const prev = el.innerHTML, o = { p: 0 };
    tl.fromTo(o, { p: 0 }, { p: 1, duration: 0.01, onUpdate: () => { el.innerHTML = o.p >= 1 ? text : prev; } }, at); }
  function uCount(s, from, to, at, dur, dec = 0) { const el = $u(s); if (!el) return; const o = { v: from };
    const fmt = (v) => dec ? v.toFixed(dec) : Math.round(v).toLocaleString("en-US"); el.textContent = fmt(from);
    tl.fromTo(o, { v: from }, { v: to, duration: dur, ease: "power2.out", onUpdate: () => { el.textContent = fmt(o.v); } }, at); }
  function uRing(s, at, col) { tl.to(s, { boxShadow: "0 0 0 4px " + col, duration: 0.2 }, at); }
'''
