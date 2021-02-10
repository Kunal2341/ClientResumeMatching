import os
from pdf2image import convert_from_path
import ntpath
from google.oauth2 import service_account
from google.cloud import vision
import io
def convert_pdf_2_image(uploaded_image_path, uploaded_image):
    project_dir = os.getcwd()
    os.chdir(uploaded_image_path)
    file_name = str(uploaded_image).replace('.pdf','')
    output_file = file_name+'.jpg'
    pages = convert_from_path(uploaded_image, 200,poppler_path='/Users/kunal/Documents/VdartWorking/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/')
    for page in pages:
        page.save(output_file, 'JPEG')
        break
    return output_file
def convert_img_2_text(imagePath):
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
import spacy
nlp = spacy.load("en_core_web_sm")
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
for i in textList:
    doc = nlp(i)
    EMAILLIST = extract_emails(doc)
    email_count = 1
    for email, start, end in EMAILLIST:
        print(str(email_count) + ":  " +  email)
        email_count+=1
    print("\n")
    NAMELIST = extract_person_names(doc)
    name_count = 1
    for name, start, end in NAMELIST:
        print(str(name_count) + ":  " + name)
        name_count +=1







