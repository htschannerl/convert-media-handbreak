import os
import subprocess
import datetime
import logging
def convert(srcpath,dstpath):
    files = os.listdir(srcpath)
    total = len(os.listdir(dstpath))
    for file in files:
        filepath = srcpath + "/" + file
        if os.path.isfile(filepath):
            print("Starting", filepath)
            t = datetime.datetime(int(file[0:4]), int(file[4:6]), int(file[6:8]), int(file[8:10]), int(file[10:12]), int(file[12:14]))
            t = t.strftime('%a %d %B %Y, %H:%M:%S')
            output = dstpath + "/S01E" + str(total).zfill(8) + "." + str(t) + ".mp4"
            if not os.path.exists(output):
                print(output)
                result = subprocess.run(["/usr/bin/HandBrakeCLI", "-Z", "Very Fast 2160p60 4K HEVC","-i",filepath,"-o",output])
                if result.returncode == 0:
                    print("Finished",file,output)
                    #os.remove(filepath)
                    total = total + 1
            else:
                print(file,"already exist removing the source")
                #os.remove(filepath)


if __name__ == '__main__':
    convert('/mnt/dados/DashCam/Origin','/mnt/dados/DashCam/Converted')

