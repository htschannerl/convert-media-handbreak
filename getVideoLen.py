# import module
import cv2
import datetime
import pandas as pd
import os

def getVideoLen(file):
    # create video capture object
    data = cv2.VideoCapture(file)

    # count the number of frames
    frames = data.get(cv2.CAP_PROP_FRAME_COUNT)
    fps = data.get(cv2.CAP_PROP_FPS)

    # calculate duration of the video
    seconds = round(frames / fps)
    video_time = datetime.timedelta(seconds=seconds)
    result = [seconds, str(video_time)]
    return result

def updateLenFile(file):
    df = pd.read_excel(file)
    df = df.set_index('srcfile')

    for index, row in df.iterrows():
        path = df.loc[index, 'Path']
        dstfile = df.loc[index, 'dstfile']
        if os.path.isfile(path + "/" + dstfile):
            result = getVideoLen(path + "/" + dstfile)
            df[index, 'seconds'] = result[0]
            df[index, 'Len'] = result[1]

    df.to_excel(file, index=True)

updateLenFile("/mnt/dados/DashCam/report.xlsx")