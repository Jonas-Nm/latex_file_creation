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
def tables():
    if '+T' in options:
        writing(Table().rf_tuning(fmax=fmax, fmin=fmin, f0=vna.f0('MHz'), bw=vna.bw('kHz'), q=vna.q(), wl=wl, rf_1rad=rf_1rad_values))
    else:
        writing(Table().rf_std(f0=vna.f0('MHz'), bw=vna.bw('kHz'), q=vna.q(), wl=wl, rf_1rad=rf_1rad_values))
    if '+W' in options:
        writing(Table().optical_wedge(aperture=aperture, wavefront=wavefront, wl=wl, intensity=intensity, r_ar=r_ar,
                                      ar=ar))  # take ar from .csv where label info, SN, tuning, etc
    else:
        writing(Table().optical_std(aperture=aperture, wavefront=wavefront, wl=wl, intensity=intensity, r_ar=r_ar,
                                      ar=ar))
    writing(footnote_page1(T=23, damage=1))

def signature():
    signature = Picture('Signature', latex_path('images', 'signature.pdf'), [0, -360], '1.51cm')
    pre_writing(signature.command)
    writing(signature.insert())
def drawing():
    if '+W' in options:
        coord = [0, -80]
    else:
        coord = [0, 120]
    if '+TXC' not in options:
        drawing = Picture('Drawing', latex_path('images/Std', 'drawing_cube_std.pdf'), coord, '12.0cm')
        pre_writing(drawing.command)
        writing(drawing.insert())
    else:
        drawing = Picture('Drawing', latex_path('images/TXC', 'TXC_drawing.pdf'), coord, '13.0cm')
        pre_writing(drawing.command)
        writing(drawing.insert())
def handling_info():
    handling_info = Picture('Handling', latex_path('images', 'handling_instructions_std.pdf'), [0, -250], '2.12cm')
    pre_writing(handling_info.command)
    writing(handling_info.insert())
def vna_pic():
    vna_pic = Picture('PictureVNA', path + '/vna_remote.png', [0, 50], '14.0cm')
    pre_writing(vna_pic.command)
    writing(vna_pic.insert())
def vna_setup_pic():
    vna_charac_setup = Picture('ResonanceCharacSetup', latex_path('images', 'resonancecharacteristics.pdf'), [0, 300], '3.4cm')
    pre_writing(vna_charac_setup.command)
    writing(vna_charac_setup.insert())
def measured_mod():
    measured_mod = Picture('MeasuredMod', path + '/measuredmodulation.pdf', [0, 60], '21.0cm')
    pre_writing(measured_mod.command)
    writing(measured_mod.insert())
def drawing_title():
    title_drawing = Picture('Title', latex_path('images/Std', 'Cube_page1.pdf'), [0, 55], '4.0cm')
    pre_writing(title_drawing.command)
    writing(title_drawing.insert())
def wedge_pic():
    wedge_pic = Picture('wedge', latex_path('images/W', 'wedge_alignment.pdf'), [0, 260], '5.0cm')
    pre_writing(wedge_pic.command)
    writing(wedge_pic.insert())
def txc_info(sensor, tec = True):
    if sensor == 'pt1000':
        pt = Picture('PT', latex_path('images/TXC', 'pt1000.pdf'), [0, 170], '13.0cm')
        pre_writing(pt.command)
        writing(pt.insert())
    elif sensor == '10kNTC':
        ntc = Picture('PT', latex_path('images/TXC', '10kNTC.pdf'), [-20, 80], '28.0cm')
        pre_writing(ntc.command)
        writing(ntc.insert())
    else:
        pass
    if tec:
        tec = Picture('tec', latex_path('images/TXC', 'TEC.pdf'), [0, -230], '8.0cm')
        pre_writing(tec.command)
        writing(tec.insert())
    else:
        pass



####
path = r'P:\Ablage\j.neumeier\aktuelleProduktion\5F_L3x3x30-NIR test'.replace('\\', '/')
pm_type, options, aperture, wl, wavefront = auftrag(file=path + r'/ProdAuftrag 22.pdf', pos=1)
fmax = [5.0, 'MHz']
fmin = [3.0, 'MHz']
intensity = 1 #W/mm^2
r_ar = 1  #%
ar = '630-1100' #nm
temp_sensor = '10kNTC'  #pt1000 or 10kNTC
####
options = ['+W', '+TXC', '+T']

vna = VNA(path + '/vna_remote.txt')
rf_1rad_values = get_RF_1rad(power_dbm_1rad(path + '/measuredmodulation.pdf'), wl) #works with beta App generated file, how about mathematica?
def fill_document():
    general_settings()
    #### first page ###
    writing(title_text(pm_type=pm_type, sn='SN22.1235', options=options))
    drawing_title()
    writing(space('60mm'))
    tables()
    #### new page ####
    writing(newpage())
    writing(banner('Measured modulation'))
    measured_mod()
    #### new page ####
    writing(newpage())
    writing(banner('Resonance characteristics'))
    vna_setup_pic()
    vna_pic()
    writing(space('180mm'))
    writing(banner('Handling instructions'))
    handling_info()
    if ('+TC' in options) or ('+TXC' in options):
        #### new page ####
        writing(newpage())
        writing(banner('TXC-option information'))
        txc_info(temp_sensor)
    #### new page ####
    writing(newpage())
    if '+W' in options:
        writing(banner('Alignment'))
        wedge_pic()
        writing(space('60mm'))
    writing(banner('Package drawing'))
    drawing()
    signature()


if __name__ == '__main__':
    # generate datasheet with content
    doc = Document(default_filepath=path + '/datasheet', document_options=['11pt'])
    fill_document()
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)


