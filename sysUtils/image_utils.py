import cv2
import numpy as np


def xyxy2xywh(boxes):
    '''
    convert from (x1, y1, x2, y2) to (x1, y1, w, h)
    '''
    boxes[:, 2] = boxes[:, 2] - boxes[:, 0]
    boxes[:, 3] = boxes[:, 3] - boxes[:, 1]
    return boxes



def getMask(width, height):
    mask = cv2.imread('tracking/mask.jpg', 0)
    mask = cv2.resize(mask, (width, height))
    mask = mask / 255.0
    mask = np.expand_dims(mask,2)
    mask = np.repeat(mask,3,2)
    return mask