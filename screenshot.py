import pyautogui
import keyboard
import os

#pyinstaller --onefile --noconsole --icon=screenshot.ico --name=screenshot main.py

# 定义一个函数，用于截取鼠标划选的范围，并将图片保存到剪切板和指定文件夹
def screenshot():
    # 获取鼠标按下时的坐标
    x1, y1 = pyautogui.position()
    # 等待鼠标松开
    pyautogui.mouseUp()
    # 获取鼠标松开时的坐标
    x2, y2 = pyautogui.position()
    # 计算截图区域的宽度和高度
    width = abs(x2 - x1)
    height = abs(y2 - y1)
    # 判断截图区域是否有效
    if width > 0 and height > 0:
        # 截取指定区域的图片
        image = pyautogui.screenshot(region=(min(x1, x2), min(y1, y2), width, height))
        # 将图片复制到剪切板
        image.save(r"D:\Desktop\screenshot\photo\temp.png")
        os.system("clip < D:\Desktop\screenshot\photo\temp.png")
        # 将图片保存到指定文件夹，并以当前时间为文件名
        image.save(r"D:\Desktop\screenshot\photo\{}.png".format(pyautogui.time.time()))

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
        screenshot()
        # 关闭截图功能
        is_screenshot = False
