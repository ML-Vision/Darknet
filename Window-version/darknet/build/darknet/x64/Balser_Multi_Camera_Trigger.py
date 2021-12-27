from pypylon import pylon
from pypylon import genicam
import numpy as np
import sys

countOfImagesToGrab = 2 # Number of images to be grabbed
maxCamerasToUse = 2 # Limits the amount of cameras used for grabbing
timeout = 5000 #max time to wait for grabbed image
serial_numbers = ['40018632', '40038871']

# The exit code of the sample application.
exitCode = 0

try:
    
    tlFactory = pylon.TlFactory.GetInstance()
    
    # get all attached devices
    devices = tlFactory.EnumerateDevices()
    
    # look for unique devices that match the serial numbers
    camera_devices = []
    for device in devices:
        serial = device.GetSerialNumber()
        print(serial)
        
        for sn in serial_numbers:
            if serial == sn:
                camera_devices.append(device)   
                serial_numbers.remove(serial)
                break                        
              
    camera_devices = tuple(camera_devices)
    
    # exit if no camera found
    if len(camera_devices) == 0:
        raise pylon.RuntimeException("No camera present.")
        
    print(str(len(camera_devices)) + ' cameras found.')

    # Create an array of instant cameras for the found devices and avoid exceeding a maximum number of devices.
    cam_array = pylon.InstantCameraArray(min(len(camera_devices), maxCamerasToUse))
        
    for i, camera in enumerate(cam_array):
        
        # Create an instant camera object
        camera.Attach(tlFactory.CreateDevice(camera_devices[i]))
    
        #camera name
        camera_name = '_'.join([camera.GetDeviceInfo().GetModelName(),
                                camera.GetDeviceInfo().GetSerialNumber()])
      
        camera.Open()

        # set camera parameters
        camera.MaxNumBuffer = 5 #count of buffers allocated for grabbing
        camera.TriggerSelector.SetValue('FrameStart')
        camera.TriggerMode.SetValue('On') #hardware trigger
        camera.TriggerSource.SetValue('Line1')
        camera.TriggerActivation.SetValue('RisingEdge')
        camera.StartGrabbingMax(countOfImagesToGrab)
        camera.ExposureAuto.SetValue('Off')
        camera.ExposureTime.SetValue(200)
        
        # Print the model name of the camera.
        print("Setup of camera ", camera_name, " complete.")
        
except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1        
    
try:  
    for i, camera in enumerate(cam_array):
        while camera.IsGrabbing():
            
            # Wait for an image and then retrieve it. A timeout of 5000 ms is used.
            grabResult = camera.RetrieveResult(timeout, pylon.TimeoutHandling_ThrowException)

            print("GrabSucceeded: ", grabResult.GrabSucceeded())

            grabResult.Release()
        camera.Close()

except genicam.GenericException as e:
    # Error handling.
    print("An exception occurred.")
    print(e.GetDescription())
    exitCode = 1

sys.exit(exitCode)