from pylatex import Document, Command
from pylatex.utils import NoEscape

def p(string):
    # writes plain latex string
    return doc.append(NoEscape(string))
def packages():
    #####packages
    doc.preamble.append(NoEscape(r'\usepackage[table]{xcolor}'))
    doc.preamble.append(NoEscape(r'\usepackage{setspace}'))
    doc.preamble.append(NoEscape(r'\usepackage{graphicx}'))
    doc.preamble.append(NoEscape(r'\usepackage{tikz}'))
    doc.preamble.append(NoEscape(r'\usepackage{atbegshi,picture}'))
    doc.preamble.append(NoEscape(r'\usepackage[a4paper, total={7in, 10.5in}]{geometry}'))
    doc.preamble.append(NoEscape(r'\usepackage{siunitx}'))
    doc.preamble.append(NoEscape(r'\usepackage{fixltx2e}'))
    doc.preamble.append(NoEscape(r'\usepackage[pscoord]{eso-pic}'))
def general_settings():
    # change font type
    p(r'\renewcommand{\familydefault}{\sfdefault}')
    # the following defines a command to set everywhere on the page a text with overlay, i.e. not disturbing other content:
    p(r'\newcommand{\placetextbox}[3]{\setbox0=\hbox{#3}\AddToShipoutPictureFG*{\put(\LenToUnit{#1\paperwidth},\LenToUnit{#2\paperheight}){\vtop{{\null}\makebox[0pt][c]{#3}}}}}')

def table_settings():
    doc.preamble.append(NoEscape(r'\setlength{\arrayrulewidth}{0.2pt}'))
    doc.preamble.append(NoEscape(r'\setlength{\tabcolsep}{8pt}'))
    doc.preamble.append(NoEscape(r'\renewcommand{\arraystretch}{1.9}'))
    doc.preamble.append(NoEscape(r'\arrayrulecolor[HTML]{999999}'))
def logo():
    p(r'\begin{tikzpicture}[remember picture,overlay]')
    p(r'\node[anchor=north west,yshift=-25.0pt,xshift=50pt] at (current page.north west){\includegraphics[height=2.5cm]{kitten.jpg}};')
    p(r'\end{tikzpicture}')
def toprightcorner():
    doc.preamble.append(NoEscape(r'\AtBeginShipoutNext{\AtBeginShipoutUpperLeft{\put(\dimexpr\paperwidth-1.5cm\relax,-2.42cm){\makebox[0pt][r]{\Large Empowering Laser Technologies}}}}'))
def title(PM_type = 'PM8-NIR', SN = 'SN22.1234'):
    p(r'\vspace{25mm}')
    p(r'\begin{spacing}{1.5}')
    p(r'\begin{center} {\Large \textbf{Test Data Sheet} \par}')
    p(r'\end{center}')
    p(r'\end{spacing}')
    p(r'\begin{center} {\large\textbf{' + PM_type + r'} \par} \end{center}')
    p(r'\begin{center} {\normalsize ' + SN + ' \par} \end{center}')
def drawing_title_modulator(filelocation = ''):
    p(r'\begin{figure}[h]')
    p(r'\includegraphics[width=8cm]{kitten.jpg}')
    p(r'\centering')
    p(r'\end{figure}')
def table1_page1(frequency_0 = 0.0):
    p(r'\begin{table}[h]')
    p(r'\centering')
    p(r'\begin{tabular}{ |p{10cm}|p{3cm}|p{1.5cm}|  }')
    p(r'\hline')
    p(r'\rowcolor[HTML]{153c4a}')
    p(r'\textcolor{white}{RF properties}  & \hfil \textcolor{white}{Value} & \hfil \textcolor{white}{Unit}  \\')
    p(r'\hline')
    p(r'Frequency & \hfil {} & \hfil MHz \\'.format(frequency_0))
    p(r'\hline')
    p(r'Aland Islands & \hfil AX   & \hfil ALA \\')
    p(r'\hline')
    p(r'Albania & \hfil AL & \hfil ALB \\')
    p(r'\hline')
    p(r'Algeria    & \hfil DZ & \hfil DZA \\')
    p(r'\hline')
    p(r'American Samoa & \multicolumn{2}{|c|}{Country List} \\')
    p(r'\hline')
    p(r'\end{tabular}')
    p(r'\end{table}')


    p(r'')
    p(r'')
    p(r'')
    p(r'')

def fill_document(doc):
    packages()
    general_settings()
    table_settings()
    toprightcorner()
    logo()
    title(PM_type = 'PM7-SWIR1\_20', SN = '22.1235')
    drawing_title_modulator(filelocation = '')
    table1_page1(frequency_0 = 15.0)

if __name__ == '__main__':
    # generate datasheet with content
    doc = Document('datasheet')
    fill_document(doc)
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)