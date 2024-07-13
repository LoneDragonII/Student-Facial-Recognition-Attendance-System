#You will require a serviceAccountKey.json from firebase
import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

# Initialize the app with a service account, granting admin privileges
#paste the appropriate URLs here
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket': ""
})


#Importing Verified Person's Images
folderPath = 'Images'
PathList = os.listdir(folderPath)
imgList = []
studentIDs = []

print("Please wait Blob is Uploading files to Database")
for path in PathList:

    imgList.append(cv2.imread(os.path.join(folderPath,path)))
    studentIDs.append(os.path.splitext(path)[0])
    
    fileName = f'{folderPath}/{path}'
    bucket = storage.bucket()
    blob = bucket.blob(fileName)
    blob.upload_from_filename(fileName)
    
print("Successfully Uploaded Files!!!")
print(studentIDs)

def Encodings(imagesList):
    encodeList = []
    for img in imagesList:
        img = cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList


print("Please Wait Image Encoding in Progress")
encodeList = Encodings(imgList)
encodeListWithIDs = [encodeList, studentIDs]
print("Finished Encoding")


file = open("Encodings.p",'wb')
pickle.dump(encodeListWithIDs,file)
file.close()
print("Encoding File Saved")