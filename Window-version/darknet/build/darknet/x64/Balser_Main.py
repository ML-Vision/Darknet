from Balser_Camera import *
import sys
def main():
    cameras,SCs = get_cameras()
    while SCs[0].cam.IsGrabbing() or SCs[1].cam.IsGrabbing() :
        SCs[0].grabResult = SCs[0].cam.RetrieveResult(600000 , py.TimeoutHandling_ThrowException)
        SCs[1].grabResult = SCs[1].cam.RetrieveResult(600000 , py.TimeoutHandling_ThrowException)
        image1, image2 = None, None
        if SCs[0].grabResult.GrabSucceeded():
            image1 = SCs[0].get_Frame()
        if SCs[1].grabResult.GrabSucceeded():
            image2 = SCs[1].get_Frame()
        if image1 is not None:
            image1 = cv2.resize(image1, (617, 512))
            SCs[0].show_live(image1)
        if image2 is not None:
            image2 = cv2.resize(image2, (617, 512))
            SCs[1].show_live(image2)
            
if __name__ == "__main__":
    main()