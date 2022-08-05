import cv2


cap = cv2.VideoCapture('2.mp4')

frames_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

print(frames_count)