from PyPDF2 import PdfFileReader
import re

file = 'full.pdf'
pdf = PdfFileReader(file)
# print(pdf.pages[0].extract_text())

s = pdf.pages[0].extract_text()
result = re.search('3 (.*) 9', s)
print(result.group(1))