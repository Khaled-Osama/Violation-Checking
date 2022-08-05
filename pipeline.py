

import logging
from pipeline_blocks.detection_block import DetectionBlock
from pipeline_blocks.hybrid_block import HybridBlock
from pipeline_blocks.tracking_block import TrackingBlock

class Pipeline:
    '''
    there are 2 options execute blocks sequentially or execute 
    the blocks alongside with each others.
    
    '''
    def __init__(self, video_path, device, makeDemo, logger) -> None:
        self.video_path = video_path
        self.device = device
        self.logger = logger
        self.makeDemo = makeDemo
        self.generateViolationPath = 'violations.csv'

    def executSequential(self):
        '''
        execute every block (detection and tracking) sequentially.
        '''
        detectionBlock = DetectionBlock(self.video_path, self.device, self.logger)
        detectionDataRepo = detectionBlock.execut()
        trackingBlock = TrackingBlock(self.video_path, detectionDataRepo, self.device, self.logger)
        trackingBlock.execut()

    def executHybrid(self):
        '''
            execute the detection alongside with tracking.
        '''
        hybirdBlock = HybridBlock(self.video_path, self.device, self.generateViolationPath, self.makeDemo, self.logger)
        hybirdBlock.execut()



