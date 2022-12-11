import np as np
import numpy as np

class VNA():
    def __init__(self, file='vna_remote.txt'):
        self.file = file
        with open(self.file, "r") as lines:
            lines = lines.readlines()[1:]
            self.freq = [float(x.split(' ')[0]) for x in lines]
            self.s21 = [float(x.split(' ')[2]) for x in lines]
        self.s21_max = np.max(self.s21)
        self.index_max = self.s21.index(self.s21_max)
        self.s21_3dB = np.max(self.s21)-3.0

    def find_nearest(self):
        array_left = np.asarray(self.s21[:self.index_max])
        array_right = np.asarray(self.s21[self.index_max:-1])
        idx_left = (np.abs(array_left - self.s21_3dB)).argmin()
        idx_right = (np.abs(array_right - self.s21_3dB)).argmin()
        return self.s21[idx_left], idx_left, self.s21[idx_right + self.index_max], idx_right + self.index_max

    def f0(self, unit='Hz'):
        if unit == 'MHz':
            return np.round(self.freq[self.index_max]/1E6, 2), 'MHz'
        if unit == 'kHz':
            return np.round(self.freq[self.index_max]/1E3, 2), 'kHz'
        else:
            return self.freq[self.index_max], 'Hz'

    def bw(self, unit='Hz'):
        x = self.find_nearest()
        if unit == 'MHz':
            return np.round(np.abs(self.freq[x[1]] - self.freq[x[3]])/1E6, 1), 'Mhz'
        if unit == 'kHz':
            return np.round(np.abs(self.freq[x[1]] - self.freq[x[3]])/1E3, 1), 'kHz'
        else:
            return np.abs(self.freq[x[1]] - self.freq[x[3]]), 'Hz'
    def q(self):
        return int(np.round(self.f0()[0]/self.bw()[0]))




