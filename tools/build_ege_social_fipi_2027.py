import json
import re
from pathlib import Path

import numpy as np
from PIL import Image


ROOT = Path("review/ege-social-2027-fipi")
ASSETS = Path("assets/ege-social-fipi-2027")
TARGET = Path("ege-social-fipi-2027-interactive.js")
STARTS = [9, 18, 27, 36, 45, 53, 62, 71, 79, 88, 97, 105, 114, 123, 132, 140, 149, 158, 167, 176, 185, 194, 203, 212, 221, 230, 239, 247, 255, 264]
MATCH_TASKS = {3, 6, 13, 15}
MATCH_RIGHT_OVERRIDES = {
    (1, 3): ["Традиционное (аграрное) общество", "Индустриальное общество", "Постиндустриальное общество"],
    (18, 3): ["Академические права", "Обязанности"],
    (20, 3): ["Массовая культура", "Элитарная культура", "Народная культура"],
    (20, 6): ["Краткосрочные конкурентные преимущества", "Долгосрочные конкурентные преимущества"],
    (30, 13): ["Исключительное ведение Российской Федерации", "Совместное ведение Российской Федерации и субъектов Российской Федерации"],
}
OPTION_OVERRIDES = {
    (1, 9): [
        "Доля тех, кто предпочитает непродовольственные товары иностранного производства, среди 46-60-летних опрошенных больше, чем среди 18-30-летних опрошенных.",
        "Среди 18-30-летних опрошенных доля тех, кто не обращает внимания на то, где товар произведён, больше доли тех, кто предпочитает непродовольственные товары иностранного производства.",
        "Среди 18-30-летних опрошенных доля тех, кто предпочитает непродовольственные товары российского производства, больше доли тех, кто затруднился ответить.",
        "Одинаковые доли 46-60-летних опрошенных ответили, что предпочитают непродовольственные товары российского и иностранного производства.",
        "Страна-производитель не имеет значения для равных долей опрошенных обеих групп.",
    ],
}
MATCH_LEFT_OVERRIDES = {
    (29, 6): [
        "Водный налог",
        "Государственная пошлина",
        "Налог на добычу полезных ископаемых",
        "Налог на имущество организаций",
        "Налог на имущество физических лиц",
    ],
    (30, 13): [
        "Федеральная государственная собственность и управление ею",
        "Определение статуса и защита государственной границы",
        "Социальная защита, включая социальное обеспечение",
        "Кадры судебных и правоохранительных органов",
        "Адвокатура, нотариат",
    ],
}

ANSWERS_1_8 = [
    "45 135 23132 134 134 42313 1456 245",
    "36 145 21211 246 235 22111 2345 145",
    "35 124 12221 146 134 31122 134 235",
    "23 124 33123 234 134 12121 1246 345",
    "14 13 31422 123 134 12324 134 2345",
    "36 234 31232 456 245 23113 256 235",
    "56 135 34124 123 345 22111 236 124",
    "16 245 11212 246 345 31212 156 235",
    "23 345 21312 356 134 11122 15 12",
    "14 135 12123 125 125 11122 45 234",
    "36 234 32311 134 2345 12312 246 135",
    "34 345 24431 456 1345 12121 145 245",
    "35 1235 22211 246 125 12122 1345 245",
    "23 134 21211 123 145 12231 16 12",
    "14 245 12213 15 345 13322 156 14",
    "35 234 12112 456 1235 31232 124 135",
    "56 145 32311 125 125 11222 1256 125",
    "14 124 11222 256 235 23311 156 124",
    "46 124 11122 236 24 12212 235 134",
    "24 124 12321 256 135 11222 234 234",
    "46 234 11233 124 235 11221 1234 123",
    "15 345 22121 345 235 11222 2345 234",
    "16 135 12122 1346 125 21333 123 13",
    "12 234 11122 236 145 12212 1456 135",
    "16 134 24431 23 123 24123 456 15",
    "26 123 13223 246 135 22311 56 123",
    "36 1235 21122 356 45 12331 246 134",
    "34 1234 22112 456 345 12122 56 2345",
    "23 345 11221 15 234 11123 13 124",
    "12 145 21122 256 1345 23123 356 124",
]

ANSWERS_9_16 = [
    "23 234 345 15 21112 135 22113 126",
    "1234 34 235 134 32143 134 22111 245",
    "145 125 146 134 43241 145 23123 1236",
    "35 45 236 134 12122 2345 22312 145",
    "345 123 145 145 33123 124 33122 2456",
    "135 125 125 12 22212 135 22112 125",
    "124 134 1256 35 21212 134 21112 1236",
    "123 12 256 13 21121 125 22112 145",
    "124 12 2456 124 13213 135 21234 124",
    "135 234 356 1245 12213 135 11212 1256",
    "124 234 234 234 12211 145 31122 124",
    "245 1345 56 124 32421 123 11212 145",
    "1234 1245 1234 125 32213 145 23123 456",
    "124 134 25 13 22112 235 12212 16",
    "123 134 146 134 21231 145 12211 1246",
    "345 134 456 234 12212 345 13312 256",
    "234 245 1356 235 22112 145 21122 123",
    "235 123 346 135 23321 125 22211 156",
    "124 1235 245 134 32131 145 34121 135",
    "124 123 1235 12 23231 1234 12121 36",
    "1235 245 145 134 12122 234 21112 456",
    "234 345 56 134 12211 125 12211 456",
    "124 1234 1456 123 31232 1235 11221 246",
    "234 124 345 245 11112 124 13231 235",
    "245 145 456 235 12212 234 21121 456",
    "124 1345 236 345 23312 145 31323 1236",
    "345 345 245 125 11223 145 31212 136",
    "145 345 256 12 11232 145 12311 235",
    "345 245 3456 134 23213 2345 33212 125",
    "15 123 456 123 11222 123 23311 246",
]


def components(page_number):
    image = np.array(Image.open(ROOT / "pages" / f"page-{page_number:03d}.png").convert("L"))
    bitmap = image[:, 50:350] < 100
    seen = np.zeros(bitmap.shape, dtype=bool)
    boxes = []
    for y, x in zip(*np.where(bitmap)):
        if seen[y, x]:
            continue
        stack = [(int(y), int(x))]
        seen[y, x] = True
        points = []
        while stack:
            cy, cx = stack.pop()
            points.append((cy, cx))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = cy + dy, cx + dx
                if 0 <= ny < bitmap.shape[0] and 0 <= nx < bitmap.shape[1] and bitmap[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if len(points) < 100:
            continue
        ys = [point[0] for point in points]
        xs = [point[1] for point in points]
        width = max(xs) - min(xs) + 1
        height = max(ys) - min(ys) + 1
        if 78 <= width <= 95 and 47 <= height <= 58:
            boxes.append((min(ys), min(xs) + 50, width, height))
    # Watermarks occasionally touch a frame and turn it into a larger connected
    # component. Recover those frames from their parallel horizontal rules.
    rules = []
    rule_bitmap = image[:, 50:350] < 140
    for y in range(150, min(2350, rule_bitmap.shape[0])):
        indices = np.where(rule_bitmap[y])[0]
        for run in np.split(indices, np.where(np.diff(indices) > 1)[0] + 1):
            if 60 <= len(run) <= 120:
                rules.append((y, int(run[0]) + 50, int(run[-1]) + 50))
    grouped = []
    for rule in rules:
        if not grouped or rule[0] > grouped[-1][-1][0] + 1:
            grouped.append([rule])
        else:
            grouped[-1].append(rule)
    representatives = [max(group, key=lambda rule: rule[2] - rule[1]) for group in grouped]
    for index, upper in enumerate(representatives):
        for lower in representatives[index + 1:]:
            gap = lower[0] - upper[0]
            overlap = min(upper[2], lower[2]) - max(upper[1], lower[1])
            candidate_width = max(upper[2], lower[2]) - min(upper[1], lower[1]) + 1
            if 47 <= gap <= 55 and overlap > 50 and 75 <= candidate_width <= 95:
                boxes.append((upper[0], min(upper[1], lower[1]), candidate_width, gap + 1))
                break
            if gap > 60:
                break
    unique = []
    for box in sorted(boxes):
        if not unique or abs(box[0] - unique[-1][0]) > 8:
            unique.append(box)
    return unique


def task_boundaries(variant):
    start = STARTS[variant - 1]
    end = STARTS[variant] - 1 if variant < 30 else 271
    candidates = []
    for page in range(start, end + 1):
        page_boxes = components(page)
        # The diagonal publisher watermark can break the frame around tasks 1
        # and 9. Their opening phrases are stable enough to restore the frame.
        for line in lines(page):
            phrase = clean(" ".join(word["text"] for word in line["words"]))
            if phrase.startswith("Ниже приведён ряд") or phrase.startswith("В ходе социолог"):
                y = line["bbox"]["y0"] - 8
                if not any(abs(box[0] - y) < 100 for box in page_boxes):
                    page_boxes.append((y, max(55, line["bbox"]["x0"] - 115), 90, 52))
        candidates.extend((page, *box) for box in sorted(page_boxes))
    if len(candidates) < 16:
        raise RuntimeError(f"Variant {variant}: only {len(candidates)} task boxes")
    return candidates[:16]


def lines(page_number):
    rows = (ROOT / "tsv" / f"page-{page_number:03d}.tsv").read_text(encoding="utf-8").splitlines()[1:]
    grouped = {}
    for row in rows:
        fields = row.split("\t")
        if len(fields) < 12 or fields[0] != "5" or not fields[11].strip():
            continue
        key = tuple(fields[1:5])
        left, top, width, height = map(int, fields[6:10])
        grouped.setdefault(key, []).append({
            "text": fields[11].strip(),
            "bbox": {"x0": left, "y0": top, "x1": left + width, "y1": top + height},
        })
    result = []
    for words in grouped.values():
        words.sort(key=lambda word: word["bbox"]["x0"])
        result.append({
            "words": words,
            "bbox": {
                "x0": min(word["bbox"]["x0"] for word in words),
                "y0": min(word["bbox"]["y0"] for word in words),
                "x1": max(word["bbox"]["x1"] for word in words),
                "y1": max(word["bbox"]["y1"] for word in words),
            },
        })
    return sorted(result, key=lambda line: (line["bbox"]["y0"], line["bbox"]["x0"]))


def clean(value):
    value = value.replace("—", "-").replace("`", "").replace("©", "")
    value = re.sub(r"(?<=\w)-\s+(?=\w)", "-", value)
    value = re.sub(r"\s+", " ", value)
    value = re.sub(r"\b83\)", "3)", value)
    value = re.sub(r"\b8\)", "3)", value)
    value = re.sub(r"\b56\)", "5)", value)
    value = re.sub(r"\b65\)", "5)", value)
    value = re.sub(r"\s+(?:АУ|КУ|Фо|[АКС])\s*$", "", value)
    value = re.sub(r"\s*[<>&®\\|]+[^\s]*\s*$", "", value)
    value = re.sub(r"\s+\([0-9]\s*$", "", value)
    value = re.sub(r"\s+«[^А-Яа-яA-Za-z0-9]*$", "", value)
    return value.strip(" ,;:.|'\\")


def region_text(boundary, next_boundary):
    page, top, left, width, height = boundary
    selected = []
    final_page = next_boundary[0] if next_boundary else page
    for current_page in range(page, final_page + 1):
        page_top = top if current_page == page else 240
        page_bottom = next_boundary[1] if next_boundary and current_page == next_boundary[0] else 2290
        cutoff = left + width + 15 if current_page == page else 230
        for line in lines(current_page):
            box = line["bbox"]
            center = (box["y0"] + box["y1"]) / 2
            if page_top <= center < page_bottom and box["x1"] > cutoff:
                words = [word["text"] for word in line["words"] if word["bbox"]["x1"] > cutoff]
                if words:
                    selected.append(" ".join(words))
    text = "\n".join(selected)
    text = re.split(r"(?im)^\s*(?:Ответ|Отве[мт]|Не забудьте|Часть 2)\b", text, maxsplit=1)[0]
    text = re.sub(r"(?im)^.*(?:Копирование|Издательство|ТИПОВЫЕ ЭКЗАМЕНАЦИОННЫЕ|ВАРИАНТ \d+).*$", "", text)
    return clean(text)


def region_lines(boundary, next_boundary):
    page, top, left, width, height = boundary
    bottom = next_boundary[1] if next_boundary and next_boundary[0] == page else 2290
    cutoff = left + width + 15
    return [
        line for line in lines(page)
        if top <= (line["bbox"]["y0"] + line["bbox"]["y1"]) / 2 < bottom
        and line["bbox"]["x1"] > cutoff
    ]


def matching_question(variant, task, boundary, next_boundary, answer):
    source_lines = region_lines(boundary, next_boundary)
    words = [word for line in source_lines for word in line["words"]]
    stop_y = next(
        (line["bbox"]["y0"] for line in source_lines if "Запишите в таблицу" in clean(" ".join(word["text"] for word in line["words"]))),
        max(word["bbox"]["y1"] for word in words),
    )
    words = [word for word in words if word["bbox"]["y0"] < stop_y]
    right_markers = [
        word for word in words
        if re.fullmatch(r"(?:[1-4]|8|83)\)", word["text"].replace(" ", ""))
        and word["bbox"]["x0"] > 700
    ]
    manual_right = MATCH_RIGHT_OVERRIDES.get((variant, task))
    if not right_markers and not manual_right:
        raise RuntimeError("Matching table right column not found")
    split_x = min(word["bbox"]["x0"] for word in right_markers) - 12 if right_markers else 1000

    def column_text(right):
        rows = []
        for line in source_lines:
            if line["bbox"]["y0"] >= stop_y:
                continue
            selected = [
                word["text"] for word in line["words"]
                if (word["bbox"]["x0"] >= split_x) == right
            ]
            if selected:
                rows.append(" ".join(selected))
        return clean("\n".join(rows))

    left_text = column_text(False)
    right_text = column_text(True)
    left_matches = list(re.finditer(r"(?<!\w)([АБВГД])\)\s*", left_text))
    manual_left = MATCH_LEFT_OVERRIDES.get((variant, task))
    if len(left_matches) < 5 and not manual_left:
        raise RuntimeError("Matching table rows not found")

    if manual_left:
        left = manual_left
    else:
        left = []
        for index, match in enumerate(left_matches[:5]):
            end = left_matches[index + 1].start() if index + 1 < 5 else len(left_text)
            left.append(clean(left_text[match.end():end]))
    maximum = max(int(char) for char in answer)
    if manual_right:
        right = manual_right
    else:
        marker_x = min(word["bbox"]["x0"] for word in right_markers)
        marker_y = min(word["bbox"]["y0"] for word in right_markers)
        groups = []
        for line in source_lines:
            row = [word for word in line["words"] if word["bbox"]["x0"] >= split_x]
            if not row or line["bbox"]["y1"] < marker_y or line["bbox"]["y0"] >= stop_y:
                continue
            if row[0]["bbox"]["x0"] <= marker_x + 35:
                groups.append([])
            if groups:
                groups[-1].extend(word["text"] for word in row)
        right = []
        for group in groups[:maximum]:
            while group and len(re.sub(r"\W", "", group[0])) <= 3:
                group.pop(0)
            right.append(clean(" ".join(group)))
    if len(left) != 5 or len(right) < maximum:
        raise RuntimeError(f"Incomplete matching table: {len(left)} x {len(right)}")
    return {
        "type": "match",
        "text": "Установите соответствие: к каждой позиции первого столбца подберите позицию из второго столбца.",
        "left": left,
        "right": right,
        "correct": [int(char) - 1 for char in answer],
    }


def choice_question(text, answer):
    matches = list(re.finditer(r"(?<!\d)([1-6]|8|83)\s*\)\s*", text))
    numbered = []
    for match in matches:
        number = int(match.group(1))
        numbered.append((3 if number in (8, 83) else number, match))
    if not any(number == 5 for number, _ in numbered):
        sixes = [index for index, (number, _) in enumerate(numbered) if number == 6]
        if len(sixes) >= 2:
            index = sixes[0]
            numbered[index] = (5, numbered[index][1])
    first_one = next((index for index, item in enumerate(numbered) if item[0] == 1), None)
    if first_one is None:
        raise RuntimeError(f"Could not find answer options in: {text[:160]}")
    numbered = numbered[first_one:]
    values = {}
    for index, (number, match) in enumerate(numbered):
        end = numbered[index + 1][1].start() if index + 1 < len(numbered) else len(text)
        option = re.split(r"\b(?:Найдите|Запишите)\b", text[match.end():end], maxsplit=1)[0]
        values.setdefault(number, clean(option))
    maximum = max(values, default=0)
    if maximum < 4 or sorted(values) != list(range(1, maximum + 1)):
        raise RuntimeError(f"Could not find answer options in: {text[:160]}")
    options = [values[number] for number in range(1, maximum + 1)]
    stem = clean(text[:numbered[0][1].start()])
    if "Найдите в приведённом списке выводы" in text:
        stem = clean(text[: text.index("Найдите в приведённом списке выводы") + len("Найдите в приведённом списке выводы, которые можно сделать на основе диаграммы.")])
    return {"type": "multi", "text": stem, "options": options, "correct": [int(char) - 1 for char in answer]}


def crop_task(variant, task, boundary, next_boundary):
    page, top, left, width, height = boundary
    bottom = next_boundary[1] - 8 if next_boundary and next_boundary[0] == page else 2260
    source = Image.open(ROOT / "pages" / f"page-{page:03d}.png").convert("RGB")
    crop = source.crop((max(85, left - 15), max(160, top - 8), 1685, min(bottom, 2320)))
    folder = ASSETS / f"variant-{variant:02d}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"task-{task:02d}.webp"
    crop.save(path, "WEBP", quality=88, method=6)
    return f"./{path.as_posix()}"


def chart_question_text(text):
    instruction = re.search(r"Найдите в приведённом списке выводы", text)
    intro = re.split(r"Полученные результаты|Результаты опроса", text, maxsplit=1)[0]
    if instruction:
        tail = text[instruction.start():]
    else:
        first_option = re.search(r"(?<!\d)1\s*\)\s*", text)
        if not first_option:
            raise RuntimeError("Chart conclusions and options not found")
        tail = "Найдите выводы, которые можно сделать на основе диаграммы. " + text[first_option.start():]
    return clean(intro + " Полученные результаты представлены на диаграмме. " + tail)


def crop_chart(variant, boundary, next_boundary):
    page, top, left, width, height = boundary
    source_lines = region_lines(boundary, next_boundary)
    result_line = next(
        (line for line in source_lines if "представлены" in clean(" ".join(word["text"] for word in line["words"])).lower()
         or "приведены на диаграмме" in clean(" ".join(word["text"] for word in line["words"])).lower()),
        None,
    )
    instruction_line = next(
        (line for line in source_lines if "Найдите в приведённом списке выводы" in clean(" ".join(word["text"] for word in line["words"]))),
        None,
    )
    if not instruction_line:
        instruction_line = next(
            (line for line in source_lines
             if line["bbox"]["y0"] > (result_line["bbox"]["y1"] if result_line else 0)
             and re.search(r"(?<!\d)1\s*\)", clean(" ".join(word["text"] for word in line["words"])))),
            None,
        )
    if not result_line:
        raise RuntimeError(f"Chart crop bounds not found for variant {variant}")
    if instruction_line and instruction_line["bbox"]["y0"] > result_line["bbox"]["y1"]:
        bottom = instruction_line["bbox"]["y0"] - 8
    elif next_boundary and next_boundary[0] > page:
        bottom = 2265
    else:
        raise RuntimeError(f"Chart crop bounds not found for variant {variant}")
    source = Image.open(ROOT / "pages" / f"page-{page:03d}.png").convert("RGB")
    crop = source.crop((235, result_line["bbox"]["y1"] + 8, 1680, bottom))
    folder = ASSETS / f"variant-{variant:02d}"
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / "task-09.webp"
    crop.save(path, "WEBP", quality=90, method=6)
    return f"./{path.as_posix()}"


def main():
    answers = [left.split() + right.split() for left, right in zip(ANSWERS_1_8, ANSWERS_9_16)]
    variants = []
    audit = []
    for variant in range(1, 31):
        boundaries = task_boundaries(variant)
        questions = []
        for index, boundary in enumerate(boundaries):
            task = index + 1
            if index + 1 < 16:
                next_boundary = boundaries[index + 1]
            else:
                end_page = STARTS[variant] - 1 if variant < 30 else 271
                next_boundary = (end_page, 2290, 0, 0, 0)
            answer = answers[variant - 1][index]
            text = region_text(boundary, next_boundary)
            if task in MATCH_TASKS:
                try:
                    question = matching_question(variant, task, boundary, next_boundary, answer)
                except RuntimeError as error:
                    raise RuntimeError(f"Variant {variant}, task {task}: {error}") from error
            else:
                try:
                    question = choice_question(chart_question_text(text) if task == 9 else text, answer)
                except RuntimeError as error:
                    (ROOT / "failed-task.txt").write_text(f"{variant}.{task}\n{text}", encoding="utf-8")
                    raise RuntimeError(f"Variant {variant}, task {task}: {error}") from error
                if task == 9:
                    if (variant, task) in OPTION_OVERRIDES:
                        question["options"] = OPTION_OVERRIDES[(variant, task)]
                    question["image"] = crop_chart(variant, boundary, next_boundary)
                    question["isChart"] = True
                    question["alt"] = f"Диаграмма и условия задания 9 варианта {variant}"
            question.update(
                sourceVariant=variant,
                sourceTask=task,
                explanation=f"Эталон из таблицы ответов: {answer}.",
            )
            questions.append(question)
            audit.append(f"{variant}.{task} {question['type']} {answer} {question['text'][:100]}")
        variants.append({"id": f"ege-social-fipi-2027-v{variant}", "title": f"Вариант {variant}", "questions": questions})
        print(f"variant {variant}: 16 tasks")

    source = {
        "subjectId": "social",
        "id": "ege-social-fipi-2027",
        "title": "Тренировочные варианты",
        "year": "2027",
        "description": "Котова-Лискова · 2027 · первая часть",
        "authorLine": "Котова-Лискова · 2027 · первая часть",
        "variants": variants,
    }
    TARGET.write_text(
        "window.localInteractiveSources = window.localInteractiveSources || [];\n"
        "window.localInteractiveSources.push(" + json.dumps(source, ensure_ascii=False, indent=2) + ");\n",
        encoding="utf-8",
    )
    (ROOT / "build-audit.txt").write_text("\n".join(audit), encoding="utf-8")


if __name__ == "__main__":
    main()
