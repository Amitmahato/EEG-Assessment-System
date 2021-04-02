
# here are the dependencies
from sklearn.metrics import classification_report, confusion_matrix
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
import pandas as pd
import matplotlib.pyplot as plt
from numpy.fft import fft, fftfreq
from numpy import abs
import mne


# In[2]:


# model fitting code part
svmdataarray = pd.read_csv('Training_data.csv')
svmdata = svmdataarray.drop('type', axis=1)
type_label = svmdataarray['type']


# In[3]:


X_train, X_test, y_train, y_test = train_test_split(
    svmdata, type_label, test_size=0.20)


# In[4]:


svclassifier = svm.SVC(kernel='linear', C=2**30)
svclassifier.fit(X_train, y_train)
y_pred = svclassifier.predict(X_test)
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))


# In[1]:


def assess_func(edf):

    raw_data = edf.get_data().T

    for j in range(32):
        fp2 = [raw_data[i][j] for i in range(len(raw_data))]
        freqs = fftfreq(len(fp2))
        freqs = freqs > 0
        vals = fft(fp2)
        vals = abs(vals)
        vals = vals[freqs]
        scale = len(freqs)//256
        a = b = d = t = 0
        th = sum([i**2 for i in vals[4*scale:8*scale]])
        d = sum([i**2 for i in vals[1*scale:4*scale]])
        a = sum([i**2 for i in vals[8*scale:13*scale]])
        b = sum([i**2 for i in vals[13*scale:40*scale]])
        t = sum([i**2 for i in vals])-sum([i**2 for i in vals[49 *
                                                              scale:51*scale]]) - sum([i**2 for i in vals[:scale]])

        rhythm = a+b+d+th
        noise = t-rhythm
        result = svclassifier.predict([[rhythm, noise]])
        if result == 0:
            print('Channel C'+str(j+1)+' is bad.')
        else:
            print('Channel C'+str(j+1)+' is good.')


# In[5]:


# the file select section
# here is numerical channel reference
# ['PG1', 'FP1', 'FP2', 'PG2', 'F7', 'F3', 'FZ', 'F4', 'F8', 'A1', 'T3', 'C3', 'CZ', 'C4', 'T4', 'A2', 'T5',
#        'P3', 'PZ', 'P4', 'T6', 'O1', 'OZ', 'O2', 'BP1', 'BP2', 'BP3', 'BP4', 'BP5', 'EX1', 'EX2', 'EX3']
edf = mne.io.read_raw_edf('00450.edf')
assess_func(edf)
