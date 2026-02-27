#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import ctypes
import warnings
import win32api
import win32con
import win32gui
import pyautogui
import pydirectinput
from loguru import logger
from PIL import ImageGrab

class InputController:
    """输入控制模块，负责处理鼠标和键盘的仿真输入"""

    def __init__(self, config=None):
        self.config = config or {}
        self.delay = self.config.get("delay", 0.1)
        self.overlimit_detection = self.config.get(
            "overlimit_detection", False
        )  # 是否开启超量识别检测
        self.use_delay = self.config.get("use_delay", True)  # 是否使用延迟，默认使用
        self.move_duration = self.config.get("move_duration", 0.2)
        self.click_duration = self.config.get("click_duration", 0.1)
        self.key_duration = self.config.get("key_duration", 0.05)

        # 禁用pyautogui的安全机制
        pyautogui.FAILSAFE = False

        # 获取屏幕尺寸
        screen = self.get_screen_shot()
        self.screen_width, self.screen_height = screen.width, screen.height

        logger.info(
            f"输入控制器初始化完成，屏幕尺寸: {self.screen_width}x{self.screen_height}"
        )

    def get_screen_size(self):
        """获取屏幕尺寸"""
        warnings.warn(
            "考虑到 pyautogui 官方文档明确表明不适用于多显示器设置，该方法已废弃",
            DeprecationWarning,
        )
        return pyautogui.size()

    def get_screen_shot(self):
        """获取屏幕截图"""
        screen = ImageGrab.grab(all_screens=True)
        return screen

    def set_mouse_position(self, x, y, delay=None, duration=None):
        """设置鼠标位置"""
        try:
            # 使用指定延迟或默认值
            move_delay = delay if delay is not None else self.delay

            # 使用指定持续时间或默认值
            move_time = duration if duration is not None else self.move_duration

            # 确保坐标在屏幕范围内
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))

            pyautogui.moveTo(x, y, duration=move_time)

            if self.use_delay:
                time.sleep(move_delay)
            logger.debug(f"鼠标移动到: ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"鼠标移动失败: {e}")
            return False

    def move_mouse(self, x, y, duration=None):
        """移动鼠标到指定位置"""
        try:
            # 确保坐标在屏幕范围内
            x = max(0, min(x, self.screen_width - 1))
            y = max(0, min(y, self.screen_height - 1))

            # 使用指定持续时间或默认值
            move_time = duration if duration is not None else self.move_duration

            # 使用PyDirectInput移动鼠标
            pydirectinput.moveTo(x, y, duration=move_time)

            # 根据配置添加延迟
            if self.use_delay:
                time.sleep(self.delay)

            logger.debug(f"鼠标移动到: ({x}, {y})")
            return True
        except Exception as e:
            logger.error(f"鼠标移动失败: {e}")
            return False

    def click(
        self, x=None, y=None, button="left", clicks=1, interval=0.2, duration=0.2
    ):
        """点击鼠标"""
        try:
            # 如果指定了位置，先移动鼠标
            if x is not None and y is not None:
                self.move_mouse(x, y)

            # 执行点击
            if button == "left":
                pydirectinput.click(clicks=clicks, interval=interval)
            elif button == "right":
                pydirectinput.rightClick(interval=interval)
            elif button == "middle":
                pydirectinput.middleClick(interval=interval)
            else:
                logger.error(f"不支持的鼠标按钮: {button}")
                return False

            # 根据配置添加延迟
            if self.use_delay:
                time.sleep(self.delay)

            logger.debug(f"鼠标{button}键点击: {clicks}次")
            return True
        except Exception as e:
            logger.error(f"鼠标点击失败: {e}")
            return False

    def mouse_down(self, button="left"):
        """按下鼠标按钮"""
        try:
            if button == "left":
                pydirectinput.mouseDown(button="left")
            elif button == "right":
                pydirectinput.mouseDown(button="right")
            elif button == "middle":
                pydirectinput.mouseDown(button="middle")
            else:
                logger.error(f"不支持的鼠标按钮: {button}")
                return False

            logger.debug(f"鼠标{button}键按下")
            return True
        except Exception as e:
            logger.error(f"鼠标按下失败: {e}")
            return False

    def mouse_up(self, button="left"):
        """释放鼠标按钮"""
        try:
            if button == "left":
                pydirectinput.mouseUp(button="left")
            elif button == "right":
                pydirectinput.mouseUp(button="right")
            elif button == "middle":
                pydirectinput.mouseUp(button="middle")
            else:
                logger.error(f"不支持的鼠标按钮: {button}")
                return False

            logger.debug(f"鼠标{button}键释放")
            return True
        except Exception as e:
            logger.error(f"鼠标释放失败: {e}")
            return False

    def drag(self, start_x, start_y, end_x, end_y, duration=None):
        """拖动鼠标"""
        try:
            # 确保坐标在屏幕范围内
            start_x = max(0, min(start_x, self.screen_width - 1))
            start_y = max(0, min(start_y, self.screen_height - 1))
            end_x = max(0, min(end_x, self.screen_width - 1))
            end_y = max(0, min(end_y, self.screen_height - 1))

            # 使用指定持续时间或默认值
            drag_time = duration if duration is not None else self.move_duration

            # 使用PyDirectInput拖动
            pydirectinput.drag(end_x - start_x, end_y - start_y, duration=drag_time)

            # 根据配置添加延迟
            if self.use_delay:
                time.sleep(self.delay)

            logger.debug(f"鼠标拖动: ({start_x}, {start_y}) -> ({end_x}, {end_y})")
            return True
        except Exception as e:
            logger.error(f"鼠标拖动失败: {e}")
            return False

    def scroll(self, x=None, y=None, clicks=1, direction="down"):
        """滚动鼠标滚轮"""
        try:
            # 如果指定了位置，先移动鼠标
            if x is not None and y is not None:
                self.move_mouse(x, y)

            # 执行滚动（使用pyautogui.scroll，因为pydirectinput没有scroll方法）
            scroll_amount = clicks if direction == "down" else -clicks
            pyautogui.scroll(scroll_amount)

            # 根据配置添加延迟
            if self.use_delay:
                time.sleep(self.delay)

            logger.debug(f"鼠标滚轮: {direction} {clicks}次")
            return True
        except Exception as e:
            logger.error(f"鼠标滚轮失败: {e}")
            return False

    def key_press(self, key, presses=1, interval=0.1):
        """按下键盘按键"""
        try:
            pydirectinput.press(key, presses=presses, interval=interval)

            # 根据配置添加延迟
            if self.use_delay:
                time.sleep(self.delay)

            logger.debug(f"键盘按键: {key} (按{presses}次)")
            return True
        except Exception as e:
            logger.error(f"键盘按键失败: {e}")
            return False

    def key_down(self, key):
        """按下按键不释放"""
        try:
            pydirectinput.keyDown(key)

            logger.debug(f"按键按下: {key}")
            return True
        except Exception as e:
            logger.error(f"按键按下失败: {e}")
            return False

    def key_up(self, key):
        """释放按键"""
        try:
            pydirectinput.keyUp(key)

            logger.debug(f"按键释放: {key}")
            return True
        except Exception as e:
            logger.error(f"按键释放失败: {e}")
            return False

    def hotkey(self, *keys, interval=0.1):
        """按下组合键"""
        try:
            # 按下所有按键
            for key in keys:
                pydirectinput.keyDown(key)
                time.sleep(interval)

            # 释放所有按键（反向顺序）
            for key in reversed(keys):
                pydirectinput.keyUp(key)
                time.sleep(interval)

            # 根据配置添加延迟
            if self.use_delay:
                time.sleep(self.delay)

            logger.debug(f"组合键: {'+'.join(keys)}")
            return True
        except Exception as e:
            logger.error(f"组合键失败: {e}")
            return False

    def typewrite(self, text, interval=0.05):
        """输入文本"""
        try:
            pydirectinput.write(text, interval=interval)

            # 根据配置添加延迟
            if self.use_delay:
                time.sleep(self.delay)

            logger.debug(f"输入文本: {text}")
            return True
        except Exception as e:
            logger.error(f"输入文本失败: {e}")
            return False

    def get_mouse_position(self):
        """获取当前鼠标位置"""
        try:
            x, y = pydirectinput.position()
            logger.debug(f"当前鼠标位置: ({x}, {y})")
            return x, y
        except Exception as e:
            logger.error(f"获取鼠标位置失败: {e}")
            return None, None

    def is_key_pressed(self, key):
        """检查按键是否被按下"""
        try:
            return pydirectinput.is_pressed(key)
        except Exception as e:
            logger.error(f"检查按键状态失败: {e}")
            return False

    def get_active_window(self):
        """获取当前活动窗口信息"""
        try:
            window_handle = win32gui.GetForegroundWindow()
            window_title = win32gui.GetWindowText(window_handle)
            window_class = win32gui.GetClassName(window_handle)

            return {
                "handle": window_handle,
                "title": window_title,
                "class": window_class,
            }
        except Exception as e:
            logger.error(f"获取活动窗口信息失败: {e}")
            return None

    def set_window_foreground(self, window_title=None, window_handle=None):
        """将指定窗口设置为前台窗口"""
        try:
            if window_handle is None and window_title is not None:
                # 通过标题查找窗口句柄
                window_handle = win32gui.FindWindow(None, window_title)
                if window_handle == 0:
                    logger.error(f"未找到窗口: {window_title}")
                    return False

            if window_handle is not None:
                # 检查窗口是否最小化
                if win32gui.IsIconic(window_handle):
                    win32gui.ShowWindow(window_handle, win32con.SW_RESTORE)

                # 设置为前台窗口
                win32gui.SetForegroundWindow(window_handle)

                logger.debug(f"窗口已设置为前台: {window_title or window_handle}")
                return True
            else:
                logger.error("未指定窗口标题或句柄")
                return False
        except Exception as e:
            logger.error(f"设置前台窗口失败: {e}")
            return False
