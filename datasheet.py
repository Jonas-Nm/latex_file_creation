from pylatex import Document, Command
from pylatex.utils import NoEscape
from vna_eval import VNA
from pdfscraping import power_dbm_1rad, auftrag
from datacsv import data

def p(string):
    # writes plain latex string after \begin{document}
    return doc.append(NoEscape(string))
def b(string):
    # writes plain latex string to preamble
    return doc.preamble.append(NoEscape(string))
def text_command():
    b(r'\newcommand{\placetextbox}[3]{% \placetextbox{<horizontal pos>}{<vertical pos>}{<stuff>}')
    b(r'\setbox0=\hbox{#3}% Put <stuff> in a box')
    b(r'\AddToShipoutPictureFG*{% Add <stuff> to current page foreground')
    b(r'\put(\LenToUnit{#1\paperwidth},\LenToUnit{#2\paperheight}){\vtop{{\null}\makebox[0pt][c]{#3}}}}}')
def picture_command_generator(type,file,coordinates,height):
    # what type of image? Is it 'Logo', 'Title' drawing, etc?
    # height for example '1.5cm'
    # put_x, put_y, e.g. -200,370 for top left corner qubig logo
    # file location, e.g. 'images/logo.pdf'
    b(r'\newcommand\BackgroundPicture'+type+r'{')
    b(r'\put('+str(coordinates[0])+','+str(coordinates[1])+r'){\parbox[b][\paperheight]{\paperwidth}{\vfill')
    b(r'\centering\includegraphics[height='+height+r']{'+file+r'}\vfill}}}')
def banner_command():
    b(r'\newcommand{\banner}[1]{\begin{table}[h]\centering')
    b(r'\begin{tabular}{|p{17cm}|}\hline\rowcolor[HTML]{153c4a}')
    b(r'\hfil \textcolor{white}{\Large \textbf{{#1}}}')
    b(r'\end{tabular}\end{table}}')
def space(size):
    p(r'\vspace{'+size+'}')
def packages():
    #####packages
    b(r'\usepackage[table]{xcolor}')
    b(r'\usepackage{graphicx}')
    b(r'\usepackage{setspace}')
    b(r'\usepackage{siunitx}')
    b(r'\usepackage{fixltx2e}')
    b(r'\usepackage[a4paper, total={7in, 10.5in}]{geometry}')
    b(r'\usepackage[pscoord]{eso-pic}')
def font():
    doc.preamble.append(NoEscape(r'\renewcommand{\familydefault}{\sfdefault}'))
class Picture():
    def __init__(self, type, file, coordinates, height):
        self.type = type
        self.file = file
        self.coordinates = coordinates
        self.height = height
        picture_command_generator(self.type, self.file, self.coordinates, self.height)
    def insert(self):
        p(r'\AddToShipoutPictureBG*{\BackgroundPicture'+self.type+r'}')
class Text():
    def __init__(self, text='', size='', coordinates=[0.0, 0.0]):
        self.text = text
        self.size = size
        self.coordinates = coordinates #[0.0, 0.0] is defined as left bottom corner, [1.0, 1.0] as top right corner
    def insert(self):
        p(r'\placetextbox{' + str(self.coordinates[0]) + r'}{' + str(self.coordinates[1]) + r'}{' + self.size + ' ' + self.text + r'}')
    def toprightcorner(self):
        self.text = 'Empowering Laser Technologies'
        self.size = r'\Large'
        self.coordinates = [0.78,0.928]
        self.insert()
    def footnote_page1(self):
        pass
def table_settings():
    b(r'\setlength{\arrayrulewidth}{0.2pt}')
    b(r'\setlength{\tabcolsep}{8pt}')
    b(r'\renewcommand{\arraystretch}{1.9}')
    b(r'\arrayrulecolor[HTML]{999999}')
def general_settings():
    packages()
    font()
    table_settings()
    text_command()
    banner_command()
    logo = Picture('Logo', 'images/logo.pdf', [-200, 370], '1.5cm')
    logo.insert()
    Text().toprightcorner()
def title_text(PM_type, SN):
    p(r'\phantom{This text will be invisible}')
    p(r'\vspace{25mm}')
    p(r'\begin{spacing}{0.5}')
    p(r'\begin{center} {\huge \textbf{Test Data Sheet} \par}')
    p(r'\end{center}')
    p(r'\end{spacing}')
    p(r'\begin{center} {\Large\textbf{' + PM_type + r'} \par} \end{center}')
    p(r'\begin{center} {\normalsize ' + SN + ' \par} \end{center}')
    p(r'\begin{center} {\Large \textbf{Resonant electro-optic phase modulator}}\end{center}')
    if options != []:
        Text('with', r'\normalsize', [0.5, 0.71]).insert()
        inc = 0.0
        for element in options:
            if element in title_options:
                inc = inc - 0.015
                Text(r'- '+title_options[element], '', [0.5, 0.71+inc]).insert()


class Table:
    def __init__(self):
        pass

    def __begin(self):
        p(r'\begin{table}[h]\centering\begin{tabular}{|p{9.5cm}|p{3cm}|p{2.0cm}|}\hline\rowcolor[HTML]{153c4a}\textcolor{white}')

    def __end(self):
        p(r'\end{tabular}\end{table}')
        p(r'\vspace{-7mm}')
    def rf_std(self, f0, bw, q, wl, rf_1rad, RF_max = 0.5):
        if len(wl) > 1:
            rf_1rad = str(rf_1rad[0])+' | '+str(rf_1rad[1])
            wl = str(wl[0])+' | '+str(wl[1])
        else:
            wl = wl[0]
            rf_1rad = str(rf_1rad[0])
        self.__begin()
        p(r'{\textbf{RF properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}}  \\ \hline')
        p(r'Resonance frequency: f$_{0}$ $^{1)}$  & \hfil '+str(f0[0])+r' & \hfil '+f0[1]+r' \\ \hline')
        p(r'Bandwidth: $\Delta \nu$  & \hfil '+str(bw[0])+r'   & \hfil '+bw[1]+r' \\ \hline')
        p(r'Quality Factor: Q & \multicolumn{2}{|c|}{'+str(q)+r'}  \\ \hline')
        p(r'Required RF power for 1rad $@$ '+str(wl)+r'nm $^{2)}$   & \hfil '+rf_1rad+r' & \hfil dBm \\ \hline')
        p(r'max. RF power: RF\textsubscript{max} $^{3)}$ & \hfil '+str(RF_max)+r'   & \hfil W \\ \hline')
        self.__end()
    def RF_tuning(self):
        pass
    def optical_std(self,aperture,wavefront,wl,intensity,r_ar,ar):
        if len(wl) > 1:
            wl = min(wl)
        else:
            wl = wl[0]
        self.__begin()
        p(r'{\textbf{Optical properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}} \\ \hline')
        p(r'Aperture & \hfil '+aperture+r' & \hfil mm$^2$ \\ \hline')
        p(r'Wavefront distortion (633nm) & \hfil $\lambda / '+str(wavefront)+r' $   & \hfil nm \\ \hline')
        p(r'Recommended optical intensity ('+str(wl)+r'nm) & \hfil \si{<} '+str(intensity)+r' & \hfil W/mm$^2$ \\ \hline')
        p(r'AR coating (R\textsubscript{avg}\si{<}'+str(r_ar)+r'\% ) & \hfil '+ar+r' & \hfil nm  \\ \hline')
        self.__end()
    def optical_wedge(self):
        pass
    def dc_port(self):
        pass
def footnote_page1(T=23,damage=1):
    Text(r'$^{1)}$'+str(T)+r'°C $^{2)}$with 50$\si{\ohm}$ termination $^{3)}$no damage with RF\textsubscript{in}\si{<}'+str(damage)+r'W',
         r'\scriptsize' , [0.30,0.06]).insert()
def measured_modulation():
    p(r'\newpage')
    p(r'\banner{Measured modulation}')
    Picture('MeasuredMod' , 'images/measuredmodulation.pdf' , [0,60] , '21.0cm').insert()
    Picture('MeasuredModSetup', 'images/measuredmodulationsetup.pdf', [0, -320], '3.4cm').insert()
    Picture('MeasuredModSubtext', 'images/measuredmodulationsubtext.pdf', [-130, -180], '4.8cm').insert()
def resonance_characteristics():
    p(r'\newpage')
    p(r'\banner{Resonance Characteristics}')
    Picture('ResonanceCharacSetup' , 'images/resonancecharacteristics.pdf' , [0,300] , '3.4cm').insert()
    Picture('PictureVNA', 'images/vna.png', [0, 50], '14.0cm').insert()
    space('180mm')
def handling_instructions():
    p(r'\banner{Handling instructions}')
    Picture('Handling', 'images/handling_instructions_std.pdf', [0, -250], '2.12cm').insert()
def package_drawing():
    p(r'\newpage')
    p(r'\banner{Package drawing}')
    Picture('Drawing', 'images/drawing_cube_std.pdf', [0, 120], '12.0cm').insert()
def signature():
    Picture('Signature', 'images/signature.pdf', [0, -360], '1.51cm').insert()
def get_RF_1rad(pow_dBm_1rad):
    rf_1rad = []
    for key in pow_dBm_1rad:
        if int(key) in wl:
            rf_1rad.append(pow_dBm_1rad[key])
    return rf_1rad

type, options, aperture, wl, wavefront = auftrag(file='PO/ProdAuftrag_T_TC.pdf', pos=1)
title_options = {'+TXC': 'Temperature control option', '+TC': 'Temperature control option', '+T1': 'Frequency tuning option',
                 '+T': 'Frequency tuning option', '+W': 'Crystal wedge option', '+DC': 'DC-port option'}
vna = VNA()
rf_1rad_values = get_RF_1rad(power_dbm_1rad()) #works with beta App generated file, how about mathematica?


def fill_document(doc):
    general_settings()
    title_text(PM_type=type, SN='SN22.1235')
    Picture('Title', 'images/Cube_page1.pdf', [0, 45], '4.0cm').insert()
    space('70mm')
    Table().rf_std(f0=vna.f0('MHz'), bw=vna.bw('kHz'), q=vna.q(), wl=wl, rf_1rad=rf_1rad_values)
    Table().optical_std(aperture=aperture, wavefront=wavefront, wl=wl, intensity=1, r_ar=1, ar='630 - 1100') #take ar from .csv where label info, SN, tuning, etc
    footnote_page1(T=23, damage=1)
    measured_modulation()
    resonance_characteristics()
    handling_instructions()
    package_drawing()
    signature()

if __name__ == '__main__':
    # generate datasheet with content
    doc = Document('datasheet', document_options=['11pt'])
    fill_document(doc)
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)