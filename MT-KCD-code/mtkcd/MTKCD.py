from mtkcd.PreProcessingPhase import PreProcessingController
from mtkcd.CandidateExtractionPhase import CandidateExtractionController
from mtkcd.CandidateEliminationPhase import CandidateEliminationController

class MTKCD:

    def mtkcd(self, x, mtkcd_parameters):
        N = len(x)

        pre_process_controller = PreProcessingController()
        candidate_extraction_controller = CandidateExtractionController()
        candidate_elimination_controller = CandidateEliminationController()

        x = pre_process_controller.apply_BPF(
            x,
            mtkcd_parameters.bpf_lower,
            mtkcd_parameters.bpf_upper,
            mtkcd_parameters.Fs)

        SG, J, R = pre_process_controller.compute_SG(
            x,
            mtkcd_parameters.Fs,
            mtkcd_parameters.L,
            mtkcd_parameters.delta_j,
            mtkcd_parameters.delta_f)

        self.SG = SG
        self.R = R

        CR =  candidate_extraction_controller.identify_CR(
            SG,
            J,
            R,
            mtkcd_parameters.Fs,
            mtkcd_parameters.f_max,
            mtkcd_parameters.i_short,
            mtkcd_parameters.i_backg,
            mtkcd_parameters.q)

        KC_cand = candidate_extraction_controller.mark_KC_cand(
            x,
            N,
            CR,
            mtkcd_parameters.delta_j,
            mtkcd_parameters.l_smth,
            mtkcd_parameters.l_backg)


        KC_cand_max = candidate_elimination_controller.one_candidate_per_region_checking(
            x,
            CR,
            mtkcd_parameters.delta_j,
            KC_cand)

        KC_out = candidate_elimination_controller.amplitude_duration_validation(
            x,
            KC_cand_max,
            mtkcd_parameters.A_min,
            mtkcd_parameters.D_max
        )

        KC_out_time_steps = []  #output in secs

        for kc in KC_out:
            start = (kc[0])
            end = (kc[1])

            KC_out_time_steps.append(
                [(start / mtkcd_parameters.Fs),
                 (end / mtkcd_parameters.Fs)]
            )

        return KC_out_time_steps

    def f(self,str):
        print("hello")
