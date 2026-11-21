"""Animated experiment diagrams for long video 2026-11-21 ("Why Your Brain Forgets Things On Purpose").
Pillow frames -> ffmpeg mp4 (1920x1080, 30 fps). Numbers come from memory/facts.md only.
Usage: python tools/diagrams_2026_11_21.py <outdir>"""
import os, subprocess, sys, math
from PIL import Image, ImageDraw, ImageFont

W, H, FPS, DUR, ANIM = 1920, 1080, 30, 20.0, 2.4
BG, Y, WHITE, GREY, RED, BLUE, LBLUE = (17, 17, 20), (255, 230, 0), (240, 240, 240), (120, 120, 128), (240, 80, 70), (70, 140, 230), (150, 200, 245)
FB = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
FR = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
def F(sz, b=True): return ImageFont.truetype(FB if b else FR, sz)
SAFE_BOTTOM = 860  # keep clear of the burned-in subtitles

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3

def frame_base(title, source):
    im = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(im)
    d.text((W // 2, 90), title, font=F(58), fill=WHITE, anchor="mm")
    d.text((W - 60, 40), source, font=F(26, False), fill=GREY, anchor="ra")
    return im, d

def ctext(d, xy, s, sz=40, fill=WHITE, b=True): d.text(xy, s, font=F(sz, b), fill=fill, anchor="mm")

def bars(d, p, items, x0, y0, bw, gap, maxv, hmax, unit=""):
    """vertical bars: items = [(label, value, color, valuelabel)]"""
    for i, (lab, v, col, vl) in enumerate(items):
        x = x0 + i * (bw + gap); hh = hmax * v / maxv * ease(p - i * 0.15)
        d.rectangle((x, y0 - hh, x + bw, y0), fill=col)
        ctext(d, (x + bw / 2, y0 + 45), lab, 38)
        if p - i * 0.15 > 0.6: ctext(d, (x + bw / 2, y0 - hh - 40), vl, 46, Y)

def person(d, x, y, col=WHITE, s=1.0):
    d.ellipse((x - 16 * s, y - 70 * s, x + 16 * s, y - 38 * s), fill=col)
    d.rounded_rectangle((x - 20 * s, y - 34 * s, x + 20 * s, y + 20 * s), 10, fill=col)

def D1(p, d):  # doorway setup
    for k, (ox, lab, door) in enumerate([(200, "One big room", False), (1010, "Through a door", True)]):
        d.rectangle((ox, 220, ox + 710, 700), outline=WHITE, width=6)
        if door:
            d.line((ox + 355, 220, ox + 355, 390), fill=WHITE, width=6); d.line((ox + 355, 530, ox + 355, 700), fill=WHITE, width=6)
            d.rectangle((ox + 345, 392, ox + 365, 528), fill=Y)
        d.rectangle((ox + 60, 420, ox + 160, 500), fill=GREY); d.rectangle((ox + 550, 420, ox + 650, 500), fill=GREY)
        q = ease(p * 1.2 - k * 0.15); x = ox + 110 + (440 * q)
        d.line((ox + 110, 560, x, 560), fill=Y, width=8)
        person(d, x, 470, Y if q > 0.98 else WHITE, 0.9)
        ctext(d, (ox + 355, 760), lab, 44)
    if p > 0.8: ctext(d, (W // 2, 830), "Same walking distance", 40, Y)

def D2(p, d):  # doorway result
    D1(1.0, d)
    if p > 0.2:
        a = ease((p - 0.2) * 2)
        d.rounded_rectangle((1110, 590, 1820, 680), 20, fill=tuple(int(c * a + b * (1 - a)) for c, b in zip(RED, BG)))
        ctext(d, (1465, 635), "Forgot more", 52, WHITE)

def D3(p, d):  # more rooms, more forgetting
    n = 4
    for i in range(n):
        x = 180 + i * 410; q = ease(p * 1.6 - i * 0.25)
        if q <= 0: continue
        d.rectangle((x, 300, x + 330, 620), outline=WHITE, width=6)
        d.rectangle((x + 320, 400, x + 340, 520), fill=Y)
        alpha = 1 - i * 0.27
        col = tuple(int(c * alpha + b * (1 - alpha)) for c, b in zip(Y, BG))
        d.ellipse((x + 115, 380, x + 215, 480), fill=col)
        ctext(d, (x + 165, 430), "?", 60, BG)
        ctext(d, (x + 165, 680), f"Room {i + 1}", 38)
    if p > 0.75: ctext(d, (W // 2, 800), "Each new room: a little more forgetting", 42, Y)

def D4(p, d, stage):  # next-in-line
    seats = 7; cx = W // 2
    d.rounded_rectangle((cx - 620, 470, cx + 620, 590), 30, outline=GREY, width=5)
    for i in range(seats):
        x = cx - 540 + i * 180; q = ease(p * 1.5 - i * 0.06)
        col = WHITE
        if i == 3: col = Y
        if stage == 2 and i in (2, 4) and p > 0.3: col = RED
        if q > 0: person(d, x, 420, col, 1.2)
        if i == 3: ctext(d, (x, 640), "YOU", 40, Y)
    if p > 0.5: ctext(d, (cx, 230), "Your own words: about 9 in 10 remembered", 44, Y)
    if stage == 2 and p > 0.4:
        ctext(d, (cx - 180, 700), "just before", 34, RED); ctext(d, (cx + 180, 700), "just after", 34, RED)
        ctext(d, (cx, 790), "Remembered worst of all", 46, RED)

def D5(p, d, stage):  # forgetting curve (savings: effort needed to relearn)
    x0, y0, x1, y1 = 330, 770, 1650, 230
    d.line((x0, y0, x1, y0), fill=WHITE, width=5); d.line((x0, y0, x0, y1), fill=WHITE, width=5)
    d.text((x0 - 20, y1 - 30), "Effort to learn it again", font=F(34), fill=WHITE, anchor="ls")
    for v, lab in [(0, "0"), (50, "half"), (100, "all")]:
        yy = y0 - (y0 - y1) * v / 100; d.text((x0 - 20, yy), lab, font=F(30, False), fill=GREY, anchor="rm")
    pts = [("20 min", 53, "about half"), ("1 day", 68, "about 2/3"), ("1 month", 96, "almost all")]
    xs = [x0 + 260, x0 + 680, x0 + 1150]
    shown = 1 if stage == 1 else 3
    prev = (x0, y0 - (y0 - y1) * 0.0)
    for i in range(shown):
        q = ease(p * 1.6 - i * 0.35)
        if q <= 0: break
        lab, v, vl = pts[i]; X, Yv = xs[i], y0 - (y0 - y1) * v / 100
        ex = prev[0] + (X - prev[0]) * q; ey = prev[1] + (Yv - prev[1]) * q
        d.line((prev[0], prev[1], ex, ey), fill=Y, width=7)
        if q > 0.95:
            d.ellipse((X - 14, Yv - 14, X + 14, Yv + 14), fill=Y)
            ctext(d, (X, Yv - 50), vl, 38, Y)
        ctext(d, (X, y0 + 45), lab, 36)
        prev = (X, Yv)

def D6(p, d, stage):  # cold water trials
    x0, scale = 330, 14  # px per second
    rows = [("Trial A", [(60, BLUE, "60 s cold")]), ("Trial B", [(60, BLUE, "60 s cold"), (30, LBLUE, "+30 s, a bit warmer")])]
    for r, (lab, parts) in enumerate(rows[:stage]):
        y = 330 + r * 230; ctext(d, (200, y + 45), lab, 42)
        x = x0; q = ease(p * 1.4)
        for sec, col, t in parts:
            w = sec * scale * q
            d.rectangle((x, y, x + w, y + 90), fill=col)
            if q > 0.9: ctext(d, (x + sec * scale / 2, y + 140), t, 32)
            x += sec * scale
    if stage == 2 and p > 0.7: ctext(d, (W // 2, 820), "Trial B = more pain in total", 40, Y)

def D7(p, d):  # 69% chose the longer trial
    ctext(d, (W // 2, 230), "Which one would you do again?", 48)
    cx, cy, r = W // 2, 520, 220
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(50, 50, 56))
    a = 360 * 0.69 * ease(p * 1.3)
    d.pieslice((cx - r, cy - r, cx + r, cy + r), -90, -90 + a, fill=Y)
    d.ellipse((cx - 130, cy - 130, cx + 130, cy + 130), fill=BG)
    if p > 0.5: ctext(d, (cx, cy - 10), "69%", 80, Y); ctext(d, (cx, cy + 60), "chose B", 34)
    if p > 0.7: ctext(d, (cx, 820), "the LONGER one", 44, Y)

def D8(p, d):  # speed estimates by verb
    ctext(d, (W // 2, 200), "About how fast were the cars going when they ___ each other?", 40)
    items = [("smashed", 40.8), ("hit", 34.0), ("contacted", 31.8)]
    for i, (w, v) in enumerate(items):
        y = 330 + i * 160; q = ease(p * 1.5 - i * 0.15)
        ctext(d, (330, y + 45), w, 46, Y if i == 0 else WHITE)
        d.rectangle((520, y, 520 + 26 * v * q, y + 90), fill=Y if i == 0 else GREY)
        if q > 0.9: d.text((540 + 26 * v, y + 45), f"{v:.1f} mph", font=F(44), fill=WHITE, anchor="lm")

def D9(p, d):  # broken glass
    ctext(d, (W // 2, 200), "A week later: \"Did you see broken glass?\"", 46)
    ctext(d, (W // 2, 270), "(there was none)", 36, GREY, False)
    bars(d, p, [("heard \"hit\"", 14, GREY, "14% yes"), ("heard \"smashed\"", 32, RED, "32% yes")], 610, 760, 260, 180, 40, 380)

def D10(p, d):  # retrieval practice
    ctext(d, (W // 2, 190), "How much they remembered", 48)
    grp = [("after 5 minutes", [("reread", 83, GREY), ("tested", 71, Y)]), ("after 1 week", [("reread", 40, GREY), ("tested", 61, Y)])]
    for g, (lab, its) in enumerate(grp):
        x0 = 380 + g * 700
        for i, (l, v, col) in enumerate(its):
            q = ease(p * 1.5 - g * 0.35 - i * 0.1); x = x0 + i * 220; hh = 4.8 * v * q
            d.rectangle((x, 770 - hh, x + 170, 770), fill=col)
            ctext(d, (x + 85, 805), l, 34)
            if q > 0.9: ctext(d, (x + 85, 770 - hh - 35), f"{v}%", 42, Y if col == Y else WHITE)
        ctext(d, (x0 + 195, 270), lab, 40, Y if g == 1 else WHITE)

def D11(p, d):  # the day cut into scenes
    scenes = [("Bedroom", "I need my keys"), ("Hallway", ""), ("Kitchen", "?")]
    x0, w, y = 160, 520, 360
    for i, (lab, note) in enumerate(scenes):
        q = ease(p * 1.6 - i * 0.3)
        if q <= 0: continue
        x = x0 + i * (w + 20)
        col = tuple(int(c * q + b * (1 - q)) for c, b in zip((60, 60, 68), BG))
        d.rounded_rectangle((x, y, x + w, y + 260), 18, fill=col)
        ctext(d, (x + w / 2, y + 70), lab, 52, WHITE)
        if note: ctext(d, (x + w / 2, y + 170), note, 38, Y if note != "?" else RED)
        if i > 0: d.line((x - 10, y - 30, x - 10, y + 290), fill=Y, width=8)
    if p > 0.8: ctext(d, (W // 2, 780), "Each doorway = a cut between scenes", 42, Y)

def D12(p, d):  # seen once fades, seen again stays
    ctext(d, (W // 2, 210), "What your brain keeps", 48)
    for i, (lab, keep) in enumerate([("seen once", False), ("seen once", False), ("comes back again and again", True), ("seen once", False)]):
        y = 320 + i * 120
        a = 1.0 if keep else max(0.15, 1 - ease(p * 1.4))
        col = tuple(int(c * a + b * (1 - a)) for c, b in zip(Y if keep else WHITE, BG))
        d.rounded_rectangle((440, y, 1480, y + 90), 16, outline=col, width=5)
        ctext(d, (960, y + 45), lab + ("  ✓ kept" if keep and p > 0.6 else ""), 40, col)

def D13(p, d):  # remembering = rebuilding
    parts = [("bits you kept", 420), ("what you know", 960), ("what someone just said", 1500)]
    for i, (lab, x) in enumerate(parts):
        q = ease(p * 1.6 - i * 0.2)
        if q <= 0: continue
        d.rounded_rectangle((x - 255, 260, x + 255, 380), 18, fill=(60, 60, 68))
        ctext(d, (x, 320), lab, 34, WHITE)
        ex, ey = x + (960 - x) * ease(p * 1.3 - 0.4), 380 + 220 * ease(p * 1.3 - 0.4)
        d.line((x, 380, ex, ey), fill=Y, width=6)
    if p > 0.75:
        d.rounded_rectangle((660, 620, 1260, 740), 20, fill=Y)
        ctext(d, (960, 680), "the memory, rebuilt", 46, BG)

def D14(p, d):  # keep the pattern, drop the noise
    import random
    rnd = random.Random(7)
    pts = [(300 + i * 60, 780 - i * 14 + rnd.randint(-90, 90)) for i in range(23)]
    a = 1 - 0.85 * ease(p * 1.5 - 0.3)
    for x, y in pts:
        col = tuple(int(c * a + b * (1 - a)) for c, b in zip(WHITE, BG))
        d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=col)
    q = ease(p * 1.5 - 0.2)
    d.line((300, 780, 300 + (1320 * q), 780 - (308 * q)), fill=Y, width=10)
    if p > 0.8:
        ctext(d, (W // 2, 250), "Keep the pattern. Drop the noise.", 50, Y)

SPECS = {
    "d01_doorway_setup": ("The doorway test", "Radvansky et al. (2011)", D1),
    "d02_doorway_result": ("The doorway test", "Radvansky et al. (2011)", D2),
    "d03_rooms": ("More rooms, more forgetting", "Radvansky et al. (2011)", D3),
    "d04_nextinline_a": ("Taking turns reading words", "Brenner (1973)", lambda p, d: D4(p, d, 1)),
    "d05_nextinline_b": ("Taking turns reading words", "Brenner (1973)", lambda p, d: D4(p, d, 2)),
    "d06_curve_a": ("The forgetting curve", "Murre & Dros (2015)", lambda p, d: D5(p, d, 1)),
    "d07_curve_b": ("The forgetting curve", "Murre & Dros (2015)", lambda p, d: D5(p, d, 2)),
    "d08_cold_a": ("The cold-water test", "Kahneman et al. (1993)", lambda p, d: D6(p, d, 1)),
    "d09_cold_b": ("The cold-water test", "Kahneman et al. (1993)", lambda p, d: D6(p, d, 2)),
    "d10_cold_result": ("The cold-water test", "Kahneman et al. (1993)", D7),
    "d11_speed": ("One word changed the memory", "Loftus & Palmer (1974)", D8),
    "d12_glass": ("Glass that never existed", "Loftus & Palmer (1974)", D9),
    "d13_retrieval": ("Rereading vs testing yourself", "Roediger & Karpicke (2006)", D10),
    "d14_scenes": ("Your day, cut into scenes", "Radvansky et al. (2011)", D11),
    "d15_keep": ("Your brain waits for proof", "Murre & Dros (2015)", D12),
    "d16_rebuild": ("Remembering = rebuilding", "Loftus & Palmer (1974)", D13),
    "d17_pattern": ("Why your brain lets go", "Richards & Frankland (2017)", D14),
}

def render(name, outdir):
    title, src, fn = SPECS[name]
    out = os.path.join(outdir, name + ".mp4")
    n_anim = int(ANIM * FPS)
    tmp = os.path.join(outdir, "_frames"); os.makedirs(tmp, exist_ok=True)
    for i in range(n_anim + 1):
        im, d = frame_base(title, src); fn(i / n_anim, d); im.save(f"{tmp}/{i:04d}.png")
    # animate, then hold the last frame for the rest of DUR
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", str(FPS), "-i", f"{tmp}/%04d.png",
                    "-vf", f"tpad=stop_mode=clone:stop_duration={DUR - ANIM:.2f},format=yuv420p",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(FPS), out], check=True)
    for f in os.listdir(tmp): os.remove(os.path.join(tmp, f))
    os.rmdir(tmp)
    return out

if __name__ == "__main__":
    od = sys.argv[1]; os.makedirs(od, exist_ok=True)
    for k in (sys.argv[2:] or SPECS): print(render(k, od))
