#!/usr/bin/env python3
import os
import sys
import subprocess
# import tk/tcl
import tkinter as tk 
from tkinter import ttk
from tkinter.filedialog import *
from tkinter import *
from tkinter import scrolledtext
from ttkbootstrap import Style  # use ttkbootstrap theme
from bs4 import BeautifulSoup
import requests
# using threading in some function
import threading
import time
import webbrowser
# add pyscripts into sys path
sys.path.append(".\\pyscripts")
# import functions I modified
import utils
# import sn read board id
import sn
import verifysn
# import ozip decrypt
import ozip_decrypt  # ozip_decrypt.main(filepath)
# import get_miui
import get_miui

# Flag
DEBUG = True                    # 显示调试信息
HIDE_CONSOLE = False            # 隐藏控制台
MENUBAR = True                  # 菜单栏
USEMYLOGO = True                # 使用自己的logo
TEXTREADONLY = True             # 文本框只读
TEXTSHOWBANNER = True           # 展示那个文本框的字符画
USEMYSTD = False                # 输出重定向到Text控件
SHOWSHIJU = False               # 展示诗句
USESTATUSBAR = False            # 使用状态栏（并不好用）
VERIFYPROG = False              # 程序验证（本来打算恰烂钱的）
EXECPATH = ".\\bin"             # 临时添加可执行程序目录到系统变量
LICENSE = "Apache 2.0"          # 程序的开源协议

# Verify
if(VERIFYPROG):
    VERIFYCODE = ".\\bin\\VERIFYCODE"
    if(os.access(VERIFYCODE, os.F_OK)):
        vf2code = verifysn.verifycode(sn.get_board_id())
        with open(VERIFYCODE) as vcode:
            vf = vcode.readline()
            f = open(VERIFYCODE, "r")
            vfcode = f.readline()
        if(vf2code == vfcode):
            print("Verify Successfully...")
        else:
            while(verifysn.Verify()==False):
                print("Verify -->")
            print("Save code ...")
            with open(VERIFYCODE,"w") as f:
                f.write(vf2code.encode("utf-8").decode("utf-8"))
    else:
        try:
            print("Verify online -->")
            snurl = "https://gitee.com/affggh/nh4-verify/raw/master/all.json"
            bypass_systemProxy = { "http" : None,
                                   "https" : None}
            fetchv = requests.get(snurl, proxies=bypass_systemProxy)
            fetchvjason = fetchv.json()
            boardid = sn.get_board_id()
            vfcode = fetchvjason[boardid]
            vf2code = verifysn.verifycode(sn.get_board_id())
            if(vfcode == vf2code):
                print("Verify Successfully...")
                print("Save code ...")
                with open(VERIFYCODE,"w") as f:
                    f.write(vfcode.encode("utf-8").decode("utf-8"))
            else:
                print("Verify Failed...")
                print("please input your active code : \n")
                while(verifysn.Verify()==False):
                    print("Verify -->")
        except:
            vf2code = verifysn.verifycode(sn.get_board_id())
            print("Verify Failed...")
            print("please input your active code : \n")
            while(verifysn.Verify()==False):
                print("Verify -->")
            print("Save code ...")
            with open(VERIFYCODE,"w") as f:
                f.write(vf2code.encode("utf-8").decode("utf-8"))

# Var
VERSION = "20220305"
AUTHOR = "affggh"
WINDOWTITLE = "NH4RomTool (沼_Rom工具箱)" + "    版本：" + VERSION + "    作者：" + AUTHOR
THEME = "vapor"  # 设置默认主题
LOGOICO = ".\\bin\\logo.ico"
BANNER = ".\\bin\\banner"
TEXTFONT = '微软雅黑'

if(EXECPATH):
    utils.addExecPath(EXECPATH)

if(HIDE_CONSOLE):  # 隐藏控制台
    utils.hideForegroundWindow

style = Style(theme=THEME)

# Begin of window
root = style.master

width = 1240
height = 440

if(USESTATUSBAR):
    height += 20

root.geometry("%sx%s" %(width,height))
# root.resizable(0,0) # 设置最大化窗口不可用
root.title(WINDOWTITLE)

# Set images
LOGOIMG = tk.PhotoImage(file=".\\bin\\logo.png")
ALIPAYIMG = tk.PhotoImage(file=".\\bin\\alipay.png")
WECHATIMG = tk.PhotoImage(file=".\\bin\\wechat.png")
ALIREDPACIMG = tk.PhotoImage(file=".\\bin\\zfbhb.png")

global WorkDir
WorkDir = False

# Var
filename = tk.StringVar()
inputvar = tk.StringVar()

# from https://www.i4k.xyz/article/weixin_49317370/108878373
class myStdout():	# 重定向类
    def __init__(self):
    	# 将其备份
        self.stdoutbak = sys.stdout		
        self.stderrbak = sys.stderr
        # 重定向
        sys.stdout = self
        sys.stderr = self

    def write(self, info):
        # info信息即标准输出sys.stdout和sys.stderr接收到的输出信息
        # text.insert('end', info)	# 在多行文本控件最后一行插入print信息
        # text.update()	# 更新显示的文本，不加这句插入的信息无法显示
        # text.see(tkinter.END)	# 始终显示最后一行，不加这句，当文本溢出控件最后一行时，不会自动显示最后一行
        if(TEXTREADONLY):
            text.configure(state='normal')
        text.insert(END,"[%s]" %(utils.get_time()) + "%s" %(info))
        text.update() # 实时返回信息
        text.yview('end')
        if(TEXTREADONLY):
            text.configure(state='disable')

    def restoreStd(self):
        # 恢复标准输出
        sys.stdout = self.stdoutbak
        sys.stderr = self.stderrbak

def logo():
    utils.chLocal()
    root.iconbitmap(LOGOICO)

if(USEMYLOGO):
    logo()

def VisitMe():
    webbrowser.open("https://github.com/affggh")

def showinfo(textmsg):
    if(TEXTREADONLY):
        text.configure(state='normal')
    text.insert(END,"[%s]" %(utils.get_time()) + "%s" %(textmsg) + "\n")
    text.update() # 实时返回信息
    text.yview('end')
    if(TEXTREADONLY):
        text.configure(state='disable')

def runcmd(cmd):
    try:
        ret = subprocess.Popen(cmd,shell=False,
                 stdin=subprocess.PIPE,
                 stdout=subprocess.PIPE,
                 stderr=subprocess.STDOUT)
        for i in iter(ret.stdout.readline,b""):
            showinfo(i.decode("utf-8").strip())
    except subprocess.CalledProcessError as e:
        for i in iter(e.stdout.readline,b""):
            showinfo(e.decode("utf-8").strip())

def showstatus():
    print("test")

def showbanner():
    if(TEXTSHOWBANNER):
        with open(BANNER, "r") as b:
            for i in b.readlines():
                showinfo(i.replace('\n',''))

def cleaninfo():
    if(TEXTREADONLY):
        text.configure(state='normal')
    text.delete(1.0, END)  # 清空text
    # text.image_create(END,image=LOGOIMG)
    # text.insert(END,"\n")
    showbanner()
    if(TEXTREADONLY):
        text.configure(state='disable')

def selectFile():
    filepath = askopenfilename()                   # 选择打开什么文件，返回文件名
    filename.set(filepath.replace('/', '\\'))      # 设置变量filename的值
    showinfo("选择文件为：\n%s" %(filepath.replace('/', '\\')))

def about():
    root2 = tk.Toplevel()
    curWidth = 300
    curHight = 180
    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)
    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    root2.geometry(size_xy)
    #root2.geometry("300x180")
    root2.resizable(0,0) # 设置最大化窗口不可用
    root2.title("关于脚本和作者信息")
    aframe1 = Frame(root2, relief=FLAT, borderwidth=1)
    aframe2 = Frame(root2, relief=FLAT, borderwidth=1)
    aframe1.pack(side=BOTTOM, expand=YES, pady=3)
    aframe2.pack(side=BOTTOM, expand=YES, pady=3)
    ttk.Button(aframe1, text='访问作者主页', command=VisitMe,style='primiary.Outline.TButton').pack(side=LEFT, expand=YES, padx=5)
    ttk.Button(aframe1, text=' 给作者打钱 ', command=VisitMe,style='success.TButton').pack(side=LEFT, expand=YES, padx=5)
    ttk.Label(aframe2, text='沼_Rom工具箱 Version %s\nGUI Written by python tk/tcl\nTheme by ttkbootstrap\n%s Copyright(R) Apache 2.0 LICENSE'%(VERSION,AUTHOR)).pack(side=BOTTOM, expand=NO, pady=3)
    utils.chLocal()
    
    imgLabe2 = ttk.Label(aframe2,image=LOGOIMG)#把图片整合到标签类中
    imgLabe2.pack(side=TOP, expand=YES, pady=3)
    root2.mainloop()

def userInputWindow():
    inputWindow = tk.Toplevel()
    curWidth = 400
    curHight = 120
    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)
    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    inputWindow.geometry(size_xy)
    #inputWindow.geometry("300x180")
    inputWindow.resizable(0,0) # 设置最大化窗口不可用
    inputWindow.title("输入文本")
    ent = ttk.Entry(inputWindow,textvariable=inputvar,width=50)
    ent.pack(side=TOP, expand=YES, padx=5)
    ttk.Button(inputWindow, text='确认', command=inputWindow.destroy,style='primiary.Outline.TButton').pack(side=TOP, expand=YES, padx=5)
    inputWindow.wait_window()

def fileChooseWindow(tips):
    chooseWindow = tk.Toplevel()
    curWidth = 400
    curHight = 120
    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)
    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    chooseWindow.geometry(size_xy)
    #chooseWindow.geometry("300x180")
    chooseWindow.resizable(0,0) # 设置最大化窗口不可用
    chooseWindow.title(tips)
    ent = ttk.Entry(chooseWindow,textvariable=filename,width=50)
    ent.pack(side=TOP, expand=NO, padx=0, pady=20)
    ttk.Button(chooseWindow, text='确认', width=15, command=chooseWindow.destroy,style='primiary.Outline.TButton').pack(side=RIGHT, expand=YES, padx=5, pady=5)
    ttk.Button(chooseWindow, text='选择文件', width=15, command=lambda:[selectFile(),chooseWindow.destroy()],style='primiary.TButton').pack(side=RIGHT, expand=YES, padx=5,  pady=5)
    chooseWindow.wait_window()

def change_theme(var):
    if(DEBUG):
        print("change Theme : " + var)
    showinfo("设置主题为 : " + var)
    style = Style(theme=var)
    style.theme_use()

def getWorkDir():
    x = table.get_children()
    for item in x:
        table.delete(item)
    d = utils.listDirHeader('.\\','NH4_')
    for item in d:
        table.insert('','end',values=item)

def SelectWorkDir():
    item_text = ['']
    for item in table.selection():
        item_text = table.item(item,"values")
    if(item_text[0]!=""):
        global WorkDir
        WorkDir = item_text[0]
        showinfo("选择工作目录为：%s" %(WorkDir))

def ConfirmWorkDir():
    if not (WorkDir):
        showinfo("Warning : 请选择一个目录")
    else:
        tabControl.select(tab2)

def tableClicked(event):
    SelectWorkDir()

def rmWorkDir():
    if(WorkDir):
        showinfo("删除目录：%s" %(WorkDir))
        utils.rmdir(WorkDir)
    else:
        showinfo("Error : 要删除的文件夹不存在")
    getWorkDir()

def mkWorkdir():
    userInputWindow()
    showinfo("用户输入：%s" %(inputvar.get()))
    utils.mkdir("NH4_" + "%s" %(inputvar.get()))
    getWorkDir()

def detectFileType():
    fileChooseWindow("检测文件类型")
    if(os.access(filename.get(), os.F_OK)):
        showinfo("文件格式为 ：")
        runcmd("gettype -i %s" %(filename.get()))
    else:
        showinfo("Error : 文件不存在")

def ozipDecrypt():
    fileChooseWindow("解密ozip")
    if(os.access(filename.get(), os.F_OK)):
        ozip_decrypt.main("%s" %(filename.get()))
    else:
        showinfo("Error : 文件不存在")

def getMiuiWindow():
    def __downloadurl(url):
        webbrowser.open(url)

    def downloadurl(url):
        T = threading.Thread(target=__downloadurl(url))
        T.start()

    def downloadMiuiRom():
        getmiuiWindow.destroy()
        url = get_miui.get("%s" %(DEVICE_CODE.get()), 
                           "%s" %(regionselect.get()), 
                           "%s" %(packagetype.get()), 
                           "%s" %(ver.get()))
        utils.thrun(downloadurl(url))

    def showurl():
        url = get_miui.get("%s" %(DEVICE_CODE.get()), "%s" %(regionselect.get()), "%s" %(packagetype.get()), "%s" %(ver.get()))
        showinfo("url : " + url)
    getmiuiWindow = tk.Toplevel()
    curWidth = 260
    curHight = 380
    # 获取屏幕宽度和高度
    scn_w, scn_h = root.maxsize()
    # print(scn_w, scn_h)
    # 计算中心坐标
    cen_x = (scn_w - curWidth) / 2
    cen_y = (scn_h - curHight) / 2
    # print(cen_x, cen_y)

    # 设置窗口初始大小和位置
    size_xy = '%dx%d+%d+%d' % (curWidth, curHight, cen_x, cen_y)
    getmiuiWindow.geometry(size_xy)
    #getmiuiWindow.geometry("300x180")
    getmiuiWindow.resizable(0,0) # 设置最大化窗口不可用
    getmiuiWindow.title("MIUI 最新rom获取程序")
    DEVICE_CODE = tk.StringVar()
    ttk.Label(getmiuiWindow,text="设备开发代号").pack(side=TOP, expand=NO, padx=5, pady=10)
    ent = ttk.Entry(getmiuiWindow,textvariable=DEVICE_CODE,width=25)
    ent.pack(side=TOP, expand=NO, padx=5)
    regionselect = tk.StringVar()
    regions = ['CN', 'RU', 'Global', 'ID', 'IN', 'EEA', 'TR', 'TW', 'JP', 'SG']
    ttk.Label(getmiuiWindow,text="区域").pack(side=TOP, expand=NO, padx=5, pady=10)
    comboxlist = ttk.Combobox(getmiuiWindow, textvariable=regionselect, width=23)
    comboxlist["values"]=(regions)
    comboxlist.current(0) # 选择第一个
    comboxlist.pack(side=TOP, expand=NO, padx=5)
    
    packagetype = tk.StringVar()
    types = ['recovery', 'fastboot']
    ttk.Label(getmiuiWindow,text="类型").pack(side=TOP, expand=NO, padx=5, pady=10)
    comboxlist2 = ttk.Combobox(getmiuiWindow, textvariable=packagetype, width=23)
    comboxlist2["values"]=(types)
    comboxlist2.current(0) # 选择第一个
    comboxlist2.pack(side=TOP, expand=NO, padx=5)
    
    ver = tk.StringVar()
    vers = ['stable', 'beta']
    ttk.Label(getmiuiWindow,text="稳定版/开发版").pack(side=TOP, expand=NO, padx=5, pady=10)
    comboxlist3 = ttk.Combobox(getmiuiWindow, textvariable=ver, width=23)
    comboxlist3["values"]=(vers)
    comboxlist3.current(0) # 选择第一个
    comboxlist3.pack(side=TOP, expand=NO, padx=5)
    ttk.Button(getmiuiWindow, text='确认', width=10, command=lambda:[showurl(),getmiuiWindow.destroy()],style='primiary.Outline.TButton').pack(side=LEFT, expand=YES, padx=10)
    ttk.Button(getmiuiWindow, text='下载', width=10, command=downloadMiuiRom,style='primiary.TButton').pack(side=LEFT, expand=YES, padx=10)
    getmiuiWindow.wait_window()

def __unzipfile():
    fileChooseWindow("选择要解压的文件")
    if(WorkDir):
        if(os.access(filename.get(), os.F_OK)):
            showinfo("正在解压文件：" + filename.get())
            utils.unzip_file(filename.get(), WorkDir + "\\rom")
            showinfo("解压完成")
        else:
            showinfo("Error : 文件不存在")
    else:
        showinfo("Error : 请先选择工作目录")

def unzipfile():
    T = threading.Thread(target=__unzipfile())
    T.start()

def __zipcompressfile():
    showinfo("输入生成的文件名")
    userInputWindow()
    if(WorkDir):
        showinfo("正在压缩 ：" + inputvar.get() + ".zip")
        utils.zip_file(inputvar.get()+".zip", WorkDir + "\\rom")
        showinfo("压缩完成")
    else:
        showinfo("Error : 请先选择工作目录")

def zipcompressfile():
    T = threading.Thread(target=__zipcompressfile())
    T.start()

def Test():
    showinfo("Test function")

if __name__ == '__main__':

    if(USEMYSTD):
        mystd = myStdout()
    else:
        # mystd.restoreStd()
        print("Use standard stdout and stderr...")
    #在中心打开主窗口
    screenwidth = root.winfo_screenwidth()  # 屏幕宽度
    screenheight = root.winfo_screenheight()  # 屏幕高度
    x = int((screenwidth - width) / 2)
    y = int((screenheight - height) / 2)
    root.geometry('{}x{}+{}+{}'.format(width, height, x, y))  # 大小以及位置

    if(MENUBAR):   # 菜单栏
        menuBar = tk.Menu(root)
        root.config(menu=menuBar)
        menu1 = tk.Menu(menuBar, tearoff=False)
        menuItem = ["关于","退出"]
        for item in menuItem:
            if(item=="关于"):
                menu1.add_command(label=item, command=about)
            if(item=="退出"):
                menu1.add_command(label=item, command=sys.exit)
        menuBar.add_cascade(label="菜单", menu=menu1)
        menu2 = tk.Menu(menuBar, tearoff=False)
        menuItem = ["cosmo","flatly","journal","literal","lumen","minty","pulse","sandstone","united","yeti","cyborg","darkly","solar","vapor","superhero"]
        for item in menuItem:
            menu2.add_command(label=item, command=lambda n=item:change_theme(n))
        menuBar.add_cascade(label="主题", menu=menu2)

    # Status bar
    if(USESTATUSBAR):
        statusbar = ttk.Label(root, text='status bar', relief='flat', anchor=tk.E, bootstyle="info")
        statusbar.pack(side=tk.BOTTOM, fill=tk.X, ipadx=12)

    # define labels
    frame = ttk.LabelFrame(root, text="- - NH4 Rom Tool - -", labelanchor="nw", relief=GROOVE, borderwidth=1)
    frame1 = ttk.LabelFrame(frame, text="功能区", labelanchor="nw", relief=SUNKEN, borderwidth=1)
    frame2 = ttk.LabelFrame(frame, text="信息反馈", labelanchor="nw", relief=SUNKEN, borderwidth=1)

    # Notebook
    tabControl = ttk.Notebook(frame1)
    # tab
    tab1 = ttk.Frame(tabControl)
    tab2 = ttk.Frame(tabControl)
    tab3 = ttk.Frame(tabControl)
    tab4 = ttk.Frame(tabControl)

    tabControl.add(tab1, text="工作目录")
    tabControl.add(tab2, text="打包解包")
    tabControl.add(tab3, text="其他工具")
    tabControl.add(tab4, text="设置")

    # Treeview  use to list work dir
    tab11 = ttk.Frame(tab1)

    columns = ["Workdir"]
    table = ttk.Treeview(
            tab11,  # 父容器
            height=10,  # 表格显示的行数,height行
            columns=columns,  # 显示的列
            show='headings',  # 隐藏首列
            )
    table.column('Workdir', width=100, anchor='center')
    table.heading('Workdir', text='工作目录')
    table.pack(side=LEFT, fill=BOTH, expand=YES)
    table.bind('<ButtonRelease-1>',tableClicked)
    getWorkDir()
    
    # Buttons under Treeview
    tab12 = ttk.Frame(tab1)
    ttk.Button(tab12, text='确认目录', width=10, command=ConfirmWorkDir,style='primiary.Outline.TButton').grid(row=0, column=0, padx='10', pady='8')
    ttk.Button(tab12, text='删除目录', width=10, command=rmWorkDir,style='primiary.Outline.TButton').grid(row=0, column=1, padx='10', pady='8')
    ttk.Button(tab12, text='新建目录', width=10, command=mkWorkdir,style='primiary.Outline.TButton').grid(row=1, column=0, padx='10', pady='8')
    ttk.Button(tab12, text='刷新目录', width=10, command=getWorkDir,style='primiary.Outline.TButton').grid(row=1, column=1, padx='10', pady='8')
    
    # Pack Buttons
    tab12.pack(side=BOTTOM, fill=BOTH, expand=NO)
    
    # pack Notebook
    tabControl.pack(fill=BOTH, expand=YES)
    tab11.pack(side=TOP, fill=BOTH, expand=YES)
    
    # tab21 // Unpack
    tab21 = ttk.LabelFrame(tab2, text="解包", labelanchor="nw", relief=SUNKEN, borderwidth=1)
    ttk.Button(tab21, text='解压', width=10, command=unzipfile,style='primiary.Outline.TButton').grid(row=0, column=0, padx='10', pady='8')
    
    # tab22 // Repack
    tab22 = ttk.LabelFrame(tab2, text="打包", labelanchor="nw", relief=SUNKEN, borderwidth=1)
    ttk.Button(tab22, text='压缩', width=10, command=zipcompressfile,style='primiary.Outline.TButton').grid(row=0, column=0, padx='10', pady='8')
    
    # pack tab2
    tab21.pack(side=TOP, fill=BOTH, expand=YES)
    tab22.pack(side=TOP, fill=BOTH, expand=YES)

    # tab3
    ttk.Button(tab3, text='检测文件格式', width=10, command=detectFileType,style='primiary.TButton').grid(row=0, column=0, padx='10', pady='8')
    ttk.Button(tab3, text='ozip解密', width=10, command=ozipDecrypt,style='primiary.TButton').grid(row=0, column=1, padx='10', pady='8')
    ttk.Button(tab3, text='get_MIUI', width=10, command=getMiuiWindow,style='primiary.TButton').grid(row=1, column=0, padx='10', pady='8')

    # ScrolledText
    text = scrolledtext.ScrolledText(frame2, width=180, height=18, font=TEXTFONT, relief=SOLID) # 信息展示 文本框
    text.pack(side=RIGHT, expand=YES, fill=BOTH , padx=4, pady=2)
    # table.bind('<ButtonPress-1>', showinfo("请点击确认目录"))

    # pack frames
    frame.pack(side=TOP, expand=NO, fill=BOTH, padx=2, pady=2)
    frame1.pack(side=LEFT, expand=YES, fill=BOTH, padx=5, pady=2)
    frame2.pack(side=LEFT, expand=YES, fill=BOTH, padx=5, pady=2)

    # bottom labels
    framebotm = ttk.Frame(root, relief=FLAT)
    ttk.Button(framebotm, text='清理信息', command=cleaninfo,style='secondary.TButton').pack(side=RIGHT, expand=NO, padx=5,pady=0)
    # shiju
    if(SHOWSHIJU):
        shiju = utils.getShiju()
        shiju_font = ('微软雅黑',12)
        shijuLable = ttk.Label(framebotm, text="%s —— %s  《%s》" %(shiju['content'],shiju['author'],shiju['origin']), font=shiju_font)
        shijuLable.pack(side=LEFT,padx=8)
    framebotm.pack(side=BOTTOM,expand=YES, fill=X, padx=8, pady=0)

    if(TEXTSHOWBANNER):
        showbanner()

    if(DEBUG):
        showinfo("Board id : " + sn.get_board_id())
    else:
        showinfo("        Version : %s" %(VERSION))
        showinfo("        Author  : %s" %(AUTHOR))
        showinfo("        LICENSE : %s" %(LICENSE))

    root.update()
    root.mainloop()
    
    if(USEMYSTD):
        mystd.restoreStd() # 还原标准输出