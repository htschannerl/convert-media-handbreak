import os
import subprocess
import datetime
import logging
import warnings
import pandas as pd
import getVideoLen
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

def convertNew(srcpath,dstpath,preset,cam):
    my_env = os.environ.copy()
    count = 1
    srcfiles = os.listdir(srcpath)
    dstfiles = os.listdir(dstpath)
    srcfiles = sorted(srcfiles)
    dstfiles = sorted(dstfiles)
    srcTotal = len(srcfiles)
    report = "/mnt/dados/DashCam/report.xlsx"
    df = pd.read_excel(report)
    df = df.set_index('srcfile')

    for srcfile in srcfiles:
        logging.info("Starting the number: " + str(count) + " of " + str(srcTotal))
        if os.path.isfile(srcpath + "/" + srcfile):
            if len(srcfile) >= 21:
                output = srcfile[0:4] + "-" + srcfile[4:6] + "-" + srcfile[6:8] + "_" + srcfile[8:10] + "-" + srcfile[10:12] + "-" + srcfile[12:14] + ".mp4"
                filepath = srcpath + "/" + srcfile
                srcstat = os.stat(filepath)
                if output in dstfiles:
                    dststat = os.stat(dstpath + "/" + output)
                    lenVideo = getVideoLen.getVideoLen(dstpath + "/" + output)
                    data = [output, round(srcstat.st_size / (1024 * 1024),2), round(dststat.st_size / (1024 * 1024),2),round(dststat.st_size / (1024 * 1024),2) - round(srcstat.st_size / (1024 * 1024),2), cam, dstpath + "/", lenVideo[0], lenVideo[1]]
                    df.loc[srcfile] = data
                    print(srcfile, "already exist removing the source",str(round(srcstat.st_size / (1024 * 1024),2)),"-",str(round(dststat.st_size / (1024 * 1024),2)))
                    logging.info(srcfile + " already exist removing the source. Removing it from the source")
                    #os.remove(filepath)
                else:
                    dstfile = output
                    output = dstpath + "/" + output
                    print("Converting",srcfile,"=>",output)
                    logging.info("Converting " + srcfile + " => " + output)
                    result = subprocess.run(["/usr/bin/HandBrakeCLI", "-Z", preset, "-i", filepath, "-o", output],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,env=my_env)
                    if result.returncode == 0:
                        dststat = os.stat(output)
                        lenVideo = getVideoLen.getVideoLen(output)
                        data = [dstfile, round(srcstat.st_size / (1024 * 1024),2), round(dststat.st_size / (1024 * 1024),2),round(dststat.st_size / (1024 * 1024),2) - round(srcstat.st_size / (1024 * 1024),2), cam, dstpath + "/", lenVideo[0], lenVideo[1]]
                        df.loc[srcfile] = data
                        logging.info("Converted " + srcfile + " => " + output)
                        print("Converted",srcfile,"=>",output,"-",str(round(srcstat.st_size / (1024 * 1024),2)),"-",str(round(dststat.st_size / (1024 * 1024),2)),lenVideo[0],lenVideo[1])
                        #os.remove(filepath)
                    else:
                        logging.error("Error " + srcfile + " => " + output)
                        logging.error(result.stderr)
            else:
                logging.info("Skipped " + srcfile)
                print("Skipped", srcfile)
                #os.remove(srcpath + "/" + srcfile)
        else:
            logging.info("Skipped " + srcfile)
            print("Skipped", srcfile)

        count = count + 1

    df.to_excel(report,index=True)


def archive(srcpath,dstpath,preset):
    my_env = os.environ.copy()
    count = 1
    srcfiles = os.listdir(srcpath)
    dstfiles = os.listdir(dstpath)
    srcfiles = sorted(srcfiles)
    dstfiles = sorted(dstfiles)
    dstTotal = len(dstfiles)
    srcTotal = len(srcfiles)

    for srcfile in srcfiles:
        logging.info("Starting the number: " + str(count) + " of " + str(srcTotal))
        filepath = srcpath + "/" + srcfile
        if os.path.isfile(filepath):
            output = srcfile
            if output in dstfiles:
                print(srcfile, "already exist removing the source")
                logging.info(srcfile + " already exist removing the source. Removing it from the source")
                #os.remove(filepath)
            else:
                output = dstpath + "/" + output
                print("Converting",srcfile,"=>",output)
                logging.info("Converting " + srcfile + " => " + output)
                result = subprocess.run(["/usr/bin/HandBrakeCLI", "-Z", preset, "-i", filepath, "-o", output],stdout=subprocess.DEVNULL,stderr=subprocess.PIPE,env=my_env)
                if result.returncode == 0:
                    logging.info("Converted " + srcfile + " => " + output)
                    print("Converted",srcfile,"=>",output)
                    #os.remove(filepath)
                else:
                    logging.error("Error " + srcfile + " => " + output)
                    logging.error(result.stderr)
        else:
            logging.info("Skipped is a dir " + srcfile)
            print("Skipped is a dir", srcfile)

        count = count + 1

def removeEpisode(srcpath,dtspath):
    srcfiles = os.listdir(srcpath)
    srcfiles = sorted(srcfiles)

    for srcfile in srcfiles:
        if os.path.isfile(srcpath + "/" + srcfile):
            dstfile = srcfile[0:19] + ".mp4"
            result = subprocess.run(["mv", srcpath + "/" + srcfile,dtspath + "/" + dstfile])
            if result.returncode == 0:
                print("Moved from:",srcpath + "/" + srcfile,"To:",dtspath + "/" + dstfile)




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

def test():
    my_env = os.environ.copy()
    print(my_env)

if __name__ == '__main__':
    warnings.filterwarnings('ignore')
    moment = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
    logdir = os.path.dirname(__file__) + "/logs/"
    if not os.path.isdir(logdir):
        os.mkdir(logdir)
    logname = logdir + moment + ".log"

    logging.basicConfig(filename=logname,
                        filemode='a',
                        format='%(asctime)s,%(msecs)s %(levelname)s %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S',
                        level=logging.DEBUG)


    convertNew('/mnt/dados/DashCam/Origin/VIDEO_F', '/mnt/dados/DashCam/Converted/Front', "H.265 QSV 2160p 4K", "Front")
    convertNew('/mnt/dados/DashCam/Origin/VIDEO_F_LOCK', '/mnt/dados/DashCam/Converted/Front', "H.265 QSV 2160p 4K", "Front")
    convertNew('/mnt/dados/DashCam/Origin/VIDEO_B', '/mnt/dados/DashCam/Converted/Back', "H.265 QSV 1080p", "Back")
    convertNew('/mnt/dados/DashCam/Origin/VIDEO_B_LOCK', '/mnt/dados/DashCam/Converted/Back', "H.265 QSV 1080p", "Back")
    #archive('/mnt/dados/DashCam/Converted/Front', '/mnt/dados/DashCam/archive/Front', "H.265 QSV 2160p 4K")
    #test()


