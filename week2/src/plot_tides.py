import matplotlib.pyplot as plt
import pandas as pd
import chardet
from dotenv import dotenv_values
#read environment values
from scraping_utils import get_data

#import environment variable
env_vars = dotenv_values('.env')
targetXLS =env_vars['XLS_container']
#style setting

plt.figure(figsize=(15, 6), dpi=100)
#public
#loc = 'C:\\Users\Gao\Documents\\assignment\week2\src\Private_Data\Table_target.xls'

#encoding
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

if __name__ == '__main__':
    get_data(2)
    draw()



