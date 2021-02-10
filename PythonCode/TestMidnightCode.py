import os, shutil #Controlling Files and paths and folder control
from shutil import copyfile
from pdf2image import convert_from_path #Libary convert pdf file to img file
from google.oauth2 import service_account #Control API Keys
from google.cloud import vision # Vision API from Google
import io
import string, random
import pandas as pd
# Imports the Google Cloud client library
from google.cloud import language_v1
from google.cloud.language_v1 import enums
#nlp = spacy.load('en_core_web_sm')

#Paths that have all folders which use everything
pdfIMGPopplerPath = '/Users/kunal/Documents/VdartResumeProject/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/'
imgTxtVisionAPIPath = "/Users/kunal/Documents/VdartResumeProject/APIKEYSGOOGLE/resumeMatcher-pdf2img.json"
runningDocumentPath = '/Users/kunal/Documents/VdartResumeProject/runningDoc/'
sourceFolderResumesPath = '/Users/kunal/Documents/VdartResumeProject/50_resumes/'
excelFilesPath = '/Users/kunal/Documents/VdartResumeProject/ExcelFiles/'
nlpAutoAPIPath = "/Users/kunal/Documents/VdartResumeProject/APIKEYSGOOGLE/resumeMatcher-NLP_create_data.json"
jsonFolderPath = '/Users/kunal/Documents/VdartResumeProject/JSONLFILES/'

def convert_pdf_2_image(uploaded_image_path, uploaded_image):
    #Using the convert_from_path function
    #Same name as pdf but converted to img
    #Watch out for poppler -- necceasary to function
    os.chdir(uploaded_image_path)
    file_name = str(uploaded_image).replace('.pdf','')
    pages = convert_from_path(uploaded_image, 200,poppler_path=pdfIMGPopplerPath)
    pageNumCount = 1
    outputNames = []
    for page in pages:
        output_file = file_name+"_"+str(pageNumCount) + '.jpg'
        page.save(output_file, 'JPEG')
        pageNumCount +=1
        outputNames.append(output_file)
    return outputNames

def convert_img_2_text(imagePath):
    #Using API from Google
    #Returns a JSON file but text is extracted from it
    keyDIR = imgTxtVisionAPIPath
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
    #Deletes all the images from a folder
    for i in os.listdir(path):
        if i.endswith(".jpg"):
            os.remove(folder_pdf + i)
def deleteEverythingInFolder(folder_pdf):
    #deletes everything in the folder including folders and files
    for file in os.listdir(folder_pdf):
        try:
            shutil.rmtree(folder_pdf+ file)
        except NotADirectoryError:
            try:
                os.remove(folder_pdf+ file)
            except:
                pass
def moveRenameAllFiles(sourceFolderResumes, folder_pdf):
    #Moves all files from source and renames them starting from 100
    #If start from 1 then the ordering will be off
    for realFile in os.listdir(sourceFolderResumes):
        copyfile(sourceFolderResumes + realFile, folder_pdf + realFile)
    os.chdir(folder_pdf)
    documentcounter = 100
    for i in os.listdir(folder_pdf):
        fileNameCreator = "Document_" + str(documentcounter) + ".pdf"
        print(i + "   changed to  " + fileNameCreator)
        os.rename(i, fileNameCreator) 
        documentcounter+=1
folder_pdf = runningDocumentPath
sourceFolderResumes = sourceFolderResumesPath

deleteEverythingInFolder(folder_pdf)
moveRenameAllFiles(sourceFolderResumes, folder_pdf)
numberOfFiles = len([name for name in os.listdir(folder_pdf) if os.path.isfile(name)])
print("There are "+ str(numberOfFiles) + " files running.")
#PNGFilesExist = checkifPNGExists(folder_pdf)

#Asks the user which document they want to run and if they don't input anything, its a random document
doubleCheckDocumentInputCount = 0
while True:
    documentRun = input("Which Document do you wanna run?")
    if documentRun == "" and doubleCheckDocumentInputCount >= 1:
        documentRun = (random.choice(os.listdir(folder_pdf)))
        print("You choose RANDOM so your document is " + documentRun)
        break
    elif documentRun == "":
        print("This is a double check if you want a random document?")
        doubleCheckDocumentInputCount+=1
    elif documentRun == "BREAK":
        print("Exiting")
        documentRun = "INVALID"
        break
    else:
        documentRun = "Document_" + documentRun + ".pdf"
        print(os.path.isfile(folder_pdf + documentRun))
        if os.path.isfile(folder_pdf + documentRun):
            print("You choose a specific number so your document is " + documentRun)
            break
        else:
            print("Document was invalid. Input >>> BREAK <<< to stop")
            continue
#Makes a folder and create images of each page in PDF document
textList = []
numberPagesList = []
for i in os.listdir(folder_pdf):
    if i == documentRun:
        os.chdir(folder_pdf)
        folderNameCreate = folder_pdf+"Fold_"+i[:-4]+"/"
        print(folderNameCreate)
        os.mkdir(folderNameCreate) #Create folder
        shutil.move(i,folderNameCreate) #MovePDF into folder
        os.chdir(folderNameCreate)
        for j in os.listdir(folderNameCreate):
            print(j)
            if j.endswith(".pdf"):
                imgName = convert_pdf_2_image(folderNameCreate, j) #call pdf2img function
                print("Running Number: " + str(len(imgName))) 
                printString = ""
                for docName in imgName:
                    printString += docName + " " 
                print(printString)
            for q in range(len(imgName)):
                text = convert_img_2_text(folderNameCreate + i[:-4] + "_" + str(q+1) + ".jpg")
                textList.append(text)     #Convert to text and append all the text to list
                numberPagesList.append(len(imgName))   
    else:
        os.chdir(folder_pdf) #delete any other file that exists
        os.remove(i)

# Convert to Excel
df = pd.DataFrame()
df['Text Extracted'] = textList
df['DocumentNum'] = numberPagesList
os.chdir(excelFilesPath)
#Save the text to excel to be extracted later
EXCELFILENAME = documentRun[:-4] + "_text.xlsx"
df.to_excel(EXCELFILENAME, index = False) 
# Read Excel if needed
EXCELFILENAME = documentRun[:-4] + "_text.xlsx"
os.chdir(excelFilesPath)
text = pd.ExcelFile(EXCELFILENAME)
dftext = text.parse("Sheet1")
print("TEXT EXTRACTED IS \n" + dftext)

#text_list = dftext["Text Extracted"].tolist()
#pagesList = dftext["DocumentNum"].tolist()

# Check for Recommendation letters
#Goes through text and finds if any of the text has recommendation word in it
count=0
numb = 0
recNumList=[]
for i in textList:
    if "Recommendation" in str(i): 
        recNumList.append(numb)
    numb+=1
if not len(recNumList) == 0:
    print("RECOMMENDATION LETTER DETECTED")
    for page in recNumList:
        print("PAGE: " + str(page))
# Converts the text files to an array but still split into pages
#Converts all text files and joins them together
runningTextFINAL = '\n'.join(textList)
# Create Sentences
textChoosen = runningTextFINAL
#Auto Split lines
setnecnceAuto = []
for line in textChoosen.splitlines():
    setnecnceAuto.append(line)
print("CHAR: " + str(len(textChoosen)) + ", LINES: " + str(len(setnecnceAuto)))
doubleCheckSentenceSplitterCount = 0
doubleCheckSentenceSplitterCount2 = 0
sentenceSplitterRun = False
while True:
    sentenceSplitter = input("Do you want to run sentence splitter? : ").lower().strip()
    if sentenceSplitter == "yes" and doubleCheckSentenceSplitterCount >=1:
        sentenceSplitterRun = True
        break
    elif sentenceSplitter == "yes":
        print("This is a double check if you want to do the sentence splitter on the document?")
        doubleCheckSentenceSplitterCount += 1
    elif sentenceSplitter == "no" and doubleCheckSentenceSplitterCount2 >=1:
         sentenceSplitterRun = False
         break
    elif sentenceSplitter == "no":
        doubleCheckSentenceSplitterCount2 +=1
    elif sentenceSplitter == "BREAK":
        print("Exiting")
        break
    else:
        print("Document was invalid. Input >>> BREAK <<< to stop")
        continue
sentenceList = []
if sentenceSplitterRun:
    sentence = ""
    char = 0
    addNumChar = (int(len(textChoosen)/(len(setnecnceAuto))))+1
    for j in range(len(setnecnceAuto)):
        #print([str(j) + " " + textChoosen[char:char + addNumChar]])
        char += addNumChar
        addword = input("Current: >>>"+ sentence+ "<<< + >>>"+ setnecnceAuto[j] + "<<<")
        if addword == "":
            sentence += setnecnceAuto[j] + " "
        elif addword == "k": # Sentence add key letter
            sentenceList.append(sentence[:-1])
            #print("Added >>>"+sentence[:-1]+"<<<")
            sentence = ""
            setnecnceAuto[j: j] = ["testfff"]
        elif addword == "BREAK": # break key word
            break
else:
    print("MUST MAKE OWN SENTENCES")

#sentenceList = ['Oleg Kotliarsky', '(720) 987-8054', 'olegkot@gmail.com', 'Profile highlights:', 'Web Development Engineer','Vast experience designing, programming and leading enterprise web applications development','Proficient in optimal UX solutions', 'Great experience in developing reusable components to optimize development time and maintenance', 'Ability to provide technical leadership and clear guidance to development team', 'High skills to research, evaluate and implement right technical solution for the enterprise application', 'Technical Knowledge:', 'JavaScript, TypeScript, ReactJS, Action Script 3.0, Java, PHP', 'Angular, AngularJS, RXJS, Karma, Java Spring, İBATIS, Apache Struts', 'Oracle, MongoDB, SQL Server, MYSQL', 'angular-cli, npm, bower, gulp, GIT', 'Languages:', 'Frameworks:', 'Databases:', 'Tools:', 'Professional Experience: Aug. 2017 - April 2020 Senior Web Developer, Comcast, CO', 'Designed and developed new app features (Columbo - ESL). (Angular6/Angular UI, Remedy, JAVA, Oracle DB):', 'data driven "case create wizard" with back-end precheck and dynamic restructure of the steps', '- case resolve "stepper" with variable number of corresponding relative issues', '- reusable components - "keyword" search, attachments list, "add attachments", PDF viewer, util service with multitude of helper functions.', '- HTTP request wrappers, HTTP response interceptor for unified error handling', 'Developed a web app (Columbo - Executive Support Line). (Hybrid AngularJS/Angular UI, Remedy, JAVA, Oracle DB); Maintain and support GIT Hub of the project', 'Dec. 2013 – June 2017 Senior UI Developer / Team Lead / Scrum Master, DN2K, CO', 'Developed customers, search, navigation modules for "MyDairyCentral" web app portal, sensors tiles carousel, responsive design, etc. (Angular4, angular-cli, Jasmine/Karma)', 'Developed sensors tiles carousel, set karma unit tests framework for "MyGrowCentral" web app portal (AngularJS, Node, responsive design, JHipster, Jasmine/Karma)', 'Developed different features of the "MyAGCentral" web app portal, including navigation tree, work orders flow, etc. (AngularJS, Node, Mongo) - client Sagelnsights: https://www.sageinsights.com/', 'Transitioned from Backbone to Angular framework (team effort) of the "MyAGCentral" web app portal', 'October 2011 - Dec. 2013 Web Developer Expert, Amdocs Inc., CO', 'Developed "Order Entry" web application for entering order to the Amdocs Enterprise order management system (HTML5/CSS3, JavaScript/jQuery, AJAX/DWR, JSP/Java 7, Oracle, Java Spring, iBatis)', 'Developed e-signature web app using previously developed JavaScript/jQuery/JSP/Java6/Spring2 framework for sending client\'s contract to "on-the-fly" signature creation (integration with docusign.com service).', 'Developed part of the real time payment integration flow utilizing Amdocs EAI framework called JESI. (Java, JSP, SOAP, Oracle, JavaScript, jQuery)', 'Developed Flex "Executive Advisor" report tool for serving different types of client statistics presented in a rich graphic interactive way (Flex 4.6, Blaze DS, Java, Oracle, Action Script 3)', 'October 2010 – Oct. 2011 Web Developer Contractor, Rose International (for Amdocs Inc.), CO', 'Developed iLink Mobile app (running on iPad Safari – used home developed framework) for sales representatives [client: DexOne]. (JavaScript, jQuery, jQTouch, AJAX, HTML5/webkit, Java, Spring, iBatis, Oracle, JSP);', 'Developed an iPad web application framework for rapid development of iOS apps that look like', 'March 2009 - October 2010 GSET Engineer, Wall Street on Demand (now Markit on Demand), Boulder, CO', 'Developed Entitlements management intranet tool [client: Goldman Sachs]. (Java, Struts, Sybase, JSP, JavaScript, jQuery, AJAX);', 'March 2008 – March 2009 Team Lead Developer, Wall Street on Demand (now Markit on Demand), Boulder, CO', 'Leaded team of web developers, working on line of Stocks Research Websites [client: Schwab Institutional] (ASP, JavaScript, AJAX);', 'August 2005 – March 2008 Senior Web Developer, Wall Street on Demand (now Markit on Demand), Boulder, CO', 'Developed Web site architecture and determine software requirements.', 'Created and optimized content for the Web site, including planning, design, integration and testing of Web-site related code.', 'Planned and designed new featured web sites according to client requirements. Close interaction with graphic designers, project managers and QA members of our group;', 'Developed Real Time DB driven web sites with Stocks market content, including price quotes graphics, charts, news, alerts etc. Schwab group projects (ASP, JScript, JavaScript, AJAX);', 'April 2004 – August 2005 Freelancer Web Developer, Denver, CO', 'Developed full code circle from templates to launch (PHP/MySql, JavaScript, HTML, CSS);', 'Created Graphics: logos, bullets, complete design (Photoshop, Flash MX);', 'Promoted web sites in search engines positioning (1st page positions in Google, Yahoo on several key words).', 'April 2003 – April 2004', 'Web developer, Gteko (purchased by Microsoft), Raanana, Israel', '- Developed JavaScript/VBScript active client side (ActiveX event\'s handling flow: version checking, upgrading, downloading and installation) of different "e-support" accounts (HP, Canon, AOL, Dell, NEC, Lenovo, etc)', 'Developed JavaScript classes reflecting graphic presentation of ActiveX control downloading and installation processes;', 'Developed a full JavaScript based interface for ActiveX control data processing - JavaScript/DOM/DHTML based model for PC scanned data show. Was a leading developer for GTWebCheck product part called "Upgrade Advisor" or "Summary Report".', 'June 2002 – April 2003 Freelancer Web developer, Tel-Aviv , Israel', 'Complete web sites production (Programming development, PHP/MYSQL/JavaScript/HTML/CSS index + forum (OOP);', "Created graphic design according to Client's requirements (logo, bullets, layout – Photoshop, Flash); Made domain name registration; Assisted in identity development, marketing, online promotion and launch;", 'Maintained web mastering; Promoted web sites for search engines positioning August 1999 - May 2002', 'Web Developer, Snapshield Ltd, Tel Aviv, Israel', "Created Web design (Photoshop, Flash) for Web based application for remote data management for tens of thousands of clients of the leading Snapshield's Telecom Encryption Service (SNAP);", 'Programmed part of the SNAP application (Customer Care) using ASP, JavaScript, VBScript, CSS, IIS 4;', 'Set required configuration for SSL on MS IIS4.', 'Created web based client-side application "Snapshield\'s Security Algorithm Benchmark" for dynamic online calculating and show for different TI DSP platforms and Snapshield algorithms. (ASP, CSS, DHTML)', 'Created Flash Animated Company Business and Technical Presentations (online, cds) in Macromedia', 'Flash 5; Integrated video streaming to companies web site (JavaScript, DHTML)', 'Created graphic and technical design, developed, published and web mastered three generations of the\ncompany\'s web site. (HTML/DHTML, JavaScript, CSS, Macromedia Flash 5, Adobe Photoshop 5.5;', 'Assisted in new branding process (migrating from Microlink to Snapshield)', 'Education:', 'BS and MS in Mathematics and Mechanics', 'St. Petersburg State University', 'Courses:', '"Oracle Certified Associate", iTerra Consulting, Ic., Denver, USA.', '"Design for Multimedia", ORT Syngalovsky College, Tel Aviv. (800 hours)', '"JavaScript - DHTML – DOM", Sela group, Tel Aviv (30 hours)', '"OOD/OOP for C++ and Java", "Network TCP/IP", Tel-Ran, Rishon-Lezion (1000 hours)']
 # Automatic Entity Creation

#Using Google prebuilt enity extraction model, I can do some basic entity analysis
#Extract the major entities
#https://cloud.google.com/natural-language/docs/basics#entity_analysis
def extractMajorEntities(text_content, salienceScoreThres):
    keyDIR = nlpAutoAPIPath
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_entities(document, encoding_type=encoding_type)
    majorValues = []
    for entity in response.entities:  
        if entity.salience > salienceScoreThres:
            majorValues.append([entity.name,entity.salience])
    return  majorValues
def extractEntities(text_content):
    keyDIR = nlpAutoAPIPath
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    encoding_type = enums.EncodingType.UTF8
    response = client.analyze_entities(document, encoding_type=encoding_type)
    nonuseEntities = ["OTHER", "NUMBER"]
    allEntitiesExtracted = []
    for entity in response.entities:
        currentRunningEntity = []
        #print(entity.name)
        #print(enums.Entity.Type(entity.type).name)
        if enums.Entity.Type(entity.type).name not in nonuseEntities:
            #print("Detected " + entity.name + " as " + enums.Entity.Type(entity.type).name)
            currentRunningEntity.append(entity.name)
            currentRunningEntity.append(enums.Entity.Type(entity.type).name)
            allEntitiesExtracted.append(currentRunningEntity)
        else: 
            for mention in entity.mentions:
                if enums.EntityMention.Type(mention.type).name == "PROPER":
                    #print("Detected " + mention.text.content + " as " + enums.EntityMention.Type(mention.type).name)
                    currentRunningEntity.append(mention.text.content)
                    currentRunningEntity.append(enums.EntityMention.Type(mention.type).name)
                    allEntitiesExtracted.append(currentRunningEntity)
        #allEntitiesExtracted.append(currentRunningEntity) if currentRunningEntity != [] else print("-")
        #allEntitiesExtracted.append(currentRunningEntity)   
    finalArray = []
    runningEnitityCount = 0
    positionValuesEnitiesList = []
    for i in range(len(allEntitiesExtracted)):
        arrayrun = []
        arrayrun.append(allEntitiesExtracted[i][0])
        arrayrun.append(allEntitiesExtracted[i][1])
        arrayrun.append(text_content.find(allEntitiesExtracted[i][0]))
        positionValuesEnitiesList.append(arrayrun)
    positionValuesEnitiesList = sorted(positionValuesEnitiesList, key=lambda x: x[2])
    #print(positionValuesEnitiesList)
    runningPositionValuesCount = 0
    for numb in range(len(positionValuesEnitiesList)-1):
        distancebetween = 0
        lenWord = len(positionValuesEnitiesList[numb][0])
        wordPosition = positionValuesEnitiesList[numb][2]
        distancebetween =((positionValuesEnitiesList[numb+1][2] - (wordPosition + lenWord)))
        sameElement = True if positionValuesEnitiesList[numb][1] == positionValuesEnitiesList[numb+1][1] else False
        #print(sameElement)
        if distancebetween < 2.5 and sameElement:
            #print(positionValuesEnitiesList[numb])
            returnArray = [text_content[positionValuesEnitiesList[numb][2]:positionValuesEnitiesList[numb+1][2]+len(positionValuesEnitiesList[numb+1][1])]]
            returnArray.append(positionValuesEnitiesList[numb][1])
            finalArray.append(returnArray)
        else: 
            finalArray.append([positionValuesEnitiesList[numb][0], positionValuesEnitiesList[numb][1]])
    #print(distancebetween)
    #if distancebetween/len(positionValuesEnitiesList)-1 < 2.5:
        #returnArray = [text_content[positionValuesEnitiesList[0][2]:positionValuesEnitiesList[-1][2]+len(positionValuesEnitiesList[-1][1])]]
        #returnArray.append(positionValuesEnitiesList[0][1])
        #print(returnArray)
    return finalArray
sentenceArrayWithEntities = []
for i in sentenceList:
    temparray = []
    temparray.append(i)
    entityArray = extractEntities(i)
    for j in entityArray:
        temparray.extend(j)
    sentenceArrayWithEntities.append(temparray)

importantEntitiesArray = extractMajorEntities(runningTextFINAL, 0.05)
print(importantEntitiesArray)
 # Check what document is about
def sample_classify_text(text_content):
    keyDIR = nlpAutoAPIPath
    credentials = service_account.Credentials.from_service_account_file(keyDIR)
    client = language_v1.LanguageServiceClient(credentials=credentials)
    type_ = enums.Document.Type.PLAIN_TEXT
    language = "en"
    document = {"content": text_content, "type": type_, "language": language}
    response = client.classify_text(document)
    # Loop through classified categories returned from the API
    categoryList = []
    for category in response.categories:
        # Get the name of the category representing the document.
        # See the predefined taxonomy of categories:
        # https://cloud.google.com/natural-language/docs/categories
        # print(u"Category name: {}".format(category.name))
        categoryList.append([category.name, category.confidence])
    return categoryList

allPossibleCategory = sample_classify_text(runningTextFINAL)
print(allPossibleCategory)
 # Save Sentences and Entities|
os.chdir(excelFilesPath)

df = pd.DataFrame(sentenceArrayWithEntities)
EXCELFILENAMESent = documentRun[:-4] + "_sentencesNew.xlsx"
df.to_excel(EXCELFILENAMESent)
# Convert Array to JSON
EXCELFILENAMESent = documentRun[:-4] + "_sentencesNew.xlsx"

print("Sentence FILE NAME: \t" + EXCELFILENAMESent)
# Extract Excel and Turn into a list
os.chdir(excelFilesPath)
text = pd.ExcelFile(EXCELFILENAMESent)
totalTextRunning = runningTextFINAL
attributes = text.parse("Sheet1")
print(attributes)
RowList = attributes.values.tolist()
attributeList = [[i for i in row if isinstance(i,str)] for row in RowList]
# Create Final List

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
def checkNotWorkingValues(textFindPosition, totalTextRunning):
    words = textFindPosition.split()
    wordPositions = []
    for singleWord in words:
        wordPositions.append(totalTextRunning.find(singleWord))
    positionsCount = 0
    numCorrect = 0
    for num in range(len(wordPositions)-1):
        if wordPositions[num]+len(words[num])+1 == wordPositions[num+1]:
            numCorrect+=1
        positionsCount+=1
    if numCorrect == len(words)-1:
        return wordPositions[0]
    else:
        return -1
numbAttributeReal = 0
for line in attributeList:
    #value_when_true if condition else value_when_false
    numbAttributeReal += int((len(line)-1)/2) if (len(line)-1)/2 != 0.5 else 0
print("NUMBER OF ATTRIBUTES IS: \t" + str(numbAttributeReal))

attributesNumberList = []
for j in attributeList[11:13]:
    runningAttributeNum = []
    if len(j) == 2:
        continue
    if j[2] == "All":
        startChar = totalTextRunning.find(j[0].strip())
        if startChar == -1:
            startChar = checkNotWorkingValues(j[0].strip(), totalTextRunning)
        if startChar == -1:
            startChar = totalTextRunning.lower().find(j[0].lower().strip())
        endChar = startChar + len(j[0].strip())
        runningAttributeNum.extend([j[1].strip().upper() , startChar, endChar])
        attributesNumberList.append(runningAttributeNum)
    else:
        #print("RUNNING " + str(int((len(j)-1)/2)))
        for w in range(0, int((len(j)-1)), 2):
            runningAttributeNum = []
            if not totalTextRunning.find(j[2+w]) == -1:
                startChar = totalTextRunning.find(j[2+w].strip())
                if startChar == -1:
                    startChar = checkNotWorkingValues(j[2+w].strip(), totalTextRunning)
                if startChar == -1:
                    startChar = totalTextRunning.lower().find(j[2+w].lower().strip())
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

print(attributesNumberList)

for testing in attributesNumberList:
    if testing[1] == -1:
        print(testing)
        attributesNumberList.remove(testing)
print("DETECTED ATTRIBUETS IS: "+ str(len(attributesNumberList)))

# MATRIX to JSON FILE
attributeCount = len(attributesNumberList)
text = totalTextRunning
attributes = attributesNumberList
def createJSONFILE(attributeCount, text, attributes):
    alphab = list(string.ascii_lowercase)
    for alpa in range(int(attributeCount/26)):
        alphab.extend(list(string.ascii_lowercase))
    totalString = """{"textSnippet":{"content":"textCODE"},"annotations":[attributeCODE]}"""
    attributeString = """{"displayName":"AtribnameCODE","textExtraction":{"textSegment":{"startOffset":"sCharCODE","endOffset":"eCharCODE"}}}"""
    totalString =  totalString.replace("textCODE", text)
    tempStringReplacer = ""
    for i in range(attributeCount):
        if i != attributeCount-1:
            tempStringReplacer+=("atriCODE"+str(i+1)+alphab[i]+",")
        else:
            tempStringReplacer+=("atriCODE"+str(i+1)+alphab[i])
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
print("JSON FILE: \n" +  file)
# Save JSONL FILE

os.chdir(jsonFolderPath)
jsonFileName = "FINAL_"+documentRun[9:-4]+".jsonl"
text_file = open(jsonFileName, "w")
text_file.write(file)
text_file.close()
print("SAVED as: " + jsonFileName)

#f = open(jsonFileName, "r")
#print(f.read())

