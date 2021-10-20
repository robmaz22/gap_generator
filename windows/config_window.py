from tkinter import *
import tkinter.ttk as ttk
from tkinter import font
from tkinter import colorchooser
from configparser import ConfigParser

LANGUAGES = ['Polski']
THEMES = ['Azure']
GAP_STYLE = ['_', '.']

DEFAULT = """[main]
language = Polski
theme_mode = light
theme = Azure
gap_style = _
char_number = 1
removed_words = 1

[text]
font = Calibri
font_size = 11
color = #000000
size_idx = 1
font_idx = 32"""


# noinspection PyUnusedLocal
class ConfigApp(Toplevel):
    def __init__(self, parent, theme=None, position=(250, 400), config_file='config.ini'):
        super().__init__(parent)
        self.iconbitmap('icon.ico')
        self.resizable(False, False)
        self.title("Preferencje")
        self.geometry(f'+{position[0] - 250}+{position[1] - 400}')

        self.parser = ConfigParser()
        self.parser.read(config_file)

        self.tabControl = ttk.Notebook(self)

        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)

        self.tabControl.add(self.tab1, text='Ogólne')
        self.tabControl.add(self.tab2, text='Tekst')
        self.tabControl.pack(expand=1, fill="both")

        # main tab
        ##############################################################################################
        ttk.Label(self.tab1, text='Język').grid(row=0, column=0, pady=2)
        ttk.Label(self.tab1, text='Tryb ciemny').grid(row=1, column=0, pady=2)
        ttk.Label(self.tab1, text='Motyw').grid(row=2, column=0, pady=2)
        ttk.Label(self.tab1, text='Styl luk').grid(row=3, column=0, pady=2)
        ttk.Label(self.tab1, text='Uwzględniaj ilość znaków').grid(row=4, column=0, pady=2)
        ttk.Label(self.tab1, text='Pokazuj usunięte wyrazy').grid(row=5, column=0, pady=2)

        self.language_cbox = ttk.Combobox(self.tab1, state='readonly')
        self.language_cbox['values'] = LANGUAGES
        self.language_cbox.grid(row=0, column=1, pady=2)
        lang_idx = LANGUAGES.index(self.parser['main']['language'])
        self.language_cbox.current(lang_idx)
        self.language_cbox.bind('<<ComboboxSelected>>', self.any_modification)

        self.theme_mode_var = StringVar()
        self.theme_mode_var.set(self.parser['main']['theme_mode'])
        self.theme_mode_var.trace_add('write', self.any_modification)
        self.theme_mode_switch = ttk.Checkbutton(self.tab1,
                                                 style='Switch.TCheckbutton',
                                                 onvalue='dark',
                                                 offvalue='light',
                                                 variable=self.theme_mode_var)
        self.theme_mode_switch.grid(row=1, column=1, pady=2)

        self.themes_cbox = ttk.Combobox(self.tab1, state='readonly')
        self.themes_cbox['values'] = THEMES
        self.themes_cbox.grid(row=2, column=1, pady=2)
        themes_idx = THEMES.index(self.parser['main']['theme'])
        self.themes_cbox.current(themes_idx)
        self.themes_cbox.bind('<<ComboboxSelected>>', self.any_modification)

        self.style_cbox = ttk.Combobox(self.tab1, state='readonly')
        self.style_cbox['values'] = GAP_STYLE
        self.style_cbox.grid(row=3, column=1, pady=2)
        style_idx = GAP_STYLE.index(self.parser['main']['gap_style'])
        self.style_cbox.current(style_idx)
        self.style_cbox.bind('<<ComboboxSelected>>', self.any_modification)

        self.nr_var = IntVar()
        self.nr_var.set(int(self.parser['main']['char_number']))
        self.nr_var.trace_add('write', self.any_modification)
        self.theme_switch = ttk.Checkbutton(self.tab1,
                                            style='Switch.TCheckbutton',
                                            onvalue=1,
                                            offvalue=0,
                                            variable=self.nr_var)
        self.theme_switch.grid(row=4, column=1, pady=2)

        self.remove_var = IntVar()
        self.remove_var.set(int(self.parser['main']['removed_words']))
        self.remove_var.trace_add('write', self.any_modification)
        self.theme_switch = ttk.Checkbutton(self.tab1,
                                            style='Switch.TCheckbutton',
                                            onvalue=1,
                                            offvalue=0,
                                            variable=self.remove_var)
        self.theme_switch.grid(row=5, column=1, pady=2)

        # text tab
        ###############################################################################################
        self.font_size = self.parser['text']['font_size']
        self.font = self.parser['text']['font']
        self.color = self.parser['text']['color']
        self.size_idx = self.parser['text']['size_idx']
        self.font_idx = self.parser['text']['font_idx']

        ttk.Label(self.tab2, text="Czcionka:").grid(column=0, row=1, padx=(20, 10), pady=7)
        ttk.Label(self.tab2, text="Rozmiar tekstu:").grid(column=0, row=2, padx=(20, 10), pady=7)
        ttk.Label(self.tab2, text="Kolor:").grid(column=0, row=3, padx=(20, 10), pady=7)
        ttk.Button(self.tab2, text='Wybierz', command=self.choose_color).grid(column=1, row=3, pady=3, padx=2, sticky=W)

        self.fonts_cbox = ttk.Combobox(self.tab2)
        self.sizes_cbox = ttk.Combobox(self.tab2)

        self.fonts = font.families()
        self.sizes = list(range(9, 72, 2))

        self.fonts_cbox['values'] = self.sizes
        self.sizes_cbox['values'] = self.fonts

        self.fonts_cbox.grid(column=1, row=2, pady=7)
        self.sizes_cbox.grid(column=1, row=1, pady=1)

        self.fonts_cbox.current(self.size_idx)
        self.sizes_cbox.current(self.font_idx)

        labelframe = ttk.LabelFrame(self.tab2, text="Przykładowy tekst")
        labelframe.grid(column=0, row=0, columnspan=2, pady=5, padx=(30, 0))

        self.example = ttk.Label(labelframe, text="Ala ma kota.",
                                 foreground=self.color,
                                 font=(self.font, self.font_size))
        self.example.pack()

        self.fonts_cbox.bind("<<ComboboxSelected>>", self.change_example)
        self.sizes_cbox.bind("<<ComboboxSelected>>", self.change_example)
        #############################################################################################################

        button_frame = Frame(self)
        button_frame.pack(expand=1, fill='both', pady=15)

        button_frame.grid_rowconfigure(0, weight=1)
        button_frame.grid_columnconfigure(0, weight=1)
        button_frame.grid_columnconfigure(1, weight=1)

        self.reset_button = ttk.Button(button_frame, text='Ustawienia domyślne', command=self.reset)
        self.reset_button.grid(column=0, row=0, columnspan=2, pady=(2, 15))
        self.accept_button = ttk.Button(button_frame, text='Zatwierdź', command=self.accept,
                                        state=DISABLED)
        self.accept_button.grid(row=1, column=0, sticky=E, padx=2)
        self.ok_button = ttk.Button(button_frame, text='Ok', command=self.ok, state=DISABLED)
        self.ok_button.grid(row=1, column=1, sticky=W, padx=2)

    # if any variable changed
    def any_modification(self, var=None, idx=None, mode=None):
        self.accept_button.configure(state=NORMAL, style='Accent.TButton')

    def choose_color(self):
        color_code = colorchooser.askcolor(title="Wybierz kolor")
        self.attributes('-topmost', True)
        self.color = color_code[1]
        self.example.configure(foreground=self.color)
        self.any_modification()

    def change_example(self, event):
        self.font_size = self.fonts_cbox.get()
        self.font = self.sizes_cbox.get()
        self.example.config(font=(self.font, self.font_size))
        self.any_modification()

    # save config file
    def accept(self):

        self.ok_button.configure(state=ACTIVE, style='Accent.TButton')

        with open('config.ini', 'w') as f:
            self.parser.set('main', 'language', self.language_cbox.get())
            self.parser.set('main', 'theme_mode', self.theme_mode_var.get())
            self.parser.set('main', 'theme', self.themes_cbox.get())
            self.parser.set('main', 'gap_style', self.style_cbox.get())
            self.parser.set('main', 'char_number', str(self.nr_var.get()))
            self.parser.set('main', 'removed_words', str(self.remove_var.get()))

            self.parser.set('text', 'font', self.font)
            self.parser.set('text', 'font_size', self.font_size)
            self.parser.set('text', 'color', self.color)
            try:
                size_idx = self.sizes.index(int(self.font_size))
                font_idx = self.fonts.index(self.font)
            except ValueError:
                size_idx = 1
                font_idx = 1
            self.parser.set('text', 'size_idx', str(size_idx))
            self.parser.set('text', 'font_idx', str(font_idx))

            self.parser.write(f)

    def ok(self):
        self.destroy()

    def reset(self):
        with open('config.ini', 'w') as file:
            file.write(DEFAULT)

        self.ok()


if __name__ == '__main__':
    file = '../config.ini'
    root = Tk()
    ConfigApp(parent=root, config_file=file)

    root.mainloop()
