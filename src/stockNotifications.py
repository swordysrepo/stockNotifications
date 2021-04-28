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
# import datetime
from threading import Thread
import threading

import mysql.connector
from mysql.connector import errorcode
#custom files
import constants
from constants import *
import config
from config import *

import sys

from datetime import datetime, timedelta

class checkAlert:
    def __init__(self):
        '''debugging can be turned off with check.debug = False '''
        self.debug=True

    # def alert():
    #     currentline=
    #     print(currentline)
    # def check(self,msg = None):
    #     print(f"check/debug {sys._getframe().f_back.f_lineno}: {msg if msg is not None else ''}")
    def check(self,msg = None):#this sends when debug is enabled
        if self.debug==True:
            msg=str(msg)
            print(f"check/debug {sys._getframe().f_back.f_lineno}: {msg if msg is not None else ''}")
    def check1(msg = None): #this sends whether debug is enabled or not
            msg=str(msg)
            print(f"check/debug {sys._getframe().f_back.f_lineno}: {msg if msg is not None else ''}")
check = checkAlert()


class stock_check():
    def __init__(self):
        self.price_changes = {}
        self.cona = rec()
        self.cona.connect_db()
        self.cona.check_db()
        self.cona.c_table()
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
    def percentage_change(self,STOCK,STOCK_price):
        old_price = self.set_price(STOCK,STOCK_price)
        percentage = (old_price - STOCK_price ) / old_price * 100
        # print(percentage)
        rounded_percentage = round(percentage,3)
        # print(rounded_percentage)
        return rounded_percentage , old_price
    def percentage_change_h(self,STOCK,STOCK_price):
        old_price = self.cona.query_h(STOCK)

        
        percentage = (old_price - STOCK_price ) / old_price * 100
        # print(percentage)
        rounded_percentage = round(percentage,3)
        # print(rounded_percentage)
        return rounded_percentage , old_price 
    def update_and_alert(self,STOCK,STOCK_price):
        percentage_change_hour , h_price_start = self.percentage_change_h(STOCK,STOCK_price)

        percentage_change,old_price = self.percentage_change(STOCK,STOCK_price)
        # print(percentage_change)
        if percentage_change >= PERCENTAGE_TO_ALERT:
            self.send_alert(STOCK,STOCK_price, old_price, percentage_change , percentage_change_hour , h_price_start)
            self.send_notification(STOCK,STOCK_price, old_price, percentage_change , percentage_change_hour , h_price_start)

        else:
            # self.send_alert(STOCK,STOCK_price, old_price,percentage_change)
            self.send_notification(STOCK,STOCK_price, old_price , percentage_change ,percentage_change_hour , h_price_start)


    def send_alert(self,STOCK,STOCK_price, old_price,percentage_change,\
                   percentage_change_hour , h_price_start):
        '''to be used when the stock has
        increased at least the specified amoutn
        within the period of time
        desktop notification
        and sound
        '''
        pass
    def send_notification(self,STOCK,STOCK_price, old_price,percentage_change\
                          ,  percentage_change_hour , h_price_start):
        '''sending basic desktop notification '''

        if DESKTOP_NOTIFICATIONS == True:
            status = self.pos_neg(percentage_change)
            toaster.show_toast(f"stock {STOCK} has {status}",\
            f"\
{percentage_change} % in {(round(REFRESH_TIME/60))} minute interval \n\
PRICE : {STOCK_price} PREVIOUS : {old_price}\n\
todays change {self.STOCK_INSTANCE.increase_percent}%\n\
hourly change {percentage_change_hour}% -- hour start {h_price_start}\n\
            ",
            icon_path=None,
            duration=12,
            threaded=True)
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

                self.STOCK_INSTANCE = stockquotes.Stock(STOCK)
                STOCK_price = self.STOCK_INSTANCE.current_price
                self.update_and_alert(STOCK,STOCK_price)
                self.cona.i_table(STOCK_price,STOCK)




                print(f"reporting {STOCK} price : {STOCK_price}\n##############################\n")
                print(f"printed {current_stock} stock of the list. remaining : {stock_count - current_stock}")
               
                today_time = datetime.now()
                print(f"waiting {REFRESH_TIME} seconds .. at time : {today_time.strftime('%H:%M:%S')}\n")

            time.sleep(REFRESH_TIME)



class rec():
    def __init__(self):
        # self.connect_db()
        pass
    def log_h(self):
        pass
    def read_h(self):
        pass
    def connect_db(self):
        try:         
          self.cnx = mysql.connector.connect(user='root',
                                        database=DB_NAME)
          check.check(f"successful connection to {DB_NAME}")
        except mysql.connector.Error as err:
          if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
          elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
          else:
            print(err)
        # else:
        #     check.check("closing connection")
        #     self.cnx.close()
    
    def create_db(self):
        try:
            self.cursor.execute(
                f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
    def check_db(self):
        check.check("trying connection")
        self.cursor = self.cnx.cursor()

        try:
            self.cursor.execute(f"USE {DB_NAME}")
            check.check(f"using database {DB_NAME}")
        except mysql.connector.Error as err:
            print(f"Database {DB_NAME} does not exists.")
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                create_database(self.cursor)
                print("Database {DB_NAME} created successfully.")
                self.cnx.database = DB_NAME
            else:
                print(err)
                exit(1)

    def query_h(self,STOCK):
        
        # query = ("SELECT first_name, last_name, hire_date FROM employees "
        #          "WHERE hire_date BETWEEN %s AND %s")
        stock_name = STOCK
        query = ("SELECT stock_price, stock_time FROM stock_track "
                 "WHERE stock_time BETWEEN %s AND %s AND stock_name = %s")
         
        
        
        # print(last_hour_date_time.strftime('%Y-%m-%d %H:%M:%S'))
        past_h_s = datetime.now() - timedelta(hours = 1) #past hour start
        past_h_e = datetime.now() #past hour end
        
        self.cursor.execute(query, (past_h_s, past_h_e, STOCK))
        entries = 0
        stock_prices = []
        for (stock_price,stock_time) in self.cursor:
                entries+=1
                stock_prices.append(stock_price)
                stock_time = stock_time.strftime("%H:%M:%S")
                print(f"pricing {stock_price} at {stock_time} for {STOCK}")
            
                
        print(f"{entries} entries found for this past hour.. populating new")
        check.check(f"the oldest entry for this hour is {stock_prices[0]}")
        return stock_prices[0]
    
    
    def c_table(self):
        
        
        
        self.cursor.execute('CREATE TABLE IF NOT EXISTS stock_track (stock_price FLOAT,\
                            stock_time DATETIME,stock_name varchar(30))')
        check.check("table exists")
        
        
    def i_table(self,stock_price,STOCK):
        ''' insert data to table '''
        check.check(f"inserting {stock_price} into the {STOCK} tables' data ")
        c_time = datetime.now()
        a_price = ("INSERT INTO stock_track "
               "(stock_price, stock_time,stock_name) "
               "VALUES (%s, %s , %s)")
        data_stock = (stock_price , c_time , STOCK)
        self.cursor.execute(a_price , data_stock)
        self.cnx.commit()


class news():
    def __init__(self):
        '''uses websites from constants file to find relevant websites '''
        self.r_web = RELEVANT_WEBSITES
        self.phonenum = SMS_NUMBERS
        pass
    def c_google_7(self):
        '''check google for past 7 days '''
        pass
    def c_google_24(self):
        '''check google for past 24 hours '''
        pass
if __name__ == "__main__":
    stock = stock_check()
    
    

    


