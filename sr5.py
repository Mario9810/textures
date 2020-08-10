import struct
from OBJ import obj
import ops as op
#-------------------------------------------------------------------------

def char(c):
    # 1 byte
    return struct.pack('=c', c.encode('ascii'))

def word(w):
    # 2 bytes
    return struct.pack('=h',w)

def dword(d):
    # 4 bytes
    return struct.pack('=l',d)

def color(r, g, b):
    return bytes([int(b), int(g), int(r)])

def baryCoords(A, B, C, P):
    # u es para la A, v es para B, w para C
    try:
        u = ( ((B[1] - C[1])*(P[0]- C[0]) + (C[0] - B[0])*(P[1]- C[1]) ) /
              ((B[1] - C[1])*(A[0] - C[0]) + (C[0] - B[0])*(A[1] - C[1])) )

        v = ( ((C[1] - A[1])*(P[0]- C[0]) + (A[0] - C[0])*(P[1]- C[1]) ) /
              ((B[1] - C[1])*(A[0] - C[0]) + (C[0] - B[0])*(A[1] - C[1])) )

        w = 1 - u - v
    except:
        return -1, -1, -1

    return u, v, w

#--------------------------------------------------------------------
clear = color(0,0,0)

class Bitmap(object):
    def __init__(self, width, height):
        self.width = width 
        self.height = height 
        self.inicialColor = clear 
        self.glClear()
        self.Clear(0,0,0)
        self.__VPStartX = 0
        self.__VPStartY = 0
        self.__VPSizeX = 0
        self.__VPSizeY = 0
        self.__name = "image.bmp"
    def glClear(self):
        self.pixel = [
            [clear for x in range(self.width)]
            for y in range(self.height)
        ]
        self.zbuffer = [ [ -float('inf') for x in range(self.width)] for y in range(self.height) ]
    def Clear(self,r,g,b):
        self.pixel = [
            [clear for x in range(self.width)]
            for y in range(self.height)
        ]

    def write(self, filename):
        archivo = open(filename, 'wb')

        archivo.write(bytes('B'.encode('ascii')))
        archivo.write(bytes('M'.encode('ascii')))

        archivo.write(dword(14 + 40 + self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(14 + 40))

        archivo.write(dword(40))
        archivo.write(dword(self.width))
        archivo.write(dword(self.height))
        archivo.write(word(1))
        archivo.write(word(24))
        archivo.write(dword(0))
        archivo.write(dword(self.width * self.height * 3))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))
        archivo.write(dword(0))

        for x in range(self.height):
            for y in range(self.width):
                archivo.write(self.pixel[x][y])


        archivo.close()
    
    def glViewPort(self,x,y,width,height):
        self.__VPStartX = x
        self.__VPStartY = y
        self.__VPSizeX = width
        self.__VPSizeY = height

    
    def glClearColor(self,r,g,b):
        self.Clear(int(r*255),int(g*255),int(b*255))
    
    def point(self, x, y):
        self.pixel[y][x] = self.inicialColor    
    
    def glVertex(self,x,y):
        VPX = int(self.__VPSizeX*(x+1)*(1/2)+self.__VPStartX)
        VPY = int(self.__VPSizeY*(y+1)*(1/2)+self.__VPStartY)
        self.point(VPX,VPY)
    def glLine(self,x1,y1,x2,y2):
        x1 = int(self.__VPSizeX*(x1+1)*(1/2)+self.__VPStartX)
        y1 = int(self.__VPSizeY*(y1+1)*(1/2)+self.__VPStartY)
        x2 = int(self.__VPSizeX*(x2+1)*(1/2)+self.__VPStartX)
        y2 = int(self.__VPSizeY*(y2+1)*(1/2)+self.__VPStartY)
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        pendiente = dy > dx
        if pendiente:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if (x1 > x2):
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        offset = 0
        umbral = dx
        y = y1
        for x in range(x1, x2 + 1):
            if pendiente:
                self.point(y,x)
            else:
                self.point(x,y)

            offset += dy * 2
            if offset >= umbral:
                y +=1 if y1 < y2 else -1
                umbral += 2 * dx
    def glLineWin(self,x1,y1,x2,y2):
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        pendiente = dy > dx
        if pendiente:
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        if (x1 > x2):
            x1, x2 = x2, x1
            y1, y2 = y2, y1
        dy = abs(y2 - y1)
        dx = abs(x2 - x1)
        offset = 0
        umbral = dx
        y = y1
        for x in range(x1, x2 + 1):
            if pendiente:
                self.point(y,x)
            else:
                self.point(x,y)

            offset += dy * 2
            if offset >= umbral:
                y +=1 if y1 < y2 else -1
                umbral += 2 * dx
    def glColor(self,r,g,b):
        self.inicialColor = color(int(r*255),int(g*255),int(b*255))
    
    def glFinish(self):
        self.write(self.__name)
    
    def transform1(self, vertex, translate=(500,500,0), scale=(300,300,300)):
        
        return  (round(vertex[0] * scale[0]+ translate[0]),
                  round(vertex[1] * scale[1]+ translate[1]),
                  round(vertex[2] * scale[2]+ translate[2]))
   
    def loadModel(self, filename, translate, scale,normobj = False):
        model = obj(filename)
        light = [0,0,1]
        for face in model.faces:

            vertCount = len(face)
            if normobj:
                for vert in range(vertCount):
                    
                    v0 = model.vertices[ int(face[vert][0]) - 1 ]
                    v1 = model.vertices[ int(face[(vert + 1) % vertCount][0]) - 1]

                    x0 = int(v0[0] * scale[0]  + translate[0])
                    y0 = int(v0[1] * scale[1]  + translate[1])
                    x1 = int(v1[0] * scale[0]  + translate[0])
                    y1 = int(v1[1] * scale[1]  + translate[1])

                    self.glLineWin(x0, y0, x1, y1)
            else:
                v0 = model.vertices[ face[0][0] - 1 ]
                v1 = model.vertices[ face[1][0] - 1 ]
                v2 = model.vertices[ face[2][0] - 1 ]
                
                v0 = self.transform1(v0,translate, scale)
                v1 = self.transform1(v1,translate, scale)
                v2 = self.transform1(v2,translate, scale)

                #polycolor = color(random.randint(0,255) / 255,
                #                  random.randint(0,255) / 255,
                #                  random.randint(0,255) / 255)

                normal = op.cross(op.subtract(v1,v0), op.subtract(v2,v0))
               
                normal =op.divide(normal, op.norm(normal))
                intensity = op.dot(normal, light)

                if intensity >=0:
                    self.triangle_bc(v0,v1,v2, self.glColor(intensity, intensity, intensity))

                if vertCount > 3: #asumamos que 4, un cuadrado
                    v3 = model.vertices[ face[3][0] - 1 ]
                    
                    if intensity >=0:
                        self.triangle_bc(v0,v2,v3, color(intensity, intensity, intensity))

    def IsInside(self,x,y,poly):
        num = len(poly)
        i = 0
        j = num - 1
        c = False
        for i in range(num):
            if ((poly[i][1] > y) != (poly[j][1] > y)) and \
                    (x < poly[i][0] + (poly[j][0] - poly[i][0]) * (y - poly[i][1]) /
                                    (poly[j][1] - poly[i][1])):
                c = not c
            j = i
        return c
    
    def FillPolygon(self,poly):
        for x in range(self.width):
            for y in range(self.height):
                In = self.IsInside(x,y,poly)
                if In:
                    self.point(x,y)
    def triangle(self, A, B, C, color = None):
        
        def flatBottomTriangle(v1,v2,v3):
            #self.drawPoly([v1,v2,v3], color)
            for y in range(v1[1], v3[1]+ 1):
                xi = round( v1[0]+ (v3[0]- v1[0])/(v3[1]- v1[1]) * (y - v1[1]))
                xf = round( v2[0]+ (v3[0]- v2[0])/(v3[1]- v2[1]) * (y - v2[1]))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.point(x,y)

        def flatTopTriangle(v1,v2,v3):
            for y in range(v1[1], v3[1]+ 1):
                xi = round( v2[0]+ (v2[0]- v1[0])/(v2[1]- v1[1]) * (y - v2[1]))
                xf = round( v3[0]+ (v3[0]- v1[0])/(v3[1]- v1[1]) * (y - v3[1]))

                if xi > xf:
                    xi, xf = xf, xi

                for x in range(xi, xf + 1):
                    self.point(x,y)

        # A[1] <= B[1] <= Cy
        if A[1] > B[1]:
            A, B = B, A
        if A[1] > C[1]:
            A, C = C, A
        if B[1] > C[1]:
            B, C = C, B

        if A[1] == C[1]:
            return

        if A[1] == B[1]: #En caso de la parte de abajo sea plana
            flatBottomTriangle(A,B,C)
        elif B[1] == C[1]: #En caso de que la parte de arriba sea plana
            flatTopTriangle(A,B,C)
        else: #En cualquier otro caso
            # y - y1 = m * (x - x1)
            # B[1] - A[1] = (C[1] - A[1])/(C[0] - A[0]) * (D[0]- A[0])
            # Resolviendo para D[0]
            x4 = A[0] + (C[0] - A[0])/(C[1] - A[1]) * (B[1] - A[1])
            D = (round(x4), B[1])
            flatBottomTriangle(D,B,C)
            flatTopTriangle(A,B,D)
    def triangle_bc(self, A, B, C, color = None):
        #bounding box
        minX = min(A[0], B[0], C[0])
        minY = min(A[1], B[1], C[1])
        maxX = max(A[0], B[0], C[0])
        maxY = max(A[1], B[1], C[1])

        for x in range(minX, maxX + 1):
            for y in range(minY, maxY + 1):
                u, v, w = baryCoords(A, B, C, (x, y))

                if u >= 0 and v >= 0 and w >= 0:

                    z = A[2] * u + B[2] * v + C[2] * w

                    if z > self.zbuffer[y][x]:
                        self.point(x, y)
                        self.zbuffer[y][x] = z


r = Bitmap(1000,1000)

r.glViewPort(20,20,640,480)
r.loadModel('model.obj', (500,500,500 ), (300,300,300) )
r.glFinish()