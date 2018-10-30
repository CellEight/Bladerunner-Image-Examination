import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import speech_recognition as sr
import re, cv2, sys

def loadImage(filename):
    return cv2.imread(filename)

def overlayGrid(n,m,img,col):
    #get dimensions of img
    x = img.shape[0]
    y = img.shape[1]
    #x/n, y/m and floor to get grid distance
    dx = int(np.ceil(x/n))
    dy = int(np.ceil(y/m))
    #draw lines onto the image in the apropriate way
    t = int(np.ceil(max(x,y)/1000))
    for i in range(1,n):
        for j in range((i*dx),(i*dx)+t):
            img[j,range(y)] = col
    for k in range(1,m):
        for l in range((k*dy),(k*dy)+t):
            img[range(x),l] = col
        #print(img[range(x),j*dy])
    cv2.imwrite("out.jpg",img)
    return img

def gridZoom(a,b,n,m,img):
    #get dimensions of img
    x = img.shape[0]
    y = img.shape[1]
    #x/n, y/m and floor to get grid distance
    dx = int(np.ceil(x/n))
    dy = int(np.ceil(y/m))
    img = img[((a-1)*dx):(a*dx),((b-1)*dy):(b*dy)]
    return img

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        audioData = r.listen(source)
        print("Got audio, now to Recognize...")
        try:
            text = r.recognize_google(audioData)
            return text
        except sr.UnknownValueError:
            print("Undecipherable")
        except sr.RequestError as e:
            print("Error: {0}".format(e))
    return ""

def imageUpdate(*args):
    """Function that is looped over by matplotlib inorder to
    update the image being shown on the screen"""
    global im, img, filename, n, m
    print("Listening...")
    data = listen()
    data = data.lower()
    print(data)
    #if data == "black and white":
    #    img = loadImage(filename)
    #    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #    im = plt.imshow(img,cmap='gray',animated=True)
    if data == "zoom out":
        img = loadImage(filename)
        im = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),animated=True)
    elif "show grid" in data:
        if "white" in data:
            im = plt.imshow(cv2.cvtColor(overlayGrid(5,5,img,255), cv2.COLOR_BGR2RGB),animated=True)
        else:
            im = plt.imshow(cv2.cvtColor(overlayGrid(5,5,img,0), cv2.COLOR_BGR2RGB),animated=True)
    #elif re.search(r"show\s[0-9]*\sby\s[0-9]\sgrid",data):
    #    string = re.search(r"show\s[0-9]*\sby\s[0-9]\sgrid",data).group()
    elif "zoom" in data and re.search(r"x\s*[1-9]+",data) and re.search(r"y\s*[1-9]+",data):
        x = int(re.search(r"[0-9]+", re.search(r"x\s*[0-9]+",data).group()).group())
        y = int(re.search(r"[0-9]+", re.search(r"y\s*[0-9]+",data).group()).group())
        img = gridZoom(x,y,n,m,img)
        im = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),animated=True)
    return im,

def init():
    return im,

filename = str(sys.argv[1])
n = 5
m = 5
fig = plt.figure()
img = loadImage(filename)
im = plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB),animated=True)

ani = animation.FuncAnimation(fig, imageUpdate, interval=50,  init_func=init, blit=True)

plt.show()
