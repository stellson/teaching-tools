"""
Script that takes a csv word list (two columns, with Swedish in the first column) and a text as input,
and returns the lines containing words from the list with the word blanked out. 
Can be used for practicing vocabulary in specific linguistic contexts.
If you want to add a translation of the words, set Translation=True at the end of the script before running.

Example output:

    Words substituted: {'ihop', 'döma', 'nog', 'redigera', 'beredd', 'typ', 'skaffa', 'brorsa', 'stöta på', 'tag', 'reta', 'ansluta'}

    – Man letar bara upp ett intressant ämne och __________ sig till ­konversationen, förklarar Gabriel.
    Ett __________ hjälpte jag honom att __________ Youtube-videor.
    Vid enstaka tillfällen har Gabriel __________ på skumma personer.
    Föräldrarna känner till att Gabriel __________ nya vänner på nätet.
"""
import csv, re, glob

class ReplaceWords:
    def __init__(self, csv_file, text_files, language, full_text=True, output_file="output_text.txt", translation=True, margin=2):
        self.csv_file = csv_file
        self.text_files = text_files
        self.language = language
        self.full_text = full_text
        self.output_file = output_file
        self.translation = translation
        self.margin = margin
        self.super_text = ""
        self.word_dict = {}
        self.base_form_dict = {}
        self.replaced_words = set()
        self.full_text_with_blanks = ""

    def load_text_files(self):
        """Reads and aggregates text from all specified files."""
        for text_file in self.text_files:
            with open(text_file, 'r', encoding='utf-8') as f:
                self.super_text += f.read() + " "

    def load_words_from_csv(self):
        """Loads and processes words from the CSV file."""
        with open(self.csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f, delimiter=',')  # Change delimiter if necessary
            for row in reader:
                words = row[0].strip().split(',')
                if self.language == "swedish":
                    words = [self.process_swedish_word(word) for word in words]
                base_form = words[0].strip()  # The base form is the first word in the list
                for word in words:
                    cleaned_word = word.strip()
                    eng_word = self.process_english_word(row[1].strip())
                    self.word_dict[cleaned_word] = eng_word.lower() if self.translation else None
                    self.base_form_dict[cleaned_word] = base_form  # Map each form to the base form

    def process_swedish_word(self, word):
        """Removes Swedish articles from the beginning of the word."""
        if word.lower().startswith("att "):
            return word[4:]
        elif word.lower().startswith("en "):
            return word[3:]
        elif word.lower().startswith("ett "):
            return word[4:]
        elif word.lower().startswith("två "):
            return word[4:]
        return word

    def process_english_word(self, word):
        """Removes English articles from the beginning of the word."""
        if word.lower().startswith("a "):
            return word[2:]
        elif word.lower().startswith("an "):
            return word[3:]
        elif word.lower().startswith("to "):
            return word[3:]
        return word

    def replace_words_in_text(self):
        """Replaces occurrences of words in the text with the blanked version."""
        sentences = re.split(r'(?<=[.!?])\s+', self.super_text)
        modified_sentences = []
        full_text = self.super_text

        for sentence in sentences:
            original_sentence = sentence
            for word, translation in self.word_dict.items():
                pattern = re.compile(r'\b' + re.escape(word) + fr'\w{{0,{self.margin}}}\b', re.IGNORECASE)
                if pattern.search(sentence):
                    replacement = f'__________({translation})' if translation else '__________'
                    sentence = pattern.sub(replacement, sentence)
                    full_text = pattern.sub(replacement, full_text)
                    self.replaced_words.add(self.base_form_dict[word])  # Add base form to replaced_words

            if '__________' in sentence:
                modified_sentences.append(sentence)

        self.full_text_with_blanks = full_text

        joined_sentences = '\n'.join(modified_sentences)
        filtered_sentences = [sentence.strip() for sentence in joined_sentences.split('\n') if '__________' in sentence]
        #print(f'{len(filtered_sentences)} sentences blanked. \n')
        blanked_sentences = '\n'.join(filtered_sentences)

        return blanked_sentences

    def create_blanked_text(self):
        """Save the full text with blanks to an output file."""
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(self.full_text_with_blanks)
            print(f"\nFull text with blanks saved to {self.output_file}")

    def run(self):
        """Run the full process."""
        self.load_text_files()
        self.load_words_from_csv()
        blanked_sentences = self.replace_words_in_text()

        print(f"Words substituted: {self.replaced_words}\n")
        print(blanked_sentences)

        if self.full_text==True:
            self.create_blanked_text()


# Change paths. .csv and .txt or .rtf files only.
csv_file = "words.csv"
text_files = glob.glob("*.txt")

# Change settings here.
wordreplacer = ReplaceWords(csv_file, text_files, language="swedish", full_text=True, translation=False, margin=0)
wordreplacer.run()
