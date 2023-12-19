import json
import csv
import os
import ndjson
import polars as pl
import pandas as pd

# Output CSV file
output_csv_file = 'profiles.csv'
original_csv_file = 'original.csv'

# Initialize a list to hold all the data from JSON files
all_data = [] # List of all the data from JSON files contains email, twitter, facebook
json_data = [] # List of all the data from JSON files 
for file in os.listdir("../enrich"):
    if file.endswith(".ndjson"):
        print(file)
        with open(file, 'r') as f:
            json_in=f.read()    
            json_in= ndjson.loads(json_in)
            json_data.extend(json_in)

# Iterate through each JSON file in the directory
for json_string in json_data:
        
    data = json.loads(json.dumps(json_string))
    if data["profile_enrich"]["contacts"]:
        email = data["profile_enrich"]["contacts"][0]["contact"].get("emails", "")
        twitter = data["profile_enrich"]["contacts"][0]["contact"].get("twitter", "")
        facebook = data["profile_enrich"]["contacts"][0]["contact"].get("facebook", "")
        flat_data = {
            "linkedin_url": data["linkedin_url"],
            "email": email[0] if email else "",
            "twitter_url": "twitter.com/" + twitter if twitter and "twitter.com/" not in twitter else twitter,
            "facebook_url": "facebook.com/" + facebook if facebook and "facebook.com/" not in facebook else facebook
            }
        all_data.append(flat_data)
    else:
        flat_data = {
            "linkedin_url": data["linkedin_url"],
            "email": "",
            "twitter_url": "",
            "facebook_url": ""
            }
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

print(f'Conversion from multiple nested JSON files to CSV completed. Data written to {output_csv_file}')
df1 = pl.read_csv(original_csv_file)
df2 = pl.read_csv(output_csv_file)
key_column = "linkedin_url"
merged_df = df1.join(df2, on=key_column, how="left")
merged_df.write_csv("final.csv")
df1 = pd.read_csv(original_csv_file)
df2 = pd.read_csv(output_csv_file)
key_column = "linkedin_url"
merged_df = df1.merge(df2, on=key_column, how="left")
merged_df.to_csv("final2.csv", index=False)