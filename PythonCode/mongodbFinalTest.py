# Username - KunalResumeSkill
# Password - VDartDigital123!
# Database name - skills
# Collection name - skillsCollection
import pymongo
from  pymongo import MongoClient

cluster = MongoClient("mongodb+srv://KunalResumeSkill:VDartDigital123!@cluster0.tuvxg.mongodb.net/skills?retryWrites=true&w=majority")
db = cluster["skills"]
collection = db["skillsCollection"]

collection.insert_one({})
collection.insert_many([{},{}])


results = collection.find({"skillName": "10BASE-T"})
resultOne = collection.find_one()
resultDelete = collection.find_one_and_delete()

collection.delete_one()

for result in results:
    print(result)
    print(result["_id"])
