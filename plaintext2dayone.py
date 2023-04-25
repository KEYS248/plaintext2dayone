import argparse
import json
from datetime import datetime, timedelta

parser = argparse.ArgumentParser(
    description="""Convert plain text file into Day One JSON file.
    If for Journey App, you will need to zip and rename the exported Day One JSON as shown here: https://help.journey.cloud/en/article/import-day-one-spkats/
    
    Plain text format:
    2000-01-01
    Journal Entry
    2000-01-02
    Journal Entry""")
parser.add_argument('--text', required=True, help="input file in plain text format where dates are a separate line above a journal entry")
parser.add_argument('--dayone', required=True, help="output file in the Day One JSON format")
args = parser.parse_args()

f = open(args.text, "r")
text_data = f.readlines()
f.close()

dayone_meta = {}
dayone_meta["version"] = "1.0"

def datetime_valid(dt_str):
    try:
        datetime.fromisoformat(dt_str)
    except:
        return False
    return True

dayone_entries = []
dayone_entry = {}
dayone_entry['text'] = '#dreams\n'
text_data.append("0001-01-01") # Adding a random date to the end of the import data ensures the last entry gets written into the new file
for text_entry in text_data:
    if datetime_valid(text_entry.strip()):
        if len(dayone_entry) > 1:
            dayone_entries.append(dayone_entry)
            dayone_entry = {}
            dayone_entry['text'] = '#dreams\n'
        dayone_entry['creationDate'] = str(datetime.fromisoformat(text_entry.strip()) + timedelta(hours = 6))
    elif len(text_entry) > 0:
        dayone_entry['text'] += text_entry
        

dayone_data = {}
dayone_data['metadata'] = dayone_meta
dayone_data['entries'] = dayone_entries
dayone = json.dumps(dayone_data, indent = 2)

f = open(args.dayone, "w")
f.write(dayone)
f.close()