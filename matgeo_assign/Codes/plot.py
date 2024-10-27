import ctypes
import numpy as np
import matplotlib.pyplot as plt

# Load the shared library
lib = ctypes.CDLL('./section.so')

# Define the struct for point and section
class Point(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double),
                ("z", ctypes.c_double)]

class Section(ctypes.Structure):
    _fields_ = [("P", Point),
                ("Q", Point),
                ("R", Point),
                ("num_points", ctypes.c_int),
                ("points", ctypes.POINTER(Point)),
                ("k", ctypes.c_double)]

# Create a section instance
sect = Section()
sect.P = Point(3, 2, -4)
sect.Q = Point(5, 4, -6)
sect.R = Point(9, 8, -10)

# Set the number of points to 500
sect.num_points = 500

# Generate points
lib.Generate_points(ctypes.byref(sect))

# Extract points from the section
points = np.array([(sect.points[i].x, sect.points[i].y, sect.points[i].z) for i in range(sect.num_points)])

# Find k
lib.Find_k(ctypes.byref(sect))

# Print k value
print(f"Value of k: {sect.k}")

# Plotting
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot(points[:, 0], points[:, 1], points[:, 2], label='Line')

# Define points to denote with colors
points_to_label = {
    'P': {'point': sect.P, 'color': 'red'},
    'Q': {'point': sect.Q, 'color': 'green'},
    'R': {'point': sect.R, 'color': 'blue'}
}

# Plot and label P, Q, R with different colors
for label, info in points_to_label.items():
    point = info['point']
    color = info['color']
    ax.scatter(point.x, point.y, point.z, color=color, s=30, label=f'{label} ({point.x}, {point.y}, {point.z})')  # Adjusted size
    ax.text(point.x, point.y, point.z, f'{label}', color='black', fontsize=12)

# Setting labels
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.legend()
plt.title('3D Line from Points P, Q, R')
plt.savefig('../figs/fig.png')
plt.show()

# Free the allocated points in C
lib.free_points(ctypes.byref(sect))

