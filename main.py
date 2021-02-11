from tkinter import *
from tkinter import messagebox
import time

# INITIALIZATIONS


main = Tk()
main.geometry('270x150')
main.title('Homebase v0.4')
main.resizable(False, False)
main.geometry('270x150')
main.iconbitmap('homebase-logo.ico')

expression = ""
hour = StringVar()
minute = StringVar()
second = StringVar()
hour.set("00")
minute.set("00")
second.set("00")
pauseState = 0


# FRAMES


homeFrame = Frame(main)
calcFrame = Frame(main)
timerFrame = Frame(main)


# FUNCTIONS


def timerStop():
    global pauseState
    pauseState = 1


def timerPause():
    global pauseState
    if pauseState == 0:
        pauseState = 1
        print('one')
    elif pauseState == 1:
        pauseState = 0
        submit()
        print('zero')
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
            messagebox.showwarning('Time is up!', 'Time is up!')
        if pauseState == 0:
            temp -= 1
            timerFrame.update()
        if pauseState == 2:
            temp = 0


def toTimer():
    homeFrame.pack_forget()
    timerFrame.pack()


def returnHome():
    calcFrame.pack_forget()
    homeFrame.pack()
    timerFrame.pack_forget()


def calcScr():
    homeFrame.pack_forget()
    calcFrame.pack()


def press(num):
    global expression
    expression = expression + str(num)
    equation.set(expression)


def equalpress():
    try:
        global expression
        total = str(eval(expression))
        equation.set(total)
        expression = ""
    except:
        equation.set(" error ")
        expression = ""


def clear():
    global expression
    expression = ""
    equation.set("")


# HOME SCREEN


infoText = Label(homeFrame, text='Homebase v0.3', font=('Arial', 18, ''))
calcButton = Button(homeFrame, text='Calculator', command=calcScr)
timerButton = Button(homeFrame, text='Timer', command=toTimer)
infoText.grid(row=0, column=1, sticky=NSEW)
calcButton.grid(row=1, column=1, sticky=NSEW)
timerButton.grid(row=2, column=1, sticky=NSEW)

homeFrame.grid_columnconfigure(1, weight=1)
homeFrame.grid_rowconfigure(0, weight=1)
homeFrame.grid_rowconfigure(1, weight=1)
homeFrame.grid_rowconfigure(2, weight=1)

homeFrame.pack()

# TIMER SCREEN

hourText = Label(timerFrame, text='Hours')
hourText.grid(row=0, column=0, sticky=NSEW)
minuteText = Label(timerFrame, text='Minutes')
minuteText.grid(row=0, column=1, sticky=NSEW)
secondText = Label(timerFrame, text='Seconds')
secondText.grid(row=0, column=2, sticky=NSEW)
hourEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=hour)
hourEntry.grid(row=1, column=0, sticky=NSEW)
minuteEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=minute)
minuteEntry.grid(row=1, column=1, sticky=NSEW)
secondEntry = Entry(timerFrame, width=3, font=("Arial", 18, ""), textvariable=second)
secondEntry.grid(row=1, column=2, sticky=NSEW)
spacer1 = Label(timerFrame, text=" ")
spacer1.grid(row=2, column=1, sticky=NSEW)
timerPauseButton = Button(timerFrame, text='Pause/Unpause', command=timerPause)
timerPauseButton.grid(row=3, column=0, sticky=NSEW)
timerSubmit = Button(timerFrame, text='Start Timer', command=submit, bg='blue')
timerSubmit.grid(row=3, column=1, sticky=NSEW)
timerStopButton = Button(timerFrame, text='Stop', command=timerStop)
timerStopButton.grid(row=3, column=2, sticky=NSEW)
toHome = Button(timerFrame, text='Home', command=returnHome, bg='green')
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


if __name__ == "__main__":
    equation = StringVar()
    expression_field = Entry(calcFrame, textvariable=equation)
    expression_field.grid(columnspan=4, ipadx=70)
    equation.set('enter your expression')
    button1 = Button(calcFrame, text=' 1 ',
                     command=lambda: press(1), height=1, width=7)
    button1.grid(row=2, column=0)
    button2 = Button(calcFrame, text=' 2 ',
                     command=lambda: press(2), height=1, width=7)
    button2.grid(row=2, column=1)
    button3 = Button(calcFrame, text=' 3 ',
                     command=lambda: press(3), height=1, width=7)
    button3.grid(row=2, column=2)
    button4 = Button(calcFrame, text=' 4 ',
                     command=lambda: press(4), height=1, width=7)
    button4.grid(row=3, column=0)
    button5 = Button(calcFrame, text=' 5 ',
                     command=lambda: press(5), height=1, width=7)
    button5.grid(row=3, column=1)
    button6 = Button(calcFrame, text=' 6 ',
                     command=lambda: press(6), height=1, width=7)
    button6.grid(row=3, column=2)
    button7 = Button(calcFrame, text=' 7 ',
                     command=lambda: press(7), height=1, width=7)
    button7.grid(row=4, column=0)
    button8 = Button(calcFrame, text=' 8 ',
                     command=lambda: press(8), height=1, width=7)
    button8.grid(row=4, column=1)
    button9 = Button(calcFrame, text=' 9 ',
                     command=lambda: press(9), height=1, width=7)
    button9.grid(row=4, column=2)
    button0 = Button(calcFrame, text=' 0 ',
                     command=lambda: press(0), height=1, width=7)
    button0.grid(row=5, column=0)
    plus = Button(calcFrame, text=' + ',
                  command=lambda: press("+"), height=1, width=7)
    plus.grid(row=2, column=3)
    minus = Button(calcFrame, text=' - ',
                   command=lambda: press("-"), height=1, width=7)
    minus.grid(row=3, column=3)
    multiply = Button(calcFrame, text=' × ',
                      command=lambda: press("×"), height=1, width=7)
    multiply.grid(row=4, column=3)
    divide = Button(calcFrame, text=' ÷ ',
                    command=lambda: press("÷"), height=1, width=7)
    divide.grid(row=5, column=3)
    equal = Button(calcFrame, text=' = ',
                   command=equalpress, height=1, width=7)
    equal.grid(row=5, column=2)
    clear = Button(calcFrame, text='Clear',
                   command=clear, height=1, width=7)
    clear.grid(row=5, column='1')
    Decimal = Button(calcFrame, text='.',
                     command=lambda: press('.'), height=1, width=7)
    Decimal.grid(row=6, column=0)
    Home = Button(calcFrame, text='Home', bg='green',
                  command=returnHome, height=1, width=7)
    Home.grid(row=6, column=3)

main.mainloop()
