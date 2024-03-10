import os
import subprocess
import datetime
import logging
import warnings
def convertOld(srcpath,dstpath):
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

def convertNew(srcpath,dstpath):
    count = 1
    srcfiles = os.listdir(srcpath)
    dstfiles = os.listdir(dstpath)
    srcfiles = sorted(srcfiles)
    dstfiles = sorted(dstfiles)
    dstTotal = len(dstfiles) + 1
    srcTotal = len(srcfiles)

    for dstfile in dstfiles:
        epsode = str(count).zfill(5)
        dstfile = dstfile.replace(".S01E" + epsode,"")
        dstfiles[count - 1] = dstfile
        count = count + 1

    for srcfile in srcfiles:
        output = srcfile[0:4] + "-" + srcfile[4:6] + "-" + srcfile[6:8] + "_" + srcfile[8:10] + "-" + srcfile[10:12] + "-" + srcfile[12:14]
        filepath = srcpath + "/" + srcfile
        if output + ".mp4" in dstfiles:
            print(srcfile, "already exist removing the source")
            #os.remove(filepath)
        else:
            epsode = "S01E" + str(dstTotal).zfill(5)
            output = dstpath + "/" + output + "." + epsode + ".mp4"
            print("Converting",srcfile,"=>",output)
            #result = subprocess.run(["/usr/bin/HandBrakeCLI", "-Z", "Very Fast 2160p60 4K HEVC", "-i", filepath, "-o", output],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
           # if result.returncode == 0:
            dstTotal = dstTotal + 1
            print("Converted",srcfile,"=>",output)
            #    os.remove(filepath)

def rename(srcpath,dstpath):
    count = 1
    srcfiles = os.listdir(srcpath)
    dstfiles = os.listdir(dstpath)
    srcfiles = sorted(srcfiles)
    dstfiles = sorted(dstfiles)
    dstTotal = len(dstfiles)
    srcTotal = len(srcfiles)

    for srcfile in srcfiles:
        filepath = srcpath + "/" + srcfile
        if os.path.isfile(filepath):
            print(srcfile[0:19])

    print("*******************************")

    for dstfile in dstfiles:
        filepath = dstpath + "/" + dstfile
        if os.path.isfile(filepath):
            print(dstfile)

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    moment = datetime.datetime.now().strftime('%Y-%m-%m-%H%M%S')
    logdir = "./logs/"
    if not os.path.isdir(logdir):
        os.mkdir(logdir)
    logname = logdir + moment + ".log"

    logging.basicConfig(filename=logname,
                        filemode='a',
                        format='%(asctime)s,%(msecs)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)

    #convert('/mnt/dados/DashCam/Origin','/mnt/dados/DashCam/Converted')
    #moveFile('/mnt/dados/DashCam/Converted', '/mnt/dados/DashCam/Converted/Front')
    convertNew('/mnt/dados/DashCam/Origin', '/mnt/dados/DashCam/Converted/Front')
    #rename('/mnt/dados/DashCam/Converted/Front', '/mnt/dados/DashCam/Converted')

