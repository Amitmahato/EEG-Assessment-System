import numpy as np

class CSV:
    def __init__(self):
        self.data = []

    def read(self,file):
        csv = open(file,'r')
        for line in csv:
            temp = [float(i)/255 for i in line.split(',')]
            # red = [[temp[int(3*i):int(3*i)+3] for i in range(len(temp)//3) ]]
            self.data.append(temp)