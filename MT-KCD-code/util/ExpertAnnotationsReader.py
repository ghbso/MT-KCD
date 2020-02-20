import numpy as np

class ExpertAnnotationsReader:

    def readGroundTruths(self,path):
        f = open(path, 'r')
        # next(f)
        groundTruths = []
        for line in f:
            if line.strip():
               values = line.split()
               try:
                   start = values[0]
                   end = float(start) + float(values[1])
                   groundTruths.append([float(start),end])
               except:
                   pass

        return groundTruths

    def readGroundTruthsNoTransformationFromFile(self, path):
        f = open(path, 'r')
        groundTruths = []
        for line in f:
            if line.strip():
                values = line.split()
                start = values[0]
                end = values[1]
                groundTruths.append([start, end])

        return groundTruths

    def readGroundTruthsNoTransformation(self, lines):
        groundTruths = []
        for line in lines:
            line = line.replace('\n', '')
            if line.strip():
                values = line.split()
                start = values[0]
                end = values[1]
                groundTruths.append([start, end])

        return groundTruths
