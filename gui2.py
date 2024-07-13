import PySimpleGUI as sg
import os
from PIL import Image
import csv
import io
import subprocess
import threading
import cv2
import numpy as np
import queue
from datetime import datetime
from Database import update_database  # Import the function from your Database.py script

# Create a queue
output_queue = queue.Queue()

# Define the window layout
layout = [[sg.Text('')],
          [sg.Text('')],
          [sg.Text('')],
          [sg.Text('')],
          [sg.Button('Mark Attendance', size=(20, 2), pad=((540, 512), 1))],
          [sg.Text('')],
          [sg.Button('Add Students', size=(20, 2), pad=((540, 512), 1))],  # Add Students button
          [sg.Text('')],
          [sg.Button('Added Students', size=(20, 2), pad=((540, 512), 1))],
          [sg.Text('')], 
          [sg.Button('Proxy Check', size=(20, 2), pad=((540, 512), 1))],
          [sg.Text('')], 
          [sg.Button('View Attendance', size=(20, 2), pad=((540, 512), 1))],
          [sg.Text('')],
          [sg.Button('Update System', size=(20, 2), pad=((540, 512), 1))],  # Update System button
          [sg.Text('')],
          [sg.Button('Update Database', size=(20, 2), pad=((540, 512), 1))],  # Update Database button
          [sg.Text('')],
          [sg.Button('Exit', size=(20, 2), pad=((540, 512), 1))],  # Exit button
          [sg.Text('')],
          [sg.Text('')],
          [sg.Text('')],
          [sg.Text('')]]

# Create the window
window = sg.Window('IST Student Attendance System', layout, size=(1280,720))

def run_script(script):
    process = subprocess.Popen(['python', script], stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == '' or process.poll() is not None:
            break
        if output:
            output_queue.put(output.strip())  # Put the output in the queue
    rc = process.poll()
    return rc

def add_student():
    layout = [[sg.Text('Enter Roll Number:'), sg.Input(key='-ROLL-')],
              [sg.Button('Take Picture', size=(20, 2), pad=((540, 512), 1))],
              [sg.Image(filename='', key='-IMAGE-')]]
    window = sg.Window('Add Student', layout, size=(1280,720))

    cap = cv2.VideoCapture(0)  # Start the webcam

    while True:
        event, values = window.read(timeout=20)
        if event == sg.WINDOW_CLOSED:
            break
        ret, frame = cap.read()
        height, width, _ = frame.shape
        size = min(height, width)
        top = (height - size) // 2
        left = (width - size) // 2
        square_frame = frame[top:top+size, left:left+size]
        resized_frame = cv2.resize(square_frame, (216, 216))
        rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)  # Convert color space from BGR to RGB
        imgbytes = cv2.imencode('.png', rgb_frame)[1].tobytes()  # Use rgb_frame here

        # Convert imgbytes back to an image and then to RGB
        nparr = np.frombuffer(imgbytes, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
        imgbytes_rgb = cv2.imencode('.png', img_rgb)[1].tobytes()

        window['-IMAGE-'].update(data=imgbytes_rgb)
        if event == 'Take Picture':
            img = Image.fromarray(rgb_frame)  # Use rgb_frame here
            img.save(f'Images/{values["-ROLL-"]}.png')

    window.close()
    cap.release()  # Release the webcam

def display_images(folder):
    layout = [[sg.Text('')],
              [sg.Listbox(values=[os.path.join(folder, f) for f in os.listdir(folder)], size=(20, 10), key='-FILE LIST-', enable_events=True), sg.Image(key='-IMAGE-')],
              [sg.Text(size=(40,1), key='-IMG NAME-')],
              [sg.Button('Back', pad=((550, 0), 1))],
              [sg.Text('')]]
    window = sg.Window('Image Viewer', layout, size=(1280,720))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Back':
            break
        if event == '-FILE LIST-':  # A file was chosen from the listbox
            try:
                filename = values['-FILE LIST-'][0]
                image = Image.open(filename)
                image.thumbnail((400, 400))
                bio = io.BytesIO()
                image.save(bio, format="PNG")
                window['-IMAGE-'].update(data=bio.getvalue())
                window['-IMG NAME-'].update('Roll No.: ' + os.path.basename(filename))
            except:
                pass
    window.close()

def display_csv(folder):
    layout = [[sg.Text('')],
              [sg.Listbox(values=[os.path.join(folder, f) for f in os.listdir(folder)], size=(20, 10), key='-FILE LIST-', enable_events=True), sg.Multiline(size=(60, 20), key='-CSV-')],
              [sg.Button('Back', pad=((550, 0), 1))],
              [sg.Text('')]]
    window = sg.Window('CSV Viewer', layout, size=(1280,720))

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Back':
            break
        if event == '-FILE LIST-':  # A file was chosen from the listbox
            try:
                filename = values['-FILE LIST-'][0]
                with open(filename, "r") as file_in:
                    reader = csv.reader(file_in)
                    csv_contents = "\n".join([",".join(row) for row in reader])
                    window['-CSV-'].update(csv_contents)
            except:
                pass
    window.close()

# Event loop
while True:
    event, values = window.read(timeout=20)
    # End program if user closes window
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break
    elif event == 'Mark Attendance':
        threading.Thread(target=run_script, args=('main.py',), daemon=True).start()
    elif event == 'Add Students':
        add_student()
    elif event == 'Added Students':
        display_images('Images')
    elif event == 'Proxy Check':
        folder = sg.popup_get_folder('Please select a folder', default_path='check')
        if folder is not None:
            display_images(folder)
    elif event == 'View Attendance':
        display_csv('attendance')
    elif event == 'Update System':
        threading.Thread(target=run_script, args=('encoding_generator.py',), daemon=True).start()
    elif event == 'Update Database':
        layout = [[sg.Text('Enter student ID:'), sg.Input(key='-ID-')],
                [sg.Text('Enter student Name:'), sg.Input(key='-NAME-')],
                [sg.Text('Enter student Roll No:'), sg.Input(key='-ROLL-')],
                [sg.Text('Enter student Department:'), sg.Input(key='-DEPT-')],
                [sg.Text('Enter student Batch:'), sg.Input(key='-BATCH-')],
                [sg.Text('Enter student Total Attendance:'), sg.Input(key='-TOTAL-')],
                [sg.Text('Last Attendance:'), sg.Input(default_text=datetime.now().strftime('%Y-%m-%d %H:%M:%S'), key='-LAST-', disabled=True)],
                [sg.Button('Submit', bind_return_key=True)]]

        window2 = sg.Window('Update Database', layout)

        while True:
            event2, values2 = window2.read()
            if event2 == sg.WINDOW_CLOSED or event2 == 'Exit':
                break
            if event2 == 'Submit':
                threading.Thread(target=update_database, args=(values2, output_queue), daemon=True).start()

    # Check if there is anything in the queue
    try:
        message = output_queue.get_nowait()
    except queue.Empty:  # The queue is empty
        pass
    else:  # There is something in the queue
        print(message)  # Replace this with code to update a text element in your PySimpleGUI window