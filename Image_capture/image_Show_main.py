import os
import cv2
import pypylon.pylon as py
import Basler_Camera as Basler
def main():
    Camera_Object = Basler.get_camera() # 카메라 객체
    maximum = 10
    index = 0
    
    while Camera_Object.cam.IsGrabbing():    
        if index == maximum : break
        Camera_Object.grabResult = Camera_Object.cam.RetrieveResult(600000, py.TimeoutHandling_ThrowException)
        if Camera_Object.rabResult.GrabSucceeded():
            image = Camera_Object[0].get_Frame()
            get_img = cv2.resize(get_img, (617, 512))
            Camera_Object.show_live(get_img)
            index += 1

if __name__ == "__main__":
    main()