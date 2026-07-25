#!/usr/bin/env python3
"""Overlay the Charybdis keymap on the KLE-style physical geometry template."""

from html import escape
from pathlib import Path

LAYERS = {
    "Base": """
+ 1 2 3 4 5 6 7 8 9 0 -
Tab Q W E R T Y U I O P \\
Esc A/CTL S/OPT D/CMD F/SYM G H J/SYM K/CMD L/OPT ;/CTL '
Magic Z X C V B N M , . / CAPS
BSPC/CUR SFT NO ENT SPACE/NUM NO NO NO
""",
    "Symbol": """
▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽
▽ ` < > - | ^ { } $ -> ▽
▽ ! * / = & # ( ) ; \" ▽
▽ ~ + [ ] % @ : ' _ ? ▽
▽ ▽ ▽ ▽ ▽ ▽ ▽ ▽
""",
    "Cursor": """
▽ ▽ Cmd-R PrevTab NextTab Cmd-[ Cmd-] PgUp Home Up End SearchSel
▽ ▽ ▽ ▽ ▽ ▽ PgDn Left Down Right ▽ ▽
▽ LCTL LALT LGUI LSFT Click ▽ Left Down Right ▽ ▽
▽ Cmd-Z Redo Cmd-C Cmd-V CmdShiftV Cmd-L SelBack SelWord SelLine ▽ ▽
▽ ▽ ▽ ▽ ▽ CycleTab Lock
""",
    "Num": """
Esc F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11
▽ / 9 8 7 * ▽ ▽ [ ] ▽ F12
▽ - 3 2 1 + ▽ RSFT RGUI RALT RCTL ▽
▽ X 6 5 4 % ▽ ▽ , . ▽ ▽
0 ▽ ▽ ▽ ▙ ▙ ▙ ▙
""",
    "Magic": """
▽ ▙ QK-KB RM-NEXT RGB-SLD RM-VALD RM-VALU HSV-0-0-255 HSV-0-255-255 HSV-74-255-255 HSV-169-255-255 ▽
▽ MediaPrev MediaNext MediaStop MediaPlay ▽ ▽ ▙ ▙ ▙ ▙ ▙ ▙
▽ VolDown VolUp Mute ▙ ▙ ▙ ▙ ▙ ▙ ▙ ▙ ▙
▽ ▙ ▙ ▙ ▙ ▙ ▙ ▙ ▙ ▙ ▙ QK-BOOT
▽ ▙ ▙ ▙ ▙ ▙ ▙ ▙
""",
}

KEY_W = 52
KEY_H = 52
TRANSLATE_X = 15
TRANSLATE_Y = 15


def labels(text: str) -> list[str]:
    result = text.split()
    if len(result) == 55:  # Cursor's thumb cluster has one additional transparent key.
        result.insert(48, "▽")
    elif len(result) == 58:  # Keep Magic's four matrix rows at twelve keys each.
        del result[24]
        del result[36]
    if len(result) != 56:
        raise ValueError(f"expected 56 labels, got {len(result)}")
    return result


def text_element(x: float, y: float, value: str, angle: float = 0, pivot: tuple[float, float] | None = None) -> str:
    pivot = pivot or (x, y)
    transform = f' transform="rotate({angle} {pivot[0]} {pivot[1]})"' if angle else ""
    size = 8 if len(value) > 5 else 10
    return f'<text x="{x}" y="{y}" text-anchor="middle" dominant-baseline="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="{size}" font-weight="600" fill="#172033"{transform}>{escape(value)}</text>'


def render(output: Path) -> None:
    template = (output.parent / "physical_layout.svg").read_text(encoding="utf-8")
    template_body = template[template.index(">") + 1 : template.rindex("</svg>")]
    section_height = 455
    height = section_height * len(LAYERS) - 20
    template = template.replace("height='435.35477246198917px'", f"height='{height}px'")
    template = template.replace("viewBox='0 0 867 435.35477246198917'", f"viewBox='0 0 867 {height}'")
    overlay: list[str] = []
    left_x = [28, 82, 136, 190, 244, 298]
    right_x = [514, 568, 622, 676, 730, 784]
    left_y = [
        [47.25, 47.25, 33.75, 27, 33.75, 40.5],
        [101.25, 101.25, 87.75, 81, 87.75, 94.5],
        [155.25, 155.25, 141.75, 135, 141.75, 148.5],
        [209.25, 209.25, 195.75, 189, 195.75, 202.5],
    ]
    right_y = [
        [40.5, 33.75, 27, 33.75, 47.25, 47.25],
        [94.5, 87.75, 81, 87.75, 101.25, 101.25],
        [148.5, 141.75, 135, 141.75, 155.25, 155.25],
        [202.5, 195.75, 189, 195.75, 209.25, 209.25],
    ]

    for layer_index, (layer_name, layer_text) in enumerate(LAYERS.items()):
        offset = layer_index * section_height
        overlay.append(f'<g transform="translate(0,{offset})">')
        overlay.append(template_body)
        overlay.append(f'<g transform="translate(15,15)" aria-label="Zachary Charybdis {layer_name} layer">')
        keys = labels(layer_text)

        for index, key in enumerate(keys[:48]):
            row, col = divmod(index, 12)
            x = (left_x if col < 6 else right_x)[col if col < 6 else col - 6] + KEY_W / 2
            y = (left_y if col < 6 else right_y)[row][col if col < 6 else col - 6]
            overlay.append(text_element(x, y, key))

        thumbs = keys[48:]
        left_pivot = (351, 229.5)
        right_pivot = (702, 229.5)
        for key, x in zip(thumbs[:3], [284.5, 338.5, 392.5]):
            overlay.append(text_element(x + 26, 297, key, 30, left_pivot))
        for key, x in zip(thumbs[3:5], [446.5, 500.5]):
            overlay.append(text_element(x + 26, 202.5, key, -30, right_pivot))
        for key, x in zip(thumbs[5:7], [338.5, 392.5]):
            overlay.append(text_element(x + 26, 351, key, 30, left_pivot))
        overlay.append(text_element(446.5 + 26, 256.5, thumbs[7], -30, right_pivot))
        overlay.append('</g>')
        overlay.append(f'<text x="20" y="420" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="11" fill="#64748b">Zachary · Charybdis 4x6 · {escape(layer_name)}</text>')
        overlay.append('</g>')

    output.write_text(template.replace('</svg>', '\n'.join(overlay) + '\n</svg>'), encoding='utf-8')


if __name__ == "__main__":
    render(Path(__file__).resolve().parents[1] / "docs" / "keymap.svg")
