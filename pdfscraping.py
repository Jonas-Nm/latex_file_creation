from PyPDF2 import PdfFileReader
import re
import os
from tika import parser  #needs java run time


#path = r'P:\Ablage\j.neumeier\aktuelleProduktion\19F_M3x3x15+AR+TXC SN22.0521 Alpine Quantum Tech'.replace('\\', '/')
#file = path + '/mod.pdf'

def power_dbm_1rad(file):
    # pdftext = PdfFileReader(file).pages[0].extract_text()
    content = parser.from_file(file)['content']
   # print(content)
    result_wl_nm = re.search('nm (.*)\n', content).group(1)
    result_1rad_dBm = re.search('P dBm |P1rad dBm (.*)\n', content).group(1)
    result_wl_meas = re.search('(.*)nm \(meas\.\)', content).group(1)
    wl_nm = result_wl_nm.split(' ')
    P_dBm = result_1rad_dBm.split(' ')
    P_dBm_1rad = {}
    for i in range(len(wl_nm)):
        P_dBm_1rad[wl_nm[i]] = P_dBm[i]
    del P_dBm_1rad[result_wl_meas]
    return P_dBm_1rad
#print(power_dbm_1rad(file))



def auftrag(file, pos = 1):
    pdf = PdfFileReader(file)
    num_pages = pdf.numPages
    pdftext = ''
    for i in range(num_pages):
        pdftext += PdfFileReader(file).pages[i].extract_text()+'\n'
    pdftext = pdftext.replace('\n', '')
    position_text = re.search('Pos\.'+str(pos)+': (.*)Pos\.'+str(pos+1), pdftext).group(1)  #does not work with 'PO/ProdAuftrag_W_TXC_DC.pdf', write exception
    type_options = re.search('(.*) \| Qty', position_text).group(1).split(' ')  # https://support.iterable.com/hc/en-us/articles/211728403-Regular-expressions-for-use-in-segmentation-and-Handlebars-RegEx-#vertical-bar
    type = type_options.pop(0)
    type = type.replace('_', '\_')
    options = type_options
    aperture = re.search('aperture: (.*)', position_text).group(1)[:3]
    if 'frequency tuning range' in position_text:
        options.append('+T')
    wl = []
    wl_ = re.search('wavelength λo:(.*)', position_text).group(1)[:5] # how is it with two wavelengths or if the unit is um and not nm?
    wl_ = wl_.replace('n', '')
    wl_ = int(wl_.replace('m', ''))
    wl.append(wl_)
    wavefront = int(re.search('λ/(.*)', position_text).group(1)[:1])

    return type, options, aperture, wl, wavefront




