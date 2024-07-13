#You will require a serviceAccountKey.json from firebase
import cv2
import os
import pickle
import face_recognition
import numpy as np
import cvzone
import firebase_admin
import csv
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime

# Get the current date
current_date = datetime.now().strftime("%m-%d-%y")  # Format the date as 'MM-DD-YY'

# Initialize the app with a service account, granting admin privileges
#paste the appropriate URLs here
cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': "",
    'storageBucket': ""
})

cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 480)

# Load the background image
img_Background = cv2.imread('Resources/background.png')

# Import images that initiate mode change
folderModePath = 'Resources/Modes'
modePathList = os.listdir(folderModePath)
imgModeList = [cv2.imread(os.path.join(folderModePath, path)) for path in modePathList]

# Load encodings
print("Loading Encodings")
with open('Encodings.p', 'rb') as file:
    encodeListWithIDs = pickle.load(file)
encodeList, studentIDs = encodeListWithIDs
print("Successfully loaded Encodings")

bucket = storage.bucket()
modeType = 0
counter = 0
StudentImg = []
idx = -1
# Initialize variables
frame_count = 0
face_locations = []
face_encodings = []

while True:
    success, img = cap.read()
    if success:
        imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)
        face_locations = face_recognition.face_locations(imgS)
        face_encodings = face_recognition.face_encodings(imgS, face_locations)
        img_Background[162:162+480, 55:55+640] = img
        img_Background[44:44+633, 808:808+414] = imgModeList[modeType]
        if face_locations:
            for FaceEncode, FaceLock in zip(face_encodings, face_locations):
                matches = face_recognition.compare_faces(encodeList, FaceEncode)
                FaceDistance = face_recognition.face_distance(encodeList, FaceEncode)
                matchIndex = np.argmin(FaceDistance)
                if matches[matchIndex]:
                    # If a new face is detected, reset counter and modeType
                    if idx != studentIDs[matchIndex]:
                        counter = 0
                        modeType = 0
                    idx = studentIDs[matchIndex]
                    y1, x2, y2, x1 = FaceLock
                    y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                    bbox = (55+x1, 162+y1, x2-x1, y2-y1)
                    img_Background = cvzone.cornerRect(img_Background, bbox, rt=0)
                    if counter == 0:
                        cvzone.putTextRect(img_Background,"Please Wait",(275,400))
                        cv2.imshow("IST Students Attendance System", img_Background)
                        cv2.waitKey(1)
                        counter = 1
                        modeType = 1
        if counter !=0:
            if counter ==1:
                studentInfo = db.reference (f'Students/{idx}').get()
                blob = bucket.get_blob(f'Images/{idx}.png')
                # Check if blob is None
                if blob is None:
                    print(f"No image found for student {idx}")
                    continue
                array = np.frombuffer(blob.download_as_string(),np.uint8)
                StudentImg = cv2.imdecode(array,cv2.COLOR_BGRA2BGR)
                datetimeObject = datetime.strptime(studentInfo['Last Attendance'],
                                                 "%Y-%m-%d %H:%M:%S")
                secondsElapsed = (datetime.now()-datetimeObject).total_seconds()
                if secondsElapsed >60:
                    ref = db.reference(f'Students/{idx}')
                    studentInfo['Total Attendance'] = int(studentInfo['Total Attendance']) + 1
                    ref.child('Total Attendance').set(studentInfo['Total Attendance'])
                    ref.child('Last Attendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                    
                    # Write attendance to CSV file
                    filename = 'attendance/' + datetime.now().strftime("%Y-%m-%d") + '.csv'
                    with open(filename, 'a', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow([studentInfo['Name'], studentInfo['Roll No'], datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
                    
                    # Save frame as image
                    image_filename = 'check/' + datetime.now().strftime("%Y-%m-%d") + '/' + studentInfo['Name'] + '.png'
                    os.makedirs(os.path.dirname(image_filename), exist_ok=True)
                    cv2.imwrite(image_filename, img)
                else:
                    modeType = 3
                    counter = 0
                    img_Background[44:44+633, 808:808+414] = imgModeList[modeType]
            if modeType !=3:
                if 10<counter<20:
                    modeType = 2
                img_Background[44:44+633, 808:808+414] = imgModeList[modeType]
                if counter<=10:
                    cv2.putText(img_Background,str(studentInfo['Total Attendance']),(861,125),
                                cv2.FONT_HERSHEY_TRIPLEX,1,(255,255,255),1)
                    cv2.putText(img_Background,str(studentInfo['Roll No']),(960,495),
                                cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1)
                    cv2.putText(img_Background,str(studentInfo['Department']),(960,553),
                                cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1)
                    cv2.putText(img_Background,str(studentInfo['Batch']),(959,625),
                                cv2.FONT_HERSHEY_TRIPLEX,0.6,(100,100,100),1)
                    cv2.putText(img_Background, current_date,(1115,625),
                                cv2.FONT_HERSHEY_TRIPLEX,0.6,(100,100,100),1)
                    cv2.putText(img_Background,str(studentInfo['Name']),(960,443),
                            cv2.FONT_HERSHEY_TRIPLEX,0.5,(255,255,255),1)
                    img_Background[175:175+216,909:909+216] = StudentImg
                counter +=1
                if counter>=20:
                    counter = 0
                    modeType = 0
                    studentInfo = []
                    StudentImg = []
                    img_Background[44:44+633, 808:808+414] = imgModeList[modeType]
        else:
            modeType = 0
            counter = 0
        cv2.imshow("IST Students Attendance System", img_Background)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        counter +=1