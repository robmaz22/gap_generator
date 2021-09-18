import webbrowser
from tkinter import *

#Basics parameters for window
VERSION = 1.0
LIGHT_GREY = "#bbbbbf"
DARK_THEME_BLUE = "#4c4cff"


class InfoWindow(Toplevel):
    def __init__(self, parent, theme):
        super().__init__(parent)
        self.resizable(False, False)
        self.title("O programie")
        Label(self, text=f'GENERATOR LUK {VERSION}', font='Helvetica 18 bold').pack(pady=(10, 5), padx=5)
        Label(self, text='Program do generowania luk w tekscie.').pack(pady=5, padx=5)

        #checking main window theme
        if theme == 'light':
            Label(self, text='Autor: Robert\n2021', font='Arial 9', fg='grey').pack(pady=(5, 5), padx=5)
            Label(self, text='Wykorzystane motywy:', font='Arial 9', fg='grey').pack(pady=(4, 0), padx=5)
            link = Label(self, text='https://github.com/rdbende/Azure-ttk-theme',
                         font='Arial 9',
                         fg="blue",
                         cursor="hand2")
        else:
            Label(self, text='Autor: Robert\n2021', font='Arial 9', fg=LIGHT_GREY).pack(pady=(5, 5), padx=5)
            Label(self, text='Wykorzystane motywy:', font='Arial 9', fg=LIGHT_GREY).pack(pady=(4, 0), padx=5)
            link = Label(self, text='https://github.com/rdbende/Azure-ttk-theme',
                         font='Arial 9',
                         fg=DARK_THEME_BLUE,
                         cursor="hand2")

        link.pack(pady=(0, 5), padx=5)
        link.bind("<Button-1>", lambda callback: self.callback('https://github.com/rdbende/Azure-ttk-theme'))

    #opening url in webbrowser
    @staticmethod
    def callback(url):
        webbrowser.open_new_tab(url)