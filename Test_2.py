import tkinter as tk

def save_to_file():
    text_to_save = entry.get()
    with open("saved_text.txt", "w") as file:
        file.write(text_to_save)
    print(entry.get())

root = tk.Tk()

frame = tk.Frame(root)
frame.pack()

entry = tk.Entry(frame)
entry.pack(pady=10)

button = tk.Button(frame, text="Сохранить в файл", command=save_to_file)
button.pack()

root.mainloop()
