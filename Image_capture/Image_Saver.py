
import os
import cv2
import pypylon.pylon as py
import Basler_Camera as Basler
from image_show import Streaming_channel as stream

def one_Camera():
    Camera_Object = Basler.get_camera() # 카메라 객체
    maximum = 100
    index = 10
    
    # 결과 폴더 만들어 주기.
    if not os.path.isdir('./Images'):
        print("없음")
        os.mkdir('./Images')
    else: print("있음")
    
    while Camera_Object.cam.IsGrabbing():    
        if index == maximum : break
        Camera_Object.grabResult = Camera_Object.cam.RetrieveResult(600000, py.TimeoutHandling_ThrowException)
        if Camera_Object.grabResult.GrabSucceeded():
            image = Camera_Object.get_Frame()
            image_name = f"{index}.jpg"
            cv2.imwrite('./Images/{}.jpg'.format(image_name),image) 
            get_img = cv2.resize(image, (617, 512))
            Camera_Object.show_live(get_img)
            index += 1
one_Camera()