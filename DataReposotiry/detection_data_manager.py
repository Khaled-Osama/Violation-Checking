import pandas as pd

class Detection:
    def __init__(self, frameID, x1, y1, x2, y2, conf, carType) -> None:
        self.frameID = frameID
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.conf = conf
        self.carType = carType

    def __str__(self) -> str:
        return f'frameID = {self.frameID}, x1 = {self.x1}, y1 = {self.y1}, x2 = {self.x2}, y2 = {self.y2}, conf = {self.conf}, carType = {self.carType}'

class DetectionDataManager:


    def __init__(self) -> None:
        self.df = None#pd.DataFrame(columns=['frame_index', 'x1', 'y1', 'x2', 'y2', 'score', 'carType'])
        self.data = []

    def addDetection(self, detection:Detection):
        
        self.data.append([detection.frameID, detection.x1, detection.y1, detection.x2, detection.y2, detection.conf, detection.carType])
        #self.df.loc[-1] = [detection.frameID, detection.x1, detection.y1, detection.x2, detection.y2, detection.conf, detection.carType]
        #self.df.index += 1 

    def save(self):
        self.df = pd.DataFrame(self.data, columns=['frame_index', 'x1', 'y1', 'x2', 'y2', 'score', 'carType'])
        self.df.to_csv('detection.csv')
    def getData(self):
        return self.df
    

    def loadDF(self, csv_path='detection.csv'):
        self.df = pd.read_csv(csv_path)
    

    def getDetections(self, frameIndx):

        det = self.df[self.df['frame_index'] == frameIndx].values
        det[:, 4] = det[:, 4] - det[:, 2]
        det[:, 5] = det[:, 5] - det[:, 3]
        return det

        