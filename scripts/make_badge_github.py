#!/usr/bin/env python3
"""Genera badge 'Powned by Motoko' estilo shields.io en WebP.

Uso:
    python3 make_badge_github.py [label] [score] [salida.webp]
Defaults: label="Powned by Motoko", score="10/10", salida=badge-motoko.webp
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont

left_txt = sys.argv[1] if len(sys.argv) > 1 else "Powned by Motoko"
right_txt = sys.argv[2] if len(sys.argv) > 2 else "10/10"
out_path = sys.argv[3] if len(sys.argv) > 3 else "badge-motoko.webp"

def font(size):
    for p in [
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/TTF/DejaVuSans-Bold.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/TTF/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ]:
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                continue
    return ImageFont.load_default()

FS = 26
f = font(FS)
pad_x = 16
h = 42
r = 10

def seg_width(t):
    b = f.getbbox(t)
    return pad_x*2 + (b[2]-b[0])

w_left = seg_width(left_txt)
w_right = seg_width(right_txt)
W = w_left + w_right

img = Image.new("RGBA", (W, h), (0,0,0,0))
d = ImageDraw.Draw(img)
d.rounded_rectangle([0,0,W-1,h-1], radius=r, fill=(255,255,255,255))
d.rounded_rectangle([w_left,0,W-1,h-1], radius=r, fill=(124,58,237,255),
                    corners=(False,True,True,False))

def draw_text(t, color, cx_center):
    dd = ImageDraw.Draw(img)
    b = f.getbbox(t)
    tw = b[2]-b[0]; th = b[3]-b[1]
    x = cx_center - tw/2 - b[0]
    y = (h - th)/2 - b[1]
    dd.text((x, y), t, font=f, fill=color)

draw_text(left_txt, (0,0,0,255), w_left/2)
draw_text(right_txt, (255,255,255,255), w_left + w_right/2)

flat = Image.new("RGBA", (W, h), (255,255,255,255))
flat.alpha_composite(img)
bd = ImageDraw.Draw(flat)
bd.rounded_rectangle([0,0,W-1,h-1], radius=r, outline=(120,120,120,255), width=2)
flat.convert("RGB").save(out_path, "WEBP", quality=95)
print("OK", out_path, W, "x", h)
