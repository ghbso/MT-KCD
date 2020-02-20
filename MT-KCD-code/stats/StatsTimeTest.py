import time
import datetime
import hashlib
import numpy as np

class Stats:

    def __init__(self, path):
        self.clear_current_stats()

        date_now = datetime.datetime.now().strftime("%Y-%m-%d")
        time_now = time.strftime("%H%M%S")
        nome = "exper-" + date_now + "-" + time_now + "-time-test"

        hash_exper = hashlib.md5(nome.encode('utf-8')).hexdigest()
        nome += "-" + hash_exper

        self.f = open(path + nome + ".out", 'w')
        self.f.write("#size,iter,avg(s),std,max,min,q1,q3")

    def start_time(self):
        self.start = time.time()

    def stop_time(self):
        self.end = time.time()

    def compute_elapsed_time(self):
        self.elapsed_time = self.end - self.start
        self.elapsed_times.append(self.elapsed_time)

    def compute_stats(self, dataset_size, is_to_print):
        size = dataset_size
        iter = len(self.elapsed_times)
        avg = np.average(self.elapsed_times)
        std = np.std(self.elapsed_times)
        min = np.min(self.elapsed_times)
        max = np.max(self.elapsed_times)
        q1 = np.percentile(self.elapsed_times, 25)
        q3 = np.percentile(self.elapsed_times, 75)
        self.f.write("#size,iter,avg,std,max,min,q1,q3")
        output = str(size) + "," + str(iter) + "," + str(avg) +"," + str(std) +"," + str(max) + "," + str(min) + "," + str(q1) + "," + str(q3)
        self.f.write("\n" + output)
        if(is_to_print):
            print(output)

    def clear_current_stats(self):
        self.start = -1
        self.end = -1
        self.elapsed_time = -1
        self.elapsed_times = []

    def close_test_file(self):
        self.f.close()