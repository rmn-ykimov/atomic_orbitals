import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import LightSource

# Define the grid
r = np.linspace(0, 5, 100)
theta = np.linspace(0, 2*np.pi, 100)
R, THETA = np.meshgrid(r, theta)

# Define the exact mathematical function for the s-orbital
Z = (1/np.sqrt(4*np.pi))*np.exp(-R/2)

# Create the plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(R*np.cos(THETA), R*np.sin(THETA), Z, cmap='rainbow')

# Add a colorbar
plt.colorbar()

# Add axis labels and a title
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.set_title('s-orbital')

# Add lighting to the image
ls = LightSource(azdeg=315, altdeg=45)
rgb = ls.shade(Z, plt.cm.rainbow)
ax.imshow(rgb, extent=[-5,5,-5,5], origin='lower')

# Show the plot
plt.show()
