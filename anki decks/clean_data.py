### raw -> cleaned
import csv
import argparse

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('input_file', nargs='?', type=str, help='Path to the input CSV file')
parser.add_argument('output_file', nargs='?', type=str, default='', help='Path to the output CSV file')

# Parse arguments
args = parser.parse_args()

# File paths from arguments
input_file_path = args.input_file
output_file_path = args.output_file
if output_file_path == '':
  dotInd = input_file_path.find('.')
  output_file_path = './cleaned/' + input_file_path[:dotInd] + '_cleaned.csv'
input_file_path = './raw/' + args.input_file


# Open the input file in read mode and output file in write mode
with open(input_file_path, mode='r', newline='') as infile, \
        open(output_file_path, mode='w', newline='') as outfile:
    # Create reader and writer objects
    reader = csv.reader(infile, delimiter='\t')
    writer = csv.writer(outfile)

    line = 0

    # Iterate through the rows in the input file
    for row in reader:
      line += 1
      if line <= 2:
        continue
      # Write only the first two columns to the output file
      print(row)
      writer.writerow(row[:2])