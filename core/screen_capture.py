#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import numpy as np
import mss
import mss.tools
from PIL import Image
import cv2
from loguru import logger


class ScreenCapture:
    """屏幕捕获模块，负责高效地捕获屏幕内容"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.region = self.config.get("region", None)
        self.resolution = self.config.get("resolution", [1920, 1080])
        self.use_delay = self.config.get("use_delay", True)  # 是否使用延迟，默认使用
        self.delay = self.config.get("delay", 0.01)  # 默认延迟0.01秒
        
        # 初始化mss对象
        self.sct = mss.mss()
        
        # 设置捕获区域
        self._setup_capture_region()
        
        logger.info(f"屏幕捕获初始化完成，捕获区域: {self.monitor}")
    
    def _setup_capture_region(self):
        """设置捕获区域"""
        if self.region is None:
            # 全屏捕获
            self.monitor = self.sct.monitors[0]  # 主显示器
        else:
            # 指定区域捕获
            x1, y1, x2, y2 = self.region
            self.monitor = {
                "top": y1,
                "left": x1,
                "width": x2 - x1,
                "height": y2 - y1
            }
    
    def capture(self, as_numpy=True):
        """捕获屏幕"""
        try:
            # 使用mss捕获屏幕
            screenshot = self.sct.grab(self.monitor)
            
            if as_numpy:
                # 转换为numpy数组
                img = np.array(screenshot)
                # mss返回的是BGRA格式，转换为BGR
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                
                # 根据配置添加延迟
                if self.use_delay:
                    time.sleep(self.delay)
                
                return img
            else:
                # 返回PIL图像
                pil_img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                
                # 根据配置添加延迟
                if self.use_delay:
                    time.sleep(self.delay)
                
                return pil_img
        except Exception as e:
            logger.error(f"屏幕捕获失败: {e}")
            return None
    
    def capture_region(self, x1, y1, x2, y2, as_numpy=True):
        """捕获指定区域"""
        try:
            # 设置临时区域
            temp_monitor = {
                "top": y1,
                "left": x1,
                "width": x2 - x1,
                "height": y2 - y1
            }
            
            # 使用mss捕获指定区域
            screenshot = self.sct.grab(temp_monitor)
            
            if as_numpy:
                # 转换为numpy数组
                img = np.array(screenshot)
                # mss返回的是BGRA格式，转换为BGR
                img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
                return img
            else:
                # 返回PIL图像
                return Image.frombytes("RGB", screenshot.size, screenshot.rgb)
        except Exception as e:
            logger.error(f"区域捕获失败: {e}")
            return None
    
    def save_screenshot(self, filename, region=None):
        """保存截图"""
        try:
            if region is None:
                # 捕获默认区域
                screenshot = self.capture(as_numpy=False)
            else:
                # 捕获指定区域
                x1, y1, x2, y2 = region
                screenshot = self.capture_region(x1, y1, x2, y2, as_numpy=False)
            
            if screenshot is not None:
                screenshot.save(filename)
                logger.info(f"截图已保存: {filename}")
                return True
            else:
                logger.error("截图失败")
                return False
        except Exception as e:
            logger.error(f"保存截图失败: {e}")
            return False
    
    def get_screen_size(self):
        """获取屏幕尺寸"""
        try:
            monitor = self.sct.monitors[0]  # 主显示器
            return (monitor["width"], monitor["height"])
        except Exception as e:
            logger.error(f"获取屏幕尺寸失败: {e}")
            return None
    
    def set_capture_region(self, region):
        """设置捕获区域"""
        try:
            self.region = region
            self._setup_capture_region()
            logger.info(f"捕获区域已更新: {self.monitor}")
            return True
        except Exception as e:
            logger.error(f"设置捕获区域失败: {e}")
            return False
    
    def reset_capture_region(self):
        """重置为全屏捕获"""
        try:
            self.region = None
            self._setup_capture_region()
            logger.info(f"捕获区域已重置为全屏: {self.monitor}")
            return True
        except Exception as e:
            logger.error(f"重置捕获区域失败: {e}")
            return False
    
    def capture_and_process(self, process_func, *args, **kwargs):
        """捕获屏幕并处理"""
        try:
            # 捕获屏幕
            screenshot = self.capture()
            
            if screenshot is not None:
                # 处理图像
                result = process_func(screenshot, *args, **kwargs)
                return result
            else:
                logger.error("屏幕捕获失败，无法处理")
                return None
        except Exception as e:
            logger.error(f"捕获并处理失败: {e}")
            return None
    
    def continuous_capture(self, callback, interval=0.1, max_iterations=None):
        """连续捕获屏幕并调用回调函数"""
        try:
            iteration = 0
            while max_iterations is None or iteration < max_iterations:
                # 捕获屏幕
                screenshot = self.capture()
                
                if screenshot is not None:
                    # 调用回调函数
                    callback(screenshot)
                
                # 等待指定间隔
                time.sleep(interval)
                iteration += 1
            
            logger.info(f"连续捕获完成，共迭代 {iteration} 次")
            return True
        except KeyboardInterrupt:
            logger.info("连续捕获被中断")
            return True
        except Exception as e:
            logger.error(f"连续捕获失败: {e}")
            return False
    
    def __del__(self):
        """析构函数，释放资源"""
        try:
            if hasattr(self, 'sct'):
                self.sct.close()
        except Exception as e:
            logger.error(f"释放屏幕捕获资源失败: {e}")