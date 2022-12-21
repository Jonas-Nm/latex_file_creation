from pylatex import Document, Command
from pylatex.utils import NoEscape
from vna_eval import VNA
from pdfscraping import power_dbm_1rad, auftrag
import os
from datacsv import data
from pathlib import Path

# class Datasheet(Document):
#     def __init__(self, default_filepath='default_filepath', *, documentclass='article', document_options=None, fontenc='T1',
#                  inputenc='utf8', font_size="normalsize", lmodern=True, textcomp=True,
#                  microtype=None, page_numbers=True, indent=None, geometry_options=None, data=None):
#         super().__init__(self, default_filepath=default_filepath, *, documentclass=documentclass,
#                          document_options=document_options, fontenc=fontenc, inputenc=inputenc, font_size=font_size, lmodern=lmodern, textcomp=textcomp,
#                          microtype=microtype, page_numbers=page_numbers, indent=indent, geometry_options=geometry_options, data=data)


def text_command():
    return [r'\newcommand{\placetextbox}[3]{% \placetextbox{<horizontal pos>}{<vertical pos>}{<stuff>}',
            r'\setbox0=\hbox{#3}% Put <stuff> in a box',
            r'\AddToShipoutPictureFG*{% Add <stuff> to current page foreground',
            r'\put(\LenToUnit{#1\paperwidth},\LenToUnit{#2\paperheight}){\vtop{{\null}\makebox[0pt][c]{#3}}}}}']
def picture_command_generator(type, file, coordinates, height):
    return [r'\newcommand\BackgroundPicture' + type + r'{',
            r'\put(' + str(coordinates[0]) + ',' + str(coordinates[1]) + r'){\parbox[b][\paperheight]{\paperwidth}{\vfill',
            r'\centering\includegraphics[height=' + height + r']{' + file + r'}\vfill}}}']
def banner_command():
    return [r'\newcommand{\banner}[1]{\begin{table}[h]\centering',
            r'\begin{tabular}{|p{18.5cm}|}\hline\rowcolor[HTML]{153c4a}',
            r'\hfil \textcolor{white}{\Large \textbf{{#1}}}',
            r'\end{tabular}\end{table}}']
def space(size):
    return [r'\vspace{' + size + '}']
def packages():
    return [r'\usepackage[table]{xcolor}', r'\usepackage{graphicx}', r'\usepackage{setspace}',
            r'\usepackage{siunitx}', r'\usepackage{fixltx2e}', r'\usepackage[a4paper, total={7.5in, 10.5in}]{geometry}',
            r'\usepackage[pscoord]{eso-pic}']
def font():
    return [r'\renewcommand{\familydefault}{\sfdefault}']
class Picture:
    def __init__(self, type, file, coordinates, height):
        self.type = type
        self.file = file
        self.coordinates = coordinates
        self.height = height
        self.command = picture_command_generator(self.type, self.file, self.coordinates, self.height)
    def insert(self):
        return [r'\AddToShipoutPictureBG*{\BackgroundPicture' + self.type + r'}']
class Text:
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
def table_settings(dc=False):
    if not dc:
        return [r'\setlength{\arrayrulewidth}{0.2pt}',
                r'\setlength{\tabcolsep}{8pt}',
                r'\renewcommand{\arraystretch}{1.9}',
                r'\arrayrulecolor[HTML]{999999}']
    else:
        return [r'\setlength{\arrayrulewidth}{0.2pt}',
                r'\setlength{\tabcolsep}{8pt}',
                r'\renewcommand{\arraystretch}{1.6}',
                r'\arrayrulecolor[HTML]{999999}']


def latex_path(folder,file, n = 0):
    if False:
        go_back = Path(__file__).parents[n]
        return os.path.join(go_back, folder, file).replace('\\', '/')
    else:
        return os.path.join(r'P:\Ablage\datasheet', folder, file).replace('\\', '/')

def title_text(pm_type, sn, options):
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
                options_list.append(Text(r'- ' + title_options[element], '', [0.5, 0.71+inc]).insert()[0])
    return string_list + options_list


class Table:
    def __init__(self):
        pass

    def __begin(self):
        return [r'\begin{table}[h]\centering\begin{tabular}{|p{9.5cm}|p{3cm}|p{2.0cm}|}\hline\rowcolor[HTML]{153c4a}\textcolor{white}']

    def __end(self):
        return [r'\end{tabular}\end{table}', r'\vspace{-7mm}']

    def rf_std(self, f0, bw, q, wl, rf_1rad, rf_max=0.5):
        if len(wl) > 1:
            rf_1rad = str(rf_1rad[0])+' | '+str(rf_1rad[1])
            wl = str(wl[0])+' | '+str(wl[1])
        else:
            wl = wl[0]
            rf_1rad = str(rf_1rad[0])

        return self.__begin()+[r'{\textbf{RF properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}}  \\ \hline',
                        r'Resonance frequency: f$_{0}$ $^{1)}$  & \hfil ' + str(f0[0]) + r' & \hfil ' + f0[1] + r' \\ \hline',
                        r'Bandwidth: $\Delta \nu$  & \hfil ' + str(bw[0]) + r'   & \hfil ' + bw[1] + r' \\ \hline',
                        r'Quality Factor: Q & \multicolumn{2}{|c|}{' + str(q) + r'}  \\ \hline',
                        r'Required RF power for 1rad $@$ ' + str(wl) + r'nm $^{2)}$   & \hfil ' + rf_1rad + r' & \hfil dBm \\ \hline',
                        r'max. RF power: RF\textsubscript{max} $^{3)}$ & \hfil ' + str(rf_max) + r'   & \hfil W \\ \hline']+self.__end()
    def rf_tuning(self, fmax, fmin, f0, bw, q, wl, rf_1rad, rf_max=0.5):
        if len(wl) > 1:
            rf_1rad = str(rf_1rad[0])+' | '+str(rf_1rad[1])
            wl = str(wl[0])+' | '+str(wl[1])
        else:
            wl = str(wl[0])
            rf_1rad = str(rf_1rad[0])

        return self.__begin()+[r'{\textbf{RF properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}}  \\ \hline',
                        r'Resonance frequency: f$_{0}$ $^{1)}$  & \hfil ' + str(fmin[0]) + ' - ' + str(fmax[0]) + r' & \hfil ' + fmax[1] + r' \\ \hline',
                        r'Preset frequency: f$_{set}$ $^{1)}$  & \hfil ' + str(f0[0]) + r' & \hfil ' + f0[1] + r' \\ \hline',
                        r'Bandwidth: $\Delta \nu$  & \hfil ' + str(bw[0]) + r'   & \hfil ' + bw[1] + r' \\ \hline',
                        r'Quality Factor: Q & \multicolumn{2}{|c|}{' + str(q) + r'}  \\ \hline',
                        r'Required RF power for 1rad $@$ ' + str(wl) + r'nm $^{2)}$   & \hfil ' + rf_1rad + r' & \hfil dBm \\ \hline',
                        r'max. RF power: RF\textsubscript{max} $^{3)}$ & \hfil ' + str(rf_max) + r'   & \hfil W \\ \hline']+self.__end()
    def optical_std(self, aperture, wavefront, wl, intensity, r_ar, ar):
        if len(wl) > 1:
            wl = min(wl)
        else:
            wl = wl[0]
        return self.__begin()+[r'{\textbf{Optical properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}} \\ \hline',
                        r'Aperture & \hfil ' + aperture + r' & \hfil mm$^2$ \\ \hline',
                        r'Wavefront distortion (633nm) & \hfil $\lambda / ' + str(wavefront) + r' $   & \hfil nm \\ \hline',
                        r'Recommended optical intensity (' + str(wl) + r'nm) & \hfil \si{<} ' + str(intensity) + r' & \hfil W/mm$^2$ \\ \hline',
                        r'AR coating (R\textsubscript{avg}\si{<}' + str(r_ar) + r'\% ) & \hfil ' + ar + r' & \hfil nm  \\ \hline']+self.__end()
    def optical_wedge(self, aperture, wavefront, wl, intensity, r_ar, ar):
        if len(wl) > 1:
            wl = min(wl)
        else:
            wl = wl[0]
        return self.__begin()+[r'{\textbf{Optical properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}} \\ \hline',
                        r'Aperture & \hfil ' + aperture + r' & \hfil mm$^2$ \\ \hline',
                        r'Wavefront distortion (633nm) & \hfil $\lambda / ' + str(wavefront) + r' $   & \hfil nm \\ \hline',
                        r'Recommended optical intensity (' + str(wl) + r'nm) & \hfil \si{<} ' + str(intensity) + r' & \hfil W/mm$^2$ \\ \hline',
                        r'AR coating (R\textsubscript{avg}\si{<}' + str(r_ar) + r'\% ) & \hfil ' + ar + r' & \hfil nm  \\ \hline',
                        r'Wedged facets & \multicolumn{2}{|c|}{0°/4°}  \\ \hline']+self.__end()
    def dc_port(self, wl, Vdc):
        if len(wl) > 1:
            wl = str(wl[0])+' | '+str(wl[1])
            Vdc = str(Vdc[0]) + ' | ' + str(Vdc[1])
        else:
            wl = str(wl[0])
            Vdc = str(Vdc[0])
        return self.__begin()+[r'{\textbf{DC properties}}  & \hfil \textcolor{white}{\textbf{Value}} & \hfil \textcolor{white}{\textbf{Unit}} \\ \hline',
                        r'DC Bandwidth: $\Delta \nu_{DC}$ (-3dB) & \hfil 11 & \hfil kHz \\ \hline',
                        r'Required DC voltage for $\pi$ rad (PM) $@$ ' + str(wl) + r'nm & \hfil ' + Vdc + r'   & \hfil V \\ \hline',
                        r'max. DC voltage: V$_{max}$ & \hfil +/-500 & \hfil Vdc \\ \hline',
                        r'Input capacitance (DC) & \hfil 1 & \hfil nF  \\ \hline']+self.__end()

    def tuning(self, fmax, fmin, n, acres):
        text = [r'\setlength{\arrayrulewidth}{0.2pt}',
                r'\setlength{\tabcolsep}{8pt}',
                r'\renewcommand{\arraystretch}{1.7}',
                r'\begin{table}[h]\small',
                r'\begin{tabular}{ |p{3.85cm}|p{0.90cm}|p{0.95cm}|p{0.8cm}| }\hline',
                r'MAX resonance frequency & \hfil f$_{0}$max & \hfil ' + str(fmax[0])  + r' & \hfil ' + fmax[1] + r' \\ \hline',
                r'Min resonance frequency  & \hfil f$_{0}$min   & \hfil ' + str(fmin[0]) + r'  & \hfil MHz \\ \hline',
                r'number of turns &  \hfil N$_{max}$   & \hfil ' + str(n) + r'  & \hfil  \\ \hline',
                r'counter clock-wise turns  & \multicolumn{3}{|c|}{higher f$_{0}$} \\ \hline',
                r'clock-wise turns & \multicolumn{3}{|c|}{lower f$_{0}$} \\ \hline',
                r'\end{tabular}\end{table}']
        if len(acres) != 0:
           text.append(r'\placetextbox{0.635}{0.09}{\footnotesize @ $\{$'+ acres + '$\}$MHz}')
        return text
def footnote_page1(T=23,damage=1):
    return Text(r'$^{1)}$' + str(T) + r'°C $^{2)}$with 50$\si{\ohm}$ termination $^{3)}$no damage with RF\textsubscript{in}\si{<}'
                + str(damage) + r'W', r'\scriptsize', [0.30, 0.06]).insert()

def banner(text):
    return [r'\banner{' + text + '}']
def newpage():
    return [r'\newpage']


def get_values(dic, wl_):
    values = []
    for key in dic:
        if key in wl_:
            values.append(dic[key])
    return values

title_options = {'+TXC': 'Temperature control option', '+TC': 'Temperature control option', '+T1': 'Frequency tuning option',
                 '+T': 'Frequency tuning option', '+W': 'Crystal wedge option', '+DC': 'DC-port option', '+AR': 'Customised AR coating option'}
