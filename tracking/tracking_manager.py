from tracking_config import TrackingConfig
from sysUtils.video_utils import VideoIterator
from tqdm import tqdm
from DataReposotiry.detection_data_manager import DetectionDataManager
from tracking.deepsort import deepsort_rbc
import cv2
import numpy as np

class TrackerManager:

    def __init__(self, videoPath, detectionDataManager: DetectionDataManager, device) -> None:
        self.device = device
        self.videoIterator = VideoIterator(videoPath)
        self.detectionDataManager = detectionDataManager
        self.deepsort = deepsort_rbc(TrackingConfig.modelPath)
        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.videoWriter = cv2.VideoWriter('tmp.avi', fourcc, 60.0, (self.videoIterator.getWidth(),self.videoIterator.getHeight()))
        self.mask =  self.getMask()
        #print(self.mask.shape);exit()

    def getMask(self):
        print(f'width = {self.videoIterator.getWidth()}')
        mask = cv2.imread('tracking/mask.jpg', 0)
        mask = cv2.resize(mask, (self.videoIterator.getWidth(), self.videoIterator.getHeight()))
        mask = mask / 255.0
        mask = np.expand_dims(mask,2)
        mask = np.repeat(mask,3,2)
        return mask
    

    def track(self):
        frameIndex = 0
        for _ in tqdm(range(self.videoIterator.getFrameCounts())):

            if not self.videoIterator.hasNext():
                break
            
            frame = self.videoIterator.next()
            origFrame = frame.copy()

            frame = frame * self.mask
            frame = frame.astype(np.uint8)
            #cv2.imwrite('frame_after_mask.jpg', frame)
            detections = self.detectionDataManager.getDetections(frameIndex)

            boxes = detections[:, 2:6]
            scores = detections[:, 6]
            types = detections[:, 7]

            if boxes.shape[0] == 0:
                print('no detections')
                frameIndex += 1
                continue

            tracker, detections_class = self.deepsort.run_deep_sort(frame, scores, boxes, types)
            '''for b in boxes:
                cv2.rectangle(frame, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])),(255,255,255), 2)

            frameIndex += 1
            self.videoWriter.write(frame)
            continue'''

            for track in tracker.tracks:
                if not track.is_confirmed() or track.time_since_update > 1:
                    continue
            
                bbox = track.to_tlbr() #Get the corrected/predicted bounding box
                id_num = str(track.track_id) #Get the ID for the particular track.
                cv2.rectangle(origFrame, (int(bbox[0]), int(bbox[1])), (int(bbox[2]), int(bbox[3])),(255,255,255), 2)
                cv2.putText(origFrame, str(id_num),(int(bbox[0]), int(bbox[1])),0, 5e-3 * 200, (0,255,0),2)
            
            origFrame[:, :, 0] = origFrame[:, :, 0] * self.mask[:, :, 0]

            frameIndex += 1
            self.videoWriter.write(origFrame)