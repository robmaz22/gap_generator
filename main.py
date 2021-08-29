import json
import random
import tkinter.ttk as ttk
from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
from File_operations import readfile, savefile
from Windows import info

WHITE = "#ffffff"
DARK = "#333333"
BLACK = '#000000'
PUNCTUATION = ('.', ',' ':', ';', '?', '!')


# noinspection PyUnusedLocal
class App:
    stop_words = []

    @classmethod
    def load_stopwords(cls):
        with open('stopwords-pl.json') as f:
            cls.stop_words = json.load(f)

    def __init__(self, master, width, height):
        #####################################################################################################
        # BASIC PARAMETERS
        ####################################################################################################
        self.master = master
        self.master.title('GENERATOR LUK')
        self.master.geometry(f'{width}x{height}')
        Grid.rowconfigure(root, index=0, weight=1)
        Grid.columnconfigure(root, index=0, weight=1)
        self.master.minsize(300, 300)
        self.font = 'Arial'
        self.font_size = 11
        self.color = BLACK
        self.size_idx = 1
        self.font_idx = 1
        self.theme = 'light'
        self.last_text = None

        #####################################################################################################
        # MAIN WINDOW ELEMENTS
        ####################################################################################################
        self.label = ttk.Label(self.master, text='Liczba luk:', font=("Arial", 12))
        self.label.grid(row=1, column=0, columnspan=3, pady=5, padx=30)
        self.entry1 = ttk.Entry(self.master, width=int(width / 200), font="Arial 11", justify='center')
        self.entry1.grid(row=2, column=0, pady=1, ipady=int(height / 200))
        self.entry1.insert(1, '10')

        self.run_btn = ttk.Button(self.master, text='Generuj', style='AccentButton',
                                  command=self.run, )
        self.run_btn.grid(row=3, column=0, columnspan=3, pady=10)

        self.master.bind('<Configure>', self.resize_textbox)
        self.master.protocol("WM_DELETE_WINDOW", self.ask_quit)

        self.scrollbar = ttk.Scrollbar(self.master)

        self.text_box = Text(root, wrap=WORD,
                             yscrollcommand=self.scrollbar.set,
                             width=int(width / 6) - 30,
                             height=int(height / 20) - 2,
                             undo=True)

        self.scrollbar.grid(row=0, column=3, sticky=NS)

        self.scrollbar.config(command=self.text_box.yview)
        self.text_box.grid(row=0, column=0, columnspan=2)

        self.text_box.bind("<Control-Key-a>", self.select_all)
        self.text_box.bind("<Control-Key-A>", self.select_all)
        self.text_box.bind("<Control-Key-n>", self.new_text)
        self.text_box.bind("<Control-Key-o>", self.open_text)
        self.text_box.bind("<Control-Key-s>", self.save_file)
        self.text_box.bind("<Control-Key-d>", self.clear_all)

        #####################################################################################################
        # MENUBAR
        ####################################################################################################
        self.menubar = Menu(self.master, background='white', fg=BLACK)
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label="Nowy", command=self.new_text, accelerator="Ctrl+N")
        self.filemenu.add_command(label="Otwórz", command=self.open_text, accelerator="Ctrl+O")
        self.filemenu.add_command(label="Zapisz jako", command=self.save_file, accelerator="Ctrl+S")
        self.menubar.add_cascade(label="Plik", menu=self.filemenu)

        self.edit_menu = Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label='Cofnij', command=self.text_box.edit_undo, accelerator="Ctrl+Z")
        self.edit_menu.add_command(label='Powtórz', command=self.text_box.edit_redo, accelerator="Ctrl+Y")
        self.edit_menu.add_command(label='Zaznacz wszystko', command=self.select_all, accelerator="Ctrl+A")
        self.edit_menu.add_command(label='Wyczyść wszystko', command=self.clear_all, accelerator="Ctrl+D")
        self.menubar.add_cascade(label="Edycja", menu=self.edit_menu)

        self.option_menu = Menu(self.menubar, tearoff=0)
        self.option_menu.add_command(label="Preferencje", command=self.config_app)
        self.option_menu.add_command(label="Ustawienia tekstu", command=self.config_text)
        self.option_menu.add_checkbutton(label="Tryb ciemny", command=self.change_theme)
        self.menubar.add_cascade(label="Opcje", menu=self.option_menu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="O programie", command=self.info)
        self.menubar.add_cascade(label="Pomoc", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        #####################################################################################################
        # MAIN FUNCTIONS
        ####################################################################################################

    def change_theme(self):
        if self.theme == 'dark':
            self.master.tk_setPalette(WHITE)
            ttk.Style().theme_use('azure')
            self.theme = 'light'
        else:
            root.tk_setPalette(DARK)
            ttk.Style().theme_use('azure-dark')
            self.theme = 'dark'

    def info(self):
        info.InfoWindow(self.master, self.theme)

    def config_text(self):
        ConfigText(self.master)

    def config_app(self):
        ConfigApp(self.master)

    def ask_quit(self):
        if len(self.text_box.get(1.0, END)) > 1:
            ask = messagebox.askyesno("Wyjście", "Pole tekstowe nie jest puste. Czy na pewno chcesz wyjść?")
            if ask == 1:
                self.master.destroy()
        else:
            self.master.destroy()

    def resize_textbox(self, event=None):
        text_width = event.width
        text_height = event.height
        self.text_box.config(width=text_width, height=text_height)

    def run(self):
        self.last_text = self.text_box.get(1.0, END)

        content = self.text_box.get(1.0, END)
        splited = content.split(' ')

        if '.........' in splited:
            messagebox.showwarning('Ostrzeżenie', 'W podanym tekscie zostały już wygenerowane luki!')
            answer = messagebox.askyesno('Pytanie', 'Kontynuować?')
            if not answer:
                return

        try:
            gap_number = int(self.entry1.get())
        except ValueError:
            messagebox.showerror('Błąd', 'Podana wartość musi być liczbą całkowitą!')
            return

        if gap_number >= len(splited) or gap_number <= 0:
            messagebox.showerror('Błąd', 'Błędna liczba luk!')
            return

        gap_indexes = []

        if (len(splited) % 2 == 0 and len(splited) / 2 >= gap_number) or (
                len(splited) + 1 % 2 == 0 and len(splited) + 1 / 2 >= gap_number):
            while len(set(gap_indexes)) < gap_number:
                idx = random.randint(0, len(splited) - 1)

                if idx - 1 not in gap_indexes and idx + 1 not in gap_indexes:
                    word = splited[idx]
                    for char in PUNCTUATION:
                        word = word.replace(char, '')
                    word = word.lower()

                    if word not in self.stop_words:
                        gap_indexes.append(idx)
        else:
            while len(set(gap_indexes)) < gap_number:
                idx = random.randint(0, len(splited) - 1)

                word = splited[idx]
                for char in PUNCTUATION:
                    word = word.replace(char, '')
                word = word.lower()

                if word not in self.stop_words:
                    gap_indexes.append(idx)

        for idx in set(gap_indexes):
            if splited[idx][-1] == '\n':
                if splited[idx][-2] in PUNCTUATION:
                    splited[idx] = f'........ {splited[idx][-2]}\n'
                else:
                    splited[idx] = f'........\n'
            elif splited[idx][-1] in PUNCTUATION:
                if splited[idx][-1] == PUNCTUATION[0]:
                    splited[idx] = '........ .'
                else:
                    splited[idx] = f'........{splited[idx][-1]}'
            else:
                splited[idx] = '.........'

        joined = ' '.join(splited)
        self.text_box.delete(1.0, END)
        self.text_box.insert(1.0, joined)

        if gap_number == 1:
            messagebox.showinfo('Sukces', f'Wygenerowano {gap_number} lukę!')
        elif gap_number in [2, 3, 4]:
            messagebox.showinfo('Sukces', f'Wygenerowano {gap_number} luki!')
        else:
            messagebox.showinfo('Sukces', f'Wygenerowano {gap_number} luk!')

    #####################################################################################################
    # EDIT FUNCTIONS
    ####################################################################################################
    def select_all(self, event=None):
        self.last_text = self.text_box.get(1.0, END)
        self.text_box.tag_add(SEL, "1.0", END)
        self.text_box.mark_set(INSERT, "1.0")
        self.text_box.see(INSERT)
        return 'break'

    def clear_all(self, event=None):
        self.text_box.delete(1.0, END)

    #####################################################################################################
    # FILE FUNCTIONS
    ####################################################################################################
    def new_text(self, event=None):
        self.last_text = self.text_box.get(1.0, END)
        choice = messagebox.askquestion('Tworzenie nowego tekstu', 'Czy chcesz utworzyć nowy tekst?')
        if choice == 'yes':
            self.text_box.delete(1.0, END)

    def open_text(self, event=None):
        self.last_text = self.text_box.get(1.0, END)
        path = filedialog.askopenfilename(title='Wybierz plik',
                                          filetypes=(("Plik tekstowy", "*.txt"),
                                                     ("Dokument programu Word 2007-365", "*.docx"),
                                                     ("Wszystkie pliki", "*.*")))
        try:
            if path.split('.')[-1] == 'txt':
                content = readfile.read_txt(path)
            else:
                content = readfile.read_docx(path)
        except UnboundLocalError:
            return
        except AttributeError:
            return

        self.text_box.delete(1.0, END)
        self.text_box.insert(1.0, content)

    def save_file(self, event=None):
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
        except AttributeError:
            return


# noinspection PyUnusedLocal
class ConfigText(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.resizable(False, False)
        self.title("Ustawienia tekstu")
        self.font_size = app.font_size
        self.font = app.font
        self.color = app.color

        ttk.Label(self, text="Czcionka:").grid(column=0, row=1, padx=10, pady=5)
        ttk.Label(self, text="Rozmiar tekstu:").grid(column=0, row=2, padx=10, pady=5)
        ttk.Button(self, text='Kolor', command=self.choose_color).grid(column=2, row=1, rowspan=2, padx=5)

        self.cbox1 = ttk.Combobox(self, width=27)
        self.cbox2 = ttk.Combobox(self, width=27)

        self.fonts = font.families()
        self.sizes = list(range(8, 72, 3))

        self.cbox1['values'] = self.sizes
        self.cbox2['values'] = self.fonts

        self.cbox1.grid(column=1, row=2)
        self.cbox2.grid(column=1, row=1)

        self.cbox1.current(app.size_idx)
        self.cbox2.current(app.font_idx)

        labelframe = ttk.LabelFrame(self, text="Przykładowy tekst")
        labelframe.grid(column=0, row=0, columnspan=3, pady=5)

        self.example = ttk.Label(labelframe, text="Ala ma kota.")
        self.example.pack()

        self.cbox1.bind("<<ComboboxSelected>>", self.change_example)
        self.cbox2.bind("<<ComboboxSelected>>", self.change_example)

        ttk.Button(self, text='Zatwierdź', style='AccentButton', command=self.change_font).grid(column=0,
                                                                                                row=3,
                                                                                                columnspan=3,
                                                                                                pady=15)

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Wybierz kolor")
        self.color = color_code[1]
        self.example.configure(foreground=self.color)

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
        except ValueError:
            app.size_idx = 1
            app.font_idx = 1
        self.destroy()


# noinspection PyUnusedLocal
class ConfigApp(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.resizable(False, False)
        self.title("Preferencje")
        # TODO zmiana motywów
        # TODO zmiana motywu luk
        # TODO Wyświetlanie usuniętych wyrazów
        # TODO Liczba liter w usuniętym wyrazie


if __name__ == '__main__':
    App.load_stopwords()
    root = Tk()

    root.tk.call("source", "Azure-ttk-theme/azure.tcl")
    root.tk.call("source", "Azure-ttk-theme/azure-dark.tcl")
    root.tk_setPalette(WHITE)
    ttk.Style().theme_use('azure')

    window_width = int((root.winfo_screenwidth() / 2))
    window_height = int((root.winfo_screenheight() / 2) + 200)
    app = App(root, window_width, window_height)

    root.mainloop()
