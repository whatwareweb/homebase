from tkinter import *
import time
from threading import Thread
from threading import Timer
import json
import subprocess
from appdirs import *
import os
import platform
from pydub import AudioSegment
from pydub.playback import play
from plyer import notification
from plyer import filechooser
import base64
from pystray import MenuItem as Item
import pystray
from PIL import Image

# INITIALIZATIONS

hb_version = "1.1-dev3"
main = Tk()
main.title('Homebase')
main.resizable(False, False)
main.geometry('270x152')
if platform.system().lower() == "windows":
    main.iconbitmap('logo.ico')
else:
    with open('logo.gif', 'rb') as icon_gif:
        _icon_base64 = base64.b64encode(icon_gif.read())
    main.iconbitmap(_icon_base64)

expression = ''
expressionText = ''
hour = StringVar()
minute = StringVar()
second = StringVar()
pauseState = 0
stopState = False
equation = StringVar()
pingaddr = StringVar()
mttVar = IntVar()
alarmEntryText = StringVar()
currentFrame = 'home'
temp = 0

pathsep = '\\' if platform.system().lower() == 'windows' else '/'


def settingsWrite():
    with open(f"{user_data_dir('Homebase', 'WhatWare')}{pathsep}settings.json", "w") as b:
        json.dump(settings, b)


try:
    with open(f"{user_data_dir('Homebase', 'WhatWare')}{pathsep}settings.json", "r") as a:
        data = a.read()
    if data != "":
        settings = json.loads(data)
    else:
        settings = {"version": hb_version, "theme": "dark", "customalarm": "alarm.wav", "minimizetotray": True}
        with open(f"{user_data_dir('Homebase', 'WhatWare')}{pathsep}settings.json", "w") as a:
            a.write(json.dumps(settings))
except:
    os.makedirs(user_data_dir('Homebase', 'WhatWare'))
    settings = {"version": hb_version, "theme": "dark", "customalarm": "alarm.wav", "minimizetotray": True}
    with open(f"{user_data_dir('Homebase', 'WhatWare')}{pathsep}settings.json", "w") as a:
        a.write(json.dumps(settings))

settings['version'] = hb_version
if settings['theme'] is None:
    settings['theme'] = 'dark'
if settings['customalarm'] is None:
    settings['customalarm'] = 'alarm.wav'
if settings['minimizetotray'] is None:
    settings['minimizetotray'] = True
settingsWrite()

alarmEntryText.set(settings['customalarm'])


def quit_window(icon):
    icon.stop()
    main.destroy()


def show_window(icon):
    icon.stop()
    main.after(0, main.deiconify)


def hide_window():
    main.withdraw()
    image = Image.open("logo.gif")
    menu = (Item('Quit', quit_window), Item('Show', show_window),
            Item(text='Default', action=show_window, visible=False, default=True, enabled=True))
    icon = pystray.Icon("name", image, "homebase", menu)
    icon.run()


if settings["minimizetotray"] == True:
    main.protocol("WM_DELETE_WINDOW", hide_window)

else:
    main.protocol("WM_DELETE_WINDOW", main.destroy)

if settings['theme'] == 'dark':
    themefg = 'gray'
    themebg = 'black'
else:
    themefg = 'black'
    themebg = 'white'
main.configure(bg=themebg)
themeVar = IntVar()

# FRAMES


homeFrame = Frame(main, bg=themebg)
calcFrame = Frame(main, bg=themebg)
timerFrame = Frame(main, bg=themebg)
settingsFrame = Frame(main, bg=themebg)
pingFrame = Frame(main, bg=themebg)


# FUNCTIONS


def setAlarm():
    settings['customalarm'] = alarmEntryText.get()
    settingsWrite()

def chooseAlarm():
    try:
        alarmEntryText.set(filechooser.open_file()[0])
    except IndexError:
        return
    settings['customalarm'] = str(alarmEntryText.get())
    settingsWrite()


def mtt():
    if mttVar.get() == 0:
        settings["minimizetotray"] = False
        main.protocol("WM_DELETE_WINDOW", main.destroy)
    else:
        settings["minimizetotray"] = True
        main.protocol("WM_DELETE_WINDOW", hide_window)
    settingsWrite()


def ping():
    try:
        host = pingaddr.get()
        param = '-n' if platform.system().lower() == 'windows' else '-c'
        command = ['ping', param, '1', host]
        pingaddr.set(subprocess.call(command) == 0)
    except:
        pingaddr.set('Error!')
        return
    if pingaddr.get() == '0':
        pingaddr.set('Error!')
    else:
        pingaddr.set(f'{host} is up')


def topinger():
    homeFrame.place_forget()
    pingFrame.place(width=270, height=152)


def themeSel():
    if themeVar.get() == 0:
        settings['theme'] = 'dark'
    elif themeVar.get() == 1:
        settings['theme'] = 'light'
    with open(f"{user_data_dir('Homebase', 'WhatWare')}{pathsep}settings.json", "w") as b:
        json.dump(settings, b)
    global themefg
    global themebg
    if settings['theme'] == 'dark':
        themefg = 'gray'
        themebg = 'black'
    else:
        themefg = 'black'
        themebg = 'white'
    gui()
    main.update()
    homeFrame.place_forget()
    main.configure(bg=themebg)
    settingsFrame.configure(bg=themebg)
    homeFrame.configure(bg=themebg)
    calcFrame.configure(bg=themebg)
    timerFrame.configure(bg=themebg)
    pingFrame.configure(bg=themebg)


def toSettings():
    homeFrame.place_forget()
    settingsFrame.pack()


def keyPressed(event):
    char_list = ['/', '*', '-', '+', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    if currentFrame == 'calculator':
        if event.char in char_list:
            press(event.char)
        elif event.char == '=' or event.char == '\r':
            equalpress()
        elif event.char == '\x08':
            calcBack()
        elif event.keycode == 46:
            calcclear()
    if currentFrame == 'timer':
        if event.char == '\r' or event.char == '=':
            submit()


def calcBack():
    global expression
    global expressionText
    mod_string = expression[:int(len(expression)) - 1]
    modStringTwo = expressionText[:int(len(expressionText)) - 1]
    expression = mod_string
    expressionText = modStringTwo
    equation.set(expressionText)


def timerPause():
    global pauseState
    global timerPauseButton
    if pauseState == 0:
        pauseState = 1
        timerPauseButton['text'] = 'Unpause'
    elif pauseState == 1:
        pauseState = 0
        timerPauseButton['text'] = 'Pause'
        submit()
    timerPauseButton.update()
    timerFrame.update()


def submit():
    global stopState
    global pauseState
    if hour.get() == '':
        hour.set('0')
    if minute.get() == '':
        minute.set('0')
    if second.get() == '':
        second.set('0')
    if stopState:
        print('Stopping timer')
        pauseState = 1
        hour.set('')
        minute.set('')
        second.set('')
        timerSubmit['text'] = 'Start'
        timerSubmit['bg'] = 'blue'
        stopState = False
    elif not stopState:
        print('Starting timer')
        timerSubmit['text'] = 'Stop'
        timerSubmit['bg'] = 'red'
        stopState = True
        global temp
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
        if pauseState == 1:
            pauseState = 0
        timerloop()


def timerloop():
    global pauseState
    global temp

    if temp > -1 and pauseState == 0:
        mins, secs = divmod(temp, 60)
        hours = 0
        if mins > 60:
            hours, mins = divmod(mins, 60)
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        time.sleep(1)
        if temp == 0 and pauseState == 0:
            submit()
            notification.notify(
                title="Homebase",
                app_icon="logo.ico" if platform.system().lower() == 'windows' else 'logo.gif',
                message="Time is up.",
                timeout=10
            )
            sound = AudioSegment.from_file(str(alarmEntryText.get()))
            play(sound)
            pauseState = None
        else:
            Timer(1, timerloop).start()
        if pauseState == 0:
            temp -= 1


def toTimer():
    global currentFrame
    currentFrame = 'timer'
    homeFrame.place_forget()
    timerFrame.place(width=270, height=152)


def returnHome():
    global currentFrame
    currentFrame = 'home'
    homeFrame.place(width=270, height=152)
    calcFrame.place_forget()
    timerFrame.place_forget()
    settingsFrame.pack_forget()
    pingFrame.place_forget()
    if str(alarmEntryText.get()) != str(settings['customalarm']):
        settings['customalarm'] = alarmEntryText.get()


def calcScr():
    global currentFrame
    currentFrame = 'calculator'
    homeFrame.place_forget()
    calcFrame.place(width=270, height=152)


def press(num):
    global expression
    global expressionText
    expression = f'{expression}{str(num)}'
    if num == '/':
        expressionText = f'{expressionText}÷'
    elif num == '*':
        expressionText = f'{expressionText}×'
    else:
        expressionText = f'{expressionText}{str(num)}'
    equation.set(expressionText)


def equalpress():
    try:
        global expression
        global expressionText
        total = str(eval(expression))
        equation.set(total)
        expression = ''
        expressionText = ''
    except:
        equation.set(' error ')
        expression = ''
        expressionText = ''


def calcclear():
    global expression
    global expressionText
    expression = ""
    equation.set("")
    expressionText = ""


class gui():
    global timerPauseButton
    global timerSubmit

    # HOME SCREEN

    infoText = Label(homeFrame, text='Homebase', font=('Arial', 18, ''), bg=themebg, fg=themefg)
    calcButton = Button(homeFrame, text='Calculator', command=calcScr, bg=themebg, fg=themefg)
    timerButton = Button(homeFrame, text='Timer', command=toTimer, bg=themebg, fg=themefg)
    settingsButton = Button(homeFrame, text='Settings', command=toSettings, bg=themebg, fg=themefg)
    pingButton = Button(homeFrame, text='Pinger', command=topinger, bg=themebg, fg=themefg)
    quitbutton = Button(homeFrame, text='Quit', command=main.destroy, bg='red')
    infoText.place(x=75, y=0, width=120, height=20)
    calcButton.place(x=15, y=30, width=120, height=30)
    timerButton.place(x=15, y=60, width=120, height=30)
    pingButton.place(x=135, y=30, width=120, height=30)
    settingsButton.place(x=135, y=60, width=120, height=30)
    quitbutton.place(x=230, y=122, width=40, height=30)

    homeFrame.place(width=270, height=152)

    # PING SCREEN

    pingText = Label(pingFrame, text='Pinger', bg=themebg, fg=themefg)
    pingEntry = Entry(pingFrame, textvariable=pingaddr, bg=themebg, fg=themefg)
    pingbutton = Button(pingFrame, text='Ping', command=lambda: Thread(target=ping).start(), bg=themebg, fg=themefg)
    homebutton = Button(pingFrame, text='Home', command=returnHome, bg='green')
    # pingText.grid(row=0, column=0)
    # pingEntry.grid(row=1, column=0)
    # pingbutton.grid(row=1, column=1)
    # homebutton.grid(row=2, column=0)
    pingText.place(x=75, y=0, width=120, height=30)
    pingEntry.place(x=75, y=30, width=120, height=20)
    pingbutton.place(x=196, y=30, width=30, height=20)
    homebutton.place(x=110, y=60, width=50, height=30)

    # TIMER SCREEN

    hourText = Label(timerFrame, text='Hours', bg=themebg, fg=themefg)
    minuteText = Label(timerFrame, text='Minutes', bg=themebg, fg=themefg)
    secondText = Label(timerFrame, text='Seconds', bg=themebg, fg=themefg)
    hourEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=hour, bg=themebg, fg=themefg,
                      insertbackground=themefg)
    minuteEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=minute, bg=themebg, fg=themefg,
                        insertbackground=themefg)
    secondEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=second, bg=themebg, fg=themefg,
                        insertbackground=themefg)
    timerPauseButton = Button(timerFrame, text='Pause', command=timerPause, bg=themebg, fg=themefg)
    timerSubmit = Button(timerFrame, text='Start', command=submit, bg='blue')
    toHome = Button(timerFrame, text='Home', command=returnHome, bg='green')
    hourText.place(x=65, y=0, width=50, height=20)
    minuteText.place(x=110, y=0, width=50, height=20)
    secondText.place(x=160, y=0, width=50, height=20)
    hourEntry.place(x=65, y=25, width=50, height=40)
    minuteEntry.place(x=110, y=25, width=50, height=40)
    secondEntry.place(x=160, y=25, width=50, height=40)
    timerSubmit.place(x=135, y=65, width=75, height=30)
    timerPauseButton.place(x=65, y=65, width=75, height=30)
    toHome.place(x=110, y=95, width=50, height=30)

    # CALC SCREEN

    expression_field = Entry(calcFrame, textvariable=equation, bg=themebg, fg=themefg)
    expression_field.place(x=0, y=0, width=270, height=22.5)
    button1 = Button(calcFrame, text=' 1 ', command=lambda: press(1), height=1, width=7, bg=themebg, fg=themefg)
    # button1.grid(row=2, column=0)
    button1.place(x=0, y=22)
    button2 = Button(calcFrame, text=' 2 ', command=lambda: press(2), height=1, width=7, bg=themebg, fg=themefg)
    # button2.grid(row=2, column=1)
    button2.place(x=70, y=22)
    button3 = Button(calcFrame, text=' 3 ', command=lambda: press(3), height=1, width=7, bg=themebg, fg=themefg)
    # button3.grid(row=2, column=2)
    button3.place(x=140, y=22)
    button4 = Button(calcFrame, text=' 4 ', command=lambda: press(4), height=1, width=7, bg=themebg, fg=themefg)
    # button4.grid(row=3, column=0)
    button4.place(x=0, y=48)
    button5 = Button(calcFrame, text=' 5 ', command=lambda: press(5), height=1, width=7, bg=themebg, fg=themefg)
    # button5.grid(row=3, column=1)
    button5.place(x=70, y=48)
    button6 = Button(calcFrame, text=' 6 ', command=lambda: press(6), height=1, width=7, bg=themebg, fg=themefg)
    # button6.grid(row=3, column=2)
    button6.place(x=140, y=48)
    button7 = Button(calcFrame, text=' 7 ', command=lambda: press(7), height=1, width=7, bg=themebg, fg=themefg)
    # button7.grid(row=4, column=0)
    button7.place(x=0, y=74)
    button8 = Button(calcFrame, text=' 8 ', command=lambda: press(8), height=1, width=7, bg=themebg, fg=themefg)
    # button8.grid(row=4, column=1)
    button8.place(x=70, y=74)
    button9 = Button(calcFrame, text=' 9 ', command=lambda: press(9), height=1, width=7, bg=themebg, fg=themefg)
    # button9.grid(row=4, column=2)
    button9.place(x=140, y=74)
    button0 = Button(calcFrame, text=' 0 ', command=lambda: press(0), height=1, width=7, bg=themebg, fg=themefg)
    # button0.grid(row=5, column=0)
    button0.place(x=0, y=100)
    plus = Button(calcFrame, text=' + ', command=lambda: press("+"), height=1, width=7, bg=themebg, fg=themefg)
    # plus.grid(row=2, column=3)
    plus.place(x=211, y=22)
    minus = Button(calcFrame, text=' - ', command=lambda: press("-"), height=1, width=7, bg=themebg, fg=themefg)
    # minus.grid(row=3, column=3)
    minus.place(x=211, y=48)
    multiply = Button(calcFrame, text=' × ', command=lambda: press("*"), height=1, width=7, bg=themebg, fg=themefg)
    # multiply.grid(row=4, column=3)
    multiply.place(x=211, y=74)
    divide = Button(calcFrame, text=' ÷ ', command=lambda: press("/"), height=1, width=7, bg=themebg, fg=themefg)
    # divide.grid(row=5, column=3)
    divide.place(x=211, y=100)
    equal = Button(calcFrame, text=' = ', command=equalpress, height=1, width=7, bg=themebg, fg=themefg)
    # equal.grid(row=5, column=2)
    equal.place(x=140, y=100)
    clear = Button(calcFrame, text='Clear', command=calcclear, height=1, width=7, bg=themebg, fg=themefg)
    # clear.grid(row=5, column='1')
    clear.place(x=70, y=100)
    Decimal = Button(calcFrame, text='.', command=lambda: press('.'), height=1, width=7, bg=themebg, fg=themefg)
    # Decimal.grid(row=6, column=0)
    Decimal.place(x=211, y=126)
    Home = Button(calcFrame, text='Home', bg='green', command=returnHome, height=1, width=7)
    Home.place(x=0, y=126)
    main.bind("<KeyPress>", keyPressed)

    # SETTINGS SCREEN

    if settings['theme'] == 'dark':
        themeVar.set('0')
    elif settings['theme'] == 'light':
        themeVar.set(1)
    if not settings['minimizetotray']:
        mttVar.set('0')
    elif settings['minimizetotray']:
        mttVar.set('1')

    darkRadio = Radiobutton(settingsFrame,
                            text='Dark mode' if platform.system().lower() != 'darwin' else 'Dark mode (LOOKS BAD ON MACOS)',
                            variable=themeVar, command=themeSel, value=0, bg=themebg,
                            fg=themefg)
    lightRadio = Radiobutton(settingsFrame, text='Light mode', variable=themeVar, command=themeSel, value=1,
                             bg=themebg, fg=themefg)
    mttCheckbox = Checkbutton(settingsFrame, text="Minimize to tray", variable=mttVar, onvalue=1, offvalue=0,
                              command=mtt, bg=themebg, fg=themefg)
    alarmPathLabel = Label(settingsFrame, text='Alarm file:', fg=themefg, bg=themebg)
    alarmPathEntry = Entry(settingsFrame, textvariable=alarmEntryText, bg=themebg, fg=themefg)
    alarmPathSelButton = Button(settingsFrame, text='📁', command=chooseAlarm, bg=themebg, fg=themefg)
    alarmPathCheck = Button(settingsFrame, text='✓', command=setAlarm)
    homeButton = Button(settingsFrame, text='Home', command=returnHome, bg='green')
    versionNum = Label(settingsFrame, text=f"Version: {hb_version}", fg=themefg, bg=themebg)
    darkRadio.grid(row=0, column=1)
    lightRadio.grid(row=1, column=1)
    mttCheckbox.grid(row=2, column=1)
    alarmPathLabel.grid(row=3, column=1)
    alarmPathEntry.grid(row=4, column=1)
    alarmPathSelButton.grid(row=4, column=0)
    alarmPathCheck.grid(row=4, column=2)
    homeButton.grid(row=5, column=1)
    versionNum.grid(row=6, column=1)


main.mainloop()
