# this is the abstraction layer which converts the data fr the GUI to use

from Renderer import Renderer
from Predictor import Predictor
from Colorer import Colorer


class Abstraction:
    def __init__(self,filePath):
        self.result = []  #bad channels and result
        self.data = []      # raw data from edf as a array
        self.color = []     #the color array to feed to the renderer
        self.bad = []       #the list of bad channels
        self.powers = []    #powerrs of the different waves
        self.channelName = []   # name of different electrodes
        self.eegLength = 0      #length of the eeg
        self.r = 0              #the rendering object
        self.filePath = filePath    #absolute filepath for the edf file from GUI
    
    def __str__(self):
        return (self.filePath.split('\\')[-1])

    def get_data(self):
        # Gets the result from the SVM model
        p = Predictor(self.filePath)
        # Gets the result using the SVM model
        p.assess_func()
        #store result
        self.result = p.result_data
        self.data = p.raw_data      #store raw data
        self.channelName = p.header #store electrodes information for the GUI
        self.eegLength = len(p.raw_data)/256    #gets the length of the eeg in seconds
        self.bad = p.bad    # Bad channels in the EEG
        self.powers = p.powers  # power of different waves in the eeg
    
    def run(self): # the main loop
        self.get_data() 
        self.make_color()
        
    def make_color(self):
        c = Colorer()
        self.color = c.coder(self.data)
        self.r = Renderer(self.bad,self.color)
    
    def render(self):
        self.r.render() #start the rendering engine