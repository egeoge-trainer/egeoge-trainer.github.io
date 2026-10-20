import argparse
from pathlib import Path

import pypdfium2 as pdf


START_PAGES = [
    6, 11, 16, 21, 26, 31, 36, 41, 46, 51,
    56, 61, 66, 72, 77, 82, 87, 93, 98, 104,
    110, 115, 120, 125, 130, 135, 140, 145, 151, 157,
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", type=Path)
    args = parser.parse_args()

    root = Path("review/oge-social-2027/pages")
    root.mkdir(parents=True, exist_ok=True)
    document = pdf.PdfDocument(str(args.pdf))

    question_pages = range(START_PAGES[0], 162)
    answer_pages = range(162, len(document) + 1)
    for number in [*question_pages, *answer_pages]:
        target = root / f"page-{number:03d}.png"
        if not target.exists():
            document[number - 1].render(scale=3).to_pil().save(target)

    print(f"Rendered {len(document) - START_PAGES[0] + 1} source pages")


if __name__ == "__main__":
    main()
