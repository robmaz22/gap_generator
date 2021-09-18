import docx


def read_txt(path):
    """
    Reading txt file
    """
    with open(path, 'r', encoding='utf-8') as file:
        content = file.read()

    return content


def read_docx(path):
    """
    Reading docx file
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
