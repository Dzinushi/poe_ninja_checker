import json
import os
from collections import defaultdict
from datetime import datetime
from enum import Enum

import urllib3


class League(Enum):
    STANDARD = 1
    CHALLENGE = 2


URLS_STANDARD = {'https://poe.ninja/api/Data/GetUniqueJewelOverview?league=Standard': 'jewels',
                 'https://poe.ninja/api/Data/GetUniqueMapOverview?league=Standard': 'maps',
                 'https://poe.ninja/api/Data/GetDivinationCardsOverview?league=Standard': 'divinations',
                 'https://poe.ninja/api/Data/GetUniqueFlaskOverview?league=Standard': 'flasks',
                 'https://poe.ninja/api/Data/GetUniqueWeaponOverview?league=Standard': 'weapons',
                 'https://poe.ninja/api/Data/GetUniqueArmourOverview?league=Standard': 'armors',
                 'https://poe.ninja/api/Data/GetUniqueAccessoryOverview?league=Standard': 'accessories'}

URLS_CHALLENGE = {'https://poe.ninja/api/Data/GetUniqueJewelOverview?league=Abyss': 'jewels',
                  'https://poe.ninja/api/Data/GetUniqueMapOverview?league=Abyss': 'maps',
                  'https://poe.ninja/api/Data/GetDivinationCardsOverview?league=Abyss': 'divinations',
                  'https://poe.ninja/api/Data/GetUniqueFlaskOverview?league=Abyss': 'flasks',
                  'https://poe.ninja/api/Data/GetUniqueWeaponOverview?league=Abyss': 'weapons',
                  'https://poe.ninja/api/Data/GetUniqueArmourOverview?league=Abyss': 'armors',
                  'https://poe.ninja/api/Data/GetUniqueAccessoryOverview?league=Abyss': 'accessories'}

# Connecting to poe.ninja API and get JSON-data
def update_html_json(league=League.STANDARD):
    # List JSON-items
    json_items = {}

    if league is League.STANDARD:
        urls = URLS_STANDARD
        print('Updating data for Standard league')
    else:
        urls = URLS_CHALLENGE
        print('Updating data for Challenge league')

    http = urllib3.PoolManager()

    # Get current time for get actually JSON data
    current_time = str(datetime.now().year) + '-' + str(datetime.now().month) + '-' + str(datetime.now().day)

    # For every urls getting html-data from poe.ninja and parse them
    for url, filename in urls.items():
        # Load page from url
        print("Loading \"" + url + "\" ...")
        response = http.request('GET', url + '&date=' + current_time)

        # Load JSON-data from response
        data = json.loads(response.data.decode('utf-8'))
        json_items[filename] = data

        print("Ok\n")

    return json_items


# For poe.ninja
def parse_json(json_items):
    # Create list_items
    list_items = defaultdict(int)

    print('Parsing data from poe.ninja')

    # Get item_type and it JSON data. Example item_type: armory, weapons, ...
    for item_type, json_data in json_items.items():
        for element in json_data.items():
            list_cur_items = element[1]
            for item in list_cur_items:
                list_items[item['name']] = item['chaosValue']
            print(item_type + ': ' + str(len(list_cur_items)))
    return list_items


# Recursive get all files path in directory
def listFilesInDir(directory, files):
    print('Get file list from ' + directory)
    for filename in os.listdir(directory):
        filename = directory + "/" + filename
        if os.path.isfile(filename):
            files.append(filename)
        elif os.path.isdir(filename):
            listFilesInDir(filename, files)
    return files
