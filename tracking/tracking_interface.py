
from tracking.deepsort import deepsort_rbc
from tracking_config import TrackingConfig
import cv2
import numpy as np
import time

class TrackingClient:


    def __init__(self, width, height, device) -> None:
        self.width = width
        self.height = height
        self.deepsort = deepsort_rbc(TrackingConfig.modelPath, device)
        self.lastID = 0
        self.IDMapping = {} # to map the tracker IDs to our IDs.
    
    def track(self, frame, detections):
        tracks = []
        if len(detections) == 0:
            return tracks
        boxes = detections[:, :4]
        scores = detections[:, 4]
        types = detections[:, 5]

         
        if boxes.shape[0] == 0:
            return tracks
        tracker, _ = self.deepsort.run_deep_sort(frame, scores, boxes, types)

        for track in tracker.tracks:
            if not track.is_confirmed() or track.time_since_update > 1: # still this track is not confirmed.
                continue
            
            bbox = track.to_tlbr() #Get the corrected/predicted bounding box
            id_num = str(track.track_id) #Get the ID for the particular track.

            if id_num not in self.IDMapping:
                self.IDMapping[id_num] = self.lastID
                self.lastID += 1

            id_num = self.IDMapping[id_num]

            tracks.append([id_num, *bbox, track.type])

        return self.filterTracks(tracks)

    def getCarsCount(self):
        '''
        returns the count of cars.
        '''
        return self.lastID


    def filterTracks(self, tracks):
        '''
        filter tracks that their coordinates are out of frame dimenstions.
        '''
        tracks = [track for track in tracks if track[1]>0 and track[3] < self.width and track[2]>0 and track[4] < self.height]
        return tracks