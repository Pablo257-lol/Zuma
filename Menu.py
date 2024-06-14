from tkinter import *
from tkinter import ttk
import re


data = "G:\Zuzu\pythonProject2\text.txt"
pack1 = False
pack2 = False

def button():
    # Кнопка которая выполняет команду farther
    btn_1 = ttk.Button(frame, text='Продолжить игру', command=data_frame)
    btn_1.place(x= 1000, rely=0.25, height=100, width=500)

    # Кнопка выхода
    btn_2 = ttk.Button(frame, text= "Выход", command=lambda :win.destroy())
    btn_2.place(x= 1000, rely=0.65, height=100, width=500)

    # Пустая кнопка(в будущем будет открываться другое окной)
    btn_3 = ttk.Button(frame, text= "Пустая кнопка")
    btn_3.place(x= 1000, rely=0.45, height=100, width=500)

def data_frame():
    global pack1
    if pack1:
        frame1_2.pack_forget()
        frame.pack(fill=BOTH, expand=True)
        pack1 = False
    else:
        frame1_2.place(relx=0.5, rely=0.5, anchor="center")
        pack1 = True
        return

def save_text():
        text = entry.get()
        with open("text.txt", "w") as file:
            file.write(text)
        file.close()
        label = Label(frame1_2,
                      text="Введенное имя должно состоять не менее 8 символов",
                      foreground="red", background="lightblue", font=("Times new Roumen", 13))
        label.place(relx= 0.5, rely= 0.6, height= 25, width= 430, anchor= "center")


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

        pack2 = True

def proverka(new_text):
    if re.match("^[a-zA-Z0-9]*$", new_text) and len(new_text) <= 16:
        return True
    else:
        return False

win = Tk()
win.title('Zuzu главный') # Name window
win.attributes('-fullscreen', True) # fullscreen

# Icon
win.iconbitmap("duck.ico")

# Image
win_bg = PhotoImage(file="background_1.png")
map_bg = PhotoImage(file="Map_1.png")
duck = PhotoImage(file="duck.png")

# Frame
frame = Frame(win)
frame.pack(fill=BOTH, expand=True)
# background
bg_logo = Label(frame, image=win_bg)
bg_logo.pack()
# button во frame
button()

# frame 1.2
frame1_2 = Frame(win, width=500, height= 300, bg= "lightblue")


prov = (frame1_2.register(proverka), '%P')
entry = Entry(frame1_2, validate="key", validatecommand=prov, font=("Times new Roman", 23))
entry.place(relx= 0.47, rely= 0.4, height= 50, width= 300, anchor="center")

btn1_1 = ttk.Button(frame1_2, text= "Продолжить", command=save_text)
btn1_1.place(relx= 0.47, rely=0.7, height=25, width=100, anchor= "center")


# frame2
frame2 = Frame(win)
map_logo = Label(frame2, image=map_bg)
map_logo.pack()
button2 = ttk.Button(frame2, text="Назад", command=farther)
button2.place(x=500, y=50)

win.mainloop() # End