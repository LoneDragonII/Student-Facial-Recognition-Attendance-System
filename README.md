This Project was deployed on Jetson Nano wiht Python==3.7. You Will require WSL to run it on Windows.
I built this project following Murtaza's Workshop - Robotics and AI on YouTube and then further refined and built off it to give the project a complete app type look.

# Facial Recognition Based Attendance System.

This is my Final Year Project presented for my BE in Avionics Engineering in 2024 at the Institute of Space Technology. The project aimed to develop an AI-based Attendance System tailored for the Avionics Department, specifically to alleviate administrative burdens, particularly within the Final Year Project Lab. The system is designed to be efficient, contactless, and hygienic, addressing the need for enhanced safety and operational ease. It offers scalability with minimal modifications, providing a robust prototype for departmental use. The project's objective was to create a working prototype that can be further refined and fully deployed across the department.

https://github.com/user-attachments/assets/ff24a78f-896f-4056-847b-6f3e0aca2422

## Features

The main interface for the attendance system was created using PySimpleGUI which provides a consolidated menu to launch every implemented feature and also displays the outputs on the side which ensures the system is running as expected.

![image](https://github.com/user-attachments/assets/d6fb9771-258a-42b6-8357-3a22b4c3a5e2)

### 1. Mark Attendance

The Mark Attendace launches the main Attendance marking system. The live camera feed is on the left and after the student is detected, their attendance is marked and thir information is displayed on the right side.

![image](https://github.com/user-attachments/assets/62d037e0-09eb-4ecf-8db2-f038c4043d25)

The right side of the attendance system has four modes that change accordingly during the attendance marking process (with ngl unfunny jokes my professors made during my degree XD).

![image](https://github.com/user-attachments/assets/9672c7da-dae4-4598-b929-b5a286666ddf)


### 2. Add Students

This button opens up a new window where we can capture the picture of a new student who is to be added to our system. It takes the picture in a 216x216 pixel format since that is what's being used by the face_recognition python library.

![image](https://github.com/user-attachments/assets/b91202be-c148-4b80-a119-f31db7518409)

### 3. Added Students

Let’s us view the current Students that are in the system according to roll number.

![image](https://github.com/user-attachments/assets/e4a4c78f-993c-414d-8a86-dc490bc2d1b1)

### 4. Proxy Check
The frame at which that student gets marked present gets stored inside a folder created by date inside the "check" directory, named according to the detected student to which the Admin/Teacher can then navigate to and see incase anyone marked attendance of a student using a picture or a phone.

![image](https://github.com/user-attachments/assets/28259e10-2684-48cd-b004-9690fb31dc28)

### 5. View Attendance

The generated CSVs are saved in the attendance folder, labeled by date. Users can view the attendances within the application. Each attendance entry contains three columns: Student Name, Roll No., and the date and time when the attendance was marked.
![image](https://github.com/user-attachments/assets/81b0ceda-623d-428e-b909-44c0db140aea)

### 6. Update System

This button updates the encoding files used by the facial recognition attendance system and uploads the images to the database's storage bucket, where they are used by the attendance system. Execution times may vary depending on the internet connection and the type of hardware being used.

![image](https://github.com/user-attachments/assets/9392b5e0-365b-4b01-9bb1-f45cec66799f)

### 7. Update Database

After clicking this button a window popps up where the student's information is filled in by the user which is to be used during attendance. The last attendance date is automatically filled as a reference starting point. Clicking "Submit" automatically updates the database. The student's total attendance is updated automatically during the attendance marking process moving forward. By providing the student ID, corrections to the database can be made through the system rather than manually modifying the database. Note that the student ID must be the same as the roll number.

![image](https://github.com/user-attachments/assets/b9847698-0ea2-495d-b87e-f5c7bb835492)

![image](https://github.com/user-attachments/assets/2023bfb2-8c8c-4849-b9bc-b27b43389d5a)

## Complete System Working

![image](https://github.com/user-attachments/assets/d243c5ac-4f1f-41ee-af11-bbfa4ff721ea)

## face_recognition library general overview on how it works

for more detailed understanding on how face_recognition actually works, you can visit their offical github page.

![image](https://github.com/user-attachments/assets/db61abee-3189-4bdd-83d6-ca2e1208920c)

## Encodings & How The System Distinguishes Between Students

The encodings are high-dimensional numerical representations of key features of a person’s face. During attendance, the student’s face will be extracted, and its encodings will be calculated. The Euclidean distance between the new and saved encodings is measured. With a threshold of 60%, the encoding with the least distance is considered the predicted person.

![image](https://github.com/user-attachments/assets/43cf2691-86fb-4afa-947c-729419a1c364)

## Testing on Unseen Data

To test the system on unseen data, five directories were labeled according to student roll numbers. Each directory contained 110 images of the respective student. In 100 images, the students were facing the camera directly. The remaining 10 images had varying degrees of head rotation. The system proved quite accurate only showing a few hiccups where the the system was unable to identify the student with excessive head rotation.

![image](https://github.com/user-attachments/assets/2faf9c84-bac3-48d9-833d-88883ac13872)

## Limited Scalability Issue

WHile the current system is scalable, it is only upt a certain extent. When the number of people increase, it becomes harder and harder for face_recognition to distinguish between people. This can be rectified further by using L-SVM or NL-SVM. Since my project was deployed on a Jetson and i was using it on low power mode, this feature was not implemented on it.

![image](https://github.com/user-attachments/assets/df33420e-c4fb-43fd-b563-26d051bc7797)

## Running on your own local system.

As mentioned before you will require Python version 3.7 to run this project ( any Python ver below 3.8 will work fine i used Python 3.7.6. There are a few issue importing dlls with higher Python version at the moment on Windows. As for running it on Linux with higher versions it might be possible but i did not test this. This project was deployed on Jetson Nano 4Gb so i used its global repository to download and setup Python as the other versions required to built manually.

face_recoognition library requires Dlib and Cmake to be installed as well. On Linux, specifically for Jetson, there is a small change that needs to be in the source file of the code. This can be found on the official article of using face_recogtnition on Jetson on the medium website. 

As for how to use the system, just simply paste 216x216 images of the students in the Images folder and click the update system button or you can use the Add Student feature as well. Make sure you have your AccountServiceKey.json in the root directory of the project as well. Additionallly for better security you can create a simple text file that imports all appropriate URLs for the system to communicate with firebase or just paste them directly into the code ( I donot recomend doing this even though this is how I've done it because I had to explain this properly during a demo video. Its best not to show show the AccountServiceKey.jason or your URLs since it can be a potential security risk. 

The System was deployed on a test enviornment on FireBase.

## Thats ALL! Hope this project helps you out if you need it!
