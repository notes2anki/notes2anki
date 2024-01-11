from openai import OpenAI
from dotenv import load_dotenv
import csv
from datetime import datetime
from random import *

input_file_path = 'os_processed.csv'
current_time = datetime.now()
dotInd = input_file_path.find('.')
output_file_path = input_file_path[:dotInd]+'-'+current_time.strftime("%H-%M-%S")+'.csv'


load_dotenv()

client = OpenAI()


with open(input_file_path, mode = 'r', newline='') as infile, \
  open(output_file_path, mode='w', newline='') as outfile:
  
  reader = csv.reader(infile)
  writer = csv.writer(outfile)

  inputs = []
  for row in reader:
    inputs.append(row)
  
  # for i in range(20):
  for i in range(1):

    # rewrite this as a batch request
    shuffle(inputs)

    num = randint(1, 10)
    subset = inputs[:num]

    print(f'Given output, it will make {num} cards.')
    formattedSubset = []

    for s in subset:
      formattedSubset.append(f"[Front: {s[0]} Back: {s[1]}]")

    cards = ",\n".join(formattedSubset)

    writtenOrNah = 'written ' if randint(0, 1) == 1 else ''

    completion = client.chat.completions.create(
      model="gpt-3.5-turbo-16k",
      messages=[
        {"role": "system", "content": "You are a computer science professor, skilled in explaining complex programming concepts and can create computer science textbook excerpts from flashcards."},
        {"role": "user", "content": f"Given the flashcards {cards}, create the {writtenOrNah}textbook notes as if the flashcards were created from them."},
        {"role": "user", "content": f"say hello"}
      ]
    )

    # message = completion.choices[0].message.content
    message = completion.choices[0].message.content
    print(len(completion.choices))
    writer.writerow([message, cards])



