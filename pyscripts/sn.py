import os, sys
import time
import wmi,zlib
import utils

def get_cpu_info() :
          tmpdict = {}
          tmpdict["CpuCores"] = 0
          c = wmi.WMI()
#          print c.Win32_Processor().['ProcessorId']
#          print c.Win32_DiskDrive()
          for cpu in c.Win32_Processor():     
    #                print cpu
                    print ("cpu id:", cpu.ProcessorId.strip())
                    tmpdict["CpuType"] = cpu.Name
                    try:
                              tmpdict["CpuCores"] = cpu.NumberOfCores
                    except:
                              tmpdict["CpuCores"] += 1
                              tmpdict["CpuClock"] = cpu.MaxClockSpeed 
                              return tmpdict
 
def _read_cpu_usage():
          c = wmi.WMI ()
          for cpu in c.Win32_Processor():
                    return cpu.LoadPercentage
 
def get_cpu_usage():
          cpustr1 =_read_cpu_usage()
          if not cpustr1:
                    return 0
          time.sleep(2)
          cpustr2 = _read_cpu_usage()
          if not cpustr2:
                    return 0
          cpuper = int(cpustr1)+int(cpustr2)/2
          return cpuper
def get_disk_info():
          tmplist = []
          encrypt_str = ""
          c = wmi.WMI ()
          for cpu in c.Win32_Processor():

#cpu 序列号
                    encrypt_str = encrypt_str+cpu.ProcessorId.strip()
                    print ("cpu id:", cpu.ProcessorId.strip())
          for physical_disk in c.Win32_DiskDrive():
                    encrypt_str = encrypt_str+physical_disk.SerialNumber.strip()

#硬盘序列号
                    print ('disk id:', physical_disk.SerialNumber.strip())
                    tmpdict = {}
                    tmpdict["Caption"] = physical_disk.Caption
                    tmpdict["Size"] = int(physical_disk.Size)/1000/1000/1000
                    tmplist.append(tmpdict)
          for board_id in c.Win32_BaseBoard():

#主板序列号
                    encrypt_str = encrypt_str+board_id.SerialNumber.strip()
                    print ("main board id:",board_id.SerialNumber.strip())
#          for mac in c.Win32_NetworkAdapter():

#mac 地址（包括虚拟机的）
#                    print "mac addr:", mac.MACAddress:
          for bios_id in c.Win32_BIOS():

#bios 序列号
                    encrypt_str = encrypt_str+bios_id.SerialNumber.strip()
                    print ("bios number:", bios_id.SerialNumber.strip())
          print ("encrypt_str:", encrypt_str)

#加密算法
          print (zlib.adler32(encrypt_str.encode()))
          return encrypt_str 

def get_board_id():
    c = wmi.WMI ()
    for board_id in c.Win32_BaseBoard():
#主板序列号
        boardid = board_id.SerialNumber.strip()
        return boardid.strip()


if __name__ == "__main__":
#     a = get_cpu_info()
     get_disk_info()
     utils.runcmd("PowerShell \"Get-WmiObject -class Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber\"")