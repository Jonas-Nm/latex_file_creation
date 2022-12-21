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
        coord = [-10, -80]
    else:
        coord = [-10, 120]
    if '+TXC' not in options:
        drawing = Picture('Drawing', latex_path('images/Std', 'drawing_cube_std.pdf'), coord, '12.0cm')
        pre_writing(drawing.command)
        writing(drawing.insert())
    else:
        drawing = Picture('Drawing', latex_path('images/TXC', 'TXC_drawing.pdf'), coord, '14.5cm')
        pre_writing(drawing.command)
        writing(drawing.insert())
def handling_info():
    handling_info = Picture('Handling', latex_path('images', 'handling_instructions_std.pdf'), [0, -250], '2.12cm')
    pre_writing(handling_info.command)
    writing(handling_info.insert())
def vna_pic():
    vna_pic = Picture('PictureVNA', path + '/vna.png', [0, 50], '14.0cm')
    pre_writing(vna_pic.command)
    writing(vna_pic.insert())
def vna_setup_pic():
    vna_charac_setup = Picture('ResonanceCharacSetup', latex_path('images', 'resonancecharacteristics.pdf'), [0, 300], '3.4cm')
    pre_writing(vna_charac_setup.command)
    writing(vna_charac_setup.insert())
def measured_mod():
    measured_mod = Picture('MeasuredMod', path + '/mod.pdf', [0, 20], '29.0cm')
    pre_writing(measured_mod.command)
    writing(measured_mod.insert())
def drawing_title():
    title_drawing = Picture('Title', latex_path('images/Std', 'Cube_page1.pdf'), [0, 45], '4.0cm')
    pre_writing(title_drawing.command)
    writing(title_drawing.insert())
def wedge_pic():
    wedge_pic = Picture('wedge', latex_path('images/W', 'wedge_alignment.pdf'), [0, 260], '6.0cm')
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
path = r'P:\Ablage\j.neumeier\aktuelleProduktion\Optronscience\0.5F_M3x3x20-VIS+W+TXC SN22.0835 Optronscience'.replace('\\', '/')

line = 21  # choose the right excel line in database
mod_scraping = True

data = data(line, r'P:\Ablage\j.neumeier\aktuelleProduktion\database.csv'.replace('\\', '/'))
sn = data[0]
pm_type = data[1].replace('_', '\_')
options = ('+' + data[2].replace('Opt.:', '').replace(',', ',+').replace(' ', '')).split(',') #['+W', '+TXC', '+T']
if len(options) == 1:
    options = []
#options = ['+W', '+T', '+TXC']
ar = data[3].replace('AR: ', '').replace('nm', '').replace('-', ' - ') #'630-1100' #nm
acoustic_res = data[13] #'5.0, 6.2, 7.4'
wl = [data[14]]  #['780','1000']
if len(data[15]) > 0:
    wl.append(data[15])
rf_1rad_values = {}
for i in range(len(wl)):
    rf_1rad_values[wl[i]] = data[16+i]
aperture = data[18]  # '3x3'
wavefront = data[19]  # '6' means lambda/6 distortion
intensity = data[20] #W/mm^2
r_ar = data[21]  #%
temp_sensor = data[25] #'pt1000' or '10kNTC'
# pm_type, options, aperture, wl, wavefront = auftrag(file=path + r'/ProdAuftrag 22.pdf', pos=1)
####
vna = VNA(path + '/vna.txt')
rf_1rad_values = get_values(rf_1rad_values, wl)
if mod_scraping:
    rf_1rad_values = []
    wl = []
    for key, value in power_dbm_1rad(path + '/mod.pdf').items():
        wl.append(key)
        rf_1rad_values.append(value)



def fill_document():
    general_settings()
    #### first page ###
    writing(title_text(pm_type=pm_type, sn=sn, options=options))
    drawing_title()
    writing(space('70mm'))
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

opt = ''
for ele in options:
    opt += ele
datasheet_name = 'datasheet_'+pm_type.replace('\\', '')+opt+' '+sn

if __name__ == '__main__':
    # generate datasheet with content
    doc = Document(default_filepath=path + '/' + datasheet_name, document_options=['11pt'])
    fill_document()
    doc.generate_pdf(clean_tex=False, compiler='pdfLaTeX')
    doc.generate_tex()
    tex = doc.dumps()
    print(tex)

print(datasheet_name)
print(options)