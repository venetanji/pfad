import requests
from lxml import html

import dotenv
import os
import datetime
import matplotlib.pyplot as plt
from scraping_utils import get_url, parse

# load the environment variables
dotenv.load_dotenv('../../week1/src/.env')

year = int(os.getenv('YEAR', 2024))
filename = os.getenv('FILENAME', "crawled-page-{year}.html").format(year=year)

# get page
page = get_url(os.getenv('URL'), filename)

# parse the page to html
tree = parse(page, 'html')

data = []

# initialize row counter
row_num = 0

for row in tree.xpath(os.getenv('ROW_XPATH')):
    columns = row.xpath(os.getenv('COL_XPATH'))
    columns = [column.text_content() for column in columns]
    columns = [column.strip() for column in columns]
    row_string = " ".join(columns).strip()

    # skip empty rows
    if row_string.strip() == "":
        continue

    row_num += 1

    print(f'Row {row_num}: {row_string}')

    month = int(columns[0])
    day = int(columns[1])
            
    for i in range(2, len(columns), 2):
        if columns[i] != "":
            # get the time in HHMM format
            hour = columns[i][:2]
            minute = columns[i][2:]

            dt = datetime.datetime(year,month,day,int(hour),int(minute))
            value = columns[i+1]
            print(f'{dt} - {value}')
            data.append((dt, value))            

# create csv file
for record in data:
    print(f'{record[0].strftime("%Y-%m-%d %H:%M")},{record[1]}')
    with open('tides.csv', 'a') as f:
        f.write(f'{record[0].strftime("%Y-%m-%d %H:%M")},{record[1]}\n')