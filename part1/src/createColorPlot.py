import matplotlib.pyplot as plt
from mpl_toolkits import mplot3d


def create_color_plot(palette):
    x = []
    y = []
    z = []
    ax = plt.axes(projection = '3d')

    colors = []
    for i in palette:
        r = i[0]
        x.append(r)

        g = i[1]
        y.append(g)

        b = i[2]
        z.append(b)

        colors.append((r/255, g/255, b/255))

    ax.scatter(x,y,z, c = colors)
    plt.show()