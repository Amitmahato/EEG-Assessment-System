from sklearn.metrics import classification_report, confusion_matrix
from sklearn import svm
from sklearn.model_selection import train_test_split
from numpy.fft import fft,fftfreq
from numpy import abs
import mne
import pickle
class Predictor:
    def __init__(self,filePath):
        self.filename = './data/trained_model.sav'
        self.raw_data = []
        self.result_data=[]
        self.bad = []
        self.header = []
        self.powers = []
        self.file = filePath

    def assess_func(self):
        edf = mne.io.read_raw_edf(self.file)
        self.raw_data = edf.get_data().T
        self.header = edf.ch_names
        svcclassifier = pickle.load(open(self.filename, 'rb'))
    
        alpha = []
        beta = []
        theta = []
        total = []

        for j in range(32):
            fp2 = [self.raw_data[i][j] for i in range(len(self.raw_data))]
            freqs = fftfreq(len(fp2))
            freqs = freqs>0
            vals = fft(fp2)
            vals = abs(vals)
            vals = vals[freqs]
            scale = len(freqs)//256
            a=b=d=t=0
            th = sum([i**2 for i in vals[4*scale:8*scale]])
            d = sum([i**2 for i in vals[1*scale:4*scale]])
            a = sum([i**2 for i in vals[8*scale:13*scale]])
            b = sum([i**2 for i in vals[13*scale:40*scale]])
            t = sum([i**2 for i in vals])-sum([i**2 for i in vals[49*scale:51*scale]]) - sum([i**2 for i in vals[:scale]])

            alpha.append(a)
            beta.append(b)
            theta.append(d)
            total.append(t)

            rhythm=a+b+d+th
            noise=t-rhythm
            result = svcclassifier.predict([[rhythm,noise]])
            if result==0:
                # print('Channel C'+str(j+1)+' is bad.')
                self.result_data.append('bad')
                self.bad.append(j)
            else:
                # print('Channel C'+str(j+1)+' is good.')
                self.result_data.append('good')
        
        self.powers.append(sum(alpha)/len(alpha))
        self.powers.append(sum(beta)/len(beta))
        self.powers.append(sum(theta)/len(theta))
        self.powers.append(sum(total)/len(total))

        self.filter_bad()

    def get_result(self):
        channelInfo = []
        for i in range(len(self.header)):
            msg = "Channel "+ str(i) + " " + self.header[i] + ' is ' + self.result_data[i]
            channelInfo.append(msg)
        return channelInfo
    
    def filter_bad(self):
        temp = self.bad
        new = []
        x = [1,2,4,5,7,8,10,11,13,14,16,17,19,20,21,23]
        for i in temp:
            if i in x:
                new.append(x.index(i))
        self.bad = new

    # ['PG1', 'FP1', 'FP2', 'PG2', 'F7', 'F3', 'FZ', 'F4', 'F8', 'A1',10 'T3', 'C3', 'CZ', 'C4',13 'T4', 'A2', 'T5',
    #        'P3', 'PZ', 'P4', 'T6', 'O1', 'OZ', 'O2', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'EX1', 'EX2', 'EX3']

    # loaded_model = pickle.load(open(self.filename, 'rb'))
    # result = loaded_model.score(X_test, y_test)
    # print(result)
    # assess_func(edf)
