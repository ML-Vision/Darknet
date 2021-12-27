from image_show import Streaming_channel as SC
from Detect_Model import Detect_Model as DM
from Parser import *

def main():
    args = parser()
    check_arguments_errors(args)
    MYDM = DM(args)
    MYDM.Load_Model()
    show1 = SC(0)
    show1.set_camera()
    show2 = SC(1)
    show2.set_camera()
    while(1):
        image1 = show1.get_Frame()
        image2 = show2.get_Frame()
        Pimage1 = MYDM.predict(image1)
        Pimage2 = MYDM.predict(image2)
        show1.show_live(Pimage1)
        show2.show_live(Pimage2)
        


if __name__ == "__main__":
    main()