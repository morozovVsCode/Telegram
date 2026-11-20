import json, re, os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 800
OUT = "images"
os.makedirs(OUT, exist_ok=True)
FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

PALETTES = [
    ("#F3EBDD", "#C98A5B", "#3B2F2A", "#E8CDB0"),
    ("#E6EEF0", "#4F8A99", "#1F3A42", "#B8D4DB"),
    ("#EEE9F3", "#8A6FB0", "#33284A", "#D3C6E6"),
    ("#E9F0E4", "#6E9B5E", "#27391F", "#C5DDBB"),
    ("#F6E9E6", "#D0705F", "#4A2620", "#F0C4BB"),
    ("#EDEDED", "#5D6B7A", "#222A33", "#C9D1D9"),
    ("#F7F0D9", "#D1A52C", "#3F3410", "#EFDB9A"),
    ("#E3F0EE", "#2F9C8D", "#173F3A", "#A9DDD5"),
    ("#F3E6EE", "#B5588A", "#44213A", "#E6B9D3"),
    ("#E8EBF5", "#4F63B5", "#1C2548", "#BAC4EA"),
    ("#F1EAE2", "#8C6A4F", "#33261D", "#D9C4B1"),
    ("#E4EFE9", "#3E8A66", "#173629", "#B3D8C5"),
]
WHITE = "#FFFFFF"


def rr(d, box, r, fill, outline=None, w=0):
    d.rounded_rectangle(box, r, fill=fill, outline=outline, width=w)


def sofa(d, c):
    bg, ac, dk, lt = c
    rr(d, (330, 200, 950, 330), 40, ac)
    rr(d, (300, 290, 980, 400), 30, ac)
    rr(d, (260, 250, 350, 410), 30, dk)
    rr(d, (930, 250, 1020, 410), 30, dk)
    rr(d, (370, 300, 630, 385), 22, lt)
    rr(d, (650, 300, 910, 385), 22, lt)
    for x in (300, 940):
        d.rectangle((x, 410, x + 30, 440), fill=dk)
    rr(d, (480, 450, 800, 480), 10, dk)
    d.rectangle((510, 480, 525, 520), fill=dk)
    d.rectangle((755, 480, 770, 520), fill=dk)
    d.ellipse((1060, 140, 1130, 210), fill="#F9D86A")
    d.rectangle((1092, 210, 1098, 440), fill=dk)
    d.ellipse((1060, 435, 1130, 455), fill=dk)


def bed(d, c):
    bg, ac, dk, lt = c
    rr(d, (300, 150, 980, 330), 24, dk)
    rr(d, (300, 300, 980, 440), 24, lt)
    rr(d, (300, 340, 980, 440), 24, ac)
    rr(d, (340, 270, 560, 340), 30, WHITE)
    rr(d, (600, 270, 820, 340), 30, WHITE)
    d.rectangle((310, 440, 340, 490), fill=dk)
    d.rectangle((940, 440, 970, 490), fill=dk)
    rr(d, (1010, 330, 1130, 490), 12, ac)
    d.rectangle((1020, 400, 1120, 405), fill=dk)
    d.polygon([(1040, 330), (1100, 330), (1085, 270), (1055, 270)], fill="#F9D86A")
    d.rectangle((1067, 330, 1073, 335), fill=dk)
    d.ellipse((120, 110, 230, 220), fill="#F4F1E8")
    d.ellipse((150, 100, 250, 200), fill=c[0])


def kitchen(d, c):
    bg, ac, dk, lt = c
    pts = [(640, 90), (330, 440), (950, 440)]
    d.line(pts + [pts[0]], fill=dk, width=8, joint="curve")
    for (x, y), name in zip(pts, ("fridge", "sink", "stove")):
        d.ellipse((x - 85, y - 85, x + 85, y + 85), fill=WHITE, outline=ac, width=8)
        if name == "fridge":
            rr(d, (x - 28, y - 55, x + 28, y + 55), 8, lt, dk, 4)
            d.line((x - 28, y - 10, x + 28, y - 10), fill=dk, width=4)
            d.line((x + 14, y - 30, x + 14, y - 20), fill=dk, width=4)
            d.line((x + 14, y, x + 14, y + 20), fill=dk, width=4)
        elif name == "sink":
            rr(d, (x - 50, y - 5, x + 50, y + 40), 10, lt, dk, 4)
            d.arc((x - 25, y - 50, x + 25, y), 180, 360, fill=dk, width=6)
            d.line((x + 25, y - 25, x + 25, y - 5), fill=dk, width=6)
        else:
            rr(d, (x - 50, y - 45, x + 50, y + 45), 10, lt, dk, 4)
            for dx, dy in ((-20, -18), (20, -18), (-20, 18), (20, 18)):
                d.ellipse((x + dx - 12, y + dy - 12, x + dx + 12, y + dy + 12), fill=dk)


def bathroom(d, c):
    bg, ac, dk, lt = c
    for i in range(7):
        for j in range(4):
            rr(d, (190 + i * 130, 60 + j * 120, 190 + i * 130 + 118, 60 + j * 120 + 108), 10, lt)
    cx, cy = 640, 300
    d.polygon([(cx, cy - 190), (cx - 120, cy + 20), (cx + 120, cy + 20)], fill=ac)
    d.ellipse((cx - 120, cy - 70, cx + 120, cy + 170), fill=ac)
    d.ellipse((cx - 70, cy - 10, cx - 30, cy + 40), fill=WHITE)
    for x, y, r in ((300, 450, 16), (330, 480, 10), (980, 440, 18), (950, 480, 9)):
        d.ellipse((x - r, y - r, x + r, y + r), fill=dk)


def hallway(d, c):
    bg, ac, dk, lt = c
    rr(d, (250, 60, 520, 470), 14, ac)
    rr(d, (280, 90, 490, 260), 10, lt)
    rr(d, (280, 290, 490, 440), 10, lt)
    d.ellipse((470, 270, 490, 290), fill=dk)
    rr(d, (600, 150, 1080, 175), 8, dk)
    for x in (650, 760, 870, 980):
        d.line((x, 175, x, 200), fill=dk, width=6)
        d.ellipse((x - 9, 198, x + 9, 216), fill=dk)
    d.polygon([(700, 200), (780, 200), (800, 360), (680, 360)], fill=lt)
    d.polygon([(900, 200), (960, 200), (980, 330), (880, 330)], fill=ac)
    rr(d, (600, 400, 1080, 440), 10, dk)
    d.rectangle((630, 440, 650, 500), fill=dk)
    d.rectangle((1030, 440, 1050, 500), fill=dk)
    for x in (680, 780):
        rr(d, (x, 365, x + 80, 400), 14, ac)


def lighting(d, c):
    bg, ac, dk, lt = c
    d.line((640, 40, 640, 140), fill=dk, width=6)
    d.polygon([(560, 220), (720, 220), (690, 140), (590, 140)], fill=ac)
    d.polygon([(560, 225), (720, 225), (900, 500), (380, 500)], fill="#FBE9A8")
    d.polygon([(560, 220), (720, 220), (690, 140), (590, 140)], fill=ac)
    d.ellipse((620, 205, 660, 245), fill="#FFF6CC")
    for x, col in ((250, "#FBD36B"), (640, "#FFF3C4"), (1030, "#BFE3FF")):
        d.ellipse((x - 45, 400, x + 45, 490), fill=col, outline=dk, width=5)
        rr(d, (x - 25, 485, x + 25, 520), 6, dk)


def palette(d, c):
    bg, ac, dk, lt = c
    for (x, y, col) in ((470, 210, ac), (810, 210, lt), (640, 380, dk)):
        d.ellipse((x - 150, y - 150, x + 150, y + 150), fill=col)
    d.ellipse((640 - 55, 270 - 55, 640 + 55, 270 + 55), fill=WHITE)
    for i, col in enumerate((ac, lt, dk, WHITE, bg)):
        d.ellipse((220, 120 + i * 80, 260, 160 + i * 80), fill=col, outline=dk, width=3)


def wardrobe(d, c):
    bg, ac, dk, lt = c
    rr(d, (330, 60, 950, 500), 14, dk)
    rr(d, (355, 85, 925, 475), 8, lt)
    d.line((640, 85, 640, 475), fill=dk, width=8)
    d.line((375, 150, 620, 150), fill=dk, width=8)
    d.line((660, 150, 905, 150), fill=dk, width=8)
    for x, col in ((410, ac), (470, dk), (530, ac), (580, "#FFFFFF")):
        d.polygon([(x - 25, 156), (x + 25, 156), (x + 30, 330), (x - 30, 330)], fill=col)
    for y in (260, 340, 420):
        d.rectangle((660, y, 905, y + 10), fill=dk)
    for x, y in ((680, 215), (780, 215), (700, 295), (800, 295)):
        rr(d, (x, y, x + 70, y + 40), 6, ac)


def materials(d, c):
    import random
    bg, ac, dk, lt = c
    rr(d, (200, 110, 460, 470), 18, "#B9814F")
    for i in range(10):
        y = 140 + i * 33
        d.arc((190, y - 20, 470, y + 30), 190, 350, fill="#8E5B31", width=4)
    rr(d, (510, 110, 770, 470), 18, "#C9C6C0")
    rnd = random.Random(5)
    for _ in range(140):
        x, y, r = rnd.randint(520, 760), rnd.randint(120, 460), rnd.randint(2, 5)
        d.ellipse((x - r, y - r, x + r, y + r), fill=rnd.choice(["#9E9B95", "#E4E1DB", "#B3B0AA"]))
    rr(d, (820, 110, 1080, 470), 18, "#9AA4AE")
    for i in range(12):
        x = 830 + i * 20
        d.polygon([(x, 120), (x + 10, 120), (x - 60, 460), (x - 70, 460)], fill="#C5CDD5")
    rr(d, (820, 110, 1080, 470), 18, None, dk, 4)
    rr(d, (200, 110, 460, 470), 18, None, dk, 4)
    rr(d, (510, 110, 770, 470), 18, None, dk, 4)


def zoning(d, c):
    bg, ac, dk, lt = c
    rr(d, (240, 60, 1040, 500), 10, WHITE, dk, 8)
    d.line((640, 60, 640, 280), fill=dk, width=6)
    for y in range(290, 500, 22):
        d.line((640, y, 640, y + 10), fill=dk, width=6)
    rr(d, (270, 90, 480, 220), 14, ac)
    rr(d, (285, 100, 340, 140), 12, WHITE)
    rr(d, (700, 100, 1000, 190), 18, lt)
    rr(d, (740, 215, 960, 270), 12, dk)
    d.ellipse((380, 330, 540, 470), fill=lt, outline=dk, width=5)
    for x, y in ((360, 400), (560, 400), (460, 310), (460, 490)):
        d.ellipse((x - 20, y - 20, x + 20, y + 20), fill=ac)
    rr(d, (760, 380, 1000, 470), 12, ac)
    for x in (800, 860, 920):
        d.ellipse((x, 400, x + 35, 435), fill=dk)


def kids(d, c):
    import math
    bg, ac, dk, lt = c
    rr(d, (300, 270, 820, 440), 24, lt)
    rr(d, (300, 220, 340, 460), 14, dk)
    rr(d, (780, 250, 820, 460), 14, dk)
    rr(d, (340, 330, 780, 440), 20, ac)
    rr(d, (360, 280, 500, 340), 28, WHITE)
    for x, y, s in ((960, 120, 55), (1080, 230, 38), (220, 130, 40), (900, 330, 28)):
        pts = []
        for k in range(10):
            r = s if k % 2 == 0 else s * 0.45
            a = -math.pi / 2 + k * math.pi / 5
            pts.append((x + r * math.cos(a), y + r * math.sin(a)))
        d.polygon(pts, fill="#F9D86A")
    for col, x in ((ac, 900), (dk, 980), (lt, 1060)):
        rr(d, (x, 400, x + 70, 470), 8, col, dk, 3)
    rr(d, (940, 330, 1010, 400), 8, lt, dk, 3)


def balcony(d, c):
    bg, ac, dk, lt = c
    rr(d, (220, 60, 1060, 500), 10, lt)
    d.rectangle((220, 330, 1060, 500), fill=ac)
    for x in range(240, 1060, 60):
        d.line((x, 330, x, 500), fill=dk, width=6)
    d.line((220, 330, 1060, 330), fill=dk, width=10)
    d.line((220, 500, 1060, 500), fill=dk, width=10)
    d.ellipse((900, 90, 990, 180), fill="#F9D86A")
    for x in (300, 420, 880):
        rr(d, (x, 250, x + 80, 330), 8, "#C0633B")
        for dx, dy, r in ((10, -30, 28), (40, -55, 32), (65, -25, 26)):
            d.ellipse((x + dx, 250 + dy - r, x + dx + 2 * r, 250 + dy + r), fill="#5E9B52")
    rr(d, (560, 250, 720, 280), 8, dk)
    d.line((580, 280, 560, 330), fill=dk, width=8)
    d.line((700, 280, 720, 330), fill=dk, width=8)
    rr(d, (560, 200, 720, 255), 12, dk)


def office(d, c):
    bg, ac, dk, lt = c
    rr(d, (250, 330, 1030, 370), 10, dk)
    d.rectangle((290, 370, 315, 500), fill=dk)
    d.rectangle((965, 370, 990, 500), fill=dk)
    rr(d, (420, 120, 860, 330), 14, dk)
    rr(d, (440, 140, 840, 310), 8, lt)
    d.line((460, 190, 680, 190), fill=ac, width=10)
    d.line((460, 225, 780, 225), fill=ac, width=10)
    d.line((460, 260, 620, 260), fill=ac, width=10)
    d.rectangle((625, 330, 655, 345), fill=dk)
    d.polygon([(1100, 330), (1060, 150), (1000, 150), (1030, 330)], fill=ac)
    d.line((1070, 150, 1010, 110), fill=dk, width=8)
    d.polygon([(985, 100), (1050, 130), (1020, 160), (960, 125)], fill="#F9D86A")
    rr(d, (520, 372, 760, 400), 10, lt)
    rr(d, (570, 420, 710, 480), 18, ac)
    d.rectangle((635, 480, 645, 520), fill=dk)


def walldecor(d, c):
    bg, ac, dk, lt = c
    frames = [(250, 90, 460, 300, ac), (500, 90, 680, 220, dk), (720, 90, 1030, 260, lt),
              (500, 250, 680, 400, lt), (720, 300, 900, 400, ac), (930, 300, 1030, 400, dk)]
    for x1, y1, x2, y2, col in frames:
        rr(d, (x1, y1, x2, y2), 6, WHITE, dk, 8)
        rr(d, (x1 + 18, y1 + 18, x2 - 18, y2 - 18), 4, col)
        d.ellipse((x1 + 40, y1 + 38, x1 + 80, y1 + 78), fill=WHITE)
    rr(d, (250, 430, 1030, 450), 8, dk)
    for x, h in ((300, 70), (350, 50), (420, 80)):
        rr(d, (x, 430 - h, x + 40, 430), 6, ac)
    d.ellipse((870, 380, 940, 430), fill=lt)


def steps(d, c):
    bg, ac, dk, lt = c
    rows = ((90, 760), (190, 700), (290, 640), (390, 580))
    for i, (y, w) in enumerate(rows):
        rr(d, (250, y, 250 + w + 120, y + 80), 18, WHITE, dk, 4)
        d.ellipse((270, y + 12, 326, y + 68), fill=ac if i < 3 else lt)
        if i < 3:
            d.line((283, y + 40, 295, y + 54), fill=WHITE, width=8)
            d.line((295, y + 54, 316, y + 26), fill=WHITE, width=8)
        else:
            d.text((290, y + 22), "4", fill=dk, font=ImageFont.truetype(FONT, 34))
        d.rounded_rectangle((350, y + 28, 350 + w - 200, y + 52), 10, fill=lt)


ICONS = [sofa, bed, kitchen, bathroom, hallway, lighting, palette, wardrobe,
         materials, zoning, kids, balcony, office, walldecor, steps]


def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def make(i, title, topic, variant):
    c = PALETTES[variant % len(PALETTES)]
    bg, ac, dk, lt = c
    img = Image.new("RGB", (W, H), bg)
    d = ImageDraw.Draw(img)
    d.ellipse((-120, -140, 280, 260), fill=lt)
    d.ellipse((1020, 380, 1420, 780), fill=lt)
    layer = Image.new("RGBA", (W, 560), (0, 0, 0, 0))
    ICONS[topic](ImageDraw.Draw(layer), c)
    if variant % 2 == 1:
        layer = layer.transpose(Image.FLIP_LEFT_RIGHT)
    img.paste(layer, (0, 30), layer)
    d = ImageDraw.Draw(img)
    rr(d, (60, 590, W - 60, 750), 28, WHITE)
    rr(d, (60, 590, 84, 750), 12, ac)
    size = 52
    while True:
        font = ImageFont.truetype(FONT, size)
        lines = wrap(d, title, font, W - 200)
        if len(lines) <= 2 or size <= 36:
            break
        size -= 2
    lh = size + 10
    y0 = 590 + (160 - lh * len(lines)) // 2 + 2
    for k, line in enumerate(lines):
        d.text((110, y0 + k * lh), line, font=font, fill=dk)
    img.save(f"{OUT}/post_{i:03d}.jpg", quality=88)


posts = json.load(open("posts.json", encoding="utf-8"))
base_titles = [re.match(r"<b>(.*?)</b>", p["text"]).group(1) for p in posts[:15]]
for i in range(1, len(posts) + 1):
    topic, variant = (i - 1) % 15, (i - 1) // 15
    make(i, base_titles[topic], topic, variant)
print("done", len(os.listdir(OUT)))
