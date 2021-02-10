# Client Resume Matcher 
### Connecting Employees to Employers
A client company is looking for employees. Employees are looking for jobs. Employees send in a resume and the company sends in a job description. Extract exact which resume matches the job description the best.

# External APIs
Uses GCP cloud platform and their vision, NLP, and entity extraction APIs which support the process of the program

-   Vision API  
	- Uses OCR to convert PDFs to readable files and gives location information about the text groups
-   NLP API
	- Extract Basic entities from document
- Entity Extraction API  
	- Using custom built AI to extract entities for common designs of resumes

# How to run it

Must install **requirments.txt** in order to have all the different libaries
Open Command Prompt - Navigate to where you installed *requirments.txt* and run 
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
Were not detected in this document

# 
