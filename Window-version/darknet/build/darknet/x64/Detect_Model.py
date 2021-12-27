import argparse
import os
import random
import darknet
import time
import cv2
import numpy as np
import darknet
from tkinter.constants import NONE
import pypylon.pylon as py

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

class Detect_Model():
    def __init__(self,args):
        self.args = args
        self.bbox_color = random.seed(3)
    def Load_Model(self):
        self.network, self.class_names, self.class_colors = darknet.load_network(
            self.args.config_file,
            self.args.data_file,
            self.args.weights,
            batch_size=self.args.batch_size
        )
    def predict(self,image):
        prev_time = time.time()
        get_img, detections = image_detection(
            image, self.network, self.class_names, self.class_colors, self.args.thresh
        )
        fps = int(1/(time.time() - prev_time))
        return get_img
