import matplotlib.pyplot as plt
import pandas as pd
from dotenv import dotenv_values
from twisted.conch.ui.tkvt100 import fontWidth

#read environment values
from scraping_utils import get_data
from week2.src.scraping_utils import scrap

page = 2 # page amounts

#import environment variable
env_vars = dotenv_values('.env')
targetXLS =env_vars['XLS_container']
#style setting

plt.figure(figsize=(15, 6), dpi=100 ,)


urls =[f"https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={page}&size=100&type=sha&order_by=percent&order=desc"
      for page in range(1,10)
]
# with open (loc,'rb') as f:
#     encode1 = chardet.detect(f.read())['encoding']

# data_location
def draw():
    df = pd.read_excel(targetXLS,usecols=['Symbol','Amount'])
    Xaxis = df['Symbol']
    Yaxis = df['Amount']

    #draw
    plt.bar(Xaxis,Yaxis)
    plt.show()

"""Main"""
if __name__ == '__main__':
    scrap()
    draw()



