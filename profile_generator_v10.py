#!/usr/bin/env python3
from pathlib import Path
from xml.sax.saxutils import escape

# This version includes the latest straight-edged PCB ASCII layout.
# Edit the CONFIG values below, then run:
#     python3 profile_generator_v10.py
#
# It generates:
#     dark_mode.svg

# ============================================================
# EDIT THESE
# ============================================================

OUTPUT_FILE = "dark_mode.svg"  # generated profile image

USERNAME = "corypearl"
HOST = "github"

SOFTWARE = [
    "AWS", "EC2", "Vercel", "Figma", "Fusion 360", "Arduino",
    "MySQL", "Node.js", "Linux", "Excel", "Git", "GitHub",
    "Apache", "Nginx", "Canva", "Cloudflare R2", "macOS",
    "Linux CLI", "FreeRTOS", "ESP-IDF", "KiCad", "EasyEDA", "FreeCAD"
]

LANGUAGES = [
    "Python", "JavaScript", "HTML/CSS", "C", "Swift",
    "AArch64 & x86 Assembly", "Arduino C++",
    "SQL", "Java", "Bash", "System Verilog"
]

HARDWARE = [
    "Arduino / Arduino Nano", "ESP32", "Raspberry Pi",
    "DigiSpark", "ATtiny85", "Soldering"
]

FOCUS = [
    "Embedded Systems", "PCB Design", "Homelab",
    "Low-Level Programming", "Open Source Hardware",
    "Full Stack Web Design", "3D Modeling"
]

REPOS = "29"
COMMITS = "500+"

TAGLINE = "> Building cool things. Learning constantly. Sharing openly."


PCB_ASCII = r'''
                    +-------------------------------------------------------------+
                    | o                                                       o   |
                    |                                                             |
                    |  J1 USB-C         C1   C2        U3 3V3 REG                 |
                    |  +--------+       ||   ||       +---------+                 |
                    |  | V D+ D-|---+---||---||-------| IN  OUT |----+            |
                    |  |   GND  |---+-----------------|   GND   |    |            |
                    |  +--------+   |                 +---------+    |            |
                    |               |                                |            |
                    |       R1      R2        +-------------------+   |           |
                    |  +---/\/\----/\/\-------|                   |---+---+       |
                    |  |                       |     ESP32-S3      |       |      |
                    |  |   +-------------------|                   |---+   |      |
                    |  |   |                   +--+--+--+--+--+---+   |   |       |
                    |  |   |                      |  |  |  |  |       |   |       |
                    |  |   +----------+-----------+  |  |  |  +---+   |   |       |
                    |  |              |              |  |  |      |   |   |       |
                    |  |        +-----+-----+        |  |  +--+   |   |   |       |
                    |  |        |  FLASH   |        |  |     |   |   |   |        |
                    |  |        |  16 MB   |        |  |     |   |   |   |        |
                    |  |        +-----+-----+        |  |     |   |   |   |       |
                    |  |              |              |  |     |   |   |   |       |
                    |  |   +----------+---+      +---+--+--+  |   |   |   |       |
                    |  +---| AUDIO AMP    |      | LCD IF  |  |   |   |   |       |
                    |      +------+-------+      +----+----+  |   |   |   |       |
                    |             |                   |       |   |   |   |       |
                    |         +---+---+           +---+---+   |   |   |   |       |
                    |         | SPKR  |           | FPC18 |   |   |   |   |       |
                    |         +-------+           +-------+   |   |   |   |       |
                    |                                         |   |   |   |       |
                    |   SW1 RESET       LED1        J2 GPIO   |   |   |   |       |
                    |   +-------+       |>|         +---------+---+---+---+       |
                    |---| RESET |---+---/\/\--------| o o o o o o o o o |         |
                    |   +-------+   |    R3         +-------------------+         |
                    |               |                                             |
                    |   GND PLANE ---+-----------------------------------------.  |
                    |                                                        |    |
                    | o                                                       o   |
                    +-------------------------------------------------------------+
'''.strip("\n")

NAME_ASCII = r'''
  ______                                      
 /      \                                     
|  $$$$$$\  ______    ______   __    __       
| $$   \$$ /      \  /      \ |  \  |  \      
| $$      |  $$$$$$\|  $$$$$$\| $$  | $$      
| $$   __ | $$  | $$| $$   \$$| $$  | $$      
| $$__/  \| $$__/ $$| $$      | $$__/ $$      
 \$$    $$ \$$    $$| $$       \$$    $$      
  \$$$$$$   \$$$$$$  \$$       _\$$$$$$$      
                              |  \__| $$      
                               \$$    $$      
                                \$$$$$$       
 _______                                 __   
|       \                               |  \  
| $$$$$$$\  ______    ______    ______  | $$  
| $$__/ $$ /      \  |      \  /      \ | $$  
| $$    $$|  $$$$$$\  \$$$$$$\|  $$$$$$\| $$  
| $$$$$$$ | $$    $$ /      $$| $$   \$$| $$  
| $$      | $$$$$$$$|  $$$$$$$| $$      | $$  
| $$       \$$     \ \$$    $$| $$      | $$  
 \$$        \$$$$$$$  \$$$$$$$ \$$       \$$  
'''.strip("\n")


WIDTH = 1200
BASE_HEIGHT = 690
RIGHT_X = 590
RIGHT_END_X = 1160


def multiline_text(text, x, y, line_height, css_class, font_size):
    spans = []
    for i, line in enumerate(text.splitlines()):
        dy = "0" if i == 0 else str(line_height)
        spans.append(f'<tspan x="{x}" dy="{dy}">{escape(line)}</tspan>')
    return (
        f'<text x="{x}" y="{y}" class="{css_class}" '
        f'font-size="{font_size}" xml:space="preserve">'
        + "".join(spans)
        + "</text>"
    )


def wrap_items(items, max_chars=58):
    lines = []
    current = ""

    for item in items:
        candidate = item if not current else current + " • " + item

        if len(candidate) <= max_chars:
            current = candidate
        else:
            if current:
                lines.append(current)
            current = item

    if current:
        lines.append(current)

    return lines


def add_section(parts, title, items, y):
    parts.append(
        f'<text x="{RIGHT_X}" y="{y}" class="head" font-size="14">'
        f'- {escape(title)}</text>'
    )

    rule_start = {
        "Software": RIGHT_X + 90,
        "Languages": RIGHT_X + 110,
        "Hardware": RIGHT_X + 95,
    }.get(title, RIGHT_X + 100)

    parts.append(
        f'<line class="rule" x1="{rule_start}" y1="{y-5}" '
        f'x2="{RIGHT_END_X}" y2="{y-5}"/>'
    )

    y += 27

    for line in wrap_items(items):
        parts.append(
            f'<text x="{RIGHT_X+17}" y="{y}" '
            f'class="body" font-size="12.3">{escape(line)}</text>'
        )
        y += 22

    return y + 19


def main():
    parts = []

    parts.append(
        f'''<svg xmlns="http://www.w3.org/2000/svg"
width="{WIDTH}" height="{BASE_HEIGHT}"
viewBox="0 0 {WIDTH} {BASE_HEIGHT}"
role="img" aria-labelledby="title desc">
<title id="title">Cory Pearl GitHub profile terminal</title>
<desc id="desc">Dark terminal profile with PCB ASCII art, Cory Pearl ASCII lettering, skills and GitHub statistics.</desc>
<style>
.bg{{fill:#0d1117}}
text{{font-family:"SFMono-Regular",Consolas,"Liberation Mono",Menlo,monospace;font-variant-ligatures:none}}
.ascii{{fill:#c9d1d9}}
.ascii2{{fill:#8b949e}}
.head{{fill:#f0883e;font-weight:700}}
.val{{fill:#79c0ff}}
.green{{fill:#7ee787}}
.muted{{fill:#8b949e}}
.body{{fill:#c9d1d9}}
.rule{{stroke:#30363d;stroke-width:1}}
</style>
<rect class="bg" width="{WIDTH}" height="{BASE_HEIGHT}" rx="10"/>'''
    )

    # Left-side ASCII placement
    parts.append(multiline_text(PCB_ASCII, 34, 18, 9.2, "ascii2", 7.8))
    parts.append(multiline_text(NAME_ASCII, 156, 395, 12.0, "ascii", 9.2))

    # Header
    parts.append(
        f'<text x="{RIGHT_X}" y="45" font-size="18" font-weight="700">'
        f'<tspan class="green">{escape(USERNAME)}</tspan>'
        f'<tspan class="muted">@</tspan>'
        f'<tspan class="val">{escape(HOST)}</tspan>'
        f'</text>'
    )
    parts.append(
        f'<line class="rule" x1="{RIGHT_X}" y1="60" '
        f'x2="{RIGHT_END_X}" y2="60"/>'
    )

    # Skills sections
    y = 92
    y = add_section(parts, "Software", SOFTWARE, y)
    y = add_section(parts, "Languages", LANGUAGES, y)
    y = add_section(parts, "Hardware", HARDWARE, y)

    # GitHub Stats
    parts.append(
        f'<text x="{RIGHT_X}" y="{y}" class="head" font-size="14">'
        f'- GitHub Stats</text>'
    )
    parts.append(
        f'<line class="rule" x1="{RIGHT_X+125}" y1="{y-5}" '
        f'x2="{RIGHT_END_X}" y2="{y-5}"/>'
    )

    y += 30
    parts.append(
        f'<text x="{RIGHT_X+17}" y="{y}" font-size="12.5">'
        f'<tspan class="head">● Repos</tspan>'
        f'<tspan class="muted"> ............ </tspan>'
        f'<tspan id="repo_data" class="val">{escape(REPOS)}</tspan>'
        f'</text>'
    )

    y += 26
    parts.append(
        f'<text x="{RIGHT_X+17}" y="{y}" font-size="12.5">'
        f'<tspan class="head">● Commits</tspan>'
        f'<tspan class="muted"> .......... </tspan>'
        f'<tspan id="commit_data" class="val">{escape(COMMITS)}</tspan>'
        f'</text>'
    )

    # Focus
    y += 42
    parts.append(
        f'<text x="{RIGHT_X}" y="{y}" class="head" font-size="14">- Focus</text>'
    )
    parts.append(
        f'<line class="rule" x1="{RIGHT_X+60}" y1="{y-5}" '
        f'x2="{RIGHT_END_X}" y2="{y-5}"/>'
    )

    y += 27
    for line in wrap_items(FOCUS):
        parts.append(
            f'<text x="{RIGHT_X+17}" y="{y}" class="body" '
            f'font-size="12.3">{escape(line)}</text>'
        )
        y += 22

    footer_rule_y = max(626, y + 7)
    footer_text_y = footer_rule_y + 30
    final_height = max(BASE_HEIGHT, footer_text_y + 20)

    parts.append(
        f'<line class="rule" x1="{RIGHT_X}" y1="{footer_rule_y}" '
        f'x2="{RIGHT_END_X}" y2="{footer_rule_y}"/>'
    )
    parts.append(
        f'<text x="{RIGHT_X}" y="{footer_text_y}" '
        f'class="green" font-size="12.5">{escape(TAGLINE)}</text>'
    )

    parts.append("</svg>")

    svg = "\n".join(parts)

    # Expand only when edited text requires more vertical room.
    if final_height != BASE_HEIGHT:
        svg = svg.replace(
            f'width="{WIDTH}" height="{BASE_HEIGHT}"',
            f'width="{WIDTH}" height="{final_height}"'
        )
        svg = svg.replace(
            f'viewBox="0 0 {WIDTH} {BASE_HEIGHT}"',
            f'viewBox="0 0 {WIDTH} {final_height}"'
        )
        svg = svg.replace(
            f'<rect class="bg" width="{WIDTH}" height="{BASE_HEIGHT}" rx="10"/>',
            f'<rect class="bg" width="{WIDTH}" height="{final_height}" rx="10"/>'
        )

    Path(OUTPUT_FILE).write_text(svg, encoding="utf-8")
    print(f"Generated: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
