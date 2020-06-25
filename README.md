# ClientResumeMatching
A client company is looking for employees. Employees are looking for jobs. Employees send in a resume and the company sends in a job description. Extract exact which resume matches the job description the best. 

## Main topics for the resume
- Skillset
- Qualifications
- Work Experience
- Career objectives
## Main topics for the Jary (free flow text from company)
- Skill set
- Experience
- Location
- Responsibilities
- Role

## Flow plan 
1.  Create a dataset of skill sets and similar skills to each using dice
	2. [https://www.dice.com/skills](https://www.dice.com/skills)
	3. Use firebase database
	4. Use web scraping → robotic process automation web scraping
2.  Connect the 50 resumes to the firebase database
	3. Be able to make database dynamic with easier to 
3.  Using NLP analysis resume getting basic understand
	4. Create new database where we can save this preliminary data
4.  Build on the main topics of the resume and connect them to the generated topic 
	5. This will be the basics of understanding
5.  Connect the website to the python code
	6. With this we must also connect the database
6.  Develop website to upload documents to database
7. Connect main topics of the Jary  
8.  Generate a SVD for understanding the topics (unstructured data)
9.  Use and Bayes Theorem and Naive Bayes to generate a basic outline of both documents
10.  U	sing transfer learning build a running base model (Spacy)
11.  Optimize model for speed and accuracy
