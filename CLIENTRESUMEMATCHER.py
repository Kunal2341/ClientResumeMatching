#
#
#
# pip install -r requirements.txt
#
#

import datetime
STARTCODETIME = datetime.datetime.now() #Setting up time to find total time spent on code
import statistics
import numpy as np
import pandas as pd
from google.oauth2 import service_account #Control API Keys
from google.cloud import vision
import os, cv2
from pdf2image import convert_from_path
from collections import Counter
from IPython.display import Image
from shapely.geometry import Polygon
import io
import shutil
from google.cloud.vision import types
from PIL import Image, ImageDraw, ImageFont
import string, spacy
from pandas import ExcelWriter
from termcolor import colored
from stop_words import get_stop_words
from google.cloud import documentai_v1beta2 as documentai
from pyresparser import ResumeParser
from matplotlib import pyplot as plt


stop_words = get_stop_words('english')
nlp = spacy.load("en_core_web_sm")
# ------- Declare all Paths ---------
#doc = '/Users/kunal/Documents/VdartResumeProject/VisionAPi/Document_402.pdf'
keyDIRDocumentAI = "/Users/kunal/Documents/VdartResumeProject/APIKEYSGOOGLE/resumeMatcher-documentAI.json"
docPath = '/Users/kunal/Documents/VdartResumeProject/VisionAPi/'
imgTxtVisionAPIPath = "/Users/kunal/Documents/VdartResumeProject/APIKEYSGOOGLE/resumeMatcher-pdf2img.json"
pdfIMGPopplerPath = '/Users/kunal/Documents/VdartResumeProject/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/'
fontPath = '/Users/kunal/Documents/VdartResumeProject/Font/FreeMonoBold.ttf'
allResumesPath = "/Users/kunal/Documents/VdartResumeProject/50_resumes/"
nlpAutoAPIPath = "/Users/kunal/Documents/VdartResumeProject/APIKEYSGOOGLE/resumeMatcher-NLP_create_data.json"
# ------- Checking for API -------
#Using API from Google and returns a JSON file but text is extracted from it
keyDIR = imgTxtVisionAPIPath #JSON key file to call the api
credentials = service_account.Credentials.from_service_account_file(keyDIR) #using service account to go through google
client = vision.ImageAnnotatorClient(credentials=credentials) # client api

filePDFPath = '/Users/kunal/Documents/VdartResumeProject/Testing_Delete/Document_402.pdf'

def deleteEverythingInFolder(folder_pdf):
    #deletes everything in the folder including folders and files
    for file in os.listdir(folder_pdf):
        try:
            shutil.rmtree(folder_pdf+ file) #remove folder
        except NotADirectoryError:
            try:
                os.remove(folder_pdf+ file) # if it is not a folder than it is a file so it removes it also
            except:
                pass
def convert_pdf_2_image(filePath):
    #os.chdir(os.path.dirname(filePath))
    uploaded_file = filePath
    output_file = str(uploaded_file).replace('.pdf','')
    pages = convert_from_path(uploaded_file, 200,poppler_path=pdfIMGPopplerPath)
    pageCount = 1
    if len(pages) != 1:
        raise Exception ("Some of the code is not compatable for multiple pages")
    for page in pages:
        page.save(output_file + "_" + str(pageCount) + ".jpg", 'JPEG')
        #print(output_file + "_" + str(pageCount) + ".jpg")
        pageCount+=1
    return output_file + "_1.jpg"

os.chdir(os.path.dirname(filePDFPath))
try:
    os.mkdir(os.path.basename(filePDFPath)[:-4])
    folderPath = os.path.dirname(filePDFPath)+"/"+os.path.basename(filePDFPath)[:-4]
except FileExistsError:
    try:
        os.mkdir(os.path.basename(filePDFPath)[:-4] + "_NEW")
        folderPath = os.path.dirname(filePDFPath)+"/"+os.path.basename(filePDFPath)[:-4] + "_NEW"
    except FileExistsError:
        deleteEverythingInFolder(os.path.basename(filePDFPath)[:-4] + "_NEW")
        folderPath = os.path.dirname(filePDFPath)+"/"+os.path.basename(filePDFPath)[:-4] + "_NEW"
try:
    shutil.move(filePDFPath, folderPath)
    if os.path.exists(folderPath+"/"+os.path.basename(filePDFPath)):
        filePDFPath = folderPath+"/"+os.path.basename(filePDFPath)
except Exception:
    pass
os.chdir(folderPath)
print(filePDFPath)
imagePath = convert_pdf_2_image(filePDFPath)
if  os.path.exists(imagePath):
    print("Running " + os.path.basename(imagePath))
else:
    raise Exception("File Doesn't Exist")
global printingToDisplay
printingToDisplay = True
print("Printing ALL info about document") if printingToDisplay else print("Printing Nothing")
bounds = []
with io.open(imagePath, 'rb') as image_file:
    content = image_file.read()
image = types.Image(content=content)
response = client.document_text_detection(image=image)
global document
document = response.full_text_annotation
global TOTALWIDTHOFDOCUMENT
global TOTALHEIGHTOFDOCUMENT
response4 = client.document_text_detection(image = image)
for i in response4.full_text_annotation.pages:
    TOTALWIDTHOFDOCUMENT = i.width
    TOTALHEIGHTOFDOCUMENT = i.height
if printingToDisplay: print("Called API --> Width:" + str(TOTALWIDTHOFDOCUMENT) + " -- Height: " + str(TOTALHEIGHTOFDOCUMENT))
# findArea --> Inputs the boundingbox from the API and returns area --> polygon calculation
def findArea(bounds):
    matrix = ((bounds.vertices[0].x, bounds.vertices[0].y),
              (bounds.vertices[1].x, bounds.vertices[1].y),
              (bounds.vertices[2].x, bounds.vertices[2].y),
              (bounds.vertices[3].x, bounds.vertices[3].y))
    polygon = Polygon(matrix)
    return polygon.area
# detect_Maximum_outlier --> Using z-score calculate the Outliers on MAX side (0.14% - equal distribution)
def detect_Maximum_outlier(data_1):
    #z = (X — μ) / σ
    #Formula for Z score = (Observation — Mean)/Standard Deviation
    outliers=[]
    threshold=3
    mean_1 = np.mean(data_1)
    std_1 =np.std(data_1)
    for y in data_1:
        z_score= (y - mean_1)/std_1
        if np.abs(z_score) > threshold and y > mean_1:
            outliers.append(y)
    return outliers
# findMaxOutliersIQR --> Using IQR find maximum outliers (x>75%)
def findMaxOutliersIQR(datasetInput):
    dataset = sorted(datasetInput)
    q1, q3= np.percentile(dataset,[25,75])
    iqr = q3 - q1
    upper_bound = q3 +(1.5 * iqr)
    outliers=[]
    for num in dataset:
        if num>upper_bound:
            outliers.append(num)
    return outliers
# find average of both of those outlier calculations
def averageOfBothOutliers(data):
    return (min(detect_Maximum_outlier(data)) + min(findMaxOutliersIQR(data)))/2
# List of all types of character (not punctiuation [a,b....y,x,z,A,B,C...Y,X,Z])
alphaList = list(string.ascii_lowercase) + list(string.ascii_uppercase)
allbbChar = []
# groupsSymbols into 52 groups of alphaList
for charater in alphaList:
    charbb = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    for symbol in word.symbols:
                        if symbol.text == charater:
                            charbb.append(symbol.bounding_box)
    allbbChar.append(charbb)
dfList = []
for i in range(len(allbbChar)):
    charLen = [alphaList[i], len(allbbChar[i])]
    dfList.append(charLen)
    #print(alphaList[i] + "\t" +  str(len(allbbChar[i])))
df=pd.DataFrame(dfList, columns=['Char','NumberOfChars'])
if printingToDisplay: print(df)
def convertBoundBoxtodiagonalRectangual(polygon):
    #print(polygon)
    if (abs(polygon.vertices[0].x - polygon.vertices[3].x)<=1 and
        abs(polygon.vertices[0].y - polygon.vertices[1].y)<=1 and
        abs(polygon.vertices[1].x - polygon.vertices[2].x)<=1 and
        abs(polygon.vertices[2].y - polygon.vertices[3].y)<=1):
        matrixCrop = (min(polygon.vertices[0].x, polygon.vertices[3].x),
                      min(polygon.vertices[0].y, polygon.vertices[1].y),
                      max(polygon.vertices[1].x, polygon.vertices[2].x),
                      max(polygon.vertices[2].y, polygon.vertices[3].y))
    else:
        matrixCrop = (min(polygon.vertices[0].x, polygon.vertices[3].x),
                      min(polygon.vertices[0].y, polygon.vertices[1].y),
                      max(polygon.vertices[1].x, polygon.vertices[2].x),
                      max(polygon.vertices[2].y, polygon.vertices[3].y))
        print("Maybe Error When Converting Polygon To Rectangle")
        #raise Exception
        #matrixCrop = (0,0,0,0)
    return matrixCrop
# convertBoundBoxtodiagonalRectangual --
# Converts the boundingbox API to a matrix format
def findModeLongWay(lst):
    if len(lst) == 0:
        return 0
    from collections import Counter
    d_mem_count = Counter(lst)
    modeLst = []
    for k in d_mem_count.keys():
        if d_mem_count[k] > 1:
            modeLst.append(k)
    try:
        return int(round(statistics.mean(modeLst)))
    except:
        try:
            return int(round(statistics.mean(modeLst)))
        except:
            try:
                print("Error when calculating Mode")
                return int(round(modeLst[0]))
            except:
                return 0
# findModeLongWay -- Sometime when calculating mode using statistics.mode() there could result in error when there
# are multiple modes so this function does it but takes longer
def cutTopandBottomBlackRowsFunction(new_img):
    # GO THROUGH EACH ROW IN ORGINAL PICTURE AND MARK OUT THE ROWS THAT NEED TO BE DELETED
    deleteRows = []
    rowNum = 0
    for row in new_img:
        ct = 0
        for rgb in row:
            if not all(rgb == 0):
                break
            else:
                ct+=1
        #print(ct==len(row))
        if (ct==len(row)):
            deleteRows.append(rowNum)
        rowNum+=1
    # GO THROUGH EACH ROW AND DELETE THE ROWS -- IMG CROPPED TOP AND BOTTOM
    rowCt = 0
    croppedTopBottomImg = []
    for row in new_img:
        if rowCt not in deleteRows:
            newrow = []
            for rgb in row:
                #print(rgb)
                newrow.append([rgb[0], rgb[1], rgb[2]])
            #print(newrow)
            #print(row)
            #print()
            croppedTopBottomImg.append(newrow)
        #print(rowCt)
        rowCt+=1
    return croppedTopBottomImg
# cutTopandBottomBlackRowsFunction --
#    |-----------|              |-XXXXXXXX--|
#    |-XXXXXXXX--|              |-X---------|
#    |-X---------|              |-XXXXXXXX--|
#    |-XXXXXXXX--|    ---->     |-X---------|
#    |-X---------|              |-XXXXXXXX--|
#    |-XXXXXXXX--|         [Removes all the empty space below and above the image]
#    |-----------|
def convertImgto01OrginalFunction(new_img):
    # CONVERT IMAGE TO 0 AND 1 IMAGE FROM THE ORGINAL IMAGE
    newImgOnly01 = []
    for row in new_img:
        newRow = []
        for rgb in row:
            newArrayRowz = []
            for color in rgb:
                if color >= 0.5:
                    newArrayRowz.append(255)
                else:
                    newArrayRowz.append(0)
            newRow.append(newArrayRowz)
        newImgOnly01.append(newRow)
    return newImgOnly01
# convertImgto01OrginalFunction--
# [255,255,255] --> 0/1
# [0,0,0]       --> 0/1
# [255,250,249] --> 0/1
def cropTopBottomFrom01Img(newImgOnly01):
    # FIND ROWS THAT NEED TO BE DELETED FROM 0 AND 1 IMAGE
    deleteRows = []
    rowNum = 0
    for row in newImgOnly01:
        ct = 0
        #print(row)
        for rgb in row:
            #print(rgb)
            if not rgb == [0,0,0]:
                break
            else:
                ct+=1
        #print(ct==len(row))
        if (ct==len(row)):
            deleteRows.append(rowNum)
        rowNum+=1
    # CREATE NEW IMAGE WITH CROPPED 0 AND 1 IMAGES
    rowCt = 0
    croppedTopBottomImgOnly01 = []
    for row in newImgOnly01:
        if rowCt not in deleteRows:
            croppedTopBottomImgOnly01.append(row)
        #print(rowCt)
        rowCt+=1
    return croppedTopBottomImgOnly01
# cropTopBottomFrom01Img -- Same as before crop top and bottom but works with the 0 and 1 image
# Cuts all top and bottom
def percentAreafromImg(img):
    if len(img) == 0:
        return 0
    ctYes = 0
    for row in img:
        for value in row:
            if value != [0,0,0]:
                ctYes+=1
    return round(ctYes/(len(croppedTopBottomImgOnly01)*len(croppedTopBottomImgOnly01[0]))*100,4)
# percentAreafromImg -- Calculates the percent area that is taken by the image
# pixelsAreBlack / totalNumPixels * 100 --> Percent area taken
def findOutlierCutoffIQR(datasetInput):
    dataset = sorted(datasetInput)
    q1, q3= np.percentile(dataset,[25,75])
    iqr = q3 - q1
    return q3 +(1.5 * iqr)
# findOutlierCutoffIQR -- finds the 75th percentile position of data
# this is where it will cut off the outliers (for percent area)
def displayImg(arrayofImgs):
    #plt.figure()
    #f, axarr = plt.subplots(1,len(display))
    #for i in range(len(display)):
        #axarr[i].imshow(display[i])
    print("Display not working")
templst = []
finalListofDataAreataken = []
strokeWidthArray = []
for i in range(len(allbbChar)):
    areaAllForChar = []
    pictureForChar = []
    heightChar = []
    widthChar = []
    for singleChar in allbbChar[i]:
        #Crop the character out of the total image
        cropPoints = convertBoundBoxtodiagonalRectangual(singleChar)
        im = Image.open(imagePath).convert("RGBA")
        im_crop = im.crop(cropPoints)
        #Converts the image into a cv2 compatiable format
        opencvImage = cv2.cvtColor(np.array(im_crop), cv2.COLOR_RGB2BGR)
        img_reverted= cv2.bitwise_not(opencvImage)
        new_img = img_reverted / 255.0
        #Calculated the different values
        heightChar.append(len(new_img)) #This is without cutting off the top and bottom
        widthChar.append(len(new_img[0])) # Vaies due to different character M - big  + I - small
        #croppedTopBottomImg = cutTopandBottomBlackRowsFunction(new_img)
        newImgOnly01 = convertImgto01OrginalFunction(new_img)
        croppedTopBottomImgOnly01 = cropTopBottomFrom01Img(newImgOnly01)
        #display = [new_img,croppedTopBottomImg, newImgOnly01, croppedTopBottomImgOnly01]
        #displayImg(display)
        percentAreaConvert = percentAreafromImg(croppedTopBottomImgOnly01)
        areaAllForChar.append(percentAreaConvert)
        pictureForChar.append(croppedTopBottomImgOnly01)
    #totalWHAllChar.append([heightChar, widthChar])
    try:
        finalListofDataAreataken.append([areaAllForChar, statistics.mode(heightChar), statistics.mode(widthChar)])
    except:
        finalListofDataAreataken.append([areaAllForChar, findModeLongWay(heightChar), findModeLongWay(widthChar)])
    strokeWidthArray.append(pictureForChar)
#print(templst)
dfAllDataForAllChars = []
for i in range(len(dfList)):
    charLstbefore = [dfList[i][0], dfList[i][1]]
    charLstbefore.append(finalListofDataAreataken[i][1])
    charLstbefore.append(finalListofDataAreataken[i][2])
    #print(charLstbefore)
    if not len(finalListofDataAreataken[i][0]) == 0:
        charLstbefore.append(round(statistics.median(finalListofDataAreataken[i][0]), 4))
        charLstbefore.append(round(statistics.mean(finalListofDataAreataken[i][0]), 4))
        try:
            charLstbefore.append(round(statistics.mode(finalListofDataAreataken[i][0]), 4))
        except:
            charLstbefore.append(round(statistics.median(finalListofDataAreataken[i][0]), 4))
        charLstbefore.append(round(findOutlierCutoffIQR(finalListofDataAreataken[i][0]), 4))
        charLstbefore.append(round(len(detect_Maximum_outlier(finalListofDataAreataken[i][0])), 4))
        charLstbefore.append(round(len(findMaxOutliersIQR(finalListofDataAreataken[i][0])), 4))
    else:
        charLstbefore.extend([0, 0, 0, 0, 0, 0])
    dfAllDataForAllChars.append(charLstbefore)
colName = ['Char', 'NumberOfChars', 'ModeHeight', 'ModeWidth', 'MedianArea', 'MeanArea', 'ModeArea',
           'MaxOutlierNum', 'NumOutlierZScore', 'NumOutlierIQR']
dfwithALLdata=pd.DataFrame(dfAllDataForAllChars, columns=colName)
FINALALLINFOLIST = dfAllDataForAllChars
#print(df)
#print("Height")
#print("Mode " + str(statistics.mode(totalWHAllChar[0][0])))
#print("Mean " + str(statistics.mean(totalWHAllChar[0][0])))
#print("Median " + str(statistics.median(totalWHAllChar[0][0])))
#print("Width")
#print("Mode " + str(statistics.mode(totalWHAllChar[0][1])))
#print("Mean " + str(statistics.mean(totalWHAllChar[0][1])))
#print("Median " + str(statistics.median(totalWHAllChar[0][1])))
#print("Height of the picture --> " + str(len(new_img)))
#print("Width of the picture -->  " + str(len(new_img[0])))
# Calculates the mode of the Height and Width of each char
#totalWHAllChar = []
#for numbforChar in range(len(allbbChar)):
#    heightChar = []
#    widthChar = []
#    for singleChar in allbbChar[numbforChar]:
#        cropPoints = convertBoundBoxtodiagonalRectangual(singleChar)
#        im = Image.open(imagePath).convert("RGBA")
#        im_crop = im.crop(cropPoints)
#        opencvImage = cv2.cvtColor(np.array(im_crop), cv2.COLOR_RGB2BGR)
#        img_reverted= cv2.bitwise_not(opencvImage)
#        new_img = img_reverted / 255.0
#        heightChar.append(len(new_img))
#        widthChar.append(len(new_img[0]))
#    #totalWHAllChar.append([heightChar, widthChar])
#    try:
#        totalWHAllChar.append([statistics.mode(heightChar), statistics.mode(widthChar)])
#    except:
#        totalWHAllChar.append([findModeLongWay(heightChar), findModeLongWay(widthChar)])
#f, axarr = plt.subplots(1,4)
#axarr[0].imshow(new_img)
#axarr[1].imshow(croppedTopBottomImg)
#axarr[2].imshow(newImgOnly01)
#axarr[3].imshow(croppedTopBottomImgOnly01)
# Prints info -- Basic
if printingToDisplay: print("There is " + str(len(strokeWidthArray)) + " symbols in the array.\nIts a,b,c,d...x,y,z, "+
                            "A,B,C...X,Y,Z.\nIn each Position is the RGB for that image")
if printingToDisplay: print("Example")
if printingToDisplay: print(strokeWidthArray[0][0][:2])
if printingToDisplay:
    for i in dfAllDataForAllChars:
        if i[1] < 10:
            print("Char "+ i[0] + " has only " + colored(str(i[1]), 'red', attrs=['bold']))

# findPosition  -- doesn't do anything to help but just helps find positions
# Helpful for debugging --
def findPosition(value):
    rowNumb = 0
    for i in dfAllDataForAllChars:
        if value == i[0]:
            return (rowNumb)
        rowNumb+=1
    return 0
# These are a list of quartiles where to find the average stroke width
positions = [["b","0-25"],
             ["c","25-75"],
             ["d","0-25"],
             ["f","75-100"],
             ["h","0-25"],
             ["p","75-100"],
             ["q","75-100"],
             ["t","75-100"],
             ["F","75-100"],
             ["L","0-25"],
             ["T","75-100"],
             ["Y","75-100"]]
newvalue = []
for i in positions:
    x = i
    x.append(findPosition(i[0]))
    newvalue.append(x)
# stokewidthofChar -- basically find the stroke width of the char
def strokewidthofChar(lstValue, quartile):
    #print(0) #0th percentile
    #print(int(heightPic/4)+1) #25 percentile
    #print(int((heightPic/4)*2)+1) #50 percentile
    #print(int((heightPic/4)*3)+1) #75 percentile
    #print(heightPic)#100 percentile
    lstStokeWidth = []
    for i in lstValue:
        running = i
        heightPic = len(running)
        rowNum = 1
        if quartile == "0-25":
            start = 0
            end = int(heightPic/4)+1
        elif quartile == "25-75":
            start = int(heightPic/4)+1
            end = int((heightPic/4)*3)+1
        elif quartile == "75-100":
            start = int((heightPic/4)*3)+1
            end = heightPic
        else:
            print("invalid input for range")
            raise Exception
        for row in running:
            if rowNum < end and rowNum >= start:
                ctYes = 0
                for i in row:
                    if i == [255,255,255]:
                        ctYes+=1
                lstStokeWidth.append(ctYes)
            rowNum+=1
    return lstStokeWidth
def findq1q3(datasetInput):
    dataset = sorted(datasetInput)
    q1, q3= np.percentile(dataset,[25,75])
    return q1, q3
def reject_outliers(data, m=2):
    return data[abs(data - np.mean(data)) < m * np.std(data)]
totalStokeWidth = []
for i in newvalue:
    totalStokeWidth.extend(strokewidthofChar(strokeWidthArray[i[2]], i[1]))
q1, q3 = findq1q3(totalStokeWidth)
#print("All Values")
lstofCount = []
for j in list(set(totalStokeWidth)):
    lstofCount.append([j, sum(i == j for i in totalStokeWidth)])
    #print(str(j) + "\t" + str(sum(i == j for i in totalStokeWidth)))
dfForStrokeWidth=pd.DataFrame(lstofCount, columns=['Detected Width','NumberOfCharsDetected'])
if printingToDisplay: print(dfForStrokeWidth)
if printingToDisplay: print("Stroke width is between " + str(q1) + " - " + str(q3) + ".\nMost likely --> " +
                            str(round(statistics.mean(totalStokeWidth),4)))
STROKEWIDTHFINAL = round(statistics.mean(totalStokeWidth),4)
FINALDFALLCHARINFOLST = []
for char in FINALALLINFOLIST:
    tempArr = char
    tempArr.extend([STROKEWIDTHFINAL])
    FINALDFALLCHARINFOLST.append(tempArr)
colName = ['Char','NumberOfChars','ModeHeight','ModeWidth','MedianArea','MeanArea','ModeArea', 'MaxOutlierNum', 'NumOutlierZScore', 'NumOutlierIQR', 'AvgStrokeWidth']

dfCharacterData=pd.DataFrame(FINALDFALLCHARINFOLST, columns=colName)
lstMode = []
for i in FINALDFALLCHARINFOLST:
    lstMode.append(i[3])
FINALAVGMODEOFCHARS = round(statistics.mean(lstMode),4) #Mode width of the char of ALL
#----------------------------
if printingToDisplay: print(df)
if printingToDisplay: print("Calculated all the infomation about the document now running the 2 differet tests")
#Repeat point
global vowelsNotI
global capitalWeight
global weights
vowelsNotI = ['a','e','o','u']
weights = [[[0, 0, 0, 0],0],
            [[0, 0, 0, 1],0.1],
            [[0, 0, 1, 0],0.2],
            [[0, 0, 1, 1],0.4],
            [[0, 1, 0, 0],0.1],
            [[0, 1, 0, 1],0.3],
            [[0, 1, 1, 0],0.4],
            [[0, 1, 1, 1],0.75],
            [[1, 0, 0, 0],0.1],
            [[1, 0, 0, 1],0.4],
            [[1, 0, 1, 0],0.7],
            [[1, 0, 1, 1],1],
            [[1, 1, 0, 0],0.4],
            [[1, 1, 0, 1],0.75],
            [[1, 1, 1, 0],1],
            [[1, 1, 1, 1],1]]
capitalWeight = 0.6 + 1
# Basically how much extra weight do u want to put to a letter being capital for the first test only
print("CAPITAL WEIGHT IS " + str(capitalWeight-1))
def findMatrix(vert):
    matrix = ((vert.vertices[0].x, vert.vertices[0].y),
              (vert.vertices[1].x, vert.vertices[1].y),
              (vert.vertices[2].x, vert.vertices[2].y),
              (vert.vertices[3].x, vert.vertices[3].y))
    return matrix
def findInfo(wordInfo):
    totalPossibleWeight = 0
    ctTrue1 = 0
    ctTrue2 = 0
    weight = 0
    for i in wordInfo:
        totalPossibleWeight+=4 if i in vowelsNotI else 3
        if i[1] == True:
            ctTrue1+=1
        if i[2] == True:
            ctTrue2+=1
        if not i[0].isalpha():
            weight+=-1
        elif i[1] == True and i[2] == True and i[0].lower() in vowelsNotI:
            weight+=5
        elif i[1] == True and i[2] == True and not i[0].lower() in vowelsNotI:
            weight+=3
        elif (i[1] == True or i[2] == True) and i[0].lower() in vowelsNotI:
            weight+=2
        elif (i[1] == True or i[2] == True) and not i[0].lower() in vowelsNotI:
            weight+=1
        elif i[1] == False or i[2] == False and i[0].lower() in vowelsNotI:
            weight+=-1
        elif i[1] == False or i[2] == False and not i[0].lower() in vowelsNotI:
            weight+=0
        else:
            print("ERROR")
    #print("Weighted Score " + str((weight/totalPossibleWeight)*100))
    #print("Total Percent Bold " + str(((ctTrue1+ctTrue2)/(len(wordInfo)*2))*100))
    #print("Test 1 only Percent Bold " + str(((ctTrue1)/(len(wordInfo)))*100))
    #print("Test 2 only Percent Bold " + str(((ctTrue2)/(len(wordInfo)))*100))
    if (weight/totalPossibleWeight)*100 < 0:
        weightscore = 0
    else:
        weightscore = (weight/totalPossibleWeight)*100
    return [weightscore, ((ctTrue1+ctTrue2)/(len(wordInfo)*2))*100, ((ctTrue1)/(len(wordInfo)))*100, ((ctTrue2)/(len(wordInfo)))*100]
def findInfoSingle(i):
    if i[1] == True and i[2] == True and i[0].lower() in vowelsNotI:
        return True
    elif i[1] == True and i[2] == True:
        return True
    else:
        return False
def convertBoundBoxtodiagonalRectangual(polygon):
    #print(polygon)
    if (abs(polygon.vertices[0].x - polygon.vertices[3].x)<=1 and
        abs(polygon.vertices[0].y - polygon.vertices[1].y)<=1 and
        abs(polygon.vertices[1].x - polygon.vertices[2].x)<=1 and
        abs(polygon.vertices[2].y - polygon.vertices[3].y)<=1):
        matrixCrop = (min(polygon.vertices[0].x, polygon.vertices[3].x),
                      min(polygon.vertices[0].y, polygon.vertices[1].y),
                      max(polygon.vertices[1].x, polygon.vertices[2].x),
                      max(polygon.vertices[2].y, polygon.vertices[3].y))
    else:
        matrixCrop = (min(polygon.vertices[0].x, polygon.vertices[3].x),
                      min(polygon.vertices[0].y, polygon.vertices[1].y),
                      max(polygon.vertices[1].x, polygon.vertices[2].x),
                      max(polygon.vertices[2].y, polygon.vertices[3].y))
        print("MaybeErrrorWhenConvertingPolygonToRectangle")
        #raise Exception
        #matrixCrop = (0,0,0,0)
    return matrixCrop
def polygonwidthCal(polygon):
    # NOT REALLY USED SO DW ABOUT IT
    if (abs(polygon.vertices[0].x - polygon.vertices[3].x)<=1 and
        abs(polygon.vertices[0].y - polygon.vertices[1].y)<=1 and
        abs(polygon.vertices[1].x - polygon.vertices[2].x)<=1 and
        abs(polygon.vertices[2].y - polygon.vertices[3].y)<=1):
        end = max(polygon.vertices[1].x, polygon.vertices[2].x)
        start = min(polygon.vertices[0].x, polygon.vertices[3].x)
    if ((end-start)/TOTALWIDTHOFDOCUMENT)*100 > 80:#-------------------------------------
        return True
    return False
def polygonwidthCalulateOnly(polygon):
    if (abs(polygon.vertices[0].x - polygon.vertices[3].x)<=1 and
        abs(polygon.vertices[0].y - polygon.vertices[1].y)<=1 and
        abs(polygon.vertices[1].x - polygon.vertices[2].x)<=1 and
        abs(polygon.vertices[2].y - polygon.vertices[3].y)<=1):
        end = max(polygon.vertices[1].x, polygon.vertices[2].x)
        start = min(polygon.vertices[0].x, polygon.vertices[3].x)
        return end-start
    else:
        print("MaybeError")
        print(polygon.vertices[1].x, polygon.vertices[2].x)
        end = max(polygon.vertices[1].x, polygon.vertices[2].x)
        start = min(polygon.vertices[0].x, polygon.vertices[3].x)
        return end-start
def calculateWeightForWord(newr):
    if len(newr) == 0:
        return ["", 0, 0, 0]
    returnLst = []
    totalSum = 0
    wordtextrunningsmall = ""
    weight = 0
    for symbol in newr:
        if symbol[0].isalpha():
            if symbol[5] == 1:
                currentValues = symbol[1:5]
                for comb in weights:
                    if comb[0] == currentValues:
                        weight += (comb[1] * capitalWeight)
                        #print(comb, end= ' ')
                        #print(comb[1] * capitalWeight)
            else:
                currentValues = symbol[1:5]
                for comb in weights:
                    if comb[0] == currentValues:
                        weight += comb[1]
                        #print(comb)
        else:
            weight = -1
        totalSum+=symbol[1]+symbol[2]+symbol[3]+symbol[4]
        wordtextrunningsmall+=symbol[0]
    if not wordtextrunningsmall in stop_words:
        returnLst.extend([wordtextrunningsmall, totalSum , weight, len(newr)])
    else:
        returnLst.extend([wordtextrunningsmall, 0, 0, len(newr)])
    #print(wordtextrunningsmall + "--> " + str((totalSum/(len(newr)*4))*100))
    #print((weight/len(newr)*100))
    return returnLst
def countofEach2Lst(lst):
    counterDict = Counter(lst)
    dictList = []
    for key, value in counterDict.items():
        temp = [key,value]
        dictList.append(temp)
    return dictList
def createIMG(lstofthresholds):
    if len(lstofthresholds) != 8:
        raise Exception("Make sure thresholds are correct")
    THRESHOLDSYMBOLMEANTESTWORD = lstofthresholds[0]
    # Splits words into symbols and run tests for each symbol using the findInfo() and their weights.
    # INSIDE THE FIND INFO FUNCTION FOR THE WEIGHTS
    # If the average of all those weights are greater than this number then it is counted
    THRESHOLDPARAGROUPSYMWORD = lstofthresholds[1]
    # Uses same method as the avg of symbols but then add another layer of averge of words
    THRESHOLDFORWORD = lstofthresholds[2]
    # threshold for the weights of the entire word summary (out of 100)
    # VAR = "weights" FOR ALL THE WEIGHTS 0 AND 1 are True and False for each out of the 4 tests
    # 4 tests are mean, median, mode, and outlier
    THRESHOLDFORPARA = lstofthresholds[3]
    # Threshold for each word in the paragraph indiviually. Para can have different thresholds as a single word
    # Also counts in the threshold of "TOTALSUMFINALPARATHRESHOLD"
    CUTOFWORDSTHATARE3ORUNDER = lstofthresholds[4]
    # simple cut off words that are under 3 letters.
    # watch out for arconmys and for words that are incorectly detected  EX: = "&"
    MAXIMUMLENGTHOFWORDSPARA = lstofthresholds[5]
    # the maximum number of words that should be in a paragraph for it to be even counted as a possiblity for bold
    TOTALSUMFINALPARATHRESHOLD = lstofthresholds[6]
    # threshold for average of the total weights for each word in the paragraph (out of 100)
    # same as word (just average)
    THRESHOLDFORANYTHINGTHATISNOTALETTER = lstofthresholds[7]
    # There are 52 detected possible letters in the english dictionary. If it is a punctionaltion or special character
    # it defaults to this number for all of the 4 tests (Mean,median,mode,outlier). EX: "." or "?"\
    bigWordBoundBoxs = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    runningWord = ""
                    uppercaseLetterCt = 0
                    totalSymbolsLeterCt = 0
                    for symbol in word.symbols:
                        if symbol.text.isupper():
                            uppercaseLetterCt+=1
                        totalSymbolsLeterCt+=1
                        runningWord+=symbol.text
                    if uppercaseLetterCt == totalSymbolsLeterCt:
                        bigWordBoundBoxs.append(findArea(word.bounding_box))
    try:
        thresholdAreaCapitailWord = min(findMaxOutliersIQR(bigWordBoundBoxs))
    except ValueError:
        thresholdAreaCapitailWord = max(bigWordBoundBoxs)
    punctionLst = []
    for char in string.punctuation:
        punctionLst.append(char)
    boundingBoxForLargeCapital = []
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    runningWord = ""
                    uppercaseLetterCt = 0
                    totalSymbolsLeterCt = 0
                    for symbol in word.symbols:
                        if symbol.text.isupper():
                            uppercaseLetterCt+=1
                        if not symbol.text in punctionLst:
                            #print(symbol.text)
                            totalSymbolsLeterCt+=1
                        runningWord+=symbol.text
                    if abs(uppercaseLetterCt - totalSymbolsLeterCt) < 1 and findArea(word.bounding_box)/thresholdAreaCapitailWord > 0.5:
                        #print(uppercaseLetterCt, totalSymbolsLeterCt)
                        #print(findArea(word.bounding_box) > thresholdAreaCapitailWord)
                        #print(findArea(word.bounding_box))
                        #print(thresholdAreaCapitailWord)
                        #print(runningWord + "\t" + str(findArea(word.bounding_box)/thresholdAreaCapitailWord))
                        #print("")
                        #print(runningWord)
                        #print(findArea(word.bounding_box))
                        boundingBoxForLargeCapital.append([word.bounding_box, round((findArea(word.bounding_box)/thresholdAreaCapitailWord )* 100,2), runningWord])
    boxesForCharsGoodMean = []
    boxesForCharsbadMean = []
    boxesForCharsGoodOutlier = []
    boxesForCharsbadOutlier = []
    avgSymbolsTest1 = []
    for page in document.pages:
        pg = []
        for block in page.blocks:
            blk = []
            for paragraph in block.paragraphs:
                para = []
                for word in paragraph.words:
                    #numSymbols = 0
                    wordText = ""
                    wordInfo = []
                    for symbol in word.symbols:
                        symbolInfo = []
                        wordText += symbol.text
                        cropPoints = convertBoundBoxtodiagonalRectangual(symbol.bounding_box)
                        if cropPoints[0] == cropPoints[2]:
                            newcropPoints = (cropPoints[0], cropPoints[1], cropPoints[2] + 1, cropPoints[3])
                            cropPoints = newcropPoints
                        im = Image.open(imagePath).convert("RGBA")
                        im_crop = im.crop(cropPoints)
                        opencvImage = cv2.cvtColor(np.array(im_crop), cv2.COLOR_RGB2BGR)
                        img_reverted = cv2.bitwise_not(opencvImage)
                        new_img = img_reverted / 255.0
                        # croppedTopBottomImg = cutTopandBottomBlackRowsFunction(new_img)
                        newImgOnly01 = convertImgto01OrginalFunction(new_img)
                        croppedTopBottomImgOnly01 = cropTopBottomFrom01Img(newImgOnly01)
                        # display = [new_img,croppedTopBottomImg, newImgOnly01, croppedTopBottomImgOnly01]
                        # displayImg(display)
                        percentAreaConverd = percentAreafromImg(croppedTopBottomImgOnly01)
                        boxUpload = False
                        currentSymbolMean = False
                        currentSymbolOutlier = False
                        for charGroup in dfAllDataForAllChars:
                            if charGroup[0] == symbol.text.strip().lower():
                                boxUpload = True
                                # ----------------------------------------------------
                                boxesForCharsGoodMean.append(symbol.bounding_box) if percentAreaConverd >= charGroup[
                                    5] else boxesForCharsbadMean.append(symbol.bounding_box)
                                currentSymbolMean = True if percentAreaConverd >= charGroup[5] else False
                                # ----------------------------------------------------
                                boxesForCharsGoodOutlier.append(symbol.bounding_box) if percentAreaConverd >= charGroup[
                                    7] else boxesForCharsbadOutlier.append(symbol.bounding_box)
                                currentSymbolOutlier = True if percentAreaConverd >= charGroup[7] else False

                        if not boxUpload:
                            # print("Running Extra -->" + symbol.text)
                            # ----------------------------------------------------
                            boxesForCharsGoodMean.append(
                                symbol.bounding_box) if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER else boxesForCharsbadMean.append(
                                symbol.bounding_box)
                            currentSymbolMean = True if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER else False
                            # ----------------------------------------------------
                            boxesForCharsGoodOutlier.append(
                                symbol.bounding_box) if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER else boxesForCharsbadOutlier.append(
                                symbol.bounding_box)
                            currentSymbolOutlier = True if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER else False

                        symbolInfo.extend([symbol.text, currentSymbolMean, currentSymbolOutlier, symbol.bounding_box])
                        wordInfo.append(symbolInfo)
                    wordInfo.append(wordText)
                    wordInfo.append(word.bounding_box)
                    para.append(wordInfo)
                    # para.append()
                blk.append(para)
                blk.append(paragraph.bounding_box)
            pg.append(blk)
            pg.append(block.bounding_box)
        avgSymbolsTest1.append(pg)
    print("Finished")
    """
    **MARKDDOWN**
    |First Test|Second Test|Is Vowel| Weight |
    |--|--|--|--|
    |True|True|True|5|
    |True|True|False|3|
    |True|False|True|2|
    |True|False|False|1|
    |False|True|True|2|
    |False|True|False|1|
    |False|False|True|-1|
    |False|False|False|0|
    """
    avgSymbolsTest1 = avgSymbolsTest1[0]
    boundingBoxAllTest1 = []
    for paraGP in range(0, len(avgSymbolsTest1), 2):
        #print("BLOCK " + str(paraGP/2) + "\t\t" + str(findMatrix(avgSymbolsTest1[paraGP+1])))
        paraGroupTest1=avgSymbolsTest1[paraGP]
        #print(str(len(paraGroupTest1)/2) + " Paragraphs")
        for i in range(0, len(paraGroupTest1), 2):
            #print("\t" + str(i/2) + "\tBounding Box Para\t" + str(findMatrix(paraGroupTest1[i+1])))
            wordSingleRunTest1 = paraGroupTest1[i]
            #print("\t\t" + str(len(wordSingleRunTest1)) + "\t Words")
            stringPrint = ""
            totalScoreForPara = []
            for symbol in wordSingleRunTest1:
                wordArray = symbol[:-2]
                removedBDWordArray = []
                for symbolsOnly in wordArray:
                    removedBDWordArray.append(symbolsOnly[:-1])
                #print(wordArray[-1])
                #for symbol in wordArray:
                    #print("Letter " + symbol[0] + " Test1 " + str(symbol[1]) + " Test2 " + str(symbol[2]))
                scoreAll = findInfo(removedBDWordArray)
                #print("fds" + str(scoreAll))
                if statistics.mean(scoreAll) > THRESHOLDSYMBOLMEANTESTWORD:
                    boundingBoxAllTest1.append([symbol[-1],round(statistics.mean(scoreAll),2), symbol[-2]])
                #print(symbol[-2]  + " "+ str(scoreAll))
                totalScoreForPara.append(scoreAll[0])
                stringPrint += symbol[-2] + " "
                #print(symbol[-1])
            if statistics.mean(totalScoreForPara) > THRESHOLDPARAGROUPSYMWORD:
                boundingBoxAllTest1.append([paraGroupTest1[i+1], round(statistics.mean(totalScoreForPara),4), "N/A"])
                #print("Yes")
            #else:
                #Uncomment if you want it to also highlight small words that are bolded
                #for symbol in wordSingleRunTest1:
                    #wordArray = symbol[:-1]
                    #for symbol in wordArray:
                        #print(symbol)
                        #if findInfoSingle(symbol) and symbol[0].isalpha():
                            #boundingBoxAllTest1.append(symbol[-1])
            #print("\t\t" + stringPrint)
            #print("-----------------------------------------------------------")
        #print("===========================================================")
    boundingBoxWordSimpleSymbolTest = []
    for wordBDScore in boundingBoxAllTest1:
        #print(wordBDScore[0])
        boundingBoxWordSimpleSymbolTest.append([wordBDScore[0], wordBDScore[1], wordBDScore[2]])
    joinedLst = []
    for j in boundingBoxAllTest1: joinedLst.append(j[0])
    for i in boundingBoxForLargeCapital: joinedLst.append(i[0])
    pointsforBD = []
    for i in joinedLst: pointsforBD.append(findMatrix(i))
    ypointsLine = []
    for i in pointsforBD: ypointsLine.append(i[0][1])
    ypointsLine.sort()
    #for x in ypointsLine:
        #print(x, end=' ')
    TINT_COLOR = (0,0,0)
    #colors = [(0,255,0), (0,0,255), (255,0,0)]
    TRANSPARENCY = 0.25
    OPACITY = int(255 * TRANSPARENCY)
    img = Image.open(imagePath)
    img = img.convert("RGBA")
    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    x, y= img.size
    TINT_COLOR = (255,0,0)
    for para in boundingBoxForLargeCapital:
        matrix = findMatrix(para[0])
        draw.polygon(matrix, fill=TINT_COLOR+(OPACITY,))
    TINT_COLOR = (0,255,0)
    for para in boundingBoxAllTest1:
        matrix = findMatrix(para[0])
        draw.polygon(matrix, fill=TINT_COLOR+(OPACITY,))
    for yPos in ypointsLine:
        shape = [(0, yPos-5), (x, yPos-5)]
        draw.line(shape, fill ="black", width = 1)
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB") # Remove alpha for saving in jpg format.
    #img.show()
    #--------------------------------------------------------------------------------------------------------------------------------------------------------
    oldIMG = img
    #os.chdir("/Users/kunal/Documents/VdartResumeProject/VisionAPi/ErosionSaveImg")
    img.save(os.path.basename(imagePath)[:-4] + "1.jpg")
    boxesForCharsGoodMedian = []
    boxesForCharsbadMedian= []
    boxesForCharsGoodMean= []
    boxesForCharsbadMean= []
    boxesForCharsGoodMode= []
    boxesForCharsbadMode= []
    boxesForCharsGoodOutlier= []
    boxesForCharsbadOutlier= []
    dfthingtester = []
    BlockNum = 1
    ParaNum = 1
    WordNum = 1
    for page in document.pages:
        for block in page.blocks:
            for paragraph in block.paragraphs:
                for word in paragraph.words:
                    wordTextRunning = ""
                    for symbol in word.symbols:
                        wordTextRunning += symbol.text
                        cropPoints = convertBoundBoxtodiagonalRectangual(symbol.bounding_box)
                        im = Image.open(imagePath).convert("RGBA")
                        im_crop = im.crop(cropPoints)
                        opencvImage = cv2.cvtColor(np.array(im_crop), cv2.COLOR_RGB2BGR)
                        img_reverted = cv2.bitwise_not(opencvImage)
                        new_img = img_reverted / 255.0
                        # croppedTopBottomImg = cutTopandBottomBlackRowsFunction(new_img)
                        newImgOnly01 = convertImgto01OrginalFunction(new_img)
                        croppedTopBottomImgOnly01 = cropTopBottomFrom01Img(newImgOnly01)
                        # display = [new_img,croppedTopBottomImg, newImgOnly01, croppedTopBottomImgOnly01]
                        # displayImg(display)
                        percentAreaConverd = percentAreafromImg(croppedTopBottomImgOnly01)
                        boxUpload = False
                        medianTF = False
                        meanTF = False
                        modeTF = False
                        outlierTF = False
                        for charGroup in dfAllDataForAllChars:
                            if charGroup[0] == symbol.text.strip().lower():
                                boxUpload = True
                                # ----------------------------------------------------
                                if percentAreaConverd >= charGroup[4]:
                                    boxesForCharsGoodMedian.append(symbol.bounding_box)
                                    medianTF = True
                                else:
                                    boxesForCharsbadMedian.append(symbol.bounding_box)
                                # ----------------------------------------------------
                                if percentAreaConverd >= charGroup[5]:
                                    boxesForCharsGoodMean.append(symbol.bounding_box)
                                    meanTF = True
                                else:
                                    boxesForCharsbadMean.append(symbol.bounding_box)
                                # ----------------------------------------------------
                                if percentAreaConverd >= charGroup[6]:
                                    boxesForCharsGoodMode.append(symbol.bounding_box)
                                    modeTF = True
                                else:
                                    boxesForCharsbadMode.append(symbol.bounding_box)
                                # ----------------------------------------------------
                                if percentAreaConverd >= charGroup[7]:
                                    boxesForCharsGoodOutlier.append(symbol.bounding_box)
                                    outlierTF = True
                                else:
                                    boxesForCharsbadOutlier.append(symbol.bounding_box)
                                # ----------------------------------------------------
                                # break
                        if not boxUpload:
                            # print("Running Extra -->" + symbol.text)
                            # ----------------------------------------------------
                            if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER:
                                boxesForCharsGoodMedian.append(symbol.bounding_box)
                                medianTF = True
                            else:
                                boxesForCharsbadMedian.append(symbol.bounding_box)
                            # ----------------------------------------------------
                            if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER:
                                boxesForCharsGoodMean.append(symbol.bounding_box)
                                meanTF = True
                            else:
                                boxesForCharsbadMean.append(symbol.bounding_box)
                            # ----------------------------------------------------
                            if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER:
                                boxesForCharsGoodMode.append(symbol.bounding_box)
                                modeTF = True
                            else:
                                boxesForCharsbadMode.append(symbol.bounding_box)
                            # ----------------------------------------------------
                            if percentAreaConverd >= THRESHOLDFORANYTHINGTHATISNOTALETTER:
                                boxesForCharsGoodOutlier.append(symbol.bounding_box)
                                outlierTF = True
                            else:
                                boxesForCharsbadOutlier.append(symbol.bounding_box)
                            # ----------------------------------------------------\
                        # print(symbol.text + "\t" + str(medianTF) + "\t" + str(meanTF) + "\t" + str(modeTF) +"\t" +
                        #      str(outlierTF))
                        capital = False
                        if symbol.text.isupper():
                            capital = True

                        dfthingtester.append([symbol.text, medianTF, meanTF, modeTF, outlierTF, capital, WordNum, ParaNum,
                                              BlockNum, word.bounding_box, paragraph.bounding_box, block.bounding_box])
                    WordNum += 1
                ParaNum += 1
            BlockNum += 1
    #print("Finished")
    colName = ["Char", "Median", "Mean", "Mode", "Outlier", "Capital", "Word", "Para", "Block", "WordBD", "ParaBD", "BlockBD"]
    df=pd.DataFrame(dfthingtester, columns=colName)
    #os.chdir(docPath)
    writer = ExcelWriter(os.path.basename(imagePath)[:-4] + '4.xlsx')
    df.to_excel(writer,'Sheet1')
    writer.save()
    dfthingtesterNew01 = []
    for i in dfthingtester:
        newRunningLst = []
        for j in i:
            if j == True:
                newRunningLst.append(1)
            elif j == False:
                newRunningLst.append(0)
            else:
                newRunningLst.append(j)
        dfthingtesterNew01.append(newRunningLst)
    print("TOTAL WORDS --> " + str(dfthingtesterNew01[-1][6]))
    runningWord = 1
    totalForWord = 0
    totalGroups = []
    for wordNumE in range(dfthingtesterNew01[-1][6]):
        newr = []
        for letter in dfthingtesterNew01:
            if letter[6] == wordNumE:
                totalForWord+=letter[1]+letter[2]+letter[3]+letter[4]
                newr.append(letter)
        if newr != []:
            totalGroups.append(newr)
            #print(totalForWord)
            #print(letter)
    lstofParasForLooping = []
    runningCurrent = totalGroups[0][0][10]
    cttemp = 0
    for kk in totalGroups:
        runningCurrentNew = kk[0][10]
        if runningCurrent != runningCurrentNew:
            lstofParasForLooping.append(cttemp - 1)
            runningCurrent = kk[0][10]
        cttemp += 1
    runningBlock = 1
    ctParaGrouping = 0
    #runningPara = 1
    runningCalculationsPara = []
    runningCalculationsBlocks = []
    bdingBoxWord = []
    bdingBoxPara = []
    bdingBoxBlock = []
    if printingToDisplay: print("Calculating if the word/paragraph/block is bold")
    for kk in totalGroups:
        weightedScoreWord = calculateWeightForWord(kk)
        if weightedScoreWord[3] > 0:  # If not then removed
            if CUTOFWORDSTHATARE3ORUNDER:
                if weightedScoreWord[3] >= 3:  # Removes words that are under 3 words long
                    if (weightedScoreWord[2] / weightedScoreWord[3]) * 100 > THRESHOLDFORWORD:
                        if polygonwidthCalulateOnly(kk[0][9]) / FINALAVGMODEOFCHARS > weightedScoreWord[3]:
                            # print(weightedScoreWord[0], end = "\t\t")
                            # print(round(((weightedScoreWord[2]/weightedScoreWord[3])*100),3))
                            if printingToDisplay: print(weightedScoreWord[0] + "\t-->\t" +
                                                        colored(str(
                                                            round(((weightedScoreWord[2] / weightedScoreWord[3]) * 100),
                                                                  2)), 'red', attrs=['bold']))
                            # -----------------------------
                            bdingBoxWord.append(
                                [kk[0][9], round(((weightedScoreWord[2] / weightedScoreWord[3]) * 100), 2),
                                 weightedScoreWord[0]])
                            # --------------------------
            else:  # Checking for less than 3 words long
                if (weightedScoreWord[2] / weightedScoreWord[
                    3]) * 100 > THRESHOLDFORWORD:  # threshold of 70 from the weights weightedScoreWord
                    if polygonwidthCalulateOnly(kk[0][9]) / FINALAVGMODEOFCHARS > weightedScoreWord[3]:
                        # print(weightedScoreWord[0], end = "\t\t")
                        # print(round(((weightedScoreWord[2]/weightedScoreWord[3])*100),3))
                        if printingToDisplay: print(weightedScoreWord[0] + "\t-->\t" +
                                                    colored(str(
                                                        round(((weightedScoreWord[2] / weightedScoreWord[3]) * 100),
                                                              2)), 'yellow', attrs=['bold']))
                        # -----------------------------
                        bdingBoxWord.append([kk[0][9], round(((weightedScoreWord[2] / weightedScoreWord[3]) * 100), 2),
                                             weightedScoreWord[0]])  # removed weightedScoreWord[3] from 2nd position
                        # --------------------------
        # print(kk[7])
        if ctParaGrouping in lstofParasForLooping:
            if runningCalculationsPara != []:
                # NewRun
                # LOOKS LIKE THE CALCULATIONS FOR TOTAL WEIGHTS PARA ARE NOT WORKING
                # totalWeightPara = 0
                # allWordsinPara = ""
                # runningCountYes = 0
                # runningTotal = 0
                # for tempWord in runningCalculationsPara:
                #    totalWeightPara+= (tempWord[2]/tempWord[3])*100
                #    runningCountYes+=tempWord[1]
                #    runningTotal+=(tempWord[3]*4)
                #    allWordsinPara += tempWord[0] + " "
                # print("---------------------------------------")
                # print(allWordsinPara + "  ALL  " + str(totalWeightPara/3))
                # print((runningCountYes/runningTotal)*100)
                # print("-=======================================")
                totalYes = 0
                allWordsinPara = ""
                for tempWord in runningCalculationsPara:
                    if (tempWord[2] / tempWord[3]) * 100 > THRESHOLDFORPARA:
                        totalYes += 1
                    allWordsinPara += tempWord[0] + " "
                # greater than 20 words
                finalParaTotalSum = totalYes / len(runningCalculationsPara) * 100
                if len(
                        runningCalculationsPara) < MAXIMUMLENGTHOFWORDSPARA and finalParaTotalSum > TOTALSUMFINALPARATHRESHOLD:
                    if printingToDisplay: print(
                        str(len(runningCalculationsPara)) + "\t-->\t" + allWordsinPara + "\t-->\t" +
                        colored(str(round(finalParaTotalSum, 3)), 'blue', attrs=['bold']))
                    # print("===================" + allWordsinPara+ "====================" + str(finalParaTotalSum))
                    # -----------------------------
                    print(findMatrix(kk[0][10]))
                    bdingBoxPara.append([kk[0][10], round(finalParaTotalSum, 3), allWordsinPara])
                    # --------------------------
                    runningCalculationsPara = []
        runningCalculationsPara.append(weightedScoreWord)
        ctParaGrouping += 1
        if kk[0][8] != runningBlock:
            if runningCalculationsBlocks != []:
                totalYesBlock = 0
                allWordsinBlock = ""
                for tempWordBlk in runningCalculationsBlocks:
                    if (tempWordBlk[2]/tempWordBlk[3])*100 > 70:
                        totalYesBlock+=1
                    allWordsinBlock += tempWordBlk[0] + " "
                #less than than 20 words
                finalBlkTotalSum = totalYesBlock/len(runningCalculationsBlocks)*100
                if len(runningCalculationsBlocks) < 20 and finalBlkTotalSum > 30:
                    if printingToDisplay: print(str(len(runningCalculationsBlocks)) + "\t-->\t" + allWordsinBlock + "\t-->\t"+
                                                colored(str(round(finalBlkTotalSum,3)), 'green', attrs=['bold']))
                    #print("------------------------" + allWordsinBlock+ "====================" + str(finalBlkTotalSum))
                    #-----------------------------
                    bdingBoxBlock.append([kk[0][11], round(finalBlkTotalSum,3), allWordsinBlock])
                    #--------------------------
            runningCalculationsBlocks=[]
            runningBlock+=1
        else:
            runningCalculationsBlocks.append(weightedScoreWord)
        #-------------------------------------------------------------------------------------------------
    if printingToDisplay: print("Finished")
    AllMatrixes = []
    TINT_COLOR = (0,0,0)
    #colors = [(0,255,0), (0,0,255), (255,0,0)]
    TRANSPARENCY = 0.25
    OPACITY = int(255 * TRANSPARENCY)
    img = Image.open(imagePath)
    img = img.convert("RGBA")
    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    font = ImageFont.truetype(fontPath, size=20)
    #for section in boundBoxAll:
    TINT_COLOR = (0,255,0)
    for block in bdingBoxBlock:
        matrix = findMatrix(block[0])
        draw.polygon(matrix, fill=TINT_COLOR+(OPACITY,))
    #----------------------------------------------------------------------
    TINT_COLOR = (255,0,0)
    for para in bdingBoxPara:
        matrix = findMatrix(para[0])
        AllMatrixes.append(matrix)
        draw.polygon(matrix, fill=TINT_COLOR+(OPACITY,))
    #----------------------------------------------------------------------
    TINT_COLOR = (0,0,255)
    for word in bdingBoxWord:
        matrix = findMatrix(word[0])
        AllMatrixes.append(matrix)
        draw.polygon(matrix, fill=TINT_COLOR+(OPACITY,))
    for wordtxt in bdingBoxWord:
        matrix = findMatrix(wordtxt[0])
        color = 'rgb(0, 0, 0)' # black color
        draw.text((matrix[0][0], matrix[0][1]-20), str(wordtxt[1]), fill=color, font=font)
    #----------------------------------------------------------------------
    TINT_COLOR = (255,0,255)
    for capitalWord in boundingBoxForLargeCapital:
        matrix = findMatrix(capitalWord[0])
        AllMatrixes.append(matrix)
        draw.polygon(matrix, fill=TINT_COLOR+(OPACITY,))
    for capitalWord in boundingBoxForLargeCapital:
        matrix = findMatrix(capitalWord[0])
        color = 'rgb(0, 0, 0)' # black color
        draw.text((matrix[0][0], matrix[0][1]-20), str(capitalWord[1]), fill=color, font=font)
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB") # Remove alpha for saving in jpg format.
    #img
    AllMatrixesNew = []
    for i in bdingBoxWord:
        AllMatrixesNew.append([findMatrix(i[0]), i[1], i[2], "Word"])
    for j in bdingBoxPara:
        AllMatrixesNew.append([findMatrix(j[0]), j[1], j[2], "Para"])
    for k in boundingBoxForLargeCapital:
        AllMatrixesNew.append([findMatrix(k[0]), k[1], k[2], "Capital"])
    for symbol in boundingBoxWordSimpleSymbolTest:
        AllMatrixesNew.append([findMatrix(symbol[0]), symbol[1], symbol[2], "SymbolAvg"])
    AllMatrixSorted = sorted(AllMatrixesNew, key=lambda l: l[0][0][1], reverse=False)
    if printingToDisplay:
        for i in AllMatrixSorted:
            try:
                print(i[2] + "\t-->\t" + colored(str(i[1]), 'red', attrs=['bold']), end= "\t\t")
                if i[3] == "Word - Capital":
                    print(colored("Word Test 2 and Capital", 'green', attrs=['bold']))
                elif i[3] == "Para - Capital":
                    print(colored("Para Test 2 and Capital", 'blue', attrs=['bold']))
                elif i[3] == "Word":
                    print(colored("Word Test 2", 'magenta', attrs=['bold']))
                elif i[3] == "Para":
                    print(colored("Para Test 2", 'cyan', attrs=['bold']))
                elif i[3] == "Capital":
                    print(colored("Capital", 'yellow', attrs=['bold']))
                elif i[3] == "SymbolAvg":
                    print(colored("Test1", 'green', attrs=['bold']))
                elif i[3] == "Word - SymbolAvg":
                    print(colored("Word Test 2 and Test 1", 'blue', attrs=['bold']))
                elif i[3] == "Capital - SymbolAvg":
                    print(colored("Test 1 and Capital", 'grey', attrs=['bold']))
                elif i[3] == "Word - Capital - SymbolAvg":
                    print(colored("Word Test 1 and Test 2 and Capital", 'cyan', attrs=['bold']))
                else:
                    print(i[3])
                #elif entityDrawingInfo[2] == "Para - Capital - SymbolAvg":
                #print(i)
            except TypeError:
                print(i)
    lstofMatrices = []
    for i in AllMatrixesNew:
        lstofMatrices.append(i[0])
    x = countofEach2Lst(lstofMatrices)
    duplicates = []
    for matrix, count in x:
        if count > 1:
            duplicates.append(matrix)
    matrixesPrintDisplay = []
    matrixesforDuplicates = []
    for i in AllMatrixesNew:
        if i[0] in duplicates:
            matrixesforDuplicates.append(i)
        else:
            matrixesPrintDisplay.append([i[0], i[1], i[3]])
    only2duplicate = []
    only3duplicate = []
    for matrix, count in x:
        if count== 2:
            only2duplicate.append(matrix)
        elif count == 3:
            only3duplicate.append(matrix)
    newDuplicatedtoAddedTemp = []
    for i in only2duplicate:
        for j in matrixesforDuplicates:
            if i==j[0]:
                newDuplicatedtoAddedTemp.append(j)
    newDuplicatedtoAddedTemp3 = []
    for i in only3duplicate:
        for j in matrixesforDuplicates:
            if i==j[0]:
                newDuplicatedtoAddedTemp3.append(j)
    DuplicatedtoAddedFINAL = []
    for x in range(0, len(newDuplicatedtoAddedTemp),2):
        #print(newDuplicatedtoAddedTemp[x][0])
        strScores = str(newDuplicatedtoAddedTemp[x][1]) + " - " + str(newDuplicatedtoAddedTemp[x+1][1])
        strtext = str(newDuplicatedtoAddedTemp[x][3]) + " - " + str(newDuplicatedtoAddedTemp[x+1][3])
        DuplicatedtoAddedFINAL.append([newDuplicatedtoAddedTemp[x][0], strScores , strtext])
    DuplicatedtoAddedFINAL3 = []
    for x in range(0, len(newDuplicatedtoAddedTemp3),3):
        #print(newDuplicatedtoAddedTemp[x][0])
        strScores = str(newDuplicatedtoAddedTemp3[x][1]) + " - " + str(newDuplicatedtoAddedTemp3[x+1][1]) + " - " + str(newDuplicatedtoAddedTemp3[x+2][1])
        strtext = str(newDuplicatedtoAddedTemp3[x][3]) + " - " + str(newDuplicatedtoAddedTemp3[x+1][3]) + " - " + str(newDuplicatedtoAddedTemp3[x+2][3])
        DuplicatedtoAddedFINAL3.append([newDuplicatedtoAddedTemp3[x][0], strScores , strtext])
    displayINFO = DuplicatedtoAddedFINAL + matrixesPrintDisplay + DuplicatedtoAddedFINAL3
    TRANSPARENCY = 0.25
    OPACITY = int(255 * TRANSPARENCY)
    img = Image.open(imagePath)
    img = img.convert("RGBA")
    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    for entityDrawingInfo in displayINFO:
        if entityDrawingInfo[2] == "Word - Capital":
            TINT_COLOR = (255,0,0)
        elif entityDrawingInfo[2] == "Para - Capital":
            TINT_COLOR = (0,255,0)
        elif entityDrawingInfo[2] == "Word":
            TINT_COLOR = (0,0,255)
        elif entityDrawingInfo[2] == "Para":
            TINT_COLOR = (255,0,255)
        elif entityDrawingInfo[2] == "Capital":
            TINT_COLOR = (255,255,0)
        elif entityDrawingInfo[2] == "SymbolAvg":
            TINT_COLOR = (0,255,255)
        elif entityDrawingInfo[2] == "Word - SymbolAvg":
            TINT_COLOR = (138, 28, 163)
        elif entityDrawingInfo[2] == "Capital - SymbolAvg":
            TINT_COLOR = (255, 166, 0)
        elif entityDrawingInfo[2] == "Word - Capital - SymbolAvg":
            TINT_COLOR = (159, 227, 113)
        elif entityDrawingInfo[2] == "Para - Capital - SymbolAvg":
            TINT_COLOR = (113, 174, 227)
        elif entityDrawingInfo[2] == "Para - SymbolAvg":
            TINT_COLOR = (90, 200, 10)
        else:
            print(entityDrawingInfo[2])
            raise Exception("SomethingWentWrong")
        draw.polygon(entityDrawingInfo[0], fill=TINT_COLOR+(OPACITY,))
        color = 'rgb(0, 0, 0)' # black color
        draw.text((entityDrawingInfo[0][0][0], entityDrawingInfo[0][0][1]-20), str(entityDrawingInfo[1]), fill=color, font=font)
    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB") # Remove alpha for saving in jpg format.
    displayINFOnotPara = []
    for i in displayINFO:
        if i[2] != "Para":
            displayINFOnotPara.append(i)
    TRANSPARENCY = 0.25
    OPACITY = int(255 * TRANSPARENCY)
    img = Image.open(imagePath)
    img = img.convert("RGBA")
    overlay = Image.new('RGBA', img.size, TINT_COLOR+(0,))
    draw = ImageDraw.Draw(overlay)  # Create a context for drawing things on it.
    for entityDrawingInfo in displayINFOnotPara:
        if entityDrawingInfo[2] == "Word - Capital":
            TINT_COLOR = (255,0,0)
        elif entityDrawingInfo[2] == "Para - Capital":
            TINT_COLOR = (0,255,0)
        elif entityDrawingInfo[2] == "Word":
            TINT_COLOR = (0,0,255)
        elif entityDrawingInfo[2] == "Para":
            TINT_COLOR = (255,0,255)
        elif entityDrawingInfo[2] == "Capital":
            TINT_COLOR = (255,255,0)
        elif entityDrawingInfo[2] == "SymbolAvg":
            TINT_COLOR = (0,255,255)
        elif entityDrawingInfo[2] == "Word - SymbolAvg":
            TINT_COLOR = (138, 28, 163)
        elif entityDrawingInfo[2] == "Capital - SymbolAvg":
            TINT_COLOR = (255, 166, 0)
        elif entityDrawingInfo[2] == "Word - Capital - SymbolAvg":
            TINT_COLOR = (159, 227, 113)
        elif entityDrawingInfo[2] == "Para - Capital - SymbolAvg":
            TINT_COLOR = (113, 174, 227)
        elif entityDrawingInfo[2] == "Para - SymbolAvg":
            TINT_COLOR = (90, 200, 10)
        else:
            print(entityDrawingInfo[2])
            raise Exception("SomethingWentWrong")
        draw.polygon(entityDrawingInfo[0], fill=TINT_COLOR+(OPACITY,))
        color = 'rgb(0, 0, 0)' # black color
        draw.text((entityDrawingInfo[0][0][0], entityDrawingInfo[0][0][1]-20), str(entityDrawingInfo[1]), fill=color, font=font)
    draw.rectangle(((0,0),(390, 180)), fill=(255,255,255), outline = "black")
    color = 'rgb(0, 0, 0)'
    draw.text((0,0), "1-Avg Symbols Score for Word", fill=color, font=font)
    draw.text((0,20), "1-Avg Para Score", fill=color, font=font)
    draw.text((0,40), "1-Capital Plus weight", fill=color, font=font)
    draw.text((0,60), "2-Weight Score for Word", fill=color, font=font)
    draw.text((0,80), "2-Weight Score for Para", fill=color, font=font)
    draw.text((0,100), "2-3 Words or Less", fill=color, font=font)
    draw.text((0,120), "2-Max Words in Para", fill=color, font=font)
    draw.text((0,140), "2-Avg Weight Score for Para", fill=color, font=font)
    draw.text((0,160), "2-Threshold non-chars", fill=color, font=font)
    color = 'rgb(255, 0, 0)'
    draw.text((350,0), str(THRESHOLDSYMBOLMEANTESTWORD), fill=color, font=font)
    draw.text((350,20), str(THRESHOLDPARAGROUPSYMWORD), fill=color, font=font)
    draw.text((350,40), str(capitalWeight-1), fill=color, font=font)
    draw.text((350,60), str(THRESHOLDFORWORD), fill=color, font=font)
    draw.text((350,80), str(THRESHOLDFORPARA), fill=color, font=font)
    draw.text((350,100), str(CUTOFWORDSTHATARE3ORUNDER)[0], fill=color, font=font)
    draw.text((350,120), str(MAXIMUMLENGTHOFWORDSPARA) , fill=color, font=font)
    draw.text((350,140), str(TOTALSUMFINALPARATHRESHOLD), fill=color, font=font)
    draw.text((350,160), str(THRESHOLDFORANYTHINGTHATISNOTALETTER), fill=color, font=font)

    img = Image.alpha_composite(img, overlay)
    img = img.convert("RGB") # Remove alpha for saving in jpg format.
    #img
    # oldIMG for old one
    x = datetime.datetime.now()
    #os.chdir("/Users/kunal/Documents/VdartResumeProject/VisionAPi/ErosionSaveImg")
    filename = os.path.basename(imagePath)[:-4] + str(x)[5:10]+"_"+str(x)[11:16] + "FINAL.jpg"
    img.save(filename)
    print("FINISHED ALL")
    print("Saved   -->" + str(filename))
    print("1 - THRESHOLDSYMBOLMEANTESTWORD --> Splits words into symbols and run tests for each symbol using the findInfo() and their weights.")
    print("\t If the average of all those weights are greater than this number then it is counted")
    print("\t\t" + str(THRESHOLDSYMBOLMEANTESTWORD) + "\t\t\n")
    print("1 - THRESHOLDPARAGROUPSYMWORD --> Uses same method as the avg of symbols but then add another layer of averge of words")
    print("\t\t" + str(THRESHOLDPARAGROUPSYMWORD) + "\t\t\n")
    print("1 - capitalWeight --> how much extra weight for capital words")
    print("\t\t" + str(capitalWeight-1) + "\t\t\n")
    print("2 - THRESHOLDFORWORD --> threshold for the weights of the entire word summary (out of 100)")
    print("\t VAR = \"weights\" FOR ALL THE WEIGHTS 0 AND 1 are True and False for each out of the 4 tests --> mean, median, mode, and outlier")
    print("\t\t" + str(THRESHOLDFORWORD) + "\t\t\n")
    print("2 - THRESHOLDFORPARA --> Threshold for each word in the paragraph indiviually. Para can have different thresholds as a single word")
    print("\t Also counts in the threshold of \"TOTALSUMFINALPARATHRESHOLD\"")
    print("\t\t" + str(THRESHOLDFORPARA) + "\t\t\n")
    print("2 - CUTOFWORDSTHATARE3ORUNDER --> Simple cut off words that are under 3 letters.")
    print("\t Watch out for arconmys and for words that are incorectly detected  EX: = \"&\"")
    print("\t\t" + str(CUTOFWORDSTHATARE3ORUNDER)[0] + "\t\t\n")
    print("2 - MAXIMUMLENGTHOFWORDSPARA --> The maximum number of words that should be in a paragraph for it to be even counted as a possiblity for bold")
    print("\t\t" + str(MAXIMUMLENGTHOFWORDSPARA) + "\t\t\n")
    print("2 - TOTALSUMFINALPARATHRESHOLD --> threshold for average of the total weights for each word in the paragraph (out of 100)")
    print("\t same as word (just average)")
    print("\t\t" + str(TOTALSUMFINALPARATHRESHOLD) + "\t\t\n")
    print("2 - THRESHOLDFORANYTHINGTHATISNOTALETTER --> There are 52 detected possible letters in the english dictionary. If it is a punctionaltion or special character")
    print("\t it defaults to this number for all of the 4 tests (Mean,median,mode,outlier). EX: \".\" or \"?\"")
    print("\t\t" + str(THRESHOLDFORANYTHINGTHATISNOTALETTER) + "\t\t\n")
    thresholdTxt = ("Avg Symbols Word " + str(THRESHOLDSYMBOLMEANTESTWORD) + "  Avg Word Score " +
                    str(THRESHOLDPARAGROUPSYMWORD) + "    " + str(THRESHOLDFORWORD) + "  Weight Para " +
                    str(THRESHOLDFORPARA) + " Remove words len(3) or less" + str(CUTOFWORDSTHATARE3ORUNDER) +
                    "  Max Words in Para" + str(MAXIMUMLENGTHOFWORDSPARA) + "  Final Sum Para" +
                    str(TOTALSUMFINALPARATHRESHOLD))
    #print(thresholdTxt)
    return (AllMatrixSorted, img)
#THRESHOLDSYMBOLMEANTESTWORD, THRESHOLDPARAGROUPSYMWORD, THRESHOLDFORWORD, THRESHOLDFORPARA, CUTOFWORDSTHATARE3ORUNDER,
#MAXIMUMLENGTHOFWORDSPARA, TOTALSUMFINALPARATHRESHOLD
#THRESHOLDSYMBOLMEANTESTWORD =
# Splits words into symbols and run tests for each symbol using the findInfo() and their weights.
# INSIDE THE FIND INFO FUNCTION FOR THE WEIGHTS
# If the average of all those weights are greater than this number then it is counted
#THRESHOLDPARAGROUPSYMWORD =
# Uses same method as the avg of symbols but then add another layer of averge of words
#THRESHOLDFORWORD =
# threshold for the weights of the entire word summary (out of 100)
# VAR = "weights" FOR ALL THE WEIGHTS 0 AND 1 are True and False for each out of the 4 tests
# 4 tests are mean, median, mode, and outlier
#THRESHOLDFORPARA =
# Threshold for each word in the paragraph indiviually. Para can have different thresholds as a single word
# Also counts in the threshold of "TOTALSUMFINALPARATHRESHOLD"
#CUTOFWORDSTHATARE3ORUNDER =
# simple cut off words that are under 3 letters.
# watch out for arconmys and for words that are incorectly detected  EX: = "&"
#MAXIMUMLENGTHOFWORDSPARA =
# the maximum number of words that should be in a paragraph for it to be even counted as a possiblity for bold
#TOTALSUMFINALPARATHRESHOLD =
# threshold for average of the total weights for each word in the paragraph (out of 100)
# same as word (just average)
#THRESHOLDFORANYTHINGTHATISNOTALETTER =
# There are 52 detected possible letters in the english dictionary. If it is a punctionaltion or special character
# it defaults to this number for all of the 4 tests (Mean,median,mode,outlier). EX: "." or "?"
"""
**Char(0)-Median(1)-Mean(2)-Mode(3)-Outlier(4)-Capital(5)-Word Count(6)-Paragraph Count(7)-Block Count(8)-WordBD(9)-ParaBD(10)-BlockBD(11)**

|Median|Mean|Mode|Outlier|Weight|
|--|--|--|--|--|
|0|0|0|0|0|
|0|0|1|0|0.1|
|0|0|1|0|0.2|
|0|0|1|1|0.4|
|0|1|0|0|0.1|
|0|1|0|1|0.3|
|0|1|1|0|0.4|
|0|1|1|1|0.75|
|1|0|0|0|0.1|
|1|0|0|1|0.4|
|1|0|1|0|0.7|
|1|0|1|1|1|
|1|1|0|0|0.4|
|1|1|0|1|0.75|
|1|1|1|0|1|
|1|1|1|1|1|
"""
lstofThresholds1 = [0, 3, 10, 0, True, 10, 0, 30]
AllMatrixSorted, TEST1PIL = createIMG(lstofThresholds1)
print(AllMatrixSorted)
dfFINALINFO =pd.DataFrame(AllMatrixSorted)



#os.chdir("/Users/kunal/Documents/VdartResumeProject/Erosion/")
#writer = ExcelWriter(os.path.basename(imagePath)[:-4] + 'xxxxxxxx2.xlsx')
#dfFINALINFO.to_excel(writer,'Sheet1')
#writer.save()

TEST1PIL.save(os.path.basename(imagePath)[:-4] + 'FINALIMAGERUN.jpg')

def show_wait_destroy(winname, img):
    img = cv2.resize(img, (960, 540))
    cv2.imshow(winname, img)
    cv2.moveWindow(winname, 500, 0)
    cv2.waitKey(0)
    cv2.destroyWindow(winname)
def calculateLocationOfLines(picMatrix, horizontal):
    lstofLines = []
    rowNum = 0
    picMatrix = picMatrix if horizontal else picMatrix.T
    for row in picMatrix:
        if any(row) != 0:
            ctStart = 0
            distance = 0
            linePos = False
            for columnSingle in row:
                if columnSingle == 0:
                    ctStart+=1
                    linePos = True
                else:
                    distance+=1
            lstofLines.append([rowNum, ctStart,ctStart+distance, distance])
        rowNum+=1
    return lstofLines
def img2HorizontalLines(horizontal):
    # Specify size on horizontal axis
    cols = horizontal.shape[1]
    horizontal_size = cols // 30
    # Create structure element for extracting horizontal lines through morphology operations
    horizontalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (horizontal_size, 1))
    # Apply morphology operations
    horizontal = cv2.erode(horizontal, horizontalStructure)
    horizontal = cv2.dilate(horizontal, horizontalStructure)
    # Show extracted horizontal lines
    #show_wait_destroy("horizontal", horizontal)
    return horizontal
def checkIfImgExists(img):
    # Load the image
    src = cv2.imread(img, cv2.IMREAD_COLOR)
    # Check if image is loaded fine
    if src is None:
        print('Error opening image: ' + img)
        raise Exception("ERROR")
    # Show source image
    #cv2.imshow("src", src)
    return src


def findHorizontalLines(img, display):
    src = checkIfImgExists(img)
    # Transform source image to gray if it is not already
    if len(src.shape) != 2:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    else:
        gray = src
    # Show gray image
    # show_wait_destroy("gray", gray)
    # Apply adaptiveThreshold at the bitwise_not of gray, notice the ~ symbol
    gray = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                               cv2.THRESH_BINARY, 15, -2)
    # Show binary image
    # show_wait_destroy("binary", bw)
    if display:
        plt.imshow(bw)
        plt.show()
    # [bin]
    # [init]
    # Create the images that will use to extract the horizontal and vertical lines
    horizontal = np.copy(bw)

    horizontalConverted = img2HorizontalLines(horizontal)

    if display:
        plt.imshow(horizontalConverted)
        plt.show()
    lstofLinesHorizontal = calculateLocationOfLines(horizontalConverted, True)
    print("YPos - Starting - Ending - Distance")
    return lstofLinesHorizontal
def img2VerticalLines(vertical):
    # Specify size on vertical axis
    rows = vertical.shape[0]
    verticalsize = rows // 30
    # Create structure element for extracting vertical lines through morphology operations
    verticalStructure = cv2.getStructuringElement(cv2.MORPH_RECT, (1, verticalsize))
    # Apply morphology operations
    vertical = cv2.erode(vertical, verticalStructure)
    vertical = cv2.dilate(vertical, verticalStructure)
    # Show extracted vertical lines
    #show_wait_destroy("vertical", vertical)
    return vertical


def findVerticalLines(img, display):
    src = checkIfImgExists(img)
    # Transform source image to gray if it is not already
    if len(src.shape) != 2:
        gray = cv2.cvtColor(src, cv2.COLOR_BGR2GRAY)
    else:
        gray = src
    # Show gray image
    # show_wait_destroy("gray", gray)
    # Apply adaptiveThreshold at the bitwise_not of gray, notice the ~ symbol
    gray = cv2.bitwise_not(gray)
    bw = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                               cv2.THRESH_BINARY, 15, -2)
    # Show binary image
    # show_wait_destroy("binary", bw)
    if display:
        plt.imshow(bw)
        plt.show()
    # [bin]
    # [init]
    # Create the images that will use to extract the horizontal and vertical lines
    vertical = np.copy(bw)

    verticalConverted = img2VerticalLines(vertical)

    if display:
        plt.imshow(verticalConverted)
        plt.show()
    lstofLinesVertical = calculateLocationOfLines(verticalConverted, False)
    print("HPos - Starting - Ending - Distance")
    # return lstofLinesVertical, verticalConverted
    return verticalConverted
vertical = findVerticalLines(imagePath, False)
horz = findHorizontalLines(imagePath, False)
similar = []
for i in horz:
    similar.append(i[0])
rowNums = []
for i in range(len(horz)):
    rowNums.append("Line " + str(i+1))
dfHorzLines = pd.DataFrame(horz, index = rowNums, columns= ["YPos","Starting","Ending","Distance"])
vert = []
countLinesVert = 0
for i in vertical:
    if any(i) != 0:
        countNumsInEachRow = 0
        for j in i:
            if j != 0:
                endingPos = j
                countNumsInEachRow +=1
        vert.append([countLinesVert, endingPos-countNumsInEachRow, endingPos, endingPos- (endingPos-countNumsInEachRow)])
    countLinesVert+=1
colsNumsVert = []
for i in range(len(vert)):
    colsNumsVert.append("Column " + str(i+1))
dfVertLines = pd.DataFrame(vert, index = colsNumsVert, columns= ["YPos","Starting","Ending","Distance"])

def findFace(imgPath):
    image = cv2.imread(imgPath)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3)
    faceArrayLst = []
    for i in faces:
        faceArrayLst.append(((i[0], i[1]), (i[0]+i[2], i[1]), (i[0]+i[2], i[1]+i[3]), (i[0], i[1]+i[3])))
    return faceArrayLst
faceArray = findFace(imagePath)
faceArrayDetailed = []
for i in faceArray:
    faceArrayDetailed.append([i[0][0], i[0][1], i[1][0], i[1][1], i[2][0], i[2][1], i[3][0], i[3][1], i])
rowNums = []
for i in range(len(faceArrayDetailed)):
    rowNums.append("Face " + str(i+1))
colNums = ["Top Left X", "Top Left Y", "Top Right X", "Top Right Y",
           "Bottom Left X", "Bottom Left Y", "Bottom Right X", "Bottom Right Y", "Matrix"]
dfFaces = pd.DataFrame(faceArrayDetailed, index=rowNums, columns=colNums)
data = ResumeParser(imagePath).get_extracted_data()
dictlist = []
for key in data:
    temp = [key,data[key]]
    dictlist.append(temp)
dfEntities = pd.DataFrame(dictlist, columns =["Entity Name", "Value"])

credentials = service_account.Credentials.from_service_account_file(keyDIRDocumentAI) #using service account to go through google
client = documentai.DocumentUnderstandingServiceClient(credentials=credentials)
gcs_source = documentai.types.GcsSource(uri="gs://document_ai_resume/Document_402.pdf")
# mime_type can be application/pdf, image/tiff,
# and image/gif, or application/json
input_config = documentai.types.InputConfig(gcs_source=gcs_source, mime_type='application/pdf')
def _get_text(el, document):
    """Doc AI identifies form fields by their offsets
    in document text. This function converts offsets
    to text snippets.
    """
    response = ''
    # If a text segment spans several lines, it will
    # be stored in different text segments.
    for segment in el.text_anchor.text_segments:
        start_index = segment.start_index
        end_index = segment.end_index
        response += document.text[start_index:end_index]
    return response
# Setting enabled=True enables form extraction
table_extraction_params = documentai.types.TableExtractionParams(enabled=True)
# Location can be 'us' or 'eu'
parent = 'projects/{}/locations/us'.format("resumematcher")
request = documentai.types.ProcessDocumentRequest(
    parent=parent,
    input_config=input_config,
    table_extraction_params=table_extraction_params)
document = client.process_document(request=request)
documentFormParser = document

dfArray = []
tableGroups = []
for page in document.pages:
    tablesPerPage = []
    dfArray.append('Page number: {}'.format(page.page_number))
    for table_num, table in enumerate(page.tables):
        dfArray.append('Table {}: '.format(table_num))
        singleTable = []
        for row_num, row in enumerate(table.header_rows):
            cells = ''.join([_get_text(cell.layout, documentFormParser) for cell in row.cells])
            dfArray.append('Header Row {}: {}'.format(row_num, cells))
            singleTable.append(["Header",row_num,cells])
        for row_num, row in enumerate(table.body_rows):
            cells = ''.join([_get_text(cell.layout, documentFormParser) for cell in row.cells])
            dfArray.append('Row {}: {}'.format(row_num, cells))
            singleTable.append(["Row", row_num, cells])
        tablesPerPage.append([singleTable, table_num])
    tableGroups.append([tablesPerPage, page.page_number])

dfTables = pd.DataFrame(dfArray)


#os.chdir("/Users/kunal/Documents/VdartResumeProject/Erosion/")
writer = ExcelWriter(os.path.basename(imagePath)[:-4] + '.xlsx')
dfCharacterData.to_excel(writer,'Character_Data')
dfHorzLines.to_excel(writer,'HorizontalLines_Data')
dfVertLines.to_excel(writer,'VerticalLines_Data')
dfFaces.to_excel(writer,'Faces_Data')
dfEntities.to_excel(writer,'Entities_Detected_Data')
dfFINALINFO.to_excel(writer, 'BoldWordsDetected_Data')
dfTables.to_excel(writer, 'Tabular_Data')

writer.save()




ENDCODETIME = datetime.datetime.now()
print(ENDCODETIME - STARTCODETIME)

