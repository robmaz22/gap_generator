import docx


def read_txt(path):
    """
    Funkcja wczytująca zawartość pliku txt
    """
    with open(path, 'r') as file:
        content = file.read()

    return content


def read_docx(path):
    """
    Funkcja zwracająca zawartość pliku docx
    """
    doc = docx.Document(path)
    fulltext = []
    for p in doc.paragraphs:
        fulltext.append(p.text)

    return '\n'.join(fulltext)


if __name__ == '__main__':
    txt = read_txt('../przykładowy_tekst.txt')
    print(txt)
    docx = read_docx('../przykładowy_tekst.docx')
    print(docx)
