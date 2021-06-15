import random
import tkinter.ttk as ttk
from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox
from tkinter.ttk import Combobox
from tkinter import font
from stop_words import get_stop_words
from tkinter import filedialog
from File_operations import readfile, savefile


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
        self.font = 'Arial'
        self.font_size = 11
        self.color = '#000000'
        self.size_idx = 1
        self.font_idx = 1

        self.menubar = Menu(self.master)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Nowy", command=self.new_text)
        self.filemenu.add_command(label="Otwórz", command=self.open_text)
        self.filemenu.add_command(label="Zapisz jako", command=self.save_file)
        self.menubar.add_cascade(label="Plik", menu=self.filemenu)

        self.option_menu = Menu(self.menubar, tearoff=0)
        self.option_menu.add_command(label="Tekst", command=self.config_text)
        self.option_menu.add_command(label="Wygląd", command=self.config_app)
        self.menubar.add_cascade(label="Opcje", menu=self.option_menu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="O programie", command=self.info)
        self.menubar.add_cascade(label="Pomoc", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        self.scrollbar = ttk.Scrollbar(self.master)
        self.scrollbar.grid(row=0, column=3, sticky=NS)

        self.text_box = Text(root, wrap=WORD,
                             yscrollcommand=self.scrollbar.set,
                             width=int(self.window_width / 6) - 30,
                             height=int(self.window_height / 20) - 2)

        self.scrollbar.config(command=self.text_box.yview)
        self.text_box.grid(row=0, column=0, columnspan=2)
        self.text_box.bind("<Control-Key-a>", self.select_all)
        self.text_box.bind("<Control-Key-A>", self.select_all)

        self.label = ttk.Label(self.master, text='Liczba luk:', font=("Arial", 12))
        self.label.grid(row=1, column=0, columnspan=3, pady=5, padx=30)
        self.entry1 = ttk.Entry(self.master, width=int(self.window_width / 200), font="Arial 11", justify='center')
        self.entry1.grid(row=2, column=0, pady=1, ipady=int(self.window_height / 200))
        self.entry1.insert(1, '10')

        self.run_btn = ttk.Button(self.master, text='Generuj',
                                  style='AccentButton',
                                  command=self.run)
        self.run_btn.grid(row=3, column=0, columnspan=3, pady=10)

        self.master.bind('<Configure>', self.resize_text)
        self.master.protocol("WM_DELETE_WINDOW", self.ask_quit)

    def select_all(self, event):
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
        except ValueError:
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

        idx = 0

        while idx < len(splitted) - 1:
            word = splitted[idx]

            if word == '*':
                splitted.insert(idx, '\n')
                idx += 1

            idx += 1

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
                                          filetypes=(("Plik tekstowy", "*.txt"),
                                                     ("Dokument programu Word 2007-365", "*.docx"),
                                                     ("Wszystkie pliki", "*.*")))
        try:
            if path.split('.')[-1] == 'txt':
                content = readfile.read_txt(path)
            else:
                content = readfile.read_docx(path)
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
                                            filetypes=(("Plik tekstowy", "*.txt"),
                                                       ("Dokument programu Word 2007-365", "*.docx"),
                                                       ("Wszystkie pliki", "*.*")))
        try:
            content = self.text_box.get(1.0, END)
            if path.split('.')[-1] == 'txt':
                savefile.save_txt(path, content)
            else:
                savefile.save_docx(path, content)
            messagebox.showinfo('Sukces', 'Poprawnie zapisano plik!')
        except Exception:
            return

    def info(self):
        InfoWindow(self.master)

    def config_text(self):
        TextWindow(self.master)

    def config_app(self):
        ConfigWindow(self.master)


class TextWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.resizable(False, False)
        self.title("Ustawienia tekstu")
        self.font_size = app.font_size
        self.font = app.font
        self.color = app.color

        Label(self, text="Czcionka:").grid(column=0, row=1, padx=10, pady=5)
        Label(self, text="Rozmiar tekstu:").grid(column=0, row=2, padx=10, pady=5)
        Button(self, text='Kolor', command=self.choose_color).grid(column=2, row=1, rowspan=2, padx=5)

        self.cbox1 = Combobox(self, width=27)
        self.cbox2 = Combobox(self, width=27)

        self.fonts = font.families()
        self.sizes = list(range(8, 72, 3))

        self.cbox1['values'] = self.sizes
        self.cbox2['values'] = self.fonts

        self.cbox1.grid(column=1, row=2)
        self.cbox2.grid(column=1, row=1)

        self.cbox1.current(app.size_idx)
        self.cbox2.current(app.font_idx)

        labelframe = LabelFrame(self, text="Przykładowy tekst")
        labelframe.grid(column=0, row=0, columnspan=3, pady=5)

        self.example = Label(labelframe, text="Ala ma kota.")
        self.example.pack()

        self.cbox1.bind("<<ComboboxSelected>>", self.change_example)
        self.cbox2.bind("<<ComboboxSelected>>", self.change_example)

        ttk.Button(self, text='Zatwierdź', style='AccentButton', command=self.change_font).grid(column=0, row=3,
                                                                                                columnspan=3,
                                                                                                pady=15)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Wybierz kolor")
        self.color = color_code[1]
        self.example.config(fg=self.color)

    def change_example(self, event):
        self.font_size = self.cbox1.get()
        self.font = self.cbox2.get()
        self.example.config(font=(self.font, self.font_size))

    def change_font(self):
        app.text_box.config(font=(self.font, self.font_size), fg=self.color)
        try:
            app.size_idx = self.sizes.index(int(self.font_size))
            app.font_idx = self.fonts.index(self.font)
            app.color = self.color
        except Exception:
            app.size_idx = 1
            app.font_idx = 1
        self.destroy()


class ConfigWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)


class InfoWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.resizable(False, False)
        self.title("O programie")
        version = 3.0
        Label(self, text=f"Program do generowania luk w tekscie.\nAutor: Robert\nWersja: {version}").pack()


if __name__ == '__main__':
    root = Tk()
    root.tk.call('source', 'Azure-ttk-theme/azure-dark.tcl')
    ttk.Style().theme_use('azure-dark')
    app = App(root)
    root.mainloop()
