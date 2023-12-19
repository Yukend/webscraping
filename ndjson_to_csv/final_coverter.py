import json
import csv
import ndjson
import pandas as pd


class JSONToCSVConverter:

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

    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.all_data = []

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
                elif name[:-1] in JSONToCSVConverter.required_fields:
                    value = ""
                    for i in range(len(value)):
                        if i != len(value)-1:
                            value += value[i] + ","
                        else:
                            value += value[i]
                    final_json[name[:-1]] = value

            else:
                if name[:-1] in JSONToCSVConverter.required_fields:
                    final_json[name[:-1]] = value

        flatten(val)
        return final_json

    def convert_to_csv(self):
        with open(self.input_file, 'r') as f:
            json_in = ndjson.load(f)

        for json_string in json_in:
            data = json.loads(json.dumps(json_string))
            flat_data = self.flatten(data)
            self.all_data.append(flat_data)

        header = set()
        for row in self.all_data:
            header.update(row.keys())

        with open(self.output_file, 'w', newline='', encoding='utf-8') as csv_file:
            csv_writer = csv.DictWriter(csv_file, fieldnames=header)
            csv_writer.writeheader()
            csv_writer.writerows(self.all_data)

    def read_csv(self):
        data = pd.read_csv(self.output_file)
        return data

    def run_conversion(self):
        self.convert_to_csv()
        print(
            f'Conversion from multiple nested JSON files to CSV completed. Data written to {self.output_file}')


if __name__ == '__main__':
    input_file = 'profiles.ndjson'
    output_file = 'profiles.csv'

    converter = JSONToCSVConverter(input_file, output_file)
    converter.run_conversion()

    # Example: Access the CSV data as a DataFrame
    data_frame = converter.read_csv()
    print(data_frame["linkedin_url"])
