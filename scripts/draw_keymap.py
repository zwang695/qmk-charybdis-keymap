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
    width = 1660
    panel_height = 300
    height = 40 + panel_height * len(LAYERS)
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        '<style>text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;fill:#172033} .title{font-size:24px;font-weight:700} .label{font-size:14px;font-weight:600} .key{font-size:13px} .muted{fill:#64748b}</style>',
        '<rect width="100%" height="100%" fill="#f8fafc"/>',
    ]
    key_w, key_h, gap = 116, 42, 7
    left = 28
    for layer_index, (name, text) in enumerate(LAYERS.items()):
        y0 = 24 + layer_index * panel_height
        parts.append(f'<text class="title" x="{left}" y="{y0 + 24}">{escape(name)}</text>')
        keys = layer_keys(text)
        for index, key in enumerate(keys[:48]):
            row, col = divmod(index, 12)
            x = left + col * (key_w + gap)
            y = y0 + 40 + row * (key_h + gap)
            if col == 6:
                x += 30
            parts.append(f'<rect x="{x}" y="{y}" width="{key_w}" height="{key_h}" rx="7" fill="{COLORS[layer_index]}" stroke="#94a3b8"/>')
            parts.append(f'<text class="key" x="{x + key_w / 2}" y="{y + 26}" text-anchor="middle">{escape(key)}</text>')
        thumbs = keys[48:]
        thumb_positions = [5, 6, 7, 9, 10, 11, 12, 13]
        for key, pos in zip(thumbs, thumb_positions):
            x = left + pos * (key_w + gap) + (30 if pos >= 6 else 0)
            y = y0 + 40 + 4 * (key_h + gap)
            parts.append(f'<rect x="{x}" y="{y}" width="{key_w}" height="{key_h}" rx="7" fill="{COLORS[layer_index]}" stroke="#94a3b8"/>')
            parts.append(f'<text class="key" x="{x + key_w / 2}" y="{y + 26}" text-anchor="middle">{escape(key)}</text>')
        parts.append(f'<text class="label muted" x="{left}" y="{y0 + 286}">Left half ←   •   → Right half</text>')
    parts.append("</svg>")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text("\n".join(parts) + "\n", encoding="utf-8")


if __name__ == "__main__":
    render(Path(__file__).resolve().parents[1] / "docs" / "keymap.svg")
