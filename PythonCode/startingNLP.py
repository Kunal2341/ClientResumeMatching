# Basic libaries
import os
import pandas as pd
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
# For PDF to Image
from pdf2image import convert_from_path
# For Image to Text
from google.cloud import vision
from google.oauth2 import service_account
import io
import ntpath

def convert_pdf_2_image(uploaded_image_path, uploaded_image, savingDir):
    project_dir = os.getcwd()
    os.chdir(uploaded_image_path)
    file_name = str(uploaded_image).replace('.pdf','')
    output_file = file_name+'.jpg'
    pages = convert_from_path(uploaded_image, 200,poppler_path='/Users/kunal/Documents/VdartWorking/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/')
    os.chdir(savingDir)
    for page in pages:
        page.save(output_file, 'JPEG')
        break
    #os.chdir(project_dir)
    #img = Image.open(output_file)
    #img = img.resize(img_size, PIL.Image.ANTIALIAS)
    #img.save(output_file)
    return output_file

#convert_pdf_2_image('/Users/kunal/Documents/ResumeNLPVdart/Testing_Delete/', "Document_402.pdf")

def convertToText(imagePath):
    keyDIR = "/Users/kunal/Documents/VdartWorking/GOOGLEAPI/vdartrealfakevision-0f30bdc03946.json"
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








