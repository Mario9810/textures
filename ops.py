def dot(x,y):
    return sum(x_i*y_i for x_i, y_i in zip(x, y))

def cross(u,v):  
    dim = len(u)
    s = []
    for i in range(dim):
        if i == 0:
            j,k = 1,2
            s.append(u[j]*v[k] - u[k]*v[j])
        elif i == 1:
            j,k = 2,0
            s.append(u[j]*v[k] - u[k]*v[j])
        else:
            j,k = 0,1
            s.append(u[j]*v[k] - u[k]*v[j])
    return s
def subtract(a,b):
    size = len(a)
    s = []
    for i in range(size):
        s.append(a[i]-b[i])
    return s

def norm(a):
    magnitude = 0
    for i in a:
        magnitude += i ** 2
    magnitude = magnitude ** 0.5
    return magnitude

def divide(a,b):
    size = len(a)
    s = []
    for i in range(size):
        s.append(a[i]/b)
    return s
