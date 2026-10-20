import json
import re
from copy import deepcopy
from difflib import SequenceMatcher
from pathlib import Path

import build_oge as base


START_PAGES = [
    6, 11, 16, 21, 26, 31, 36, 41, 46, 51,
    56, 61, 66, 72, 77, 82, 87, 93, 98, 104,
    110, 115, 120, 125, 130, 135, 140, 145, 151, 157,
]
SELECTED = [2, 3, 4, 5, 6, 9, 10, 11, 13, 14, 15, 16]

SHORT_KEYS = [
    ["патриотизм"],
    ["учитель", "преподаватель", "педагог"],
    ["экономическая"], ["отпуск"], ["личность"], ["объект"],
    ["верховенство"], ["юридические"], ["потребитель"],
    ["экономические", "материальные"], ["земля"], ["розничная"],
    ["труд"], ["театр"], ["скульптура", "архитектура"], ["массовая"],
    ["уголовная"], ["акция"], ["идеальные", "духовные"], ["милосердие"],
    ["суверенитет"], ["учение", "учёба", "учеба"], ["трудовые"], ["гимн"],
    ["информационные"], ["владение"], ["оппозиционная"],
    ["федерация", "федеративное"], ["социальные"], ["монархия"],
]

SHORT_TEXTS = [
    "Заполните пропуск в таблице. Какая общественная ценность означает чувство любви и преданности Отечеству, готовность подчинить частные интересы интересам страны?",
    "Заполните пропуск в таблице. Как называют специалиста, который занимается обучением и воспитанием детей, а также профессиональной подготовкой взрослых?",
    "Заполните пропуск в таблице. Какая сфера общества связана с производством, распределением, обменом и потреблением благ и услуг?",
    "Заполните пропуск в таблице. Как называют временное освобождение от работы на определённый период для отдыха с сохранением места работы?",
    "Заполните пропуск в таблице. Как называют совокупность социально значимых качеств индивида, формирующихся в процессе общественной жизни?",
    "Заполните пропуск в таблице. Как называют охраняемые законом ценности, интересы и блага, которым причиняется вред правонарушением?",
    "Заполните пропуск в таблице. Какое свойство Конституции означает обязательность её соблюдения всеми органами власти, должностными лицами и гражданами?",
    "Заполните пропуск в таблице. Как называют субъекты гражданского права, к которым относятся производственные кооперативы, хозяйственные общества и товарищества?",
    "Заполните пропуск в таблице. Какую роль выполняет человек, пользующийся товарами и услугами?",
    "Заполните пропуск в таблице. Как называют стимулы труда, к которым относятся повышение заработной платы, премии и бонусы?",
    "Заполните пропуск в таблице. Какой фактор производства включает все виды природных ресурсов, пригодных для производства экономических благ?",
    "Заполните пропуск в таблице. Как называют торговлю, при которой товар продаётся поштучно или небольшими количествами для личного потребления?",
    "Заполните пропуск в таблице. Какой фактор производства представляет деятельность людей с использованием физических и интеллектуальных возможностей, навыков и опыта?",
    "Заполните пропуск в таблице. Какой вид искусства представляет драматические произведения на сцене?",
    "Заполните пропуск в таблице. Какой вид искусства создаёт произведения, имеющие материальный объём и трёхмерную форму?",
    "Заполните пропуск в таблице. Как называют политическую партию с чёткой организацией, местными отделениями и постоянной работой с избирателями?",
    "Заполните пропуск в таблице. Какой вид юридической ответственности предусматривает штраф, принудительные работы и лишение свободы?",
    "Заполните пропуск в таблице. Как называют долевую ценную бумагу, дающую право на долю в капитале фирмы и дивиденд?",
    "Заполните пропуск в таблице. Как называют потребности в познании, красоте, религиозной вере и художественном творчестве?",
    "Заполните пропуск в таблице. Какая духовно-нравственная ценность означает готовность помочь оказавшемуся в трудном положении и проявить сострадание?",
    "Заполните пропуск в таблице. Какой признак государства означает независимость во внешних делах и верховенство государственной власти внутри страны?",
    "Заполните пропуск в таблице. Как называют целенаправленный процесс получения знаний и развития умений?",
    "Заполните пропуск в таблице. Как называют ресурсы домохозяйства, связанные со способностью и готовностью членов семьи участвовать в ведении хозяйства?",
    "Заполните пропуск в таблице. Как называют торжественную песню, служащую музыкальным символом государства?",
    "Заполните пропуск в таблице. Как называют знания домочадцев о приготовлении пищи, ремонте и других бытовых технологиях как ресурс семьи?",
    "Заполните пропуск в таблице. Какое правомочие собственника означает возможность фактически обладать вещью и относиться к ней как к своей?",
    "Заполните пропуск в таблице. Как называют партию, выступающую с критикой деятельности правящей партии или блока партий?",
    "Заполните пропуск в таблице. Как называют форму устройства, представляющую добровольное объединение территориальных образований с политической самостоятельностью?",
    "Заполните пропуск в таблице. Как называют стимулы труда, связанные с профессиональным ростом, карьерой и получением образования?",
    "Заполните пропуск в таблице. Какая форма правления предполагает принадлежность верховной власти единоличному правителю и её передачу по наследству?",
]

LEGACY_TASKS = {3: 19, 4: 3, 5: 10, 6: 11, 9: 8, 10: 9, 11: 13, 13: 14, 14: 15, 15: 16, 16: 17}

SINGLE_KEYS = {
    4: "224111433212222" + "444313244144311",
    5: "311121424424442" + "422442232243111",
    6: "123332333133333" + "333331111111232",
    9: "344441441314112" + "213322414421414",
    10: "233222133331333" + "412124133343133",
    11: "342112332224134" + "234244222232144",
    13: "432443242141241" + "222434322414123",
    15: "413123114433411" + "224411323114224",
    16: "143333114143321" + "122112323423332",
}

GROUP_KEYS = "1234 1423 1324 1324 1423 1234 1423 1324 2314 2413 1234 3412 1423 1423 3412 1324 2314 2413 1324 2413 1324 1324 1423 1423 1423 1234 1423 2314 1423 3412".split()
MATCH_KEYS = "22312 31312 22112 21234 11212 21211 12211 11222 22211 12221 31221 23213 23211 21122 32123 13122 12121 12334 32312 13211 12123 11122 21121 22112 12121 32211 31121 12221 23121 33212".split()


def variant_pages(variant):
    start = START_PAGES[variant - 1]
    end = START_PAGES[variant] if variant < 30 else 162
    return range(start, end)


def matching_columns(variant):
    if variant == 26:
        return [
            "А) Физик Ю. А. Лебедев провёл серию экспериментов в рамках своего исследования.\n"
            "Б) Инженер Р. А. Петров с семьёй смотрели в Большом театре балет «Лебединое озеро».\n"
            "В) Учитель Ю. Л. Рыбкина посетила Феодосийскую картинную галерею имени И. К. Айвазовского.\n"
            "Г) Первокурсница Ирина сдала первую сессию на «отлично».\n"
            "Д) Антон учится на третьем курсе медицинского университета.",
            "1) образование\n2) искусство\n3) наука",
        ]
    root = Path("review/oge-social-2027/ocr")
    for page in variant_pages(variant):
        data = json.loads((root / f"page-{page:03d}.json").read_text(encoding="utf-8"))
        lines = [line for block in data["blocks"] for paragraph in block["paragraphs"] for line in paragraph["lines"]]
        starts = [line["bbox"]["y0"] for line in lines if "Установите соответствие" in line["text"]]
        if not starts:
            continue
        top = starts[0]
        end = next(line["bbox"]["y0"] for line in lines if line["bbox"]["y0"] > top and "Запишите в таблицу" in line["text"])
        words = [word for line in lines for word in line["words"] if top < word["bbox"]["y0"] < end]
        first_left = next(word["bbox"]["y0"] for word in words if word["text"] == "А)")
        right_numbers = [word for word in words if re.fullmatch(r"[1234]\)", word["text"])]
        if not right_numbers:
            right_numbers = [word for word in words if word["text"] in ("1)", "2)", "3)", "4)")]
        split = min(word["bbox"]["x0"] for word in right_numbers if word["bbox"]["x0"] > 800) - 8
        columns = []
        for right in (False, True):
            rows = []
            for line in lines:
                selected = [word["text"] for word in line["words"] if first_left - 25 <= word["bbox"]["y0"] < end and (word["bbox"]["x0"] >= split) == right]
                if selected:
                    rows.append(" ".join(selected))
            columns.append("\n".join(rows))
        return columns
    raise ValueError(f"Matching columns not found: {variant}")


def task_two(text, variant):
    start = re.search(r"(?m)^\s*\[\s*2\s*[^\w\s]*\s*Заполните пропуск", text)
    if not start:
        raise ValueError(f"Task 2 boundaries not found: {variant}")
    end_relative = re.search(r"(?m)^\s*\[\s*3\s*[^\w\s]*\s*", text[start.end():])
    if not end_relative:
        raise ValueError(f"Task 2 end not found: {variant}")
    end = start.end() + end_relative.start()
    block = text[start.start():end]
    block = re.split(r"Ответ\s*[:;]", block, maxsplit=1)[0]
    return {
        "type": "short",
        "text": base.clean(block),
        "correct": SHORT_KEYS[variant - 1],
    }


def task_three_span(text, variant):
    instruction_match = re.search(r"первую\s+колонку\s+таблицы", text)
    if not instruction_match:
        raise ValueError(f"Task 3 instruction not found: {variant}")
    instruction = instruction_match.start()
    markers = list(re.finditer(r"(?m)^\s*\[\s*3\s*[^\w\s]*\s*", text[:instruction]))
    if not markers:
        raise ValueError(f"Task 3 boundaries not found: {variant}")
    start = markers[-1]
    block = text[start.start():]
    tokens = list(re.finditer(r"(?<!\d)(1|2|3|4|8|83)\)\s*", block))[:4]
    if len(tokens) != 4:
        raise ValueError(f"Variant {variant}: expected 4 comparison items, got {len(tokens)}")
    last_line_end = block.find("\n", tokens[3].end())
    if last_line_end < 0:
        last_line_end = len(block)
    return start.start(), start.start() + last_line_end


def task_three(text, variant):
    start, end = task_three_span(text, variant)
    block = text[start:end]
    tokens = list(re.finditer(r"(?<!\d)(1|2|3|4|8|83)\)\s*", block))[:4]
    left = [base.clean(block[token.end():tokens[index + 1].start() if index + 1 < 4 else len(block)]) for index, token in enumerate(tokens)]
    answer = GROUP_KEYS[variant - 1]
    return {
        "type": "match",
        "text": base.clean(block[:tokens[0].start()]),
        "left": left,
        "right": ["Черты сходства", "Черты различия"],
        "correct": [0 if str(index + 1) in answer[:2] else 1 for index in range(4)],
    }


def main():
    legacy_text = Path("oge-interactive.js").read_text(encoding="utf-8")
    legacy_json = legacy_text[legacy_text.index("push(") + 5:legacy_text.rindex(");")]
    legacy = json.loads(legacy_json)
    root = Path("review/oge-social-2027/ocr")
    base.MATCH_KEYS = MATCH_KEYS
    base.GROUP_KEYS = GROUP_KEYS
    base.matching_columns = matching_columns
    variants = []
    report = []

    for variant in range(1, 31):
        texts = [(root / f"page-{page:03d}.txt").read_text(encoding="utf-8") for page in variant_pages(variant)]
        combined = re.sub(r"Выберите\s+и\s+запишите", "Выберите и запишите", "\n\n".join(texts))
        combined = re.sub(r"\bОтвет\s*(?=\[)", "Ответ: ", combined)
        questions = {2: {"type": "short", "text": SHORT_TEXTS[variant - 1], "correct": SHORT_KEYS[variant - 1]}}
        questions[3] = task_three(combined, variant)
        task_three_start, task_three_end = task_three_span(combined, variant)
        without_three = combined[:task_three_start] + combined[task_three_end:]
        questions[14], remaining = base.match_block(without_three, variant)
        single_items = base.singles(remaining)
        single_numbers = list(SINGLE_KEYS)
        manual = None
        if variant == 19 and len(single_items) == 8:
            manual = (10, "Верны ли следующие суждения о заработной плате? А. Заработная плата - оплата трудовых услуг, предоставляемых наёмными работниками. Б. В условиях высокой инфляции номинальная и реальная заработная плата полностью совпадают.")
        elif variant == 29 and len(single_items) == 8:
            manual = (6, "Верны ли следующие суждения о патриотизме? А. Патриотизм - это любовь к Отечеству. Б. Патриотизм означает стремление граждан своими действиями служить интересам своей страны.")
        elif len(single_items) != 9:
            raise ValueError(f"Variant {variant}: expected 9 single-choice tasks, got {len(single_items)}")
        if manual:
            missing_number, missing_text = manual
            single_numbers.remove(missing_number)
            questions[missing_number] = {"type": "single", "text": missing_text, "options": ["верно только А", "верно только Б", "верны оба суждения", "оба суждения неверны"], "correct": int(SINGLE_KEYS[missing_number][variant - 1]) - 1}
        for number, question in zip(single_numbers, single_items):
            question["correct"] = int(SINGLE_KEYS[number][variant - 1]) - 1
            questions[number] = question

        legacy_questions = {question["sourceTask"]: question for question in legacy["variants"][variant - 1]["questions"]}
        for new_number, legacy_number in LEGACY_TASKS.items():
            old = legacy_questions[legacy_number]
            current = questions[new_number]
            similarity = SequenceMatcher(None, re.sub(r"\W", "", old["text"].lower()), re.sub(r"\W", "", current["text"].lower())).ratio()
            if old["correct"] == current["correct"] and similarity >= 0.72:
                questions[new_number] = deepcopy(old)

        if variant == 7:
            questions[16]["options"][3] = "оба суждения неверны"
        for question in questions.values():
            for field in ("text",):
                question[field] = re.sub(r"\s+", " ", re.sub(r"[&<>©]", "", question[field])).strip(" |;«»")
            for field in ("options", "left", "right"):
                if field in question:
                    question[field] = [re.sub(r"\s+", " ", re.sub(r"[&<>©]", "", value)).strip(" |;«»") for value in question[field]]

        ordered = []
        for number in SELECTED:
            question = questions[number]
            question.update(sourceVariant=variant, sourceTask=number)
            if number == 2:
                key = "/".join(SHORT_KEYS[variant - 1])
            elif number == 3:
                key = GROUP_KEYS[variant - 1]
            elif number == 14:
                key = MATCH_KEYS[variant - 1]
            else:
                key = SINGLE_KEYS[number][variant - 1]
            question["explanation"] = f"Эталон из таблицы ответов: {key}."
            ordered.append(question)
            report.append(f"{variant}.{len(ordered)} (original {number}) " + json.dumps(question, ensure_ascii=False))

        variants.append({
            "id": f"kotova-liskova-oge-social-2027-v{variant}",
            "title": f"Вариант {variant}",
            "questions": ordered,
        })

    source = {
        "subjectId": "social_oge",
        "id": "kotova-liskova-oge-social-2027",
        "title": "Тренировочные варианты",
        "year": "2027",
        "description": "Котова-Лискова · ОГЭ · 2027",
        "authorLine": "Котова-Лискова · ОГЭ · 2027",
        "variants": variants,
    }
    Path("oge-social-2027-interactive.js").write_text(
        "window.localInteractiveSources = window.localInteractiveSources || [];\n"
        "window.localInteractiveSources.push(" + json.dumps(source, ensure_ascii=False, indent=2) + ");\n",
        encoding="utf-8",
    )
    Path("review/oge-social-2027/tasks.txt").write_text("\n".join(report), encoding="utf-8")
    print("Built 30 variants, 360 tasks")


if __name__ == "__main__":
    main()
