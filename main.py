import os
import subprocess
import datetime
import logging
import warnings
import pandas as pd
import getVideoLen
import change_video_datetime
from include import job_parser
import yaml
from include.save_report import save_report

class main:
    def __init__(self):
        args = job_parser.parse_arguments()

        # Load YAML file
        with open(f"{os.path.dirname(__file__)}/config.yaml", "r") as f:
            config = yaml.safe_load(f)

        warnings.filterwarnings('ignore')
        moment = datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')
        logdir = os.path.dirname(__file__) + "/logs/"
        if not os.path.isdir(logdir):
            os.mkdir(logdir)
        logname = f"{logdir}{moment}-{args.action}.log"

        logging.basicConfig(filename=logname,
                            filemode='a',
                            format='%(asctime)s,%(msecs)s %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.DEBUG)

        if args.action == "convert":
            for convert in config["convert"]:
                src = config["convert"][convert]["srcpath"]
                dst = config["convert"][convert]["dstpath"]
                preset = config["convert"][convert]["preset"]
                cam = config["convert"][convert]["cam"]
                report = config["report"]
                self.convert(src,dst,preset,cam,report)

        if args.action == "backup":
            report = config["report"]
            self.backup(config["backup"],report)

    def backup(self,config,report):
        my_env = os.environ.copy()
        df = pd.read_excel(report)

        for cam in config:
            limit = config[cam]["limit"]
            compress = config[cam]["compress"]
            dst = config[cam]["dstpath"]
            for index, row in df.iterrows():
                if row["Cam"] == cam and int(row["seconds"]) <= limit:
                    filename = row["dstfile"]
                    src = f"{row['Path']}/{filename}"
                    backup = row["backup"]
                    if os.path.isfile(src):
                        print(f"Compressing the file {src}")
                        logging.info(f"Compressing the file {src}")
                        if compress:
                            result = subprocess.run(["/usr/bin/7z", "a",f"{dst}/{cam}.7z",src,"-t7z","-m0=LZMA2","-mx=9","-md=1024m","-mfb=64","-ms=on","-mmt=on"],
                                                    stdout=subprocess.DEVNULL, stderr=subprocess.PIPE, env=my_env)
                            if result.returncode == 0:
                                df.loc[index,"backup"] = "yes"
                                os.remove(src)
                    else:
                        df.loc[index, "backup"] = "yes"
                        logging.info(f"The file {src} is not in the folder and the status is {backup}")
                        print(f"The file {src} is not in the folder and the status is {backup}")

        df = df.set_index('srcfile')
        df = df.sort_index()
        df.to_excel(report, index=True)


    def moveFile(self,srcpath,dstpath):
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

    def convert(self,srcpath,dstpath,preset,cam,report):
        my_env = os.environ.copy()
        count = 1
        srcfiles = os.listdir(srcpath)
        dstfiles = os.listdir(dstpath)
        srcfiles = sorted(srcfiles)
        dstfiles = sorted(dstfiles)
        srcTotal = len(srcfiles)
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
                        data = [output, round(srcstat.st_size / (1024 * 1024),2), round(dststat.st_size / (1024 * 1024),2),round(dststat.st_size / (1024 * 1024),2) - round(srcstat.st_size / (1024 * 1024),2), cam, dstpath + "/", lenVideo[0], lenVideo[1],"no"]
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
                            data = [dstfile, round(srcstat.st_size / (1024 * 1024),2), round(dststat.st_size / (1024 * 1024),2),round(dststat.st_size / (1024 * 1024),2) - round(srcstat.st_size / (1024 * 1024),2), cam, dstpath + "/", lenVideo[0], lenVideo[1],"no"]
                            df.loc[srcfile] = data
                            change_video_datetime.change_video_metadata(output,srcfile)
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
        df = df.sort_index()
        df.to_excel(report,index=True)
        saveReport = save_report()
        saveReport.insertReport(df.reset_index())

    def archive(self,srcpath,dstpath,preset):
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

    def removeEpisode(self,srcpath,dtspath):
        srcfiles = os.listdir(srcpath)
        srcfiles = sorted(srcfiles)

        for srcfile in srcfiles:
            if os.path.isfile(srcpath + "/" + srcfile):
                dstfile = srcfile[0:19] + ".mp4"
                result = subprocess.run(["mv", srcpath + "/" + srcfile,dtspath + "/" + dstfile])
                if result.returncode == 0:
                    print("Moved from:",srcpath + "/" + srcfile,"To:",dtspath + "/" + dstfile)




    def rename(self,srcpath,dstpath):
        count = 1
        srcfiles = os.listdir(srcpath)
        dstfiles = os.listdir(dstpath)
        srcfiles = sorted(srcfiles)
        dstfiles = sorted(dstfiles)

        for srcfile in srcfiles:
            filepath = srcpath + "/" + srcfile
            if os.path.isfile(filepath):
                print(srcfile[0:19])

        print("*******************************")

        for dstfile in dstfiles:
            filepath = dstpath + "/" + dstfile
            if os.path.isfile(filepath):
                print(dstfile)

    def test(self):
        my_env = os.environ.copy()
        print(my_env)

run = main()