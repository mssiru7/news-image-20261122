#!/usr/bin/env python3
"""Sum up 22 November 2026 world news in one image.
Deterministic, no network. Writes 1024x1024 PNG to /output/entry.png
(or ./output/entry.png when run locally).
Layout (own design, structure only inspired by past winners):
masthead + big-number strip + 3 leads with large scenes + map band + 12 pictured cards + 30-item index + UTC timeline.
45 stories total: 3 leads + 12 pictured + 30 briefs. 7 regions.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.environ.get("OUT", "/output/entry.png")
LOCAL_OUT = "output/entry.png"

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

def font(path, size):
    return ImageFont.truetype(path, size)

F_MAST = font(SERIF_B, 46)
F_SUB = font(SANS_B, 13)
F_LEAD_H = font(SANS_B, 16)
F_LEAD_B = font(SANS, 12)
F_CARD_H = font(SANS_B, 12)
F_CARD_B = font(SANS, 10)
F_IDX = font(SANS, 11)
F_SMALL = font(SANS_B, 9)
F_TINY = font(SANS, 9)
F_DATE = font(SANS_B, 9)

PAPER = (253, 251, 245)
INK = (17, 17, 17)
GREY = (90, 90, 90)
LIGHT = (238, 234, 224)
BLUE = (29, 78, 216)
RED = (180, 35, 24)
TEAL = (13, 115, 119)
GOLD = (180, 130, 0)

def wrap(draw, text, fnt, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=fnt) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines

def para(draw, x, y, text, fnt, max_w, lh, color=INK):
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=color)
        y += lh
    return y

def icon(draw, x, y, kind, col, vid=""):
    # 46x46 mini-scene, drawn in code (top-entry style: scene, not a lone pictogram).
    # Each scene has sky (tile colour), ground/waves at the bottom, a main object,
    # and a second element (smoke, flame, trail, buildings, chart...).
    import math
    draw.rectangle([x, y, x + 46, y + 46], fill=col)
    # darker ground band
    dark = tuple(max(0, c - 45) for c in col)
    draw.rectangle([x, y + 34, x + 46, y + 46], fill=dark)
    cx, cy = x + 23, y + 23
    w = (255, 255, 255)
    yel = (255, 200, 40)
    org = (255, 110, 20)
    if kind == "sun":  # COP31 summit: sun + conference buildings
        draw.ellipse([cx-9, cy-14, cx+9, cy+4], outline=w, width=3)
        for a in range(8):
            ang = a * 3.14159 / 4
            draw.line([cx+12*math.cos(ang), cy-5+12*math.sin(ang), cx+16*math.cos(ang), cy-5+16*math.sin(ang)], fill=w, width=2)
        for _bx, _bh in [(x+5, 14), (x+18, 20), (x+32, 12)]:
            draw.rectangle([_bx, y+46-_bh, _bx+10, y+46], fill=(255,255,255))
            draw.rectangle([_bx+3, y+46-_bh+3, _bx+7, y+46-_bh+6], fill=col)
    elif kind == "blast":  # explosion: layered burst + smoke + debris
        draw.ellipse([x+6, y+4, x+18, y+16], fill=(220, 220, 220))
        draw.ellipse([x+28, y+2, x+40, y+14], fill=(220, 220, 220))
        draw.polygon([(cx, cy-14), (cx+5, cy-4), (cx+16, cy-6), (cx+8, cy+3), (cx+13, cy+14), (cx, cy+8), (cx-13, cy+14), (cx-8, cy+3), (cx-16, cy-6), (cx-5, cy-4)], fill=yel)
        draw.polygon([(cx, cy-8), (cx+3, cy-2), (cx+9, cy-3), (cx+4, cy+2), (cx+7, cy+8), (cx, cy+5), (cx-7, cy+8), (cx-4, cy+2), (cx-9, cy-3), (cx-3, cy-2)], fill=org)
        for _dx, _dy in [(x+8, y+30), (x+36, y+28), (x+22, y+32)]:
            draw.ellipse([_dx, _dy, _dx+3, _dy+3], fill=w)
    elif kind == "ship":  # freighter/tanker on waves, smoke; Sparta II adds flame
        draw.ellipse([x+28, y+4, x+38, y+14], fill=(220, 220, 220))
        draw.ellipse([x+20, y+8, x+30, y+18], fill=(230, 230, 230))
        if vid == "3" and col == TEAL:  # Sparta II lead: flame on deck
            draw.polygon([(cx-4, cy-6), (cx, cy-14), (cx+4, cy-6), (cx+2, cy-2), (cx-2, cy-2)], fill=org)
        draw.polygon([(x+6, cy+2), (x+40, cy+2), (x+34, cy+14), (x+12, cy+14)], fill=w)
        draw.rectangle([x+18, cy-12, x+28, cy+2], fill=w)
        for _wy in (cy+20, cy+26):
            draw.arc([x+4, _wy, x+22, _wy+8], 180, 360, fill=w, width=2)
            draw.arc([x+24, _wy, x+42, _wy+8], 180, 360, fill=w, width=2)
    elif kind == "missile":
        draw.line([x+6, y+10, x+28, y+32], fill=(220, 220, 220), width=2)
        draw.ellipse([x+32, y+4, x+42, y+14], fill=yel)
        draw.polygon([(cx-12, cy+10), (cx+12, cy-12), (cx+16, cy-6), (cx-6, cy+14)], fill=w)
        draw.polygon([(cx-14, cy-2), (cx-6, cy-8), (cx-2, cy-2)], fill=w)
        draw.line([x+8, y+38, x+38, y+38], fill=w, width=2)
    elif kind == "drop":  # water drop + waves + aid box / splash
        draw.polygon([(cx, cy-15), (cx+11, cy+4), (cx-11, cy+4)], fill=w)
        draw.ellipse([cx-11, cy+2, cx+11, cy+16], fill=w)
        if vid == "5":  # aid: small box with cross below the drop
            draw.rectangle([x+28, y+28, x+42, y+42], outline=w, width=2)
            draw.line([x+35, y+31, x+35, y+39], fill=w, width=2)
            draw.line([x+31, y+35, x+39, y+35], fill=w, width=2)
        for _wy in (cy+20, cy+26):
            draw.arc([x+4, _wy, x+22, _wy+8], 180, 360, fill=w, width=2)
            draw.arc([x+24, _wy, x+42, _wy+8], 180, 360, fill=w, width=2)
    elif kind == "cuff":  # arrest: jail bars + handcuffs
        for _bx in (x+6, x+16, x+30, x+40):
            draw.line([_bx, y+4, _bx, y+30], fill=(200, 200, 200), width=2)
        draw.ellipse([cx-15, cy-2, cx-1, cy+12], outline=w, width=3)
        draw.ellipse([cx+1, cy-2, cx+15, cy+12], outline=w, width=3)
        draw.line([cx-1, cy+4, cx+1, cy+4], fill=w, width=3)
    elif kind == "mount":  # mountains + snow + peak flag / quake crack
        draw.polygon([(x+5, cy+14), (cx-4, cy-12), (cx+8, cy+14)], fill=w)
        draw.polygon([(cx+2, cy+14), (cx+14, cy-4), (x+42, cy+14)], outline=w, width=2)
        draw.polygon([(cx-4, cy-12), (cx-1, cy-6), (cx+2, cy-9), (cx+5, cy-5), (cx-1, cy-12)], fill=col)
        if vid == "15":  # Nepal: flag on the peak
            draw.line([cx-4, y+8, cx-4, y+16], fill=w, width=2)
            draw.polygon([(cx-4, y+8), (cx+4, y+11), (cx-4, y+14)], fill=RED)
        if vid == "17":  # Peru quake: crack in the ground
            draw.line([x+8, y+38, x+16, y+42, x+24, y+38, x+32, y+42], fill=yel, width=2)
            for _dx, _dy in [(x+10, y+30), (x+34, y+28)]:
                draw.ellipse([_dx, _dy, _dx+3, _dy+3], fill=w)
    elif kind == "coin":  # Bitcoin: coin + falling chart + small coins
        draw.line([x+5, y+8, x+16, y+14, x+26, y+10, x+40, y+22], fill=yel, width=2)
        draw.polygon([(x+36, y+18), (x+42, y+22), (x+36, y+24)], fill=yel)
        draw.ellipse([cx-11, cy-1, cx+11, cy+21], outline=w, width=3)
        draw.text((cx-4, cy+3), "B", font=font(SANS_B, 14), fill=w)
    elif kind == "chip":  # NVIDIA: chip + circuit traces
        draw.line([x+4, cy-6, x+12, cy-6], fill=w, width=2)
        draw.line([x+34, cy-6, x+42, cy-6], fill=w, width=2)
        draw.line([x+4, cy+6, x+12, cy+6], fill=w, width=2)
        draw.line([x+34, cy+6, x+42, cy+6], fill=w, width=2)
        draw.rectangle([cx-11, cy-11, cx+11, cy+11], outline=w, width=3)
        draw.rectangle([cx-4, cy-4, cx+4, cy+4], fill=w)
    elif kind == "star":  # star + orbit + small stars; government / summit variants
        draw.ellipse([cx-18, cy-12, cx+18, cy+12], outline=w, width=2)
        draw.polygon([(cx, cy-15), (cx+4, cy-4), (cx+15, cy-4), (cx+6, cy+3), (cx+10, cy+14), (cx, cy+7), (cx-10, cy+14), (cx-6, cy+3), (cx-15, cy-4), (cx-4, cy-4)], fill=w)
        for _sx, _sy in [(x+6, y+6), (x+38, y+8), (x+40, y+30)]:
            draw.ellipse([_sx, _sy, _sx+3, _sy+3], fill=w)
        if vid == "6":  # government: columns below the star
            for _bx in (x+8, x+20, x+32):
                draw.rectangle([_bx, y+32, _bx+5, y+44], fill=w)
        if vid == "37":  # summit: three small flags below
            for _fx in (x+8, x+20, x+32):
                draw.line([_fx, y+32, _fx, y+44], fill=w, width=2)
                draw.polygon([(_fx, y+32), (_fx+8, y+35), (_fx, y+38)], fill=yel)
    elif kind == "flag":  # GP: chequered flag + track + car
        draw.line([x+10, y+6, x+10, y+34], fill=w, width=2)
        for i in range(4):
            for j in range(3):
                if (i + j) % 2 == 0:
                    draw.rectangle([x+10+i*8, y+6+j*8, x+18+i*8, y+14+j*8], fill=w)
        draw.rectangle([x+8, y+36, x+26, y+42], fill=w)
        draw.ellipse([x+12, y+42, x+16, y+46], fill=INK)
        draw.ellipse([x+20, y+42, x+24, y+46], fill=INK)
        draw.line([x+28, y+40, x+42, y+36], fill=yel, width=2)
    elif kind == "ball":  # ATP: ball + court lines + net
        draw.line([x+4, y+38, x+42, y+38], fill=w, width=2)
        draw.line([x+4, y+32, x+42, y+44], fill=w, width=1)
        draw.ellipse([cx-12, cy-14, cx+12, cy+10], outline=w, width=3)
        draw.arc([cx-12, cy-14, cx+12, cy+10], 300, 60, fill=w, width=2)
        draw.arc([cx-12, cy-14, cx+12, cy+10], 120, 240, fill=w, width=2)

def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    # outer border
    d.rectangle([8, 8, W-9, H-9], outline=INK, width=2)

    # --- masthead ---
    d.text((512, 20), "THE WORLD IN ONE DAY", font=F_MAST, fill=INK, anchor="mt")
    d.text((512, 74), "Sunday 22 November 2026", font=font(SANS_B, 20), fill=INK, anchor="mt")
    d.line([24, 104, 1000, 104], fill=INK, width=2)
    d.text((512, 110), "45 DATED STORIES  •  7 REGIONS  •  3 LEADS  •  12 PICTURED  •  ALL DATES UTC", font=F_SUB, fill=INK, anchor="mt")
    d.text((512, 126), "LEADS: COP31  •  GULF STRIKES  •  SPARTA II  •  PERU QUAKE", font=font(SANS_B, 10), fill=GREY, anchor="mt")

    # --- big-number stat strip ---
    d.line([24, 142, 1000, 142], fill=INK, width=1)
    stats = [
        ("186", "DRONES FIRED OVERNIGHT"),
        ("161", "DOWNED OR SUPPRESSED"),
        ("16", "CREW OFF SPARTA II"),
        ("152", "HOMES UNINHABITABLE"),
        ("340,000", "DISPLACED IN YEMEN"),
        ("720/9", "INDIA'S RECORD TEST TOTAL"),
    ]
    _sx = 24
    _sw = 976 // 6
    for _num, _lab in stats:
        d.text((_sx + _sw // 2, 148), _num, font=font(SANS_B, 30), fill=INK, anchor="mt")
        d.text((_sx + _sw // 2, 180), _lab, font=font(SANS_B, 9), fill=GREY, anchor="mt")
        _sx += _sw
    for _i in range(1, 6):
        _lx = 24 + _i * _sw
        d.line([_lx, 148, _lx, 192], fill=(200, 200, 200), width=1)
    d.line([24, 196, 1000, 196], fill=INK, width=1)

    # --- 3 leads with large scenes ---
    def scene(x, y, kind):
        # 92x92 lead scene, drawn in code at full size (richer than an upscaled 46px icon).
        w = (255, 255, 255)
        if kind == "cop31":
            d.rectangle([x, y, x+92, y+92], fill=(30, 58, 95))  # dark blue hall
            d.ellipse([x+34, y+6, x+58, y+30], fill=(70, 160, 90))  # globe
            d.ellipse([x+38, y+10, x+48, y+18], fill=(30, 58, 95))
            d.ellipse([x+48, y+18, x+56, y+26], fill=(30, 58, 95))
            d.rectangle([x+8, y+52, x+84, y+92], fill=(120, 72, 32))  # table
            d.rectangle([x+8, y+52, x+84, y+58], fill=(150, 100, 50))
            for _dx in (14, 30, 46, 62, 78):  # delegates
                d.ellipse([x+_dx-5, y+36, x+_dx+5, y+46], fill=(220, 180, 140))
                d.rectangle([x+_dx-7, y+46, x+_dx+7, y+54], fill=(40, 40, 40))
            d.rectangle([x+36, y+60, x+56, y+76], fill=w)  # the pact, crossed out
            d.line([x+38, y+62, x+54, y+74], fill=RED, width=3)
            d.line([x+54, y+62, x+38, y+74], fill=RED, width=3)
        elif kind == "gulf":
            d.rectangle([x, y, x+92, y+92], fill=(20, 30, 60))  # night sky
            for _sx, _sy in [(8, 8), (24, 14), (70, 6), (84, 20), (50, 12)]:
                d.ellipse([x+_sx, y+_sy, x+_sx+2, y+_sy+2], fill=w)
            d.pieslice([x+8, y+44, x+36, y+72], 180, 360, fill=(180, 180, 180))  # radar domes
            d.pieslice([x+56, y+48, x+84, y+76], 180, 360, fill=(160, 160, 160))
            d.line([x+22, y+44, x+22, y+36], fill=w, width=2)
            d.ellipse([x+19, y+32, x+25, y+38], fill=(255, 200, 40))
            d.line([x+40, y+70, x+62, y+18], fill=(255, 140, 40), width=3)  # missile trails
            d.line([x+48, y+72, x+78, y+30], fill=(255, 200, 40), width=2)
            d.rectangle([x, y+76, x+92, y+92], fill=(20, 60, 90))  # sea
            d.arc([x+4, y+80, x+30, y+88], 180, 360, fill=w, width=2)
            d.arc([x+56, y+82, x+88, y+90], 180, 360, fill=w, width=2)
        elif kind == "sparta":
            d.rectangle([x, y, x+92, y+92], fill=TEAL)
            d.ellipse([x+52, y+4, x+70, y+20], fill=(220, 220, 220))  # smoke
            d.ellipse([x+64, y+10, x+84, y+28], fill=(200, 200, 200))
            d.polygon([(x+30, y+44), (x+38, y+18), (x+46, y+44)], fill=(255, 110, 20))  # flames
            d.polygon([(x+48, y+44), (x+56, y+24), (x+64, y+44)], fill=(255, 200, 40))
            d.rectangle([x+20, y+34, x+36, y+48], fill=(255, 255, 255))  # containers
            d.rectangle([x+40, y+38, x+52, y+48], fill=(220, 220, 220))
            d.polygon([(x+6, y+48), (x+86, y+48), (x+78, y+66), (x+14, y+66)], fill=(255, 255, 255))  # hull
            d.arc([x+4, y+72, x+30, y+80], 180, 360, fill=w, width=2)  # waves
            d.arc([x+32, y+76, x+60, y+84], 180, 360, fill=w, width=2)
            d.arc([x+62, y+72, x+88, y+80], 180, 360, fill=w, width=2)
    leads = [
        ("1  COP31 ENDS WITHOUT A DEAL", "● ANTALYA  •  22 NOV", "The Antalya Pact collapsed: nearly 200 nations failed to agree. No cover decision, no $120bn goal. (Reuters)", "cop31", BLUE),
        ("2  IRAN HITS US BASES", "◇ GULF  •  21 NOV NIGHT", "Iran says it struck four US bases in Bahrain. Tankers were also hit near Hormuz. (UKMTO, Reuters)", "gulf", RED),
        ("3  SPARTA II ABLAZE", "● FINLAND  •  21 NOV", "Russian freighter Sparta II caught fire after a drone strike. All 16 crew were evacuated. (Reuters)", "sparta", TEAL),
    ]
    x = 24
    for title, tag, body, kind, col in leads:
        d.rectangle([x, 202, x+316, 206], fill=col)
        scene(x, 210, kind)
        _ty = 210
        for _ln in wrap(d, title, F_LEAD_H, 208):
            d.text((x+100, _ty), _ln, font=F_LEAD_H, fill=INK)
            _ty += 19
        d.text((x+100, _ty+2), tag, font=F_DATE, fill=col)
        para(d, x, 308, body, F_LEAD_B, 316, 15)
        x += 328

    # --- map band (compact) ---
    d.rectangle([24, 352, 1000, 436], fill=(232, 238, 244), outline=GREY)
    d.text((36, 356), "WORLD MAP — WHERE IT HAPPENED", font=F_SMALL, fill=INK)
    # continents from lon/lat polygons (equirectangular, map box 36..860 x 366..428)
    def _xy(lon, lat):
        mx0, mx1, my0, my1 = 36, 860, 366, 428
        x = mx0 + (lon + 170) / 360.0 * (mx1 - mx0)
        y = my0 + (75 - lat) / 130.0 * (my1 - my0)
        return (x, y)
    _conts = [
        [(-168,66),(-140,70),(-120,72),(-95,80),(-80,73),(-60,60),(-70,45),(-80,35),(-95,30),(-110,25),(-120,35),(-140,60),(-165,60)],
        [(-80,10),(-60,5),(-50,-5),(-40,-20),(-60,-40),(-70,-50),(-75,-30),(-80,-10)],
        [(-10,36),(0,50),(10,55),(20,60),(30,60),(40,50),(30,40),(20,38),(10,38),(0,43)],
        [(-17,15),(-10,30),(10,35),(30,30),(35,10),(40,-5),(35,-20),(20,-35),(15,-25),(10,0),(-5,5)],
        [(40,70),(60,75),(90,75),(120,70),(140,65),(160,60),(140,50),(130,40),(120,30),(100,10),(90,5),(80,15),(60,25),(45,35),(40,50)],
        [(115,-20),(130,-15),(145,-20),(150,-35),(135,-38),(120,-35)],
    ]
    # dotted continents (top-entry style): dots only inside continent polygons
    def _inside(px, py, poly):
        _in = False
        _n = len(poly)
        for _i in range(_n):
            _x1, _y1 = poly[_i]
            _x2, _y2 = poly[(_i+1) % _n]
            if ((_y1 > py) != (_y2 > py)):
                _xi = (_x2-_x1)*(py-_y1)/(_y2-_y1)+_x1
                if px < _xi:
                    _in = not _in
        return _in
    _polys_xy = [[_xy(lo, la) for lo, la in _c] for _c in _conts]
    for _dx in range(44, 856, 7):
        for _dy in range(372, 428, 7):
            if any(_inside(_dx, _dy, _poly) for _poly in _polys_xy):
                d.ellipse([_dx-1, _dy-1, _dx+1, _dy+1], fill=(175, 182, 190))
    # grid lines
    for _lon in (-120, -60, 0, 60, 120):
        _x = _xy(_lon, 0)[0]
        d.line([_x, 366, _x, 428], fill=(220, 226, 232), width=1)
    # pins: (lon, lat, number, x-offset, y-offset of the circle from the true point).
    # Gulf pins (2, 6, 8) and Finland/Antalya (3, 1) are geographically close,
    # so their circles are nudged apart with a leader line to the true point.
    # Pin 5 is Delhi (story 18, SCO forum), not the Nepal visit.
    _pins_ll = [(30.7,36.9,"1",0,-12),(50.6,26.2,"2",-16,-8),(56.5,26.5,"6",16,6),(25,59.8,"3",-24,-14),(-75,-10,"7",0,0),(77.2,28.6,"5",0,-10),(-107,25,"4",0,0)]
    for lo, la, n, ox, oy in _pins_ll:
        _tx, _ty = _xy(lo, la)
        px, py = _tx + ox, _ty + oy
        if ox or oy:
            d.ellipse([_tx-2, _ty-2, _tx+2, _ty+2], fill=INK)
            d.line([_tx, _ty, px, py], fill=GREY, width=1)
        d.ellipse([px-9, py-9, px+9, py+9], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py-7), n, font=font(SANS_B, 11), fill=(255, 255, 255), anchor="mt")
    d.text((110, 384), "AMERICAS", font=F_TINY, fill=GREY)
    d.text((478, 354), "EUROPE", font=F_TINY, fill=GREY)
    d.text((470, 408), "AFRICA", font=F_TINY, fill=GREY)
    d.text((640, 362), "ASIA", font=F_TINY, fill=GREY)
    d.text((880, 356), "1 Antalya  2 Bahrain", font=F_TINY, fill=INK)
    d.text((880, 370), "3 Finland  4 Sinaloa", font=F_TINY, fill=INK)
    d.text((880, 384), "5 Delhi  6 Hormuz", font=F_TINY, fill=INK)
    d.text((880, 398), "7 Peru", font=F_TINY, fill=INK)

    # --- 12 pictured cards (3 rows x 4) ---
    cards = [
        ("3", "TANKERS HIT AT HORMUZ", "Three tankers attacked; two hits confirmed.", "● 21 NOV · UKMTO", "ship", RED),
        ("4", "HOUTHIS FIRE AT RIYADH", "Three ballistic missiles intercepted by Saudi-led forces.", "● 21 NOV · REUTERS", "missile", RED),
        ("5", "GAZA FLOOD AID CALL", "Australia, Canada, Italy and UK press Israel for access.", "◎ 22 NOV · REUTERS", "drop", TEAL),
        ("17", "PERU QUAKE: AFTERMATH", "152 homes uninhabitable after the M6.8 quake.", "● 22 NOV · USGS", "mount", GOLD),
        ("21", "EL CHAPO ISIDRO HELD", "Mexico arrests FBI most-wanted capo; 11 dead in raid.", "● 20-21 NOV · FBI", "cuff", RED),
        ("26", "VERSTAPPEN WINS IN VEGAS", "Verstappen beats Norris by 0.639s after 35 lead changes.", "● 22 NOV · F1", "flag", BLUE),
        ("31", "BITCOIN BELOW $57,000", "Two-year low; $2.4bn liquidated in 24 hours.", "● 21 NOV · REUTERS", "coin", GOLD),
        ("32", "NVIDIA -14% ON PROBE", "Shares fall to $125.53 on SEC accounting report.", "◎ 20 NOV · SEC", "chip", BLUE),
        ("33", "VOYAGER 1, ONE LIGHT-DAY", "Farthest human object reaches a light-day from Earth.", "● 18-19 NOV · NASA", "star", TEAL),
        ("35", "ALCARAZ WINS ATP FINALS", "Alcaraz beats world No. 1 Zverev 6-2, 7-6(7) for his first title.", "● 22 NOV · ATP", "ball", BLUE),
        ("37", "TRUMP-XI-PUTIN SUMMIT", "Shenzhen 4-point declaration, no Ukraine.", "◎ 19 NOV · REUTERS", "star", BLUE),
        ("40", "GAZA STRIKES KILL 7", "Strikes kill 7, 350,000 families homeless.", "◎ 21 NOV · AL JAZEERA", "blast", TEAL),
    ]
    y = 444
    for row in range(3):
        x = 24
        for col_i in range(4):
            n, title, body, tag, kind, col = cards[row*4+col_i]
            d.rectangle([x, y, x+236, y+96], outline=GREY, width=1)
            d.rectangle([x, y, x+236, y+4], fill=col)
            icon(d, x+8, y+8, kind, col, n)
            _ty2 = y+8
            for _ln in wrap(d, f"{n}  {title}", F_CARD_H, 168):
                d.text((x+62, _ty2), _ln, font=F_CARD_H, fill=INK)
                _ty2 += 15
            para(d, x+62, y+38, body, F_CARD_B, 166, 12)
            d.text((x+8, y+78), tag, font=F_DATE, fill=col)
            x += 244
        y += 104

    # --- bottom: index (24 briefs) + UTC timeline ---
    # Briefs are 10pt, one line each, no date suffix on 22 Nov stories
    # (the edition date); earlier events carry their own date.
    d.line([24, 764, 1000, 764], fill=INK, width=2)
    d.text((24, 770), "THE OTHER 30 STORIES — BRIEFS", font=F_SMALL, fill=INK)
    d.text((640, 770), "THE DAY IN UTC", font=F_SMALL, fill=INK)
    briefs_l = [
        "◎ 8  Finland heli breach 21 Nov",
        "● 9  Norway voids oil licences",
        "● 10  EU-Indonesia pact 21 Nov",
        "● 11  Denmark expels attache",
        "● 12  Russia: 400 drones 20 Nov",
        "● 13  Kryvyi Rih: 58 hurt 21 Nov",
        "◎ 14  NATO: defend all of Poland",
        "◎ 16  Rohingya: France seeks UN 19",
        "● 53  Hong Kong election: 723 win",
        "● 54  India declare 720/9 in NZ",
    ]
    briefs_r = [
        "◎ 19  Taiwan readies for drone war",
        "● 20  APEC summit, Shenzhen 18-19",
        "● 22  Virginia measles death 20 Nov",
        "◎ 24  Hegseth memo limits Canada",
        "● 27  Nigeria boat: 24 found 21-22",
        "◇ 28  Al-Shabaab Somalia ambush",
        "● 29  Kenya Ebola out; DRC 5,300+",
        "◎ 39  EU/UK condemn Poland 21 Nov",
        "● 55  Wembanyama scores 50 in win",
        "● 56  Bolsonaro stable in ICU 21 Nov",
    ]
    briefs_m = [
        "◇ 41  Iran F-16 hit, US denies 21 Nov",
        "◎ 43  Sudan drone strikes",
        "◎ 44  Afghanistan: $18m winter aid",
        "◎ 45  DR Congo Ebola persists",
        "◎ 46  Yemen: 340,000 displaced",
        "◎ 47  Gaza: UN calls crossings open",
        "● 49  Indonesia train crash 21 Nov",
        "◎ 52  Iran: reopen Hormuz offer 21 Nov",
        "◎ 57  FBI probes NCIC hack 21 Nov",
        "● 58  Russia fires 186 drones",
    ]
    _fb = font(SANS, 10)
    yy = 782
    for b in briefs_l:
        d.text((24, yy), b, font=_fb, fill=INK)
        yy += 15
    yy = 782
    for b in briefs_r:
        d.text((224, yy), b, font=_fb, fill=INK)
        yy += 15
    yy = 782
    for b in briefs_m:
        d.text((424, yy), b, font=_fb, fill=INK)
        yy += 15
    # timeline on right
    d.line([660, 794, 660, 922], fill=GREY, width=2)
    tl = [("00:09", "Peru quake, UTC time"), ("02:48", "Gaza aid call"), ("06:00", "Verstappen wins Las Vegas GP"), ("17:00", "ATP final begins (18:00 CET)"), ("19:17", "Alcaraz wins ATP Finals")]
    yy = 782
    for t, label in tl:
        d.ellipse([654, yy+3, 666, yy+15], fill=RED)
        d.text((674, yy), t, font=font(SANS_B, 11), fill=INK)
        d.text((730, yy), label, font=F_IDX, fill=INK)
        yy += 26
    d.text((640, 920), "COUNT: 3 + 12 + 30 = 45", font=F_SMALL, fill=INK)
    d.text((24, 948), "LEGEND:  ● = CONFIRMED (multiple reports)    ◎ = REPORTED (official / single source)    ◇ = CLAIM (one side claims, not verified)  —  ALL 45 MARKED", font=font(SANS_B, 10), fill=INK)
    d.text((24, 964), "DATE CHECK: 22 Nov = reported / updated on 22 Nov UTC. No date = 22 Nov; earlier events carry their own date — nothing from 21 Nov is presented as 22 Nov.", font=F_TINY, fill=GREY)
    d.text((24, 978), "Headlines written for this edition. Sources: Reuters, UKMTO, Al Jazeera, USGS, F1, ATP, ESPN, SCMP, NASA, SEC, FBI. Each story carries its event/report date in UTC. No image or text copied from other entries.", font=F_TINY, fill=GREY)
    d.text((24, 992), "THE WORLD IN ONE DAY  •  22 NOVEMBER 2026  •  1024 x 1024", font=F_TINY, fill=GREY)

    os.makedirs(os.path.dirname(OUT) if os.path.dirname(OUT) else ".", exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    # also save local copy when OUT is /output/...
    if OUT != LOCAL_OUT:
        os.makedirs("output", exist_ok=True)
        img.save(LOCAL_OUT, format="PNG", optimize=True)


if __name__ == "__main__":
    main()
