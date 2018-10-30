import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import cv2
fig = plt.figure()
i = 1
im = plt.imshow(cv2.imread('neuromancer'+str(i)+'.jpg'), animated=True)


def updatefig(*args):
    global i
    if i == 1:
        i = 2
    else:
        i = 1
    print(i)
    im = plt.imshow(cv2.cvtColor(cv2.imread('neuromancer'+str(i)+'.jpg'), cv2.COLOR_BGR2RGB),animated=True)
    #plt.imshow(im, interpolation = 'bicubic')
    return im

ani = animation.FuncAnimation(fig, updatefig, interval=50, blit=True)
plt.show()
