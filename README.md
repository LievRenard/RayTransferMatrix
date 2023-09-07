# RayTransferMatrix

A library for calculate Ray Transfrom Matrix.

## Usage

![](https://upload.wikimedia.org/wikipedia/commons/thumb/5/5e/RayTransferMatrixDefinitions.svg/1920px-RayTransferMatrixDefinitions.svg.png)

### class rvec(x, a, z = 0)
A class of ray vector with z(propagation direction) coordinate.

x : scalar

- X coordinate from propagation axis

a : scalar

- Beam propagation angle from propagation axis. Use radian unit

z : scalar

- Propagated(z) position

### rvec.propagate(self, d)
Calculates beam propagation for length d.

d : scalar

- Propagation length

Return : rvec

- Ray vector after d propagation.

### rvec.thick_lens(self, n1, n2, R1, R2, t)
Calculates refraction after thick lens.

n1 : scalar

- Refractive index of outside of lens.

n2 : scalar

- Refractive index of lens.

R1 : scalar

- Curvature of front side of lens. Positive for convex lens.

R2 : scalar

- Curvature of back side of lens. Negative for convex lens.

t : scalar

- Centre thickness of lens.

Return : rvec

- Ray vector at back side of lens.

### rvec.thin_lens(self, f)
Calculates refraction after thin lens.

f : scalar

- Focal length of thin lens. Positive for convex lens.

Return : rvec

- Ray vector at back side of lens.

## Example

4F system with 1" lenses with 10cm focus
```python
import numpy as np
import matplotlib.pyplot as plt
import RTM

n_air = 1.0
n_N_BK7 = 1.5106
rad_curv = 38.6
c_thick = 4.1
f = 74.8
fb = 72.0

# Length unit = mm
for j in [(-1.3/2,'b'),(0,'g'),(1.3/2,'r')]: #beam start point
    for i in np.linspace(-7,7,10): #beam angle (deg)
        p = [RTM.rvec(j[0],np.deg2rad(i))]

        # Calculations
        p.append(p[-1].propagate(f))
        p.append(p[-1].thick_lens(n_air, n_N_BK7, rad_curv, -np.inf, c_thick))
        p.append(p[-1].propagate(2*fb))
        p.append(p[-1].thick_lens(n_air, n_N_BK7, np.inf, -rad_curv, c_thick))
        p.append(p[-1].propagate(f+20))

        # Draw
        z = np.linspace(p[0].z,p[-1].z,100)
        x = np.interp(z,[rv.z for rv in p],[rv.x for rv in p])
        plt.plot(z,x,j[1])

line_pos = np.zeros(2)
for i in [0,f,c_thick,fb,fb,c_thick,f]:
    line_pos += i
    plt.plot(line_pos,[-25.4/2,25.4/2],'k')
plt.show()
```

Result:

![](Figure_1.png)
