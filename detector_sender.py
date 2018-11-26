# coding: utf-8

import numpy as np
import cv2
import time
import threading, Queue, os
import os
import datetime
from PIL import Image
from focal_sizes import exif, coordinates, measures
import requests
from math import pi

path_to_read = './demo/rawdata'
path_to_little = './demo/little'

def send_coords(x,y):
    resulting = {}
    resulting["date"] = datetime.datetime.now().isoformat()
    resulting["provider"] = "provider1"
    resulting["objects"] = [{"type":"human", "x":x, "y":y}]
    requests.post("http://localhost:3000/objects", json=resulting)

def inside(r, q):
    rx, ry, rw, rh = r
    qx, qy, qw, qh = q
    return rx > qx and ry > qy and rx + rw < qx + qw and ry + rh < qy + qh


def process_detections(img_name, rects):
    tagcloud = exif.get_tagcloud(img_name)
    matrix_pixel_x, matrix_pixel_y = exif.get_dims(tagcloud)
    matrix_mm_x, matrix_mm_y = exif.get_matrix_mm()
    focal = exif.get_focal_len(tagcloud)
    realsize_mm_y = 1800.0

    for x, y, w, h in rects:
        # the HOG detector returns slightly larger rectangles than the real objects.
        # so we slightly shrink the rectangles to get a nicer output.
        pad_w, pad_h = int(0.15 * w), int(0.05 * h)
        x_begin = x
        x_end = x+w
        pixelsize_y = h
        meas = measures.full_collection(x_begin,x_end,matrix_mm_x,matrix_pixel_x,
                        realsize_mm_y,
                        pixelsize_y,
                        matrix_mm_y,
                        matrix_pixel_y,
                        focal)
        camera = {}

        camera["x"] = 32000.0
        camera["y"] = 20300.0
        camera["yaw"] = 3 * pi / 2
        coords = coordinates.angle_to_coords(camera["x"], camera["y"], meas["distance_z"], meas["x_angle"], camera["yaw"])
        print x, y, x+w, y+h, img_name, meas["distance_z"], coords
        send_coords(round(coords[0]/1000.0,2), round(coords[1]/1000.0,2))



def findPeople(img_name):
    p_img = Image.open(img_name)
    r_img = p_img#.resize((800, 533), Image.ANTIALIAS)
    r_img_name = img_name#path_to_little + img_name.split("/")[-1]
    #r_img.save(r_img_name)

    s = datetime.datetime.now()
    hog = cv2.HOGDescriptor()
    hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
    # cap=cv2.VideoCapture('vid.avi')
    # img = cv2.imread('/home/sergi/projects/hren/opencv/photos_ds/IMG_2214.JPG',cv2.IMREAD_COLOR)
    img = cv2.imread(r_img_name, cv2.IMREAD_COLOR)
    # while True:
    # _,frame=cap.read()
    found, w = hog.detectMultiScale(img, winStride=(11, 11), padding=(8, 8), scale=1.05)
    # print found
    # print w
    process_detections(img_name, found)
    # cv2.imshow('feed',img)
    e = datetime.datetime.now()
    d = e - s

for i in os.listdir(path_to_read):
    findPeople(os.path.join(path_to_read, i))  # передаем данные в нашу функцию


# this is example of commit just for Loycerton