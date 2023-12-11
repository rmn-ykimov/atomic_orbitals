import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

r = np.linspace(0, 5, 100)
theta = np.linspace(0, 2*np.pi, 100)
R, THETA = np.meshgrid(r, theta)

# Defining the s-orbital function
Z = (1/np.sqrt(4*np.pi))*np.exp(-R/2)

# Creating a 3D plot
fig = plt.figure(figsize=(8, 6))
ax = fig.add_subplot(111, projection='3d')

# Adding lighting
ls = LightSource(azdeg=315, altdeg=45)
colors = ls.shade(Z, cmap=plt.cm.rainbow, vert_exag=0.1, blend_mode='soft')

# Drawing the surface with lighting
surf = ax.plot_surface(R*np.cos(THETA), R*np.sin(THETA), Z, facecolors=colors, cmap='rainbow')

# Setting the appearance of the axes
ax.grid(False)
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('s-orbital')

# Adding a color scale
plt.colorbar(surf, shrink=0.5, aspect=5)

# Displaying the plot
plt.show()
