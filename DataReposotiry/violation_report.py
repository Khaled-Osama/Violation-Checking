import numpy as np
import math
import pandas as pd


from DataReposotiry.car_types import CarSpeedLimit, IDtoClass

class Violation:
    '''
    this class represents car Violation in a specific frame.
    
    '''

    def __init__(self, frameIndex, carID, carType, speed) -> None:
        '''
        frameIndex: the frame number that this violation happens
        carID: the ID of the car of this violation.
        CarType: the type of the car that cause this violation.
        speed = speed of the car in this frame.
        '''

        self.frameIndex = frameIndex
        self.carID = carID
        self.carType = carType
        self.speed = speed
        
class ViolationReport:
    '''
    this class acts as a violation manager that responsible of adding violation and generate the final report.
    '''
    def __init__(self, framesDelta, generateViolationPath, logger):
        self.violations = []
        self.frameDelta = framesDelta
        self.generateViolationPath = generateViolationPath
        self.logger = logger

    def addViolation(self, trafficViolation: Violation):
        self.violations.append(trafficViolation)

    def saveViolations(self):
        '''
        export all violations of all cars into a csv file.
        
        '''
        data = []
        self.logger.info('start export violations as a csv file')
        for violation in self.violations:
            data.append(list(vars(violation).values()))
        df = pd.DataFrame(data, columns=['frame_index', 'car_id', 'car_type', 'speed'])
        df.to_csv(self.generateViolationPath)
    

    def euclidianDistance(self, pt1, pt2):
        '''
        calculate the euclidian distance of the track on 2 different frames with its center in the two frames.
        '''
        sum1 = math.pow(pt1[0] - pt2[0], 2)
        sum2 = math.pow(pt1[1] - pt2[1], 2)
        return int(math.sqrt( sum1 + sum2))

    def calculateSpeed(self, track):
        '''
        calculate the speed of the track in the time_delta then normalize to pixel per second.
        
        '''
        center1 = ( ( int(track[3]) - int(track[1])) // 2 + int(track[1]), (int(track[4]) - int(track[2])) // 2 + int(track[2]))
        center2 = ( ( int(track[9]) - int(track[7]) ) // 2 + int(track[7]), ( int(track[10]) - int(track[8]) ) // 2 + int(track[8]) )

        distance = self.euclidianDistance(center1, center2)

        return distance * (60 / self.frameDelta) # to get the speed in pixels per second.

    def checkViolations(self, frameIndex, currentTracks, prevTracks) -> set:
        '''
        check if a track in the current frame exceeds the speed limit if so add this violation in the violation report.
        '''
        s = set()

        # there's no tracks in this frame.
        if len(prevTracks) == 0:
            return s
        concatenatedTracks = []
        #for each track in the current frame get the same track from previous frame.
        for row1 in currentTracks:
            for row2 in prevTracks:
                if row1[0] == row2[0]: # check by trackID
                    concatenatedTracks.append(row1 + row2)
                    break
        
        for car in concatenatedTracks:
            speed = self.calculateSpeed(car) # get the speed.
            carType = IDtoClass[str(car[5])] # get vehicle type.
            if speed > CarSpeedLimit.speedLimits[carType]:
                self.addViolation(Violation(frameIndex, car[0], carType, speed))
                s.add(car[0])
        return s



    