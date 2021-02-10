import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data
from pandas import DataFrame as df # premier library for data organization
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import ast
import pymongo
from  pymongo import MongoClient
# Username - KunalResumeSkill
# Password - VDartDigital123!
# Database name - skills
# Collection name - skillsCollection

def listofSkills(link):
    URL = link
    page = requests.get(URL)
    page.encoding = 'ISO-885901'
    soup = BeautifulSoup(page.text, 'html.parser')
    dollar_tree_list = soup.find_all(class_ = 'col-md-3')
    del dollar_tree_list[-1]
    DataCollected = []
    for i in dollar_tree_list:
        example = i
        content = example.contents
        attrs = content[1].attrs
        try:
            HREF = content[1]['href']
            #print(example_href)
        except KeyError as e:
            print(e)
        nameOfSkill = clearName(HREF)
        tempListMORECONTENT = [content, attrs, HREF,nameOfSkill]
        tempList = [HREF,nameOfSkill]
        DataCollected.append(tempList)
    return DataCollected


def clearName(link):
    text = link.replace("/skills/","").replace("+"," ").replace("%26%2347", "/").replace("%27", "'").replace("%26%2345","-")
    return text

alpha_list = [chr(x) for x in range(ord('a'), ord('z') + 1)]
number_list = ["1","2","3","4","5"]
FinalList = number_list+alpha_list
webLink_List = []
for i in FinalList:
    webLink_List.append("https://www.dice.com/skills/browse/"+i)
#print(webLink_List)

ALLSKILLSLIST = []
for i in webLink_List:
    test = listofSkills(i)
    ALLSKILLSLIST+=test

SKILLSDF = pd.DataFrame(ALLSKILLSLIST, columns=["HREF", "Skill Name"])

writer = pd.ExcelWriter('output2.xlsx')
SKILLSDF.to_excel(writer,'Sheet1')
writer.save()
def GetName(text):
    ini_string = text
    c = ">"
    res = None
    for i in range(0, len(ini_string)):
        if ini_string[i] == c:
            res = i + 1
            break
    finalText = ini_string[res:]
    finalText = finalText.replace("</div>", "")
    return finalText
def MainClosestSkill(virus):
    return '(204, 204, 204)' in virus
def numberOfSkills(driver):
    for i in range(100):
        num = i+1
        maxnum = 1
        try:
            driver.find_element_by_id(str(num))
        except:
            maxnum = num-1
            break
    CONNECTEDSKILLLIST = []
    for i in range(maxnum):
        CONNECTEDSKILLLIST.append(i+1)
    return CONNECTEDSKILLLIST
def CloseSkillsTotal(link, driver):
    # Using Chrome to access web
    # Open the website
    driver.get(link)
    NumberOfSkillsList = numberOfSkills(driver)
    CLOSESKILLTOTAL =[]
    for i in NumberOfSkillsList:
        SKILL = driver.find_element_by_id(str(i))
        SKILLNAME = SKILL.text
        source_code = SKILL.get_attribute("outerHTML")
        #print(SKILLNAME)
        if SKILLNAME == '':
            SKILLNAME =  GetName(source_code)
            #print("YES", source_code)
        closeSkill = MainClosestSkill(source_code)
        #print(closeSkill)
        #True if close skill and far for other
        temp_List = [SKILLNAME, closeSkill]
        CLOSESKILLTOTAL.append(temp_List)
    #print(CLOSESKILLTOTAL)
    return CLOSESKILLTOTAL
cluster = MongoClient("mongodb+srv://KunalResumeSkill:VDartDigital123!@cluster0.tuvxg.mongodb.net/skills?retryWrites=true&w=majority")
db = cluster["skills"]
collection = db["skillsCollection"]
jsonFileStr = """

{
    "skillName": "sNCode",
    "url": "UCode",
    "relation" : [
        {
            "skill_a" : {
                "relatedSkill_a1" : "rS_a1Code", 
                "relatedSkill_a2" : "rS_a2Code",
                "relatedSkill_a3" : "rS_a3Code",
                "relatedSkill_a4" : "rS_a4Code",
                "relatedSkill_a5" : "rS_a5Code"
            }, 
            "skill_b" : {
                "relatedSkill_b1" : "rS_b1Code", 
                "relatedSkill_b2" : "rS_b2Code",
                "relatedSkill_b3" : "rS_b3Code",
                "relatedSkill_b4" : "rS_b4Code",
                "relatedSkill_b5" : "rS_b5Code"
            },
            "skill_c" : {
                "relatedSkill_c1" : "rS_c1Code", 
                "relatedSkill_c2" : "rS_c2Code",
                "relatedSkill_c3" : "rS_c3Code",
                "relatedSkill_c4" : "rS_c4Code",
                "relatedSkill_c5" : "rS_c5Code"
            },
            "skill_d" : {
                "relatedSkill_d1" : "rS_d1Code", 
                "relatedSkill_d2" : "rS_d2Code",
                "relatedSkill_d3" : "rS_d3Code",
                "relatedSkill_d4" : "rS_d4Code",
                "relatedSkill_d5" : "rS_d5Code"
            },
            "skill_e" : {
                "relatedSkill_e1" : "rS_e1Code", 
                "relatedSkill_e2" : "rS_e2Code",
                "relatedSkill_e3" : "rS_e3Code",
                "relatedSkill_e4" : "rS_e4Code",
                "relatedSkill_e5" : "rS_e5Code"
            }
        }
    ]
}"""
print("Finished running 7000")
countn = input("Where do you want to start")
similarSkillsTotalList = []
for i in ALLSKILLSLIST[countn:7000]:
    jsonFileRunning = jsonFileStr
    # print( str(i[0]))
    link = "https://www.dice.com" + str(i[0])
    driver = webdriver.Chrome(ChromeDriverManager().install())
    DATA = CloseSkillsTotal(link, driver)
    driver.close()
    running = True
    if len(DATA) == 0:
        jsonFileRunning = jsonFileStr
        print("ERROR WATCH OUT SKIPPING ", i[0])
        jsonFileRunning = jsonFileRunning.replace("sNCode", i[1]).replace("UCode", i[0])
        letterList = ["a", "b", "c", "d", "e"]
        for i in letterList:
            for j in range(5):
                numb = j + 1
                text = "rS_" + i + str(numb) + "Code"
                jsonFileRunning = jsonFileRunning.replace(text, "n/a")
        running = False
    if running == True:
        skillnameCode = DATA[0][0]
        jsonFileRunning = jsonFileRunning.replace("sNCode", skillnameCode).replace("UCode", str(i[0]))
        if len(DATA) > 1:
            print("Running " + str(countn))
            DATANEW = DATA[1:]
            count = 0
            SkillcountLetter = ["a", "b", "c", "d", "e"]
            Skillcount = 0
            for i in DATANEW:
                if i[1] == True:
                    textString = "skill_" + SkillcountLetter[Skillcount]
                    # print(textString + i[0])
                    relatedSkillcount = 1
                    jsonFileRunning = jsonFileRunning.replace(textString, i[0])
                    for j in range(5):
                        z = j + count + 1
                        textString2 = "rS_" + SkillcountLetter[Skillcount] + str(relatedSkillcount) + "Code"
                        # print(textString2 + str(DATANEW[z][0]))
                        jsonFileRunning = jsonFileRunning.replace(textString2, str(DATANEW[z][0]))
                        relatedSkillcount += 1
                    Skillcount += 1
                count += 1
        else:
            letterList = ["a", "b", "c", "d", "e"]
            for i in letterList:
                for j in range(5):
                    numb = j + 1
                    text = "rS_" + i + str(numb) + "Code"
                    jsonFileRunning = jsonFileRunning.replace(text, "n/a")
    if not jsonFileRunning.find('.') == -1:
        jsonFileRunning = jsonFileRunning.replace('.', '-')
        # print(jsonFileRunning)
    jsonFormatUpload = ast.literal_eval(jsonFileRunning)

    try:
        collection.insert_one(jsonFormatUpload)
        print("Uploaded: \t\t\t", skillnameCode)
    except Exception as e:
        print("ERROR WITH THE UPLOAD TO MONGODB CHECK")
        print(i)
        break
    similarSkillsTotalList.append(DATA)
    countn += 1
    # print(similarSkillsTotalList)
def checkerDNEMULTIPLE():
    DNEL = []
    MultipleL = []
    for i in ALLSKILLSLIST[0:300]:
        results = collection.find({"skillName": str(i[1])})
        count = 0
        printString = ""
        for result in results:
            count += 1
        if count == 0:
            printString = "DNE"
            DNEL.append(i)
            print(str(i[1]) + "\t:\t\t" + printString)
        elif count == 1:
            printString = "Good"
        elif count > 1:
            printString = "Multiple" + str(count)
            MultipleL.append(i)
            print(str(i[1]) + "\t:\t\t" + printString)
    return DNEL, MultipleL
runChecker = input("Run checker?")
if runChecker == "Yes":
    LISTDNE, LISTMULTIPLE = checkerDNEMULTIPLE()

runMultipleremove = input("RUN MULTIPLE REMOVER?")
if runMultipleremove == "Yes":
    for j in LISTMULTIPLE[0:1]:
        results = collection.find({"skillName": str(j[1])})
        counter = 0
        for result in results:
            counter += 1
        # print(counter)
        for i in range(counter):
            if i > 0:
                collection.delete_one({"skillName": str(j[1])})
                print("Deleted: \t" + str(j[1]))
            else:
                print("NOTDELETED: \t" + str(j[1]))

print("FINISHED")