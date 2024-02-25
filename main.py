import os
import subprocess
import logging
def convert(srcpath,dstpath):
    files = os.listdir(srcpath)
    for file in files:
        os.path.isfile(srcpath + "/" + file)
        output = file[0:4] + "-" + file[4:6] + "-" + file[6:8] + "_" + file[8:10] + "-" + file[10:12] + "-" + file[12:14] + "-" + file[14:16] + file[16:18] + ".mp4"
        subprocess.run(["HandBrakeCLI", "-Z \"Fast 2160p60 4K AV1\"","-i" + srcpath + "/" + file,"-o" + dstpath + "/" + output])
        print(file,output,subprocess.CompletedProcess())


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    convert('/run/media/henrique/5857-40EA/VIDEO_F','/home/henrique/Videos')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
