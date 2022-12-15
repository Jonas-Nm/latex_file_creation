import csv
import os

#path = r'P:\Ablage\j.neumeier\aktuelleProduktion'.replace('\\', '/')
def data(line_num, file):
    with open(file, newline='') as csvfile:
        line = csv.reader(csvfile, delimiter=';', quotechar='"')
        i = 1
        for row in line:
            if i == line_num:
                x = row
            i += 1
        return x


