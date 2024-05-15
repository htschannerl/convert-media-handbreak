import cv2

# create video capture object
cap = cv2.VideoCapture('/mnt/dados/DashCam/Converted/Front/2024-05-14_07-57-48.mp4')

# count the number of frames
fps = cap.get(cv2.CAP_PROP_FPS)
totalNoFrames = cap.get(cv2.CAP_PROP_FRAME_COUNT)
durationInSeconds = totalNoFrames // fps

print("Video Duration In Seconds:", durationInSeconds, "s")