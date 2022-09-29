import PySimpleGUI as sg


def layout3():
    layout = [[sg.Image("home.png")]]
    window = sg.Window("Home", layout)
    while True:
        event, values = window.read()
        if event in (None, 'Exit'):
            break
        elif event == sg.WIN_CLOSED:
            break
    window.close()
