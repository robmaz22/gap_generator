from tkinter import *
import tkinter.ttk as ttk


class RemovedWords(Toplevel):
    def __init__(self, parent, words_list):
        super().__init__(parent)
        self.iconbitmap('icon.ico')
        self.resizable(False, True)
        self.title("Usunięte wyrazy")
        self.geometry('330x250')
        self.words_list = words_list

        self.scrollbar = ttk.Scrollbar(self, orient="vertical")
        self.lb = Listbox(self, width=35, yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.lb.yview)

        for i, w in enumerate(self.words_list):
            self.lb.insert(i + 1, w)

        self.lb.pack(side='left', fill='y', expand=True)
        self.scrollbar.pack(side='right', fill='y')

if __name__ == '__main__':
    root = Tk()
    words_list = ['word1', 'word2', 'word3']
    RemovedWords(root, words_list)
    root.mainloop()