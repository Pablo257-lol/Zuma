from tkinter import *
import time
import tkinter as tk
import math
import random

first = 0

####################### CREATING AND MOVING A BALL ############################
def create_ball(canvas, x, y, color):
    return canvas.create_oval(x, y, x+50, y+50, fill=color)

def move_towards_point(canvas, ball, target_x, target_y, chain_balls, color_ball):
    coords = canvas.coords(ball)
    start_x = (coords[0] + coords[2]) / 2
    start_y = (coords[1] + coords[3]) / 2
    dx = target_x - start_x
    dy = target_y - start_y
    distance = ((dx ** 2) + (dy ** 2)) ** 0.5
    if distance != 0:
        steps = int(distance // 50)# Скорость полета шара
        dx_step = dx / steps
        dy_step = dy / steps


    def move_step(step):
        nonlocal start_x, start_y
        if step < 400:
            start_x += dx_step
            start_y += dy_step

            # Проверка на прикосновение шара к другому
            for (x, y, color, ball_id, kol) in chain_balls:

                # Смещение цепочки и создание в ней нового шара
                def changing_chain(kol):
                    # Создает шар в цепочке
                    if kol < len(chain_balls):

                        # повторяем цикл перемещением шаров, с интервалом 0,01 сек.
                        for _ in range(10):
                            for i in range(kol, len(chain_balls)):
                                canvas.move((chain_balls[i])[3], 5, 0)
                            canvas.update()
                            time.sleep(0.01)

                        index = kol
                        x1 = int(canvas.coords(chain_balls[index][3])[0] - 25)
                        y1 = 800
                        new_id = canvas.create_oval(x1 - 25, y1 - 25, x1 + 25, y1 + 25, fill=color_ball)
                        chain_balls.insert(kol, (x1, y1, color_ball, new_id, kol + 1))

                        # Изменяем данные у шаров, в записях
                        for a in range(index + 1, len(chain_balls)):
                            list_index = list(chain_balls[a])
                            list_index[4] += 1
                            list_index[0] += 50
                            chain_balls[a] = tuple(list_index)

                    else:
                        # Если шар попадет в самый последний шар
                        x1 = int(canvas.coords(chain_balls[kol - 1][3])[0] + 25 * 3)
                        y1 = 800
                        new_id = canvas.create_oval(x1 - 25, y1 - 25, x1 + 25, y1 + 25, fill=color_ball)
                        chain_balls.insert(kol, (x1, y1, color_ball, new_id, kol + 1))

####################################################### FIRST ###############################################################
                # Столкновение летящего шара с другим
                if ((start_x - x) ** 2 + (start_y - y) ** 2) <= (25 * 2) ** 2:
                    combo = 0

                    # Условие, чтобы шар был сзади
                    if start_x < x:
                        canvas.delete(ball)
                        changing_chain(kol - 1)

                    # Условие, чтобы шар был спереди
                    if start_x == x or start_x > x:
                        canvas.delete(ball)
                        changing_chain(kol)
                        kol += 1

                    index_kol = kol
                    dele = []
                    kol_dele = 1
                    dele.append(index_kol)
                    # Проверяем кол-во шаров одинакового цвета, которые идут сзади от летящего шара
                    while index_kol >= 2 and chain_balls[index_kol - 1][2] == chain_balls[index_kol - 2][2]:
                        kol_dele += 1
                        dele.append(index_kol - 1)
                        index_kol -= 1

                    index_kol = kol
                    # Проверяем кол-во шаров одинакового цвета, которые идут спереди от летящего шара
                    while index_kol != len(chain_balls) and chain_balls[index_kol - 1][2] == chain_balls[index_kol][2]:
                        kol_dele += 1
                        dele.append(index_kol + 1)
                        index_kol += 1

                    # Сортируем список по убыванию, в котором находятся индексы шаров с одинаковым цветом
                    dele.sort(reverse= True)
                    # Если шаров с одинаковым цветом будет не менее 3, то их удаляем везде
                    if kol_dele >= 3:
                        for excess in range(0, len(dele)):
                            index = dele[excess]

                            excess = (chain_balls[index - 1][3])
                            canvas.delete(excess)

                            excess = (chain_balls[index - 1])
                            chain_balls.remove((excess))
                        combo += 1

                        # Изменяем данные у шаров, в записях
                        for _ in range(kol_dele):
                            for a in range(index - 1, len(chain_balls)):
                                list_index = list(chain_balls[a])
                                list_index[4] -= 1
                                list_index[0] -= 50
                                chain_balls[a] = tuple(list_index)

                            # повторяем цикл перемещением шаров, с интервалом 0,01 сек.
                            for _ in range(10):
                                for i in range(index - 1, len(chain_balls)):
                                    canvas.move((chain_balls[i])[3], -5, 0)
                                canvas.update()
                                time.sleep(0.01)
########################################################################################################################

######################################################## REPLAY ########################################################
                    # Если первое удаление шаров было, то идет повторная проверка до тех пор, пока не перестанут попадаться такие комбинации шаров с одинаковыми цветами
                    if combo != 0:
                        combo_update = combo
                        kol = dele[-1]
                        # Точно такой же процесс, как и первый
                        if kol < len(chain_balls):
                            while (kol >= 2 and chain_balls[kol - 1][2] == chain_balls[kol - 2][2]) or (kol != len(chain_balls) and chain_balls[kol - 1][2] == chain_balls[kol][2]):
                                index_kol = dele[-1]
                                kol = dele[-1]
                                dele = []
                                kol_dele_right = 1
                                kol_dele_left = 0
                                dele.append(index_kol)

                                while index_kol >= 2 and chain_balls[index_kol - 1][2] == chain_balls[index_kol - 2][2]:
                                    kol_dele_left += 1
                                    dele.append(index_kol - 1)
                                    index_kol -= 1

                                index_kol = kol
                                while index_kol != len(chain_balls) and chain_balls[index_kol - 1][2] == chain_balls[index_kol][2]:
                                    kol_dele_right += 1
                                    dele.append(index_kol + 1)
                                    index_kol += 1

                                dele.sort(reverse=True)
                                kol_dele = kol_dele_left + kol_dele_right
                                if kol_dele_left > 0 and kol_dele >= 3:
                                    for excess in range(0, len(dele)):
                                        index = dele[excess]

                                        excess = (chain_balls[index - 1][3])
                                        canvas.delete(excess)

                                        excess = (chain_balls[index - 1])
                                        chain_balls.remove((excess))
                                    combo_update += 1

                                    for _ in range(kol_dele):
                                        for a in range(index - 1, len(chain_balls)):
                                            list_index = list(chain_balls[a])
                                            list_index[4] -= 1
                                            list_index[0] -= 50
                                            chain_balls[a] = tuple(list_index)

                                        # повторяет цикл перемещением шаров, с интервалом 0,01 сек.
                                        for _ in range(10):
                                            for i in range(index - 1, len(chain_balls)):
                                                canvas.move((chain_balls[i])[3], -5, 0)
                                            canvas.update()
                                            time.sleep(0.01)
                                # Прекращает цикл, когда новых комбинаций не появляется
                                if combo_update != combo:
                                    combo += 1
                                else: return
                    return

########################################################################################################################

            # Передвигает летящий шар каждые 20 мс.
            canvas.move(ball, dx_step, dy_step)
            canvas.after(20, move_step, step + 1)
        else:
            # Удаляет летящий шар, когда он достигает конца окна
            canvas.delete(ball)


    move_step(0)

def click_event(event,canvas, chain_balls, preview_ball, second_ball, colors):
    c_ball = canvas.itemcget(preview_ball, 'fill')
    ball = create_ball(canvas, 125, 150, c_ball)  # Создаем шар в центре экрана
    move_towards_point(canvas, ball, event.x, event.y, chain_balls, c_ball)
    update_preview_color(canvas, preview_ball, second_ball, colors)
################################################################################

# Функция для обновления цвета шара предварительного просмотра
def update_preview_color(canvas, preview_ball, second_ball, colors):
    global first
    fill_color = canvas.itemcget(second_ball, 'fill')

    # Условие, при котором цвет первого шара создается рандомно, в остальных случаях цвет будет браться со второго шара
    if first == 0:
        color = random.choice(colors)
        canvas.itemconfig(preview_ball, fill=color)
        first += 1
    else:
        canvas.itemconfig(preview_ball, fill=fill_color)

    color_sec = random.choice(colors)
    canvas.itemconfig(second_ball, fill= color_sec)

# Функция, которая заменяет цвета шаров предварительного просмотра на противоположные
def color_replacement(event, canvas, preview_ball, second_ball):
    first_color = canvas.itemcget(preview_ball, 'fill')
    second_color = canvas.itemcget(second_ball, 'fill')
    canvas.itemconfig(preview_ball, fill= second_color)
    canvas.itemconfig(second_ball, fill= first_color)


############################ TURNING THE TOWER #################################
def init_rotating_shape(canvas, shape, center_x, center_y):
    angle = 0
    canvas_shape = None

    def draw():
        nonlocal canvas_shape
        if canvas_shape:
            canvas.delete(canvas_shape)

        rotated_shape = rotate_polygon(shape, angle)
        canvas_shape = canvas.create_polygon(rotated_shape, fill="blue", outline="black")

    def rotate_polygon(polygon, angle):
        cx = center_x
        cy = center_y
        rotated_points = []
        for x, y in polygon:
            x -= cx
            y -= cy
            new_x = x * math.cos(math.radians(angle)) - y * math.sin(math.radians(angle))
            new_y = x * math.sin(math.radians(angle)) + y * math.cos(math.radians(angle))
            rotated_points.append((new_x + cx, new_y + cy))
        return rotated_points

    def update_angle(event):
            nonlocal angle
            x, y = event.x, event.y
            angle = math.degrees(math.atan2(y - center_y, x - center_x))
            draw()

    return draw, update_angle
#################################################################################

################################ BALLS ###################################
def init_chain(canvas, num_balls, chain_balls, colors):
    kol = 0
    for i in range(num_balls):
        kol += 1
        color = random.choice(colors)
        x = 600 + i * 50  # Расстояние между шарами (координата x, кол-во шаров, расстояние между шарами)
        y = 800  # Высота для всех шаров
        ball_id = canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=color)
        chain_balls.append((x, y, color, ball_id, kol))
#########################################################################


def init_app(root):
    canvas = tk.Canvas(root)
    canvas.pack(fill= BOTH, expand=True)

    # Список из которого будут рандомно выбираться цвета для шаров
    colors = ["red", "blue", "yellow", "green", "orange"]

    # Пример многоугольника (треугольника)
    shape = [(100, 100), (150, 100), (150, 200), (100, 200)]
    center_x = 125
    center_y = 150
    draw, update_angle = init_rotating_shape(canvas, shape, center_x, center_y)

    num_balls = 20 # Кол-во шаров
    chain_balls = []
    init_chain(canvas, num_balls, chain_balls, colors) # Создание цепочки шаров


    # Создаем шар для предварительного просмотра цвета
    preview_ball = canvas.create_oval(1686, 849, 1786, 949, fill="white")
    second_ball = canvas.create_oval(1710, 974, 1760, 1024, fill='white')

    # Запускаем обновление цвета предварительного просмотра
    update_preview_color(canvas, preview_ball, second_ball, colors)

    canvas.bind("<Motion>", update_angle)
    canvas.bind("<Button-3>", lambda event: color_replacement(event, canvas, preview_ball, second_ball))
    canvas.bind("<Button-1>", lambda event: click_event(event, canvas, chain_balls, preview_ball, second_ball, colors))