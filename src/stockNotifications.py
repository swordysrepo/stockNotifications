# -*- coding: utf-8 -*-
"""
Created on Sat Apr 24 19:28:47 2021

@author: swordysrepo
"""
import bs4 
import bs4 as BeautifulSoup
import lxml
import stockquotes
import time
from win10toast import ToastNotifier
toaster = ToastNotifier()

from datetime import datetime

from threading import Thread
import threading


#custom files
import constants
from constants import *
import config 
from config import *

class stock_check():
    def __init__(self):
        self.price_changes = {}
        self.run_updates()
        
        pass
    def set_price(self,STOCK,STOCK_price):
        try:
            old_price = self.price_changes[STOCK]["current_price"]
        except:
            self.price_changes[STOCK] = {"current_price":STOCK_price}
            old_price = STOCK_price
        
        self.price_changes[STOCK].update({"current_price":STOCK_price})
        
        return old_price

        pass
    def percentage_change(self,STOCK,STOCK_price):
        old_price = self.set_price(STOCK,STOCK_price)
        
        return ((old_price - STOCK_price ) / old_price * 100),old_price
    
    def update_and_alert(self,STOCK,STOCK_price):
        
        percentage_change,old_price = self.percentage_change(STOCK,STOCK_price)
        
        if percentage_change >= PERCENTAGE_TO_ALERT:
            self.send_alert(STOCK,STOCK_price, old_price, percentage_change)
            self.send_notification(STOCK,STOCK_price, old_price, percentage_change)
 
        else:
            # self.send_alert(STOCK,STOCK_price, old_price,percentage_change)
            self.send_notification(STOCK,STOCK_price, old_price , percentage_change)
            
            
    def send_alert(self,STOCK,STOCK_price, old_price,percentage_change):
        '''to be used when the stock has
        increased at least the specified amoutn
        within the period of time
        desktop notification
        and sound
        '''
        
        pass
    def send_notification(self,STOCK,STOCK_price, old_price,percentage_change):
        '''sending basic desktop notification '''
        
        if DESKTOP_NOTIFICATIONS == True:
            status = self.pos_neg(percentage_change)
            toaster.show_toast("Stock {STOCK}",\
            f"stock {STOCK} has {status}\n\
            {percentage_change} % \n\
            PRICE : {STOCK_price} PREVIOUS : {old_price}\
            ",
            icon_path=None,
            duration=5,
            threaded=True)
            print("got here")
            # Wait for threaded notification to finish
            while toaster.notification_active(): time.sleep(0.1)
        
        
    def pos_neg(self,n):
        '''checks whether nubmer is positive or negative '''
        if n > 0:
            return "increased"
        else:
            return "decreased"
            
        
        

    def run_updates(self):
        while True:
            stock_count  = len(STOCKS_TO_CHECK)
            current_stock = 0
            for STOCK in STOCKS_TO_CHECK:
                current_stock += 1
                STOCK_INSTANCE = stockquotes.Stock(STOCK)
                STOCK_price = STOCK_INSTANCE.current_price
                self.update_and_alert(STOCK,STOCK_price)
                print(f"reporting {STOCK} price : {STOCK_price}\n##############################\n")
                print(f"printed {current_stock} stock of the list. remaining : {stock_count - current_stock}")
                today_time = datetime.now()
                print(f"waiting {REFRESH_TIME} seconds .. at time : {today_time.strftime('%H:%M:%S')}\n")
                # print(f"waiting {REFRESH_TIME} seconds .. at {datetime.now()}")
        
            time.sleep(REFRESH_TIME)
            
if __name__ == "__main__":
    stock = stock_check()

    


