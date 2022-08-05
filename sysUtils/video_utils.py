from abc import ABC, abstractmethod
import cv2

def readVideo(video_path):
    cap = cv2.VideoCapture(video_path)
    framesCount = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    return cap, framesCount



class Iterator(ABC):

    @abstractmethod
    def hasNext(self):
        pass
    @abstractmethod
    def next(self):
        pass

class VideoIterator(Iterator):
    def __init__(self, video_path):
        self.videoCapture = cv2.VideoCapture(video_path)
        self.frames_count = int(self.videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
        self.frame_index = 0

    def hasNext(self):
        return self.frame_index < self.frames_count

    def getFrameCounts(self):
        return self.frames_count
    def getWidth(self):
        return int(self.videoCapture.get(3))
    def getHeight(self):
        return int(self.videoCapture.get(4))

    def next(self):
        ret, frame = self.videoCapture.read()
        if ret == False:
            return None
        self.frame_index += 1
        return frame