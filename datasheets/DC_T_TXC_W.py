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
    pre_writing(table_settings(dc=True))
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
    writing(Table().dc_port(wl=wl, Vdc=Vdc_values))
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
    drawing = Picture('Drawing', latex_path('images/DC', 'DC_drawing.pdf'), [0, 15], '14.0cm')
    pre_writing(drawing.command)
    writing(drawing.insert())

def handling_info():
    handling_info = Picture('Handling', latex_path('images', 'handling_instructions_std.pdf'), [0, 320], '2.12cm')
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
    title_drawing = Picture('Title', latex_path('images/Std', 'Cube_page1.pdf'), [0, 55], '4.0cm')
    pre_writing(title_drawing.command)
    writing(title_drawing.insert())
def wedge_pic():
    wedge_pic = Picture('wedge', latex_path('images/W', 'wedge_alignment.pdf'), [0, -150], '6.5cm')
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
#path = r'P:\Ablage\j.neumeier\aktuelleProduktion\Government Scientific Source\5.2T_M3x3x30-SWIR1+W+TXC+DC SN22.0803 Government Scientific Source'.replace('\\', '/')

line = 11  # choose the right excel line in database


###
data = data(line, r'P:\Ablage\j.neumeier\aktuelleProduktion\database.csv'.replace('\\', '/'))
sn = data[0]
pm_type = data[1].replace('_', '\_')
options = ('+' + data[2].replace('Opt.: ', '').replace(',', ',+')).split(',') #['+W', '+TXC', '+T']
#options = ['+W', '+T', '+TXC']
ar = data[3].replace('AR: ', '').replace('nm', '').replace('-', ' - ') #'630-1100' #nm
fmax = [float(data[7]), data[8]]  #  [5.0, 'MHz']
fmin = [float(data[5]), data[8]]
acoustic_res = data[13] #'5.0, 6.2, 7.4'
wl = [data[14]]  #['780','1000']
if len(data[15]) > 0:
    wl.append(data[15])
rf_1rad_values = {}
for i in range(len(wl)):
    rf_1rad_values[wl[i]] = data[16+i]
Vdc_values = {}
for i in range(len(wl)):
    Vdc_values[wl[i]] = data[22+i]
aperture = data[18]  # '3x3'
wavefront = data[19]  # '6' means lambda/6 distortion
intensity = data[20] #W/mm^2
r_ar = data[21]  #%
tuningturns = data[24]
temp_sensor = data[25] #'pt1000' or '10kNTC'
# pm_type, options, aperture, wl, wavefront = auftrag(file=path + r'/ProdAuftrag 22.pdf', pos=1)
####
vna = VNA(path + '/vna.txt')
#rf_1rad_values = get_RF_1rad(power_dbm_1rad(os.path.join(path, 'mod.pdf')), wl) #works with beta App generated file, how about mathematica?
rf_1rad_values = get_values(rf_1rad_values, wl)
Vdc_values = get_values(Vdc_values, wl)



def fill_document():
    general_settings()
    #### first page ###
    writing(title_text(pm_type, sn, options))
    writing(space('40mm'))
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
    writing((banner('Tuning performance')))
    tuning_pic = Picture('Tuning', latex_path('images/T', 'tuning.pdf'), [125, -292], '6.7cm')
    writing(tuning_pic.command)
    writing(tuning_pic.insert())
    tuninginfo_pic = Picture('Tuninginfo', latex_path('images/T', 'tuning_info.pdf'), [-145, -350], '2.48cm')
    writing(tuninginfo_pic.command)
    writing(tuninginfo_pic.insert())
    writing(space('-7mm'))
    writing(Table().tuning(fmax=fmax, fmin=fmin, n=tuningturns, acres=acoustic_res))
    #### new page ####
    writing(newpage())
    writing(banner('DC characteristics'))
    dc_pic = Picture('DC', latex_path('images/DC', 'DC_characteristics.pdf'), [0, 180], '12cm')
    writing(dc_pic.command)
    writing(dc_pic.insert())
    writing(space('130mm'))
    writing(banner('Alignment'))
    wedge_pic()
    if ('+TC' in options) or ('+TXC' in options):
        #### new page ####
        writing(newpage())
        writing(banner('TXC-option information'))
        txc_info(temp_sensor)
    #### new page ####
    writing(newpage())
    writing(banner('Handling instructions'))
    handling_info()
    writing(space('30mm'))
    writing(banner('Package drawing'))
    drawing()
    tuningattention_pic = Picture('Tuningattention', latex_path('images/T', 'tuning_attention.pdf'), [0, - 240], '3.0cm')
    writing(tuningattention_pic.command)
    writing(tuningattention_pic.insert())
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
