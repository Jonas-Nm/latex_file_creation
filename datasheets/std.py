from datasheet_package import *
from datacsv import data


def pre_writing(func):
    for i in range(len(func)):
        doc.preamble.append(NoEscape(func[i]))
def writing(func):
    for i in range(len(func)):
        doc.append(NoEscape(func[i]))
def general_settings():
    pre_writing(packages())
    pre_writing(font())
    pre_writing(table_settings())
    pre_writing(text_command())
    pre_writing(banner_command())
    logo = Picture('Logo',
                   latex_path('images', 'logo.pdf'),
                   [-200, 370], '1.5cm')
    pre_writing(logo.command)
    writing(logo.insert())
    writing(Text().toprightcorner())


####
path = r'P:\Ablage\j.neumeier\aktuelleProduktion\5F_L3x3x30-NIR test'.replace('\\', '/')
pm_type, options, aperture, wl, wavefront = auftrag(file=path + r'/ProdAuftrag 22.pdf', pos=1)
####


vna = VNA(path + '/vna_remote.txt')
rf_1rad_values = get_RF_1rad(power_dbm_1rad(path + '/measuredmodulation.pdf'), wl) #works with beta App generated file, how about mathematica?
def fill_document():
    general_settings()
    #### first page ###
    writing(title_text(pm_type=pm_type, sn='SN22.1235', options=options))
    title_drawing = Picture('Title', latex_path('images/Std', 'Cube_page1.pdf'), [0, 45], '4.0cm')
    pre_writing(title_drawing.command)
    writing(title_drawing.insert())
    writing(space('70mm'))
    writing(Table().rf_std(f0=vna.f0('MHz'), bw=vna.bw('kHz'), q=vna.q(), wl=wl, rf_1rad=rf_1rad_values))
    writing(Table().optical_std(aperture=aperture, wavefront=wavefront, wl=wl, intensity=1, r_ar=1, ar='630 - 1100')) #take ar from .csv where label info, SN, tuning, etc
    writing(footnote_page1(T=23, damage=1))
    #### new page ####
    writing(measured_modulation())
    measured_mod = Picture('MeasuredMod', path + '/measuredmodulation.pdf', [0, 60], '21.0cm')
    pre_writing(measured_mod.command)
    writing(measured_mod.insert())
    #### new page ####
    writing(resonance_characteristics())
    vna_charac_setup = Picture('ResonanceCharacSetup', latex_path('images', 'resonancecharacteristics.pdf'), [0, 300], '3.4cm')
    pre_writing(vna_charac_setup.command)
    writing(vna_charac_setup.insert())
    vna_pic = Picture('PictureVNA', path + '/vna_remote.png', [0, 50], '14.0cm')
    pre_writing(vna_pic.command)
    writing(vna_pic.insert())
    writing(space('180mm'))
    writing(handling_instructions())
    handling_info = Picture('Handling', latex_path('images', 'handling_instructions_std.pdf'), [0, -250], '2.12cm')
    pre_writing(handling_info.command)
    writing(handling_info.insert())
    #### new page ####
    writing(package_drawing())
    drawing = Picture('Drawing', latex_path('images/Std', 'drawing_cube_std.pdf'), [0, 120], '12.0cm')
    pre_writing(drawing.command)
    writing(drawing.insert())
    signature = Picture('Signature', latex_path('images', 'signature.pdf'), [0, -360], '1.51cm')
    pre_writing(signature.command)
    writing(signature.insert())


if __name__ == '__main__':
    # generate datasheet with content
    doc = Document(default_filepath=path + '/datasheet', document_options=['11pt'])
    fill_document()
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)



