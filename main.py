import logging
import sys

sys.path.insert(0, 'detection')
sys.path.insert(0, 'tracking')

from pipeline import Pipeline
import torch
import logging
import cv2

if __name__ == '__main__':
    logging.basicConfig(filename="logs.log",
                    format='%(asctime)s %(message)s',
                    filemode='w', force=True,
                    level=logging.DEBUG) # defing the logging file.
    logger = logging.getLogger('systemLogging')
    device = torch.device('cpu') # select the device we want to run onto.
    videoPath = 'road_traffic.webm' # the video path that we want to run.
    makeDemo = True # create Demo flag.
    pipeline = Pipeline(videoPath, device, makeDemo, logger) # define a pipleine.
    pipeline.executHybrid() #start the pipeline.
