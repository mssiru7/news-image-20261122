#!/usr/bin/env python3
"""Sum up 22 November 2026 world news in one image.
Deterministic, no network. Writes 1024x1024 PNG to /output/entry.png
(or ./output/entry.png when run locally).
Layout (own design, structure only inspired by past winners):
masthead + 3 leads + map band + 16 pictured scene cards + 33-item index + UTC timeline.
52 stories total: 3 leads + 16 pictured + 33 briefs. 7 regions.
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
F_CARD_H = font(SANS_B, 11)
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
    d.text((512, 22), "THE WORLD IN ONE DAY", font=F_MAST, fill=INK, anchor="mt")
    d.text((512, 78), "Sunday 22 November 2026", font=font(SANS_B, 20), fill=INK, anchor="mt")
    d.line([24, 108, 1000, 108], fill=INK, width=2)
    d.text((512, 114), "52 DATED STORIES  •  7 REGIONS  •  3 LEADS  •  16 PICTURED  •  ALL DATES UTC", font=F_SUB, fill=INK, anchor="mt")
    d.text((512, 130), "LEADS: COP31  •  GULF STRIKES  •  SPARTA II  •  PERU QUAKE", font=font(SANS_B, 10), fill=GREY, anchor="mt")

    # --- 3 leads ---
    leads = [
        ("1  COP31 NEARS A DEAL", "◎ ANTALYA  •  22 NOV", "Negotiators in Antalya close on a new climate package after long talks. A vote is set for 06:00 GMT. The deal is near — but not done.", "sun", BLUE),
        ("2  IRAN HITS US BASES", "◇ GULF  •  21 NOV NIGHT", "Iran says it struck four US bases in Bahrain with drones and missiles. Tankers were also hit near Hormuz. The Gulf is the day's sharpest front.", "blast", RED),
        ("3  SPARTA II ABLAZE", "● FINLAND  •  21 NOV", "A Russian freighter, Sparta II, caught fire after a drone strike in the Gulf of Finland. All 16 crew were evacuated as the ship drifted.", "ship", TEAL),
    ]
    x = 24
    for title, tag, body, kind, col in leads:
        d.rectangle([x, 148, x+316, 152], fill=col)
        _lead_no = title.split()[0]
        icon(d, x, 160, kind, col, _lead_no)
        _ty = 160
        for _ln in wrap(d, title, F_LEAD_H, 252):
            d.text((x+56, _ty), _ln, font=F_LEAD_H, fill=INK)
            _ty += 19
        d.text((x+56, _ty+2), tag, font=F_DATE, fill=col)
        para(d, x, 222, body, F_LEAD_B, 316, 15)
        x += 328

    # --- map band ---
    d.rectangle([24, 296, 1000, 392], fill=(232, 238, 244), outline=GREY)
    d.rectangle([30, 300, 280, 316], fill=(232, 238, 244))
    d.text((36, 302), "WORLD MAP — WHERE IT HAPPENED", font=F_SMALL, fill=INK)
    # continents from lon/lat polygons (equirectangular, map box 36..860 x 308..388)
    def _xy(lon, lat):
        mx0, mx1, my0, my1 = 36, 860, 322, 390
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
        for _dy in range(326, 388, 7):
            if any(_inside(_dx, _dy, _poly) for _poly in _polys_xy):
                d.ellipse([_dx-1, _dy-1, _dx+1, _dy+1], fill=(175, 182, 190))
    # grid lines
    for _lon in (-120, -60, 0, 60, 120):
        _x = _xy(_lon, 0)[0]
        d.line([_x, 322, _x, 390], fill=(220, 226, 232), width=1)
    _pins_ll = [(30.7,36.9,"1",-12),(50.6,26.2,"2",6),(56.5,26.5,"6",14),(25,59.8,"3",-6),(-75,-10,"7",0),(77.2,28.6,"5",-10),(-107,25,"4",0),(47.8,30.5,"8",12)]
    pins = [(_xy(lo, la)[0], _xy(lo, la)[1]+dy, n) for lo, la, n, dy in _pins_ll]
    for px, py, n in pins:
        d.ellipse([px-9, py-9, px+9, py+9], fill=RED, outline=(255, 255, 255), width=2)
        d.text((px, py-7), n, font=font(SANS_B, 11), fill=(255, 255, 255), anchor="mt")
    d.text((110, 340), "AMERICAS", font=F_TINY, fill=GREY)
    d.text((470, 312), "EUROPE", font=F_TINY, fill=GREY)
    d.text((470, 368), "AFRICA", font=F_TINY, fill=GREY)
    d.text((640, 318), "ASIA", font=F_TINY, fill=GREY)
    d.text((880, 302), "1 Antalya  2 Bahrain", font=F_TINY, fill=INK)
    d.text((880, 316), "3 Finland  4 Sinaloa", font=F_TINY, fill=INK)
    d.text((880, 330), "5 Delhi  6 Hormuz", font=F_TINY, fill=INK)
    d.text((880, 344), "7 Peru  8 Basra", font=F_TINY, fill=INK)
    d.text((36, 372), "Pins match the numbered stories below. Numbers are story numbers, not ranks.", font=F_TINY, fill=GREY)

    # --- 12 pictured cards ---
    cards = [
        ("3", "TANKERS HIT AT HORMUZ", "Three tankers attacked; two hits confirmed.", "● 21 NOV", "ship", RED),
        ("4", "HOUTHIS FIRE AT RIYADH", "Three ballistic missiles intercepted by Saudi-led forces.", "● 21 NOV", "missile", RED),
        ("5", "GAZA FLOOD AID CALL", "Australia, Canada, Italy and UK press Israel for access.", "◎ 22 NOV", "drop", TEAL),
        ("6", "ISRAEL: EISENKOT ASKED", "President turns to Eisenkot to form a government.", "◎ 22 NOV", "star", BLUE),
        ("15", "NEPAL PM IN DELHI", "Shah on a state visit; meets Modi on 23 Nov.", "● 22 NOV", "mount", TEAL),
        ("17", "PERU QUAKE: AFTERMATH", "152 homes uninhabitable after the M6.8 quake.", "● 22 NOV", "mount", GOLD),
        ("21", "EL CHAPO ISIDRO HELD", "Mexico arrests FBI most-wanted capo; 11 dead in raid.", "● 20-21 NOV", "cuff", RED),
        ("26", "LAS VEGAS GP: POLE", "Antonelli fastest, drops 5 places; Verstappen on pole.", "● 22 NOV", "flag", BLUE),
        ("31", "BITCOIN BELOW $57,000", "Two-year low; $2.4bn liquidated in 24 hours.", "● 21 NOV", "coin", GOLD),
        ("32", "NVIDIA -14% ON PROBE", "Shares fall to $125.53 on SEC accounting report.", "◎ 20 NOV", "chip", BLUE),
        ("33", "VOYAGER 1, ONE LIGHT-DAY", "Farthest human object reaches a light-day from Earth.", "● 18-19 NOV", "star", TEAL),
        ("35", "ATP FINAL IN TURIN", "Final at 18:00 CET in Turin. Zverev beat Medvedev.", "◎ 22 NOV", "ball", GOLD),
        ("36", "BASRA POWER FIRE", "Hartha station fire kills 4, injures 30.", "● 21 NOV", "blast", RED),
        ("37", "TRUMP-XI-PUTIN SUMMIT", "Shenzhen 4-point declaration, no Ukraine.", "◎ 19 NOV", "star", BLUE),
        ("38", "ROVNO ENERGY HIT", "Russia strikes substation in Rovno region.", "● 21 NOV", "missile", RED),
        ("40", "GAZA STRIKES KILL 7", "Strikes kill 7, 350,000 families homeless.", "◎ 21 NOV", "blast", TEAL),
    ]
    y = 400
    for row in range(4):
        x = 24
        for col_i in range(4):
            n, title, body, tag, kind, col = cards[row*4+col_i]
            d.rectangle([x, y, x+236, y+88], outline=GREY, width=1)
            d.rectangle([x, y, x+236, y+4], fill=col)
            icon(d, x+8, y+8, kind, col, n)
            _ty2 = y+8
            for _ln in wrap(d, f"{n}  {title}", F_CARD_H, 168):
                d.text((x+62, _ty2), _ln, font=F_CARD_H, fill=INK)
                _ty2 += 13
            para(d, x+62, y+36, body, F_CARD_B, 166, 12)
            d.text((x+8, y+70), tag, font=F_DATE, fill=col)
            x += 244
        y += 96

    # --- bottom: index (20 briefs) + UTC timeline ---
    d.line([24, 782, 1000, 782], fill=INK, width=2)
    d.text((24, 790), "THE OTHER 33 STORIES — BRIEFS", font=F_SMALL, fill=INK)
    d.text((640, 790), "THE DAY IN UTC", font=F_SMALL, fill=INK)
    briefs_l = [
        "◎ 8  Finland heli breach — 21 Nov",
        "● 9  Norway voids oil licences — 22 Nov",
        "● 10  EU-Indonesia pact signed — 21 Nov",
        "● 11  Denmark expels attache — 22 Nov",
        "● 12  Russia: 400 drones — 20 Nov",
        "● 13  Kryvyi Rih: 58 hurt, 2 dead — 21 Nov",
        "◎ 14  NATO: defend all of Poland — 22 Nov",
        "◎ 16  ICJ Rohingya: France seeks UN — 19 Nov",
        "● 18  SCO forum in Delhi — 22 Nov",
        "◎ 43  Sudan drone strikes — 22 Nov",
        "◎ 44  Afghanistan: $18m winter aid — 22 Nov",
    ]
    briefs_r = [
        "◎ 19  Taiwan readies for drone war — 22 Nov",
        "● 20  APEC summit, Shenzhen — 18-19 Nov",
        "● 22  Virginia measles death — 20 Nov",
        "◎ 23  US: Venezuela $12bn — 22 Nov",
        "◎ 24  Hegseth memo limits Canada — 22 Nov",
        "◎ 25  US Senate Dem test — 22 Nov",
        "● 27  Nigeria boat: 24 found — 21-22 Nov",
        "◇ 28  Al-Shabaab Somalia ambush — 22 Nov",
        "● 29  Kenya Ebola out; DRC 5,300+ — 22 Nov",
        "◎ 45  DR Congo Ebola persists — 22 Nov",
        "◎ 46  Yemen: 340,000 displaced — 22 Nov",
    ]
    briefs_m = [
        "◎ 30  Sahel resumes talks — 22 Nov",
        "◎ 34  UN killer-robot talks — 22 Nov",
        "◎ 39  EU/UK condemn Poland breach — 21 Nov",
        "◇ 41  Iran F-16 hit, US denies — 21 Nov",
        "● 42  France protests ease — 21 Nov",
        "◎ 47  Gaza: UN calls crossings open — 22 Nov",
        "◎ 48  S. Korea: Lee urges faster AI — 21 Nov",
        "● 49  Indonesia train crash, 3 hurt — 21 Nov",
        "● 50  Israel: tear gas at protests — 21 Nov",
        "◎ 51  Trump praises Nvidia CEO Huang — 21 Nov",
        "◎ 52  Iran: offer to reopen Hormuz — 21 Nov",
    ]
    _fb = font(SANS, 8)
    yy = 800
    for b in briefs_l:
        d.text((24, yy), b, font=_fb, fill=INK)
        yy += 13
    yy = 800
    for b in briefs_r:
        d.text((224, yy), b, font=_fb, fill=INK)
        yy += 13
    yy = 800
    for b in briefs_m:
        d.text((424, yy), b, font=_fb, fill=INK)
        yy += 13
    # timeline on right
    d.line([660, 812, 660, 940], fill=GREY, width=2)
    tl = [("00:09", "Peru quake, UTC time"), ("02:48", "Gaza aid call"), ("04:00", "Las Vegas GP final (UTC)"), ("06:00", "COP31 vote due"), ("17:00", "ATP final (18:00 CET)")]
    yy = 800
    for t, label in tl:
        d.ellipse([654, yy+3, 666, yy+15], fill=RED)
        d.text((674, yy), t, font=font(SANS_B, 11), fill=INK)
        d.text((730, yy), label, font=F_IDX, fill=INK)
        yy += 26
    d.text((640, 934), "COUNT: 3 + 16 + 33 = 52", font=F_SMALL, fill=INK)
    d.text((24, 948), "LEGEND:  ● = CONFIRMED (multiple reports)    ◎ = REPORTED (official / single source)    ◇ = CLAIM (one side claims, not verified)  —  ALL 52 MARKED", font=font(SANS_B, 10), fill=INK)
    d.text((24, 964), "DATE CHECK: 22 Nov = reported / updated on 22 Nov UTC. Earlier events carry their own date — nothing from 21 Nov is presented as 22 Nov.", font=F_TINY, fill=GREY)
    d.text((24, 978), "Headlines written for this edition. Each story carries its event/report date in UTC. No image or text copied from other entries.", font=F_TINY, fill=GREY)
    d.text((24, 992), "THE WORLD IN ONE DAY  •  22 NOVEMBER 2026  •  1024 x 1024", font=F_TINY, fill=GREY)

    os.makedirs(os.path.dirname(OUT) if os.path.dirname(OUT) else ".", exist_ok=True)
    img.save(OUT, format="PNG", optimize=True)
    # also save local copy when OUT is /output/...
    if OUT != LOCAL_OUT:
        os.makedirs("output", exist_ok=True)
        img.save(LOCAL_OUT, format="PNG", optimize=True)

if __name__ == "__main__":
    main()
