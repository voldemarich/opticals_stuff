import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt
from os import path
from os import listdir
import time

pot_cascade = cv.CascadeClassifier('cascades/haarcascade_fullbody.xml')
imgpath = "upperbody/raw/"
savepath = "upperbody/boxed/"

start_time = time.time()

for i in listdir(imgpath):
    thispath = path.join(imgpath,i)
    try:
        img = cv.imread(thispath)
        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    except:
        continue

    bodies = pot_cascade.detectMultiScale(img)
    for (x, y, w, h) in bodies:
        img = cv.rectangle(img, (x,y),(x+w, y+h),(0,255,0),3)
    #cv.imwrite(path.join(savepath,i), img)
    #     plt.imshow(img)
    #     plt.show()
    #     break

print time