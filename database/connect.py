from pymongo import MongoClient

client = MongoClient('mongodb://172.22.132.178:27017')
Chicago_Accidents = client['Chicago_Accidents']
