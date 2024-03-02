import os
import subprocess
import datetime
import logging
def convert(srcpath,dstpath):
    files = os.listdir(srcpath)
    total = len(os.listdir(dstpath))
    if total == 0:
        total = 1
    for file in files:
        filepath = srcpath + "/" + file
        if os.path.isfile(filepath):
            print("Starting", filepath)
            #t = datetime.datetime(int(file[0:4]), int(file[4:6]), int(file[6:8]), int(file[8:10]), int(file[10:12]), int(file[12:14]))
            #t = t.strftime('%a %d %B %Y, %H:%M:%S')
            output = dstpath + "/" + file[0:4] + "-" + file[4:6] + "-" + file[6:8] + "_" + file[8:10] + "-" + file[10:12] + "-" + file[12:14] + ".mp4"
            if not os.path.exists(output):
                print(output)
                result = subprocess.run(["/usr/bin/HandBrakeCLI", "-Z", "Very Fast 2160p60 4K HEVC","-i",filepath,"-o",output])
                if result.returncode == 0:
                    print("Finished",file,output)
                    os.remove(filepath)
                    total = total + 1
            else:
                print(file,"already exist removing the source")
                os.remove(filepath)

def moveFile(srcpath,dstpath):
    count = 1
    files = os.listdir(srcpath)
    files = sorted(files)
    for file in files:
        filepath = srcpath + "/" + file
        if os.path.isfile(filepath):
            epsode = str(count).zfill(5)
            result = subprocess.run(["mv", filepath, dstpath + "/" + file + ".S01" + epsode + "."])
            if result.returncode == 0:
                count = count + 1
            print(file)

def renameFile(srcpath,dstpath):
    count = 1
    srcfiles = os.listdir(srcpath)
    dstfiles = os.listdir(dstpath)
    srcfiles = sorted(srcfiles)
    dstfiles = sorted(dstfiles)
    dstTotal = len(dstfiles)
    srcTotal = len(srcfiles)
    print(srcTotal,"of",dstTotal)

if __name__ == '__main__':
    #convert('/mnt/dados/DashCam/Origin','/mnt/dados/DashCam/Converted')
    #moveFile('/mnt/dados/DashCam/Converted', '/mnt/dados/DashCam/Converted/Front')
    renameFile('/mnt/dados/DashCam/Origin', '/mnt/dados/DashCam/Converted/Front')

