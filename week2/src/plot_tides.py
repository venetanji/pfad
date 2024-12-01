# warning: it seems like some memory leak , I do not know how to fix it
import threading
import time

import matplotlib.pyplot as plt
import pandas as pd
from dotenv import dotenv_values

from week2.src.scraping_utils import scrap
from functools import wraps
page = 2 # page amounts

#import environment variable
env_vars = dotenv_values('.env')
targetXLS =env_vars['XLS_container']
#style setting
plt.figure(figsize=(15, 6), dpi=100 ,)
# data_location



'''function'''
lock = threading.Lock()
'''ensure the thread safety'''
def thread_lock(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        lock.acquire()
        try:
            result = func(*args, **kwargs)
        finally:
            lock.release()
        return result
    return wrapper

def repeat_1000(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        results = []
        for _ in range(200):
            results.append(func(*args, **kwargs))
            time.sleep(0.02)
        return results
    return wrapper

'''decorate end'''
@repeat_1000
@thread_lock
def scrap_wrapper():
    print('Executive function scrap')
    return scrap()

@repeat_1000
@thread_lock
def draw():
    print('Executive function Draw')
    df = pd.read_excel(targetXLS,usecols=['Symbol','Amount'])
    Xaxis = df['Symbol']
    Yaxis = df['Amount']

    #draw
    plt.bar(Xaxis,Yaxis)
    plt.show()


'''Threading pool'''
thread1 = threading.Thread(target=scrap_wrapper)
thread2 = threading.Thread(target=draw)

"""Main"""
if __name__ == '__main__':
    thread1.start()
    thread2.start()


