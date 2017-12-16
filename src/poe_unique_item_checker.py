import os
import threading
import time
import winsound
from collections import defaultdict
from random import randint
from tkinter import *

import poe_ninja_parser


def find_poe_item(buffer_data):
    # or divination card
    if buffer_data.find('Rarity: Unique') != -1 or buffer_data.find('Rarity: Divination Card') != -1:
        return True
    else:
        return False


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


# Check conditions for buffer
def check_conditions(interval):
    while True:
        buffer_data = window.clipboard_get()
        window.focus_force()
        # print(buffer_data)
        # Parse buffer and run process
        if find_poe_item(buffer_data=buffer_data):
            print('Find poe item')
            # Getting item name
            item_name = get_item_name(buffer_data)
            if items_dic[item_name] > 0:
                print('Item: {}\nPrice: {} chaos'.format(item_name, items_dic[item_name]))
                sound = music_for_good_item[randint(0, len(music_for_good_item) - 1)]
            else:
                print('shit')
                sound = music_for_bad_item[randint(0, len(music_for_bad_item) - 1)]

            winsound.PlaySound(sound, winsound.SND_ASYNC | winsound.SND_ALIAS)

            # Clear buffer
            window.clipboard_clear()
            window.clipboard_append('')

        time.sleep(interval)


# Get item name
def get_item_name(buffer_data):
    list_params = buffer_data.split('\n')
    return list_params[1]


# Get data from source file and creating dictionary of items
def get_data():
    # Read source files
    divinations_dic = poe_ninja_parser.divination_format_html(filename='../resources/html/divinations.html',
                                                              price_filters=[10000000, 5])
    weapons_dic = poe_ninja_parser.weapons_format_html(filename='../resources/html/weapons.html',
                                                       price_filters=[10000000, 5])
    armors_dic = poe_ninja_parser.weapons_format_html(filename='../resources/html/armors.html',
                                                      price_filters=[10000000, 5])
    flasks_dic = poe_ninja_parser.flasks_format_html(filename='../resources/html/flasks.html',
                                                     price_filters=[10000000, 5])
    accessories_dic = poe_ninja_parser.accessories_format_html(filename='../resources/html/accessories.html',
                                                               price_filters=[10000000, 5])
    jewels_dic = poe_ninja_parser.jewels_format_html(filename='../resources/html/jewels.html',
                                                     price_filters=[10000000, 5])

    maps_dic = poe_ninja_parser.jewels_format_html(filename='../resources/html/maps.html',
                                                   price_filters=[10000000, 5])

    # Creating one dictionary
    items_dic.update(divinations_dic)
    items_dic.update(weapons_dic)
    items_dic.update(armors_dic)
    items_dic.update(flasks_dic)
    items_dic.update(accessories_dic)
    items_dic.update(jewels_dic)
    items_dic.update(maps_dic)


# Run function check_conditions in thread
def start(event):
    # Get data from source
    get_data()
    window.withdraw()
    t = threading.Thread(target=check_conditions, args=(1,))
    t.daemon = True
    t.start()


# Set variables
buffer_data = ''
# interval = 15.0  # seconds
t = None

# Full good item list
items_dic = defaultdict(int)

# Set music
music_for_good_item = listFilesInDir('../resources/sounds/good', [])
music_for_bad_item = listFilesInDir('../resources/sounds/bad', [])

# Create window
window = Tk()
window.geometry("300x200+100+100")

# Create button
button = Button(window, text='Start')
button.pack(expand='YES')
button.bind('<Button-1>', start)

# Run window
window.mainloop()
