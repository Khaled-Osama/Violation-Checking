


from DataReposotiry.detection_data_manager import Detection, DetectionDataManager
from detection.yolo_detector import YoloDetector
from pipeline_blocks.block import Block
from sysUtils.video_utils import VideoIterator
from detection.detection_config import DetectionConfig
from tqdm import tqdm
import numpy as np
import os

class DetectionBlock(Block):

    def __init__(self, videoPath, device, logger=None) -> None:
        '''
        for running the detectio block only and save the result in a csv.
        '''
        self.videoPath = videoPath
        self.logger = logger
        self.blockName = 'Detection'
        self.device = device
        
    def execut(self):
        
        self.onStart()
        videoIterator = VideoIterator(self.videoPath)
        yoloDetector = YoloDetector(self.device)
        detectionDataManager = DetectionDataManager()
        if os.path.isfile('detection.csv'):
            detectionDataManager.loadDF()
            return detectionDataManager
            
        for i in tqdm(range(videoIterator.getFrameCounts()), desc='Detection ...'):
            if not videoIterator.hasNext():
                break
            frame = videoIterator.next()
            boxes = yoloDetector.predict(frame)
            boxes[:, :4] = boxes[:, :4].astype(np.int)
            for box in boxes:
                detection = Detection(i, *box)
                detectionDataManager.addDetection(detection)
        detectionDataManager.save()
        self.onEnd()
        return detectionDataManager

    def onStart(self):
        return super().onStart(self.blockName, self.logger)

    def onEnd(self):
        return super().onEnd(self.blockName, self.logger)
    
    
