import numpy as np

class CandidateExtractionController:


    def identify_CR(self,
                    SG,
                    J,
                    R,
                    Fs,
                    f_max,
                    i_short,
                    i_backg,
                    q):

        c = self.compute_power_concentrations(SG, J, R, Fs, f_max)

        c_short = self.cma(c, i_short)
        c_backg = self.cma(c, i_backg)
        c_diff = np.subtract(c_short, c_backg)
        percentile = np.percentile(c_diff, q, axis=0)

        CR = []

        start_region=-1
        end_region=-1

        for index in range(0, len(c_diff)):
            if ((c_diff[index])>= percentile):
                if(start_region==-1):
                    start_region = index
            else:
                if(start_region!=-1):
                    end_region=index-1
                    if ( (end_region-start_region) > 0) :
                        CR.append([start_region, end_region])
                    start_region=-1
                    end_region=-1

        return CR

    def mark_KC_cand(self,
                     x,
                     N,
                     CR,
                     delta_j,
                     l_smth,
                     l_backg):

        x_backg = self.cma(x, l_backg)
        std_backg = self.cmsd(x, l_backg)

        A_sup = np.sum([x_backg, std_backg], axis=0)
        A_inf = np.subtract(x_backg, std_backg)

        x_smth = self.cma(x, l_smth)

        KC_cand = []

        for candidate_region in CR:
            start_cr = candidate_region[0]
            end_cr = candidate_region[1]

            start_x = (int) (start_cr*delta_j)
            end_x = (int) (end_cr*delta_j)

            index = start_x
            while (index <= end_x):
                is_leakage_a_inf = False

                if (x_smth[index] < A_inf[index]):
                    is_leakage_a_inf = True

                if (is_leakage_a_inf):

                    kc_start_index = index
                    kc_end_index = index + 1

                    is_overpass_x_backg = False
                    is_leakage_a_sup = False

                    while (True):
                        if (x_smth[kc_start_index] >= x_backg[kc_start_index] or kc_start_index < 0):
                            break
                        kc_start_index -= 1;

                    while (kc_end_index < N):

                        if (x_smth[kc_end_index] >= x_backg[kc_end_index]):
                            is_overpass_x_backg = True
                            break

                        kc_end_index += 1
                    if (is_overpass_x_backg):
                        while (kc_end_index < N):
                            if (x_smth[kc_end_index] <= x_backg[kc_end_index]):
                                break
                            else:
                                if (x_smth[kc_end_index] > A_sup[kc_end_index]):
                                    is_leakage_a_sup = True

                            kc_end_index += 1

                    index = kc_end_index + 1

                    if (is_overpass_x_backg and is_leakage_a_sup):
                        KC_cand.append(
                            [kc_start_index,kc_end_index - 1])
                else:
                    index += 1

        return  KC_cand

    def compute_power_concentrations(self, SG, J, R, Fs, f_max):
        index_freq = 0
        for r in range(0, R):
            equivalent_frequency = r * (Fs / R)
            if (equivalent_frequency > f_max):
                break
            index_freq += 1
        sequence = [SG[i][int(0):int(J)] for i in range(0, index_freq)]
        sum = np.sum(sequence, axis=0)
        return sum

    def cma(self, x, window):
        cma = []

        qtd_left = window // 2
        qtd_right = window - qtd_left

        for i in range(0, len(x)):
            start = i - qtd_left
            end = i + qtd_right
            if (start < 0):
                start = 0

            if (end > len(x)):
                end = len(x)
            sequence = x[start: end]
            mean = np.mean(sequence)
            cma.append(mean)

        return cma

    def cmsd(self, x, window):
        cmsd = []

        qtd_left = window // 2
        qtd_right = window - qtd_left

        for i in range(0, len(x)):
            start = i - qtd_left
            end = i + qtd_right
            if (start < 0):
                start = 0
            if (end > len(x)):
                end = len(x)
            sequence = x[start: end]
            std = np.std(sequence)
            cmsd.append(std)

        return cmsd

