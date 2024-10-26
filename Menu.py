from tkinter import *
import tkinter as tk
from tkinter import font
import Game
import re
from PIL import Image, ImageTk
import pyaudio
import wave
import threading

data = "Data/text.txt"
pack1 = False
pack2 = False
pack3 = True

# Начальное изображение на кнопке
current_image = 1
is_playing = False
thread = None

def button(frame, btn_font, frame1_2, frame3):
    global current_image
    # Кнопка, для перехода в окно выбора уровней
    btn_1 = Button(frame, font=btn_font, text='Начать игру', command=lambda: data_frame(frame, frame1_2))
    btn_1.place(x= 1000, rely=0.25, height=100, width=500)

    # Кнопка выхода
    btn_2 = Button(frame, font=btn_font, text= "Выход", command=lambda :win.destroy())
    btn_2.place(x= 1000, rely=0.65, height=100, width=500)

    # Результаты игры
    btn_3 = Button(frame, font=btn_font, text= "Результаты", command=lambda :farther(frame, frame3, btn_font, frame1_2))
    btn_3.place(x= 1000, rely=0.45, height=100, width=500)


    # Загрузка изображений
    image_path1 = "Images/on.png"  # Замените на путь к первому изображению
    image_path2 = "Images/off.png"  # Замените на путь ко второму изображению

    image1 = Image.open(image_path1)
    image2 = Image.open(image_path2)

    razm = 5

    # Изменяем их размеры
    resized_image1 = image1.resize((image1.width // (razm + 1), image1.height // (razm + 1)))
    resized_image2 = image2.resize((image2.width // razm, image2.height // razm))

    photo1 = ImageTk.PhotoImage(resized_image1)
    photo2 = ImageTk.PhotoImage(resized_image2)
    if current_image == 1:
        btn_zv = Button(frame, image= photo1, command= lambda: toggle_image(btn_zv, photo1, photo2))
    else:
        btn_zv = Button(frame, image=photo2, command=lambda: toggle_image(btn_zv, photo1, photo2))
    btn_zv.place(x= 1810, y= 10, height= 100, width= 100)

# Переходит во frame1_2
# (при повторном вызове, будет постоянно переходить во frame2)
def data_frame(frame, frame1_2):
    global pack1
    if pack1:
        import Game
        frame.pack_forget()
        Game.init_app(win, init_app_two)
    else:
        for widget in frame.winfo_children():  # Перебираем все дочерние элементы Canvas
            if isinstance(widget, tk.Button):  # Проверяем, является ли элемент кнопкой
                widget.config(state="disabled")  # Блокируем кнопку
        frame1_2.place(relx=0.5, rely=0.5, anchor="center")
        pack1 = True
        return


# Сохраняет введенные данные в файл text.txt,
# если длинна текста будет не меньше 8 символов
def save_text(entry, frame, label, frame1_2):
    if len(entry.get()) >= 4:
        with open("Data/text.txt", "w") as file:
            file.write(entry.get())
        file.close()
        frame.pack_forget()
        frame1_2.destroy()
        Game.init_app(win, init_app_two)
    else:
        label.place(relx=0.5, rely=0.57, height=25, width=430, anchor="center")
        label.after(5000, lambda: label.place_forget()) # 5000 ms

# Переход между frame и frame3
def farther(frame, frame3, btn_font, frame1_2):
    global pack2
    if pack2:
        frame3.pack_forget()
        frame.pack(fill=BOTH, expand=True)
        button(frame, btn_font, frame1_2, frame3)
        pack2 = False
    else:
        frame.pack_forget()
        frame3.pack(fill=BOTH, expand=True)
        pack2 = True


def proverka(new_text):
    if re.match("^[a-zA-Z]*$", new_text) and len(new_text) <= 16:
        return True
    else:
        return False

# Очистим всё, что было на экране
def clean():
    for widget in win.winfo_children():
        widget.destroy()


def draw_circle(canvas, x, y, radius):
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, outline='black', fill='blue')


# Функция для чтения строк из файла и сортировки по числам от большего к меньшему
def read_and_sort_lines_by_number(filename):
    with open(filename, 'r') as file:
        lines = file.readlines()

    # Функция для извлечения числового значения из строки (если есть)
    def extract_number(line):
        numbers = re.findall(r'\d+', line)  # Ищем все числа в строке
        return int(numbers[0]) if numbers else 0  # Берем первое найденное число или 0, если нет чисел

    # Сортируем строки по числовому значению, от большего к меньшему
    sorted_lines = sorted(lines, key=extract_number, reverse=True)
    return [line.strip() for line in sorted_lines]  # Убираем лишние пробелы и символы новой строки

def toggle_image(button, photo1, photo2):
    # Переключение изображения на кнопке при нажатии
    global current_image
    # Переключение изображения
    if current_image == 1:
        button.config(image=photo2)
        current_image = 2
        toggle_music()
    else:
        button.config(image=photo1)
        current_image = 1
        toggle_music()


def play_music():
    global is_playing
    # Открываем WAV файл
    wf = wave.open('Music\Пляжные Волны.wav', 'rb')  # Укажите путь к вашему WAV файлу

    # Инициализация PyAudio
    p = pyaudio.PyAudio()

    # Открываем поток
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                     channels=wf.getnchannels(),
                     rate=wf.getframerate(),
                     output=True)

    while is_playing:
        # Сброс позиции в начало файла
        wf.rewind()
        data = wf.readframes(1024)
        while data and is_playing:
            stream.write(data)
            data = wf.readframes(1024)

    # Закрытие потока и PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()
    wf.close()

def toggle_music():
    global is_playing, thread
    if is_playing:
        is_playing = False
        if thread is not None:
            thread.join()  # Ждем завершения потока
    else:
        is_playing = True
        thread = threading.Thread(target=play_music)
        thread.start()


def init_app_two(win):
    global pack1
    pack1 = False

    clean()

    toggle_music() # Запуск музыки

    # Image
    win_bg = PhotoImage(file="Images/background_1.png")
    btn_font = font.Font(family='Times new Roman', size=30)

    # Frame
    frame = Frame(win)
    frame.pack(fill=BOTH, expand=True)
    # background
    bg_logo = Label(frame, image= win_bg)
    bg_logo.pack()

    # Frame - Поле ввода информации
    frame1_2 = Frame(win, width=500, height= 300, bg= "lightblue", highlightthickness=10, highlightbackground="black")

    prov = (frame1_2.register(proverka), '%P')
    entry = Entry(frame1_2, validate="key", validatecommand=prov, font=("Times new Roman", 23))
    entry.place(relx= 0.49, rely= 0.4, height= 50, width= 300, anchor="center")

    label_nad = Label(frame1_2,
                  text="Введите никнейм",
                  foreground="black", background="lightblue", font=("Times new Roumen", 30))
    label_nad.place(relx=0.5, rely=0.15, height=40, width=430, anchor="center")

    label = Label(frame1_2,
                      text="Введенное имя должно состоять не менее 4 символов",
                      foreground="red", background="lightblue", font=("Times new Roumen", 13))

    btn1_1 = Button(frame1_2, font= ('Times new Roman', 20), text= "Продолжить", command=lambda: save_text(entry, frame, label, frame1_2))
    btn1_1.place(relx= 0.49, rely=0.75, height=50, width=150, anchor= "center")

########################################################################################################################
    # frame1.3 - Результаты игры
    frame3 = tk.Frame(win)

    bg_logo = Label(frame3, image= win_bg)
    bg_logo.pack()

    frame3_2 = Frame(frame3, width=1050, height= 680, bg= "lightblue", highlightthickness=10, highlightbackground="black")
    frame3_2.place(x= 450, y= 185)
    btn1_3 = Button(frame3, font= btn_font, text= 'Главное меню', command=lambda :farther(frame, frame3, btn_font, frame1_2))
    btn1_3.place(x= 1501, y= 17, height=137, width=403)
    label_info = tk.Label(frame3_2, text= 'ИГРОК - ОЧКИ', bg= 'lightblue', font=('Arial', 50))
    label_info.place(x= 300, y=0)
    canvas_line = tk.Canvas(frame3, width= 1029, height= 10, bg= 'black')
    canvas_line.place(x= 460, y= 285)

    # Создаем Canvas для размещения строк
    canvas = tk.Canvas(frame3_2, width=1030, height= 780, bg="lightblue", highlightthickness=1, highlightbackground="lightblue")
    scrollbar = tk.Scrollbar(frame3_2, width= 50, orient=tk.VERTICAL, command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg= 'lightblue')

    scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    canvas.create_window((0, 15), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Чтение и отображение строк из файла, отсортированных по числам
    filename = 'Data/Players.txt'  # Задайте путь к вашему файлу
    lines = read_and_sort_lines_by_number(filename)

    for line in lines:
        label_data = tk.Label(scrollable_frame, text=line, font=("Arial", 50), bg='lightblue')
        label_data.pack(anchor="w", padx=10, pady=2)

    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(padx= 0, pady= 100)
########################################################################################################################

    # button во frame
    button(frame, btn_font, frame1_2, frame3)

    win.mainloop() # End

win = tk.Tk()
win.title('Zuzu главный')  # Name window
win.attributes('-fullscreen', True)  # fullscreen

init_app_two(win)