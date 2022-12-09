from pylatex import Document, Command
from pylatex.utils import NoEscape

def p(string):
    # writes plain latex string
    return doc.append(NoEscape(string))


def packages():
    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))
    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))
    doc.preamble.append(NoEscape(r'\usepackage{graphicx}'))
    doc.preamble.append(NoEscape(r'\usepackage{setspace}'))
    #doc.preamble.append(NoEscape(r'\usepackage{tikz}'))
    #doc.preamble.append(NoEscape(r'\usepackage{atbegshi,picture}'))
    doc.preamble.append(NoEscape(r'\usepackage{siunitx}'))
    doc.preamble.append(NoEscape(r'\usepackage{fixltx2e}'))
    doc.preamble.append(NoEscape(r'\usepackage[a4paper, total={7in, 10.5in}]{geometry}'))
    doc.preamble.append(NoEscape(r'\usepackage{eso-pic}'))

  #  doc.preamble.append(NoEscape(r'\usepackage[pscoord]{eso-pic}% The zero point of the coordinate systemis the lower left corner of the page (the default).'))
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
    doc.preamble.append(NoEscape(r'\newcommand\BackgroundPicture{'))
    doc.preamble.append(NoEscape(r'  \put(-200,350){'))
    doc.preamble.append(NoEscape(r'   \parbox[b][\paperheight]{\paperwidth}{'))
    doc.preamble.append(NoEscape(r'     \vfill'))
    doc.preamble.append(NoEscape(r'     \centering'))
    doc.preamble.append(NoEscape(r'     \includegraphics[height=1.5cm]{images/logo.pdf}'))
    doc.preamble.append(NoEscape(r'     \vfill'))
    doc.preamble.append(NoEscape(r'    }'))
    doc.preamble.append(NoEscape(r'  }'))
    doc.preamble.append(NoEscape(r'}'))


def logo():
    p(r'\AddToShipoutPictureBG*{\BackgroundPicture}')


def fill_document(doc):
    packages()
    logo()
    p(r'asd')

if __name__ == '__main__':
    # generate datasheet with content
    doc = Document('datasheet', document_options = ['11pt'])
    fill_document(doc)
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)


