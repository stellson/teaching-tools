import json
import random
import os
import re


class NounDeclensionQuiz:

    def __init__(self, json_filepath, number_of_nouns=5):
        self.json_filepath = json_filepath
        self.data = []
        self.number_of_nouns = number_of_nouns
        self.quiz_set = []

    def load_data(self):
        with open(self.json_filepath, "r", encoding="utf-8") as f:
            self.data = json.load(f)

    def generate_quiz(self):
        self.quiz_set = []
        filtered = self.data

        selected_nouns = random.sample(
            filtered, min(self.number_of_nouns, len(filtered)))
        nounforms = ["sing_indef", "sing_def", "plur_indef", "plur_def"]

        for noun in selected_nouns:
            random.shuffle(nounforms)
            questions = []
            for form in nounforms:
                if form in noun["meningar"] and noun["meningar"][form]:
                    mening = noun["meningar"][form]
                    answer = noun["conjugations"][form]

                    question = {
                        "noun": noun["noun"],
                        "form": form,
                        "mening": re.sub(rf"\b{re.escape(answer)}\b", "_______", mening, flags=re.IGNORECASE),
                        "answer": noun["conjugations"][form]
                    }
                    questions.append(question)
            self.quiz_set.extend(questions)

        return self.quiz_set


current_dir = os.path.dirname(os.path.abspath(__file__))
noun_data_path = os.path.join(current_dir, "noun_data.json")
quiz = NounDeclensionQuiz(noun_data_path)
quiz.load_data()
number_of_nouns = 5
