from cv2 import *
class Streaming_channel():
    def __init__(self,num):
        self.channel = num
    def set_camera(self):
        self.camera = VideoCapture(self.channel,CAP_DSHOW)
    def get_Frame(self):
        ret,frame = self.camera.read()
        return frame
    def show_image(self):
        ret,frame = self.camera.read()
        imshow("Camera{}".format(self.channel), frame);
        ch = waitKey(1);
        if (ch != 'q') : key = ch;
    def show_live(self,image):
        imshow("Camera{}".format(self.channel), image);
        ch = waitKey(1);
        if (ch != 'q') : key = ch;
    def destory_camera(self):
        self.camera.release()