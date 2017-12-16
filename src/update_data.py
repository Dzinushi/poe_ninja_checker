from enum import Enum
import unicodedata

from bs4 import BeautifulSoup
from selenium import webdriver

class League(Enum):
    STANDARD = 1
    CHALLENGE = 2


URLS_STANDARD = {'https://poe.ninja/standard/unique-jewels': 'jewels.html',
                 'https://poe.ninja/standard/unique-maps': 'maps.html',
                 'https://poe.ninja/standard/divinationcards': 'divinations.html',
                 'https://poe.ninja/standard/unique-flasks': 'flasks.html',
                 'https://poe.ninja/standard/unique-weapons': 'weapons.html',
                 'https://poe.ninja/standard/unique-armours': 'armors.html',
                 'https://poe.ninja/standard/unique-accessories': 'accessories.html'}

URLS_CHALLENGE = {'https://poe.ninja/challenge/unique-jewels': 'jewels.html',
                  'https://poe.ninja/challenge/unique-maps': 'maps.html',
                  'https://poe.ninja/challenge/divinationcards': 'divinations.html',
                  'https://poe.ninja/challenge/unique-flasks': 'flasks.html',
                  'https://poe.ninja/challenge/unique-weapons': 'weapons.html',
                  'https://poe.ninja/challenge/unique-armours': 'armors.html',
                  'https://poe.ninja/challenge/unique-accessories': 'accessories.html'}

PHANTOMJS_PATH = '../phantomjs-2.1.1-windows/bin/phantomjs.exe'
HTML_PATH = '../resources/html/'


# Updating html-files
def update_html(league=League.STANDARD):
    # Run phantomJS browser to open web-page
    driver = webdriver.PhantomJS(executable_path=PHANTOMJS_PATH)

    if league is League.STANDARD:
        urls = URLS_STANDARD
        print('Updating data for Standard league')
    else:
        urls = URLS_CHALLENGE
        print('Updating data for Challenge league')

    # For every urls getting html-data from poe.ninja and parse them
    for url, filename in urls.items():
        print("Loading \"" + url + "\" ...")
        driver.get(url)
        driver.find_element_by_class_name('outer-container')

        # Finding table with content
        print("Finding table content in page ...")
        soup = BeautifulSoup(driver.page_source, 'lxml')
        body = soup.find('table').contents[1]
        budy_s = str(body)

        # Saving content to file
        print("Saving ...")
        html_file = open(HTML_PATH + filename, encoding='utf-8', mode='w')
        html_file.write(budy_s)
        html_file.close()

        print("Ok\n")

    # Close driver connections
    driver.close()
