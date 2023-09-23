import pyautogui
import tkinter as tk
import os
# pip install pillow, 用Image模块操作图片文件
from PIL import Image
import keyboard
# BytesIO是操作二进制数据的模块
from io import BytesIO

# pip install pywin32, win32clipboard是操作剪贴板的模块
import win32clipboard

def send_msg_to_clip(type_data, msg):
    """
    操作剪贴板分四步：
    1. 打开剪贴板：OpenClipboard()
    2. 清空剪贴板，新的数据才好写进去：EmptyClipboard()
    3. 往剪贴板写入数据：SetClipboardData()
    4. 关闭剪贴板：CloseClipboard()

    :param type_data: 数据的格式，
    unicode字符通常是传 win32con.CF_UNICODETEXT
    :param msg: 要写入剪贴板的数据
    """
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(type_data, msg)
    win32clipboard.CloseClipboard()


def paste_img(file_img):
    """
    图片转换成二进制字符串，然后以位图的格式写入剪贴板

    主要思路是用Image模块打开图片，
    用BytesIO存储图片转换之后的二进制字符串

    :param file_img: 图片的路径
    """
    # 把图片写入image变量中
    # 用open函数处理后，图像对象的模式都是 RGB
    image = Image.open(file_img)

    # 声明output字节对象
    output = BytesIO()

    # 用BMP (Bitmap) 格式存储
    # 这里是位图，然后用output字节对象来存储
    image.save(output, 'BMP')

    # BMP图片有14字节的header，需要额外去除
    data = output.getvalue()[14:]

    # 关闭
    output.close()

    # DIB: 设备无关位图(device-independent bitmap)，名如其意
    # BMP的图片有时也会以.DIB和.RLE作扩展名
    # 设置好剪贴板的数据格式，再传入对应格式的数据，才能正确向剪贴板写入数据
    send_msg_to_clip(win32clipboard.CF_DIB, data)


root = tk.Tk()
root.overrideredirect(True)         # 隐藏窗口的标题栏
root.attributes("-alpha", 0.1)      # 窗口透明度10%
root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.configure(bg="black")

# 再创建1个Canvas用于圈选
cv = tk.Canvas(root)
x, y = 0, 0
xstart,ystart = 0 ,0
xend,yend = 0, 0
rec = ''

# 绘制工具条
canvas = tk.Canvas(root)
canvas.configure(width=300)
canvas.configure(height=100)
canvas.configure(bg="yellow")
canvas.configure(highlightthickness=0)  # 高亮厚度
canvas.place(x=(root.winfo_screenwidth()-500),y=(root.winfo_screenheight()-300))
canvas.create_text(150, 50,font='Arial -20 bold',text='ESC退出, 假装工具条')




def move(event):
    global x, y ,xstart,ystart
    new_x = (event.x-x)+canvas.winfo_x()
    new_y = (event.y-y)+canvas.winfo_y()
    s = "300x200+" + str(new_x)+"+" + str(new_y)    
    canvas.place(x = new_x - xstart,y = new_y -ystart)   
    print("s = ", s)
    print(root.winfo_x(), root.winfo_y())
    print(event.x, event.y)

def button_1(event):
    global x, y ,xstart,ystart
    global rec
    x, y = event.x, event.y
    xstart,ystart = event.x, event.y
    print("event.x, event.y = ", event.x, event.y)
    xstart,ystart = event.x, event.y  
    cv.configure(height=1)
    cv.configure(width=1)
    cv.config(highlightthickness=0) # 无边框
    cv.place(x=event.x, y=event.y)
    rec = cv.create_rectangle(0,0,0,0,outline='red',width=0,dash=None)

def b1_Motion(event):
    global x, y,xstart,ystart
    x, y = event.x, event.y
    print("event.x, event.y = ", event.x, event.y)
    cv.configure(height = event.y - ystart)
    cv.configure(width = event.x - xstart)
    cv.coords(rec,0,0,event.x-xstart,event.y-ystart)

def buttonRelease_1(event):
    global xend,yend
    xend, yend = event.x, event.y

def button_3(event):
    global xstart,ystart,xend,yend
    cv.delete(rec)
    cv.place_forget()
    img = pyautogui.screenshot(region=[xstart,ystart,xend-xstart,yend-ystart]) # x,y,w,h
    # img.save('screenshot.png')
    photo = r"D:\Desktop\screenshot\photo\{}.png".format(pyautogui.time.time())
    img.save(photo)
    file_image = photo
    paste_img(file_image)
    sys_out(None)

def sys_out(even):
    root.destroy()

exit_button = tk.Button(canvas, text="退出", command=sys_out) # 添加command参数 
exit_button.place(x=(root.winfo_screenwidth()-500),y=(root.winfo_screenheight()-300)) # 调整按钮位置

# 绑定事件
canvas.bind("<B1-Motion>", move)   # 鼠标左键移动->显示当前光标位置
root.bind('<Escape>',sys_out)      # 键盘Esc键->退出
root.bind("<Button-1>", button_1)  # 鼠标左键点击->显示子窗口 
root.bind("<B1-Motion>", b1_Motion)# 鼠标左键移动->改变子窗口大小
root.bind("<ButtonRelease-1>", buttonRelease_1) # 鼠标左键释放->记录最后光标的位置
root.bind("<Button-3>",button_3)   #鼠标右键点击->截屏并保存图片

# 定义一个变量，用于记录是否启动截图功能
is_screenshot = False

# 定义一个函数，用于切换截图功能的状态
def toggle_screenshot():
    global is_screenshot
    is_screenshot = not is_screenshot

# 注册快捷键ctrl+b，用于切换截图功能的状态
keyboard.add_hotkey("ctrl+b", toggle_screenshot)

# 进入无限循环，等待快捷键的响应
while True:
    # 如果启动了截图功能
    if is_screenshot:
        # 等待鼠标按下
        pyautogui.mouseDown()
        # 调用截图函数
        # 关闭截图功能
        is_screenshot = False
        break

root.mainloop()