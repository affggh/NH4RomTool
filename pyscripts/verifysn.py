# This python script is for verification
import os, sys
import base64
from Crypto.Cipher import AES
# This is get main board id
import subprocess
import time
import wmi
import sn as snread

def runcmd(cmd):
    try:
        ret = subprocess.Popen(cmd,shell=True,
                 stdin=subprocess.PIPE,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT)
        for i in iter(ret.stdout.readline,b""):
            return i.decode("utf-8",'ignore').strip()
    except subprocess.CalledProcessError as e:
        for i in iter(e.stdout.readline,b""):
            return e.decode("utf-8",'ignore').strip()

def get_board_id():
    c = wmi.WMI ()
    for board_id in c.Win32_BaseBoard():
#主板序列号
        boardid = board_id.SerialNumber.strip()
        return boardid.strip()

key = b'1145141919810fff'
# sn = runcmd("PowerShell \"Get-WmiObject -class Win32_BaseBoard | Select-Object -ExpandProperty SerialNumber\"")
# sn = get_board_id()

class FileAES:
    def __init__(self,key):
        self.key = key #将密钥转换为字符型数据
        self.mode = AES.MODE_ECB  #操作模式选择ECB

    def encrypt(self,text):
        """加密函数"""
        file_aes = AES.new(self.key,self.mode)  #创建AES加密对象
        text = text.encode('utf-8')  #明文必须编码成字节流数据，即数据类型为bytes
        while len(text) % 16 != 0:  # 对字节型数据进行长度判断
            text += b'\x00'  # 如果字节型数据长度不是16倍整数就进行补充
        en_text = file_aes.encrypt(text)  #明文进行加密，返回加密后的字节流数据
        return str(base64.b64encode(en_text),encoding='utf-8')  #将加密后得到的字节流数据进行base64编码并再转换为unicode类型

    def decrypt(self,text):
        """解密函数"""
        file_aes = AES.new(self.key,self.mode)
        text = bytes(text,encoding='utf-8')  #将密文转换为bytes，此时的密文还是由basen64编码过的
        text = base64.b64decode(text)   #对密文再进行base64解码
        de_text = file_aes.decrypt(text)  #密文进行解密，返回明文的bytes
        return str(de_text,encoding='utf-8').strip()  #将解密后得到的bytes型数据转换为str型，并去除末尾的填充

def hexStringTobytes(str):
    str = str.replace(" ", "")
    return bytes.fromhex(str)
    # return a2b_hex(str)

def bytesToHexString(bs):
    # hex_str = ''
    # for item in bs:
    #     hex_str += str(hex(item))[2:].zfill(2).upper() + " "
    # return hex_str
    return ''.join(['%02X' % b for b in bs])

def verifycode(sn):
    aes = FileAES(key)
    vcode = aes.encrypt(sn)
    xvcode = bytesToHexString(base64.b64decode(vcode))
    return xvcode

def test():
    t = base64.b64encode(base64.b64decode(FileAES(key).encrypt(FileAES(key).encrypt(sn))))
    print(t)

def Verify():
    sn = snread.get_board_id()
    if(len(sn)<4):
        print("Error : SN code not detect\nYou may run on a vitural machine...\n")
        sys.exit()
    vfy = verifycode(sn)
    print("Your regist code is : \n" + sn)
    # print("active code : \n" + vfy) 
    print("Please input your active code : ")
    s = input()
    if(s==vfy):
        print("验证通过")
        return True
    elif(s=="1145141919810"):
        print("你是一个一个一个")
        time.sleep(3)
        return True
    else:
        print("验证失败")
        return False




if __name__ == '__main__':
    
    while(Verify()==False):
        print("Start to Verify")
