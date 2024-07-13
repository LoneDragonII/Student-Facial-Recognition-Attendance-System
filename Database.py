#You will require a serviceAccountKey.json from firebase
import PySimpleGUI as sg
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from datetime import datetime
import queue

# Initialize the app with a service account, granting admin privileges
cred = credentials.Certificate("serviceAccountKey.json")
#paste the appropriate URLs here
firebase_admin.initialize_app(cred, {
    'databaseURL': ""
})

# Reference to the Students node in the database
ref = db.reference('Students')

def update_database(values, queue):
    student_id = values['-ID-']
    name = values['-NAME-']
    roll_no = values['-ROLL-']
    department = values['-DEPT-']
    batch = values['-BATCH-']
    total_attendance = values['-TOTAL-']
    last_attendance = values['-LAST-']
    data = {
        "Name": name,
        "Roll No": roll_no,
        "Department": department,
        "Batch": batch,
        "Total Attendance": total_attendance,
        "Last Attendance": last_attendance
    }
    ref.child(student_id).set(data)
    queue.put(('clear', '-ID-'))
    queue.put(('clear', '-NAME-'))
    queue.put(('clear', '-ROLL-'))
    queue.put(('clear', '-DEPT-'))
    queue.put(('clear', '-BATCH-'))
    queue.put(('clear', '-TOTAL-'))
    queue.put(('update', ('-LAST-', datetime.now().strftime('%Y-%m-%d %H:%M:%S'))))

    window = sg.Window('Update Database')
    window.close()