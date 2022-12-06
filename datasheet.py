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
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
    # the following defines a command to set everywhere on the page a text with overlay, i.e. not disturbing other content:
    doc.preamble.append(NoEscape(r'\newcommand{\placetextbox}[3]{\setbox0=\hbox{#3}\AddToShipoutPictureFG*{\put(\LenToUnit{#1\paperwidth},\LenToUnit{#2\paperheight}){\vtop{{\null}\makebox[0pt][c]{#3}}}}}'))

def table_settings():
    doc.preamble.append(NoEscape(r'\setlength{\arrayrulewidth}{0.2pt}'))
    doc.preamble.append(NoEscape(r'\setlength{\tabcolsep}{8pt}'))
    doc.preamble.append(NoEscape(r'\renewcommand{\arraystretch}{1.9}'))
    doc.preamble.append(NoEscape(r'\arrayrulecolor[HTML]{999999}'))
def logo():
    p(r'\begin{tikzpicture}[remember picture,overlay]\node[anchor=north west,yshift=-25.0pt,xshift=40pt] at (current page.north west){\includegraphics[height=1.5cm]{pics/logo.pdf}};\end{tikzpicture}')
def toprightcorner():
    doc.preamble.append(NoEscape(r'\AtBeginShipoutNext{\AtBeginShipoutUpperLeft{\put(\dimexpr\paperwidth-1.5cm\relax,-2.42cm){\makebox[0pt][r]{\Large Empowering Laser Technologies}}}}'))
def title(PM_type = 'PM8-NIR', SN = 'SN22.1234'):
    p(r'\vspace{22mm}')
    p(r'\begin{spacing}{1.5}')
    p(r'\begin{center} {\huge \textbf{Test Data Sheet} \par}')
    p(r'\end{center}')
    p(r'\end{spacing}')
    p(r'\begin{center} {\Large\textbf{' + PM_type + r'} \par} \end{center}')
    p(r'\begin{center} {\normalsize ' + SN + ' \par} \end{center}')
    p(r'\begin{center} {\Large \textbf{Resonant electro-optic phase modulator}}\end{center}')
def drawing_title_modulator(filelocation = ''):
    p(r'\begin{figure}[h]')
    p(r'\includegraphics[width=4cm]{pics/Cube_page1}')
    p(r'\centering')
    p(r'\end{figure}')
def table1_page1(frequency_0 = 0.0):
    p(r'\begin{table}[h]')
    p(r'\centering')
    p(r'\begin{tabular}{ |p{9.5cm}|p{3cm}|p{2.0cm}|  }')
    p(r'\hline')
    p(r'\rowcolor[HTML]{153c4a}')
    p(r'\textcolor{white}{\textbf{RF properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}}  \\')
    p(r'\hline')
    p(r'Resonance frequency: f$_{0}$ $^{1)}$   & \hfil 5.0 & \hfil MHz \\')
    p(r'\hline')
    p(r'Bandwidth: $\Delta \nu$  & \hfil 101   & \hfil kHz \\')
    p(r'\hline')
    p(r'Quality Factor: Q & \multicolumn{2}{|c|}{8}  \\')
    p(r'\hline')
    p(r'Required RF power for 1rad $@$ 852nm $^{2)}$   & \hfil 9.3 & \hfil dBm \\')
    p(r'\hline')
    p(r'max. RF power: RF\textsubscript{max} $^{3)}$ & \hfil 0.5   & \hfil W \\')
    p(r'\hline')
    p(r'\end{tabular}')
    p(r'\end{table}')
    p(r'\vspace{-5mm}')
def table2_page1():
    p(r'\begin{table}[h]')
    p(r'\centering')
    p(r'\begin{tabular}{ |p{9.5cm}|p{3cm}|p{2.0cm}|  }')
    p(r'\hline')
    p(r'\rowcolor[HTML]{153c4a}')
    p(r'\textcolor{white}{\textbf{Optical properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}} \\')
    p(r'\hline')
    p(r'Aperture & \hfil 3x3 & \hfil mm$^2$ \\')
    p(r'\hline')
    p(r'Wavefront distortion (633nm) & \hfil $\lambda / 6$   & \hfil nm \\')
    p(r'\hline')
    p(r'Recommended optical intensity (852nm) & \hfil \si{<} 1 & \hfil W/mm$^2$ \\')
    p(r'\hline')
    p(r'AR coating (R\textsubscript{avg}\si{<}1\% ) & \hfil 630 - 1100 & \hfil nm  \\')
    p(r'\hline')
    p(r'\end{tabular}')
    p(r'\end{table}')
def footnote_page1():
    p(r'\placetextbox{0.30}{0.06}{\scriptsize $^{1)}$25°C   $^{2)}$with 50$\si{\ohm}$ termination   $^{3)}$no damage with RF\textsubscript{in}\si{<}1W  }')

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
    table2_page1()
    footnote_page1()

if __name__ == '__main__':
    # generate datasheet with content
    doc = Document('datasheet', document_options = ['11pt'])
    fill_document(doc)
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)