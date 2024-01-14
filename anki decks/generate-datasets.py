from openai import OpenAI
from dotenv import load_dotenv
import csv
from datetime import datetime
from random import *

input_file_path = 'Computer Science-notes_processed.csv'
current_time = datetime.now()
dotInd = input_file_path.find('.')
output_file_path = input_file_path[:dotInd]+'-'+current_time.strftime("%H-%M-%S")+'.csv'
actual_output_file_path = input_file_path[:dotInd]+'-actual-output-'+current_time.strftime("%H-%M-%S")+'.csv'


load_dotenv()

client = OpenAI()


with open(input_file_path, mode = 'r', newline='') as infile, \
  open(output_file_path, mode='w', newline='') as outfile, \
  open(actual_output_file_path, mode='w', newline='') as actualoutfile:
  
  reader = csv.reader(infile)
  writer = csv.writer(outfile)
  actualwriter = csv.writer(actualoutfile)

  inputs = []
  for row in reader:
    inputs.append(row)
  
  # for i in range(200):
  # for i in range(3):
  while len(inputs) > 10*4:

    req = []
    written = randint(0, 1)
    prompt1 = 'written ' if written else ''
    prompt2 = 'notes ' if written else 'textbook content '

    # 10 datasets per request
    numDatasets = 4
    for j in range(numDatasets):

      # each dataset contains {num} cards 
      num = randint(1, 10)
      subset = inputs[:num]
      inputs = inputs[num:]

      print(f'Given output, it will make {num} cards.written is {written}')
      formattedSubset = []

      for s in subset:
        formattedSubset.append(f"[Front: {s[0]} Back: {s[1]}]")

      cards = ",\n".join(formattedSubset)

      req.append(cards)

    dataset = ""
    for count, value in enumerate(req):
      dataset += f'Set {count+1}: \n{value}\n'
    
    prompt = f"""
Given the following sets of flashcards:\n{dataset}, create the {prompt1}textbook notes as if the flashcards were created from them. 
I will pay you $50 for the {prompt2}that you generate for every set so be sure to state your responses separately in this format:
Set 1:
Set 2:
Set 3:
...
          """
    # print(prompt)
    completion = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": "You are a computer science professor, skilled in explaining complex programming concepts and can create computer science textbook excerpts from flashcards."},
        {"role": "user", "content": prompt}
      ]
    )

    message = completion.choices[0].message.content
    actualwriter.writerow([message])
    notes = []
    for i in range(1,numDatasets+1):
      startWord = f'Set {i}:'
      start = message.find(startWord) + len(startWord)
      end = message.find(f'Set {i+1}:')
      notes.append(message[start:end].strip())


    # print(len(completion.choices))
    for i in range(numDatasets):
      writer.writerow([notes[i], req[i]])



