import pymongo
import pymodm

"""
from pymodm import connect, fields, MongoModel
from pymongo import MongoClient

connect('mongodb://localhost:27017/myDatabase')
client = MongoClient('mongodb://localhost:27017/')

db = client.myDatabase



from pymongo import MongoClient
client = MongoClient("mongodb+srv://Test-User:MongodbVdartPass@cluster0.4pywk.gcp.mongodb.net/test?retryWrites=true&w=majority")
#Create database object called jack
db = client.jack
#Check server status to make sure all is working
ServerStat = db.command("serverStatus")
print(ServerStat)

order = {"Name": "Jack Smart",
        "Order": "Pizza",
        "Price": 15.00
        }
db.Cluster0.inset_one(order)


# import datetime module
import datetime
# import pymongo module
import pymongo
# connection string
client = pymongo.MongoClient("mongodb+srv://gsweene2:MongodbVdartPass@cluster0-obuqd.mongodb.net/test?retryWrites=true&w=majority")
# test
db = client['SampleDatabase']
# define collection
collection = db['SampleCollection']
# sample data
document = {"company":"Capital One",
"city":"McLean",
"state":"VA",
"country":"US"}
# insert document into collection
id = collection.insert_one(document).inserted_id
print("id")
print(id)


import pymongo
client = pymongo.MongoClient("//127.0.0.1:27017")
db = client['SkillsDatabase']

printer_collection = db['printer_collection']
printer_a = {'printer_name': 'X Printer Co', 'printer_model': 231901, 'price': 250.00}
printer_b = {'printer_name': 'X Printer Co', 'printer_model': 938901, 'price': 450.00}
printer_c = {'printer_name': 'Hyper Global Printers Inc', 'printer_model': 901, 'price': 299.00}
results = printer_collection.insert_many([printer_a, printer_b, printer_c])


print(results.inserted_ids)

"""
import pymongo
# Connect to MongoDB instance running on localhost
client = pymongo.MongoClient()

# Access the 'restaurants' collection
# in the 'test' database
collection = client.test.restaurants

new_documents = [
  {
    "name": "Sun Bakery Trattoria",
    "stars": 4,
    "categories": ["Pizza","Pasta","Italian","Coffee","Sandwiches"]
  }, {
    "name": "Blue Bagels Grill",
    "stars": 3,
    "categories": ["Bagels","Cookies","Sandwiches"]
  }
]

collection.insert_many(new_documents)


for restaurant in collection.find():
  pprint.pprint(restaurant)