
from google.cloud import storage
from firebase import firebase
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="/Users/kunal/Documents/ResumeNLPVdart/JSON/resumematcher-8706e-a196bc9dec39.json"
firebase = firebase.FirebaseApplication('https://resumematcher-8706e.firebaseio.com/')
client = storage.Client()
bucket = client.get_bucket('resumematcher-8706e.appspot.com')
# posting to firebase storage
imageBlob = bucket.blob("/")
# imagePath = [os.path.join(self.path,f) for f in os.listdir(self.path)]
imagePath = "/Users/kunal/Documents/ResumeNLPVdart/flaskWebsite/uploadedFiles/Document_402.pdf"
imageBlob = bucket.blob("TestingDocument")
imageBlob.upload_from_filename(imagePath)