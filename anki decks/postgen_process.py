### generated notes -> postgen processed
### Remove redundant content, and combine all csvs into one

import csv
import os
from huggingface_hub import HfApi

def combine_csv(folder_path, output_file):
    # first_file = True

    with open(output_file, 'w', newline='', encoding='utf-8') as f_output:
        writer = csv.writer(f_output)
        writer.writerow(["notes", "cards"])

        for filename in os.listdir(folder_path):
            if filename.endswith('.csv'):
                with open(os.path.join(folder_path, filename), 'r', newline='', encoding='utf-8') as f_input:
                    reader = csv.reader(f_input)

                    # if first_file:
                    #     # Write the header of the first file
                    #     writer.writerow(next(reader))
                    #     first_file = False
                    # else:
                    #     # Skip the header for subsequent files
                    #     next(reader)

                    # Write the data
                    for row in reader:
                        writer.writerow(row)

# Example usage
folder_path = 'generated notes'  # Replace with your folder path
output_file = 'hugging_face_upload/dataset.csv'      # Name of the output file
combine_csv(folder_path, output_file)

api = HfApi()
api.upload_file(
    path_or_fileobj="hugging_face_upload/dataset.csv",
    path_in_repo="dataset.csv",
    repo_id="fairnightzz/anki-generated",
    repo_type="dataset",
)