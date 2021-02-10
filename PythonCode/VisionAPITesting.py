from google.oauth2 import service_account #Control API Keys
from google.cloud import vision
from pdf2image import convert_from_path #Libary convert pdf file to img file
import os
import io
import random
from random import randrange
doc = '/Users/kunal/Documents/VdartResumeProject/VisionAPi/Document_402.pdf'
docPath = '/Users/kunal/Documents/VdartResumeProject/VisionAPi/'
imgTxtVisionAPIPath = "/Users/kunal/Documents/VdartResumeProject/APIKEYSGOOGLE/resumeMatcher-pdf2img.json"
pdfIMGPopplerPath = '/Users/kunal/Documents/VdartResumeProject/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/'
imagePath = '/Users/kunal/Documents/VdartResumeProject/VisionAPi/Document_402_1.jpg'
#Using API from Google
#Returns a JSON file but text is extracted from it
keyDIR = imgTxtVisionAPIPath #JSON key file to call the api
credentials = service_account.Credentials.from_service_account_file(keyDIR) #using service account to go through google
client = vision.ImageAnnotatorClient(credentials=credentials) # client api

