
import requests # for making standard html requests
from bs4 import BeautifulSoup # magical tool for parsing html data
import json # for parsing data
from pandas import DataFrame as df # premier library for data organization
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

def listofSkills(link, id):
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
        tempList = [HREF,nameOfSkill, id]
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
count = 1
for i in webLink_List:
    test = listofSkills(i, count)
    ALLSKILLSLIST+=test
    count+=1
#print("/n", ALLSKILLSLIST)
#SKILLSDF = pd.DataFrame(ALLSKILLSLIST, columns=["HREF", "Skill Name", "ID"])
#writer = pd.ExcelWriter('output.xlsx')
from firebase import firebase
firebase = firebase.FirebaseApplication("https://resumematcher-8706e.firebaseio.com/", None)
resultofUpload = []
for i in ALLSKILLSLIST:
    name = i[1]
    data = {
        'HREF': i[0],
        'Skill_name': i[1],
        'ID': i[2],
    }
    result = firebase.post("Skills", data)
    resultofUpload.append(result)
print(resultofUpload)
print("DONE")