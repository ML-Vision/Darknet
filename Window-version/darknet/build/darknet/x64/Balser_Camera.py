import cv2
import pypylon.pylon as py
from pypylon import genicam
import sys
class Streaming_channel():
    def __init__(self,cam,name):
        self.cam = cam
        self.name = name
        self.grabResult = None
        self.converter = py.ImageFormatConverter()
        self.converter.OutputPixelFormat = py.PixelType_BGR8packed
        self.converter.OutputBitAlignment = py.OutputBitAlignment_MsbAligned
    def get_Frame(self):
        image = self.converter.Convert(self.grabResult)
        img = image.GetArray()
        return img
    def show_live(self,image):
        cv2.imshow(self.name, image);
        ch = cv2.waitKey(1);
        if (ch != 'q') : key = ch;
        
def camera_setting(cam,Line):
    cam = py.InstantCamera(cam)
    cam.Open()
    cam.RegisterConfiguration(py.ConfigurationEventHandler(), py.RegistrationMode_ReplaceAll, py.Cleanup_Delete)
    cam.MaxNumBuffer = 4
    
    cam.TriggerSelector.SetValue('FrameStart')
    cam.AcquisitionMode.SetValue('Continuous')

    cam.TriggerMode.SetValue('On')

    cam.TriggerSource.SetValue(Line)

    cam.TriggerActivation.SetValue('RisingEdge')

    cam.TriggerDelayAbs.SetValue(10.0)
    cam.PixelFormat.SetValue('Mono8')
    cam.StartGrabbing(py.GrabStrategy_OneByOne)
    return cam

def get_cameras():
    maxCamerasToUse = 2
    try:
        # Get the transport layer factory.
        tlFactory = py.TlFactory.GetInstance()

        # Get all attached devices and exit application if no device is found.
        devices = tlFactory.EnumerateDevices()
        print(len(devices))
        if len(devices) == 0:
            raise py.RuntimeException("No camera present.")

        # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
        cameras = py.InstantCameraArray(min(len(devices), maxCamerasToUse))

        cams = []
        # Create and attach all Pylon Devices.
        for i, cam in enumerate(cameras):
            name = "Right" if i == 0 else "Left"
            print(name)
            cur_cam = (tlFactory.CreateDevice(devices[i]))
            cam.Attach(cur_cam)
            cur_cam = camera_setting(cur_cam,"Line1")
            
            cams.append(Streaming_channel(cur_cam,name))
            # Print the model name of the camera.
            print("Using device ", cam.GetDeviceInfo().GetModelName())
        
        return cameras,cams
    
    except genicam.GenericException as e:
        # Error handling
        print("An exception occurred.", e.GetDescription())
        exitCode = 1
    # Comment the following two lines to disable waiting on exit.
    sys.exit(exitCode)