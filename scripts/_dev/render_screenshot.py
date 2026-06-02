"""Render terminal output as a PNG screenshot for docs/.

Simple: fixed-width text on dark background, ANSI-aware for a curated palette.
Usage: python scripts/_dev/render_screenshot.py <input.txt> <output.png> [title]
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

# We use Microsoft YaHei (msyh.ttc) because it covers CJK + Latin + emoji.
# Trade-off: not strictly monospace, but the report's mixed CJK/English
# content renders correctly without per-character font fallback.
FONT_CANDIDATES = [
    r"C:\Windows\Fonts\msyh.ttc",        # Microsoft YaHei
    r"C:\Windows\Fonts\NotoSansSC-VF.ttf",
    r"C:\Windows\Fonts\CascadiaMono.ttf",
    r"C:\Windows\Fonts\consola.ttf",
]
FONT_SIZE = 16


def pick_font() -> str:
    # Try to load each candidate; the one that loads with a real glyph
    # for `用` wins. We compare widths: the missing-glyph box and a real
    # CJK char have different widths in a real CJK font.
    for p in FONT_CANDIDATES:
        try:
            f = ImageFont.truetype(p, FONT_SIZE)
            # Real CJK glyphs are wide (~16px at 16pt); missing-glyph
            # boxes are narrower. If the candidate renders "用" at the
            # same width as a Latin char, it doesn't have the glyph.
            if abs(f.getlength("用") - f.getlength("M")) > 2:
                return p
        except Exception:
            continue
    return FONT_CANDIDATES[0]
LINE_HEIGHT = 22
PADDING_X = 24
PADDING_Y_TOP = 56  # room for title bar
PADDING_Y_BOT = 24
BG_COLOR = (30, 30, 30)         # #1e1e1e (VS Code-ish)
FG_COLOR = (212, 212, 212)      # #d4d4d4
TITLE_BG = (43, 43, 43)         # #2b2b2b
TITLE_FG = (204, 204, 204)
DOT_RED = (229, 96, 96)
DOT_YEL = (229, 192, 96)
DOT_GRN = (96, 192, 96)
TRAFFIC_LIGHT = [DOT_RED, DOT_YEL, DOT_GRN]

# ANSI 16-color palette (approximate, dark-background friendly)
ANSI = {
    "30": (0, 0, 0), "31": (224, 108, 117), "32": (152, 195, 121),
    "33": (229, 192, 123), "34": (97, 175, 239), "35": (198, 120, 221),
    "36": (86, 181, 193), "37": (220, 220, 220),
    "90": (128, 128, 128), "91": (224, 108, 117), "92": (152, 195, 121),
    "93": (229, 192, 123), "94": (97, 175, 239), "95": (198, 120, 221),
    "96": (86, 181, 193), "97": (240, 240, 240),
    "0":  FG_COLOR,    # reset
    "1":  None,        # bold - keep default
    "4":  None,        # underline - skip
}

# Regex matches ANSI CSI sequences: ESC[ ... m
ANSI_RE = re.compile(r"\x1b\[([0-9;]*)m")


def parse_ansi(line: str) -> list[tuple[str, str]]:
    """Split a line into (text, ansi_code) segments."""
    segments: list[tuple[str, str]] = []
    pos = 0
    current = ""
    for m in ANSI_RE.finditer(line):
        if m.start() > pos:
            current += line[pos:m.start()]
        if current:
            segments.append((current, "0"))  # last applied
            current = ""
        code = m.group(1)
        # Combine multiple codes (e.g. "1;33") into a single key for the palette
        segments.append(("", code if code else "0"))
        pos = m.end()
    if pos < len(line):
        current += line[pos:]
    if current:
        segments.append((current, "0"))
    # Merge: ANSI codes are 0-length, merge into adjacent text
    merged: list[tuple[str, str]] = []
    cur_text = ""
    cur_code = "0"
    for text, code in segments:
        if text == "":
            cur_code = code if code else "0"
        else:
            cur_text += text
            merged.append((cur_text, cur_code))
            cur_text = ""
    return merged


def color_for(code: str) -> tuple[int, int, int]:
    # last code in the sequence wins
    parts = code.split(";")
    last = parts[-1] if parts and parts[-1] else "0"
    return ANSI.get(last, FG_COLOR)


def render(input_path: Path, output_path: Path, title: str) -> None:
    raw_lines = input_path.read_text(encoding="utf-8", errors="replace").splitlines()
    # Strip empty trailing lines
    while raw_lines and not raw_lines[-1].strip():
        raw_lines.pop()

    font_path = pick_font()
    font = ImageFont.truetype(font_path, FONT_SIZE)

    # Measure widest line (segments can extend max width, but plain text is good enough)
    max_chars = max((len(re.sub(r"\x1b\[[0-9;]*m", "", ln)) for ln in raw_lines), default=80)
    char_w = int(font.getlength("M"))  # monospace, "M" is widest
    width = PADDING_X * 2 + max_chars * char_w
    height = PADDING_Y_TOP + len(raw_lines) * LINE_HEIGHT + PADDING_Y_BOT

    img = Image.new("RGB", (width, height), BG_COLOR)
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([(0, 0), (width, PADDING_Y_TOP - 8)], fill=TITLE_BG)
    for i, color in enumerate(TRAFFIC_LIGHT):
        cx = PADDING_X // 2 + i * 22
        draw.ellipse([(cx - 6, PADDING_Y_TOP // 2 - 10), (cx + 6, PADDING_Y_TOP // 2 + 2)], fill=color)
    # Title text
    title_font = ImageFont.truetype(font_path, FONT_SIZE - 2)
    title_w = draw.textlength(title, font=title_font)
    draw.text(((width - title_w) // 2, PADDING_Y_TOP // 2 - 10), title, fill=TITLE_FG, font=title_font)

    # Body text
    y = PADDING_Y_TOP
    for line in raw_lines:
        x = PADDING_X
        for text, code in parse_ansi(line):
            if not text:
                continue
            color = color_for(code)
            # Bold simulation: bright color
            if code.startswith("1;") or code == "1":
                # 1;31 etc. handled below
                pass
            draw.text((x, y), text, fill=color, font=font)
            x += int(font.getlength(text))
        y += LINE_HEIGHT

    output_path.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_path, "PNG")
    print(f"wrote {output_path} ({width}x{height})")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("usage: render_screenshot.py <input.txt> <output.png> [title]")
        sys.exit(1)
    render(Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else "aisurface")
