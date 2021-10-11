
# Client Resume Matcher 
### Connecting Employees to Employers
A client company is looking for employees. Employees are looking for jobs. Employees send in a resume and the company sends in a job description. Extract exact which resume matches the job description the best.
## Learning more about how it works
All my reasearch and powerpoint descriptions are in this directory
https://github.com/Kunal2341/ClientResumeMatching/tree/master/DocumentsEXPLAINING
# Architecture Diagram
Example architecture of the process of the program. Lays out the details for database connections and fucntions deployment. 
![Architecture Diagram](https://github.com/Kunal2341/ClientResumeMatching/blob/master/DocumentsEXPLAINING/WorkFlowVdart.PNG?raw=true)

# Naive Baise Classifier
The following Jupyter Notebook gives a step-by-step description on Naive Baise Classifier
https://github.com/Kunal2341/ClientResumeMatching/blob/master/Jnotebooks/Naive%20Bayes%20Classifier.ipynb

# External APIs
Uses GCP cloud platform and their vision, NLP, and entity extraction APIs which support the process of the program

-   Vision API  
	- Uses OCR to convert PDFs to readable files and gives location information about the text groups
-   NLP API
	- Extract Basic entities from document
- Entity Extraction API  
	- Using custom built AI to extract entities for common designs of resumes
- Document AI
	- To get the data in a tabular form
## GCP Entity Extraction Personal Model
The data is still being generated but the model will be able to extract entities from the resume. Check https://github.com/Kunal2341/ClientResumeMatching/blob/master/Jnotebooks/ALL%20CODE%20.ipynb to learn more. 
![Example GCP Entity Extraction UI](https://raw.githubusercontent.com/Kunal2341/ClientResumeMatching/master/DocumentsEXPLAINING/GCPEntityExtraction.png)
# How to run it

Must install **requirments.txt** in order to have all the different libaries
Open Command Prompt - Navigate to where you installed *requirments.txt* and run 
It takes **~ 2 minutes** to run
```
pip install -r requirements.txt
```
The file is displayed below
```python
numpy==1.18.5
pandas==1.2.0
google-cloud-documentai==0.3.0
google-cloud==0.34.0
google-auth==1.23.0
google-auth-oauthlib==0.4.2
google-cloud-storage==1.35.1
google-cloud-vision==2.0.0
imutils==0.5.4
opencv-python==4.5.1.48
oauthlib==3.1.0
pdf2image==1.14.0
Pillow==8.1.0
scipy==1.6.0
spacy==3.0.1
Shapely==1.7.1
termcolor==1.1.0
webcolors==1.11.1
pyresparser==1.0.6
en-core-web-lg @ https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.0.0/en_core_web_lg-3.0.0-py3-none-any.whl
```
## File Managment
Before Running
```
└── ResumeFiles
    └── Document_201.pdf
    └── Document_202.pdf
    └── Document_203.pdf
```
After Running
```
└── ResumeFiles
    └── Document_201
	    └── Document_201.pdf
	    └── Document_201_1.jpg
	    └── Document_201_1.xlsx
	    └── Document_402_1FINALIMAGERUN.png
	    └── Document_402_11.jpg
	    └── Document_402_14.xlsx
	    └── Document_402_102-10_09
    └── Document_202.pdf
    └── Document_203.pdf
```
## Pdf2image

So for my project I really struggled in converting a pdf to a image so here is a step by step instuction\

1. Install pdf2image 
	1. `pip install pdf2image`
2.  Install poppler
	1. This is very important
	2. [https://poppler.freedesktop.org/](https://poppler.freedesktop.org/)
		3. Click on "https://poppler.freedesktop.org/poppler-0.86.1.tar.xz" 
		4.  This will install a compressed file of poppler so then you use 7zip (must install seperatly)
		5.  Once you extract it, move the file to your specific location
		6. Now you know the poppler location path
3. Make sure you have these libaries imported. Use `pip install` if not working
	4. `import PIL`
	5. `from PIL import Image`
	6. `from pdf2image import convert_from_path`	
	7. `import os`
4. Code
**Make sure you change your poppler path**
```python
def convert_pdf_2_image(uploaded_image_path, uploaded_image,img_size):
    project_dir = os.getcwd()
    os.chdir(uploaded_image_path)
    file_name = str(uploaded_image).replace('.pdf','')
    output_file = file_name+'.jpg'
    pages = convert_from_path(uploaded_image, 200,poppler_path='/Users/kunal/Documents/VdartWorking/Poppler/poppler-0.68.0_x86/poppler-0.68.0/bin/')
    for page in pages:
        page.save(output_file, 'JPEG')
        break
    os.chdir(project_dir)
    img = Image.open(output_file)
    img = img.resize(img_size, PIL.Image.ANTIALIAS)
    img.save(output_file)
    return output_file

os.chdir("/Users/kunal/Documents/")
convert_pdf_2_image("/Users/kunal/Documents/", "invite.pdf", (200,200))
```
# Final Output
Check **ExampleResult.txt** for an example printed result
The Final Output will be the *Document_201_1.xlsx* file. Inside the file you get data about 
 - Character_Data 
	- Each character *a-z* and *A-Z* data 
		- Number of those Characters in Document
		- Mode of the Height of Character
		- Mode of the Width of Character
		- Median of the area taken up by the character
		- Mean of the area taken up by the character
		- Mode of the area taken up by the character
		- Largest Area taken up by a character
		- Z-score of the distribution of the area of that character
		- IQR of the distribition of the area of that character
		- Approximate stroke width of all characters
 - HorizontalLines_Data 
	- Vertical-Position
	- Starting Point
	- Ending Point
	- Length of line
 - VerticalLines_Data 
	- 	Horzontal-Position
	- Starting Point
	- Ending Point
	- Length of line
 - Faces_Data
	- Top Left X
	 - Top Left Y 
	 - Top Right X 
	 - Top Right Y 
	 - Bottom Left X 
	 - Bottom Left Y 
	 - Bottom Right X 
	 - Bottom Right Y 
	 - Matrix
 - Entities_Detected_Data
	 - name
	- email
	- mobile_number
	- skills
	- college_name
	- degree
	- designation
	- experience
	- company_names
	- no_of_pages
	- total_experience
 - BoldWordsDetected_Data
	 - Matrix
	 - Score
	 - Word
	 - Which way it achieves threshold
 - Tabular_Data
	 - Header
	 - Row
	 - Value
# Character Data
The first 2 rows out of all 56 is shown below. 
This data can be vital to understand and calculate to understand if a entire word is bold. Check lines **62-330**  for  more information

|Char|NumberOfChars|ModeHeight|ModeWidth|MedianArea|MeanArea|ModeArea|MaxOutlierNum|NumOutlierZScore|NumOutlierIQR|AvgStrokeWidth|
|-|-|-|-|-|-|-|-|-|-|-|
|a|159|31|10|46.1538|47.7806|46.1538|60.1099|1|17|2.8397|
|b|21|31|12|35.4067|36.207|35.406|52.1931|0|0|2.8397

# Bold Words
|Part|Threshold Name|Definition|Number|
|-|-|-|-|
|1|THRESHOLDSYMBOLMEANTESTWORD|Splits words into symbols and run tests for each symbol using the findInfo() and their weights. If the average of all those weights are greater than this number then it is counted|0|
|1|THRESHOLDPARAGROUPSYMWORD|Uses same method as the avg of symbols but then add another layer of averge of words|3|
|1|capitalWeight |How much extra weight for capital words|0.6|
|2|THRESHOLDFORWORD |threshold for the weights of the entire word summary (out of 100) VAR = "weights" FOR ALL THE WEIGHTS 0 AND 1 are True and False for each out of the 4 tests --> mean, median, mode, and outlier|10|
|2|THRESHOLDFORPARA |Threshold for each word in the paragraph indiviually. Para can have different thresholds as a single word. Also counts in the threshold of "TOTALSUMFINALPARATHRESHOLD"|0|
|2|CUTOFWORDSTHATARE3ORUNDER |Simple cut off words that are under 3 letters. 	 Watch out for arconmys and for words that are incorectly detected  EX: = "&"|T|
|2|MAXIMUMLENGTHOFWORDSPARA |The maximum number of words that should be in a paragraph for it to be even counted as a possiblity for bold|10|
|2|TOTALSUMFINALPARATHRESHOLD |threshold for average of the total weights for each word in the paragraph (out of 100) - same as word (just average)|0|
|2|THRESHOLDFORANYTHINGTHATISNOTALETTER|There are 52 detected possible letters in the english dictionary. If it is a punctionaltion or special character. It defaults to this number for all of the 4 tests (Mean,median,mode,outlier). EX: "." or "?"|30|

# Faces
An example Image is the following once the face has been highlighted on Document
The area is the calculated using a Polygon Matrix 
**((114, 157), (399, 157), (399, 442), (114, 442))**
Each is a point on a polygon as shown in the image
![Example Highlighted Face Img](https://raw.githubusercontent.com/Kunal2341/ClientResumeMatching/master/DocumentsEXPLAINING/FacehighlightedExample.png)

# Entities Data
An Example Result is as the following
|Key|Data|
|-|-|
|Name|Serhii Kalinin|
|Email|kalininsergg92@gmail.com|
|Mobile Number|437-231-5807|
|Skills| ['Algorithms','Reports','Quality management','Usability','Quality assurance','Automation','Sql','Windows','Linux','Segmentation','Programming',  'Agile','Workflow','Python','Java','Recruiting','System','Javascript'...]
|College Name|None|
|Degree|Bachelor of veterinary medicine|
|Designation(Race)| ['Ukrainian - native']|
|Experience|['LLC Materialise Ukraine','Apr 2019 — March 2020','Test-Engineer',  'Image recognition algorithms testing;','Manual QA Engineer','April 2018 — April 2019','Start IT Training Center','Febr 2018 — April 2018','QA Trainee', 'Espresso Window', 'Sept 2015 — Febr 2018', 'Small business co-founder and co-owner', ...]
|Page Count| 5|
|total_experience|4.67|

# Horizontal and Veritcal Lines
This can be used to detect page breaks and other major sectioning in the resume
## Horizontal Lines
The first 3 lines of an example result of Horizontal lines is the following
|Line #|YPos|Starting|Ending|Distance|
|-|-|-|-|-|
|1|146|1319|1654|335|
|2|206|1439|1654|215|
|3|207|1439|1654|215|

## Vertical Lines
Were not detected in this document but the format will be the same as Horizontal lines except it will be HPos instead of YPos. 

# Tabular Data
This is from the DocumentAI API from GCP. 
An example is the following:

```
Page number: 1
Table 0: 
Header Row 0: Finance Consultant, Consulting Engagements (3 Firms), 2018-2020

Row 0: • Interim o o o Director Of Finance & Interim Controller, Aptitude Health (Engaged by RGP), 2019-2020
Issue & Scope: Director Of Finance for $17 Million multi-entity organization resigned with short notice
Tools & Analysis: Intacct & Excel
Findings & Results: Fulfilled month-end & year-end responsibilities with minimal training & guidance,
enabling organization to continue financial operations without disruption; Performed analysis that yielded

Row 1: 95% decrease in quarterly commissions calculations time; Improved financial processes

Row 2: • IT Finance Consultant, McKesson (Engaged by Strive Consulting), 2019
```
# Entities Document AI
This is using the Document AI API which returnns a list of major values in the Document with their score. An example is shown below:
|Entity|Percent Accurate|[Number of Times detected, Start Index, End Index]|
|-|-|-|
|kalininsergg92@gmail.com|0.966053|[[1, 59, 91]]|
|437-231-58-07|0.939058|[[1, 92, 112]]|
|05/27/1992|0.486468|[[1, 113, 137]]|

This can be used to understand what exactly the document is doing

# Entites Form Key Value Document AI
This can be much more usefull than the Entities Form because it gives a Key to the Value in a dictonary format
|Key|Value|Percent Accurate|Page #|
|-|-|-|-|
|E-mail:|kalininsergg92@gmail.com\n|0.966053|1|
|Phone:|437-231-58-07\n|0.939058|1
|DATE OF BIRTH\n|05/27/1992\n|0.486468|1|

# Conclusion
This project and give a very conclusive result for any resume. 
I need to uptade the code so that it will adapt to resumes for multiple pages. 

Made by Kunal Aneja through Vdart Digital.
kunal.aneja101@gmail.com
