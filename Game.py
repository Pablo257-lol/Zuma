from tkinter import *
import tkinter as tk
import math
import random

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
        steps = int(distance // 5)
        dx_step = dx / steps
        dy_step = dy / steps



    def move_step(step):
        nonlocal start_x, start_y
        if step < 400:
            start_x += dx_step
            start_y += dy_step

            # Проверка на прикосновение шара к другому
            for (x, y, color, ball_id) in chain_balls:
                chain_ball = (x, y, color, ball_id)
                if ((start_x - x) ** 2 + (start_y - y) ** 2) <= (25 * 2) ** 2 and color_ball == color:
                    canvas.delete(ball)
                    canvas.delete(ball_id)
                    chain_balls.remove(chain_ball)
                    return

                if ((start_x - x) ** 2 + (start_y - y) ** 2) <= (25 * 2) ** 2 and color_ball != color:
                    canvas.delete(ball)
                    for i in range(ball_id, len(chain_balls)):
                        canvas.move((chain_balls[i])[3], 25 * 2, 0)

                    if ball_id < len(chain_balls):
                        index = ball_id
                        x1 = canvas.coords(chain_balls[index])[0] + 25 * 2
                        y1 = 800
                        new_ball = canvas.create_oval(x1, y1, x1 + 25 * 2, y1 + 25 * 2, fill= color_ball)
                        chain_balls.insert(ball_id + 1, new_ball)
                    return



            canvas.move(ball, dx_step, dy_step)
            canvas.after(10, move_step, step+1)
        else:
            canvas.delete(ball)


    move_step(0)

def click_event(event,canvas, chain_balls):
    colors = ["red", "blue", "yellow", "green", "orange"]
    c_ball = random.choice(colors)
    ball = create_ball(canvas, 125, 150, c_ball)  # Создаем шар в центре экрана
    move_towards_point(canvas, ball, event.x, event.y, chain_balls, c_ball)
################################################################################

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
def init_chain(canvas, num_balls, chain_balls):
    colors = ["red", "blue", "yellow", "green", "orange"]
    for i in range(num_balls):
        color = random.choice(colors)
        x = 600 + i * 50  # Расстояние между шарами (координата x, кол-во шаров, расстояние между шарами)
        y = 800  # Высота для всех шаров
        ball_id = canvas.create_oval(x - 25, y - 25, x + 25, y + 25, fill=color)

        chain_balls.append((x, y, color, ball_id))

def ini_app(canvas, chain_balls):

    num_balls = 20  # Количество шаров в цепочке
    init_chain(canvas, num_balls, chain_balls)

#########################################################################


def init_app(root):
    canvas = tk.Canvas(root)
    canvas.pack(fill= BOTH, expand=True)

    # Example polygon (triangle)
    shape = [(100, 100), (150, 100), (150, 200), (100, 200)]
    center_x = 125
    center_y = 150
    draw, update_angle = init_rotating_shape(canvas, shape, center_x, center_y)

    chain_balls = []
    ini_app(canvas, chain_balls) # Создание цепочки шаров

    canvas.bind("<Motion>", update_angle)
    canvas.bind("<Button-1>", lambda event: click_event(event, canvas, chain_balls))

