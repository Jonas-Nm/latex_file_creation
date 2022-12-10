from PyPDF2 import PdfFileReader
import re


def Power_dbm_1rad(file):
    pdftext = PdfFileReader(file).pages[0].extract_text()
    result_wl_nm = re.search('l nm (.*)\n', pdftext)
    result_1rad_dBm = re.search('P dBm (.*)\n', pdftext)
    wl_nm = result_wl_nm.group(1).split(' ')
    P_dBm = result_1rad_dBm.group(1).split(' ')
    P_dBm_1rad = {}
    for i in range(len(wl_nm)):
        P_dBm_1rad[wl_nm[i]] = P_dBm[i]
    return P_dBm_1rad
