from pylatex import Document, Command
from pylatex.utils import NoEscape
from vna_eval import VNA
from pdfscraping import power_dbm_1rad, auftrag
from datacsv import data

# class Datasheet(Document):
#     def __init__(self, default_filepath='default_filepath', *, documentclass='article', document_options=None, fontenc='T1',
#                  inputenc='utf8', font_size="normalsize", lmodern=True, textcomp=True,
#                  microtype=None, page_numbers=True, indent=None, geometry_options=None, data=None):
#         super().__init__(self, default_filepath=default_filepath, *, documentclass=documentclass,
#                          document_options=document_options, fontenc=fontenc, inputenc=inputenc, font_size=font_size, lmodern=lmodern, textcomp=textcomp,
#                          microtype=microtype, page_numbers=page_numbers, indent=indent, geometry_options=geometry_options, data=data)

def pre_writing(func):
    for i in range(len(func)):
        doc.preamble.append(NoEscape(func[i]))
def writing(func):
    for i in range(len(func)):
        doc.append(NoEscape(func[i]))
def text_command():
    return [r'\newcommand{\placetextbox}[3]{% \placetextbox{<horizontal pos>}{<vertical pos>}{<stuff>}',
            r'\setbox0=\hbox{#3}% Put <stuff> in a box',
            r'\AddToShipoutPictureFG*{% Add <stuff> to current page foreground',
            r'\put(\LenToUnit{#1\paperwidth},\LenToUnit{#2\paperheight}){\vtop{{\null}\makebox[0pt][c]{#3}}}}}']
def picture_command_generator(type,file,coordinates,height):
    # what type of image? Is it 'Logo', 'Title' drawing, etc?
    # height for example '1.5cm'
    # put_x, put_y, e.g. -200,370 for top left corner qubig logo
    # file location, e.g. 'images/logo.pdf'
    b(r'\newcommand\BackgroundPicture'+type+r'{')
    b(r'\put('+str(coordinates[0])+','+str(coordinates[1])+r'){\parbox[b][\paperheight]{\paperwidth}{\vfill')
    b(r'\centering\includegraphics[height='+height+r']{'+file+r'}\vfill}}}')
def picture_command_generator(type,file,coordinates,height):
    return [r'\newcommand\BackgroundPicture'+type+r'{',
            r'\put('+str(coordinates[0])+','+str(coordinates[1])+r'){\parbox[b][\paperheight]{\paperwidth}{\vfill',
            r'\centering\includegraphics[height='+height+r']{'+file+r'}\vfill}}}']

def banner_command():
    return [r'\newcommand{\banner}[1]{\begin{table}[h]\centering',
            r'\begin{tabular}{|p{17cm}|}\hline\rowcolor[HTML]{153c4a}',
            r'\hfil \textcolor{white}{\Large \textbf{{#1}}}',
            r'\end{tabular}\end{table}}']
def space(size):
    return [r'\vspace{'+size+'}']

def packages():
    return [r'\usepackage[table]{xcolor}', r'\usepackage{graphicx}', r'\usepackage{setspace}',
            r'\usepackage{siunitx}', r'\usepackage{fixltx2e}', r'\usepackage[a4paper, total={7in, 10.5in}]{geometry}',
            r'\usepackage[pscoord]{eso-pic}']
def font():
    return [r'\renewcommand{\familydefault}{\sfdefault}']
class Picture():
    def __init__(self, type, file, coordinates, height):
        self.type = type
        self.file = file
        self.coordinates = coordinates
        self.height = height
        self.command = picture_command_generator(self.type, self.file, self.coordinates, self.height)
    def insert(self):
        return [r'\AddToShipoutPictureBG*{\BackgroundPicture'+self.type+r'}']
class Text():
    def __init__(self, text='', size='', coordinates=[0.0, 0.0]):
        self.text = text
        self.size = size
        self.coordinates = coordinates #[0.0, 0.0] is defined as left bottom corner, [1.0, 1.0] as top right corner
    def insert(self):
        return [r'\placetextbox{' + str(self.coordinates[0]) + r'}{' + str(self.coordinates[1]) + r'}{' + self.size + ' ' + self.text + r'}']
    def toprightcorner(self):
        self.text = 'Empowering Laser Technologies'
        self.size = r'\Large'
        self.coordinates = [0.78, 0.928]
        return self.insert()
    def footnote_page1(self):
        pass
def table_settings():
    return [r'\setlength{\arrayrulewidth}{0.2pt}',
            r'\setlength{\tabcolsep}{8pt}',
            r'\renewcommand{\arraystretch}{1.9}',
            r'\arrayrulecolor[HTML]{999999}']

def general_settings():
    pre_writing(packages())
    pre_writing(font())
    pre_writing(table_settings())
    pre_writing(text_command())
    pre_writing(banner_command())
    logo = Picture('Logo', r'C:/Users/j.neumeier/PycharmProjects/latex_file_creation/images/logo.pdf', [-200, 370], '1.5cm')
    pre_writing(logo.command)
    writing(logo.insert())
    writing(Text().toprightcorner())
def title_text(pm_type, sn):
    string_list = [r'\phantom{This text will be invisible}',
                   r'\vspace{25mm}',
                   r'\begin{spacing}{0.5}',
                   r'\begin{center} {\huge \textbf{Test Data Sheet} \par}',
                   r'\end{center}', r'\end{spacing}',
                   r'\begin{center} {\Large\textbf{' + pm_type + r'} \par} \end{center}',
                   r'\begin{center} {\normalsize ' + sn + ' \par} \end{center}',
                   r'\begin{center} {\Large \textbf{Resonant electro-optic phase modulator}}\end{center}']
    options_list = []
    if options != []:
        options_list.append(Text('with', r'\normalsize', [0.5, 0.71]).insert()[0])
        inc = 0.0
        for element in options:
            if element in title_options:
                inc = inc - 0.015
                options_list.append(Text(r'- '+title_options[element], '', [0.5, 0.71+inc]).insert()[0])
    return string_list + options_list


class Table:
    def __init__(self):
        pass

    def __begin(self):
        return [r'\begin{table}[h]\centering\begin{tabular}{|p{9.5cm}|p{3cm}|p{2.0cm}|}\hline\rowcolor[HTML]{153c4a}\textcolor{white}']

    def __end(self):
        return [r'\end{tabular}\end{table}', r'\vspace{-7mm}']

    def rf_std(self, f0, bw, q, wl, rf_1rad, RF_max = 0.5):
        if len(wl) > 1:
            rf_1rad = str(rf_1rad[0])+' | '+str(rf_1rad[1])
            wl = str(wl[0])+' | '+str(wl[1])
        else:
            wl = wl[0]
            rf_1rad = str(rf_1rad[0])

        return self.__begin()+[r'{\textbf{RF properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}}  \\ \hline',
                        r'Resonance frequency: f$_{0}$ $^{1)}$  & \hfil '+str(f0[0])+r' & \hfil '+f0[1]+r' \\ \hline',
                        r'Bandwidth: $\Delta \nu$  & \hfil ' + str(bw[0]) + r'   & \hfil ' + bw[1] + r' \\ \hline',
                        r'Quality Factor: Q & \multicolumn{2}{|c|}{' + str(q) + r'}  \\ \hline',
                        r'Required RF power for 1rad $@$ ' + str(wl) + r'nm $^{2)}$   & \hfil ' + rf_1rad + r' & \hfil dBm \\ \hline',
                        r'max. RF power: RF\textsubscript{max} $^{3)}$ & \hfil ' + str(RF_max) + r'   & \hfil W \\ \hline']+self.__end()

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
def get_RF_1rad(pow_dBm_1rad, wl_):
    rf_1rad = []
    for key in pow_dBm_1rad:
        if int(key) in wl_:
            rf_1rad.append(pow_dBm_1rad[key])
    return rf_1rad

path = r"P:/Ablage/j.neumeier/aktuelleProduktion/5F_L3x3x30-NIR test/"
pm_type, options, aperture, wl, wavefront = auftrag(file='PO/ProdAuftrag_T_TC.pdf', pos=1)
title_options = {'+TXC': 'Temperature control option', '+TC': 'Temperature control option', '+T1': 'Frequency tuning option',
                 '+T': 'Frequency tuning option', '+W': 'Crystal wedge option', '+DC': 'DC-port option'}
vna = VNA(path + 'vna_remote.txt')
rf_1rad_values = get_RF_1rad(power_dbm_1rad(path + 'measuredmodulation.pdf'), wl) #works with beta App generated file, how about mathematica?




def fill_document():
    general_settings()
    writing(title_text(pm_type=pm_type, sn='SN22.1235'))
    # Picture('Title', 'images/Cube_page1.pdf', [0, 45], '4.0cm').insert()
    writing(space('70mm'))
    writing(Table().rf_std(f0=vna.f0('MHz'), bw=vna.bw('kHz'), q=vna.q(), wl=wl, rf_1rad=rf_1rad_values))
    # Table().optical_std(aperture=aperture, wavefront=wavefront, wl=wl, intensity=1, r_ar=1, ar='630 - 1100') #take ar from .csv where label info, SN, tuning, etc
    # footnote_page1(T=23, damage=1)
    # measured_modulation()
    # resonance_characteristics()
    # handling_instructions()
    # package_drawing()
    # signature()

if __name__ == '__main__':
    # generate datasheet with content
    #doc = Document('datasheet_stack', document_options=['11pt'])
    doc = Document(default_filepath=path + 'datasheet_stack', document_options=['11pt'])
    fill_document()
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)