import subprocess
from datetime import datetime
import os

import exiftool
def change_video_datetime(input_file, output_file, new_datetime):
    """
    Change the metadata datetime of a video file using ffmpeg

    :param input_file: Path to input video file
    :param output_file: Path to output video file
    :param new_datetime: datetime object with the new timestamp
    """
    Y = new_datetime[0:4]
    m = new_datetime[4:6]
    d = new_datetime[6:8]
    H = new_datetime[8:10]
    M = new_datetime[10:12]
    S = new_datetime[12:14]

    # Format datetime for ffmpeg (YYYY-MM-DD HH:MM:SS)
    new_date = datetime(int(Y), int(m), int(d), int(H), int(M), int(S))
    formatted_dt = new_date.strftime("%Y-%m-%d %H:%M:%S")
    print(formatted_dt)

    command = [
        'ffmpeg',
        '-i', input_file,
        '-metadata', f'creation_time={formatted_dt}',
        '-codec', 'copy',  # Copy streams without re-encoding
        output_file
    ]
    print(command)

    subprocess.run(command, check=True)


def change_video_metadata(input_file, new_datetime):
    """
    Change video metadata using ExifTool

    :param input_file: Path to video file (modified in-place)
    :param new_datetime: datetime object with new timestamp
    """
    new_datetime = new_datetime.replace("-","")
    new_datetime = new_datetime.replace("_", "")
    Y = new_datetime[0:4]
    m = new_datetime[4:6]
    d = new_datetime[6:8]
    H = new_datetime[8:10]
    M = new_datetime[10:12]
    S = new_datetime[12:14]

    # Format datetime for ffmpeg (YYYY-MM-DD HH:MM:SS)
    new_date = datetime(int(Y), int(m), int(d), int(H), int(M), int(S))
    formatted_dt = new_date.strftime("%Y:%m:%d %H:%M:%S")

    print(f"{input_file} - {formatted_dt}")
    with exiftool.ExifTool() as et:
        et.execute(
            b'-overwrite_original',
            b'-CreateDate=' + formatted_dt.encode(),
            b'-DateTimeOriginal=' + formatted_dt.encode(),
            b'-ModifyDate=' + formatted_dt.encode(),
            input_file.encode()
        )

def change_folder(srcpath):
    srcfiles = os.listdir(srcpath)
    srcfiles = sorted(srcfiles)
    for srcfile in srcfiles:
        change_video_metadata(f"{srcpath}/{srcfile}",srcfile)
