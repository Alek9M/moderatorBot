import logging
import os
from dotenv import load_dotenv
import json
from datetime import datetime

load_dotenv()
logging.basicConfig(level=logging.WARNING)

def count_group_members(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    group_member_counts = {}
    for obj in data:
        group_name = obj.get("group_name")
        member_count = len(obj.get("members", []))
        group_member_counts[group_name] = member_count

    return group_member_counts


def print_usernames(filename):
    with open(filename, "r") as file:
        data = json.load(file)

    group_member_counts = {}
    for obj in data:
        print(obj.get("group_name"))
        for member in obj.get("members", []):
            print("@" + member.get("username"))
        print("")

if __name__ == '__main__':
    filename = os.getenv('DOWNLOADFOLDER') + "snapshot_2024-06-04.json"
    # count_group_members(filename)
    print_usernames(filename)