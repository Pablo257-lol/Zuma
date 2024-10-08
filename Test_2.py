import tkinter as tk
from tkinter import BOTH

def update(canvas, label, initial_value, current_value, line):
    if current_value > 0:
        current_value -= 1
        label.config(text=str(current_value))

        # Обновление длины черты
        length = (current_value / initial_value) * 200
        canvas.coords(line, 618, 34, 618 + length, 34)

        # Запланировать следующее обновление через 1 секунду
        canvas.after(1000, update, canvas, label, initial_value, current_value, line)

def init_app(root):
    canvas = tk.Canvas(root)
    canvas.pack(fill=BOTH, expand=True)

    #################################################### PANEL #############################################################
    initial_value = 50000
    current_value = initial_value

    canvas.create_rectangle((533, 1), (1486, 64), width=5, fill='yellow')
    canvas.create_rectangle((618, 19), (1409, 49), width=5)
    line = canvas.create_line(618, 34, 1409, 34, fill="cyan2", width=30)

    label = tk.Label(canvas, text=str(current_value), background="#FFFF00", fg='black', borderwidth=5,
                     font=("Arial", 30), relief='solid')
    label.place(x=0, y=0, width=532, height=67)

    update(canvas, label, initial_value, current_value, line)

if __name__ == "__main__":
    root = tk.Tk()
    init_app(root)
    root.mainloop()
