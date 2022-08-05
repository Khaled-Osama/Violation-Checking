from DataReposotiry.detection_data_manager import DetectionDataManager
from pipeline_blocks.block import Block
from tracking.tracking_manager import TrackerManager


class TrackingBlock(Block):

    def __init__(self, videoPath, detectionDataRepo, device, logger=None) -> None:
        self.videoPath = videoPath
        self.detectionDataRepo: DetectionDataManager = detectionDataRepo
        self.logger = logger
        self.blockName = 'Tracking'
        self.device = device

    def execut(self):
        trackerManager = TrackerManager(self.videoPath, self.detectionDataRepo, self.device)
        trackerManager.track()


    def onStart(self):
        return super().onStart(self.blockName, self.logger)
    
    def onEnd(self):
        return super().onEnd(self.blockName, self.logger)
        
