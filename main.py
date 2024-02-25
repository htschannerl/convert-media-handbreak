import os
import subprocess
import logging
def convert(srcpath,dstpath):
    files = os.listdir(srcpath)
    for file in files:
        print("Starting",file)
        os.path.isfile(srcpath + "/" + file)
        output = file[0:4] + "-" + file[4:6] + "-" + file[6:8] + "_" + file[8:10] + "-" + file[10:12] + "-" + file[12:14] + "-" + file[14:16] + file[16:18] + ".mp4"
        print(output)
        if not os.path.isfile(output):
            result = subprocess.run(["HandBrakeCLI -Z \"Very Fast 2160p60 4K AV1\" -i " + srcpath + "/" + file + " -o " + output])
            print(result.args)
        print("Finished",file,output)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    convert('/mnt/dados/DashCam','/mnt/dados/DashCam/Converted')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
