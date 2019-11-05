import requests  
import datetime
from time import sleep

from openapi_client import openapi
from datetime import datetime, timedelta
from pytz import timezone
from matplotlib import pyplot as plt
from datetime import *
from datetime import timedelta
from dateutil.tz import tzutc
import random
import time
import json
import seaborn as sns
from threading import Thread

#8dd805eb8832dd154ace676690
#7b}RnA6%

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=10):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        resp = requests.get(self.api_url + method, params)
        result_json = resp.json()['result']
        return result_json

    def send_message(self, chat_id, text):
        params = {'chat_id': chat_id, 'text': text}
        method = 'sendMessage'
        resp = requests.post(self.api_url + method, params)
        return resp

    def get_last_update(self):
        get_result = self.get_updates()

        if len(get_result) > 0:
            last_update = get_result[-1]
            flag = True
        else:
            flag = False

        return last_update, flag

class MyThread(Thread):
    def __init__(self, interval, func, delta):
        Thread.__init__(self)
        self.interval = interval
        self.func = func
        self.delta = delta
    
    def run(self):
        while(1):
            time.sleep(self.interval)
            for key in figi:
                dif = self.func(figi[key])
                if abs(dif) >= self.delta:
                    for chat_id in user_ids:
                        greet_bot.send_message(chat_id, key +"  " + str(dif) + '%')

def create_threads(funcs, intervals, deltas):
    for i in range(len(funcs)):
        name = "Thread #%s" % (i+1)
        my_thread = MyThread(intervals[i], funcs[i], deltas[i])
        my_thread.start()
        print ('Tread', name, 'started')


def min15_dif(figi):
    ans = client.market.market_candles_get(figi = figi, 
                                     _from = (datetime.now() - timedelta(minutes=20) - time_shift).isoformat()+'+03:00',
                                     to = (datetime.now() - time_shift).isoformat()+'+03:00' ,
                                     interval = '15min')

    try:
        ans = ans.to_dict()['payload']['candles'][-1]
        print('min 15 requesting')
        return (ans['c'] - ans['o'])/ans['o'] * 100
    except:
        return 0    
def hour_dif(figi):
    ans = client.market.market_candles_get(figi = figi, 
                                     _from = (datetime.now() - timedelta(minutes=90) - time_shift).isoformat()+'+03:00',
                                     to = (datetime.now() - time_shift).isoformat()+'+03:00' ,
                                     interval = 'hour')

    try:
        ans = ans.to_dict()['payload']['candles'][-1]
        return (ans['c'] - ans['o'])/ans['o'] * 100
    except:
        return 0  
def day_dif(figi):
    ans = client.market.market_candles_get(figi = figi, 
                                     _from = (datetime.now() - timedelta(hours=25) - time_shift).isoformat()+'+03:00',
                                     to = (datetime.now() - time_shift).isoformat()+'+03:00' ,
                                     interval = 'day')

    try:
        ans = ans.to_dict()['payload']['candles'][-1]
        return (ans['c'] - ans['o'])/ans['o'] * 100
    except:
        return 0 
def week_dif(figi):
    ans = client.market.market_candles_get(figi = figi, 
                                     _from = (datetime.now() - timedelta(days=8) - time_shift).isoformat()+'+03:00',
                                     to = (datetime.now() - time_shift).isoformat()+'+03:00' ,
                                     interval = 'week')

    try:
        ans = ans.to_dict()['payload']['candles'][-1]
        return (ans['c'] - ans['o'])/ans['o'] * 100
    except:
        return 0 

token_telegram = '860172291:AAHehQPDO-oFSsLnVmNvm1hPLqqKS2InWwg'
greet_bot = BotHandler(token_telegram)  

token_sandbox = 't.rxYo9fDNVFHA52jYHq9pOl4bWaQV5C-AqJLg5KxExzPyk8SLIFWcPorKjrzel2w53S9AZsJRArSpRqZxiZAG9A'
client = openapi.sandbox_api_client(token_sandbox)

user_ids = set()
figi = {}

funcs = [min15_dif, hour_dif, day_dif, week_dif]
intervals = [60 * 5, 60 * 20, 60 * 60 * 8, 60 * 60 * 24]
deltas = [3, 5, 5, 7]

time_shift = timedelta(hours=8)

def main():  
    #get figies
    stocks = client.market.market_stocks_get().to_dict()['payload']['instruments']
    for stock in stocks:
        figi[stock['name']] = stock['figi']

    #set client params
    client.sandbox.sandbox_clear_post()
    client.sandbox.sandbox_register_post()
    client.sandbox.sandbox_currencies_balance_post(sandbox_set_currency_balance_request={"currency": "USD", "balance": 1000})

    #create a thread for each function
    create_threads(funcs, intervals, deltas)

    new_offset = None
    while True:
        greet_bot.get_updates(new_offset)

        data, flag = greet_bot.get_last_update()
        
        if flag:
            update_id = data['update_id']
            chat_id  = data['message']['chat']['id']
        

            if not(chat_id in user_ids):
                print(len(chat_id),'users')
                user_ids.add(chat_id)
                
            sleep(1)   
            new_offset = update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()