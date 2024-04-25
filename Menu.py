from tkinter import *
from tkinter import ttk
from tkinter import font
from PIL import Image, ImageTk

# Переход с одного окна на другой
def open_new_window():
    win.withdraw()

    new_window = Toplevel(win)
    new_window.title("Карта")
    new_window.attributes('-fullscreen', True)

    new_window.iconphoto(False, duck)

    bg_logo_2 = ttk.Label(new_window, image=map_bg)
    bg_logo_2.grid(row=0, column=0)

    def close_new_window():
        new_window.destroy()
        win.deiconify()

    button_back = ttk.Button(new_window, text="Вернуться назад", command=close_new_window)
    button_back.place(x= 1000, rely=0.25, height=100, width=500)


win = Tk()

win.title('Zuzu главный') # Name window
win.attributes('-fullscreen', True) # fullscreen

# Icon
duck = PhotoImage(file="duck.png")
win.iconphoto(False,duck)

# Image
win.bg = PhotoImage(file="background_1.png")
map_bg = PhotoImage(file="Map_1.png")

# background
bg_logo = Label(win, image=win.bg)
bg_logo.grid(row=0, column=0)

# Кнопка перехода
bth = ttk.Button(win, text='Продолжить игру', command=open_new_window)
bth.place(x= 1000, rely=0.25, height=100, width=500)

# Кнопка выхода
bth_2 = ttk.Button(win, text= "Выход", command=lambda :win.destroy())
bth_2.place(x= 1000, rely=0.65, height=100, width=500)

# Пустая кнопка(в будущем будет открываться другое окной)
bth_3 = ttk.Button(win, text= "Пустая кнопка")
bth_3.place(x= 1000, rely=0.45, height=100, width=500)



win.mainloop() # End
