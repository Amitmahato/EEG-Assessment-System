from sklearn.metrics import classification_report, confusion_matrix
from sklearn import svm
from sklearn.model_selection import train_test_split
from numpy.fft import fft,fftfreq
from numpy import abs
import mne
import pickle
class Predictor:
    def __init__(self,filePath):
        # trained model
        self.filename = './data/trained_model.sav'
        self.raw_data = [] #raw eeg data
        self.result_data=[] #result data
        self.bad = [] #bad channel data
        self.header = [] #header information
        self.powers = [] # power of different waves
        self.file = filePath # filepath

    def assess_func(self):
        edf = mne.io.read_raw_edf(self.file) #read eeg file
        self.raw_data = edf.get_data().T # raw eeg voltage
        self.header = edf.ch_names # channel names
        svcclassifier = pickle.load(open(self.filename, 'rb')) # load svm model data
    
        alpha = []
        beta = []
        theta = []
        total = []

        for j in range(len(self.header)):
            fp2 = [self.raw_data[i][j] for i in range(len(self.raw_data))]
            freqs = fftfreq(len(fp2))
            freqs = freqs>0
            vals = fft(fp2)
            vals = abs(vals)
            vals = vals[freqs]
            scale = len(freqs)//256
            a=b=d=t=0
            # calculate the power of the channels differentiated by the frequency
            th = sum([i**2 for i in vals[4*scale:8*scale]])
            d = sum([i**2 for i in vals[1*scale:4*scale]])
            a = sum([i**2 for i in vals[8*scale:13*scale]])
            b = sum([i**2 for i in vals[13*scale:40*scale]])
            t = sum([i**2 for i in vals])-sum([i**2 for i in vals[49*scale:51*scale]]) - sum([i**2 for i in vals[:scale]])
            # append them to lists
            alpha.append(a)
            beta.append(b)
            theta.append(d+th)
            total.append(t)
            # Calculate more mumbo jumbo i.e. rhythm and noise
            rhythm=a+b+d+th
            noise=t-rhythm
            #  finally prediction and classification
            result = svcclassifier.predict([[rhythm,noise]])
            if result==0:
                self.result_data.append('bad')
                self.bad.append(j)
            else:
                self.result_data.append('good')
        at = sum(total)/len(total)
        self.powers.append(((sum(alpha)/len(alpha))/at)*100)
        self.powers.append(((sum(beta)/len(beta))/at)*100)
        self.powers.append(((sum(theta)/len(theta))/at)*100)
        f = self.powers
        self.powers.append(100-sum(f))
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
        # change bad to renderable
        x = [1,2,4,5,7,8,10,11,13,14,16,17,19,20,21,23]
        for i in temp:
            if i in x:
                new.append(x.index(i))
        self.bad = new
