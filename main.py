import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LightSource

NUM_POINTS = 100
LIGHT_AZDEG = 315
LIGHT_ALTDEG = 45
PLOT_SIZE = (8, 6)


def s_orbital_function(r, theta_points=NUM_POINTS):
    """Calculate s-orbital values."""
    R, THETA = np.meshgrid(r, np.linspace(0, 2 * np.pi, theta_points))
    Z = (1 / np.sqrt(4 * np.pi)) * np.exp(-R / 2)
    return R, THETA, Z


def setup_lighting(Z, azdeg=LIGHT_AZDEG, altdeg=LIGHT_ALTDEG,
                   cmap=plt.cm.rainbow):
    """Set up lighting for the plot."""
    ls = LightSource(azdeg=azdeg, altdeg=altdeg)
    colors = ls.shade(Z, cmap=cmap, vert_exag=0.1, blend_mode='soft')
    return colors


def create_3d_plot(R, THETA, Z, colors, size=PLOT_SIZE):
    """Create and display a 3D plot."""
    fig = plt.figure(figsize=size)
    ax = fig.add_subplot(111, projection='3d')
    surf = ax.plot_surface(R * np.cos(THETA), R * np.sin(THETA), Z,
                           facecolors=colors, cmap='rainbow')
    ax.grid(False)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('s-orbital')
    plt.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()


# Main execution
r = np.linspace(0, 5, NUM_POINTS)
R, THETA, Z = s_orbital_function(r)
colors = setup_lighting(Z)
create_3d_plot(R, THETA, Z, colors)
