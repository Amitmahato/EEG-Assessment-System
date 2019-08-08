class Objloader:
    def __init__(self):
        self.vertices = []
        self.index = []
    
    def loader(self,obj):
        for lines in open('./data/'+obj,'r'):
            if '#' in lines:
                continue
            points = lines.split()
            if not points:
                continue
            if points[0] == 'v':
                self.vertices.append([float(i) for i in points[1:4]])
            if points[0] == 'f':
                self.index.append([int(points[i].split('/')[0]) - 1 for i in range(1,4)])
        return self.vertices
