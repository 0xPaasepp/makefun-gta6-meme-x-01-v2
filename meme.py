#!/usr/bin/env python3
"""LEONIDA EXPRESS — GTA VI delivery tracker meme (1080x1080).

Deterministic Pillow build: no randomness, no network, no clock.
Run: python3 meme.py  ->  writes meme.png next to this file.
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "meme.png")
GHOST = os.path.join(HERE, "assets", "mark-1024.png")

W = H = 1080
PAPER = "#EDE8DF"
NAVY = "#1F2A44"
GRAY = "#6B6B6B"
DARK = "#3A3A3A"
ORANGE = "#FF7A1A"
GREEN = "#1E9E5A"
PINK = "#FFF0F5"
TRACK = "#E3E0D8"

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


F_TITLE = lambda s: font("LiberationSans-Bold.ttf", s)        # noqa: E731
F_REG = lambda s: font("LiberationSans-Regular.ttf", s)       # noqa: E731
F_MONO = lambda s: font("LiberationMono-Regular.ttf", s)      # noqa: E731
F_MONO_B = lambda s: font("LiberationMono-Bold.ttf", s)       # noqa: E731


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns list of lines."""
    lines, cur = [], ""
    for word in text.split(" "):
        trial = word if not cur else cur + " " + word
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def dashed_rect(draw, box, dash=10, gap=7, fill=GRAY, width=2):
    x0, y0, x1, y1 = box
    # top / bottom
    x = x0
    while x < x1:
        draw.line([(x, y0), (min(x + dash, x1), y0)], fill=fill, width=width)
        draw.line([(x, y1), (min(x + dash, x1), y1)], fill=fill, width=width)
        x += dash + gap
    y = y0
    while y < y1:
        draw.line([(x0, y), (x0, min(y + dash, y1))], fill=fill, width=width)
        draw.line([(x1, y), (x1, min(y + dash, y1))], fill=fill, width=width)
        y += dash + gap


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # --- card ---
    d.rounded_rectangle([36, 36, 1044, 1044], radius=36, fill="white")

    # --- header: package icon + LEONIDA EXPRESS / tracking no. ---
    ix, iy, isize = 100, 88, 52
    d.rounded_rectangle([ix, iy, ix + isize, iy + isize], radius=8,
                        outline=NAVY, width=4)
    d.line([(ix, iy + 16), (ix + isize, iy + 16)], fill=NAVY, width=3)
    d.line([(ix + isize // 2, iy), (ix + isize // 2, iy + isize)],
           fill=NAVY, width=3)
    d.text((164, 92), "LEONIDA EXPRESS", font=F_TITLE(44), fill=NAVY)
    d.text((980, 100), "GTA-VI-13-YEARS", font=F_MONO(24), fill=GRAY,
           anchor="ra")

    # --- status pill ---
    pill_text = "DELIVERED \u2014 13 YEARS LATE"
    pf = F_TITLE(36)
    tw = d.textlength(pill_text, font=pf)
    pw, ph, py = int(tw) + 64, 60, 152
    px0 = (W - pw) // 2
    d.rounded_rectangle([px0, py, px0 + pw, py + ph], radius=ph // 2,
                        fill=GREEN)
    d.text((W // 2, py + ph // 2), pill_text, font=pf, fill="white",
           anchor="mm")

    # --- order + sub line ---
    d.text((100, 232), "GTA VI \u2014 1 GAME \u2022 214 GB",
           font=F_TITLE(34), fill=NAVY)
    d.text((100, 274), "Estimated delivery: May 26, 2026 (allegedly)",
           font=F_REG(26), fill=GRAY)

    # --- progress bar ---
    d.rounded_rectangle([100, 322, 980, 336], radius=7, fill=TRACK)
    d.rounded_rectangle([100, 322, 100 + int(880 * 0.99), 336], radius=7,
                        fill=ORANGE)
    d.text((100, 346), "99% \u2014 the last 1% took 13 years.",
           font=F_REG(26), fill=DARK)
    d.text((100, 378), "SIZE: 214 GB \u2022 FRAGILE: YES, EMOTIONALLY",
           font=F_MONO(24), fill=GRAY)

    # --- timeline ---
    events = [
        ("SEP 17, 2013", "Order placed",
         "You bought GTA V and pre-ordered VI in your head. "
         "Status: still processing."),
        ("DEC 5, 2023", "Trailer 1 delivered",
         "You memorized every frame. The game stayed in the warehouse."),
        ("2025", "Delayed again",
         "Your package is now old enough to play the game inside it."),
        ("MAY 26, 2026", "Out for delivery",
         "214 GB. Your internet provider has blocked your number."),
        ("TODAY", "Delivered",
         "Not by the courier \u2014 by your AI agent. It earned $250 on "
         "make.fun while you waited for the install."),
    ]
    f_date = F_MONO_B(24)
    f_title = F_TITLE(30)
    f_joke = F_REG(27)
    title_h, joke_lh, gap = 36, 31, 10
    y0 = 420
    # Measure event heights first (final event joke width is narrower:
    # ghost occupies the right side of its row).
    heights = []
    wrapped = []
    for i, (_date, _title, joke) in enumerate(events):
        max_w = 700 if i == 4 else 860
        lines = wrap(d, joke, f_joke, max_w)
        wrapped.append(lines)
        heights.append(title_h + joke_lh * len(lines) + gap)
    total = sum(heights)
    # Vertical line spans first dot centre to last dot centre.
    line_top = y0 + 8
    line_bot = y0 + total - gap - heights[-1] + 8
    # Pink rect behind the final event (drawn before line/dots/text).
    final_y = y0 + sum(heights[:-1])
    d.rounded_rectangle([92, final_y - 12, 988,
                         final_y + heights[-1] - gap + 6],
                        radius=18, fill=PINK)
    d.line([(110, line_top), (110, line_bot)], fill="#D8D2C4", width=3)

    y = y0
    for i, (date, title, _joke) in enumerate(events):
        cy = y + 8  # dot centre
        dot_fill = "#FF5DA2" if i == 4 else ORANGE
        d.ellipse([110 - 8, cy - 8, 110 + 8, cy + 8], fill=dot_fill)
        # date + title on one line
        d.text((150, y), date, font=f_date, fill=ORANGE)
        dw = d.textlength(date, font=f_date)
        d.text((150 + dw + 14, y - 3), title, font=f_title, fill=NAVY)
        jy = y + title_h
        for line in wrapped[i]:
            d.text((150, jy), line, font=f_joke, fill=DARK)
            jy += joke_lh
        y += heights[i]

    # Ghost, right side of the final row, 84px.
    ghost = Image.open(GHOST).convert("RGBA").resize((84, 84),
                                                     Image.LANCZOS)
    gy = final_y + (heights[-1] - gap - 84) // 2
    img.paste(ghost, (896, gy), ghost)

    # --- delivery notes box ---
    notes = ("DELIVERY NOTES: Leave with the neighbour. Tell work I'm "
             "sick. Tell my girlfriend it's a work trip.")
    nf = F_MONO(24)
    nlines = wrap(d, notes, nf, 848)
    assert len(nlines) <= 2, nlines
    ny = y + 14
    nh = 14 + 30 * len(nlines) + 14
    dashed_rect(d, [100, ny, 980, ny + nh])
    ty = ny + 14
    for line in nlines:
        d.text((116, ty), line, font=nf, fill=DARK)
        ty += 30

    # --- footer ---
    d.text((540, 1012), "make.fun", font=F_TITLE(44), fill=NAVY,
           anchor="mb")

    img.save(OUT, "PNG")
    print("wrote", OUT, img.size,
          "| timeline", y0, "->", y, "| notes", ny, "->", ny + nh)


if __name__ == "__main__":
    main()
