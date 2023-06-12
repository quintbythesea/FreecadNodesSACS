import math
import numpy as np

steel_dens = 7850

class tube:

    def __init__(self, name:str,diam:float,tube_len:float,tube_th:float,tube_pos:list,tube_dir=None):
        self.name = name
        self.diam = diam
        self.th = tube_th
        self.len = tube_len
        self.dir=tube_dir
        self.pos=tube_pos

    @property
    def vol(self):
        d = self.diam - 2 * self.th
        return math.pi * (self.diam ** 2 - d ** 2) * 0.25 * 10 ** -6

    @property
    def weight(self):
        return round(self.vol*steel_dens,0)

    def info(self):
            return f"Name:  {self.name} and id: {self.id} "

def dump(obj):
    for k, v in obj.__dict__.items():
        print(k, v)

c1 = tube('c1',273,1000,6.35,[0,0,0],[1,0,0])

print (c1.weight)

c1.th=20
print(c1.th,c1.weight)







# Define the position and orientation of the cylinders
cylinder1_pos = np.array([0, 0, 0])
cylinder2_pos = np.array([0, 0, 0])
cylinder3_pos = np.array([0, 0, ])
cylinder4_pos = np.array([2, 2, 0])

cylinder1_orientation = np.array([1, 0, 0])
cylinder2_orientation = np.array([0, 1, 0])
cylinder3_orientation = np.array([0, 0, 1])
cylinder4_orientation = np.array([1, 1, 0])

# Define the function to calculate the COG of a cylinder
def cylinder_cog(height, radius):
    return np.array([0, 0, height/2])

# Calculate the COG of each cylinder
