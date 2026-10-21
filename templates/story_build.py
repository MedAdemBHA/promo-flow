"""Story composition template — reference: ST01 · D-30 «214 وظيفة… و30 يوم» (collage only, no app UI).

    python3 build.py   → index.html   (then: npx --yes hyperframes@<pinned> check)

To make a new story, edit only the data blocks, top to bottom:
  1. VO / END            VO start (+0.4 s) and total duration (VO end + ~3 s outro)
  2. CAPS                exact VO lines + their ranges from `vo_timing.sh` (coarse)
  3. W_* word hits       from `vo_timing.sh` (fine) — objects pop on their word
  4. CUTS                scene cut points (= page tears)
  5. SFX / FIELDS        sound hits and extra collage pieces
  6. the scene sections  (A … G) in the HTML, and their tweens in the <script>
Asset paths are relative to the story's assets/ (filled by new_story.sh + prep_media.py).
"""
import random

VO = 0.4  # VO start in the composition
END = 22.8

# ---- VO lines (exact text from 00-bible/VO-MASTER-SA-QA.md) and their spoken ranges (composition time)
CAPS = [
    (0.40, 2.75, "باقي ثلاثين يوم على الافتتاح."),
    (3.20, 6.10, "ومنتجع ساحل يبي مئتين وأربعطعش موظف."),
    (6.65, 10.45, "شيف، ممرض، مهندس، محاسب… كل المجالات."),
    (11.00, 13.85, 'وقدّام عبدالعزيز… جبل من الـ <span class="lt">CVs</span>.'),
    (14.43, 15.85, "السؤال مو مين قدّم…"),
    (16.55, 18.70, "السؤال: مين يستاهل؟"),
]
# word hits inside line 3
W_CHEF, W_NURSE, W_ENG, W_ACC, W_ALL = 6.66, 7.24, 7.99, 8.62, 9.64

# ---- scenes (cut points)
CUTS = [3.0, 6.5, 10.6, 12.6, 16.3, 18.8]


def tear_poly(seed):
    """Left edge of a torn paper sheet: jagged points, right side straight."""
    rnd = random.Random(seed)
    pts = ["100% 0%", "100% 100%"]
    y = 100.0
    left = []
    while y > 0:
        left.append(f"{rnd.uniform(0.2, 2.6):.2f}% {y:.2f}%")
        y -= rnd.uniform(0.8, 2.2)
    left.append("1.2% 0%")
    return "polygon(" + ", ".join(pts + left) + ")"


def note_poly(seed):
    rnd = random.Random(seed)
    top = [f"{x}% {rnd.uniform(0, 7):.1f}%" for x in range(0, 101, 5)]
    bot = [f"{x}% {100 - rnd.uniform(0, 7):.1f}%" for x in range(100, -1, -5)]
    return "polygon(" + ", ".join(top + bot) + ")"


def note(id_, text, x, y, w, rot, seed, size=60, cls=""):
    return (f'<div id="{id_}" class="note {cls}" style="left:{x}px; top:{y}px; width:{w}px; transform:rotate({rot}deg); '
            f'clip-path:{note_poly(seed)}; font-size:{size}px;">{text}</div>')


def tool(id_, src, x, y, w, rot=0):
    return f'<img id="{id_}" class="tool blend" src="assets/img/{src}.png" alt="" style="left:{x}px; top:{y}px; width:{w}px; transform:rotate({rot}deg);" />'


tears = "\n".join(
    f'      <div id="tear{i}" class="clip tear" data-start="{c - 0.32:.2f}" data-duration="0.62" data-track-index="4" '
    f'style="clip-path:{tear_poly(i * 7 + 3)};"></div>' for i, c in enumerate(CUTS))

caps = "\n".join(
    f'      <div id="cap{i + 1}" class="clip cap" data-start="{a:.2f}" data-duration="{b - a:.2f}" data-track-index="6"><p>{t}</p></div>'
    for i, (a, b, t) in enumerate(CAPS))

# ---- sound design
SFX = [("stamp", 0.33, 0.30), ("pop", W_CHEF, 0.22), ("pop", W_NURSE, 0.22), ("pop", W_ENG, 0.22), ("pop", W_ACC, 0.22),
       ("thud", 4.95, 0.22), ("press", 5.9, 0.18), ("riser", W_ALL - 0.5, 0.12),
       ("pop", W_ALL + 0.1, 0.12), ("pop", W_ALL + 0.25, 0.12), ("pop", W_ALL + 0.4, 0.12),
       ("pop", 11.1, 0.2), ("thud", 12.75, 0.18), ("stamp2", 15.6, 0.22), ("pop", 17.55, 0.25),
       ("chime", 20.05, 0.22), ("sparkle", 21.5, 0.2)]
SFX += [("whoosh", c - 0.3, 0.16) for c in CUTS]
DUR = {"stamp": 0.9, "stamp2": 0.9, "pop": 0.4, "thud": 0.9, "press": 0.4, "riser": 1.2, "chime": 1.6, "sparkle": 1.2, "whoosh": 0.6}
sfx = "\n".join(
    f'      <audio id="fx{i}" src="assets/sfx/{n}.wav" data-start="{t:.2f}" data-duration="{DUR[n]}" data-track-index="{12 + i}" data-volume="{v}"></audio>'
    for i, (n, t, v) in enumerate(SFX))

FIELDS = [  # small extra tools for «كل المجالات»
    ("TL-05_pan", 40, 1060, 250, -8), ("TL-13_flask", 800, 1040, 220, 7), ("TL-16_gas-detector", 10, 640, 170, -6),
    ("TL-06_keycard", 820, 250, 230, 8), ("TL-11_blueprints", 430, 1110, 240, -3), ("TL-09_syringe", 440, 210, 210, 10)]
fields = "\n".join(tool(f"f{i}", s, x, y, w, r) for i, (s, x, y, w, r) in enumerate(FIELDS))

html = f"""<!doctype html>
<html lang="ar">
  <head>
    <meta charset="utf-8" />
    <title>ST01 · D-30</title>
    <script src="assets/gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Almarai"; src: url("assets/fonts/Almarai-ExtraBold.ttf"); font-weight: 800; }}
      @font-face {{ font-family: "Almarai"; src: url("assets/fonts/Almarai-Bold.ttf"); font-weight: 700; }}
      @font-face {{ font-family: "Urbanist"; src: url("assets/fonts/Urbanist.ttf"); font-weight: 100 900; }}
      :root {{ --cream: #F2EBDE; --green: #77B800; --green-strong: #5F9300; --green-ink: #3E7A12; --lime: #CBE88C; --ink: #0D1103; --alert: #D32F2F; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: var(--cream); }}
      #root {{ position: relative; width: 100%; height: 100%; overflow: hidden; background: var(--cream); font-family: "Almarai", sans-serif; color: var(--ink); }}
      .paper {{ position: absolute; inset: 0; background: var(--cream) url("assets/img/PP-01_paper.png") center / cover; }}
      .layer {{ position: absolute; inset: 0; }}
      .vid {{ position: absolute; left: 0; top: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .blend {{ mix-blend-mode: multiply; }}
      .tool {{ position: absolute; height: auto; }}
      .lt {{ font-family: "Urbanist", sans-serif; font-weight: 800; direction: ltr; unicode-bidi: isolate; }}

      /* torn paper notes (cream label + tape) */
      .note {{ position: absolute; background: #FBF8F1; padding: 26px 34px 30px; text-align: center; font-weight: 800; line-height: 1.15; direction: rtl;
        color: var(--ink); filter: drop-shadow(0 10px 14px rgba(13,17,3,0.18)); }}
      .note .g {{ color: var(--green-strong); }}
      .tape {{ position: absolute; width: 150px; mix-blend-mode: multiply; opacity: 0.9; }}

      /* headline (collage) */
      .hl {{ position: absolute; left: 70px; right: 70px; direction: rtl; text-align: center; font-weight: 800; line-height: 1.05; }}
      .hl .g {{ color: var(--green-strong); }}

      /* countdown stamp */
      #stamp {{ position: absolute; left: 64px; top: 190px; width: 210px; height: 210px; border-radius: 50%; border: 9px solid var(--green);
        box-shadow: inset 0 0 0 5px #F2EBDE, inset 0 0 0 10px var(--green); display: grid; place-items: center; transform: rotate(-12deg);
        background: rgba(242,235,222,0.88); color: var(--green-strong); text-align: center; }}
      #stamp b {{ display: block; font: 900 74px/1 "Urbanist", sans-serif; letter-spacing: -2px; direction: ltr; }}
      #stamp small {{ display: block; font: 800 30px/1 "Almarai", sans-serif; margin-top: 6px; }}

      /* page tear transition */
      .tear {{ position: absolute; top: 0; left: 0; width: 1500px; height: 1920px; background: #F7F2E8 url("assets/img/PP-01_paper.png") center / cover;
        filter: drop-shadow(-14px 0 18px rgba(13,17,3,0.25)); }}

      /* captions */
      .cap {{ position: absolute; left: 60px; right: 60px; bottom: 300px; display: flex; justify-content: center; }}
      .cap p {{ direction: rtl; text-align: center; font-weight: 700; font-size: 44px; line-height: 1.45; color: var(--ink); background: rgba(251,248,241,0.96);
        padding: 16px 38px 20px; border-radius: 28px; max-width: 960px; box-shadow: 0 14px 30px -16px rgba(13,17,3,0.35); border: 2px solid rgba(119,184,0,0.35); }}
      .cap p::before {{ content: ""; display: inline-block; width: 16px; height: 16px; border-radius: 50%; background: var(--green); margin-left: 16px; vertical-align: 6px; }}
      .cap .lt {{ font-weight: 700; color: var(--green-strong); }}

      #strike {{ position: absolute; height: 12px; border-radius: 6px; background: var(--alert); transform-origin: 100% 50%; }}
      #loopbox {{ position: absolute; left: -200px; top: 430px; width: 1480px; height: 833px;
        -webkit-mask-image: radial-gradient(ellipse 46% 44% at 50% 50%, #000 62%, transparent 100%); mask-image: radial-gradient(ellipse 46% 44% at 50% 50%, #000 62%, transparent 100%); }}
      #loopbox video {{ width: 100%; height: 100%; object-fit: cover; mix-blend-mode: multiply; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <div id="base" class="clip paper" data-start="0" data-duration="{END}" data-track-index="0"></div>

      <!-- Flow clips (track 1) -->
      <video id="v-cal" class="clip vid" src="assets/vid/VID-02_calendar-tear.mp4" muted playsinline data-start="0" data-duration="3.0" data-media-start="0.8" data-track-index="1"></video>
      <video id="v-abd" class="clip vid" src="assets/vid/VID-03_abdulaziz.mp4" muted playsinline data-start="10.6" data-duration="2.0" data-media-start="0.3" data-track-index="1"></video>
      <video id="v-cv" class="clip vid" src="assets/vid/VID-01_cv-mountain.mp4" muted playsinline data-start="12.6" data-duration="3.7" data-media-start="1.6" data-track-index="1"></video>

      <div id="loopbox"><video id="v-loop" class="clip" src="assets/vid/VID-14_loop.mp4" muted playsinline data-start="18.8" data-duration="{END - 18.8:.1f}" data-media-start="1.2" data-track-index="2"></video></div>

      <!-- A · 30 days -->
      <section id="sA" class="clip layer" data-start="0" data-duration="3.0" data-track-index="3">
        {note("a-hl", '<span style="font-size:58px;">باقي</span><br><span class="lt g" style="font-size:230px; line-height:0.95;">30</span> <span class="g">يوم</span><br><span style="font-size:58px;">على الافتتاح</span>', 250, 620, 580, -2, 11, 120)}
      </section>

      <!-- B · Sahel Resort needs 214 -->
      <section id="sB" class="clip layer" data-start="3.0" data-duration="3.5" data-track-index="3">
        <div id="b-lbl" class="hl" style="top:450px; font-size:62px;">منتجع <span class="g">ساحل</span> <span style="font-weight:700; font-size:44px; opacity:0.7;">· البحر الأحمر</span></div>
        <img id="b-res" class="tool blend" src="assets/img/SK-09_resort-facade.png" alt="" style="left:40px; top:540px; width:1000px;" />
        <img id="b-tix" class="tool" src="assets/img/PP-04_ticket.png" alt="" style="left:110px; top:1000px; width:860px; transform:rotate(-3deg);" />
        <div id="b-num" class="hl" style="top:1085px; font-size:96px; transform:rotate(-3deg);"><span id="b-cnt" class="lt g" style="font-size:250px; line-height:0.9;">0</span> موظف</div>
      </section>

      <!-- C · every field -->
      <section id="sC" class="clip layer" data-start="6.5" data-duration="4.1" data-track-index="3">
        <div id="c-grid" class="layer">
          {tool("c-t1", "TL-04_knife", 590, 420, 380, -6)}
          {tool("c-t2", "TL-07_stethoscope", 110, 420, 380, 5)}
          {tool("c-t3", "TL-15_hardhat", 590, 830, 380, 4)}
          {tool("c-t4", "TL-17_calculator", 110, 830, 380, -5)}
          {note("c-n1", "شيف", 650, 740, 250, 4, 21, 64)}
          {note("c-n2", "ممرض", 170, 740, 260, -4, 22, 64)}
          {note("c-n3", "مهندس", 640, 1160, 270, -3, 23, 64)}
          {note("c-n4", "محاسب", 160, 1160, 270, 3, 24, 64)}
        </div>
        <div id="c-fields" class="layer">
{fields}
        </div>
        <div id="c-all" class="hl" style="top:1290px; font-size:130px;">كل <span class="g">المجالات</span></div>
      </section>

      <!-- D · Abdulaziz -->
      <section id="sD" class="clip layer" data-start="10.6" data-duration="2.0" data-track-index="3">
        {note("d-tag", 'عبدالعزيز<br><span style="font-size:40px; font-weight:700; white-space:nowrap;">مدير التوظيف · منتجع ساحل</span>', 400, 1110, 620, -3, 31, 64)}
        <img id="d-tape" class="tape" src="assets/img/PP-03_tape.png" alt="" style="left:640px; top:1075px; transform:rotate(8deg);" />
      </section>

      <!-- E · CV mountain -->
      <section id="sE" class="clip layer" data-start="12.6" data-duration="3.7" data-track-index="3">
        {note("e-hl", 'جبل من الـ <span class="lt g">CVs</span>', 180, 300, 720, -2, 41, 104)}
        <div id="e-q" class="layer">
          {note("e-who", "مين قدّم؟", 250, 1180, 580, 2, 42, 110)}
          <div id="strike" style="left:240px; top:1290px; width:600px; transform:rotate(-6deg);"></div>
        </div>
      </section>

      <!-- F · who deserves it -->
      <section id="sF" class="clip layer" data-start="16.3" data-duration="2.5" data-track-index="3">
        <img id="f-mag" class="tool blend" src="assets/img/SK-12_magnifier.png" alt="" style="left:170px; top:330px; width:740px;" />
        <div id="f-q1" class="hl" style="top:1090px; font-size:70px; font-weight:700;">السؤال:</div>
        <div id="f-q2" class="hl" style="top:1190px; font-size:132px; white-space:nowrap;">مين <span class="g">يستاهل؟</span></div>
      </section>

      <!-- G · brand -->
      <section id="sG" class="clip layer" data-start="18.8" data-duration="{END - 18.8:.1f}" data-track-index="3">
        <img id="g-logo" src="assets/brand/logo.png" alt="" style="position:absolute; left:250px; top:1210px; width:580px;" />
        <div id="g-tag" class="hl" style="top:1350px; font-size:48px; font-weight:700; line-height:1.4;">نحن نكشف الإشارات.<br><span class="g" style="font-weight:800;">وأنتم تكتشفون المواهب.</span></div>
        <div id="g-next" class="hl" style="top:1560px; font-size:36px; font-weight:700; opacity:0.75;"><span class="lt">D‑29</span> · الحلقة الجاية: وظيفة في دقيقة</div>
      </section>

      <!-- page tears (track 4) -->
{tears}

      <!-- countdown stamp (track 5) -->
      <div id="stampw" class="clip" data-start="0.3" data-duration="18.5" data-track-index="5" style="position:absolute; inset:0;">
        <div id="stamp"><div><b>D‑30</b><small>للافتتاح</small></div></div>
      </div>

      <!-- captions (track 6) -->
{caps}

      <audio id="vo" src="assets/audio/ST01.wav" data-start="{VO}" data-duration="18.24" data-track-index="10" data-volume="1"></audio>
{sfx}
    </div>

    <script>
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});

      // stamp slams
      tl.fromTo("#stamp", {{ scale: 2.4, opacity: 0, rotation: -24 }}, {{ scale: 1, opacity: 1, rotation: -12, duration: 0.22, ease: "power4.in" }}, 0.3);
      tl.to("#stamp", {{ scale: 1.06, duration: 0.08, yoyo: true, repeat: 1 }}, 0.52);

      // page tears: right → left
      document.querySelectorAll(".tear").forEach((el) => {{
        tl.fromTo(el, {{ x: 1080 }}, {{ x: -1520, duration: 0.62, ease: "none" }}, +el.dataset.start);
      }});

      // A
      tl.fromTo("#a-hl", {{ y: 60, scale: 0.85, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.7)" }}, 0.55);
      tl.to("#a-hl", {{ scale: 1.04, duration: 2.0, ease: "none" }}, 1.05);

      // B
      tl.fromTo("#b-lbl", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "power3.out" }}, 3.2);
      tl.fromTo("#b-res", {{ clipPath: "inset(0 0 0 100%)" }}, {{ clipPath: "inset(0 0 0 0%)", duration: 1.3, ease: "power2.inOut" }}, 3.15);
      tl.fromTo("#b-tix", {{ y: 120, rotation: -9, opacity: 0 }}, {{ y: 0, rotation: -3, opacity: 1, duration: 0.45, ease: "back.out(1.6)" }}, 4.45);
      tl.fromTo("#b-num", {{ scale: 0.7, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.35, ease: "back.out(2)" }}, 4.75);
      const cnt = {{ v: 0 }};
      tl.to(cnt, {{ v: 214, duration: 0.9, ease: "power2.out", onUpdate: () => {{ document.getElementById("b-cnt").textContent = Math.round(cnt.v); }} }}, 4.85);
      tl.to("#b-num", {{ scale: 1.08, duration: 0.12, yoyo: true, repeat: 1, ease: "power2.out" }}, 5.75);

      // C — each field lands on its word
      [["#c-t1", "#c-n1", {W_CHEF}], ["#c-t2", "#c-n2", {W_NURSE}], ["#c-t3", "#c-n3", {W_ENG}], ["#c-t4", "#c-n4", {W_ACC}]].forEach(([t, n, at]) => {{
        tl.fromTo(t, {{ scale: 0.6, opacity: 0, y: 40 }}, {{ scale: 1, opacity: 1, y: 0, duration: 0.38, ease: "back.out(2)" }}, at - 0.08);
        tl.fromTo(n, {{ scale: 0.5, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.3, ease: "back.out(2.4)" }}, at + 0.04);
      }});
      tl.to("#c-grid", {{ scale: 0.74, y: 40, duration: 0.5, ease: "power3.inOut", transformOrigin: "50% 45%" }}, {W_ALL} - 0.1);
      document.querySelectorAll("#c-fields .tool").forEach((el, i) => {{
        tl.fromTo(el, {{ scale: 0.4, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.34, ease: "back.out(2.2)" }}, {W_ALL} + 0.05 + i * 0.07);
      }});
      tl.fromTo("#c-all", {{ y: 50, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.4, ease: "back.out(1.8)" }}, {W_ALL});

      // D
      tl.fromTo("#d-tag", {{ x: 160, rotation: 6, opacity: 0 }}, {{ x: 0, rotation: -3, opacity: 1, duration: 0.42, ease: "back.out(1.6)" }}, 11.05);
      tl.fromTo("#d-tape", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 0.9, scale: 1, duration: 0.2 }}, 11.35);

      // E
      tl.fromTo("#e-hl", {{ y: -60, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.42, ease: "back.out(1.7)" }}, 12.7);
      tl.fromTo("#e-who", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.36, ease: "back.out(2)" }}, 14.45);
      tl.fromTo("#strike", {{ scaleX: 0 }}, {{ scaleX: 1, duration: 0.28, ease: "power3.out" }}, 15.55);
      tl.to("#e-who", {{ opacity: 0.55, duration: 0.3 }}, 15.7);

      // F
      tl.fromTo("#f-mag", {{ scale: 0.8, opacity: 0, rotation: -8 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.6, ease: "back.out(1.5)" }}, 16.3);
      tl.to("#f-mag", {{ x: -30, y: 20, duration: 2.0, ease: "sine.inOut" }}, 16.9);
      tl.fromTo("#f-q1", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }}, 16.55);
      tl.fromTo("#f-q2", {{ scale: 0.6, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.4, ease: "back.out(2.2)" }}, 17.5);

      // G
      tl.fromTo("#g-logo", {{ y: 40, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 20.0);
      tl.fromTo("#g-tag", {{ y: 30, opacity: 0 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power3.out" }}, 20.3);
      tl.fromTo("#g-next", {{ opacity: 0 }}, {{ opacity: 0.75, duration: 0.5 }}, 20.8);

      // captions ease in
      document.querySelectorAll(".cap").forEach((el) => {{
        tl.fromTo(el.querySelector("p"), {{ y: 18, scale: 0.96, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.24, ease: "back.out(1.8)" }}, +el.dataset.start);
      }});

      document.querySelectorAll(".note, .tool, .hl, .tape, #stamp, #strike, .tear, #loopbox, #g-logo").forEach((el) => el.setAttribute("data-layout-allow-overlap", ""));
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""
open("index.html", "w").write(html)
print("index.html written", len(html))
