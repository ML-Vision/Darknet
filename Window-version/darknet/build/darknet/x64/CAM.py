import argparse
import os
import glob
import random
import darknet
import time
import cv2
import numpy as np
import darknet
from tkinter.constants import NONE
import pypylon.pylon as py
import win32api

# Custom Class
from Parser import *
from Detect_Model import *
import Basler_Camera as Basler
from Detect_Model import Detect_Model as DM
from image_show import Streaming_channel as stream

def one_Camera(args):
    Camera_Object = Basler.get_camera() # 카메라 객체
    MYDM = DM(args) # Detect Model 객체
    MYDM.Load_Model()
    maximum = 10
    index = 0
    
    # 결과 폴더 만들어 주기.
    if not os.path.isdir(args.model_name):
        print("없음")
        os.mkdir(args.model_name)
    else: print("있음")
    
    while Camera_Object.cam.IsGrabbing():    
        if index == maximum : break
        Camera_Object.grabResult = Camera_Object.cam.RetrieveResult(600000, py.TimeoutHandling_ThrowException)
        if Camera_Object.rabResult.GrabSucceeded():
            image = Camera_Object[0].get_Frame()
            image_name = f"{index}.jpg"
            get_img,fps = MYDM.predict(image)
            print("FPS: {}".format(fps))
            cv2.imwrite(os.path.join('./output', image_name),get_img, params=[cv2.IMWRITE_PNG_COMPRESSION,0]) 
            if not args.dont_show:
                get_img = cv2.resize(get_img, (617, 512))
                Camera_Object.show_live(get_img)
            index += 1
def web_cam(args):
    args = parser() # 매개변수 
    check_arguments_errors(args)
    
    MYDM = DM(args) # Detect Model
    MYDM.Load_Model()
    
    show = stream(0) # streamimg Channel 생성
    show.set_camera() # Camera 설정
    maximum = 10
    # 결과 폴더 만들어 주기.
    if not os.path.isdir(args.model_name):
        print("없음")
        os.mkdir(args.model_name)
    else: print("있음")
    
    index = 0
    
    while True:
        if index == maximum : break
        image = show.get_Frame()
        image_name = f"{index}.jpg"
        get_img,fps = MYDM.predict(image) # 판별결과, 속도
        print("FPS: {}".format(fps))
        cv2.imwrite(args.model_name + image_name, get_img)
        if not args.dont_show:
            show.show_live(get_img)
        index += 1
    
    
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # unconmment next line for an example of batch processing
    # batch_detection_example()
    args = parser()
    check_arguments_errors(args)
    #print(args)
    if parser().web_cam == False:
        if parser().camera_mode == "Double":
            one_Camera(args)
        else:
            one_Camera(args)
    else:
        if parser().camera_mode == "Double":
            web_cam(args)
        else:
            web_cam(args)
        