#!/usr/bin/env python3
"""Overlay the Charybdis keymap on the KLE-style physical geometry template."""

from html import escape
from pathlib import Path

BASE = """
+ 1 2 3 4 5 6 7 8 9 0 -
Tab Q W E R T Y U I O P \\
Esc A S D F G H J K L ; '
Magic Z X C V B N M , . / CAPS
BSPC SFT SYM NUM ENT NO SPACE LLCK
"""

KEY_W = 52
KEY_H = 52
TRANSLATE_X = 15
TRANSLATE_Y = 15


def labels(text: str) -> list[str]:
    result = text.split()
    if len(result) != 56:
        raise ValueError(f"expected 56 labels, got {len(result)}")
    return result


def text_element(x: float, y: float, value: str, angle: float = 0, pivot: tuple[float, float] | None = None) -> str:
    pivot = pivot or (x, y)
    transform = f' transform="rotate({angle} {pivot[0]} {pivot[1]})"' if angle else ""
    size = 8 if len(value) > 5 else 10
    return f'<text x="{x}" y="{y}" text-anchor="middle" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="{size}" font-weight="600" fill="#172033"{transform}>{escape(value)}</text>'


def render(output: Path) -> None:
    template = (output.parent / "physical_layout.svg").read_text(encoding="utf-8")
    overlay: list[str] = [
        '<g transform="translate(15,15)" aria-label="Zachary Charybdis base layer">',
    ]
    keys = labels(BASE)
    left_x = [28, 82, 136, 190, 244, 298]
    right_x = [514, 568, 622, 676, 730, 784]
    row_y = [21.25, 75.25, 129.25, 183.25]

    for index, key in enumerate(keys[:48]):
        row, col = divmod(index, 12)
        x = (left_x if col < 6 else right_x)[col if col < 6 else col - 6] + KEY_W / 2
        y = row_y[row] + 29
        overlay.append(text_element(x, y, key))

    thumbs = keys[48:]
    left_pivot = (351, 229.5)
    right_pivot = (702, 229.5)
    for key, x in zip(thumbs[:3], [284.5, 338.5, 392.5]):
        overlay.append(text_element(x + 26, 271 + 29, key, 30, left_pivot))
    for key, x in zip(thumbs[3:5], [446.5, 500.5]):
        overlay.append(text_element(x + 26, 176.5 + 29, key, -30, right_pivot))
    for key, x in zip(thumbs[5:7], [338.5, 392.5]):
        overlay.append(text_element(x + 26, 325 + 29, key, 30, left_pivot))
    overlay.append(text_element(446.5 + 26, 230.5 + 29, thumbs[7], -30, right_pivot))
    overlay.append('</g>')
    overlay.append('<text x="20" y="420" font-family="-apple-system,BlinkMacSystemFont,Segoe UI,sans-serif" font-size="11" fill="#64748b">Zachary · Charybdis 4x6 · Base</text>')
    output.write_text(template.replace('</svg>', '\n'.join(overlay) + '\n</svg>'), encoding='utf-8')


if __name__ == "__main__":
    render(Path(__file__).resolve().parents[1] / "docs" / "keymap.svg")
