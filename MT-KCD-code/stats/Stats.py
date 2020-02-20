class Stats:

    def __init__(self):
        self.tp = 0
        self.fp = 0
        self.tn = 0
        self.fn = 0
        self.tp_matcheds_indexes = []
        self.fp_matcheds_indexes = []
        self.fn_matcheds_indexes = []
        self.tn_matcheds_indexes = []

    def calc_stats(self, kcomplexes_especialistas, kcomplexes_algoritmo):

        is_visited = []

        for kcomplex_algoritmo in kcomplexes_algoritmo:
            start_sec_alg = kcomplex_algoritmo[0]
            end_sec_alg = kcomplex_algoritmo[1]
            is_matched = False
            for kcomplex_especialista in kcomplexes_especialistas:

                start_sec_esp = kcomplex_especialista[0]
                end_sec_esp = kcomplex_especialista[1]

                if(start_sec_alg<=end_sec_esp and start_sec_esp <=end_sec_alg):
                    if(kcomplex_especialista not in is_visited):
                        is_visited.append(kcomplex_especialista)
                        self.tp_matcheds_indexes.append(kcomplex_algoritmo)
                        self.tp += 1
                        is_matched = True
                        break

            if(is_matched==False):
               self.fp_matcheds_indexes.append(kcomplex_algoritmo)
               self.fp+=1

        for kcomplex_especialista in kcomplexes_especialistas:
            start_sec_esp = kcomplex_especialista[0]
            end_sec_esp = kcomplex_especialista[1]

            is_matched = False
            for kcomplex_algoritmo in kcomplexes_algoritmo:
                start_sec_alg = kcomplex_algoritmo[0]
                end_sec_alg = kcomplex_algoritmo[1]

                if (start_sec_alg <= end_sec_esp and start_sec_esp <= end_sec_alg):
                    is_matched = True
                    break


            if (is_matched == False):
                self.fn += 1
                self.fn_matcheds_indexes.append(kcomplex_especialista)

    def exists_in_experts_annotations(self, kcomplex_algoritmo, kcomplexes_especialistas, kc_visiteds):

        start_sec_alg = kcomplex_algoritmo[0]
        end_sec_alg = kcomplex_algoritmo[1]
        is_matched = False
        for kcomplex_especialista in kcomplexes_especialistas:
            start_sec_esp = kcomplex_especialista[0]
            end_sec_esp = kcomplex_especialista[1]
            if (start_sec_alg <= end_sec_esp and start_sec_esp <= end_sec_alg):
                if (kcomplex_especialista not in kc_visiteds):
                    kc_visiteds.append(kcomplex_especialista)
                    self.tp_matcheds_indexes.append(kcomplex_algoritmo)
                    self.tp += 1
                    return kc_visiteds, True
                    break


        return kc_visiteds, is_matched

    def exists_in_mtkcd_markings(self, kcomplex_especialista, kcomplexes_algoritmo):

        start_sec_esp = kcomplex_especialista[0]
        end_sec_esp = kcomplex_especialista[1]

        is_matched = False

        for kcomplex_algoritmo in kcomplexes_algoritmo:

            start_sec_alg = kcomplex_algoritmo[0]
            end_sec_alg = kcomplex_algoritmo[1]


            if (start_sec_alg <= end_sec_esp and start_sec_esp <= end_sec_alg):
                return True

        return is_matched



    def recall(self):
        if (self.tp == 0 and self.fn == 0):
            return 0

        try:
            recall = (self.tp / (self.tp + self.fn) )*100
        except:
            recall = 0
        return recall

    def precision(self):
        if(self.tp==0 and self.fp==0):
            return 0

        try:
            precision = (self.tp / (self.tp + self.fp)) * 100
        except:
            precision = 0
        return precision

    def f1(self):
        try:
            f1 = 2 * ((self.precision() * self.recall()) / (self.precision() + self.recall()))
        except:
            f1 = 0
        return f1

    def f2(self):
        try:
            f2 = 5 * (self.precision() * self.recall()) / ((4 * self.precision()) + self.recall())
        except:
            f2 = 0
        return f2


    def print_stats(self):

        print("Recall: ", "{0:.2f}%".format(round(self.recall(),2)))
        print("Precision: ","{0:.2f}%".format(round(self.precision(),2)))
        print("F1: ","{0:.2f}%".format(round(self.f1(),2)))
        print("F2: ","{0:.2f}%".format(round(self.f2(),2)))

