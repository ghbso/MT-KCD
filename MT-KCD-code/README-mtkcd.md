# MT-KCD

Multitaper-based K-Complex detection, MT-KCD, is a new method for automatic identiﬁcation of K-Complexs in human sleep EEG. 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. 

### Prerequisites

You need have Python = 3.x installed on your machine.

## Settings

 The database used to perform the tests is DREAMS database. The EEG data and the corresponding experts annotations are placed in */dreams* folder. The runnable file is main.py. The instructions above must be done in it. 

### Parameters 
 The MT-KCD parameters are setted in lines 16-30 .

### Evaluation scenarios 

You need choose evalutation scenario to run the MT-KCD.

If you want evaluate in scenario (i), you must uncomment the following command lines:
```
# scenario = "scenario-i"
# desc_scenario = "Both experts"
# path_patients_expert_annotations += "scoring_expert01_expert02_patient"
```

If you want evaluate in scenario (ii), you must uncomment the following command lines:
```
# scenario = "scenario-ii"
# desc_scenario = "Expert 01"
# path_patients_expert_annotations += "scoring_expert01_patient"
```

Otherwise, if you want evaluate in scenario (iii), you must uncomment the following command lines:
```
# scenario = "scenario-iii"
# desc_scenario = "Expert 02"
# path_patients_expert_annotations += "scoring_expert02_patient"
```

## Running

To run MT-KCD you must execute following command:
```
python main.py
```

After run the command above, it will print on console the **recall, precision, F1 and F2  values** achieved by MT-KCD. In addition, it will generated for each patient a set of graphical results, each one containing the spectrogram, MT-KCD markings and expert annotations (according to chosen evaluation scenario). These graphicals will be placed  in */tmp* folder.

To run MT-KCD runtime tests for each patient you must execute following command:
```
python main-time-test-by-patient.py
```

After run the command above, it will print on console the **size, iter, avg(s), std, max, min, q1, q3  values** achieved by MT-KCD for each patient. These values will also be saved on a output file placed in */tmp* folder.

To run MT-KCD runtime tests when increasing the input size you must execute following command:
```
python main-time-test.py
```

After run the command above, it will print on console the **size, iter, avg(s), std, max, min, q1, q3  values** achieved by MT-KCD for each syntetic dataset. These values will also be saved on a output file placed in */tmp* folder.


## Authors

* **Gustavo Henrique Batista Santos Oliveira**
* Luciano Reis Coutinho 
* Josenildo Costa da Silva
* Ivan de Jesus Pereira Pinto
* Júlia Manayara Ferreira Silva
* Franciso José da Silva e Silva
* Davi Viana Santos
* Arieal Soares Teles

## Acknowledgments

This work was supported by the Foundation for Research and Scientiﬁc and Technological Development of Maranhão (FAPEMA) [grant number TIAC-06418/16].


