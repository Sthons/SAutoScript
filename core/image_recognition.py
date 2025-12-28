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
        if key in self.pools and not self.pools[key].empty():
            try:
                array = self.pools[key].get_nowait()
                # 重置数组内容
                array.fill(0)
                return array
            except:
                pass
        
        # 如果无锁获取失败，尝试加锁获取
        with self.lock:
            if key in self.pools and not self.pools[key].empty():
                array = self.pools[key].get()
                array.fill(0)
                return array
        
        # 池中没有可用数组，创建新的
        return np.zeros(shape, dtype=dtype)
    
    def return_array(self, array):
        """将数组返回到池中"""
        key = (array.shape, array.dtype)
        
        # 快速路径：如果池未满，尝试无锁归还
        if key in self.pools and self.pools[key].qsize() < self.max_size:
            try:
                self.pools[key].put_nowait(array)
                return
            except:
                pass
        
        # 慢速路径：需要加锁处理
        with self.lock:
            if key not in self.pools:
                self.pools[key] = Queue(maxsize=self.max_size)
            
            # 如果池未满，则将数组放回池中
            if self.pools[key].qsize() < self.max_size:
                try:
                    self.pools[key].put_nowait(array)
                except:
                    # 池已满，直接丢弃
                    pass
    
    def clear_pool(self):
        """清空所有对象池"""
        with self.lock:
            self.pools.clear()
        
    def get_pool_stats(self):
        """获取池的统计信息"""
        with self.lock:
            stats = {}
            for key, queue in self.pools.items():
                stats[key] = queue.qsize()
            return stats


class ImageRecognition:
    """图像识别模块，负责处理图像识别和模板匹配，使用对象池优化性能"""
    
    def __init__(self, config=None):
        self.config = config or {}
        self.threshold = self.config.get("threshold", 0.8)
        # 将字符串方法名转换为OpenCV整数常量
        method_str = self.config.get("method", "cv2.TM_CCOEFF_NORMED")
        self.method = getattr(cv2, method_str.split('.')[-1]) if '.' in method_str else eval(method_str)
        template_dir = self.config.get("template_dir", "assets/templates")
        
        # 对象池配置
        pool_config = self.config.get("object_pool", {})
        self.max_pool_size = pool_config.get("max_size", 50)
        self.enable_object_pool = pool_config.get("enabled", True)
        
        # 初始化对象池
        if self.enable_object_pool:
            self.array_pool = NumpyArrayPool(max_size=self.max_pool_size)
            logger.info(f"图像识别对象池已启用，最大池大小: {self.max_pool_size}")
        else:
            self.array_pool = None
            logger.info("图像识别对象池已禁用")
        
        # 获取项目根目录的绝对路径
        current_dir = os.path.dirname(os.path.abspath(__file__))
        project_root = os.path.dirname(current_dir)
        
        # 使用绝对路径
        self.template_dir = os.path.join(project_root, template_dir)
        
        # 确保模板目录存在
        os.makedirs(self.template_dir, exist_ok=True)
        
        # 缓存已加载的模板
        self.template_cache = {}
    
    def _get_temp_array(self, shape, dtype=np.uint8):
        """获取临时数组，优先从对象池获取"""
        if self.array_pool:
            return self.array_pool.get_array(shape, dtype)
        return np.zeros(shape, dtype=dtype)
    
    def _return_temp_array(self, array):
        """归还临时数组到对象池"""
        if self.array_pool and array is not None:
            self.array_pool.return_array(array)
    
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
    
    def find_template(self, screenshot: np.ndarray, template_name: str, threshold: Optional[float] = None) -> Optional[Tuple[int, int]]:
        """在截图中查找模板
        
        Args:
            screenshot: 截图数组
            template_name: 模板名称
            
        Returns:
            匹配位置 (x, y) 或 None
        """
        template = self.load_template(template_name)
        if template is None:
            return None
            
        try:
            # 确保截图是灰度图像（与模板保持一致）
            if len(screenshot.shape) == 3:
                screenshot_gray = cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY)
            else:
                screenshot_gray = screenshot.copy()
            
            # 使用对象池获取匹配结果数组
            match_result = self._get_temp_array(
                (screenshot_gray.shape[0] - template.shape[0] + 1,
                 screenshot_gray.shape[1] - template.shape[1] + 1),
                dtype=np.float32
            )
            
            try:
                # 执行模板匹配，移除dst参数以解决兼容性问题
                result = cv2.matchTemplate(screenshot_gray, template, self.method)
                np.copyto(match_result, result)
                
                # 使用传入的阈值或默认阈值
                match_threshold = threshold if threshold is not None else self.threshold
                
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(match_result)
                
                if max_val >= match_threshold:
                    x, y = max_loc
                    logger.debug(f"找到模板 '{template_name}' 位置: ({x}, {y}), 相似度: {max_val:.3f}")
                    return {"found": True, "template_name": template_name,"position":(x, y)}
                    
                logger.debug(f"未找到模板 '{template_name}', 最高相似度: {max_val:.3f}")
                return {"found": False, "template_name": template_name}
                
            finally:
                # 归还数组到对象池
                self._return_temp_array(match_result)
                
        except Exception as e:
            logger.error(f"模板匹配失败: {e}")
            return None
    
    def find_all_templates(self, screenshot, template_name, threshold=None):
        """在截图中查找所有匹配的模板，使用对象池优化内存使用"""
        # 使用指定阈值或默认阈值
        match_threshold = threshold if threshold is not None else self.threshold
        
        # 加载模板
        template = self.load_template(template_name)
        if template is None:
            return []
        
        # 临时数组变量
        screenshot_gray = None
        result = None
        
        try:
            # 转换截图为灰度图像
            if len(screenshot.shape) == 3:
                screenshot_gray = self._get_temp_array(screenshot.shape[:2], np.uint8)
                cv2.cvtColor(screenshot, cv2.COLOR_BGR2GRAY, dst=screenshot_gray)
            else:
                screenshot_gray = screenshot.copy()
            
            # 获取模板尺寸
            template_h, template_w = template.shape
            
            # 创建结果数组
            result_shape = (
                screenshot_gray.shape[0] - template_h + 1,
                screenshot_gray.shape[1] - template_w + 1
            )
            result = self._get_temp_array(result_shape, np.float32)
            
            # 执行模板匹配，移除dst参数以解决兼容性问题
            temp_result = cv2.matchTemplate(screenshot_gray, template, self.method)
            np.copyto(result, temp_result)
            
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
        finally:
            # 归还临时数组到对象池
            if screenshot_gray is not None and len(screenshot.shape) == 3:
                self._return_temp_array(screenshot_gray)
            if result is not None:
                self._return_temp_array(result)
    
    def clear_cache(self):
        """清空模板缓存和对象池"""
        self.template_cache.clear()
        if self.array_pool:
            self.array_pool.clear_pool()
        logger.info("模板缓存和对象池已清空")
    
    def get_pool_stats(self):
        """获取对象池统计信息"""
        if self.array_pool:
            stats = self.array_pool.get_pool_stats()
            logger.info(f"对象池统计: {stats}")
            return stats
        return {}
    
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