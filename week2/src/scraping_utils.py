import requests
import pandas as pd
from pprint import pprint
from dotenv import dotenv_values
import threading
import time
import random
#read environment values
env_vars = dotenv_values('.env')
targetXLS =env_vars['XLS_container']
data_list=[]

#print(targetXLS)

#url = "https://4.push2delay.eastmoney.com/api/qt/clist/get?cb=jQuery112409776567584598126_1727105507570&pn=1&pz=5&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&dect=1&wbp2u=|0|0|0|web&fid=f11&fs=m:0+t:6,m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f26,f22,f28,f11,f62,f128,f136,f115,f152,f34,f35,f108&_=1727105507581"
#url = "https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=2&size=100&type=sha&order_by=percent&order=desc"
urls =[f"https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page={page}&size=10&type=sha&order_by=percent&order=desc"
      for page in range(1,3)
]

headers = {
        'Cookie':'xq_a_token=927886df384cbb16c88673ae7f519c76650c54b9; xqat=927886df384cbb16c88673ae7f519c76650c54b9; xq_r_token=1d46f0ed628506486164e5055a4993f9b54b2f4c; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcyOTIxMjc4NCwiY3RtIjoxNzI3MTQxNDQ1NjE3LCJjaWQiOiJkOWQwbjRBWnVwIn0.atE1pSOvzrZXwnGxV2T6iSkKLPEalJ8lJd7jKUlxTccwmdzxbywKGqzRwp0zGXxlPQLXlS21xoUIomgkM7LtNboWEfSre9X9EGXZRwaC2slxnpFzf6xD4E7vQFiRq9kLryi9GSp4zsAfJU3_wcYs-Cv27uXW0on9O-V7pveZ9n2zz7CCVul2A-MJp-VBRbxRAMDTv17mATnD7eD4RXFUqoRxlXiGKvROdZ2Wj2QDuOX1BijR8M4yrNLJyCHqZaQk6ol_B23NZOvBKzzw69FfCgo6C7ns7ri-CvqBBq1vgTA3Ot8P8gqqKw1_TP8fhr928lFtP1-48f31hZHuV1Ec1w; cookiesu=341727141459448; u=341727141459448; ssxmod_itna=eqGOGK4UxfOxODzZDUiARhSEiYKDtD9DmuingDDsqQrDSxGKidDqxBWnlxY2e2q5Q7ARxGOi1Yh3beY0RrrP37Olgwx++Ge0aDbqGkKuAPiiyDCeDIDWeDiDGbOD=xGYDjBIz1yDm4i7DiKDpx0kGgI4ZQvkAxGCVxDC2BPDwx0C2rDDBgmTqnexDm+kcgpwqFoDnOW1qQGkD7ypDlPqnbGkrFM6emH16/fAfGFhP40OD09GUxibGaoP26vATCG3NCie/lDYrinDK=DYmmGr+A=FQG/DNY+TAGG4e00xcvR9gTDDigwNqYD=; ssxmod_itna2=eqGOGK4UxfOxODzZDUiARhSEiYKDtD9DmuinDikEeDlp4QId08D+rYD=; device_id=5af4e32f994ba963db092e5a246b57ea; Hm_lvt_1db88642e346389874251b5a1eded6e3=1727141460; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1727141460; HMACCOUNT=BB75758882D6E33E',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'
}

#style

def get_data(url):
    r = requests.get(url, headers=headers)
    json_data = r.json()
    # print(json_data)
    for index in json_data['data']['list']:
        #pprint(index)
        dic = {
            'Symbol': index['symbol'],
            'Amount': index['amount'],
        }
        #pprint(dic)
        #store the data
        data_list.append(dic)



"""test function"""
# for url in urls:
#     get_data(url)
# def test_multiTread(url):
#     print(url)

def multi_thread():
    threads = []
    for url in urls:
        threads.append(
            threading.Thread(target=get_data, args=(url,))
        )
    for thread in threads:
        thread.start()
        print(f"thread {url}begin")
    for thread in threads:
        thread.join()
        pass


def scrap():
    #count time
    start = time.time()
    multi_thread()
    end = time.time()
    print(f'time cost={end-start}s ')
    dl = pd.DataFrame(data_list)
    random.shuffle(data_list)
    dl.to_excel(targetXLS, engine='openpyxl')