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
def parser():
    parser = argparse.ArgumentParser(description="YOLO Object Detection")
    parser.add_argument("--input", type=str, default="",
                        help="image source. It can be a single image, a"
                        "txt with paths to them, or a folder. Image valid"
                        " formats are jpg, jpeg or png."
                        "If no input is given, ")
    parser.add_argument("--batch_size", default=1, type=int,
                        help="number of images to be processed at the same time")
    parser.add_argument("--weights", default="yolov4.weights",
                        help="yolo weights path")
    parser.add_argument("--dont_show", action='store_true',
                        help="windown inference display. For headless systems")
    parser.add_argument("--ext_output", action='store_true',
                        help="display bbox coordinates of detected objects")
    parser.add_argument("--save_labels", action='store_true',
                        help="save detections bbox for each image in yolo format")
    parser.add_argument("--config_file", default="./cfg/yolov4.cfg",
                        help="path to config file")
    parser.add_argument("--data_file", default="./cfg/coco.data",
                        help="path to data file")
    parser.add_argument("--model_name", default="./CAM_Detections/No_model_name/",
                        help="path to data file")
    parser.add_argument("--web_cam", default=False, type=bool,
                        help="path to data file")
    parser.add_argument("--thresh", type=float, default=.25,
                        help="remove detections with lower confidence")
    return parser.parse_args()


def check_arguments_errors(args):
    assert 0 < args.thresh < 1, "Threshold should be a float between zero and one (non-inclusive)"
    if not os.path.exists(args.config_file):
        raise(ValueError("Invalid config path {}".format(os.path.abspath(args.config_file))))
    if not os.path.exists(args.weights):
        raise(ValueError("Invalid weight path {}".format(os.path.abspath(args.weights))))
    if not os.path.exists(args.data_file):
        raise(ValueError("Invalid data file path {}".format(os.path.abspath(args.data_file))))
    if args.input and not os.path.exists(args.input):
        raise(ValueError("Invalid image path {}".format(os.path.abspath(args.input))))


def check_batch_shape(images, batch_size):
    """
        Image sizes should be the same width and height
    """
    shapes = [image.shape for image in images]
    if len(set(shapes)) > 1:
        raise ValueError("Images don't have same shape")
    if len(shapes) > batch_size:
        raise ValueError("Batch size higher than number of images")
    return shapes[0]



def prepare_batch(images, network, channels=3):
    width = darknet.network_width(network)
    height = darknet.network_height(network)

    darknet_images = []
    for image in images:
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_resized = cv2.resize(image_rgb, (width, height),
                                   interpolation=cv2.INTER_LINEAR)
        custom_image = image_resized.transpose(2, 0, 1)
        darknet_images.append(custom_image)

    batch_array = np.concatenate(darknet_images, axis=0)
    batch_array = np.ascontiguousarray(batch_array.flat, dtype=np.float32)/255.0
    darknet_images = batch_array.ctypes.data_as(darknet.POINTER(darknet.c_float))
    return darknet.IMAGE(width, height, channels, darknet_images)


def image_detection(img,  network, class_names, class_colors, thresh):
    # Darknet doesn't accept numpy images.
    # Create one with image we reuse for each detect
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    darknet_image = darknet.make_image(width, height, 3)
    image_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                               interpolation=cv2.INTER_LINEAR)

    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.detect_image(network, class_names, darknet_image, thresh=thresh)
    darknet.free_image(darknet_image)
    image = darknet.draw_boxes(detections, image_resized, class_colors)
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB), detections


def batch_detection(network, images, class_names, class_colors,
                    thresh=0.25, hier_thresh=.5, nms=.45, batch_size=4):
    image_height, image_width, _ = check_batch_shape(images, batch_size)
    darknet_images = prepare_batch(images, network)
    batch_detections = darknet.network_predict_batch(network, darknet_images, batch_size, image_width,
                                                     image_height, thresh, hier_thresh, None, 0, 0)
    batch_predictions = []
    for idx in range(batch_size):
        num = batch_detections[idx].num
        detections = batch_detections[idx].dets
        if nms:
            darknet.do_nms_obj(detections, num, len(class_names), nms)
        predictions = darknet.remove_negatives(detections, class_names, num)
        images[idx] = darknet.draw_boxes(predictions, images[idx], class_colors)
        batch_predictions.append(predictions)
    darknet.free_batch_detections(batch_detections, batch_size)
    return images, batch_predictions


def image_classification(image, network, class_names):
    width = darknet.network_width(network)
    height = darknet.network_height(network)
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image_resized = cv2.resize(image_rgb, (width, height),
                                interpolation=cv2.INTER_LINEAR)
    darknet_image = darknet.make_image(width, height, 3)
    darknet.copy_image_from_bytes(darknet_image, image_resized.tobytes())
    detections = darknet.predict_image(network, darknet_image)
    predictions = [(name, detections[idx]) for idx, name in enumerate(class_names)]
    darknet.free_image(darknet_image)
    return sorted(predictions, key=lambda x: -x[1])


def convert2relative(image, bbox):
    """
    YOLO format use relative coordinates for annotation
    """
    x, y, w, h = bbox
    height, width, _ = image.shape
    return x/width, y/height, w/width, h/height


def save_annotations(name, image, detections, class_names):
    """
    Files saved with image_name.txt and relative coordinates
    """
    file_name = os.path.splitext(name)[0] + ".txt"
    with open(file_name, "w") as f:
        for label, confidence, bbox in detections:
            x, y, w, h = convert2relative(image, bbox)
            label = class_names.index(label)
            f.write("{} {:.4f} {:.4f} {:.4f} {:.4f} {:.4f}\n".format(label, x, y, w, h, float(confidence)))

def set_saved_video(size):
    fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    fps = int(2)
    video = cv2.VideoWriter('output.avi', fourcc, fps, size)
    return video

def main(cam,converter):
    args = parser()
    check_arguments_errors(args)

    random.seed(3)  # deterministic bbox colors
    network, class_names, class_colors = darknet.load_network(
        args.config_file,
        args.data_file,
        args.weights,
        batch_size=args.batch_size
    )
    count = 0
    maximum = 10
    video = set_saved_video((cam.Width.GetValue(),cam.Height.GetValue()))
    if not video.isOpened():
        print('File open failed!')
        cam.release()
        exit()
    index = 0
    
    # 결과 폴더 만들어 주기.
    if not os.path.isdir(args.model_name):
        print("없음")
        os.mkdir(args.model_name)
    else: print("있음")
    
    while cam.IsGrabbing():    
        if count == maximum : break
        grabResult = cam.RetrieveResult(600000, py.TimeoutHandling_ThrowException)
        if grabResult.GrabSucceeded():
            image = converter.Convert(grabResult)
            img = image.GetArray()
            image_name = f"{index}.jpg"
            prev_time = time.time()
            get_img, detections = image_detection(
                img, network, class_names, class_colors, args.thresh
                )
            if args.save_labels:
                save_annotations(image_name, image, detections, class_names)
            darknet.print_detections(detections, args.ext_output)
            fps = int(1/(time.time() - prev_time))
            print("FPS: {}".format(fps))
            cv2.imwrite(os.path.join('./output', str(count)+'.jpg'),get_img, params=[cv2.IMWRITE_PNG_COMPRESSION,0]) 
            video.write(get_img)
            if not args.dont_show:
                cv2.imshow('Inference', get_img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            index += 1
        
def camera_seting():
    cam = NONE
    converter = NONE
    try:
        tlf = py.TlFactory.GetInstance()
        cam = py.InstantCamera(tlf.CreateFirstDevice())
        cam.Open()
    except:
        print("No Camera")
        return NONE,NONE
    try:
        converter = py.ImageFormatConverter()
        converter.OutputPixelFormat = py.PixelType_BGR8packed
        converter.OutputBitAlignment = py.OutputBitAlignment_MsbAligned
        cam.RegisterConfiguration(py.ConfigurationEventHandler(), py.RegistrationMode_ReplaceAll, py.Cleanup_Delete)
        cam.MaxNumBuffer = 4
        
        cam.TriggerSelector.SetValue('FrameStart')
        cam.AcquisitionMode.SetValue('Continuous')

        cam.TriggerMode.SetValue('On')

        cam.TriggerSource.SetValue('Line1')

        cam.TriggerActivation.SetValue('RisingEdge')

        cam.TriggerDelayAbs.SetValue(10.0)
        cam.PixelFormat.SetValue('Mono8')

        cam.StartGrabbing(py.GrabStrategy_OneByOne)
        return cam,converter
    except:
        return NONE,NONE

def web_cam():
    args = parser()
    check_arguments_errors(args)

    random.seed(3)  # deterministic bbox colors
    network, class_names, class_colors = darknet.load_network(
        args.config_file,
        args.data_file,
        args.weights,
        batch_size=args.batch_size
    )
    count = 0
    maximum = 10
    cam = cv2.VideoCapture(0)
    print("--------------------------------",cam)
    # 결과 폴더 만들어 주기.
    if not os.path.isdir(args.model_name):
        print("없음")
        os.mkdir(args.model_name)
    else: print("있음")
    
    index = 0
    
    while True:
        ret,frame = cam.read()
        image_name = f"{index}.jpg"
        image = frame
        prev_time = time.time()
        get_img, detections = image_detection(
            image, network, class_names, class_colors, args.thresh
        )
        if args.save_labels:
            save_annotations(image_name, image, detections, class_names)
        darknet.print_detections(detections, args.ext_output)
        fps = int(1/(time.time() - prev_time))
        print("FPS: {}".format(fps))
        cv2.imwrite(args.model_name + str(index) + '.jpg', get_img)
        if not args.dont_show:
            cv2.imshow('Inference', get_img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        index += 1
    
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # unconmment next line for an example of batch processing
    # batch_detection_example()
    if(parser().web_cam == False):
        cam,converter = camera_seting()
        if(cam == NONE):
            win32api.MessageBox(0, 'NoCamera', 'CAM.py')
            exit()
        main(cam,converter)
    else:
        web_cam()
