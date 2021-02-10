from pdf2image import convert_from_path #Libary convert pdf file to img file
import os
import spacy
nlp = spacy.load("en_core_web_sm")

doc = '/Users/kunal/Documents/VdartResumeProject/VisionAPi/Document_619.pdf'
docPath = '/Users/kunal/Documents/VdartResumeProject/VisionAPi/'
pdfIMGPopplerPath = '/Users/kunal/Documents/VdartResumeProject/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/'

def convert_pdf_2_image(uploaded_image_path, uploaded_image):
    #Using the convert_from_path function
    #Same name as pdf but converted to img
    #Watch out for poppler -- necceasary to function
    os.chdir(uploaded_image_path) # Change the working diretory to path that contains the PDF file
    file_name = str(uploaded_image).replace('.pdf','') # file name for png still going to get changed later
    pages = convert_from_path(uploaded_image, 200,poppler_path=pdfIMGPopplerPath) #function to change pdf to img
    pageNumCount = 1 #numbering for all the different images if pdf is multiple pages
    outputNames = []
    for page in pages:
        output_file = file_name+"_"+str(pageNumCount) + '.jpg'#uptaded name for image
        page.save(output_file, 'JPEG')#save img
        pageNumCount +=1
        outputNames.append(output_file)
    return outputNames #names of img

output = convert_pdf_2_image(docPath, doc)
print(output)