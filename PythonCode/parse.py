import datetime
STARTCODETIME = datetime.datetime.now() #Setting up time to find total time spent on code
from google.oauth2 import service_account #Control API Keys
from google.cloud import vision
import os, cv2
from pdf2image import convert_from_path
import string, spacy
from stop_words import get_stop_words
import shutil

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
    os.chdir(os.path.dirname(filePath))
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