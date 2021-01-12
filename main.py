from tkinter import *

# INITIALIZATIONS

expression = ""

main = Tk()
main.geometry('500x200')
main.title('Homebase v0.3')
main.resizable(False, False)

# FRAMES

homeFrame = Frame(main)
calcFrame = Frame(main)

# FUNCTIONS

def returnHome():
    calcFrame.pack_forget()
    homeFrame.pack()

def calcScr():
    homeFrame.pack_forget()
    calcFrame.pack()
    main.geometry('270x150')

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

infoText = Label(homeFrame, text='Homebase v0.3')
calcButton = Button(homeFrame, text='Calculator', command=calcScr)
infoText.pack()
calcButton.pack()

homeFrame.pack()

# CALC SCREEN

# Driver code
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