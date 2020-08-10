class obj(object):
    def __init__(self,filename):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.faces = []
        self.__filename = filename
        self.getData()
    def getData(self):
        f = open(self.__filename,'r')
        lines = f.readlines()
        
        for i in lines:
            #print(i)
            mode, data = i.split(" ",1)
            
            if mode == "f":
                self.faces.append([list(map(int,vert.split('/'))) for vert in data.split(' ')])
            
            if mode == "v":
                self.vertices.append(list(map(float,data.split(' '))))
        
        
        f.close()

