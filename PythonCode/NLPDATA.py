import os, random

doubleCheckSentenceSplitterCount = 0
doubleCheckSentenceSplitterCount2 = 0
while True:
    sentenceSplitter = input("Do you want to run sentence splitter? : ").lower().strip()
    if sentenceSplitter == "yes" and doubleCheckSentenceSplitterCount >=1:
        break
    elif sentenceSplitter == "yes":
        print("This is a double check if you want to do the sentence splitter on the document?")
        doubleCheckSentenceSplitterCount += 1
    elif sentenceSplitter == "no" and doubleCheckSentenceSplitterCount2 >=1:
         break
    elif sentenceSplitter == "no":
        doubleCheckSentenceSplitterCount2 +=1
    elif sentenceSplitter == "BREAK":
        print("Exiting")
        break
    else:
        print("Document was invalid. Input >>> BREAK <<< to stop")
        continue

