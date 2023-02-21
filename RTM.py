import numpy as np
import numpy.linalg as nl
import matplotlib.pyplot as plt

class rvec:
    def __init__(self, x, a, z=0):
        self.x = x
        self.a = a
        self.vec = np.array([x,a])
        self.z = z

    def propagate(self, d):
        RTM = np.array([[1,d],[0,1]])
        vec = RTM@self.vec
        return rvec(vec[0], vec[1], self.z+d)

    def thick_lens(self, n1, n2, R1, R2, t):
        RTM1 = np.array([[1,0],[(n2-n1)/R2/n1,n2/n1]])
        RTM2 = np.array([[1,t],[0,1]])
        RTM3 = np.array([[1,0],[(n1-n2)/R1/n2,n1/n2]])
        vec = RTM1@(RTM2@(RTM3@self.vec))
        return rvec(vec[0], vec[1], self.z+t)

class rvec_list:
    def __init__(self, vec):
        self.rvecs = [vec]

    def s_x(self):
        l = []
        for vec in self.rvecs:
            l.append(vec.x)
        return l
    
    def s_z(self):
        l = []
        for vec in self.rvecs:
            l.append(vec.z)
        return l

    def range_z(self):
        return (self.rvecs[0].z, self.rvecs[-1].z)

    def __lshift__(self, vec):
        self.rvecs.append(vec)

    def __invert__(self):
        return self.rvecs[-1]

# MainEntry
n_air = 1.0
n_N_BK7 = 1.5106
rad_curv = 38.6
c_thick = 4.1
f = 74.8
fb = 72.0

for j in [(-1.3/2,'b'),(0,'g'),(1.3/2,'r')]:
    for i in np.linspace(-7,7,10):
        p = rvec(j[0],np.deg2rad(i))
        q = rvec_list(p)

        # Calculations
        q <<(~q).propagate(f)
        q <<(~q).thick_lens(n_air, n_N_BK7, rad_curv, -np.inf, c_thick)
        q <<(~q).propagate(2*fb)
        q <<(~q).thick_lens(n_air, n_N_BK7, np.inf, -rad_curv, c_thick)
        q <<(~q).propagate(f+20)

        # Draw
        z = np.linspace(q.range_z()[0],q.range_z()[1],100)
        x = np.interp(z,q.s_z(),q.s_x())
        plt.plot(z,x,j[1])

#plt.plot(q.s_z(),q.s_x(),'.r')
line_pos = np.zeros(2)
for i in [0,f,c_thick,fb,fb,c_thick,f]:
    line_pos += i
    plt.plot(line_pos,[-25.4/2,25.4/2],'k')
plt.show()
