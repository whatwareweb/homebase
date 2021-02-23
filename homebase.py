from tkinter import *
from tkinter import messagebox
import time
from playsound import playsound
from threading import Thread
import json

# INITIALIZATIONS


main = Tk()
main.geometry('270x150')
main.title('Homebase v0.4')
main.resizable(False, False)
main.geometry('270x150')
main.iconbitmap('homebase-logo.ico')

expression = ''
expressionText = ''
hour = StringVar()
minute = StringVar()
second = StringVar()
hour.set('00')
minute.set('00')
second.set('00')
pauseState = 0
equation = StringVar()
currentFrame = 'home'
with open("settings.json", "r") as a:
    settings = json.load(a)
if settings['theme'] == 'dark':
    themefg = 'gray'
    themebg = 'black'
else:
    themefg = 'black'
    themebg = 'white'
main.configure(bg=themebg)
themeVar = IntVar()


# FRAMES


homeFrame = Frame(main)
calcFrame = Frame(main)
timerFrame = Frame(main)
settingsFrame = Frame(main)
homeFrame.configure(bg=themebg)
calcFrame.configure(bg=themebg)
timerFrame.configure(bg=themebg)
settingsFrame.configure(bg=themebg)


# FUNCTIONS


def themeSel():
    print(f'function called with var {themeVar.get()}')
    if themeVar.get() == 0:
        print('dark selected')
        settings['theme'] = 'dark'
    elif themeVar.get() == 1:
        print('light selected')
        settings['theme'] = 'light'
    with open('settings.json', 'w') as b:
        json.dump(settings, b)
    global themefg
    global themebg
    if settings['theme'] == 'dark':
        themefg = 'gray'
        themebg = 'black'
    else:
        themefg = 'black'
        themebg = 'white'
    buttondefinitions()
    main.update()
    homeFrame.pack_forget()
    main.configure(bg=themebg)
    settingsFrame.configure(bg=themebg)
    homeFrame.configure(bg=themebg)
    calcFrame.configure(bg=themebg)
    timerFrame.configure(bg=themebg)


def toSettings():
    homeFrame.pack_forget()
    settingsFrame.pack()


def timersound():
    playsound(settings['customalarm'])


def timermsg():
    messagebox.showwarning('Time is up!', 'Time is up!')


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
        if event.char == '\r':
            submit()


def calcBack():
    global expression
    global expressionText
    mod_string = expression[:int(len(expression)) - 1]
    modStringTwo = expressionText[:int(len(expressionText)) - 1]
    expression = mod_string
    expressionText = modStringTwo
    equation.set(expressionText)


def timerStop():
    global pauseState
    pauseState = 1


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
    global pauseState
    if pauseState == 1:
        pauseState = 0
    try:
        temp = int(hour.get()) * 3600 + int(minute.get()) * 60 + int(second.get())
    except:
        return
    while temp > -1 and pauseState == 0:
        mins, secs = divmod(temp, 60)
        hours = 0
        if mins > 60:
            hours, mins = divmod(mins, 60)
        hour.set("{0:2d}".format(hours))
        minute.set("{0:2d}".format(mins))
        second.set("{0:2d}".format(secs))
        timerFrame.update()
        time.sleep(1)
        if temp == 0 and pauseState == 0:
            a = Thread(target=timersound)
            b = Thread(target=timermsg)
            a.start()
            b.start()
        if pauseState == 0:
            temp -= 1
            timerFrame.update()
        if pauseState == 2:
            temp = 0


def toTimer():
    global currentFrame
    currentFrame = 'timer'
    homeFrame.pack_forget()
    timerFrame.pack()


def returnHome():
    global currentFrame
    currentFrame = 'home'
    calcFrame.pack_forget()
    homeFrame.pack()
    timerFrame.pack_forget()
    settingsFrame.pack_forget()


def calcScr():
    global currentFrame
    currentFrame = 'calculator'
    homeFrame.pack_forget()
    calcFrame.pack()


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

def buttondefinitions():
    # HOME SCREEN

    infoText = Label(homeFrame, text='Homebase v0.4', font=('Arial', 18, ''), bg=themebg, fg=themefg)
    calcButton = Button(homeFrame, text='Calculator', command=calcScr, bg=themebg, fg=themefg)
    timerButton = Button(homeFrame, text='Timer', command=toTimer, bg=themebg, fg=themefg)
    settingsButton = Button(homeFrame, text='Settings', command=toSettings, bg=themebg, fg=themefg)
    infoText.grid(row=0, column=1, sticky=NSEW)
    calcButton.grid(row=1, column=1, sticky=NSEW)
    timerButton.grid(row=2, column=1, sticky=NSEW)
    settingsButton.grid(row=3, column=1, sticky=NSEW)

    homeFrame.grid_columnconfigure(1, weight=1)
    homeFrame.grid_rowconfigure(0, weight=1)
    homeFrame.grid_rowconfigure(1, weight=1)
    homeFrame.grid_rowconfigure(2, weight=1)

    homeFrame.pack()

    # TIMER SCREEN

    hourText = Label(timerFrame, text='Hours', bg=themebg, fg=themefg)
    hourText.grid(row=0, column=0, sticky=NSEW)
    minuteText = Label(timerFrame, text='Minutes', bg=themebg, fg=themefg)
    minuteText.grid(row=0, column=1, sticky=NSEW)
    secondText = Label(timerFrame, text='Seconds', bg=themebg, fg=themefg)
    secondText.grid(row=0, column=2, sticky=NSEW)
    hourEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=hour, bg=themebg, fg=themefg)
    hourEntry.grid(row=1, column=0, sticky=NSEW)
    minuteEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=minute, bg=themebg, fg=themefg)
    minuteEntry.grid(row=1, column=1, sticky=NSEW)
    secondEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=second, bg=themebg, fg=themefg)
    secondEntry.grid(row=1, column=2, sticky=NSEW)
    spacer1 = Label(timerFrame, text=" ", bg=themebg, fg=themefg)
    spacer1.grid(row=2, column=1, sticky=NSEW)
    timerPauseButton = Button(timerFrame, text='Pause', command=timerPause, bg=themebg, fg=themefg)
    timerPauseButton.grid(row=3, column=0, sticky=NSEW)
    timerSubmit = Button(timerFrame, text='Start Timer', command=submit, bg='blue', fg=themefg)
    timerSubmit.grid(row=3, column=1, sticky=NSEW)
    timerStopButton = Button(timerFrame, text='Stop', command=timerStop, bg=themebg, fg=themefg)
    timerStopButton.grid(row=3, column=2, sticky=NSEW)
    toHome = Button(timerFrame, text='Home', command=returnHome, bg='green', fg=themefg)
    toHome.grid(row=4, column=1, sticky=NSEW)
    timerFrame.grid_columnconfigure(0, weight=1)
    timerFrame.grid_columnconfigure(1, weight=1)
    timerFrame.grid_columnconfigure(2, weight=1)
    timerFrame.grid_rowconfigure(0, weight=1)
    timerFrame.grid_rowconfigure(1, weight=1)
    timerFrame.grid_rowconfigure(2, weight=1)
    timerFrame.grid_rowconfigure(3, weight=1)
    timerFrame.grid_rowconfigure(4, weight=1)

    # CALC SCREEN

    expression_field = Entry(calcFrame, textvariable=equation, bg=themebg, fg=themefg)
    expression_field.grid(columnspan=4, ipadx=70)
    equation.set('Enter your equation!')
    button1 = Button(calcFrame, text=' 1 ', command=lambda: press(1), height=1, width=7, bg=themebg, fg=themefg)
    button1.grid(row=2, column=0)
    button2 = Button(calcFrame, text=' 2 ', command=lambda: press(2), height=1, width=7, bg=themebg, fg=themefg)
    button2.grid(row=2, column=1)
    button3 = Button(calcFrame, text=' 3 ', command=lambda: press(3), height=1, width=7, bg=themebg, fg=themefg)
    button3.grid(row=2, column=2)
    button4 = Button(calcFrame, text=' 4 ', command=lambda: press(4), height=1, width=7, bg=themebg, fg=themefg)
    button4.grid(row=3, column=0)
    button5 = Button(calcFrame, text=' 5 ', command=lambda: press(5), height=1, width=7, bg=themebg, fg=themefg)
    button5.grid(row=3, column=1)
    button6 = Button(calcFrame, text=' 6 ', command=lambda: press(6), height=1, width=7, bg=themebg, fg=themefg)
    button6.grid(row=3, column=2)
    button7 = Button(calcFrame, text=' 7 ', command=lambda: press(7), height=1, width=7, bg=themebg, fg=themefg)
    button7.grid(row=4, column=0)
    button8 = Button(calcFrame, text=' 8 ', command=lambda: press(8), height=1, width=7, bg=themebg, fg=themefg)
    button8.grid(row=4, column=1)
    button9 = Button(calcFrame, text=' 9 ', command=lambda: press(9), height=1, width=7, bg=themebg, fg=themefg)
    button9.grid(row=4, column=2)
    button0 = Button(calcFrame, text=' 0 ', command=lambda: press(0), height=1, width=7, bg=themebg, fg=themefg)
    button0.grid(row=5, column=0)
    plus = Button(calcFrame, text=' + ', command=lambda: press("+"), height=1, width=7, bg=themebg, fg=themefg)
    plus.grid(row=2, column=3)
    minus = Button(calcFrame, text=' - ', command=lambda: press("-"), height=1, width=7, bg=themebg, fg=themefg)
    minus.grid(row=3, column=3)
    multiply = Button(calcFrame, text=' × ', command=lambda: press("*"), height=1, width=7, bg=themebg, fg=themefg)
    multiply.grid(row=4, column=3)
    divide = Button(calcFrame, text=' ÷ ', command=lambda: press("/"), height=1, width=7, bg=themebg, fg=themefg)
    divide.grid(row=5, column=3)
    equal = Button(calcFrame, text=' = ', command=equalpress, height=1, width=7, bg=themebg, fg=themefg)
    equal.grid(row=5, column=2)
    clear = Button(calcFrame, text='Clear', command=calcclear, height=1, width=7, bg=themebg, fg=themefg)
    clear.grid(row=5, column='1')
    Decimal = Button(calcFrame, text='.', command=lambda: press('.'), height=1, width=7, bg=themebg, fg=themefg)
    Decimal.grid(row=6, column=0)
    Home = Button(calcFrame, text='Home', bg='green', command=returnHome, height=1, width=7, fg=themefg)
    Home.grid(row=6, column=3)
    main.bind("<KeyPress>", keyPressed)

    # SETTINGS SCREEN

    darkRadio = Radiobutton(settingsFrame, text='Dark mode', variable=themeVar, command=themeSel,
                            value=0, bg=themebg, fg=themefg)
    lightRadio = Radiobutton(settingsFrame, text='Light mode', variable=themeVar, command=themeSel,
                             value=1, bg=themebg, fg=themefg)
    homeButton = Button(settingsFrame, text='Home', command=returnHome, bg='green')
    darkRadio.grid(row=0, column=0)
    lightRadio.grid(row=1, column=0)
    homeButton.grid(row=2, column=0)

buttondefinitions()

main.mainloop()
