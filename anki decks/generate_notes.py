from openai import OpenAI
from dotenv import load_dotenv
import csv
from datetime import datetime
from random import *

NUM_DATASETS = 3

load_dotenv()
client = OpenAI()

### files
notesOrTextbook = randint(0, 1)
subprompt1 = 'textbook chapters'
subprompt2 = 'professor'

input_file = 'algo_anki_cleaned.csv' # TODO: input arg
input_file_path = './cleaned/algo_anki_cleaned.csv'
dotInd = input_file.find('_cleaned')
output_file_path = './generated/' + input_file[:dotInd] + '_generated_' + subprompt1.split(' ')[0] + '_' + subprompt1.split(' ')[1] + '.csv'
with open(input_file_path, mode = 'r', newline='') as infile, \
  open(output_file_path, mode='w', newline='') as outfile:
  reader = csv.reader(infile)
  writer = csv.writer(outfile)
  
  
  ### convert input to array
  inputs = []
  for row in reader:
    inputs.append(row)
  
  
  ### generate request message
  while len(inputs) > 10 * NUM_DATASETS:
    requests = []

    # j datasets per request
    for j in range(NUM_DATASETS):
        formattedSubdecks = []
        num = randint(1, 10) # each dataset contains {num} cards 
        subdeck = inputs[:num]
        inputs = inputs[num:]
    
        formattedSubdecks = [f"[Front: {card[0]} Back: {card[1]}]" for card in subdeck]
        requests.append(",\n".join(formattedSubdecks))
        
        requestMessage = ""
        for count, value in enumerate(requests):
            requestMessage += f'Set {count+1}: \n{value}\n'
    
    
    ### gpt
    prompt = f"""
              Given the following sets of flashcards:\n{requestMessage}\n, create the {subprompt1} as if the flashcards were created from them. 
              I will pay you $100 for the {subprompt1} that you generate for every set so be sure to state your responses separately in this format:
              Set 1:
              Set 2:
              Set 3:
              ...
            """
    response = client.chat.completions.create(
      model="gpt-3.5-turbo",
      messages=[
        {"role": "system", "content": f"You are a computer science {subprompt2}, skilled in explaining complex programming concepts and can create computer science {subprompt1} from flashcards."},
        {"role": "user", "content": prompt}
      ]
    )
    response = response.choices[0].message.content
    
    
    ### write output file
    notes = []
    for i in range(1,NUM_DATASETS+1):
      startWord = f'Set {i}:'
      start = response.find(startWord) + len(startWord)
      end = response.find(f'Set {i+1}:')
      notes.append(response[start:end].strip())

    for i in range(NUM_DATASETS):
      writer.writerow([notes[i], requests[i]])
