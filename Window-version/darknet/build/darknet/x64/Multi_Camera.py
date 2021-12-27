import os
import cv2
import threading as th

def get_camera_info():
    cv2.VideoCapture(0)

def Camera_Streaming():
    first = "start python Streaming_Camera0.py"
    second = "start python Streaming_Camera1.py"
    os.system(first)
    os.system(second)
    
Camera_Streaming()