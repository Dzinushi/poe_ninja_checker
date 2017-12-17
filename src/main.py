import os
import threading
import time
import winsound
from random import randint
from tkinter import *

import utils


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
    window.clipboard_clear()
    window.clipboard_append('poe.ninja checker_(by Dzinushi)')

    global items_dic

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


# Run function check_conditions in thread
def start(event):
    # Hide window
    window.withdraw()

    global items_dic, rbutton_choose

    if rbutton_choose.get() is 1:
        league = utils.League.STANDARD
    else:
        league = utils.League.CHALLENGE

    # Update data from poe.ninja
    json_data = utils.update_html_json(league)

    # Parse JSON-data
    items_dic = utils.parse_json(json_data)

    # Create thread for main process
    t = threading.Thread(target=check_conditions, args=(1,))
    t.daemon = True
    t.start()


# Set variables
buffer_data = ''

# Set music
music_for_good_item = listFilesInDir('../resources/sounds/good', [])
music_for_bad_item = listFilesInDir('../resources/sounds/bad', [])

# Full item list
items_dic = None

# Create window
window = Tk()
window.geometry("300x200+100+100")

# Create button
button = Button(window, text='Start')
button.pack(expand='YES')
button.bind('<Button-1>', start)

# Create radiobuttons
rbutton_choose = IntVar()
rbutton_standard = Radiobutton(window, text='Standard', variable=rbutton_choose, value=1)
rbutton_standard.pack(expand='YES')
rbutton_challenge = Radiobutton(window, text='Challenge', variable=rbutton_choose, value=2)
rbutton_challenge.pack(expand='YES')

rbutton_choose.set(1)

# Run window
window.mainloop()
