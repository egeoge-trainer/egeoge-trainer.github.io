from pathlib import Path

import numpy as np
from PIL import Image, ImageOps


ROOT = Path("review/ege-social-2027-fipi")
PAGES = (272, 273)


def groups(values):
    chunks = np.split(values, np.where(np.diff(values) > 1)[0] + 1)
    return [(int(chunk[0]), int(chunk[-1])) for chunk in chunks if len(chunk)]


for page_number in PAGES:
    source = Image.open(ROOT / "pages" / f"page-{page_number}.png").convert("L")
    pixels = np.array(source)
    ink = pixels < 170
    x_lines = groups(np.where(ink.sum(axis=0) > 1000)[0])
    y_lines = groups(np.where(ink.sum(axis=1) > 1000)[0])

    x_edges = [round((start + end) / 2) for start, end in x_lines[:10]]
    y_edges = [round((start + end) / 2) for start, end in y_lines]
    # The first two horizontal rules belong to the two-row header.
    data_edges = y_edges[2:33]
    if len(x_edges) != 10 or len(data_edges) != 31:
        raise RuntimeError(
            f"Unexpected answer grid on page {page_number}: "
            f"{len(x_edges)} columns, {len(data_edges) - 1} rows"
        )

    row_width = 9 * 260
    row_height = 92
    montage = Image.new("L", (row_width, 30 * row_height), 255)
    for row in range(30):
        for column in range(9):
            cell = source.crop(
                (
                    x_edges[column] + 5,
                    data_edges[row] + 4,
                    x_edges[column + 1] - 5,
                    data_edges[row + 1] - 4,
                )
            )
            cell = ImageOps.autocontrast(cell)
            cell.thumbnail((220, 70), Image.Resampling.LANCZOS)
            left = column * 260 + (260 - cell.width) // 2
            top = row * row_height + (row_height - cell.height) // 2
            montage.paste(cell, (left, top))

    montage.save(ROOT / f"answers-{page_number}-cells.png")
    print(f"page {page_number}: {len(x_edges) - 1} columns x {len(data_edges) - 1} rows")
