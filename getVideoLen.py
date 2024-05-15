# import module
import cv2
import datetime

# create video capture object
data = cv2.VideoCapture('/mnt/dados/DashCam/Converted/Front/2024-05-14_07-57-48.mp4')

# count the number of frames
frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
fps = data.get(cv2.CAP_PROP_FPS)

# calculate duration of the video
seconds = round(frames / fps)
video_time = datetime.timedelta(seconds=seconds)
print(f"duration in seconds: {seconds}")
print(f"video time: {video_time}")