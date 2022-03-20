#!/usr/bin/env python3
# Python script edit by affggh
import os

def checkMagic(file):
    if(os.access(file, os.F_OK)):
        magic = b'AVB0'
        with open(file, "rb") as f:
            buf = f.read(4)
            if(magic==buf):
                print("magic check pass")
                return True
            else:
                print("file is not a vbmeta file")
                return False
    else:
        print("File dose not exist!")

def readVerifyFlag(file):
    if(os.access(file, os.F_OK)):
        with open(file, "rb") as f:
            f.seek(123, 0)
            flag = f.read(1)
            if(flag == b'\x00'):
                print("Verify boot and dm-verity is on")
                return 0  # Verify boot and dm-verity is on
            elif(flag == b'\x01'):
                print("Verify boot but dm-verity is off")
                return 1  # Verify boot but dm-verity is off
            elif(flag == b'\x02'):
                print("All verity is off")
                return 2  # All verity is off
            else:
                print("Unknow")
    else:
        print("File does not exist!")

def restore(file):
    if(os.access(file, os.F_OK)):
        flag = b'\x00'
        with open(file, "rb+") as f:
            f.seek(123,0)
            f.write(flag)
    else:
        print("File does not exist!")

def disableDm(file):
    if(os.access(file, os.F_OK)):
        flag = b'\x01'
        with open(file, "rb+") as f:
            f.seek(123,0)
            f.write(flag)
    else:
        print("File does not exist!")

def disableAVB(file):
    if(os.access(file, os.F_OK)):
        flag = b'\x02'
        with open(file, "rb+") as f:
            f.seek(123,0)
            f.write(flag)
    else:
        print("File does not exist!")

# 测试用
if(__name__=="__main__"):
    file = "vbmeta.img"
    if(checkMagic(file)):
        readVerifyFlag(file)
        disableDm(file)
        readVerifyFlag(file)
        disableAVB(file)
        readVerifyFlag(file)
        restore(file)
        readVerifyFlag(file)
    else:
        pass