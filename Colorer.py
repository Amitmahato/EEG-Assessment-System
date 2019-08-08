import numpy as np

class Colorer:
    def __init__(self): # the name of electrodes to shohw in the 3d model and the color files
        self.electrode = ['FP1','FP2','F7','F3','F4','F8','T3','C3','C4','T4','T5','P3','P4','T6','O1','O2']
        self.color = []

    def inverse(self,arr):
        # Inverts the matrix in the raw data for use in this function
        temp = [[arr[j][i] for j in range(len(arr))] for i in range(len(arr[0]))]
        return temp

    def coder(self,data):
        #invert the data
        data = self.inverse(data)
        # store data as dictionary
        dic = dict(zip(self.electrode,data))
        
        # total time in second
        time = len(data[0])//256
        # to store information about the data
        processed = []
        for time_point in range(time):
            elect = []
            for e in self.electrode:

                # start the fast fourier transform for each channel for eaach second
                start = 256*time_point
                sec  = dic[e][start:start+256]
                amps = np.abs(np.fft.fft(sec))
                amps = amps[:128]

                # some estimation and some normalization effort
                alpha = sum([i for i in amps[8:13]])/0.01
                beta = sum([i for i in amps[13:30]])/0.12
                delta = sum([i for i in amps[1:8]])/0.075

                # append them to a list
                elect.append(alpha)
                elect.append(beta)
                elect.append(delta)
            processed.append(elect)

        #  exports the colors
        self.color = processed
        return self.color