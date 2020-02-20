import numpy as np

class CandidateEliminationController:

    def one_candidate_per_region_checking(self,
                                          x,
                                          CR,
                                          delta_j,
                                          kComplexes):

        KC_cand_max = []

        index_kc = 0

        for index_cr in range(0, len(CR)):
            kcs_by_cr = []

            start_cr = CR[index_cr][0] * delta_j
            end_cr = CR[index_cr][1] * delta_j

            while (True):
                if (index_kc >= len(kComplexes)):
                    break

                start_kc = (kComplexes[index_kc][0])
                end_kc = (kComplexes[index_kc][1])

                if (start_kc > end_cr):
                    break
                else:
                    if (start_kc <= end_cr and start_cr <= end_kc):
                        kcs_by_cr.append([start_kc,end_kc])

                    index_kc += 1

            paa_by_kc = []
            for kcomplex in kcs_by_cr:
                sequence = x[int(kcomplex[0]): int(kcomplex[1])]
                diff = np.max(sequence) - np.min(sequence)
                paa_by_kc.append(diff)

            qnt_max = 1
            if (len(paa_by_kc) > 0):
                qnt_visited = 0
                max_by_trecho = np.max(paa_by_kc)

                while (qnt_visited < qnt_max and qnt_visited < len(paa_by_kc)):
                    index_max = np.argmax(paa_by_kc)
                    KC_cand_max.append(kcs_by_cr[index_max])
                    qnt_visited = qnt_visited + 1
                    paa_by_kc[index_max] = max_by_trecho


        return KC_cand_max

    def amplitude_duration_validation(self,
                                      x,
                                      KC_cand_max,
                                      A_min,
                                      D_max):

        KC_out = []
        for kComplex in KC_cand_max:
            start = (kComplex[0])
            end = (kComplex[1])

            duration=end-start
            sequence = x[start:end + 1]

            min = np.min(sequence)
            max = np.max(sequence)

            if (abs(max - min) >= A_min and duration<= D_max ):
                KC_out.append([start,end])

        return KC_out
