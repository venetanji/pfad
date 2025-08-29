import requests
from lxml import html

import dotenv
import os
import datetime
import matplotlib.pyplot as plt
from scraping_utils import get_url, parse

# load the environment variables
dotenv.load_dotenv()

# get the year and filename from the environment variables
year = int(os.getenv('YEAR', 2024))
filename = os.getenv('FILENAME', "crawled-page-{year}.html").format(year=year)

# get page
page = get_url(os.getenv('URL'), filename)

# parse the page to html
tree = parse(page, 'html')

# initialize the data list
data = []

# initialize row counter
row_num = 0

# iterate over the rows
for row in tree.xpath(os.getenv('ROW_XPATH')):

    # get the columns
    columns = row.xpath(os.getenv('COL_XPATH'))

    # get the text content of each column
    columns = [column.text_content() for column in columns]

    # strip whitespace from each column
    columns = [column.strip() for column in columns]

    # join the columns into a single string
    row_string = " ".join(columns).strip()

    # skip empty rows
    if row_string.strip() == "":
        continue

    # increment the row counter
    row_num += 1

    # print the row
    print(f'Row {row_num}: {row_string}')

    # get the month and day
    month = int(columns[0])
    day = int(columns[1])

    # get the time and value
    for i in range(2, len(columns), 2):

        # check if the column is not empty
        if columns[i] != "":
            
            # get the time in HHMM format
            hour = columns[i][:2]
            minute = columns[i][2:]

            # create the datetime object
            dt = datetime.datetime(year,month,day,int(hour),int(minute))

            # get the value
            value = columns[i+1]

            # print the datetime and value
            print(f'{dt} - {value}')

            # append the datetime and value to the data list
            data.append((dt, value))

# create csv file
for record in data:
    
    # print the record for debugging purposes
    print(f'{record[0].strftime("%Y-%m-%d %H:%M")},{record[1]}')

    # open the csv file
    with open('tides.csv', 'a') as f:

        # write the record to the csv file
        f.write(f'{record[0].strftime("%Y-%m-%d %H:%M")},{record[1]}\n')