import random
from tkinter import *
from tkinter import messagebox
from stop_words import get_stop_words
from tkinter import filedialog


class App:
    def __init__(self, master):
        self.master = master
        self.master.title('GENERATOR LUK')
        self.window_width = int((root.winfo_screenwidth() / 2))
        self.window_height = int((root.winfo_screenheight() / 2) + 200)
        self.master.geometry(f'{self.window_width}x{self.window_height}')
        Grid.rowconfigure(root, index=0, weight=1)
        Grid.columnconfigure(root, index=0, weight=1)
        self.master.minsize(300, 300)

        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Nowy", command=self.new_text)
        self.filemenu.add_command(label="Otwórz", command=self.open_text)
        self.filemenu.add_command(label="Zapisz jako", command=self.save_file)
        self.menubar.add_cascade(label="Plik", menu=self.filemenu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="O programie", command=self.info)
        self.menubar.add_cascade(label="Pomoc", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        self.scrollbar = Scrollbar(self.master)
        self.scrollbar.grid(row=0, column=3, sticky=NS)

        self.text_box = Text(root, wrap=WORD,
                             yscrollcommand=self.scrollbar.set,
                             width=int(self.window_width / 6) - 30,
                             height=int(self.window_height / 20) - 2)

        self.scrollbar.config(command=self.text_box.yview)
        self.text_box.grid(row=0, column=0, columnspan=2)
        self.text_box.bind("<Control-Key-a>", self.select_all)
        self.text_box.bind("<Control-Key-A>", self.select_all)

        self.label = Label(root, text='Liczba luk:', font=("Arial", 12))
        self.label.grid(row=1, column=0, columnspan=3, pady=5, padx=30)
        self.entry1 = Entry(root, width=int(self.window_width / 200), font="Arial 11", justify='center')
        self.entry1.grid(row=2, column=0, pady=1, ipady=int(self.window_height / 200))
        self.entry1.insert(1, '10')

        self.run_btn = Button(root, text='Generuj',
                              command=self.run,
                              font=("Arial", 12),
                              width=int(self.window_width / 50),
                              height=int(self.window_height / 300))
        self.run_btn.grid(row=3, column=0, columnspan=3, pady=10)

        self.master.bind('<Configure>', self.resize_text)
        self.master.protocol("WM_DELETE_WINDOW", self.ask_quit)

    def select_all(self):
        self.text_box.tag_add(SEL, "1.0", END)
        self.text_box.mark_set(INSERT, "1.0")
        self.text_box.see(INSERT)
        return 'break'

    def run(self):
        stop_words = get_stop_words('pl')

        content = self.text_box.get(1.0, END)

        splitted = content.split()

        try:
            gap_number = int(self.entry1.get())
        except Exception:
            messagebox.showerror('Błąd', 'Błędna liczba luk!')
            return

        gap_gen = int(self.entry1.get())

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
        self.text_box.delete(1.0, END)
        self.text_box.insert(1.0, joined)
        messagebox.showinfo('Sukces', f'Wygenerowano {gap_gen} luk!')

    def new_text(self):
        choice = messagebox.askquestion('Tworzenie nowego tekstu', 'Czy chcesz utworzyć nowy tekst?')
        if choice == 'yes':
            self.text_box.delete(1.0, END)

    def resize_text(self, event):
        text_width = event.width
        text_height = event.height
        self.text_box.config(width=text_width, height=text_height)

    def open_text(self):
        path = filedialog.askopenfilename(title='Wybierz plik',
                                          filetypes=(("Plik tekstowy", "*.txt"), ("Wszystkie pliki", "*.*")))

        try:
            with open(path, 'r') as file:
                content = file.read()
        except Exception:
            return

        self.text_box.delete(1.0, END)
        self.text_box.insert(1.0, content)

    def ask_quit(self):
        if len(self.text_box.get(1.0, END)) > 1:
            ask = messagebox.askyesno("Wyjście", "Pole tekstowe nie jest puste. Czy na pewno chcesz wyjść?")
            if ask == 1:
                self.master.destroy()
        else:
            self.master.destroy()

    def save_file(self):
        path = filedialog.asksaveasfilename(title='Zapisz plik',
                                            filetypes=(("Plik tekstowy", "*.txt"), ("Wszystkie pliki", "*.*")))

        try:
            with open(path, 'w') as file:
                content = self.text_box.get(1.0, END)
                file.write(content)
            messagebox.showinfo('Sukces', 'Poprawnie zapisano plik!')
        except Exception:
            return

    def info(self):
        info_window = Toplevel(self.master)
        info_window.resizable(False, False)
        info_window.title("O programie")
        Label(info_window, text="Program do generowania luk w tekscie.\nAutor: Robert\nWersja: 2.7").pack()


if __name__ == '__main__':
    root = Tk()
    app = App(root)

    root.mainloop()
