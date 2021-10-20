from ctypes import windll
import os
import json
import random

import tkinter.ttk as ttk
from configparser import ConfigParser
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from files import readfile, savefile
from windows import config_window, removed_words, info

# basic parameters
WHITE = "#ffffff"
DARK = "#333333"
BLACK = '#000000'
PUNCTUATION = ('.', ',' ':', ';', '?', '!')


# noinspection PyUnusedLocal
class App:
    parser = None
    stop_words = []

    # Loading stopwords from json file
    @classmethod
    def load_stopwords(cls):
        with open('stopwords-pl.json') as f:
            cls.stop_words = json.load(f)

    @classmethod
    def load_config(cls):
        cls.parser = ConfigParser()
        cls.parser.read('config.ini')

    def __init__(self, master, width, height):
        #####################################################################################################
        # BASIC APP PROPERTIES
        ####################################################################################################
        self.master = master
        self.master.title('GENERATOR LUK')
        self.master.iconbitmap('icon.ico')
        self.master.geometry(f'{width}x{height}+{width // 2}+100')
        Grid.rowconfigure(root, index=0, weight=1)
        Grid.columnconfigure(root, index=0, weight=1)
        self.master.minsize(300, 300)
        self.last_text = None
        self.generated = False

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

        self.run_btn = ttk.Button(self.master, text='Generuj', style='Accent.TButton', width=screen_width // 60,
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
        self.menubar.add_cascade(label="Opcje", menu=self.option_menu)

        self.helpmenu = Menu(self.menubar, tearoff=0)
        self.helpmenu.add_command(label="O programie", command=self.info)
        self.menubar.add_cascade(label="Pomoc", menu=self.helpmenu)

        self.master.config(menu=self.menubar)

        self.set_config()
        #####################################################################################################
        # MAIN FUNCTIONS
        ####################################################################################################

    # set app params
    def set_config(self):
        self.font = self.parser['text']['font']
        self.font_size = self.parser['text']['font_size']
        self.theme = self.parser['main']['theme_mode']
        self.color = self.parser['text']['color']
        self.gap_style = self.parser['main']['gap_style']
        if self.gap_style == '_':
            self.gap_style = self.gap_style + ' '
        self.char_number = self.parser['main']['char_number']
        self.removed_words = int(self.parser['main']['removed_words'])

        self.text_box.config(font=(self.font, self.font_size), fg=self.color)
        self.change_theme()

    # Counting number of words in the text box
    def key_press(self, event=None):
        words = self.text_box.get("1.0", "end-1c")
        number = words.split()
        if len(number) == 0:
            self.generated = False
        self.words_label.config(text=f'Liczba wyrazów: {len(number)}')

    # Changing app theme
    def change_theme(self):
        if self.theme == 'light':
            self.master.tk_setPalette(WHITE)
            self.master.tk.call("set_theme", "light")
            self.theme = 'dark'
        else:
            root.tk_setPalette(DARK)
            self.master.tk.call("set_theme", "dark")
            self.theme = 'light'

    # Showing info window
    def info(self):
        info.InfoWindow(self.master, self.theme, (screen_width, screen_height))

    # showing app preferences window
    def config_app(self):
        top = config_window.ConfigApp(self.master, self.theme, (screen_width, screen_height))
        self.master.wait_window(top)
        self.load_config()
        self.set_config()

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

        # removed words
        removed_list = []

        # reading text from textbox and save last status
        self.last_text = self.text_box.get(1.0, END)
        content = self.last_text.split(' ')

        # if gaps exist
        if self.generated:
            messagebox.showwarning('Ostrzeżenie', 'W podanym tekscie zostały już wygenerowane luki!')
            answer = messagebox.askyesno('Pytanie', 'Kontynuować?')
            if not answer:
                return

        # reading number of gaps input
        try:
            gap_number = int(self.entry1.get())
        except ValueError:
            messagebox.showerror('Błąd', 'Podana wartość musi być liczbą całkowitą!')
            return

        if gap_number >= len(content) or gap_number <= 0:
            messagebox.showerror('Błąd', 'Błędna liczba luk!')
            return

        # showing progress
        popup = Toplevel()
        popup.title('')
        popup.geometry(f'+{screen_width - 50}+{screen_height - 300}')

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

        indices_left = list(range(len(content)))
        gap_indices = []

        # If it is possible to put a gap between each word
        if (len(content) % 2 == 0 and len(content) / 2 >= gap_number) or (
                len(content) + 1 % 2 == 0 and len(content) + 1 / 2 >= gap_number):
            while len(gap_indices) < gap_number:
                popup.update()
                idx = random.choice(indices_left)

                if len(content[idx]) <= 2 or not (c.isalpha() for c in content[idx]):
                    continue

                if idx - 1 not in gap_indices and idx + 1 not in gap_indices:
                    word = content[idx].lower()
                    if word[-1] in PUNCTUATION:
                        word = word[:-1]

                    if word not in self.stop_words:
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
                        self.entry1.delete(0, END)
                        self.entry1.insert(0, counter)
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

                if len(content[idx]) <= 2 or not (c.isalpha() for c in content[idx]):
                    continue
                word = content[idx].lower()

                if word[-1] in PUNCTUATION:
                    word = word[:-1]

                if word not in self.stop_words:
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

        # replace words
        for idx in sorted(gap_indices):
            word = content[idx].replace('\n', '').replace('.', '').replace(',', '')
            # show nr of chars in removed word
            if self.char_number:
                char_nr = len(word)
            else:
                char_nr = 8

            if self.removed_words:
                removed_list.append(word)

            if content[idx][-1] == '\n':
                if content[idx][-2] in PUNCTUATION:
                    content[idx] = f'{self.gap_style * char_nr} {content[idx][-2]}\n'
                else:
                    content[idx] = f'{self.gap_style * char_nr}\n'
            elif content[idx][-1] in PUNCTUATION:
                if content[idx][-1] == PUNCTUATION[0]:
                    content[idx] = f'{self.gap_style * char_nr} .'
                else:
                    content[idx] = f'{self.gap_style * char_nr}{content[idx][-1]}'
            else:
                content[idx] = self.gap_style * char_nr

        joined = ' '.join(content)
        self.text_box.delete(1.0, END)
        self.text_box.insert(1.0, joined)

        popup.destroy()

        # show removed words
        if self.removed_words:
            removed_words.RemovedWords(self.master, removed_list)

        self.generated = True

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
        self.generated = False

    #####################################################################################################
    # FILE FUNCTIONS
    ####################################################################################################
    def new_text(self, event=None):
        self.generated = False
        self.last_text = self.text_box.get(1.0, END)
        choice = messagebox.askquestion('Tworzenie nowego tekstu', 'Czy chcesz utworzyć nowy tekst?')
        if choice == 'yes':
            self.text_box.delete(1.0, END)
            self.key_press()

    def open_text(self, event=None):
        self.generated = False
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


if __name__ == '__main__':

    # if running on Windows
    if os.name == 'nt':
        windll.shcore.SetProcessDpiAwareness(1)

    App.load_stopwords()
    App.load_config()
    root = Tk()

    # Loading theme
    root.tk.call("source", "Azure-ttk-theme/azure.tcl")
    # root.tk.call("source", "Azure-ttk-theme/azure-dark.tcl")
    root.tk_setPalette(WHITE)
    root.tk.call("set_theme", "light")

    # Screen size
    screen_width = root.winfo_screenwidth() // 2
    screen_height = root.winfo_screenheight() // 2 + 200
    app = App(root, screen_width, screen_height)

    root.mainloop()
