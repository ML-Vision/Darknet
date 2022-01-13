import os
import cv2
from image_show import Streaming_channel as SC
def main():
    show1 = SC(0)
    show1.set_camera()
    i = 0
    print(os.path)
    while(1):
        image1 = show1.get_Frame()
        show1.show_live(image1)
        
        cv2.imwrite('./Images/output{}.jpg'.format(i), image1) 
        i += 1


if __name__ == "__main__":
    main()