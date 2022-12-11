from PyPDF2 import PdfFileReader
import re



def power_dbm_1rad(file='images/measuredmodulation.pdf'):
    pdftext = PdfFileReader(file).pages[0].extract_text()
    result_wl_nm = re.search('l nm (.*)\n', pdftext)
    result_1rad_dBm = re.search('P dBm (.*)\n', pdftext)
    wl_nm = result_wl_nm.group(1).split(' ')
    P_dBm = result_1rad_dBm.group(1).split(' ')
    P_dBm_1rad = {}
    for i in range(len(wl_nm)):
        P_dBm_1rad[wl_nm[i]] = P_dBm[i]
    return P_dBm_1rad

def auftrag(file='PO/ProdAuftrag_W_T.pdf', pos = 1):
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




