# -*- coding: utf-8 -*-
import os,re,shutil
import sys
import glob

def search(filename):
    
    dirfile = glob.glob(filename + "/*")
    for file in dirfile:
        search(file)
        if fsn == "system":
            filea = file.replace(dirna + "/system/","")
        else:
            filea = file.replace(dirna + "/","")
        # os.system("echo " + filea + " >> " + fsa)
        with open(fsa,"a") as f:
            f.write(filea+"\n")
        



filename = sys.argv[1]
fsa = sys.argv[2]
dirna = sys.argv[3]
fsn = sys.argv[4]
search(filename)
os.system("sort  -n " + fsa + "| uniq > " + fsa + "a")
shutil.move(fsa + "a",fsa)
os.system("cut -d ' ' -f 1 " + dirna + "/TI_config/" + fsn + "_fs_config > " + dirna + "/TI_config/a")
e = open(dirna + "/TI_config/a","r")
b = open(fsa,"r")
g = e.read().split()
d = b.read().split()
re = set(d).difference(set(g))
if not re == set():
    no = open(dirna + "/TI_config/" + fsn + "_fs_config","r")
    nonei = no.read()
    new = open (dirna + "/TI_config/" + fsn + "_fs_confign","w")
    for i in re:
        if os.path.isdir(dirna + "/system/" + i):
            new.write(i + " 0 0 0755\n")
        elif os.path.isfile(dirna + "/system/" +i):
            new.write(i + " 0 0 0644\n")
        elif os.path.isdir(dirna + "/" + i):
            new.write(i + " 0 0 0755\n")
        elif os.path.isfile(dirna + "/" +i):
                new.write(i + " 0 0 0644\n")
    for a in nonei:
        new.write(str(a))
    shutil.move(dirna + "/TI_config/" + fsn + "_fs_confign",dirna + "/TI_config/" + fsn + "_fs_config")
os.remove(fsa)
os.remove(dirna + "/TI_config/a")
           
        