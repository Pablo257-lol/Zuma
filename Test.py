from tkinter import *
from PIL import Image, ImageTk

win = Tk()
win.geometry('800x800')
win.resizable(True, True)

main_frame = Frame(win, bg='white')
main_frame.pack(fill=BOTH, expand=True)
main_frame.columnconfigure(0, weight=1)
main_frame.rowconfigure(0, weight=1)

duck = ImageTk.PhotoImage(Image.open('background.png'))

lable_duck = Label(
    main_frame,
    image=duck,
    bg='white',
)

lable_duck.grid(row=0, column=0)

win.mainloop()