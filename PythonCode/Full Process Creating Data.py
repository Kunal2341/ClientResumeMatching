# IMPORT
import os
from pdf2image import convert_from_path
import ntpath
from google.oauth2 import service_account
from google.cloud import vision
import io
import string
import pandas as pd
import ast
import spacy
nlp = spacy.load('en_core_web_sm')
from __future__ import unicode_literals, print_function
from spacy.lang.en import English # updated
# PDF TO TEXT
def convert_pdf_2_image(uploaded_image_path, uploaded_image):
    project_dir = os.getcwd()
    os.chdir(uploaded_image_path)
    file_name = str(uploaded_image).replace('.pdf','')
    pages = convert_from_path(uploaded_image, 200,poppler_path='/Users/kunal/Documents/VdartWorking/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/')
    pageNumCount = 1
    outputNames = []
    for page in pages:
        output_file = file_name+"_"+str(pageNumCount) + '.jpg'
        page.save(output_file, 'JPEG')
        pageNumCount +=1
        outputNames.append(output_file)
    return outputNames
def convert_img_2_text(imagePath):
    keyDIR = "/Users/kunal/Documents/ResumeNLPVdart/APIKEYSGOOGLE/resumeMatcher-pdf2img.json"
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = vision.ImageAnnotatorClient(credentials=credentials)
    with io.open(imagePath, 'rb') as image_file:
        content = image_file.read()
    image = vision.types.Image(content=content)
    response = client.text_detection(image=image)
    texts = response.text_annotations
    totalString = ''
    for text in texts:
        totalString+=text.description
    totalString = totalString.rsplit(' ', 1)[0]
    return totalString
def deleteIMG(path):
    for i in os.listdir(path):
        if i.endswith(".jpg"):
            os.remove(folder_pdf + i)
folder_pdf = '/Users/kunal/Documents/ResumeNLPVdart/Testing_Delete/'
deleteIMG(folder_pdf)
textList = []
numberPagesList = []
folder_pdf = '/Users/kunal/Documents/ResumeNLPVdart/Testing_Delete/'
for i in os.listdir(folder_pdf):
    if os.path.exists(folder_pdf + i[:-4] + ".jpg") == False:
        if i.endswith(".pdf"):
            imgName = convert_pdf_2_image(folder_pdf, i)
            print("Running Number :" + str(len(imgName))) 
            printString = ""
            for docName in imgName:
                printString += docName + " " 
            print(printString)
    for q in range(len(imgName)):
        text = convert_img_2_text(folder_pdf + i[:-4] + "_" + str(q+1) + ".jpg")
        textList.append(text)    
        numberPagesList.append(len(imgName))
# Convert to Excel
df = pd.DataFrame()
df['Text Extracted'] = textList
df['DocumentNum'] = numberPagesList
os.chdir('/Users/kunal/Documents/ResumeNLPVdart/ExcelFilesStorage/')
df.to_excel('test1.xlsx', index = False)
# Read Excel
text = pd.ExcelFile("test1.xlsx")
dftext = text.parse("Sheet1")
text_list = dftext["Text Extracted"].tolist()
pagesList = dftext["DocumentNum"].tolist()
# Check for Recommendation letters
count=0
pageNumberShortList = []
for i in text_list:
    if not count >= len(pagesList):
        pageNumberShortList.append(pagesList[count])
        count+=pagesList[count]
count=0
numb = 0
recNumList=[]
for i in text_list:
    if "Recommendation" in str(i): 
        recNumList.append(numb)
    numb+=1
pageNumberrunning = 1
for q in pageNumberShortList:
    for v in recNumList:
        if pageNumberrunning == v:
            print("asdfjfsdjkf")
    pageNumberrunning +=q
#STILL DOESN"T WORK
 # Converts the text files to an array but still split into pages
totalText = []
for u in range(len(pagesList)):
    textExtracted = ""
    for h in range(pagesList[u]):
        try:
            textExtracted = textExtracted + "\n" + text_list[u]
        except:
            continue
        totalText.append(textExtracted)
totalText = []
for u in range(len(pagesList)):
    textExtracted = ""
    if pagesList[u] == 1:
        textExtracted = text_list[u]
        #print("Added " + text_list[u][:10])
    else:
        print(u)
        for h in range(pagesList[u]):
            if (u+h == len(text_list)):
                break
            if (isinstance(text_list[u+h], str) == False):
                continue
            textExtracted = textExtracted + "\n" + text_list[u+h]
        u += h
        print(u)
    totalText.append(textExtracted)
# Var Names
print("Variable Name for text Files = ")
varNameL = []
for n, val in enumerate(textList):
    globals()["text%d"%n] = val
    varNameL.append("text%d"%n)
    #print("text%d"%n)
print("Total: " + str(n+1))
 # Create Sentences
# Create Sentences Using Full sentences -- better
textChoosen = textList[10]
setnecnceAuto = []
for line in textChoosen.splitlines():
    setnecnceAuto.append(line)
sentence = ""
sentenceList = []
char = 0
addNumChar = (int(len(textChoosen)/(len(setnecnceAuto)-10)))+1
for j in range(len(setnecnceAuto)):
    print([str(j) + " " + textList[10][char:char + addNumChar]])
    char += addNumChar
    addword = input("Current: >>>"+ sentence+ "<<< + >>>"+ setnecnceAuto[j] + "<<<")
    if addword == "":
        sentence += setnecnceAuto[j] + " "
    elif addword == "g":
        sentenceList.append(sentence[:-1])
        print("Added >>>"+sentence[:-1]+"<<<")
        sentence = ""
        setnecnceAuto[j: j] = ["testfff"]
    elif addword == "fff":
        break
# Create Sentences Using Words splitter
word = ""
listofWords = []
for i in textList[5]:
    if not (i == " " or i == "\n"):
        word += i 
    else:
        listofWords.append(word)
        word = ""
sentence = ""
sentenceList = []
for j in range(len(listofWords)):
    #print(listofWords[j])
    #print("running " + listofWords[j])
    addword = input("Current: >>>"+ sentence+ "<<< + >>>"+ listofWords[j] + "<<<")
    if addword == "":
        sentence += listofWords[j] + " "
    elif addword == "g":
        sentenceList.append(sentence[:-1])
        print("Added >>>"+sentence[:-1]+"<<<")
        sentence = ""
        listofWords[j: j] = ["testfff"]
    elif addword == "fff":
        break
# FINAL SENTENCE LIST MADE
sentenceList = ['Microsoft CERTIFIED',
 'aws certified',
 'Professional',
 'Hem Chandra',
 'Rockville, Maryland',
 '469-436-9015',
 'manoj@centillioninfotech.com',
 'OBJECTIVE: Lead Developer with more than 15+ years of experience in full-stack development (C#, VB.NET, .Net, ASP.NET, ASP.NET MVC, Web API, Angular, AWS, SharePoint, InfoPath, SQL Server, SSIS, SSRS, Web services, WCF, LINQ, XML, TFS 2010/13, SVN, VSS, GitHub, Telerik Controls, UML, JQuery and JavaScript) for building various desktop and web applications.',
 'SUMMARY:',
 'Working experience on ASP.NET, ASP.NET MVC framework, Web API and Entity Framework.',
 'Working experience on SharePoint 2013 and SharePoint 2010.',
 'Proficiently learned AWS (Design, Deployment, AWS EC2, S3, Cloud watch, Load balancing & Lambda etc.).',
 'Understanding of Microsoft Azure Cloud (Design, Deployment, app services, Azure Functions etc.).',
 'Extensive experience in coding using C# and VB.NET experience of various designs patterns (GOF).',
 'in Creation, Development and Deployment of SSIS packages in SQL Server.',
 'Used SQL Profiler for Performance monitor to resolve Dead Locks and long running queries by checking appropriate changes to Transaction Isolation levels',
 'Database Performance of Index tuning with using Database Engine Tuning Advisor to resolve Performance issues.',
 'Performed and fine-tuned Stored Procedures, SQL Queries and User Defined Functions.',
 'Extensive experience in developing UML Models using Visio and Rational Rose.',
 'Practical experience to implement SOA (Service Oriented Architecture: WCF) and Three-tier architecture.',
 'Methodology: AGILE, Scrum, Test Driven Development.',
 'Worked as TFS administrator (TFS Server setup, installation, collection creation, build automation, branching & merging etc.)',
 'Vertical/Domain Experience: Travel, Banking, Insurance, Chemical, Water and Energy',
 'Proficiently learned new technology Angular to meet client need.',
 'PROFESSIONAL EXPERIENCE Maryland Department of Labor',
 'Lead Developer',
 'Description:',
 'Foreclosure System-The Foreclosure Registration System is a web-based application for submission of those foreclosure-related notices and registrations that are mandated by Maryland law. System verifies lender companies using Nationwide Multistate Licensing System & Registry',
 '(NMLS). Application is divided into three sub-systems. 1.',
 'NOI (Notice of Intent to Foreclose): Lender companies can submit NOI to DLLR. Notice is created in pdf and send to borrower thorough email as well as by post. User can also upload predefined csv files for bulk submission.',
 'SSIS package reads and saves data into database. System sends processed NOI status email to user.',
 '2. NOF (Notice of Foreclosure Filing): Lender submits NOF in the system which creates notice in pdf and sends NOF to borrower through email.']
df = pd.DataFrame(sentenceList)
df.to_excel("sentenceLISTNEW.xlsx")
 # Convert Array to JSON
# Extract Excel and Turn into a list
os.chdir('/Users/kunal/Documents/ResumeNLPVdart/')
text = pd.ExcelFile("sentenceLISTT.xlsx")
attributes = text.parse("Sheet1")
RowList = attributes.values.tolist()
attributeList = [[i for i in row if isinstance(i,str)] for row in RowList]
totalTextRunning = totalText[0]
attributesNumberList = []
for j in attributeList:
    runningAttributeNum = []
    if len(j) == 2:
        continue
    if j[2] == "All":
        startChar = totalTextRunning.find(j[0])
        endChar = startChar + len(j[0])
        runningAttributeNum.extend([j[1], startChar, endChar])
    else:
        #print(int((len(j)-1)/2))
        for w in range(int((len(j)-1)/2)):
            startChar = totalTextRunning.find(j[2+w])
            endChar = startChar + len(j[2+w])
            runningAttributeNum.extend([j[1+w], startChar, endChar])
        attributesNumberList.append(runningAttributeNum)
def sentence_2_word(sentence):
    word = ""
    listofWords = []
    for i in sentence:
        if not (i == " " or i == "\n"):
            word += i 
        else:
            listofWords.append(word)
            word = ""
    if len(listofWords) == 0:
        listofWords.append(sentence)
    return listofWords
def find_all_indexes(input_str, search_str):
    l1 = []
    length = len(input_str)
    index = 0
    while index < length:
        i = input_str.find(search_str, index)
        if i == -1:
            return l1
        l1.append(i)
        index = i + 1
    return l1[0]
totalTextRunning = totalText[0]
attributesNumberList = []
for j in attributeList:
    runningAttributeNum = []
    if len(j) == 2:
        continue
    if j[2] == "All":
        startChar = totalTextRunning.find(j[0])
        endChar = startChar + len(j[0])
        runningAttributeNum.extend([j[1].upper() , startChar, endChar])
        attributesNumberList.append(runningAttributeNum)
    else:
        #print("RUNNING " + str(int((len(j)-1)/2)))
        for w in range(0, int((len(j)-1)), 2):
            runningAttributeNum = []
            if not totalTextRunning.find(j[2+w]) == -1:
                startChar = totalTextRunning.find(j[2+w])
                endChar = startChar + len(j[2+w])
                runningAttributeNum.extend([j[1+w].upper(), startChar, endChar])
            else:
                words = sentence_2_word(j[2+w])
                detected = 0
                for g in words:
                    if not j[2+w].find(g) == -1:
                        #charTemp = j[2+w].find(g)
                        detected+=1
                if detected/len(words) > 0.95:
                    startChar = totalTextRunning.find(words[0])
                    endChar = startChar + len(words[0])
                    runningAttributeNum.extend([words[0].upper(), startChar, endChar])
                else:
                    charTemp = -1
                    print("NOT DETECTED")
                    endChar , startChar = -1
                    runningAttributeNum.extend(["NOTDETECTED", startChar, endChar])
            attributesNumberList.append(runningAttributeNum)
for testing in attributesNumberList:
    if testing[1] == -1:
        attributesNumberList.remove(testing)
# DataSet to JSON FILE
attributeCount = len(attributesNumberList)
text = totalTextRunning
attributes = attributesNumberList
def createJSONFILE(attributeCount, text, attributes):
    alphab = list(string.ascii_lowercase)
    for alpa in range(int(attributeCount/26)):
        alphab.extend(list(string.ascii_lowercase))
    totalString = """{
        "annotations": [
            attributeCODE
        ],
        "text_snippet": {
            "content": "textCODE"
        }
    }

    """
    attributeString = """       
        {
          "text_extraction": {
            "text_segment": {
              "end_offset": eCharCODE,
              "start_offset": sCharCODE
            }
          },
          "display_name": "AtribnameCODE"
        },
    """
    totalString =  totalString.replace("textCODE", text)
    tempStringReplacer = ""
    for i in range(attributeCount):
        tempStringReplacer+=("atriCODE"+str(i+1)+alphab[i]+"\n")
    totalString = totalString.replace("attributeCODE", tempStringReplacer)
    for i in range(attributeCount):
        attributeStringNEW = attributeString
        #print(attributes[i])
        attributeStringNEW = attributeStringNEW.replace("AtribnameCODE", attributes[i][0])
        attributeStringNEW = attributeStringNEW.replace("sCharCODE", str(attributes[i][1])).replace("eCharCODE", str(attributes[i][2]))
        totalString = totalString.replace(("atriCODE"+str(i+1)+alphab[i]), attributeStringNEW)
    return totalString


# Final Run Create JSON
file = createJSONFILE(attributeCount, text, attributes)
print(file)
jsonFormatUpload = ast.literal_eval(file)
# Test DataSet
dataset = """{
  "annotations": [
    {
      "text_extraction": {
        "text_segment": {
          "end_offset": 67,
          "start_offset": 62
        }
      },
      "display_name": "Modifier"
    },
    {
      "text_extraction": {
        "text_segment": {
          "end_offset": 158,
          "start_offset": 141
        }
      },
      "display_name": "SpecificDisease"
    }
  ],
  "text_snippet": {
    "content": "10051005\tA common MSH2 mutation in English and North American HNPCC families:
      origin, phenotypic expression, and sex specific differences in colorectal cancer .\tThe
      frequency , origin , and phenotypic expression of a germline MSH2 gene mutation previously
      identified in seven kindreds with hereditary non-polyposis cancer syndrome (HNPCC) was
      investigated . The mutation ( A-- > T at nt943 + 3 ) disrupts the 3 splice site of exon 5
      leading to the deletion of this exon from MSH2 mRNA and represents the only frequent MSH2
      mutation so far reported . Although this mutation was initially detected in four of 33
      colorectal cancer families analysed from eastern England , more extensive analysis has
      reduced the frequency to fou"
  }
}"""
# Upload to Google Bucket

from gcloud import storage
from oauth2client.service_account import ServiceAccountCredentials
import os


credentials_dict = {
    'type': 'service_account',
    'client_id': os.environ['BACKUP_CLIENT_ID'],
    'client_email': os.environ['BACKUP_CLIENT_EMAIL'],
    'private_key_id': os.environ['BACKUP_PRIVATE_KEY_ID'],
    'private_key': os.environ['BACKUP_PRIVATE_KEY'],
}
credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    credentials_dict
)
client = storage.Client(credentials=credentials, project='myproject')
bucket = client.get_bucket('mybucket')
blob = bucket.blob('myfile')
blob.upload_from_filename('myfile')
from google.cloud import storage

def upload_to_bucket(blob_name, path_to_file, bucket_name):
    """ Upload data to a bucket"""

    # Explicitly use service account credentials by specifying the private key
    # file.
    storage_client = storage.Client.from_service_account_json(
        'creds.json') #ALREADY CRAETED KEY

    #print(buckets = list(storage_client.list_buckets())

    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(path_to_file)

    #returns a public url
    return blob.public_url

## SPACY
def checkattributes(text):
    doc = nlp(text)
    EMAILLIST = extract_emails(doc)
    NAMELIST = extract_person_names(doc)
    #print(NAMELIST)
    #print(EMAILLIST)
    if (NAMELIST == [] and not EMAILLIST == []) or (not EMAILLIST == [] and not NAMELIST == []):
        return ["EMAIL", EMAILLIST[0][0], EMAILLIST[0][1], EMAILLIST[0][2]]
    #elif EMAILLIST == [] and not NAMELIST == []:
        #return ["NAME", NAMELIST[0][0], NAMELIST[0][1], NAMELIST[0][2]]
    #elif NAMELIST == [] and EMAILLIST == []:
        #return ["N/A", "" , 0,  0]
    else:
        return ["N/A", "" , 0,  0]
def extract_emails(doc):
    resultlis = []
    for token in doc:
        if token.like_email:
            resultlis.append((token.text,token.idx, token.idx + len(token)))
    return resultlis
def extract_person_names(doc):
    personL = []
    for entity in doc.ents:
        if entity.label_=="PERSON":
            personL.append([entity.text, entity.start_char, entity.end_char])
    return personL
# Check Attributes for each Sentence in Document
for i in sentenceList:
    print(checkattributes(i))

# # Create JSON from Array -- NOTWORKING
attributeCount = 3
sentenceCount = 2
text = "NISARGA HASSAN SREEDHAR"
attributes = [["NAME", "NISARGA HASSAN SREEDHAR", 0, 23],
              ["LOCATION", "San Jose, California", 12, 18],
              ["PROGRAMMING LANGUAGE", "PYTHON", 17, 20]]
def createJSON(attributeCount, sentenceCount, text, attributes):
    totalString = """
    "sentenceCode": [
        "text": "textCODE",
        "entities" : [
    attributeCODE
        ]
    ],
    """
    attributeString = """       "attributeCode" : {
               "Atribname": "AtribnameCODE",
               "textDetected": "textDetectedCODE",
               "sChar": sCharCODE,
               "eChar": eCharCODE
           }
    """
    sentenceStringReplacer = "sentence" + str(sentenceCount)
    totalString =  totalString.replace("sentenceCode", sentenceStringReplacer)
    totalString =  totalString.replace("textCODE", text)
    tempStringReplacer = ""
    for i in range(attributeCount):
        tempStringReplacer+=("atriCODE"+str(i+1)+"\n")
    totalString = totalString.replace("attributeCODE", tempStringReplacer)
    for i in range(attributeCount):
        attributeStringNEW = attributeString
        print(attributes[i])
        attributeStringNEW = attributeStringNEW.replace("AtribnameCODE", attributes[i][0]).replace("textDetectedCODE", attributes[i][1])
        attributeStringNEW = attributeStringNEW.replace("sCharCODE", str(attributes[i][2])).replace("eCharCODE", str(attributes[i][3]))
        totalString = totalString.replace(("atriCODE"+str(i+1)), attributeStringNEW)
    return totalString
data = """
{
    "Document1Sentences" : [
        "sentence1": [
            "text": "NISARGA HASSAN SREEDHAR",
            "entities" : [
                "attribute1" : {
                    "Atribname": "NAME",
                    "textDetected": "NISARGA HASSAN SREEDHAR",
                    "sChar": 0,
                    "eChar": 23
                }
            ]
        ],
        "sentence2": [
            "text": "San Jose, California",
            "entities" : [
                "attribute1" : {
                    "Atribname": "LOCATION",
                    "textDetected": "San Jose, California",
                    "sChar": 0,
                    "eChar": 18
                }
            ]
        ],
        "sentence3": [
            "text": "Programming: Python, Java",
            "entities" : [
                "attribute1" : {
                    "Atribname": "Programming Language",
                    "textDetected": "Python",
                    "sChar": 13,
                    "eChar": 18
                },
                "attribute2" : {
                    "Atribname": "Programming Language",
                    "textDetected": "Java",
                    "sChar": 20,
                    "eChar": 24
                }
            ]
        ],
        "sentence4": [
            "text": "Aug 2019 - Dec 2019",
            "entities" : [
                "attribute1" : {
                    "Atribname": "DATE",
                    "textDetected": "Aug 2019",
                    "sChar": 0,
                    "eChar": 12
                },
                "attribute2" : {
                    "Atribname": "DATE",
                    "textDetected": "Dec 2019",
                    "sChar": 16,
                    "eChar": 20
                }
            ]
        ]
    ]
}
"""
# Test Creating Loop for creating Sentences
wordCount = 0
elementList = []
for i in listofWords:
    elementGoing = ""
    print(str(wordCount) +  "   " +  i)
    elementContain = input("Does this contain a element")
    while elementContain == "" or not (elementContain == "n" or elementContain == "y") :
        elementContain = input("Does this contain a element")
    if elementContain == "Y" or elementContain == "y":
        elementGoing += i
        continueaddElement = input("Add more to this element?")
        while continueaddElement == "":
            continueaddElement = input("Add more to this element?")
        while continueaddElement == "Y" or continueaddElement == "y":
            print(listofWords[wordCount+1])
            countineElement2  = input("Add more to this element?")
            while countineElement2 == "":
                countineElement2 = input("Add more to this element?")
            while countineElement2 == "Y" or countineElement2 == "y":
                print(listofWords[wordCount+2])
                countineElement2 =  input("Add more to this element?")
        if continueaddElement == "x":
            break
    if elementContain == "x":
        break
    wordCount+=1

 # Write a program that goes through the text file and extracts each entity and its starting position and ending position and its name