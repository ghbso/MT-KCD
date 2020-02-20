from mtkcd.MTKCDParameters import MTKCDParameters
from mtkcd.MTKCDPrinterBuilder import MTKCDPrinterBuilder
import numpy as np
from util.ExpertAnnotationsReader import ExpertAnnotationsReader
from mtkcd.MTKCD import MTKCD
from stats.Stats import Stats
from pathlib import Path
import os

### Define path
path_patients_data = "dreams/patients/"
path_patients_expert_annotations = "dreams/patients_expert_annotations/"
path_to_save_graphics = "tmp/"

### Define parameters
mtkcd_parameters = MTKCDParameters
mtkcd_parameters.bpf_lower = 0.3
mtkcd_parameters.bpf_upper = 35
mtkcd_parameters.Fs = 200
mtkcd_parameters.L = 1 * mtkcd_parameters.Fs
mtkcd_parameters.delta_j= 0.05 * mtkcd_parameters.Fs
mtkcd_parameters.delta_f=4
mtkcd_parameters.f_max=3
mtkcd_parameters.q=95
mtkcd_parameters.i_short = int ( (0.5 * mtkcd_parameters.Fs) / mtkcd_parameters.delta_j );
mtkcd_parameters.i_backg = int ( (5.0 * mtkcd_parameters.Fs) / mtkcd_parameters.delta_j );
mtkcd_parameters.l_smth = int (0.15 * mtkcd_parameters.Fs);
mtkcd_parameters.l_backg= int (5.0 * mtkcd_parameters.Fs);
mtkcd_parameters.A_min=75
mtkcd_parameters.D_max=2* mtkcd_parameters.Fs

### Define scenario
scenario = "scenario-i"
desc_scenario = "Both experts"
path_patients_expert_annotations += "scoring_expert01_expert02_patient"

# scenario = "scenario-ii"
# desc_scenario = "Expert 01"
# path_patients_expert_annotations += "scoring_expert01_patient"

#scenario = "scenario-iii"
#desc_scenario = "Expert 02"
#path_patients_expert_annotations += "scoring_expert02_patient"


### Define others settings
reader = ExpertAnnotationsReader()
nums_patient= [1,2,3,4,5]


### iterate all patients
recalls = []
precisions = []
f1s = []
f2s = []

for num_patient in nums_patient:
    print("patient" + str(num_patient))

    ### load dataset and annotations
    desc = "patient" + str(num_patient)
    path_patient = Path().resolve() / Path(path_patients_data + desc + ".txt")  # absolute path
    path_patient_expert_annotations = Path().resolve() / Path(path_patients_expert_annotations +  str(num_patient) + '.txt')

    x = np.loadtxt(path_patient)
    expert_annotations = reader.readGroundTruths(path_patient_expert_annotations)
    ### run algo
    kc_algo = MTKCD()
    KC_out = kc_algo.mtkcd(x, mtkcd_parameters)

    ### update stats
    stats = Stats()
    stats.calc_stats(expert_annotations, KC_out)
    stats.print_stats()
    recalls.append(stats.recall())
    precisions.append(stats.precision())
    f1s.append(stats.f1())
    f2s.append(stats.f2())

    ### generate graphics
    maxFreqToShow = 25
    fontsize = 22
    fontsize_tick = 18
    N = len(x)
    for i in range(0, N // mtkcd_parameters.Fs, 90):
        segment = [i, (i + 90)]
        mtkcd_printer_builder = MTKCDPrinterBuilder(3, 1)
        desc = "patient-" + str(num_patient) + "_" + str(segment[0]) + "-" + str(segment[1]) + "_" + scenario + ".png"

        frq_step = mtkcd_parameters.Fs / kc_algo.R
        frq = np.arange(0, mtkcd_parameters.Fs, frq_step);

        indexFreq=0
        for f in frq:
            if (f >= 25):
                break
            indexFreq += 1
        frq = frq[:indexFreq]

        mtkcd_printer_builder.add_spec(segment,
                                       mtkcd_parameters.delta_j,
                                       mtkcd_parameters.Fs,
                                       kc_algo.SG,
                                       frq)\
                            .add_kc_markings(segment,
                                             x,
                                             mtkcd_parameters.Fs,
                                             KC_out,
                                             'red') \
                            .add_kc_markings(segment,
                                             x,
                                             mtkcd_parameters.Fs,
                                             KC_out,
                                             'blue')

        mtkcd_printer_builder.axes[0].set_ylabel("", fontsize=fontsize)
        mtkcd_printer_builder.axes[1].set_ylabel("MT-KCD", fontsize=fontsize)
        mtkcd_printer_builder.axes[2].set_ylabel(desc_scenario, fontsize=fontsize)

        mtkcd_printer_builder.axes[0].yaxis.get_label().set_fontsize(fontsize)
        mtkcd_printer_builder.axes[1].yaxis.get_label().set_fontsize(fontsize)
        mtkcd_printer_builder.axes[2].yaxis.get_label().set_fontsize(fontsize)

        mtkcd_printer_builder.axes[0].tick_params(labelsize=fontsize_tick)
        mtkcd_printer_builder.axes[1].tick_params(labelsize=fontsize_tick)
        mtkcd_printer_builder.axes[2].tick_params(labelsize=fontsize_tick)

        path_save = Path().resolve() / Path(path_to_save_graphics + desc)
        mtkcd_printer_builder.build(str(path_save), height=8, width=15)

### print mean stats
print("\nMean recall:", "{0:.2f}%".format(np.mean(recalls),2))
print("Mean precision:", "{0:.2f}%".format(np.mean(precisions),2))
print("Mean F1:", "{0:.2f}%".format(np.mean(f1s),2))
print("Mean F2:", "{0:.2f}%".format(np.mean(f2s),2))
