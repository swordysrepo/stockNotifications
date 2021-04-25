# stockNotifications
Sending notifications about changes in stock prices



this a file utilizing the stockquotes library from kj7rrv on github
found here https://github.com/kj7rrv/stockquotes

to use this project we need to install the stockquotes library using
``` pip3 install stockquotes```





we run our project using 
```python stockNotifications.py``` 
in command prompt

# **Usage:*
## dependencies

- install bs4 ```pip install bs4```
- install win10toast ```pip install win10toast```
- change stocks to collect (inside constants.py file)
- set desktop notification on or off (in config.py file)





## **Features:**

- reports % of change since last query
- desktop notifications<picture of the desktop notification>

- discord notifications (future update)<picture of the discord>
- sound alerts (future update)


## **options:**


  - no notifications (only prints the result in cmd, no update notification)

  - no desktop notifications (prints in cmd and sends alerts (not updates))


## **upcoming update::**

  - adding an overlay for the current stock price

  - sound alerts

  - discord notifications
  - packaging this as one
  - adding percentage change of current hour
  - adding percentage change of the day

  - documentation for custom options inside cmd (instead of editting project files)




