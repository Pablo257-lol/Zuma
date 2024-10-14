from tkinter import *
import tkinter as tk
from tkinter import font
import Game
import math
import re

data = "text.txt"
pack1 = False
pack2 = False

def button(frame, btn_font, frame1_2, frame3, frame2):
    # Кнопка, которая выполняет команду farther
    btn_1 = Button(frame, font=btn_font, text='Начать игру', command=lambda: data_frame(frame, frame1_2))
    btn_1.place(x= 1000, rely=0.25, height=100, width=500)

    # Кнопка выхода
    btn_2 = Button(frame, font=btn_font, text= "Выход", command=lambda :win.destroy())
    btn_2.place(x= 1000, rely=0.65, height=100, width=500)

    # Пустая кнопка(в будущем будет открываться другое окной)
    btn_3 = Button(frame, font=btn_font, text= "Результаты", command=lambda :farther(frame, frame3, btn_font, frame1_2, frame3))
    btn_3.place(x= 1000, rely=0.45, height=100, width=500)
    if pack1:
        btn_1['text'] = 'Продолжить игру'

# Переходит во frame1_2
# (при повторном вызове, будет постоянно переходить во frame2)
def data_frame(frame, frame1_2):
    global pack1
    if pack1:
        frame.pack_forget()
    else:
        frame1_2.place(relx=0.5, rely=0.5, anchor="center")
        pack1 = True
        return

# Сохраняет введенные данные в файл text.txt,
# если длинна текста будет не меньше 8 символов
def save_text(entry, frame, frame2, label, frame1_2):
    global pack2
    if len(entry.get()) >= 8:
        with open("text.txt", "w") as file:
            file.write(entry.get())
        file.close()
        frame.pack_forget()
        frame1_2.destroy()

        frame2.pack()
        pack2 = True
    else:
        label.place(relx=0.5, rely=0.57, height=25, width=430, anchor="center")
        label.after(5000, lambda: label.place_forget()) # 5000 ms

# Переход с frame на frame2
def farther(frame, frame2, btn_font, frame1_2, frame3):
    global pack2
    if pack2:
        frame2.pack_forget()
        frame.pack(fill=BOTH, expand=True)
        button(frame, btn_font, frame1_2, frame3, frame2)
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

# Очистим всё, что было на экране
def clean():
    for widget in win.winfo_children():
        widget.destroy()

def init_app_two(win):

    clean()

    # Image
    win_bg = PhotoImage(file="background_1.png")
    map_bg = PhotoImage(file="Map_1.png")
    duck = PhotoImage(file="duck.png")

    btn_font = font.Font(family='Times new Roman', size=20)

    # Frame
    frame = Frame(win)
    frame.pack(fill=BOTH, expand=True)
    # background
    bg_logo = Label(frame, image= win_bg)
    bg_logo.pack()


    # Frame - Поле ввода информации
    frame1_2 = Frame(win, width=500, height= 300, bg= "lightblue")

    prov = (frame1_2.register(proverka), '%P')
    entry = Entry(frame1_2, validate="key", validatecommand=prov, font=("Times new Roman", 23))
    entry.place(relx= 0.49, rely= 0.4, height= 50, width= 300, anchor="center")

    label = Label(frame1_2,
                      text="Введенное имя должно состоять не менее 8 символов",
                      foreground="red", background="lightblue", font=("Times new Roumen", 13))

    btn1_1 = Button(frame1_2, font= btn_font, text= "Продолжить", command=lambda: save_text(entry, frame, frame2, label, frame1_2))
    btn1_1.place(relx= 0.49, rely=0.75, height=50, width=150, anchor= "center")

    # frame1.3 - Результаты игры
    frame3 = Frame(win)

    bg_logo = Label(frame3, image= win_bg)
    bg_logo.pack()

    frame3_2 = Frame(frame3, width=1050, height= 890, bg= "lightblue")
    frame3_2.place(x= 450, y= 185)
    btn1_3 = Button(frame3, font= btn_font, text= 'Главное меня', command=lambda :farther(frame, frame3, btn_font, frame1_2, frame3))
    btn1_3.place(x= 1501, y= 17, height=137, width=403)


    # frame2 - выбор уровней
    frame2 = Frame(win)
    map_logo = Label(frame2, image= map_bg)
    map_logo.pack()
    button2 = Button(frame2, font= btn_font, text="Главное меню", command=lambda: farther(frame, frame2, btn_font, frame1_2, frame3))
    button2.place(x=10, y=10, width=200, height=300)

    # button во frame
    button(frame, btn_font, frame1_2, frame3, frame2)

    win.mainloop() # End


win = tk.Tk()
win.title('Zuzu главный')  # Name window
win.attributes('-fullscreen', True)  # fullscreen


init_app_two(win)