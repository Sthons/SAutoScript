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
        self.sct_monitor = self.config.get("monitor", 0)  # 主显示器
        self.resolution = self.config.get("resolution", [1920, 1080])
        self.use_delay = self.config.get("use_delay", True)  # 是否使用延迟，默认使用
        self.delay = self.config.get("capture_delay", 0.01)  # 默认延迟0.01秒
        
        # 截图方法配置
        self.capture_method = self.config.get("capture_method", "mss")  # 默认使用mss
        
        # 质量设置
        self.quality = self.config.get("quality", "medium")  # 默认中等质量
        self._setup_quality_settings()
        
        # 根据截图方法初始化相应的对象
        self._init_capture_method()
        
        # 设置捕获区域
        self._setup_capture_region()
        
        logger.info(f"屏幕捕获初始化完成，捕获方法: {self.capture_method}，捕获区域: {self.monitor}，质量设置: {self.quality}")
    
    def _init_capture_method(self):
        """根据配置的截图方法初始化相应的对象"""
        if self.capture_method == "mss":
            self.sct = mss.mss()
            logger.info("使用mss库进行屏幕捕获")
        elif self.capture_method == "pil":
            # PIL方式不需要特殊初始化
            logger.info("使用PIL库进行屏幕捕获")
        elif self.capture_method == "pyautogui":
            import pyautogui
            # 禁用pyautogui的安全检查
            pyautogui.FAILSAFE = False
            logger.info("使用pyautogui库进行屏幕捕获")
        else:
            # 默认使用mss
            self.capture_method = "mss"
            self.sct = mss.mss()
            logger.warning(f"不支持的捕获方法: {self.capture_method}，已切换到mss")
    
    def _setup_quality_settings(self):
        """根据质量设置配置相应的参数"""
        if self.quality == "low":
            self.resize_factor = 0.5  # 缩小一半
            self.jpeg_quality = 70
        elif self.quality == "high":
            self.resize_factor = 1.0  # 原始大小
            self.jpeg_quality = 95
        else:  # medium
            self.resize_factor = 0.75  # 缩小到75%
            self.jpeg_quality = 85
    
    def _setup_capture_region(self):
        """设置捕获区域"""
        if self.capture_method == "mss":
            # 获取所有显示器信息
            monitors = self.sct.monitors
            
            # 确保监控器索引有效
            if 0 <= self.sct_monitor < len(monitors):
                self.monitor = monitors[self.sct_monitor]
            else:
                # 默认使用主显示器
                self.monitor = monitors[0]
                logger.warning(f"无效的显示器索引: {self.sct_monitor}，已切换到主显示器")
            
            # 如果指定了区域，则覆盖默认区域
            if self.region:
                self.monitor = {
                    "top": self.region[1],
                    "left": self.region[0],
                    "width": self.region[2],
                    "height": self.region[3]
                }
    
    def capture(self):
        """捕获屏幕内容
        
        Returns:
            PIL.Image: 屏幕截图
        """
        try:
            if self.use_delay:
                time.sleep(self.delay)
            
            if self.capture_method == "mss":
                # 使用mss捕获屏幕
                sct_img = self.sct.grab(self.monitor)
                # 转换为PIL图像
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            elif self.capture_method == "pil":
                # 使用PIL捕获屏幕
                from PIL import ImageGrab
                if self.region:
                    img = ImageGrab.grab(bbox=(self.region[0], self.region[1], 
                                             self.region[0] + self.region[2], 
                                             self.region[1] + self.region[3]))
                else:
                    img = ImageGrab.grab()
            elif self.capture_method == "pyautogui":
                # 使用pyautogui捕获屏幕
                import pyautogui
                if self.region:
                    img = pyautogui.screenshot(region=(self.region[0], self.region[1], 
                                                     self.region[2], self.region[3]))
                else:
                    img = pyautogui.screenshot()
            else:
                # 默认使用mss
                sct_img = self.sct.grab(self.monitor)
                img = Image.frombytes("RGB", sct_img.size, sct_img.bgra, "raw", "BGRX")
            
            # 根据质量设置调整图像大小
            if self.resize_factor != 1.0:
                new_width = int(img.width * self.resize_factor)
                new_height = int(img.height * self.resize_factor)
                img = img.resize((new_width, new_height), Image.LANCZOS)
            
            logger.debug(f"屏幕捕获成功，大小: {img.width}x{img.height}")
            return img
        except Exception as e:
            logger.error(f"屏幕捕获失败: {e}")
            return None
    
    def capture_numpy(self):
        """捕获屏幕内容并返回numpy数组
        
        Returns:
            numpy.ndarray: 屏幕截图的numpy数组
        """
        img = self.capture()
        if img is not None:
            # 转换为numpy数组
            img_np = np.array(img)
            # 转换为BGR格式（OpenCV使用）
            img_np = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
            return img_np
        return None
    
    def capture_to_file(self, filename):
        """捕获屏幕并保存到文件
        
        Args:
            filename: 保存的文件名
        
        Returns:
            bool: 是否成功保存
        """
        img = self.capture()
        if img is not None:
            try:
                img.save(filename, quality=self.jpeg_quality)
                logger.info(f"屏幕截图已保存到: {filename}")
                return True
            except Exception as e:
                logger.error(f"保存屏幕截图失败: {e}")
                return False
        return False
