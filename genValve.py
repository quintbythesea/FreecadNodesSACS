import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np

# Define the properties of the cylinders
cylinder_height = 1
cylinder_radius = 0.5
cylinder_density = 1000

# Define the position and orientation of the cylinders
cylinder1_pos = np.array([0, 0, 0])
cylinder2_pos = np.array([2, 0, 0])
cylinder3_pos = np.array([0, 2, 0])
cylinder4_pos = np.array([2, 2, 0])

cylinder1_orientation = np.array([1, 0, 0])
cylinder2_orientation = np.array([0, 1, 0])
cylinder3_orientation = np.array([0, 0, 1])
cylinder4_orientation = np.array([1, 1, 0])

# Define the function to calculate the COG of a cylinder
def cylinder_cog(height, radius):
    return np.array([0, 0, height/2])

# Calculate the COG of each cylinder
cylinder1_cog = cylinder1_pos + np.dot(cylinder_cog(cylinder_height, cylinder_radius), cylinder1_orientation)
cylinder2_cog = cylinder2_pos + np.dot(cylinder_cog(cylinder_height, cylinder_radius), cylinder2_orientation)
cylinder3_cog = cylinder3_pos + np.dot(cylinder_cog(cylinder_height, cylinder_radius), cylinder3_orientation)
cylinder4_cog = cylinder4_pos + np.dot(cylinder_cog(cylinder_height, cylinder_radius), cylinder4_orientation)

# Calculate the total mass and COG of the system
total_mass = cylinder_density * np.pi * cylinder_radius**2 * cylinder_height * 4
total_cog = (cylinder1_cog + cylinder2_cog + cylinder3_cog + cylinder4_cog) / 4

# Create the 3D plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Add the cylinders to the plot
cylinder1 = plt.Circle((cylinder1_pos[0], cylinder1_pos[1]), cylinder_radius, color='r')
cylinder2 = plt.Circle((cylinder2_pos[0], cylinder2_pos[1]), cylinder_radius, color='g')
cylinder3 = plt.Circle((cylinder3_pos[0], cylinder3_pos[1]), cylinder_radius, color='b')
cylinder4 = plt.Circle((cylinder4_pos[0], cylinder4_pos[1]), cylinder_radius, color='y')

ax.add_patch(cylinder1)
ax.add_patch(cylinder2)
ax.add_patch(cylinder3)
ax.add_patch(cylinder4)

# Add the height of each cylinder as a third dimension
cylinder1_z = np.array([cylinder1_pos[2], cylinder1_pos[2] + cylinder_height])
cylinder2_z = np.array([cylinder2_pos[2], cylinder2_pos[2] + cylinder_height])
cylinder3_z = np.array([cylinder3_pos[2], cylinder3_pos[2] + cylinder_height])
cylinder4_z = np.array([cylinder4_pos[2], cylinder4_pos[2] + cylinder_height])

cylinder1 = ax.plot([cylinder1_pos[0], cylinder1_pos[0]], [cylinder1_pos[1], cylinder1_pos[1]], cylinder1_z, color='r')
#cylinder2 = ax.plot([cylinder2_pos[0],
