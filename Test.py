import tkinter as tk
import random

# Настройки
num_balls = 10
ball_radius = 20
canvas_width = 600
canvas_height = 200


# Функция для генерации случайного цвета
def random_color():
    return f'#{random.randint(0, 0xFFFFFF):06x}'


# Функция для сдвига шаров
def shift_balls(index):
    global balls

    # Сдвигаем все шары вперед на одно место
    for i in range(index + 1, len(balls)):
        canvas.move(balls[i][0], ball_radius * 2 + 10, 0)  # balls[i][0] - идентификатор шара

    # Проверяем наличие пустого места и добавляем новый шар
    if index + 1 < len(balls):
        x1 = canvas.coords(balls[index][0])[0] + ball_radius * 2 + 10
        y1 = 100
        new_ball = canvas.create_oval(x1, y1, x1 + ball_radius * 2, y1 + ball_radius * 2, fill=random_color())
        balls.insert(index + 1, (new_ball, (x1, y1)))  # Добавляем шар и его координаты


# Функция для анимации
def move_balls():
    if len(balls) > 0:
        # Выбираем случайный шар для сдвига
        index = random.randint(0, len(balls) - 1)
        shift_balls(index)

    # Запускаем функцию снова через 3000 мс (3 секунды)
    root.after(3000, move_balls)


# Создаем главное окно
root = tk.Tk()
root.title("Цепочка шаров")

# Создаем холст
canvas = tk.Canvas(root, width=canvas_width, height=canvas_height, bg='white')
canvas.pack()

# Создаем шары
balls = []
for i in range(num_balls):
    x = 50 + i * (ball_radius * 2 + 10)
    y = 100
    ball = canvas.create_oval(x, y, x + ball_radius * 2, y + ball_radius * 2, fill=random_color())
    balls.append((ball, (x, y)))  # Сохраняем идентификатор шара и его координаты

# Запускаем анимацию
move_balls()

# Запускаем главный цикл приложения
root.mainloop()
