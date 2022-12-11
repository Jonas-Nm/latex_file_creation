import csv


def data(line_num, file='data.csv'):
    with open(file, newline='') as csvfile:
        line = csv.reader(csvfile, delimiter=';', quotechar='"')
        i = 1
        for row in line:
            if i == line_num:
                x = row
            i += 1
        return x


