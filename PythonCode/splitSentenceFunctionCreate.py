import os
from pdf2image import convert_from_path
import ntpath
from google.oauth2 import service_account
from google.cloud import vision
import io
import pandas as pd
import spacy
nlp = spacy.load('en_core_web_sm')
import spacy
from spacy.lang.en import English # updated
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
#deleteIMG(folder_pdf)
textList = []
folder_pdf = '/Users/kunal/Documents/ResumeNLPVdart/Testing_Delete/'
for i in os.listdir(folder_pdf):
    if os.path.exists(folder_pdf + i[:12] + ".jpg") == False:
        if i.endswith(".pdf"):
            imgName = convert_pdf_2_image(folder_pdf, i)
            print(imgName)
    text = convert_img_2_text(folder_pdf + i[:12] + ".jpg")
    textList.append(text)
print("Variable Name for text Files = ")
varNameL = []
for n, val in enumerate(textList):
    globals()["text%d"%n] = val
    varNameL.append("text%d"%n)
    print("text%d"%n)
print("Total: " + str(n+1))
word = ""
listofWords = []
print(textList[3])
for i in textList[3]:
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


df = pd.DataFrame(sentenceList)
df.to_excel("sentenceLISTTNEW.xlsx")









"""
textDATA = "His having within saw become ask passed misery giving. Recommend questions get too fulfilled. He fact in we case miss sake. Entrance be throwing he do blessing up. Hearts warmth in genius do garden advice mr it garret. Collected preserved are middleton dependent residence but him how. "
word = ""
wordList = []
for i in textDATA:
    if not i == " ":
        word= word+i
    else:
        #print(word)
        wordList.append(word)
        word = ""
count = 0
numWordShow = 5
for i in range(len(wordList)):
    print(str(numWordShow)+  " words is shown")
    for j in range(numWordShow):
        print(wordList[j+count])
    i+=numWordShow
    count+=1
for i in range(0, len(wordList), 5):
    for j in wordList[i:i+5]:
        shortListofWord = shortListofWord + j + " "
    print(shortListofWord)
    elementContain = input("Is there a element in the text?")
    if elementContain == "y":
        printLonger = input("Need more text?")
        if printLonger == "y":
            print("continuing")
            continue
        elif printLonger == "n":
            startChar = in
    elif elementContain == "n":
        print("bad")
        shortListofWord = ""
    elif elementContain == "m":
        print(shortListofWord)
        continue
"""