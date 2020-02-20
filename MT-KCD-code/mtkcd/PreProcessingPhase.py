from util.MultitaperSpectrogram import MultitaperSpectrogram
import numpy as np

class PreProcessingController:

    def apply_BPF(self, data, lower_freq, upper_freq, Fs):

        fft = np.fft.fft(data)
        n = len(data)
        frq = np.linspace(start=0, stop=(Fs // 2), num=(n // 2))
        for i in range(len(frq)):
            if frq[i] > upper_freq:  # cut off all frequencies higher than 0.005
                fft[i] = 0.0
                fft[(int)(len(data) / 2 + i)] = 0.0
            elif frq[i] < lower_freq:  # cut off all frequencies higher than 0.005
                fft[i] = 0.0
                fft[(int)(len(data) / 2 + i)] = 0.0

        inverse = np.fft.ifft(fft)
        return inverse.real



    def compute_SG(self, x, Fs, L, delta_j, delta_f):
        multitaper_spectrogram = MultitaperSpectrogram()

        SG, J, R = multitaper_spectrogram.calc_multitaper_spectrogram(x,
                                                                      Fs,
                                                                      L,
                                                                      delta_j,
                                                                      delta_f)

        return SG, J, R