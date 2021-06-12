import random
from tkinter import *
from tkinter import messagebox
from stop_words import get_stop_words
from tkinter import filedialog


def select_all(event):
    text_box.tag_add(SEL, "1.0", END)
    text_box.mark_set(INSERT, "1.0")
    text_box.see(INSERT)
    return 'break'


def run():
    stop_words = get_stop_words('pl')

    content = text_box.get(1.0, END)

    splitted = content.split()

    try:
        gap_number = int(entry1.get())
    except Exception:
        messagebox.showerror('Błąd', 'Błędna liczba luk!')
        return

    gap_gen = int(entry1.get())

    if gap_number >= len(splitted) or gap_number <= 0:
        messagebox.showerror('Błąd', 'Błędna liczba luk!')
        return

    gaped = []
    cycle = 0

    while gap_number > 0 and cycle < len(splitted):
        gap = random.randint(1, len(splitted) - 2)
        if gap not in gaped:
            if gap < len(splitted):

                word = splitted[gap]
                word = word.replace('.', '')
                word = word.replace(',', '')
                word = word.lower()

                if word not in stop_words and len(word) > 1:
                    if splitted[gap - 1] != '........' and splitted[gap + 1] != '........':
                        if '.' in splitted[gap] or ',' in splitted[gap]:
                            if ',' in splitted[gap]:
                                splitted[gap] = f'........,'
                                gaped.append(gap)
                            else:
                                splitted[gap] = '....... .'
                                gaped.append(gap)
                        else:
                            splitted[gap] = '........'
                            gaped.append(gap)
                        gap_number -= 1
        cycle += 1

    joined = ' '.join(splitted)
    text_box.delete(1.0, END)
    text_box.insert(1.0, joined)
    messagebox.showinfo('Sukces', f'Wygenerowano {gap_gen} luk!')


def new_text():
    choice = messagebox.askquestion('Tworzenie nowego tekstu', 'Czy chcesz utworzyć nowy tekst?')
    if choice == 'yes':
        text_box.delete(1.0, END)


root = Tk()
root.title('GENERATOR LUK')
root.resizable(False, False)
screen_width = int((root.winfo_screenwidth() / 2))
screen_height = int((root.winfo_screenheight() / 2) + 200)
root.geometry(f'{screen_width}x{screen_height}')


def open_text():
    path = filedialog.askopenfilename(title='Wybierz plik',
                                      filetypes=(("Plik tekstowy", "*.txt"), ("Wszystkie pliki", "*.*")))

    try:
        with open(path, 'r') as file:
            content = file.read()
    except Exception:
        return

    text_box.delete(1.0, END)
    text_box.insert(1.0, content)


def ask_quit():
    if len(text_box.get(1.0, END)) > 1:
        ask = messagebox.askyesno("Wyjście", "Pole tekstowe nie jest puste. Czy na pewno chcesz wyjść?")
        if ask == 1:
            root.destroy()
    else:
        root.destroy()


def save_file():
    path = filedialog.asksaveasfilename(title='Zapisz plik',
                                        filetypes=(("Plik tekstowy", "*.txt"), ("Wszystkie pliki", "*.*")))

    try:
        with open(path, 'w') as file:
            content = text_box.get(1.0, END)
            file.write(content)
        messagebox.showinfo('Sukces', 'Poprawnie zapisano plik!')
    except Exception:
        return

def info():
    info_window = Toplevel(root)
    # info_window.geometry('300x100')
    info_window.resizable(False, False)
    info_window.title("O programie")
    Label(info_window,text="Program do generowania luk w tekscie.\nAutor: Robert\nWersja: 2.5").pack()


menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Nowy", command=new_text)
filemenu.add_command(label="Otwórz", command=open_text)
filemenu.add_command(label="Zapisz jako", command=save_file)
menubar.add_cascade(label="Plik", menu=filemenu)

helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_command(label="O programie", command=info)
menubar.add_cascade(label="Pomoc", menu=helpmenu)

root.config(menu=menubar)

scrollbar = Scrollbar(root)
scrollbar.grid(row=0, column=3, sticky=NS)

text_box = Text(root, wrap=WORD,
                yscrollcommand=scrollbar.set,
                width=int(screen_width / 6) - 30,
                height=int(screen_height / 20) - 2)

scrollbar.config(command=text_box.yview)
text_box.grid(row=0, column=0, columnspan=2)
text_box.bind("<Control-Key-a>", select_all)
text_box.bind("<Control-Key-A>", select_all)

label = Label(root, text='Liczba luk', font=("Arial", 12))
label.grid(row=1, column=0, pady=5, sticky=E, padx=2)
entry1 = Entry(root, width=int(screen_width / 200), font=("Arial 11"))
entry1.grid(row=1, column=1, pady=5, sticky=W, ipady=int(screen_height / 200))
entry1.insert(1, '10')

run_btn = Button(root, text='Generuj',
                 command=run,
                 font=("Arial", 12),
                 width=int(screen_width / 50),
                 height=int(screen_height / 300))
run_btn.grid(row=2, column=0, columnspan=3, pady=10)

root.protocol("WM_DELETE_WINDOW", ask_quit)
root.mainloop()
