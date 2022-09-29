import VirtualPainter as vp
import os
import PySimpleGUI as sg
from datetime import datetime
from session_sent import emailsender
from PIL import Image
import home as h
import slide

# using now() to get current time
background_layout = [sg.theme_text_color(), sg.theme_background_color(), [sg.Image(r'image1.png')]]
file_types = [("JPEG (*.jpg)", "*.jpg"),
              ("All files (*.*)", "*.*")]
font = ("Arial", 20)
font1 = ("Arial", 15)
column1 = []
layout = [[sg.Image("Airo_Board.png")],
          [sg.Text("-----------------------------------------------------------------------------", key='-text-',
                   font=font)],
          [sg.Text("                                             "), sg.Button("HOME", font=("Arial", 12)),
           sg.Button("ABOUT", font=("Arial", 12)), sg.Button("WORKS", font=("Arial", 12))],
          [sg.Text("-----------------------------------------------------------------------------", key='-text-',
                   font=font)],
          [sg.Text('User Name', key='-text-', font=font1), sg.InputText()],
          [sg.Text(size=(40, 1), key='-OUTPUT-')],
          [sg.Text('Password ', key='-text-', font=font1), sg.InputText()],
          [sg.Text('_' * 80)],
          [sg.Text('Choose An Image to insert', size=(40, 1))],
          [sg.Text('Your Folder', size=(15, 1), justification='right'), sg.InputText('Default Folder', key="-FILE-"),
           sg.FileBrowse(file_types=file_types), sg.Button("Load Image")],
          [sg.Text(
              "---------------------------------------------------------------------------------------------------------------------------         ")],
          [sg.Frame(layout=[
              [sg.CBox('Audio Recording', size=(10, 1)),
               sg.CBox('Video Recording', default=True)]
          ], title='Options For Recording', relief=sg.RELIEF_SUNKEN,
              tooltip='Use these to set flags'), sg.Col(column1)],
          [sg.Text(
              "---------------------------------------------------------------------------------------------------------------------------         ")],
          [sg.Button("Virtual Board", font=("Arial", 15)), sg.Button("Slide Show", font = ("Arial", 15))]
          ]
layout2 = [[sg.Text("                                      Thank you using Airoboard ")],

           [sg.Text(
               "---------------------------------------------------------------------------------------------------------------------------         ")],
           [sg.Text("                                         Send Your Drawing To Your Email")],
           [sg.Text(
               "---------------------------------------------------------------------------------------------------------------------------         ")],
           [sg.Text("Enter Your Email Address to send Screen time and Drawing")],
           [sg.Text('Email : '), sg.InputText()],
           [sg.Text(size=(40, 1), key='-OUTPUT-')],
           [sg.Button("Send Email")],
           [sg.Text(
               "---------------------------------------------------------------------------------------------------------------------------         ")],
           [sg.Text("                                            Send Your Feedback")],
           [sg.Text(
               "                                                                                                                                                                        ")],

           [sg.Multiline(size=(30, 5), key='textbox')],
           [sg.Text(
               "                                                                                                                                                                        ")],
           [sg.Button("Send Feedback")]
           ]

# Create the window
window = sg.Window("Virtual Paint", layout)
image = 0

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    print(event)
    if event == "HOME":
        print(values)
        h.layout3()

    elif event == sg.WIN_CLOSED:
        break
    if event == "Load Image":
        filename = values["-FILE-"]
        if os.path.exists(filename):
            image = Image.open(values["-FILE-"])
            image.thumbnail((400, 400))
            # bio = io.BytesIO()
            # image.save(bio, format="PNG")
            # window["-IMAGE-"].update(data=bio.getvalue())
    if event == "Virtual Board":
        print(values)
        if values[1]:
            if values[2] == "root":
                name = values[1]
                now = datetime.now()
                session_start_time = now.strftime('Date: %d/%Y/%m Time: %I:%M:%S')
                vp.airoboard(session_start_time, name, image)
                window.close()
                # window = sg.Window("Virtual Paint", layout)

            else:
                window['-OUTPUT-'].update("Wrong Password !", text_color='red')
        else:
            window['-OUTPUT-'].update("Please enter the User Name!", text_color='red')
        if values[3]:
            # rec_audios()
            pass
        if values[4]:
            pass
    elif event == sg.WIN_CLOSED:
        window = sg.Window("Experience", layout2)
    if event == "Send Email":
        if values[0]:
            emailsender("SS1.jpg")
    if event == "Slide Show":
        if values[1]:
            if values[2] == "root":
                name = values[1]
                now = datetime.now()
                session_start_time = now.strftime('Date: %d/%Y/%m Time: %I:%M:%S')
                slide.playslide()
                window.close()
                # window = sg.Window("Virtual Paint", layout)
            else:
                window['-OUTPUT-'].update("Wrong Password !", text_color='red')
        else:
            window['-OUTPUT-'].update("Please enter the User Name!", text_color='red')

window.close()
