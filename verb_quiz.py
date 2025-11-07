import json
import random
import re
import os


def load_data(json_filepath):
    with open(json_filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        return data


def generate_quiz(json_filepath, selected_group, specific_verb, number_of_verbs):
    data = load_data(json_filepath)

    quiz_set = []
    
    if selected_group:
        filtered = [
            v for v in data if re.match(selected_group, v["verb_group"])
        ]
    elif specific_verb:
        filtered = [v for v in data if v["verb"] == specific_verb]
    else:
        filtered = data

    selected_verbs = random.sample(
        filtered, min(number_of_verbs, len(filtered)))
    verbforms = [
        "infinitiv", "imperativ", "presens", "preteritum", "supinum"
    ]

    for verb in selected_verbs:
        random.shuffle(verbforms)
        questions = []
        for form in verbforms:
            if form in verb["meningar"] and verb["meningar"][form]:
                mening = verb["meningar"][form]
                answer = verb["conjugations"][form]
                question = {
                    "verb": verb["verb"],
                    "form": form,
                    "mening": re.sub(rf"\b{re.escape(answer)}\b", "_______", mening, flags=re.IGNORECASE),
                    "answer": verb["conjugations"][form]
                }
                questions.append(question)
        quiz_set.extend(questions)

    return quiz_set


def run_quiz(selected_group=None, specific_verb=None, number_of_verbs=5):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    json_filepath = os.path.join(current_dir, "verb_data.json")
    questions = generate_quiz(json_filepath, selected_group, specific_verb, number_of_verbs)
    return questions


def generate_table_quiz(json_filepath, selected_group):
    data = load_data(json_filepath)

    if selected_group:
        filtered = [v for v in data if v["verb_group"] == selected_group]
    else:
        filtered = data

    selected_verbs = random.sample(filtered, len(filtered))

    quiz_data = []
    verbforms = ["infinitiv", "imperativ", "presens", "preteritum", "supinum"]

    for verb in selected_verbs:
        filled_form = random.choice(verbforms)
        table_rows = []

        for form in verbforms:
            table_rows.append({
                "form": form,
                "answer": verb["conjugations"][form],
                "prefilled": (form == filled_form)
            })

        quiz_data.append({
            "verb": verb["verb"],
            "verb_group": verb["verb_group"],
            "translation": verb.get("translation", ""),
            "rows": table_rows
        })

    return quiz_data
