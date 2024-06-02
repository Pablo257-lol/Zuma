from tkinter import *
from tkinter import ttk
from tkinter import font


pack = False

def button():
    # Кнопка которая выполняет команду farther
    btn_1 = ttk.Button(frame, text='Продолжить игру', command=farther)
    btn_1.place(x= 1000, rely=0.25, height=100, width=500)

    # Кнопка выхода
    btn_2 = ttk.Button(frame, text= "Выход", command=lambda :win.destroy())
    btn_2.place(x= 1000, rely=0.65, height=100, width=500)

    # Пустая кнопка(в будущем будет открываться другое окной)
    btn_3 = ttk.Button(frame, text= "Пустая кнопка")
    btn_3.place(x= 1000, rely=0.45, height=100, width=500)

# Переход с frame на frame2
def farther():
    global pack
    if pack:
        frame2.pack_forget()

        frame.pack()
        frame.pack(fill=BOTH, expand=True)
        bg_logo = Label(frame, image=win_bg)
        bg_logo.grid(row=0, column=0)
        button()
        pack = False

    else:
        frame.pack_forget()

        frame2.pack(fill=BOTH, expand=True)
        map_logo = Label(frame2, image=map_bg)
        map_logo.grid(row=0, column=0)
        button2 = ttk.Button(frame2, text="Назад", command=farther)
        button2.place(x=500, y=50)
        pack = True

win = Tk()

win.title('Zuzu главный') # Name window
win.attributes('-fullscreen', True) # fullscreen

# Frame
frame = Frame(win)
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
bg_logo.grid(row=0, column=0)

# Создание кнопок
button()


win.mainloop() # End
