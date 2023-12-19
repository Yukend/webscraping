import json
import csv
import ndjson

# Output CSV file
output_csv_file = 'test_profiles.csv'

# Initialize a list to hold all the data from JSON files
all_data = []

required_fields = [
    "profile_enrich_contacts_0_emails",
    "profile_enrich_contacts_0_contact_twitter",
    "profile_enrich_contacts_0_contact_facebook",
    "linkedin_url",
    "profile_username",
    "profile_lastName",
    "profile_hasFetchedFollowing",
    "profile_industry",
    "profile_connectionsCount",
    "profile_birthDate",
    "profile_firstName",
    "profile_premium",
    "profile_influencer",
    "profile_location_country",
    "profile_location_city",
    "profile_location_state",
    "profile_id",
    "profile_summary",
    "profile_scoreEngagements",
    "profile_score",
    "profile_scoreRatioEngagement",
    "profile_scoreFollowers",
    "profile_scoreNbPosts",
    "profile_nbEngagements",
    "profile_nbPosts",
    "profile_image",
    "profile_imageHosted",
    "profile_companyIsAgency",
    "profile_companyIsStartup",
    "profile_companyIsSaas",
    "profile_companyName",
    "profile_companyIndustryTags",
    "profile_companyUsername",
    "profile_companyTargetMarket",
    "profile_enrichedCompanyVersion",
    "profile_isCompanyEnriched",
    "profile_fetchVersion",
    "profile_followersCount",
    "profile_imageBanner"
]

with open('profiles.ndjson', 'r') as f:
    json_in = f.read()
    json_in = ndjson.loads(json_in)

# Helper function to flatten nested JSON


def flatten(val):
    """Recursively flatten a nested JSON."""
    final_json = {}

    def flatten(value, name=''):
        if name[:-1] == "profile_zFull":
            final_json[name[:-1]] = json.dumps(value)
        elif type(value) is dict:
            for a in value:
                flatten(value[a], name + a + '_')
        elif type(value) is list:
            if value != [] and type(value[0]) is dict:
                i = 0
                for a in value:
                    flatten(a, name + str(i) + '_')
                    i += 1
            elif name[:-1] in required_fields:
                value_string = ""
                for i in range(len(value)):
                    if i != len(value)-1:
                        value_string += value[i] + ","
                    else:
                        value_string += value[i]
                final_json[name[:-1]] = value_string

        else:
            if name[:-1] in required_fields:
                final_json[name[:-1]] = value

    flatten(val)
    return final_json


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

print(
    f'Conversion from multiple nested JSON files to CSV completed. Data written to {output_csv_file}')
