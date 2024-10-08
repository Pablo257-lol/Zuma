import tkinter as tk

# Начальное значение
initial_value = 100
current_value = initial_value


def update():
    global current_value
    if current_value > 0:
        current_value -= 1
        label.config(text=str(current_value))

        # Обновление длины черты
        length = (current_value / initial_value) * 200
        canvas.coords(line, 50, 100, 50 + length, 100)

        # Запланировать следующее обновление через 1 секунду
        root.after(1000, update)


# Создание основного окна
root = tk.Tk()
root.title("Countdown App")

# Создание холста для рисования
canvas = tk.Canvas(root, width=300, height=200)
canvas.pack()

# Отображение начального числа
label = tk.Label(root, text=str(current_value), font=("Arial", 24))
label.pack(pady=10)

# Начальное состояние черты
line = canvas.create_line(50, 100, 250, 100, fill="black", width=5)

# Запуск обновления
update()

# Запуск главного цикла приложения
root.mainloop()
