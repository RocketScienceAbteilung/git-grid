import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb, rgb_to_hsv
from mpl_toolkits.mplot3d import Axes3D
import gitgrid.gridcontroller.push as push

RGB_COLOR_TABLE = push.Push.color_table

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

V, H = np.mgrid[0:1:100j, 0:1:300j]
S = np.ones_like(V)
HSV = np.dstack((H, S, V))
RGB = hsv_to_rgb(HSV)
# plt.imshow(RGB, origin="lower", extent=[0, 255, 0, 1], aspect=150)

cols = RGB_COLOR_TABLE
val = rgb_to_hsv(cols / 255.)
ax.scatter(val[:, 0] * 255., val[:, 1], val[:, 2], c=cols / 255., s=100)

plt.xlabel("H")
plt.ylabel("V")
plt.title("$S_{HSV}=1$")
plt.show()
