import pandas as pd
import numpy as np

class Colorer:
    def __init__(self):
    # csv = pd.read_csv('00409.csv', skipinitialspace=True)
        self.electrode = ['FP1','FP2','F7','F3','F4','F8','T3','C3','C4','T4','T5','P3','P4','T6','O1','O2']
        self.out = []

    def inverse(self,arr):
        temp = [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]
        return temp

    def coder(self,data):
        # data = []
        # for e in self.electrode:
        #     data.append(csv[e].tolist())
        data = self.inverse(data)
        dic = dict(zip(self.electrode,data))
        
        l = len(data[0])//256
        processed = []
        for i in range(l):
            elect = []
            for e in self.electrode:       
                start = 256*i
                sec  = dic[e][start:start+256]
                amps = np.abs(np.fft.fft(sec))
                amps = amps[:128]
                alpha = sum([i for i in amps[8:13]])/0.01
                beta = sum([i for i in amps[13:30]])/0.12
                delta = sum([i for i in amps[1:8]])/0.075
                elect.append(alpha)
                elect.append(beta)
                elect.append(delta)
            processed.append(elect)
        # here is the data
        # np.savetxt('data2.csv',processed,delimiter=',')
        
        self.out = processed
        return self.out
