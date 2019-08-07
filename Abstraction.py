# import pyop
# from Renderer import Renderer
# badch = [1,5,8,3]
# c = Renderer(badch)
# c.render()
from Renderer import Renderer
from Predictor import Predictor
from Colorer import Colorer


class Abstraction:
    def __init__(self,filePath):
        self.result = []
        self.data = []
        self.color = []
        self.bad = []
        self.powers = []
        self.eegLength = 0
        self.r = 0
        self.filePath = filePath
    
    def __str__(self):
        return (self.filePath.split('\\')[-1])

    def get_data(self):
        p = Predictor(self.filePath)
        p.assess_func()
        self.result = p.result_data
        self.data = p.raw_data
        self.eegLength = len(p.raw_data)/256
        self.bad = p.bad
        self.powers = p.powers
    
    def run(self):
        self.get_data()
        self.make_color()
        
    def make_color(self):
        c = Colorer()
        self.color = c.coder(self.data)
        self.r = Renderer(self.bad,self.color)
    
    def render(self):
        self.r.render()

# if __name__ == "__main__":  
#     a = Abstraction('00408')
#     a.render()
