import requests
import os
from lxml import html
import json


def get_url(url, filename):
    if not os.path.exists(filename):

        # fetch the page if it doesn't exist
        page = requests.get(url)

        # save the page to a file
        with open(filename, 'w', encoding='UTF8') as f:
            f.write(page.text)

        page = page.text

    else:
        # if the page exists, read it from the file
        with open(filename, 'r', encoding='UTF8') as f:
            page = f.read() 
            
    return page

def parse(page, mode = 'html'):
    match mode:
        case 'html':
            return html.fromstring(page)
        case 'json':
            return json.loads(page)