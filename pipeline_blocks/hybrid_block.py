
import time
from tqdm import tqdm
from DataReposotiry.car_types import CarLegalVisColor, IDtoClass
from DataReposotiry.violation_report import ViolationReport
from sysUtils.image_utils import getMask, xyxy2xywh
from sysUtils.video_utils import VideoIterator
from pipeline_blocks.block import Block
from detection.yolo_detector import YoloDetector
import cv2
from tracking.tracking_interface import TrackingClient
from DataReposotiry.tracking_data_repo import TrackingDataRepo
import logging
import numpy as np

class HybridBlock(Block):


    def __init__(self, videoPath, device, generateViolationPath, makeDemo, logger: logging.Logger) -> None:
        '''
        videoPath: the path of the video.
        device: torch.device that the system will run onto
        logger: Logging.Logger to write the logs
        '''

        self.blockName = 'Detection With Tracking'
        self.frameDelta = 3
        self.videoIterator = VideoIterator(videoPath)
        self.detectorClient = YoloDetector(device)
        self.trackingClient = TrackingClient(self.videoIterator.getWidth(), self.videoIterator.getHeight(), device)
        self.trackingDataRepo = TrackingDataRepo(self.frameDelta)
        self.violationReport = ViolationReport(self.frameDelta, generateViolationPath, logger)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.videoWriter = cv2.VideoWriter('Demo.avi', fourcc, 25.0, (self.videoIterator.getWidth(),self.videoIterator.getHeight()))
        self.mask = getMask(self.videoIterator.getWidth(),self.videoIterator.getHeight())
        self. applyMask = True
        self.logger = logger
        self.makeDemo = makeDemo
    def execut(self):
        '''
            Start executing the pipeline
        '''
        self.onStart()
        frame_index = 0
        for _ in tqdm(range(self.videoIterator.getFrameCounts()), desc='Detection with tracking ...'):
            
            if not self.videoIterator.hasNext():
                self.logger.info('The video processing is finished')
                break

            frame = self.videoIterator.next()
            if frame is None:
                self.logger.warning("video capture cant read the frame")
                continue


            visualizedFrame = frame.copy()
            if self.applyMask:
                frame = frame * self.mask
                frame = frame.astype(np.uint8)

            # get detection bounding boxes for a frame.
            detectionPreds = self.detectorClient.predict(frame)

            if len(detectionPreds) != 0:
                detectionPreds = xyxy2xywh(detectionPreds)
                
            tracks = self.trackingClient.track(frame, detectionPreds)
            #print('\r' f'time = {time.time()-t1}', end='')
            self.trackingDataRepo.addTracks(frame_index, tracks)
            
            illegalIDs = set()
            if frame_index >= self.frameDelta:
                prev_tracks = self.trackingDataRepo.getTracks(frame_index - self.frameDelta + 1)
                illegalIDs = self.violationReport.checkViolations(frame_index, tracks, prev_tracks)
            # make output video ith boudning boxes.
            if self.makeDemo:
                frame = self.drawBoxes(visualizedFrame, tracks, frame_index, illegalIDs)
                self.videoWriter.write(frame)

                

            frame_index += 1
        self.violationReport.saveViolations()
        self.onEnd()
    def drawBoxes(self, frame, tracks, frameIndex, illegalIds):
        '''
        frame: np.ndarray represents the image
        tracks: 2d list represents the tracks of the current frame.
        '''
        for id_num, *bbox, type in tracks:
            color = CarLegalVisColor.colors[IDtoClass[str(type)]] # get class color

            
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])), color, thickness=2, lineType=cv2.LINE_AA)
            w, h = cv2.getTextSize(str(id_num), 0, fontScale=1, thickness=2)[0]
            cv2.rectangle(frame, (int(bbox[0]), int(bbox[1])), (int(bbox[0] + w), int(bbox[1] - h - 3)), color, -1, cv2.LINE_AA)
            cv2.putText(frame, str(id_num),(int(bbox[0]), int(bbox[1])),0, 1, (255, 255, 255), 1, lineType=cv2.LINE_AA)
            cv2.putText(frame, 'frame_number: '+str(frameIndex),(40, 40),0, 1, (0,255,0),2, lineType=cv2.LINE_AA)
            cv2.putText(frame, 'vehicle Count: '+str(self.trackingClient.getCarsCount()),(40, 80),0, 1, (0,255,0),2, cv2.LINE_AA)
            if id_num in illegalIds:
                frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2]), 2] = 255
        
        return frame
    

    def onStart(self):
        return super().onStart(self.blockName, self.logger)
    
    def onEnd(self):
        return super().onEnd(self.blockName, self.logger)
