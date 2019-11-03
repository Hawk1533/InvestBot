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

class BotHandler:

    def __init__(self, token):
        self.token = token
        self.api_url = "https://api.telegram.org/bot{}/".format(token)

    def get_updates(self, offset=None, timeout=10):
        method = 'getUpdates'
        params = {'timeout': timeout, 'offset': offset}
        print(self.api_url+method, params)
        resp = requests.get(self.api_url + method, params)

        result_json = resp.json()['result']
        print(result_json)
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
            last_update = get_result[len(get_result)]
            flag = False

        return last_update, flag

class MyThread(Thread):
    def __init__(self, interval, func):
        Thread.__init__(self)
        self.interval = interval
        self.func = func
    
    def run(self):
        while(1):
            time.sleep(self.interval)
            for key in figi:
                dif = self.func(figi[key])
                print(dif)
                for chat_id in user_ids:
                    greet_bot.send_message(chat_id, key + str(dif) + '%')

def create_threads(funcs, intervals):
    for i in range(len(funcs)):
        name = "Thread #%s" % (i+1)
        my_thread = MyThread(intervals[i], funcs[i])
        my_thread.start()
        print ('Tread', name, 'started')

def min1_dif(figi):
    ans = client.market.market_candles_get(figi = figi, 
                                     _from = (datetime.now() - timedelta(minutes=2)).isoformat()+'+03:00',
                                     to = datetime.now().isoformat()+'+03:00' ,
                                     interval = '1min')

    try:
        ans = ans.to_dict()['payload']['candles'][0]
        return (ans['c'] - ans['o'])/ans['o'] * 100
    except:
        return -1
    

token_telegram = '860172291:AAHehQPDO-oFSsLnVmNvm1hPLqqKS2InWwg'
greet_bot = BotHandler(token_telegram)  

token_sandbox = 't.rxYo9fDNVFHA52jYHq9pOl4bWaQV5C-AqJLg5KxExzPyk8SLIFWcPorKjrzel2w53S9AZsJRArSpRqZxiZAG9A'
client = openapi.sandbox_api_client(token_sandbox)
client.sandbox.sandbox_clear_post()
client.sandbox.sandbox_register_post()
client.sandbox.sandbox_currencies_balance_post(sandbox_set_currency_balance_request={"currency": "USD", "balance": 1000})
figi = {'yandex': 'BBG006L8G4H1'}

user_ids = set()

def main():  
    funcs = [min1_dif]
    intervals = [10]
    create_threads(funcs, intervals)



    new_offset = None
    while True:
        greet_bot.get_updates(new_offset)

        data, flag = greet_bot.get_last_update()
        print(flag)
        
        if flag:
            update_id = data['update_id']
            chat_id  = data['message']['chat']['id']
        

            if not(chat_id in user_ids):
                print('New user', chat_id)
                user_ids.add(chat_id)

            try:
                print(1)
                #payload = {'key':yt_token,'text': data['message']['text'],'lang':'ru-en'}
                #translate = requests.post("https://translate.yandex.net/api/v1.5/tr.json/translate",data=payload).json()['text']
                #greet_bot.send_message(chat_id, translate)
            except:
                greet_bot.send_message(chat_id, "Err")
                
            sleep(1)   
            new_offset = update_id + 1

if __name__ == '__main__':  
    try:
        main()
    except KeyboardInterrupt:
        exit()