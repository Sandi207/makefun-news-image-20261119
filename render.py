#!/usr/bin/env python3
"""Offline, deterministic editorial illustration. Requires Pillow to re-render only."""

from functools import lru_cache
from pathlib import Path
import math

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
SCALE = 2
PAPER = "#F6F3EC"
INK = "#182630"
MUTED = "#53616B"
RULE = "#D4CDC1"
WHITE = "#FFFEFA"
PURPLE = "#6B4387"
BLUE = "#315A77"
RUST = "#A45439"
RED = "#A44239"
GOLD = "#926522"
SLATE = "#4C6374"

img = Image.new("RGB", (1024 * SCALE, 1024 * SCALE), PAPER)
draw = ImageDraw.Draw(img)


@lru_cache(maxsize=None)
def font(size, style="regular"):
    names = {
        "regular": "DejaVuSans.ttf",
        "bold": "DejaVuSans-Bold.ttf",
        "serif": "DejaVuSerif-Bold.ttf",
    }
    return ImageFont.truetype(
        "/usr/share/fonts/truetype/dejavu/" + names[style], round(size * SCALE)
    )


class Canvas:
    def __init__(self, x=0, y=0):
        self.x, self.y = x, y

    def point(self, p):
        return (round((self.x + p[0]) * SCALE), round((self.y + p[1]) * SCALE))

    def bounds(self, box):
        return (*self.point(box[:2]), *self.point(box[2:]))

    def rect(self, box, fill, outline=None, width=1, radius=0):
        method = draw.rounded_rectangle if radius else draw.rectangle
        kwargs = {"radius": round(radius * SCALE)} if radius else {}
        method(self.bounds(box), fill=fill, outline=outline, width=round(width * SCALE), **kwargs)

    def ellipse(self, box, fill, outline=None, width=1):
        draw.ellipse(self.bounds(box), fill=fill, outline=outline, width=round(width * SCALE))

    def line(self, points, fill, width=1):
        draw.line([self.point(p) for p in points], fill=fill, width=round(width * SCALE), joint="curve")

    def poly(self, points, fill):
        draw.polygon([self.point(p) for p in points], fill=fill)

    def text(self, x, y, text, size, color=INK, style="regular", align="left", limit=None):
        f = font(size, style)
        length = draw.textlength(text, font=f) / SCALE
        if limit is not None:
            assert length <= limit, f"Text overflow ({length:.1f} > {limit}): {text}"
        if align == "center":
            x -= length / 2
        elif align == "right":
            x -= length
        draw.text(self.point((x, y)), text, font=f, fill=color, anchor="lt")


c = Canvas()


def star(a, x, y, outer, inner, color, n=5, rotation=-math.pi / 2):
    points = []
    for i in range(n * 2):
        r = outer if i % 2 == 0 else inner
        theta = rotation + i * math.pi / n
        points.append((x + r * math.cos(theta), y + r * math.sin(theta)))
    a.poly(points, color)


def card(x, y, h, accent, section, headline, headline_size):
    a = Canvas(x, y)
    a.rect((0, 0, 472, h), WHITE, RULE, radius=6)
    a.rect((1, 1, 471, 5), accent, radius=2)
    a.text(16, 15, section, 11, accent, "bold", limit=440)
    a.text(16, 36, headline, headline_size, INK, "bold", limit=440)
    return a


def gta_art(x, y):
    a = Canvas(x, y)
    a.rect((0, 0, 440, 148), "#EDE5F3", radius=5)
    a.ellipse((180, 20, 268, 108), "#D8C5E4")
    a.text(16, 20, "VI", 100, PURPLE, "bold")
    a.line([(139, 128), (428, 128)], PURPLE, 2)
    # Fictional, geometric neon city: an illustration of the game, not a news location.
    buildings = [(145, 77, 26), (174, 55, 31), (208, 70, 23), (235, 40, 34),
                 (273, 67, 29), (307, 52, 34), (345, 88, 29), (378, 78, 30), (412, 61, 16)]
    for bx, by, bw in buildings:
        a.rect((bx, by, bx + bw, 127), PURPLE)
        for wx in range(bx + 5, bx + bw - 3, 8):
            for wy in range(by + 8, 123, 14):
                a.rect((wx, wy, wx + 2, wy + 5), "#C5A3D6")
    a.line([(190, 125), (186, 54)], INK, 4)
    for tip in [(158, 48), (162, 62), (174, 37), (202, 39), (214, 54), (210, 64)]:
        a.line([(186, 52), ((186 + tip[0]) / 2, min(47, tip[1] - 8)), tip], INK, 3)
    # Controller silhouette, directional pad, sticks, and four face buttons.
    a.poly([(238, 90), (256, 84), (341, 84), (358, 90), (374, 126),
            (371, 140), (351, 142), (334, 122), (265, 122), (248, 142),
            (229, 139), (227, 127)], INK)
    a.poly([(240, 94), (258, 90), (338, 90), (353, 96), (367, 127),
            (365, 135), (354, 136), (338, 116), (262, 116), (246, 136),
            (235, 133), (234, 126)], WHITE)
    a.rect((248, 104, 270, 109), PURPLE)
    a.rect((257, 95, 262, 117), PURPLE)
    for bx, by in [(344, 99), (352, 107), (344, 115), (336, 107)]:
        a.ellipse((bx - 3, by - 3, bx + 3, by + 3), PURPLE)
    a.ellipse((275, 110, 288, 123), INK)
    a.ellipse((314, 110, 327, 123), INK)
    a.rect((298, 99, 308, 103), PURPLE, radius=1)
    a.rect((346, 9, 431, 70), WHITE, radius=4)
    a.text(388.5, 16, "99", 36, PURPLE, "bold", "center")
    a.text(388.5, 55, "METACRITIC", 9, INK, "bold", "center", limit=79)


def usa_flag(a, x, y):
    a.rect((x, y, x + 100, y + 39), WHITE)
    for row in range(0, 13, 2):
        a.rect((x, y + row * 3, x + 100, y + row * 3 + 2), "#A54B4B")
    a.rect((x, y, x + 43, y + 21), BLUE)
    for row in range(4):
        for col in range(6):
            a.ellipse((x + 4 + col * 6, y + 3 + row * 5,
                       x + 5 + col * 6, y + 4 + row * 5), WHITE)


def summit_art(x, y):
    a = Canvas(x, y)
    a.rect((0, 0, 440, 148), "#E6ECF0", radius=5)
    for bx, by, bw in [(7, 73, 18), (33, 63, 21), (113, 50, 24),
                       (159, 67, 17), (267, 64, 26), (304, 45, 23), (409, 61, 21)]:
        a.rect((bx, by, bx + bw, 142), "#CCD9E0")
    usa_flag(a, 26, 10)
    a.rect((170, 10, 270, 49), "#AE423B")
    star(a, 184, 24, 8, 3.4, "#F4D18A")
    for sx, sy in [(195, 15), (201, 21), (201, 30), (195, 37)]:
        star(a, sx, sy, 3, 1.2, "#F4D18A")
    for fy, color in [(10, WHITE), (23, BLUE), (36, "#AE423B")]:
        a.rect((314, fy, 414, fy + 12), color)
    # Trump, Xi, and Putin beneath their flags. Xi's arm reaches around Trump.
    for cx in (76, 220, 364):
        a.poly([(cx - 22, 99), (cx + 22, 99), (cx + 39, 113),
                (cx + 39, 148), (cx - 39, 148), (cx - 39, 113)], BLUE)
        a.poly([(cx - 12, 100), (cx + 12, 100), (cx, 131)], WHITE)
        a.poly([(cx - 3, 110), (cx + 3, 110), (cx + 5, 132),
                (cx, 137), (cx - 5, 132)], "#AE423B")
    a.line([(205, 109), (161, 95), (104, 103)], BLUE, 16)
    a.ellipse((93, 98, 110, 108), "#D7AE8E")
    for cx, face in [(76, "#E3B595"), (220, "#D7AE8E"), (364, "#E0B9A0")]:
        a.rect((cx - 7, 88, cx + 7, 106), face)
        a.ellipse((cx - 19, 58, cx + 19, 103), face)
        a.line([(cx - 9, 79), (cx - 5, 79)], INK, 1)
        a.line([(cx + 5, 79), (cx + 9, 79)], INK, 1)
        a.line([(cx, 81), (cx - 1, 87), (cx + 2, 88)], "#AB8068", 1)
        a.line([(cx - 5, 93), (cx + 5, 93)], "#8E6253", 1)
    a.poly([(57, 76), (57, 63), (66, 57), (88, 57), (96, 64),
            (91, 70), (81, 68), (68, 72)], "#C99744")
    a.poly([(201, 75), (201, 65), (208, 57), (230, 57), (239, 64),
            (238, 77), (232, 69), (215, 67), (207, 71)], INK)
    a.line([(346, 74), (347, 67), (351, 65)], "#928E86", 3)
    a.line([(381, 74), (380, 67), (376, 65)], "#928E86", 3)
    for cx, label in [(76, "TRUMP"), (220, "XI"), (364, "PUTIN")]:
        a.text(cx, 134, label, 11, WHITE, "bold", "center")


def gulf_art(x, y):
    a = Canvas(x, y)
    a.rect((0, 0, 190, 112), "#E8EEEC", radius=4)
    a.poly([(0, 0), (64, 0), (70, 25), (99, 55), (121, 85), (137, 112), (0, 112)], "#E8D9CD")
    a.poly([(81, 0), (190, 0), (190, 112), (151, 112), (135, 73),
            (111, 45), (91, 26)], "#E8D9CD")
    a.text(148, 47, "IRAN", 10, RUST, "bold", "center")
    a.text(92, 99, "GULF", 10, MUTED, "bold", "center")
    # Kuwait at the northwestern end; Bahrain off the western shore.
    for px, py in [(70, 28), (103, 73)]:
        a.ellipse((px - 5, py - 5, px + 5, py + 5), RUST)
        a.ellipse((px - 2, py - 2, px + 2, py + 2), WHITE)
    a.text(5, 37, "KUWAIT", 11, INK, "bold")
    a.text(13, 80, "BAHRAIN", 11, INK, "bold")
    # Quadcopter above the Gulf with a dotted path to the targets.
    a.line([(133, 14), (169, 34)], INK, 3)
    a.line([(133, 34), (169, 14)], INK, 3)
    for px, py in [(133, 14), (169, 34), (133, 34), (169, 14)]:
        a.ellipse((px - 7, py - 3, px + 7, py + 3), None, INK, 1)
    a.rect((145, 18, 157, 30), INK, radius=2)
    for px, py in [(137, 43), (129, 50), (121, 57), (113, 64), (93, 28), (83, 28)]:
        a.ellipse((px - 1, py - 1, px + 1, py + 1), RUST)


def bangladesh_art(x, y):
    a = Canvas(x, y)
    a.rect((0, 0, 190, 112), "#F2E4DD", radius=4)
    for bx, by, r in [(80, 12, 14), (103, 9, 11), (111, 24, 16), (70, 27, 13)]:
        a.ellipse((bx - r, by - r, bx + r, by + r), "#D4C8C1")
    a.rect((38, 49, 146, 106), "#D9B49D", RED, 2)
    a.poly([(26, 54), (92, 23), (158, 54)], RED)
    for wx in (51, 109):
        a.rect((wx, 63, wx + 22, 83), INK)
        a.line([(wx + 11, 63), (wx + 11, 83)], "#D9B49D", 2)
    a.rect((82, 77, 102, 106), INK)
    for fx, fy, h in [(54, 51, 31), (75, 42, 38), (99, 45, 33), (124, 50, 28)]:
        a.poly([(fx - 9, fy), (fx - 11, fy - 11), (fx - 3, fy - 19),
                (fx + 1, fy - h), (fx + 6, fy - 17), (fx + 11, fy - 8),
                (fx + 8, fy)], RED)
        a.poly([(fx - 4, fy), (fx - 3, fy - 12), (fx + 2, fy - 19),
                (fx + 6, fy - 7), (fx + 4, fy)], "#E2A575")
    for px, py in [(10, 88), (29, 96), (158, 91), (179, 96)]:
        a.ellipse((px - 5, py - 11, px + 5, py - 1), INK)
        a.poly([(px - 7, py + 2), (px + 7, py + 2), (px + 11, 112), (px - 11, 112)], INK)
    a.line([(158, 97), (146, 79)], INK, 3)
    a.line([(29, 103), (35, 86)], INK, 3)


def ipo_art(x, y):
    a = Canvas(x, y)
    a.rect((0, 0, 190, 112), "#F0E9DB", radius=4)
    for xx, yy in [(96, 80), (127, 63), (159, 38)]:
        a.rect((xx, yy, xx + 19, 102), "#CFB98D", radius=2)
    a.line([(84, 103), (180, 103)], GOLD, 1)
    a.line([(85, 85), (117, 65), (141, 72), (173, 23)], GOLD, 4)
    a.poly([(161, 25), (177, 17), (177, 34)], GOLD)
    a.rect((16, 37, 77, 94), GOLD, radius=5)
    a.rect((22, 43, 71, 88), WHITE, radius=2)
    for pin in range(25, 72, 10):
        a.line([(pin, 30), (pin, 37)], GOLD, 3)
        a.line([(pin, 94), (pin, 101)], GOLD, 3)
    for pin in range(47, 89, 10):
        a.line([(9, pin), (16, pin)], GOLD, 3)
        a.line([(77, pin), (84, pin)], GOLD, 3)
    a.text(46.5, 51, "AI", 30, GOLD, "bold", "center")


def bridge_art(x, y):
    a = Canvas(x, y)
    a.rect((0, 0, 190, 112), "#E6EBED", radius=4)
    a.rect((0, 78, 190, 112), "#CCD8DF")
    for yy in (88, 100):
        for xx in (2, 36, 70, 105, 142, 176):
            a.line([(xx, yy), (xx + 18, yy)], "#A9BEC9", 1)
    for px in (29, 67, 128, 167):
        a.rect((px - 3, 30, px + 3, 91), SLATE)
    a.line([(0, 57), (29, 30), (67, 57)], SLATE, 2)
    a.line([(108, 57), (128, 30), (167, 57), (190, 39)], SLATE, 2)
    for px in (9, 19, 39, 49, 59, 117, 139, 149, 159, 179):
        a.line([(px, 45), (px, 59)], SLATE, 1)
    a.rect((0, 58, 80, 64), INK)
    a.rect((105, 58, 190, 64), INK)
    a.poly([(79, 58), (90, 73), (85, 77), (75, 63)], INK)
    a.poly([(107, 58), (99, 70), (104, 74), (113, 63)], INK)
    for bx, by, r in [(94, 21, 12), (105, 14, 10), (109, 30, 11)]:
        a.ellipse((bx - r, by - r, bx + r, by + r), "#B6C4CC")
    star(a, 93, 53, 29, 12, SLATE, n=9)
    star(a, 93, 53, 17, 7, WHITE, n=7)


def summary(a, text, y, size=16):
    assert len(text.split()) <= 12, text
    a.text(16, y, text, size, INK, limit=440)


def render():
    c.text(32, 14, "THE DAY IN ONE IMAGE", 11, MUTED, "bold")
    c.text(992, 14, "GLOBAL EDITION", 11, MUTED, "bold", "right")
    c.text(512, 34, "WORLD NEWS", 111, INK, "bold", "center", limit=960)
    c.rect((32, 127, 992, 187), INK, radius=3)
    c.text(512, 138, "THURSDAY 19 NOVEMBER 2026", 50, WHITE, "bold", "center", limit=930)

    a = card(32, 207, 305, PURPLE, "CULTURE / GAMING", "GTA VI LAUNCHES TODAY", 28)
    gta_art(48, 287)
    summary(a, "A 13-year wait ends on PS5 and Xbox Series X|S.", 249)
    a.text(16, 275, "$79.99", 20, PURPLE, "bold")
    a.text(111, 282, "STANDARD EDITION", 10, MUTED, "bold")
    a.line([(226, 276), (226, 294)], RULE)
    a.text(240, 275, "$1 billion", 20, PURPLE, "bold")
    a.text(352, 275, "EST. COST", 10, MUTED, "bold")
    a.text(352, 288, "PRODUCTION", 9, MUTED, "bold")

    a = card(520, 207, 305, BLUE, "DIPLOMACY / APEC SUMMIT", "TRUMP–XI–PUTIN", 32)
    summit_art(536, 287)
    summary(a, "Xi hugs Trump as three leaders gather at APEC.", 249)
    a.text(236, 276, "SHENZHEN, CHINA", 22, BLUE, "bold", "center", limit=440)

    a = card(32, 528, 200, RUST, "CONFLICT / MIDDLE EAST", "IRAN WIDENS GULF ATTACKS", 24)
    gulf_art(48, 590)
    a.text(222, 65, "KUWAIT", 12, RUST, "bold")
    a.text(222, 84, "First attack since September", 13, INK, limit=234)
    a.text(222, 115, "BAHRAIN", 12, RUST, "bold")
    a.text(222, 134, "Fourth attack in six days", 14, INK, limit=234)
    summary(a, "Iranian drones hit US assets in Kuwait and Bahrain.", 179, 16)

    a = card(520, 528, 200, RED, "UNREST / SOUTH ASIA", "BANGLADESH VIOLENCE", 26)
    bangladesh_art(536, 590)
    a.text(222, 65, "YUNUS'S HOME", 14, RED, "bold")
    a.text(222, 86, "Ablaze in Chattogram", 14, INK, limit=234)
    a.text(222, 114, "OVER 37", 25, RED, "bold")
    a.text(222, 143, "Grameen Bank branches", 13, INK, limit=234)
    a.text(222, 160, "targeted since 10 November", 12, MUTED, limit=234)
    summary(a, "Awami League lockdown grips Bangladesh.", 179, 16)

    a = card(32, 744, 200, GOLD, "BUSINESS / ARTIFICIAL INTELLIGENCE", "ANTHROPIC RECORD IPO", 26)
    ipo_art(48, 806)
    a.text(222, 66, "$81.3 billion", 29, GOLD, "bold", limit=234)
    a.text(222, 101, "BIGGEST IPO OF ALL TIME", 11, MUTED, "bold", limit=234)
    a.text(222, 125, "> $1.4 trillion", 26, GOLD, "bold", limit=234)
    a.text(222, 157, "PROSPECTIVE DEBUT VALUE", 11, MUTED, "bold", limit=234)
    summary(a, "AI company poised for its stock-market debut.", 179, 16)

    a = card(520, 744, 200, SLATE, "WAR / BLACK SEA", "CRIMEAN BRIDGE HIT AGAIN", 24)
    bridge_art(536, 806)
    a.text(222, 65, "THIRD STRIKE", 23, SLATE, "bold", limit=234)
    a.text(222, 94, "IN A WEEK", 15, SLATE, "bold")
    a.text(222, 126, "Traffic temporarily closed", 14, INK, limit=234)
    a.text(222, 149, "Damage being assessed", 14, MUTED, limit=234)
    summary(a, "Aksyonov confirms strike; traffic temporarily closed.", 179, 15)

    c.line([(32, 956), (992, 956)], INK, 1)
    c.text(512, 963, "VAN GOGH: $190.4 MILLION RECORD  •  ICJ: ROHINGYA VERDICT AGAINST MYANMAR TODAY", 12, INK, "bold", "center", limit=960)
    c.text(512, 982, "CYCLONE AKVAN LANDFALL • VOYAGER 1 REACHES ONE LIGHT-DAY • HAKEEM JEFFRIES SET TO BE FIRST AFRICAN-AMERICAN HOUSE SPEAKER", 12, MUTED, "bold", "center", limit=960)
    c.text(512, 1005, "19 November 2026 — the day in one image", 12, INK, "regular", "center", limit=960)

    result = img.resize((1024, 1024), Image.Resampling.LANCZOS)
    destination = ROOT / "entry.png"
    result.save(destination, format="PNG", optimize=True, compress_level=9)
    assert destination.stat().st_size <= 1_048_576
    with Image.open(destination) as check:
        assert check.format == "PNG" and check.size == (1024, 1024)
        check.verify()
    print(f"Wrote {destination.name}: {destination.stat().st_size} bytes, 1024×1024, valid PNG")


if __name__ == "__main__":
    render()
