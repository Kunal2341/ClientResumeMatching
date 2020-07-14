# Username - KunalResumeSkill
# Password - VDartDigital123!
# Database name - skills
# Collection name - skillsCollection
import pymongo
from  pymongo import MongoClient

cluster = MongoClient("mongodb+srv://KunalResumeSkill:VDartDigital123!@cluster0.tuvxg.mongodb.net/skills?retryWrites=true&w=majority")

db = cluster["skills"]
collection = db["skillsCollection"]



post = {"_id": 0, "name": "tim", "score": 5}

#collection.insert_one(post)
#collection.insert_many([post1, post2])


results = collection.find({"name" : "tim"})
for result in results:
    print(result)
results = collection.find({})
for result in results:
    print(result)
