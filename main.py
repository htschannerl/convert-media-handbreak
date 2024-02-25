import os
import subprocess
import logging
def convert(srcpath,dstpath):
    files = os.listdir(srcpath)
    for file in files:
        filepath = srcpath + "/" + file
        if os.path.isfile(filepath):
            print("Starting", filepath)
            output = dstpath + "/" + file[0:4] + "-" + file[4:6] + "-" + file[6:8] + "_" + file[8:10] + "-" + file[10:12] + "-" + file[12:14] + "-" + file[14:16] + file[16:18] + ".mp4"
            if not os.path.exists(output):
                print(output)
                result = subprocess.run(["HandBrakeCLI", "-Z", "Very Fast 2160p60 4K AV1","-i",filepath,"-o",output])
                if result.returncode == 0:
                    print("Finished",file,output)
                    os.remove(file)
            else:
                print(file,"already exist removing the source")
                os.remove(filepath)


if __name__ == '__main__':
    convert('/mnt/dados/DashCam','/mnt/dados/DashCam/Converted')

