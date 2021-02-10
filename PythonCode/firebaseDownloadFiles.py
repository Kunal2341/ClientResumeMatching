from firebase import firebase

storage = firebase.storage()
datadir = "/Users/kunal/Documents/ResumeNLPVdart"

all_files = storage.child("myfirebasefolder").list_files()

for file in all_files:
    try:
        file.download_to_filename(datadir + file.name)
    except:
        print('Download Failed')