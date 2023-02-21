import numpy as np
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