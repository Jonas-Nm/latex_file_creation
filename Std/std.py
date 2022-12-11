from pylatex import Document, Command
from pylatex.utils import NoEscape
from vna_eval import VNA
from pdfscraping import power_dbm_1rad, auftrag
from datasheet_stack import *
from datacsv import data



type, options, aperture, wl, wavefront = auftrag(file=r'C:\Users\Jonas\PycharmProjects\latex_file_creation\PO\ProdAuftrag_T_TC.pdf', pos=1)
title_options = {'+TXC': 'Temperature control option', '+TC': 'Temperature control option', '+T1': 'Frequency tuning option',
                 '+T': 'Frequency tuning option', '+W': 'Crystal wedge option', '+DC': 'DC-port option'}
vna = VNA()
rf_1rad_values = get_RF_1rad(power_dbm_1rad(), wl) #works with beta App generated file, how about mathematica?


def fill_document(doc):
    general_settings()
    title_text(PM_type=type, SN='SN22.1235', opt=options, title_opt=title_options)
    Picture('Title', r'C:\Users\Jonas\PycharmProjects\latex_file_creation\images\Cube_page1.pdf', [0, 45], '4.0cm').insert()
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
    doc = Document('datasheet_std', document_options=['11pt'])
    fill_document(doc)
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)