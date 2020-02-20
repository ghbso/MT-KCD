import numpy as np
import operator
import math
import nitime.algorithms as tsa

class MultitaperSpectrogram:

    def __radix2(self, i):
        n = 1
        while n < i: n *= 2
        return n

    def calc_multitaper_spectrogram(self, x, Fs, L, delta_j, delta_f):
        N = len(x)
        TW = (L * delta_f) / (2 * Fs)
        K = 2 * TW
        K = int(K) - 1

        R = self.__radix2(L);

        J = math.floor(N / delta_j)

        W, e = tsa.dpss_windows(L, NW=TW, Kmax=K)

        SG = [[0 for y in range((J))] for x in range((R))]

        index_column = 0

        for i in range(0, int(len(x) - L), int(delta_j)):
            start = i

            end = start + L
            start = int(start)
            end = int(end)
            window = x[start:end]

            mtp = self.calc_multitaper_spectrum(window, W, R, Fs)
            for index_freq in range(len(mtp)):
                SG[index_freq][index_column] = mtp[index_freq]
            index_column += 1

        SG = np.add(SG, 1)
        SG = 10 * np.log10(SG)

        return SG, J, R

    def calc_multitaper_spectrum(self, x, W, R, Fs):

        multitaper = [0] * R
        j = []
        j_conj = []

        for tp in W:
            tappered_data = x * tp
            F = (np.fft.fft(tappered_data, R))

            j.append(F)
            j_conj.append(np.conjugate(F))
            multitaper += F[0:R]

        B = np.multiply(j_conj, j).real;
        B /= Fs

        multitaper = np.mean(B, axis=0)

        return multitaper