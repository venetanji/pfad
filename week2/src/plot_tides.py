import matplotlib.pyplot as plt
import pandas as pd
import chardet


#public
loc = 'C:\\Users\Gao\Documents\\assignment\week2\src\Private_Data\9999.HK_historical_data.xlsx'

#encoding
# with open (loc,'rb') as f:
#     encode1 = chardet.detect(f.read())['encoding']

# data_location

df = pd.read_excel(loc,usecols=['Date','Close'])
Xaxis = df['Date']
Yaxis = df['Close']


print(Xaxis)

#draw
plt.plot(Xaxis,Yaxis)
plt.show()


#encoding_xls



#data = []

