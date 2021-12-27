import cv2
from Parser import *
import pypylon.pylon as py
import Basler_Camera as Basler
from Detect_Model import Detect_Model as DM
def main():
    args = parser()
    check_arguments_errors(args)
    MYDM = DM(args)
    MYDM.Load_Model()
    SCs = Basler.get_cameras()
    while SCs[0].cam.IsGrabbing() or SCs[1].cam.IsGrabbing() :
        SCs[0].grabResult = SCs[0].cam.RetrieveResult(600000 , py.TimeoutHandling_ThrowException)
        SCs[1].grabResult = SCs[1].cam.RetrieveResult(600000 , py.TimeoutHandling_ThrowException)
        image1, image2 = None, None
        if SCs[0].grabResult.GrabSucceeded():
            image1 = SCs[0].get_Frame()
            Pimage1,fps1 = MYDM.predict(image1)
        if SCs[1].grabResult.GrabSucceeded():
            image2 = SCs[1].get_Frame()
            Pimage2,fps2 = MYDM.predict(image2)
        if image1 is not None:
            image1 = cv2.resize(image1, (617, 512))
            SCs[0].show_live(Pimage1)
            print("FPS1: {}".format(fps1))
        if image2 is not None:
            image2 = cv2.resize(image2, (617, 512))
            SCs[1].show_live(Pimage2)
            print("FPS2: {}".format(fps2))
if __name__ == "__main__":
    main()