from mtkcd.MTKCDParameters import MTKCDParameters
from mtkcd.MTKCDPrinterBuilder import MTKCDPrinterBuilder
import numpy as np
from util.ExpertAnnotationsReader import ExpertAnnotationsReader
from mtkcd.MTKCD import MTKCD
from stats.StatsTimeTest import Stats
from pathlib import Path
import warnings

warnings.filterwarnings("ignore")

### Define path
path_patients_data = "dreams/size-test/"
path_patients_expert_annotations = "dreams/patients_expert_annotations/"
path_to_save_stats = "tmp/"

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

scenario = "scenario-i"
desc_scenario = "Both experts"
path_patients_expert_annotations += "scoring_expert01_expert02_patient"


### Define others settings
reader = ExpertAnnotationsReader()

### iterate all patients
recalls = []
precisions = []
f1s = []
f2s = []


warmup = 0
iterations = 1
num_datasets_size=5

print("warming up...." + str(warmup))
for j in range(0, warmup):
    print("--> warm " + str(j))

    ### load dataset and annotations
    desc = "dreams-kc-30min"
    path_patient = Path().resolve() / Path(path_patients_data + desc + ".txt")  # absolute path
    x = np.loadtxt(path_patient)
    ### run algo
    kc_algo = MTKCD()
    KC_out = kc_algo.mtkcd(x, mtkcd_parameters)

stats = Stats(path_to_save_stats)

print("testing....")
for i in range(0,num_datasets_size):
   ### load dataset and annotations
   desc = "dreams-kc-" + str(30*(i+1)) + "min"
   path_patient = Path().resolve() / Path(path_patients_data + desc + ".txt")  # absolute path
   x = np.loadtxt(path_patient)
   print("dataset size:" + str(len(x)))
   for j in range(0, iterations):
       ### run algo
       print("--> iter " + str(j))
       kc_algo = MTKCD()
       stats.start_time()
       KC_out = kc_algo.mtkcd(x, mtkcd_parameters)
       stats.stop_time()
       stats.compute_elapsed_time()

   stats.compute_stats(len(x), True)
   stats.clear_current_stats()