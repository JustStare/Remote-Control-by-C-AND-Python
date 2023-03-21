import tkinter
import tkinter.messagebox
import struct
import socket
import numpy as np
from PIL import Image, ImageTk
import threading
from cv2 import cv2
import time
import sys
import platform
import client_C
root = tkinter.Tk()

# 画面周期
IDLE = 0.05

# 放缩大小
scale = 1

# 原传输画面尺寸
fixw, fixh = 0, 0

# 放缩标志
wscale = False

# 屏幕显示画布
showcan = None

# socket缓冲区大小
bufsize = 10240

# 线程
th = None

# socket
soc = None

# socks5

socks5 = None

# 平台
PLAT = b''
if sys.platform == "win32":
    PLAT = b'win'
elif sys.platform == "darwin":
    PLAT = b'osx'
elif platform.system() == "Linux":
    PLAT = b'x11'

# 初始化socket

def SetSocket():
    global soc, host_en # 声明全局变量soc和host_en，分别用于存储套接字对象和主机地址输入框
    host = host_en.get() # 获取输入框中的主机地址
    if host is None: # 如果主机地址为空
        tkinter.messagebox.showinfo('提示', 'Host设置错误！') # 弹出提示框显示错误信息
        return # 返回函数
    hs = host.split(":") # 用冒号分割主机地址，得到一个列表hs，包含IP地址和端口号
    if len(hs) != 2: # 如果列表长度不等于2，说明主机地址格式不正确
        tkinter.messagebox.showinfo('提示', 'Host设置错误！') # 弹出提示框显示错误信息
        return # 返回函数
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # 创建一个套接字对象soc，使用IPv4协议和TCP协议
    soc.connect((hs[0], int(hs[1]))) # 用soc连接到指定的IP地址和端口号，hs[0]是IP地址，hs[1]是端口号，需要转换成整数类型
    threading.Thread(target=client_C.start_run, args=(hs[0],)).start()  # 创建一个新的线程，并执行client_C模块中的start_run函数，传入IP地址作为参数


def SetScale(x):
    global scale, wscale # 声明全局变量scale和wscale，分别用于存储缩放比例和缩放标志位
    scale = float(x) / 100 # 将x转换成浮点数，并除以100得到缩放比例scale，x是滑动条的值
    wscale = True # 设置缩放标志位为True


def ShowScreen():
    global showcan, root, soc, th, wscale # 声明全局变量showcan、root、soc、th和wscale，分别用于存储弹出窗口、根窗口、套接字对象、线程对象和缩放标志位
    if showcan is None: # 如果弹出窗口不存在（第一次点击Show按钮）
        wscale = True # 设置缩放标志位为True
        showcan = tkinter.Toplevel(root) # 创建一个弹出窗口showcan，并指定根窗口root为其父窗口
        th = threading.Thread(target=run) # 创建一个线程对象th，并指定run函数为其目标函数（run函数未在代码中给出）
        th.start()
    else:
        soc.close()
        showcan.destroy()


# 创建一个变量，用于存储输入的host信息
val = tkinter.StringVar()

# 创建一个标签，显示“Host:”字样
host_lab = tkinter.Label(root, text="Host:")

# 创建一个输入框，用于输入host信息
host_en = tkinter.Entry(root, show=None, font=('Arial', 14), textvariable=val)

# 创建一个标签，显示“Scale:”字样
sca_lab = tkinter.Label(root, text="Scale:")

# 创建一个滑动条，用于控制显示比例
sca = tkinter.Scale(root, from_=10, to=100, orient=tkinter.HORIZONTAL, length=100,
                    showvalue=100, resolution=0.1, tickinterval=50, command=SetScale)

# 创建一个按钮，用于启动/停止显示屏幕
show_btn = tkinter.Button(root, text="Show", command=ShowScreen)

# 将上述控件放置在窗口中的指定位置
host_lab.grid(row=0, column=0, padx=10, pady=10, ipadx=0, ipady=0)
host_en.grid(row=0, column=1, padx=0, pady=0, ipadx=40, ipady=0)
sca_lab.grid(row=1, column=0, padx=10, pady=10, ipadx=0, ipady=0)
sca.grid(row=1, column=1, padx=0, pady=0, ipadx=100, ipady=0)
show_btn.grid(row=2, column=1, padx=0, pady=10, ipadx=30, ipady=0)

# 设置滑动条的初始值为100
sca.set(100)

# 设置输入框的初始值为'127.0.0.1:80'
val.set('127.0.0.1:80')

# 记录当前时间
last_send = time.time()


def BindEvents(canvas):
    global soc, scale
    '''
    处理事件
    '''
    def EventDo(data):
        soc.sendall(data)  # 就是发送
    # 鼠标左键
                    ## 其中 B 是 1个字节 H 是两个字节 BBHH 也就是6个字节 前两个 是 1 ，100 后两个是 e.x/scale  e.y/scale 也是就是鼠标位置
    def LeftDown(e):           ## 鼠标左键 按下
        return EventDo(struct.pack('>BBHH', 1, 100, int(e.x/scale), int(e.y/scale)))
    def LeftUp(e):
        return EventDo(struct.pack('>BBHH', 1, 117, int(e.x/scale), int(e.y/scale)))
    canvas.bind(sequence="<1>", func=LeftDown)
    canvas.bind(sequence="<ButtonRelease-1>", func=LeftUp)

    # 鼠标右键
    def RightDown(e):
        return EventDo(struct.pack('>BBHH', 3, 100, int(e.x/scale), int(e.y/scale)))

    def RightUp(e):
        return EventDo(struct.pack('>BBHH', 3, 117, int(e.x/scale), int(e.y/scale)))
    canvas.bind(sequence="<3>", func=RightDown)
    canvas.bind(sequence="<ButtonRelease-3>", func=RightUp)

    # 鼠标滚轮
    if PLAT == b'win' or PLAT == 'osx':
        # windows/mac
        def Wheel(e):
            if e.delta < 0:
                return EventDo(struct.pack('>BBHH', 2, 0, int(e.x/scale), int(e.y/scale)))
            else:
                return EventDo(struct.pack('>BBHH', 2, 1, int(e.x/scale), int(e.y/scale)))
        canvas.bind(sequence="<MouseWheel>", func=Wheel)
    elif PLAT == b'x11':
        # linux
        def WheelDown(e):
            return EventDo(struct.pack('>BBHH', 2, 0, int(e.x/scale), int(e.y/scale)))
        def WheelUp(e):
            return EventDo(struct.pack('>BBHH', 2, 1, int(e.x/scale), int(e.y/scale)))
        canvas.bind(sequence="<Button-4>", func=WheelUp)
        canvas.bind(sequence="<Button-5>", func=WheelDown)

    # 鼠标滑动
    # 100ms发送一次
    def Move(e):
        global last_send
        cu = time.time() # 开始计时
        if cu - last_send > IDLE:
            last_send = cu #
            sx, sy = int(e.x/scale), int(e.y/scale)
            return EventDo(struct.pack('>BBHH', 4, 0, sx, sy))
    canvas.bind(sequence="<Motion>", func=Move)

    # 键盘
    def KeyDown(e):
        return EventDo(struct.pack('>BBHH', e.keycode, 100, int(e.x/scale), int(e.y/scale)))

    def KeyUp(e):
        return EventDo(struct.pack('>BBHH', e.keycode, 117, int(e.x/scale), int(e.y/scale)))
    canvas.bind(sequence="<KeyPress>", func=KeyDown)
    canvas.bind(sequence="<KeyRelease>", func=KeyUp)


def run():
    global wscale, fixh, fixw, soc, showcan
    SetSocket()
    # 发送平台信息
    soc.sendall(PLAT)
    lenb = soc.recv(5)
    imtype, le = struct.unpack(">BI", lenb)
    imb = b''
    while le > bufsize:
        t = soc.recv(bufsize)
        imb += t
        le -= len(t)
    while le > 0:
        t = soc.recv(le)
        imb += t
        le -= len(t)
    data = np.frombuffer(imb, dtype=np.uint8)
    img = cv2.imdecode(data, cv2.IMREAD_COLOR)
    h, w, _ = img.shape
    fixh, fixw = h, w
    imsh = cv2.cvtColor(img, cv2.COLOR_RGB2RGBA)
    imi = Image.fromarray(imsh)
    imgTK = ImageTk.PhotoImage(image=imi)
    cv = tkinter.Canvas(showcan, width=w, height=h, bg="white")
    cv.focus_set()
    BindEvents(cv)
    cv.pack()
    cv.create_image(0, 0, anchor=tkinter.NW, image=imgTK)
    h = int(h * scale)
    w = int(w * scale)
    while True:
        if wscale:
            h = int(fixh * scale)
            w = int(fixw * scale)
            cv.config(width=w, height=h)
            wscale = False
        try:
            lenb = soc.recv(5)
            imtype, le = struct.unpack(">BI", lenb)
            imb = b''
            while le > bufsize:
                t = soc.recv(bufsize)
                imb += t
                le -= len(t)
            while le > 0:
                t = soc.recv(le)
                imb += t
                le -= len(t)
            data = np.frombuffer(imb, dtype=np.uint8)
            ims = cv2.imdecode(data, cv2.IMREAD_COLOR)
            if imtype == 1:
                # 全传
                img = ims
            else:
                # 差异传
                img = img ^ ims
            imt = cv2.resize(img, (w, h))
            imsh = cv2.cvtColor(imt, cv2.COLOR_RGB2RGBA)
            imi = Image.fromarray(imsh)
            imgTK.paste(imi)
        except:
            showcan = None
            ShowScreen()
            return


root.mainloop()
