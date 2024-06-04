import logging
import os
from dotenv import load_dotenv
from firebase import Firebase
import json
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.WARNING)

firebase = Firebase()


def extract_and_save(data):
    extracted_data = []
    for obj in data:
        group = {
            "group_name": obj.title,
            "members": [{"username": member.username} for member in obj.members]
        }
        extracted_data.append(group)

    filename = os.getenv('DOWNLOADFOLDER') + "snapshot_" + datetime.now().strftime("%Y-%m-%d") + ".json"
    with open(filename, "w") as file:
        json.dump(extracted_data, file, indent=4)

if __name__ == '__main__':
    groups = firebase.export()

    extract_and_save(groups)
