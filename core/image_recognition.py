#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import cv2
import numpy as np
from loguru import logger


class ImageRecognition:
    """图像识别模块，负责处理图像识别和模板匹配"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.threshold = self.config.get("threshold", 0.8)
        self.method = self.config.get("method", "cv2.TM_CCOEFF_NORMED")
        template_dir = self.config.get("template_dir", "assets/templates")
        
        # 获取项目根目录的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # 使用绝对路径
        self.template_dir = os.path.join(project_root, template_dir)
        
        # 确保模板目录存在
        os.makedirs(self.template_dir, exist_ok=True)
        
        # 缓存已加载的模板
        self.template_cache = {}
    
    def load_template(self, template_name):
        """加载模板图像"""
        # 检查缓存
        if template_name in self.template_cache:
            return self.template_cache[template_name]
        
        # 构建模板路径
        template_path = os.path.join(self.template_dir, template_name)
        
        # 如果没有扩展名，尝试添加.png
        if not os.path.splitext(template_name)[1]:
            template_path = os.path.join(self.template_dir, template_name + ".png")
        
        try:
            # 读取模板图像
            template = cv2.imread(template_path)
            if template is None:
                logger.error(f"无法加载模板图像: {template_path}")
                return None
            
            # 转换为灰度图像
            template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
            
            # 缓存模板
            self.template_cache[template_name] = template_gray
            
            return template_gray
        except Exception as e:
            logger.error(f"加载模板图像失败: {e}")
            return None
    
    def find_template(self, screenshot, template_name, threshold=None):
        """在截图中查找模板"""
        # 使用指定阈值或默认阈值
        match_threshold = threshold if threshold is not None else self.threshold
        
        # 加载模板
        template = self.load_template(template_name)
        if template is None:
            return None
        
        try:
            # 转换截图为灰度图像
            if len(screenshot.shape) == 3:
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            else:
                screenshot_gray = screenshot
            
            # 获取模板尺寸
            template_h, template_w = template.shape
            
            # 执行模板匹配
            result = cv2.matchTemplate(screenshot_gray, template, eval(self.method))
            
            # 查找最佳匹配位置
            min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
            
            # 根据匹配方法确定匹配位置
            if eval(self.method) in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
                match_location = min_loc
                match_value = 1 - min_val  # 转换为相似度
            else:
                match_location = max_loc
                match_value = max_val
            
            # 检查匹配度是否达到阈值
            if match_value >= match_threshold:
                # 计算匹配区域的中心点
                center_x = match_location[0] + template_w // 2
                center_y = match_location[1] + template_h // 2
                
                return {
                    "found": True,
                    "position": (center_x, center_y),
                    "top_left": match_location,
                    "bottom_right": (match_location[0] + template_w, match_location[1] + template_h),
                    "confidence": match_value,
                    "template_name": template_name
                }
            else:
                return {
                    "found": False,
                    "confidence": match_value,
                    "template_name": template_name
                }
        except Exception as e:
            logger.error(f"模板匹配失败: {e}")
            return None
    
    def find_all_templates(self, screenshot, template_name, threshold=None):
        """在截图中查找所有匹配的模板"""
        # 使用指定阈值或默认阈值
        match_threshold = threshold if threshold is not None else self.threshold
        
        # 加载模板
        template = self.load_template(template_name)
        if template is None:
            return []
        
        try:
            # 转换截图为灰度图像
            if len(screenshot.shape) == 3:
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            else:
                screenshot_gray = screenshot
            
            # 获取模板尺寸
            template_h, template_w = template.shape
            
            # 执行模板匹配
            result = cv2.matchTemplate(screenshot_gray, template, eval(self.method))
            
            # 查找所有匹配位置
            locations = np.where(result >= match_threshold)
            
            matches = []
            for pt in zip(*locations[::-1]):  # 切换x和y坐标
                # 计算匹配区域的中心点
                center_x = pt[0] + template_w // 2
                center_y = pt[1] + template_h // 2
                
                # 获取匹配度
                match_value = result[pt[1], pt[0]]
                
                matches.append({
                    "found": True,
                    "position": (center_x, center_y),
                    "top_left": pt,
                    "bottom_right": (pt[0] + template_w, pt[1] + template_h),
                    "confidence": match_value,
                    "template_name": template_name
                })
            
            return matches
        except Exception as e:
            logger.error(f"多模板匹配失败: {e}")
            return []
    
    def clear_cache(self):
        """清空模板缓存"""
        self.template_cache.clear()
        logger.info("模板缓存已清空")
    
    def save_screenshot_region(self, screenshot, region, filename):
        """保存截图区域作为模板"""
        try:
            x1, y1, x2, y2 = region
            region_img = screenshot[y1:y2, x1:x2]
            
            # 确保目录存在
            os.makedirs(self.template_dir, exist_ok=True)
            
            # 保存图像
            template_path = os.path.join(self.template_dir, filename)
            cv2.imwrite(template_path, region_img)
            
            logger.info(f"模板已保存: {template_path}")
            return True
        except Exception as e:
            logger.error(f"保存模板失败: {e}")
            return False