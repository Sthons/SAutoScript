@echo off
chcp 65001 >nul
echo ========================================
echo DNAAS 模板创建工具
echo ========================================
echo.
echo 此工具将帮助您创建游戏截图模板
echo.
echo 使用说明:
echo 1. 将鼠标移动到要截图区域的左上角
echo 2. 按下F1键记录左上角坐标
echo 3. 将鼠标移动到要截图区域的右下角
echo 4. 按下F2键记录右下角坐标
echo 5. 输入模板文件名
echo 6. 按下F3键保存截图
echo.
echo 按任意键开始...
pause >nul

REM 检查虚拟环境是否存在
if not exist ".venv\Scripts\python.exe" (
    echo 虚拟环境不存在，正在创建...
    call python install.py
    if errorlevel 1 (
        echo 安装失败，请检查错误信息
        pause
        exit /b 1
    )
)

.venv\Scripts\python -c "
import os
import sys
import time
import pyautogui
from PIL import Image
import numpy as np
import mss
import mss.tools

# 初始化mss对象
sct = mss.mss()

# 存储坐标
coords = {'top_left': None, 'bottom_right': None}

def on_press(key):
    try:
        if key.name == 'f1':
            # 记录左上角坐标
            x, y = pyautogui.position()
            coords['top_left'] = (x, y)
            print(f'左上角坐标已记录: ({x}, {y})')
        elif key.name == 'f2':
            # 记录右下角坐标
            x, y = pyautogui.position()
            coords['bottom_right'] = (x, y)
            print(f'右下角坐标已记录: ({x}, {y})')
        elif key.name == 'f3':
            # 保存截图
            if coords['top_left'] and coords['bottom_right']:
                x1, y1 = coords['top_left']
                x2, y2 = coords['bottom_right']
                
                # 确保坐标顺序正确
                left = min(x1, x2)
                top = min(y1, y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                
                # 设置捕获区域
                monitor = {
                    'top': top,
                    'left': left,
                    'width': width,
                    'height': height
                }
                
                # 捕获屏幕
                screenshot = sct.grab(monitor)
                
                # 转换为PIL图像
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # 获取文件名
                filename = input('请输入模板文件名(不带扩展名): ')
                if not filename:
                    filename = f'template_{int(time.time())}'
                
                # 保存文件
                filepath = os.path.join('assets', 'templates', f'{filename}.png')
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                img.save(filepath)
                
                print(f'模板已保存: {filepath}')
                return False  # 停止监听
            else:
                print('请先记录左上角和右下角坐标')
    except Exception as e:
        print(f'错误: {e}')
    
    return True  # 继续监听

# 监听键盘事件
import keyboard

print('开始监听键盘事件...')
print('F1: 记录左上角坐标')
print('F2: 记录右下角坐标')
print('F3: 保存截图')
print('ESC: 退出')

while True:
    try:
        if keyboard.is_pressed('f1'):
            x, y = pyautogui.position()
            coords['top_left'] = (x, y)
            print(f'左上角坐标已记录: ({x}, {y})')
            time.sleep(0.5)  # 防止重复触发
        elif keyboard.is_pressed('f2'):
            x, y = pyautogui.position()
            coords['bottom_right'] = (x, y)
            print(f'右下角坐标已记录: ({x}, {y})')
            time.sleep(0.5)  # 防止重复触发
        elif keyboard.is_pressed('f3'):
            if coords['top_left'] and coords['bottom_right']:
                x1, y1 = coords['top_left']
                x2, y2 = coords['bottom_right']
                
                # 确保坐标顺序正确
                left = min(x1, x2)
                top = min(y1, y2)
                width = abs(x2 - x1)
                height = abs(y2 - y1)
                
                # 设置捕获区域
                monitor = {
                    'top': top,
                    'left': left,
                    'width': width,
                    'height': height
                }
                
                # 捕获屏幕
                screenshot = sct.grab(monitor)
                
                # 转换为PIL图像
                img = Image.frombytes('RGB', screenshot.size, screenshot.rgb)
                
                # 获取文件名
                filename = input('请输入模板文件名(不带扩展名): ')
                if not filename:
                    filename = f'template_{int(time.time())}'
                
                # 保存文件
                filepath = os.path.join('assets', 'templates', f'{filename}.png')
                os.makedirs(os.path.dirname(filepath), exist_ok=True)
                img.save(filepath)
                
                print(f'模板已保存: {filepath}')
                break
            else:
                print('请先记录左上角和右下角坐标')
                time.sleep(0.5)  # 防止重复触发
        elif keyboard.is_pressed('esc'):
            print('退出')
            break
        
        time.sleep(0.1)
    except KeyboardInterrupt:
        print('\n退出')
        break
    except Exception as e:
        print(f'错误: {e}')
        break
"

echo.
echo 模板创建完成
echo.
pause