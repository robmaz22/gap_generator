from ctypes import windll
import os
import json
import random

import tkinter.ttk as ttk
from tkinter import *
from tkinter import colorchooser
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog

from files import readfile, savefile
from windows import info

# basic parameters
WHITE = "#ffffff"
DARK = "#333333"
BLACK = '#000000'
PUNCTUATION = ('.', ',' ':', ';', '?', '!')


# noinspection PyUnusedLocal
class App:
    stop_words = []

    # Loading stopwords from json file
    @classmethod
    def load_stopwords(cls):
        with open('stopwords-pl.json') as f:
            cls.stop_words = json.load(f)

    def __init__(self, master, width, height):
        #####################################################################################################
        # BASIC APP PROPERTIES
        ####################################################################################################
        self.master = master
        self.master.title('GENERATOR LUK')
        self.master.geometry(f'{width}x{height}+{width // 2}+100')
        Grid.rowconfigure(root, index=0, weight=1)
        Grid.columnconfigure(root, index=0, weight=1)
        self.master.minsize(300, 300)
        self.font = 'Arial'
        self.font_size = 11
        self.size_idx = 1
        self.font_idx = 1
        self.theme = 'light'
        self.color = None
        self.last_text = None

        #####################################################################################################
        # MAIN WINDOW ELEMENTS
        ####################################################################################################
        self.words_label = ttk.Label(self.master, text='Liczba wyrazów: 0', font=("Arial", 10))
        self.words_label.grid(row=1, column=0, columnspan=3, pady=5, padx=5, sticky=W)
        self.label = ttk.Label(self.master, text='Liczba luk:', font=("Arial", 12))
        self.label.grid(row=2, column=0, columnspan=3, pady=5, padx=30)
        self.entry1 = ttk.Entry(self.master, width=int(width / 200), font="Arial 11", justify='center')
        self.entry1.grid(row=3, column=0, pady=1, ipady=int(height / 200))
        self.entry1.insert(1, '10')

        self.run_btn = ttk.Button(self.master, text='Generuj', style='AccentButton', width=window_width // 60,
                                  command=self.generate)
        self.run_btn.grid(row=4,
                          column=0,
                          columnspan=3,
                          pady=10)

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
        self.text_box.bind('<KeyRelease>', self.key_press)
        self.text_box.focus()

        #####################################################################################################
        # MENUBAR
        ####################################################################################################
        self.menubar = Menu(self.master)
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

    # Counting number of words in the text box
    def key_press(self, event=None):
        words = self.text_box.get("1.0", "end-1c")
        number = words.split()
        self.words_label.config(text=f'Liczba wyrazów: {len(number)}')

    # Changing app theme
    def change_theme(self):
        if self.theme == 'dark':
            self.master.tk_setPalette(WHITE)
            ttk.Style().theme_use('azure')
            self.theme = 'light'
        else:
            root.tk_setPalette(DARK)
            ttk.Style().theme_use('azure-dark')
            self.theme = 'dark'

    # Showing info window
    def info(self):
        info.InfoWindow(self.master, self.theme)

    # Showing text preferences window
    def config_text(self):
        ConfigText(self.master)

    # showing app preferences window
    def config_app(self):
        ConfigApp(self.master)

    # closing app
    def ask_quit(self):
        if len(self.text_box.get(1.0, END)) > 1:
            ask = messagebox.askyesno("Wyjście", "Pole tekstowe nie jest puste. Czy na pewno chcesz wyjść?")
            if ask == 1:
                self.master.destroy()
        else:
            self.master.destroy()

    # resizing textbox if window size changed
    def resize_textbox(self, event=None):
        text_width = event.width
        text_height = event.height
        self.text_box.config(width=text_width, height=text_height)

    # generating gaps in text
    def generate(self):

        # reading text from textbox
        content = self.text_box.get(1.0, END)
        splited = content.split(' ')

        if '.........' in splited:
            messagebox.showwarning('Ostrzeżenie', 'W podanym tekscie zostały już wygenerowane luki!')
            answer = messagebox.askyesno('Pytanie', 'Kontynuować?')
            if not answer:
                return

        self.last_text = self.text_box.get(1.0, END)

        # reading number of gaps input
        try:
            gap_number = int(self.entry1.get())
        except ValueError:
            messagebox.showerror('Błąd', 'Podana wartość musi być liczbą całkowitą!')
            return

        if gap_number >= len(splited) or gap_number <= 0:
            messagebox.showerror('Błąd', 'Błędna liczba luk!')
            return

        # showing progress
        popup = Toplevel()
        popup.title('')
        popup.geometry(f'+{window_width - 50}+{window_height - 300}')

        popup.overrideredirect(1)

        popup.resizable(False, False)
        Label(popup, text="Generowanie...").grid(row=0, column=0, padx=5, pady=5)

        cycle = gap_number * 10
        counter = 0
        last_status = None
        step = 100 / gap_number
        progress = 0
        progress_var = DoubleVar()
        progress_bar = ttk.Progressbar(popup, variable=progress_var, maximum=100)
        progress_bar.grid(row=1, column=0)
        popup.pack_slaves()

        indices_left = list(range(len(splited)))
        gap_indices = []

        # If it is possible to put a gap between each word
        if (len(splited) % 2 == 0 and len(splited) / 2 >= gap_number) or (
                len(splited) + 1 % 2 == 0 and len(splited) + 1 / 2 >= gap_number):
            while len(gap_indices) < gap_number:
                popup.update()
                idx = random.choice(indices_left)

                if idx - 1 not in gap_indices and idx + 1 not in gap_indices:
                    word = splited[idx]
                    for char in PUNCTUATION:
                        word = word.replace(char, '')
                    word = word.lower()

                    if word not in self.stop_words and len(word) >= 2:
                        gap_indices.append(idx)
                        indices_left.remove(idx)
                        progress += step
                        progress_var.set(int(progress))
                        counter += 1

                    if counter == last_status:
                        cycle -= 1
                    else:
                        last_status = counter

                    # Progress freeze
                    if cycle == 0:
                        self.entry1.delete(1.0, END)
                        self.entry1.insert(1.0, counter)
                        messagebox.showwarning("Ostrzeżenie",
                                               f"W podanym tekście nie udało się wygenerować wszystkich luk (Możliwa "
                                               f"ilość: {counter})")
                        answer = messagebox.askyesno('Pytanie', 'Czy chcesz kontynuować?')
                        if answer == 0:
                            popup.destroy()
                            return
                        else:
                            progress_var.set(100)
                            gap_number = counter
        else:
            while len(gap_indices) < gap_number:
                popup.update()
                idx = random.choice(indices_left)

                word = splited[idx]
                for char in PUNCTUATION:
                    word = word.replace(char, '')
                word = word.lower()

                if word not in self.stop_words and len(word) >= 2:
                    gap_indices.append(idx)
                    indices_left.remove(idx)
                    progress += step
                    progress_var.set(int(progress))
                    counter += 1

                if counter == last_status:
                    cycle -= 1
                else:
                    last_status = counter

                if cycle == 0:
                    self.entry1.delete(0, END)
                    self.entry1.insert(1, counter)
                    messagebox.showwarning("Ostrzeżenie",
                                           f"W podanym tekście nie udało się wygenerować wszystkich luk (Możliwa ilość: {counter})")
                    answer = messagebox.askyesno('Pytanie', 'Czy chcesz kontynuować?')
                    if answer == 0:
                        popup.destroy()
                        return
                    else:
                        progress_var.set(100)
                        gap_number = counter

        for idx in gap_indices:
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

        popup.destroy()

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
            self.key_press()

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
        self.key_press()

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
        self.sizes = list(range(9, 72, 2))

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
        self.attributes('-topmost', True)
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

    # if running on windows
    if os.name == 'nt':
        windll.shcore.SetProcessDpiAwareness(1)

    App.load_stopwords()
    root = Tk()

    # Loading theme
    root.tk.call("source", "Azure-ttk-theme/azure.tcl")
    root.tk.call("source", "Azure-ttk-theme/azure-dark.tcl")
    root.tk_setPalette(WHITE)
    ttk.Style().theme_use('azure')

    # Screen size
    window_width = root.winfo_screenwidth() // 2
    window_height = root.winfo_screenheight() // 2 + 200
    app = App(root, window_width, window_height)

    root.mainloop()
