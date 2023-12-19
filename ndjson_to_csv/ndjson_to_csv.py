import json
import csv
import ndjson
import pandas as pd

# Output CSV file
output_csv_file = 'profiles.csv'

# Initialize a list to hold all the data from JSON files
all_data = []

with open('profiles.ndjson', 'r') as f:
    json_in=f.read()    
    json_in= ndjson.loads(json_in)

# Helper function to flatten nested JSON
def flatten(y):
    """Recursively flatten a nested JSON."""
    out = {}

    def flatten(x, name=''):
        if type(x) is dict:
            for a in x:
                flatten(x[a], name + a + '_')
        elif type(x) is list:
            i = 0
            for a in x:
                flatten(a, name + str(i) + '_')
                i += 1
        else:
            print(name)
            out[name[:-1]] = x

    flatten(y)
    return out

# Iterate through each JSON file in the directory
for json_string in json_in:
        
    data = json.loads(json.dumps(json_string))
    
    # Flatten the nested JSON data and append it to the all_data list
    flat_data = flatten(data)
    all_data.append(flat_data)

# Extract all unique keys to create the CSV header
header = set()
for row in all_data:
    header.update(row.keys())

# Write the combined data to a CSV file
with open(output_csv_file, 'w', newline='', encoding='utf-8') as csv_file:
    # Create a CSV writer object
    csv_writer = csv.DictWriter(csv_file, fieldnames=header)

    # Write the header row
    csv_writer.writeheader()

    # Write the data rows
    csv_writer.writerows(all_data)

data = pd.read_csv(output_csv_file)
print(data["linkedin_url"])

print(f'Conversion from multiple nested JSON files to CSV completed. Data written to {output_csv_file}')
