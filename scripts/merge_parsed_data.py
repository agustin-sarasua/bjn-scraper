import os
import json

INDEX_NAME = "sentencias-index"

def merge_json_files_to_jsonl(input_dir, output_file):
    # Initialize an empty list to store the JSON objects
    json_data = []
    
    # Iterate through the directory structure
    for root, dirs, files in os.walk(input_dir):
        for idx, file in enumerate(files):
            if file.endswith(".json"):
                # Construct the full path to the JSON file
                file_path = os.path.join(root, file)

                # Read the JSON file and append its contents to the list
                with open(file_path, "r", encoding="utf-8") as json_file:
                    try:
                        json_obj = json.load(json_file)
                        json_data.append({ "index" : { "_index": INDEX_NAME, "_id" : f"{idx}" } })
                        json_data.append(json_obj)
                    except json.JSONDecodeError as e:
                        print(f"Error parsing {file_path}: {str(e)}")

    # Write the list of JSON objects to the JSONL file
    with open(output_file, "w", encoding="utf-8") as jsonl_file:
        for obj in json_data:
            jsonl_file.write(json.dumps(obj) + "\n")

# Usage example:
input_directory = "parsed_data"
output_jsonl_file = "merged_data.jsonl"
merge_json_files_to_jsonl(input_directory, output_jsonl_file)