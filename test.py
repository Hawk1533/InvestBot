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

figi = {'yandex': 'BBG006L8G4H1'}

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
            	print (key, dif, "%")



def min1_dif(figi):
    ans = client.market.market_candles_get(figi = figi, 
                                     _from = (datetime.now() - timedelta(minutes=2)).isoformat()+'+03:00',
                                     to = datetime.now().isoformat()+'+03:00' ,
                                     interval = '1min')

    
    ans = ans.to_dict()['payload']['candles'][0]

    return (ans['c'] - ans['o'])/ans['o'] * 100


def create_threads(funcs, intervals):
    for i in range(len(funcs)):
        name = "Thread #%s" % (i+1)
        my_thread = MyThread(intervals[i], funcs[i])
        my_thread.start()
    





if __name__ == "__main__":
	token_prod = 't.7NtUAgpCETQULN320S0FRJa5brFuWiMljw3iO39L1O1km1b5kmHNwESb1zZMU_4mWQ_t_AbCtsIrEd0Rx-uCVA'
	token_sandbox = 't.rxYo9fDNVFHA52jYHq9pOl4bWaQV5C-AqJLg5KxExzPyk8SLIFWcPorKjrzel2w53S9AZsJRArSpRqZxiZAG9A'

	token = token_sandbox
	client = openapi.sandbox_api_client(token)
	client.sandbox.sandbox_clear_post()
	client.sandbox.sandbox_register_post()
	client.sandbox.sandbox_currencies_balance_post(sandbox_set_currency_balance_request={"currency": "USD", "balance": 1000})



	funcs = [min1_dif]
	intervals = [10]
	create_threads(funcs, intervals)