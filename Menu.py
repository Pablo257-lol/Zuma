from tkinter import *
from tkinter import ttk
from tkinter import font


pack1 = False
pack2 = False

def button():
    # Кнопка которая выполняет команду farther
    btn_1 = ttk.Button(frame, text='Продолжить игру', command=data)
    btn_1.place(x= 1000, rely=0.25, height=100, width=500)

    # Кнопка выхода
    btn_2 = ttk.Button(frame, text= "Выход", command=lambda :win.destroy())
    btn_2.place(x= 1000, rely=0.65, height=100, width=500)

    # Пустая кнопка(в будущем будет открываться другое окной)
    btn_3 = ttk.Button(frame, text= "Пустая кнопка")
    btn_3.place(x= 1000, rely=0.45, height=100, width=500)

def data():
    global pack1
    if pack1:
        frame1_2.pack_forget()

        frame.pack()
        pack1 = False
    else:
        frame.pack_forget()

        frame1_2.pack(fill=BOTH, expand=True)
        win2_logo = Label(frame1_2, image=map_bg)
        win2_logo.pack()
        entry = Entry(frame1_2)
        entry.place(relx=0.5, rely=0.5, anchor=CENTER)
        btn1_1 = ttk.Button(frame1_2, text= "Продолжить", command=save_text)
        btn1_1.place(x = 910, rely=0.52, height=25, width=100)
        pack1 = True

def save_text():
    text = entry.get()
    with open("text.txt", "w") as file:
        file.write(text)
    print(entry.get())

# Переход с frame на frame2
def farther():
    global pack2
    if pack2:
        frame2.pack_forget()

        frame.pack(fill=BOTH, expand=True)
        bg_logo.pack()
        button()
        pack2 = False

    else:
        frame.pack_forget()

        frame2.pack(fill=BOTH, expand=True)
        map_logo = Label(frame2, image=map_bg)
        map_logo.pack()
        button2 = ttk.Button(frame2, text="Назад", command=farther)
        button2.place(x=500, y=50)
        pack2 = True

win = Tk()

win.title('Zuzu главный') # Name window
win.attributes('-fullscreen', True) # fullscreen

# Frame
frame = Frame(win)
frame.pack(fill=BOTH, expand=True)

# frame 1.2
frame1_2 = Frame(win)
frame.pack(fill=BOTH, expand=True)

# frame2
frame2 = Frame(win)
frame2.pack(fill=BOTH, expand=True)

# Icon
duck = PhotoImage(file="duck.png")
win.iconphoto(False,duck)

# Image
win_bg = PhotoImage(file="background_1.png")
map_bg = PhotoImage(file="Map_1.png")

# background
bg_logo = Label(frame, image=win_bg)
bg_logo.pack()

entry = Entry(frame1_2)
entry.place(relx=0.5, rely=0.5, anchor=CENTER)

# Создание кнопок
button()


win.mainloop() # End
