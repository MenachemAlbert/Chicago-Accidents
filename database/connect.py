from pymongo import MongoClient

client = MongoClient('mongodb://172.22.132.178:27017')
chicago_accidents = client['Chicago_Accidents']

daily = chicago_accidents['daily']
weakly = chicago_accidents['weakly']
monthly = chicago_accidents['monthly']
areas = chicago_accidents['areas']
