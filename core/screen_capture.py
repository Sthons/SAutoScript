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
        
        # 质量设置
        self.quality = self.config.get("quality", "medium")  # 默认中等质量
        self._setup_quality_settings()
        
        # 初始化mss对象
        self.sct = mss.mss()
        
        # 设置捕获区域
        self._setup_capture_region()
        
        logger.info(f"屏幕捕获初始化完成，捕获区域: {self.monitor}, 质量设置: {self.quality}")
    
    def _setup_quality_settings(self):
        """根据质量设置调整参数"""
        if self.quality == "low":
            # 低质量：降低分辨率，增加延迟
            self.scale_factor = 0.5  # 缩放到50%
            self.jpeg_quality = 60  # JPEG压缩质量
            self.processing_delay = 0.02  # 处理延迟
        elif self.quality == "high":
            # 高质量：原始分辨率，最小延迟
            self.scale_factor = 1.0  # 原始分辨率
            self.jpeg_quality = 95  # 高质量JPEG
            self.processing_delay = 0.005  # 最小延迟
        else:  # medium
            # 中等质量：平衡设置
            self.scale_factor = 0.75  # 缩放到75%
            self.jpeg_quality = 80  # 中等JPEG质量
            self.processing_delay = 0.01  # 标准延迟
    
    def _setup_capture_region(self):
        """设置捕获区域"""
        if self.region is None:
            # 全屏捕获
            self.monitor = self.sct.monitors[self.sct_monitor]  # 显示器
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
                
                # 根据质量设置调整分辨率
                if self.scale_factor != 1.0:
                    new_width = int(img.shape[1] * self.scale_factor)
                    new_height = int(img.shape[0] * self.scale_factor)
                    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
                
                # 根据配置添加延迟
                if self.use_delay:
                    time.sleep(self.delay)
                
                return img
            else:
                # 返回PIL图像
                pil_img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                
                # 根据质量设置调整分辨率
                if self.scale_factor != 1.0:
                    new_width = int(pil_img.width * self.scale_factor)
                    new_height = int(pil_img.height * self.scale_factor)
                    pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
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
                
                # 根据质量设置调整分辨率
                if self.scale_factor != 1.0:
                    new_width = int(img.shape[1] * self.scale_factor)
                    new_height = int(img.shape[0] * self.scale_factor)
                    img = cv2.resize(img, (new_width, new_height), interpolation=cv2.INTER_AREA)
                
                return img
            else:
                # 返回PIL图像
                pil_img = Image.frombytes("RGB", screenshot.size, screenshot.rgb)
                
                # 根据质量设置调整分辨率
                if self.scale_factor != 1.0:
                    new_width = int(pil_img.width * self.scale_factor)
                    new_height = int(pil_img.height * self.scale_factor)
                    pil_img = pil_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                
                return pil_img
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
                # 根据文件扩展名决定保存格式和质量
                if filename.lower().endswith(('.jpg', '.jpeg')):
                    # 使用JPEG质量和优化
                    screenshot.save(filename, 'JPEG', quality=self.jpeg_quality, optimize=True)
                elif filename.lower().endswith('.png'):
                    # PNG格式使用最佳压缩
                    screenshot.save(filename, 'PNG', optimize=True)
                else:
                    # 其他格式使用默认设置
                    screenshot.save(filename)
                
                logger.info(f"截图已保存: {filename}, 质量设置: {self.quality}")
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
    
    def continuous_capture(self, callback, interval=None, max_iterations=None):
        """连续捕获屏幕并调用回调函数"""
        try:
            iteration = 0
            # 如果没有指定interval，使用质量设置中的处理延迟
            capture_interval = interval if interval is not None else self.processing_delay
            
            while max_iterations is None or iteration < max_iterations:
                # 捕获屏幕
                screenshot = self.capture()
                
                if screenshot is not None:
                    # 调用回调函数
                    callback(screenshot)
                
                # 等待指定间隔
                time.sleep(capture_interval)
                iteration += 1
            
            logger.info(f"连续捕获完成，共迭代 {iteration} 次，使用间隔: {capture_interval}秒")
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