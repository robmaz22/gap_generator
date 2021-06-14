import docx


def save_txt(path, content):
    """
    Funkcja zapisująca przekazaną zawartośc do pliku txt
    """
    with open(path, 'w') as file:
        file.write(content)

    return True


def save_docx(path, content):
    """
    Funkcja zapisująca przekazaną zawartośc do pliku docx
    """
    doc = docx.Document()
    doc.add_paragraph(content)
    doc.save(path)

    return True


if __name__ == '__main__':
    string = 'Tekst zapisany do pliku.'

    txt = save_txt('../test.txt', string)
    print(txt)
    docx = save_docx('../test.docx', string)
    print(docx)
