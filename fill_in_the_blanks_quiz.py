"""
This script reads all .csv files and all .txt files in the current directory and creates an interactive quiz that's run directly in the terminal,
where each sentence from the .txt files in which any of the words from the .csv files occur (in any conjugation, given different conjugations are 
included in an entry in the csv file) will be presented as one question of the quiz, with the word blanked out.
"""
import csv, re, glob

class Quiz:

    def __init__(self, csv_file, text_files, language, margin=1):
        self.csv_file = csv_file
        self.text_files = text_files
        self.language = language
        self.margin = margin
        self.super_text = ""
        self.base_form_dict = {}
        self.replaced_words = []
        self.eng_swe_dict = {}
        self.blanked_sentences = []
        self.expected_answers = []

    def load_text_files(self):
        """Reads and aggregates text from all specified files."""
        for text_file in self.text_files:
            with open(text_file, 'r', encoding='utf-8') as f:
                self.super_text += f.read() + " "

    def load_words_from_csv(self):
        """Loads and processes words from the CSV file."""
        for file in self.csv_file:
            with open(file, 'r', encoding='utf-8') as f:
                reader = csv.reader(f, delimiter=',')  # Adjust delimiter as needed
                for row in reader:
                    swe_word = row[0].strip().split(',') # a list
                    eng_word = self.process_english_word(row[1].strip())

                    if self.language == "swedish":
                        words = [self.process_swedish_word(word) for word in swe_word]

                    base_form = words[0]  # The base form is the first word in the list
                    for word in words:
                        self.eng_swe_dict[word.strip()] = eng_word
                        eng_word = self.process_english_word(row[1].strip())
                        self.eng_swe_dict[word] = eng_word.lower()
                        self.base_form_dict[word] = base_form  # Map each form to the base form

    def process_swedish_word(self, word):
        """Removes Swedish articles from the beginning of the word."""
        if word.lower().startswith(("att ", "en ", "ett ", "två ")):
            return word.split(" ", 1)[1]
        return word.strip()

    def process_english_word(self, word):
        """Removes English articles from the beginning of the word."""
        return word.split(" ", 1)[1] if word.lower().startswith("a ") else word

    def replace_words_in_text(self):
        """Replaces occurrences of words in the text with the blanked version."""
        sentences = re.split(r'(?<=[.!?])\s+', self.super_text)
        for sentence in sentences:
            original_sentence = sentence
            for word, translation in self.eng_swe_dict.items():
                pattern = re.compile(r'\b' + re.escape(word) + fr'\w{{0,{self.margin}}}\b', re.IGNORECASE)
                match = pattern.search(sentence)
                if match:
                    found_word = match.group()
                    replacement = f'__________({translation})'
                    blanked_sentence = pattern.sub(replacement, sentence)
                    self.expected_answers.append(found_word)

                    if not blanked_sentence in self.blanked_sentences:
                        self.blanked_sentences.append(blanked_sentence)
        joined_sentences = '\n'.join(self.blanked_sentences)
        self.blanked_sentences = [sentence.strip() for sentence in joined_sentences.split('\n') if '__________' in sentence]
        #print(self.blanked_sentences)

    def swe_test(self):
        print(f"Du kommer att få {len(self.blanked_sentences)} meningar. Fyll i rätt ord på raden. Tänk på stavningen och böjningar/kongruens! \nSvara 'stopp' för att avsluta quizet.\n")
        points = 0
        for i, sentence in enumerate(self.blanked_sentences):
            expected_answer = self.expected_answers[i]
            test = input(f"{i+1}. {sentence}\n")
            if test.lower() == "stopp":
                print(f"Okej, vi stoppar där! Du fick totalt {points}/{len(self.blanked_sentences)} poäng.")
                return
            if test.lower() == expected_answer.lower():
                points += 1
                print(f"Det är rätt! Du har totalt {points}/{len(self.blanked_sentences)} poäng.")
            else:
                print(f"Det är fel tyvärr, rätt svar är '{expected_answer}'! Du har fortfarande {points}/{len(self.blanked_sentences)} poäng.")

        while True:
            y_n = input("Vill du göra quizet igen? Ja/nej? \n").lower()
            if y_n in ("nej", "n", "stopp"):
                print(f"Bra jobbat! Du fick totalt {points}/{len(self.blanked_sentences)} poäng.")
                break
            elif y_n in ("ja", "j"):
                self.swe_test()
            #else:
             #   print("Vill du göra quizet igen? Ja/nej?.")

    def run(self):
        self.load_text_files()
        self.load_words_from_csv()
        self.replace_words_in_text()
        self.swe_test()

csv_file = glob.glob("*.csv")
text_files = glob.glob("*.txt")

quizzer = Quiz(csv_file, text_files, language="swedish")
quizzer.run()
