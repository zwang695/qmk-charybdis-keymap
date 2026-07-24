#!/usr/bin/env python3
"""Render the Charybdis keymap as a dependency-free SVG."""

from html import escape
from pathlib import Path

LAYERS = {
    "Base": """
DRG_TOG DPI- DPI+ BTN2 BTN1 Cmd-C Cmd-V Left Right + - NO
Tab Q W E R T Y U I O P \\
Esc A S D F G H J K L ; '
Magic Z X C V B N M , . / CAPS
BSPC SFT SYM NUM ENT NO SPACE LLCK
""",
    "Symbol": """
TRNS ` < > - | ^ { } $ ARROW TRNS
TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS
TRNS ! * / = & # ( ) ; \" TRNS
TRNS ~ + [ ] % @ : ' _ ? TRNS
TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS
""",
    "Cursor": """
TRNS TRNS Cmd-R PrevTab NextTab Cmd-[ Cmd-] PgUp Home Up End Search
TRNS TRNS TRNS TRNS TRNS TRNS PgDn Left Down Right TRNS TRNS
TRNS LCTL LALT LGUI LSFT Click TRNS Left Down Right TRNS TRNS
TRNS Undo Redo Cmd-C Cmd-V Redo Cmd-L SelBack SelWord SelLine TRNS TRNS
TRNS TRNS TRNS TRNS TRNS TRNS Cmd-Tab LLCK
""",
    "Number": """
Esc F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11
TRNS / 9 8 7 * TRNS TRNS [ ] TRNS F12
TRNS - 3 2 1 + TRNS RSFT RGUI RALT RCTL TRNS
TRNS X 6 5 4 % TRNS TRNS , . TRNS TRNS
0 TRNS TRNS TRNS TRNS TRNS LLCK TRNS
""",
    "Magic": """
TRNS RM_TOG QK_KB RM_NEXT RGB RM_VALD RM_VALU Red Green Blue Purple TRNS
TRNS PrevTrack NextTrack Stop Play TRNS TRNS TRNS TRNS TRNS TRNS TRNS
TRNS Vol- Vol+ Mute TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS
TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS Boot
TRNS TRNS TRNS TRNS TRNS TRNS TRNS TRNS
""",
}

COLORS = ["#d9e8ff", "#e6dcff", "#d9f2df", "#fff0c9", "#ffe0e8"]


def layer_keys(text: str) -> list[str]:
    keys = text.split()
    if len(keys) != 56:
        raise ValueError(f"expected 56 keys, got {len(keys)}")
    return keys


def render(output: Path) -> None:
    width = 867
    panel_height = 455
    height = 40 + panel_height * len(LAYERS)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#172033} .title{font-size:18px;font-weight:700} .label{font-size:11px;font-weight:600;fill:#64748b} .key{font-size:9px;font-weight:600} .outer{fill:#c8cdd3;stroke:#111;stroke-width:1.5} .inner{stroke:rgba(0,0,0,.15);stroke-width:1}</style>',
        '<rect width="100%" height="100%" fill="#eef0f2"/>',
    ]
    key_w = key_h = 52
    left_x = [28, 82, 136, 190, 244, 298]
    right_x = [514, 568, 622, 676, 730, 784]
    row_y = [21.25, 75.25, 129.25, 183.25]

    def draw_key(parts: list[str], x: float, y: float, key: str, fill: str, angle: float = 0, pivot: tuple[float, float] | None = None) -> None:
        pivot = pivot or (x + key_w / 2, y + key_h / 2)
        transform = f' transform="rotate({angle} {pivot[0]} {pivot[1]})"' if angle else ""
        parts.append(f'<g{transform}><rect class="outer" x="{x}" y="{y}" width="{key_w}" height="{key_h}" rx="5"/>')
        parts.append(f'<rect class="inner" x="{x + 6}" y="{y + 3}" width="40" height="40" rx="5" fill="{fill}"/>')
        shown = escape(key)
        parts.append(f'<text class="key" x="{x + key_w / 2}" y="{y + 27}" text-anchor="middle">{shown}</text></g>')

    for layer_index, (name, text) in enumerate(LAYERS.items()):
        y0 = 24 + layer_index * panel_height
        parts.append(f'<text class="title" x="28" y="{y0 + 20}">{escape(name)}</text>')
        keys = layer_keys(text)
        for index, key in enumerate(keys[:48]):
            row, col = divmod(index, 12)
            x = left_x[col] if col < 6 else right_x[col - 6]
            y = y0 + 36 + row_y[row]
            draw_key(parts, x, y, key, COLORS[layer_index])

        # Coordinates and rotations follow zzkt/charybdis's KLE-style layout.
        thumb_y = y0 + 36
        thumbs = keys[48:]
        for key, x, y in zip(thumbs[:3], [284.5, 338.5, 392.5], [thumb_y + 235, thumb_y + 235, thumb_y + 235]):
            draw_key(parts, x, y, key, COLORS[layer_index], 30, (351, thumb_y + 193.5))
        for key, x in zip(thumbs[3:5], [446.5, 500.5]):
            draw_key(parts, x, thumb_y + 140.5, key, COLORS[layer_index], -30, (702, thumb_y + 193.5))
        for key, x in zip(thumbs[5:7], [338.5, 392.5]):
            draw_key(parts, x, thumb_y + 289.5, key, COLORS[layer_index], 30, (351, thumb_y + 193.5))
        for key in thumbs[7:]:
            draw_key(parts, 446.5, thumb_y + 194.5, key, COLORS[layer_index], -30, (702, thumb_y + 193.5))
        parts.append(f'<circle cx="635" cy="{thumb_y + 194.5}" r="27" fill="#b51f4f" stroke="#333" stroke-width="2"/>')
        parts.append(f'<text class="label" x="635" y="{thumb_y + 199}" text-anchor="middle" fill="white">trackball</text>')
        parts.append(f'<text class="label" x="28" y="{y0 + 438}">Left half ←   •   → Right half</text>')
    parts.append("</svg>")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render(Path(__file__).resolve().parents[1] / "docs" / "keymap.svg")
