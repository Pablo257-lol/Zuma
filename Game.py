from tkinter import *
import math
import random

def create_ball(canvas, x, y, color):
    return canvas.create_oval(x, y, x+20, y+20, fill=color)

def move_towards_point(canvas, ball, target_x, target_y):
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
            canvas.move(ball, dx_step, dy_step)
            canvas.after(10, move_step, step+1)
        else:
            canvas.delete(ball)

    move_step(0)

def click_event(event,canvas):
    colors = ["red", "blue", "yellow", "green", "orange"]
    color = random.choice(colors)
    ball = create_ball(canvas, 125, 150, color)  # Создаем шар в центре экрана
    move_towards_point(canvas, ball, event.x, event.y)




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


def init_app(root):
    canvas = Canvas(root)
    canvas.pack(fill= BOTH, expand=True)

    # Example polygon (triangle)
    shape = [(100, 100), (150, 100), (150, 200), (100, 200)]
    center_x = 125
    center_y = 150
    draw, update_angle = init_rotating_shape(canvas, shape, center_x, center_y)

    canvas.bind("<Motion>", update_angle)
    canvas.bind("<Button-1>", lambda event: click_event(event, canvas))
