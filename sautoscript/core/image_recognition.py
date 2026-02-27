#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from loguru import logger
from queue import Queue
import threading
from typing import Optional, Tuple, List, Dict, Any


class NumpyArrayPool:
    """numpy数组对象池，用于减少内存分配和释放的开销"""
    
    def __init__(self, max_size=50):
        self.max_size = max_size
        self.pools = {}  # 按形状分组的对象池
        self.lock = threading.Lock()
        # 预分配一些常用大小的数组以提高性能
        self._preallocate_common_arrays()
    
    def _preallocate_common_arrays(self):
        """预分配一些常用大小的数组"""
        common_shapes = [
            ((1000, 1000), np.uint8),
            ((500, 500), np.uint8),
            ((200, 200), np.uint8),
            ((1000, 1000), np.float32),
            ((500, 500), np.float32),
        ]
        
        for shape, dtype in common_shapes:
            key = (shape, dtype)
            if key not in self.pools:
                self.pools[key] = Queue(maxsize=self.max_size)
            
            # 预分配几个数组
            for _ in range(min(5, self.max_size)):
                array = np.zeros(shape, dtype=dtype)
                try:
                    self.pools[key].put_nowait(array)
                except:
                    break
    
    def get_array(self, shape, dtype=np.uint8):
        """从池中获取指定形状和类型的数组"""
        key = (shape, dtype)
        
        # 首先尝试无锁获取
        if key in self.pools:
            try:
                return self.pools[key].get_nowait()
            except:
                pass
        
        # 如果无锁获取失败，尝试加锁获取
        with self.lock:
            # 再次检查，因为可能在获取锁的过程中其他线程已经创建了池
            if key not in self.pools:
                self.pools[key] = Queue(maxsize=self.max_size)
            
            try:
                return self.pools[key].get_nowait()
            except:
                # 池中没有可用数组，创建新的
                return np.zeros(shape, dtype=dtype)
    
    def return_array(self, array):
        """将数组返回池中"""
        if array is None:
            return
        
        shape = array.shape
        dtype = array.dtype
        key = (shape, dtype)
        
        with self.lock:
            if key in self.pools:
                try:
                    # 重置数组内容
                    array.fill(0)
                    self.pools[key].put_nowait(array)
                except:
                    # 池已满，丢弃数组
                    pass


class ImageRecognition:
    """图像识别模块，用于模板匹配和图像处理"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.template_dir = self.config.get("template_dir", "assets/templates")
        self.default_threshold = self.config.get("default_threshold", 0.8)
        
        # 确保模板目录存在
        os.makedirs(self.template_dir, exist_ok=True)
        
        # 初始化numpy数组池
        self.array_pool = NumpyArrayPool()
        
        logger.info(f"图像识别模块初始化完成，模板目录: {self.template_dir}")
    
    def load_template(self, template_name):
        """加载模板图像
        
        Args:
            template_name: 模板名称
            
        Returns:
            numpy.ndarray: 模板图像
        """
        template_path = os.path.join(self.template_dir, template_name)
        
        # 如果没有扩展名，尝试添加常见的图像扩展名
        if not os.path.isfile(template_path):
            for ext in [".png", ".jpg", ".jpeg", ".bmp"]:
                temp_path = template_path + ext
                if os.path.isfile(temp_path):
                    template_path = temp_path
                    break
        
        try:
            template = cv2.imread(template_path, cv2.IMREAD_COLOR)
            if template is None:
                logger.error(f"加载模板失败: {template_path}")
                return None
            
            logger.debug(f"模板加载成功: {template_path}")
            return template
        except Exception as e:
            logger.error(f"加载模板时发生错误: {e}")
            return None
    
    def match_template(self, image, template, threshold=None):
        """模板匹配
        
        Args:
            image: 待匹配的图像
            template: 模板图像
            threshold: 匹配阈值
            
        Returns:
            dict: 匹配结果
        """
        if image is None or template is None:
            logger.error("图像或模板为空")
            return {"found": False}
        
        if threshold is None:
            threshold = self.default_threshold
        
        try:
            # 转换为numpy数组
            if hasattr(image, "numpy"):
                img_np = image.numpy()
            else:
                img_np = np.array(image)
            
            # 转换为BGR格式
            if len(img_np.shape) == 3 and img_np.shape[2] == 3:
                img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            else:
                img_gray = img_np
            
            # 转换模板为灰度图
            if len(template.shape) == 3 and template.shape[2] == 3:
                template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            else:
                template_gray = template
            
            # 获取模板大小
            template_height, template_width = template_gray.shape[:2]
            
            # 确保图像大于模板
            if img_gray.shape[0] < template_height or img_gray.shape[1] < template_width:
                logger.warning("图像大小小于模板大小")
                return {"found": False}
            
            # 执行模板匹配
            result = cv2.matchTemplate(img_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            
            # 查找最大值和位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            if max_val >= threshold:
                # 计算中心点
                center_x = max_loc[0] + template_width // 2
                center_y = max_loc[1] + template_height // 2
                
                logger.debug(f"模板匹配成功，相似度: {max_val:.2f}，位置: ({center_x}, {center_y})")
                return {
                    "found": True,
                    "position": (center_x, center_y),
                    "confidence": max_val,
                    "rectangle": (
                        max_loc[0],
                        max_loc[1],
                        max_loc[0] + template_width,
                        max_loc[1] + template_height
                    )
                }
            else:
                logger.debug(f"模板匹配失败，最高相似度: {max_val:.2f} < {threshold}")
                return {"found": False}
        except Exception as e:
            logger.error(f"模板匹配时发生错误: {e}")
            return {"found": False}
    
    def find_template(self, image, template_name, threshold=None):
        """查找模板
        
        Args:
            image: 待匹配的图像
            template_name: 模板名称
            threshold: 匹配阈值
            
        Returns:
            dict: 匹配结果
        """
        template = self.load_template(template_name)
        if template is None:
            return {"found": False}
        
        return self.match_template(image, template, threshold)
    
    def save_screenshot_region(self, screenshot, region, filename):
        """保存截图的指定区域为模板
        
        Args:
            screenshot: 截图
            region: 区域 (x, y, width, height)
            filename: 保存的文件名
            
        Returns:
            bool: 是否成功保存
        """
        try:
            # 确保模板目录存在
            os.makedirs(self.template_dir, exist_ok=True)
            
            # 提取区域
            x, y, width, height = region
            region_image = screenshot.crop((x, y, x + width, y + height))
            
            # 保存图像
            save_path = os.path.join(self.template_dir, filename)
            region_image.save(save_path)
            
            logger.info(f"模板已保存到: {save_path}")
            return True
        except Exception as e:
            logger.error(f"保存模板失败: {e}")
            return False
    
    def preprocess_image(self, image):
        """预处理图像以提高识别效果
        
        Args:
            image: 输入图像
            
        Returns:
            numpy.ndarray: 预处理后的图像
        """
        try:
            # 转换为numpy数组
            if hasattr(image, "numpy"):
                img_np = image.numpy()
            else:
                img_np = np.array(image)
            
            # 转换为灰度图
            if len(img_np.shape) == 3 and img_np.shape[2] == 3:
                img_gray = cv2.cvtColor(img_np, cv2.COLOR_RGB2GRAY)
            else:
                img_gray = img_np
            
            # 应用高斯模糊
            blurred = cv2.GaussianBlur(img_gray, (5, 5), 0)
            
            # 应用自适应阈值
            thresh = cv2.adaptiveThreshold(
                blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                cv2.THRESH_BINARY, 11, 2
            )
            
            return thresh
        except Exception as e:
            logger.error(f"图像预处理失败: {e}")
            return None
