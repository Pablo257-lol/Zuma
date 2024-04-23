from tkinter import *
def finish():
    win.destroy()

win = Tk()

win.title('Zuzu') # Name window
win.protocol('WM_DELETE_WINDOW', finish)
win.attributes('-fullscreen', True) # fullscreen
canvas = Canvas(win, width=1920, height=1080, bd=0, highlightthickness=0)
canvas.pack()

duck = PhotoImage(file="duck.png")
win.iconphoto(False,duck)

# background
bg = PhotoImage(file="background_1.png")
bg = bg.subsample(1,1)
bg_id1 = canvas.create_image(0,0,anchor=NW,image=bg)

win.mainloop() # End