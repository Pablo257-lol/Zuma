from tkinter import *
import time
import tkinter as tk
import math
import random
from tkinter import font

first = 0
locked = True
save = True
clean_ball = False

####################### CREATING AND MOVING A BALL ############################
def create_ball(canvas, x, y, color):
    return canvas.create_oval(x, y, x+50, y+50, fill=color)

def move_towards_point(canvas, ball, target_x, target_y, chain_balls, color_ball, speeds, colors, moving_points, cou_balls, label, points, filename, current_value, initial_value, line, root, init_app_two, preview_ball, second_ball):
    coords = canvas.coords(ball)
    start_x = (coords[0] + coords[2]) / 2
    start_y = (coords[1] + coords[3]) / 2
    dx = target_x - start_x
    dy = target_y - start_y
    distance = ((dx ** 2) + (dy ** 2)) ** 0.5
    if distance != 0:
        steps = int(distance // 50) # Скорость полета шара
        dx_step = dx / steps
        dy_step = dy / steps


    def move_step(step):
        nonlocal start_x, start_y
        global clean_ball
        if clean_ball:
            canvas.delete(ball)
        else:
            if step < 50:
                start_x += dx_step
                start_y += dy_step

                # Проверка на прикосновение шара к другому
                for (x, y, color, ball_id, kol, point) in chain_balls:
                    # Смещение цепочки и создание в ней нового шара
                    def changing_chain(kol):
                        # Создает шар в цепочке
                        if kol < len(chain_balls):

                            # повторяем цикл перемещением шаров, с интервалом 0,01 сек.
                            print(speeds)

                            x1 = chain_balls[kol][0]
                            y1 = chain_balls[kol][1]
                            speed = chain_balls[kol][5]

                            for _ in range(17):
                                for i in range(kol, len(chain_balls)):
                                    check = True
                                    coords = canvas.coords(chain_balls[i][3])
                                    index_speed = chain_balls[i][5]
                                    if index_speed > len(speeds):
                                        end(canvas, points, root, init_app_two)
                                        return changing_chain, move_step
                                    list_index = list(chain_balls[i])
                                    list_index[0] += speeds[index_speed - 1][0]
                                    list_index[1] += speeds[index_speed - 1][1]

                                    if index_speed <= len(speeds):
                                        if speeds[index_speed - 1][0] != 0 and speeds[index_speed - 1][1] != 0 and index_speed + 1 < len(speeds):
                                            if abs(moving_points[(chain_balls[i][5])][0] - chain_balls[i][0]) <= abs(speeds[index_speed - 1][0]) and abs(moving_points[(chain_balls[i][5])][1] - chain_balls[i][1]) <= abs(speeds[index_speed - 1][1]):
                                                list_index[5] += 1
                                                list_index[0] = moving_points[(chain_balls[i][5])][0]
                                                list_index[1] = moving_points[(chain_balls[i][5])][1]
                                                check = False
                                        else:
                                            if speeds[index_speed - 1][0] != 0:
                                                if abs(moving_points[(chain_balls[i][5])][0] - chain_balls[i][0]) <= abs(speeds[index_speed - 1][0]):
                                                    list_index[5] += 1
                                                    list_index[0] = moving_points[(chain_balls[i][5])][0]
                                                    check = False
                                            else:
                                                if abs(moving_points[(chain_balls[i][5])][1] - chain_balls[i][1]) <= abs(speeds[index_speed - 1][1]):
                                                    list_index[5] += 1
                                                    list_index[1] = moving_points[(chain_balls[i][5])][1]
                                                    check = False

                                        if check:
                                            canvas.move((chain_balls[i])[3], speeds[index_speed - 1][0], speeds[index_speed - 1][1])
                                        else:
                                            canvas.move((chain_balls[i])[3], (moving_points[chain_balls[i][5]][0] - chain_balls[i][0]), (moving_points[chain_balls[i][5]][1] - chain_balls[i][1]))
                                        chain_balls[i] = tuple(list_index)
                                        # print((coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2, chain_balls[i], moving_points[chain_balls[i][5]])

                                        # print(chain_balls[i])
                                    else:
                                        stop_movement()
                                        end(canvas, points, root, init_app_two)
                                        return changing_chain, move_step, move_towards_point

                                canvas.update()
                                time.sleep(0.01)

                            index = kol
                            new_id = canvas.create_oval(x1 - 25, y1 - 25, x1 + 25, y1 + 25, fill=color_ball)
                            chain_balls.insert(kol, (x1, y1, color_ball, new_id, kol + 1, speed))

                            for a in range(index + 1, len(chain_balls)):
                                list_index = list(chain_balls[a])
                                list_index[4] += 1
                                chain_balls[a] = tuple(list_index)

                        else:
                            # Если шар попадет в самый последний шар
                            index_speed = chain_balls[kol - 1][5]
                            x1 = chain_balls[kol - 1][0]
                            y1 = chain_balls[kol - 1][1]

                            for i in range(17):

                                if index_speed >= len(moving_points):
                                    print('asdasdadasdasda')
                                    stop_movement()
                                    end(canvas, points, root, init_app_two)
                                    return changing_chain, move_step

                                if abs(moving_points[index_speed][0] - x1) <= abs(speeds[index_speed - 1][0]) and abs(moving_points[index_speed][1] - y1) <= abs(speeds[index_speed - 1][1]):
                                    index_speed += 1
                                else:
                                    x1 += speeds[index_speed - 1][0]
                                    y1 += speeds[index_speed - 1][1]

                            new_id = canvas.create_oval(x1 - 25, y1 - 25, x1 + 25, y1 + 25, fill=color_ball)
                            chain_balls.append((x1, y1, color_ball, new_id, kol + 1, index_speed))

    ####################################################### FIRST ###############################################################
                    # Столкновение летящего шара с другим
                    if ((start_x - x) ** 2 + (start_y - y) ** 2) <= (25 * 2) ** 2:
                        combo = 0

                        distant_start_x = abs(moving_points[point][0] - start_x)
                        distant_start_y = abs(moving_points[point][1] - start_y)
                        distant_x = abs(moving_points[point][0] - chain_balls[kol - 1][0])
                        distant_y = abs(moving_points[point][1] - chain_balls[kol - 1][1])

                        # Условие, чтобы шар был сзади
                        if (distant_start_x + distant_start_y) > (distant_x + distant_y):
                            print('зад', kol)
                            stop_movement()
                            canvas.delete(ball)
                            changing_chain(kol - 1)
                            resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two)


                        # Условие, чтобы шар был спереди
                        if (distant_start_x + distant_start_y) <= (distant_x + distant_y):
                            if kol == len(chain_balls):
                                canvas.delete(ball)
                                changing_chain(kol)
                                kol += 1
                            else:
                                print('перед', kol)
                                stop_movement()
                                canvas.delete(ball)
                                changing_chain(kol)
                                resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two)
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

                        print(dele)
                        # Смещаем цепочку шаров
                        def offset(kol_dele, index, zamena):
                            for a in range(index - 1, len(chain_balls)):
                                chek = True
                                index_speed = chain_balls[a][5]
                                list_index = list(chain_balls[a])
                                list_index[0] -= speeds[index_speed - 1][0]
                                list_index[1] -= speeds[index_speed - 1][1]
                                if zamena == 0:
                                    list_index[4] -= kol_dele
                                # print(moving_points[(chain_balls[a][5]) - 1], chain_balls[a], speeds[index_speed - 1])

                                if speeds[index_speed - 1][0] != 0 and speeds[index_speed - 1][1] != 0:
                                    if abs(moving_points[(chain_balls[a][5]) - 1][0] - chain_balls[a][0]) <= abs(
                                            speeds[index_speed - 1][0]) and abs(
                                            moving_points[(chain_balls[a][5]) - 1][1] - chain_balls[a][1]) <= abs(
                                            speeds[index_speed - 1][1]):
                                        # print(chain_balls[a])
                                        list_index[5] -= 1
                                        list_index[0] = moving_points[(chain_balls[a][5]) - 1][0]
                                        list_index[1] = moving_points[(chain_balls[a][5]) - 1][1]
                                        chek = False

                                else:
                                    if speeds[index_speed - 1][0] != 0:
                                        if abs(moving_points[(chain_balls[a][5]) - 1][0] - chain_balls[a][0]) <= abs(
                                                speeds[index_speed - 1][0]):
                                            # print(chain_balls[a])
                                            list_index[5] -= 1
                                            list_index[0] = moving_points[(chain_balls[a][5]) - 1][0]
                                            chek = False

                                    else:
                                        if abs(moving_points[(chain_balls[a][5]) - 1][1] - chain_balls[a][1]) <= abs(
                                                speeds[index_speed - 1][1]):
                                            # print(chain_balls[a])
                                            list_index[5] -= 1
                                            list_index[1] = moving_points[(chain_balls[a][5]) - 1][1]
                                            chek = False

                                if chek:
                                    canvas.move((chain_balls[a])[3], -(speeds[index_speed - 1][0]),
                                                -(speeds[index_speed - 1][1]))
                                else:
                                    canvas.move((chain_balls[a])[3],
                                                (moving_points[chain_balls[a][5] - 1][0] - chain_balls[a][0]),
                                                (moving_points[chain_balls[a][5] - 1][1] - chain_balls[a][1]))
                                chain_balls[a] = tuple(list_index)


                        # print(dele, kol)
                        # Если шаров с одинаковым цветом будет не менее 3, то их удаляем везде
                        if kol_dele >= 3:
                            for excess in range(0, len(dele)):
                                index = dele[excess]

                                excess = (chain_balls[index - 1][3])
                                canvas.delete(excess)

                                excess = (chain_balls[index - 1])
                                chain_balls.remove((excess))
                            combo += 1

                            decrease_number(canvas, label, points, filename, current_value, initial_value, line, combo, kol_dele) # Начисление очков


                            # print(index, len(chain_balls), '0987654310987654321098765432109886675645453442313233')
                            zamena = 0
                            if 1 < index <= len(chain_balls):
                                stop_movement()

                                # Изменяем данные у шаров, в списке
                                while ((chain_balls[index - 1][0] - chain_balls[index - 2][0]) ** 2 + (chain_balls[index - 1][1] - chain_balls[index - 2][1]) ** 2) > (25 * 2) ** 2:
                                    offset(kol_dele, index, zamena)
                                        # print(chain_balls[a], (coords[0] + coords[2]) / 2, (coords[1] + coords[3]) / 2)

                                    zamena += 1

                                    canvas.update()
                                    time.sleep(0.01)


                                resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two)

                            if index == 1:
                                stop_movement()
                                for _ in range(kol_dele):
                                    for i in range(17):
                                        offset(kol_dele, index, zamena)

                                        canvas.update()
                                        time.sleep(0.01)

                                        zamena += 1

                                resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root,init_app_two)
                                print(chain_balls)

    ########################################################################################################################

    ######################################################## REPLAY ########################################################
                        # Если первое удаление шаров было, то идет повторная проверка до тех пор, пока не перестанут попадаться такие комбинации шаров с одинаковыми цветами
                        if combo != 0:
                            combo_update = combo
                            kol = dele[-1]
                            dele = [kol]

                            print(dele, kol)
                            print(chain_balls)
                            # Точно такой же процесс, как и первый
                            if kol < len(chain_balls) and kol != 1:
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

                                        decrease_number(canvas, label, points, filename, current_value, initial_value, line, combo_update, kol_dele) # Начисление очков

                                        zamena = 0
                                        if 1 < index <= len(chain_balls):
                                            stop_movement()

                                            while ((chain_balls[index - 1][0] - chain_balls[index - 2][0]) ** 2 + (chain_balls[index - 1][1] - chain_balls[index - 2][1]) ** 2) > (25 * 2) ** 2:
                                                offset(kol_dele, index, zamena)

                                                zamena += 1

                                                canvas.update()
                                                time.sleep(0.01)

                                            resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two)

                                        if index == 1:
                                            stop_movement()
                                            for _ in range(kol_dele):
                                                for i in range(17):
                                                    offset(kol_dele, index, zamena)

                                                    canvas.update()
                                                    time.sleep(0.01)

                                                    zamena += 1

                                            resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two)

                                    # Прекращает цикл, когда новых комбинаций не появляется
                                    if combo_update != combo:
                                        combo += 1
                                    else:
                                        canvas.bind("<Button-1>",lambda event: click_event(event, canvas, chain_balls, preview_ball, second_ball, colors, speeds, moving_points, cou_balls, label, points, filename, current_value, initial_value, line, root, init_app_two))
                                        return

                        canvas.bind("<Button-1>",lambda event: click_event(event, canvas, chain_balls, preview_ball, second_ball,  colors, speeds, moving_points, cou_balls, label, points, filename, current_value, initial_value, line, root,  init_app_two))
                        return

    ########################################################################################################################

                # Передвигает летящий шар каждые 20 мс.
                canvas.move(ball, dx_step, dy_step)
                canvas.after(20, move_step, step + 1)
            else:
                # Удаляет летящий шар, когда он достигает конца окна
                canvas.delete(ball)
                canvas.bind("<Button-1>",lambda event: click_event(event, canvas, chain_balls, preview_ball, second_ball, colors, speeds, moving_points, cou_balls, label, points, filename, current_value, initial_value, line, root, init_app_two))



    move_step(0)

def click_event(event,canvas, chain_balls, preview_ball, second_ball, colors, speeds, moving_points, cou_balls, label, points, filename, current_value, initial_value, line, root, init_app_two):
    canvas.unbind("<Button-1>")
    c_ball = canvas.itemcget(preview_ball, 'fill')
    ball = create_ball(canvas, 125, 150, c_ball)  # Создаем шар в центре экрана
    move_towards_point(canvas, ball, event.x, event.y, chain_balls, c_ball, speeds, colors, moving_points, cou_balls, label, points, filename, current_value, initial_value, line, root, init_app_two, preview_ball, second_ball)
    update_preview_color(canvas, preview_ball, second_ball, colors)
########################################################################################################################

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

####################################################### END ############################################################
def end(canvas, points, root, init_app_two):
    global clean_ball

    for widget in canvas.winfo_children():  # Перебираем все дочерние элементы Canvas
        if isinstance(widget, tk.Button):  # Проверяем, является ли элемент кнопкой
            widget.config(state="disabled")  # Блокируем кнопку

    clean_ball = True
    canvas_end = tk.Canvas(canvas, width= 954, height= 470, bg= 'yellow', highlightthickness=5, highlightbackground="black")
    canvas_end.place(x= 477, y= 304)

    label_end = tk.Label(canvas_end, text= 'Конец игры', background="#FFFF00",font=("Arial", 50))
    label_end.place(relx= 0.32, rely= 0.1)
    label_points = tk.Label(canvas_end, text= f'Количество набранных очков: {points[0]}', bg= 'yellow', font=('Arial', 30))
    label_points.place(relx= 0.14, rely= 0.4)

    update_data(points[1], points[0], 'Players.txt')

    def comanda(root, init_app_two):
        global save, clean_ball
        save = False
        clean_ball = False
        reset(root, init_app_two)

    but_again = tk.Button(canvas_end, text= 'Начать заново', width= 15, font= ('Times new Roman', 30), command= lambda :comanda(root, init_app_two))
    but_again.place(relx= 0.55, rely= 0.7)
    but_exit = tk.Button(canvas_end, text='Главное меню', width= 15, font=('Times new Roman', 30), command= lambda :reset(root, init_app_two))
    but_exit.place(relx=0.1, rely=0.7)
########################################################################################################################

################################ BALLS ##########################################
def calculation(speeds, moving_points):
    for count in range(len(moving_points) - 1):
        dx = moving_points[count + 1][0] - moving_points[count][0]
        dy = moving_points[count + 1][1] - moving_points[count][1]
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        steps = int(distance // 3)  # Скорость полета шара
        dx_step = dx / steps
        dy_step = dy / steps

        speeds.insert(count, (dx_step, dy_step))


# Создает шар в цепочке и добавляет его в начало списка
def init_chain(canvas, chain_balls, colors, spawn):
    # if len(chain_balls) == cou_balls:
    #     return
    # else:
    spawn_x = spawn[0][0] # Начальные координаты шара
    spawn_y = spawn[0][1]
    color = random.choice(colors)
    x = spawn_x  # Ширина
    y = spawn_y  # Высота
    ball_id = canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=color)
    chain_balls.insert(0, (x, y, color, ball_id, 1, 1))
    if len(chain_balls) > 0: # Изменяет номер каждого шара, чтобы они все шли поочередно
        for a in range(1, len(chain_balls)):
            list_index = list(chain_balls[a])
            list_index[4] += 1
            chain_balls[a] = tuple(list_index)
    # print(chain_balls)

# Передвижение цепочки шаров и изменение их координат
distant = 0
is_moving = True
chek = 1
def move_balls(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two):
    global distant, is_moving
    if not is_moving:
        return

    if len(chain_balls) == 0:
        init_chain(canvas, chain_balls, colors, moving_points)

    for i in range(len(chain_balls)): # проходится по каждому шару в цепочке
        index = chain_balls[i][5]
        if index >= len(moving_points):
            end(canvas, points, root, init_app_two)
            return
        coords = canvas.coords(chain_balls[i][3])
        start_x = (coords[0] + coords[2]) / 2
        start_y = (coords[1] + coords[3]) / 2
        dx = moving_points[index][0] - round(start_x)
        dy = moving_points[index][1] - round(start_y)
        distance = ((dx ** 2) + (dy ** 2)) ** 0.5
        if distance != 0:

            def move_step_balls():
                nonlocal start_x, start_y, index
                global distant, chek

                if moving_points[index][0] != int(chain_balls[i][0]) or moving_points[index][1] != int(chain_balls[i][1]):
                    if i == 0:
                        distant += 1
                    start_x += speeds[index - 1][0]
                    start_y += speeds[index - 1][1]

                    # Передвигает летящий шар каждые 20 мс.
                    canvas.move(chain_balls[i][3], speeds[index - 1][0], speeds[index - 1][1])

                    # Изменяет данные координат в списке chain_balls
                    list_index = list(chain_balls[i])
                    list_index[0] += speeds[index - 1][0]
                    list_index[1] += speeds[index - 1][1]
                    chain_balls[i] = tuple(list_index)

                    if i + 1 == len(chain_balls) and distant >= 17 and chek != cou_balls: # Создает новый шар когда начальный шар проходит нужную дистанцию
                        distant = 0
                        chek += 1
                        init_chain(canvas, chain_balls, colors, moving_points)

            move_step_balls()

        else:
            list_index = list(chain_balls[i])
            list_index[5] += 1
            chain_balls[i] = tuple(list_index)
            if chain_balls[i][5] == len(moving_points): # Заканчивает игру, когда цепочка доходит до конечного пути
                end(canvas, points, root, init_app_two)
                return move_balls

    canvas.after(40, lambda: move_balls(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two))

def stop_movement():
    global is_moving
    is_moving = False

def resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two):
    global is_moving
    is_moving = True
    move_balls(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two)

########################################################################################################################
# Функция для изменения шкалы прогресса
def update(canvas, initial_value, current_value, line):
    if current_value > 0:
        # Обновление длины черты
        length = (current_value / initial_value) * 791
        canvas.coords(line, 618, 34, 618 + length, 34)


# Функция для чтения числа из файла
def read_points_from_file(filename):
    with open(filename, 'r') as file:
        number = file.read().strip()
        return int(number)

def read_name_from_file(filename):
    with open(filename, 'r') as file:
        name = file.read().strip()
    return str(name)


def update_data(name, points, output_file):
    # Читаем старое содержимое выходного файла, если оно существует
    try:
        with open(output_file, 'r', encoding='utf-8') as out:
            old_content = out.read()  # Читаем всё старое содержимое файла
    except FileNotFoundError:
        old_content = ""  # Если файл не существует, старое содержимое пустое

    # Записываем новую строку в начале файла, а затем старое содержимое
    with open(output_file, 'w', encoding='utf-8') as out:
        out.write(f"{name} - {points}\n{old_content}")  # Записываем данные в формате "Имя 123456"


# Функция для записи числа в файл
def write_number_to_file(filename, number):
    with open(filename, 'w') as file:
        file.write(str(number))

# Функция для увеличения очков
def decrease_number(canvas, label, points, filename, current_value, initial_value, line, combo, kol_dele):
    points[0] += (100 * kol_dele) * combo
    current_value -= points[0]
    label.config(text=str(points[0]))
    write_number_to_file(filename, points[0])  # Обновляем число в файле
    update(canvas, initial_value, current_value, line) # Изменяем шкалу прогресса

# Сброс уровня
def reset(root, init_app_two):
    global locked, first, distant, is_moving, chek, save, clean_ball
    clean_ball = False
    first = 0
    locked = True
    distant = 0
    is_moving = True
    chek = 1
    write_number_to_file('points.txt', 0)
    if save:
        init_app_two(root)
    else:
        save = True
        init_app(root, init_app_two)

####################################################################### MAIN PART ############################################################################################################

def init_app(root, init_app_two):

    # Очистим всё, что было на экране
    for widget in root.winfo_children():
        widget.destroy()

    canvas = tk.Canvas(root)
    canvas.pack(fill= BOTH, expand=True)

    btn_font = font.Font(family='Times new Roman', size=20)

#################################################### PANEL #############################################################
    filename = 'points.txt'
    points = [read_points_from_file(filename)]

    name = read_name_from_file('text.txt')
    points.append(name)

    initial_value = 10000 # Кол-во очков, которых нужно набрать в уровне
    current_value = initial_value

    canvas.create_rectangle((528, 2), (1483, 64), width= 5, fill= 'yellow')
    canvas.create_rectangle((618, 19), (1409, 49), width=5)
    line = canvas.create_line(618, 34, 1409, 34, fill="cyan2", width=30)

    label = tk.Label(canvas, text=str(points[0]), background="#FFFF00", fg='black', borderwidth=5,font=("Arial", 30), relief='solid')
    label.place(x=0, y=0, width=532, height=67)

    def locked_or_unlocked(): # Создание окна паузы
        global locked, clean_ball
        nonlocal pau, label_2, but_end, but_continue
        locked = not locked
        if locked:
            clean_ball = False
            enable_events()
            resume_movement(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two)
            canvas.delete(pau)
            label_2.pack_forget()
            but_end.destroy()
            but_continue.destroy()
            pause_but.config(state= tk.NORMAL)
        else:
            clean_ball = True
            disable_events()
            stop_movement()
            pau = canvas.create_rectangle((477, 304), (1431, 774), fill='#FFFF00', outline='black', width=5)
            label_2.pack(padx= 711, pady= 400)
            but_end = tk.Button(canvas, text='Завершить уровень', font=('Times new Roman', 30), command= lambda: reset(root, init_app_two))
            but_continue = tk.Button(canvas, text='Возобновить', font=('Times new Roman', 30), width= 16, command=locked_or_unlocked)

            canvas.create_window(726, 645, window= but_end)
            canvas.create_window(1184, 645, window= but_continue)
            pause_but.config(state= tk.DISABLED)


    pau = None
    label_2 = tk.Label(canvas, text='ПАУЗА', font=('Times new Roman', 60), bg='#FFFF00')
    but_end = tk.Button(canvas, text='Завершить уровень', font=btn_font, command= lambda: reset(root, init_app_two))
    but_continue = tk.Button(canvas, text='Возобновить', font=btn_font, command=locked_or_unlocked)

    pause_but = tk.Button(canvas, text= 'Приостановить', font= btn_font, bg= "#FFFF00", fg= 'black', borderwidth= 10, command= locked_or_unlocked)
    pause_but.place(x= 1486, width= 444, height= 67)

#######################################################################################################################
    # Список из которого будут рандомно выбираться цвета для шаров
    colors = ["red", "blue", "yellow", "green", "orange"]

    # Пример многоугольника (прямугольника)
    shape = [(100, 100), (150, 100), (150, 200), (100, 200)]
    center_x = 125
    center_y = 150
    draw, update_angle = init_rotating_shape(canvas, shape, center_x, center_y)

    cou_balls = 100 # Кол-во шаров
    chain_balls = []
    moving_points = [(1347, 132), (1149, 190)]
    speeds = []
    init_chain(canvas, chain_balls, colors, moving_points) # Создание цепочки шаров
    calculation(speeds, moving_points) # Высчитываем направление шаров в каждой зоны
    move_balls(canvas, chain_balls, moving_points, colors, speeds, cou_balls, points, root, init_app_two) # Запуск анимации шаров


    # Создаем шары для предварительного просмотра цвета`
    preview_ball = canvas.create_oval(1686, 849, 1786, 949, fill="white")
    second_ball = canvas.create_oval(1710, 974, 1760, 1024, fill='white')

    # Запускаем обновление цвета предварительного просмотра
    update_preview_color(canvas, preview_ball, second_ball, colors)

    def enable_events():
        canvas.bind("<Motion>", update_angle)
        canvas.bind("<Button-3>", lambda event: color_replacement(event, canvas, preview_ball, second_ball))
        canvas.bind("<Button-1>", lambda event: click_event(event, canvas, chain_balls, preview_ball, second_ball, colors, speeds, moving_points, cou_balls, label, points, filename, current_value, initial_value, line, root, init_app_two))

    def disable_events():
        canvas.unbind("<Motion>")
        canvas.unbind("<Button-3>")
        canvas.unbind("<Button-1>")

    enable_events()

    create_ball(canvas, 143, 933, 'black')