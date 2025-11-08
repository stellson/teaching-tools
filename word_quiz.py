"""
This is a simple word quiz. It will read any csv files (two columns, Swedish in the first column) found in the same directory as this script and create a word quiz
that is ran directly in the terminal.
"""

import csv, re, glob

class Quiz:

  def __init__(self, csv_file):
    self.csv_file = csv_file
    self.rows_lst = []
    self.eng_swe_dict = {}

  def get_csv(self):
    with open(self.csv_file, 'r') as file:
      reader = csv.reader(file, delimiter=',')
      self.rows_lst = list(reader)

  def eng_swe(self):
    for row in self.rows_lst:
      self.eng_swe_dict[row[1]] = row[0]

  def swe_test(self):
    print(f"Du kommer att få {len(self.eng_swe_dict)} frågor. Tänk på stavningen och inkludera artiklar (en/ett)! Svara 'stopp' för att avsluta quizet.")
    while True:  # Making the code for the test run indefinitely until the user breaks it manually.
      points = 0
      for k, v in self.eng_swe_dict.items():
        test = input("Vad heter '"+k+"' på svenska? \n")  # Asks the user for the translation.
        if test=="stopp":
          print("Bra jobbat! Du fick totalt", points,"/", len(self.eng_swe_dict))
          return
        if test == v:
          points += 1  # If the user provides the corresponding v to the k, one point is added to the total.
          print("Det är rätt! Du har totalt", points,"/", len(self.eng_swe_dict), "poäng.")
        else:
          print("Det är fel tyvärr, men nästa fråga tar du! Du har nu", points,"/", len(self.eng_swe_dict), "poäng.")

      while True: # Keeps asking user if they want to play again, until loop is broken by them saying no.
        y_n = input("Vill du spela igen? Ja/nej? \n")
        if re.match (r"^(nej|n|Nej)", y_n):
          print("Bra jobbat! Du fick totalt", points,"/", len(self.eng_swe_dict))
          return
        elif re.match(r"^(ja|j|Ja|Ja!|ja!)", y_n):
          break
        else:
          print("Vill du spela igen? Skriv ja eller nej.")

  def run(self):
    self.get_csv()
    self.eng_swe()
    self.swe_test()

csv_files = glob.glob("*.csv")
quizzer = Quiz(csv_files[0])
quizzer.run()
