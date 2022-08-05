
import torch
from detection.utils.metrics import box_iou
from models.common import DetectMultiBackend
from utils.general import non_max_suppression
import cv2
import numpy as np
from detection_config import DetectionConfig

class YoloDetector:
    '''
        this is yolo detector interface which is responsible of getting the frame and get the bounding boxes from yolo.
    '''
    def __init__(self, device) -> None:
        self.device = device #select_device()#torch.device('cpu')
        self.model = self.loadModel(DetectionConfig.modelPath)
        self.imgsz = DetectionConfig.imgSize

    def loadModel(self, modelPath):
        model = DetectMultiBackend(modelPath, device=self.device, dnn=False, data='data/coco128.yaml')
        self.half = False
        self.half &= (model.pt or model.jit or model.onnx or model.engine) and self.device.type != 'cpu'  # FP16 supported on limited backends with CUDA
        if model.pt or model.jit:
            model.half() if self.half else model.float()
        return model

    def predict(self, origImg):
        '''
        extract the bounding boxes from the Image.
        
        
        '''        
        img = cv2.resize(origImg, self.imgsz)
        img = np.transpose(img, (2, 0, 1))
        img = torch.from_numpy(img)

        img = img.half() if self.half else img.float()  # uint8 to fp16/32
        img /= 255  # 0 - 255 to 0.0 - 1.0
        if len(img.shape) == 3:
            img = img[None]  # expand for batch dim
        img =img.to(self.device)
        preds = self.model(img, augment=False, visualize=False)
        preds = non_max_suppression(preds, 0.25, 0.45, None, False, max_det=1000)[0] # filter overlapped boxes.
        preds = preds.detach().cpu().numpy()
        preds = self.filter(preds)
        if len(preds) > 0:
            preds[:, :4] = self.scaleCoordinates(img.shape[2:], preds[:, :4], origImg.shape) # scale the boxes coordinates to match the original frame diemsnion.
        return preds


    def scaleCoordinates(self, scaledImgShape, coords, origImgShape):
        '''
        scaledImgShape: the dimensions after resizing the image.
        coords: current boxes coordinates on the resized image.
        origImgShape: the dimensions of the original frame. 
        '''
        widthRatio = origImgShape[0]/scaledImgShape[0]
        heightRatio = origImgShape[1]/scaledImgShape[1]
        coords[:, 1] *= widthRatio
        coords[:, 0] *= heightRatio
        coords[:, 3] *= widthRatio
        coords[:, 2] *= heightRatio
        coords = coords.astype(np.int)
        return coords
    

    def filter(self, boxes):
        #print(type(boxes));exit()
        boxes = [box for box in boxes if box[4] >= 0.2]
        return np.array(boxes)

        