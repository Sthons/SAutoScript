#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import win32gui
import win32con
from loguru import logger


class WindowLocator:
    """窗口定位模块，用于获取窗口位置和大小"""
    
    def __init__(self, config=None):
        self.config = config or {}
        logger.info("窗口定位模块初始化完成")
    
    def get_window_rect(self, window_title=None, window_class=None, hwnd=None):
        """获取窗口的位置和大小
        
        Args:
            window_title: 窗口标题（部分匹配）
            window_class: 窗口类名
            hwnd: 窗口句柄（如果已知）
            
        Returns:
            dict: 包含窗口位置和大小信息的字典
                {
                    'hwnd': 窗口句柄,
                    'title': 窗口标题,
                    'left': 左边距,
                    'top': 上边距,
                    'right': 右边距,
                    'bottom': 下边距,
                    'width': 宽度,
                    'height': 高度
                }
            或 None（如果未找到窗口）
        """
        if hwnd:
            # 如果提供了窗口句柄，直接使用
            target_hwnd = hwnd
        else:
            # 根据标题或类名查找窗口
            target_hwnd = self._find_window(window_title, window_class)
        
        if not target_hwnd:
            logger.warning(f"未找到窗口: title={window_title}, class={window_class}")
            return None
        
        try:
            # 获取窗口矩形
            rect = win32gui.GetWindowRect(target_hwnd)
            left, top, right, bottom = rect
            
            # 获取窗口标题
            title = win32gui.GetWindowText(target_hwnd)
            
            # 计算宽度和高度
            width = right - left
            height = bottom - top
            
            result = {
                'hwnd': target_hwnd,
                'title': title,
                'left': left,
                'top': top,
                'right': right,
                'bottom': bottom,
                'width': width,
                'height': height
            }
            
            logger.info(f"获取窗口信息成功: {title} ({width}x{height} at {left},{top})")
            return result
            
        except Exception as e:
            logger.error(f"获取窗口信息失败: {e}")
            return None
    
    def _find_window(self, window_title=None, window_class=None):
        """根据标题或类名查找窗口
        
        Args:
            window_title: 窗口标题（部分匹配）
            window_class: 窗口类名
            
        Returns:
            int: 窗口句柄，如果未找到则返回None
        """
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                
                # 检查标题匹配
                title_match = True
                if window_title:
                    title_match = window_title.lower() in title.lower()
                
                # 检查类名匹配
                class_match = True
                if window_class:
                    class_match = window_class.lower() in class_name.lower()
                
                # 如果都匹配，添加到结果列表
                if title_match and class_match:
                    windows.append((hwnd, title, class_name))
            
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        if not windows:
            return None
        
        # 返回第一个匹配的窗口句柄
        return windows[0][0]
    
    def list_windows(self, filter_title=None, filter_class=None):
        """列出所有可见窗口
        
        Args:
            filter_title: 标题过滤字符串（部分匹配）
            filter_class: 类名过滤字符串（部分匹配）
            
        Returns:
            list: 窗口信息列表，每个元素是一个字典
        """
        def enum_windows_callback(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                class_name = win32gui.GetClassName(hwnd)
                
                # 检查标题过滤
                title_match = True
                if filter_title:
                    title_match = filter_title.lower() in title.lower()
                
                # 检查类名过滤
                class_match = True
                if filter_class:
                    class_match = filter_class.lower() in class_name.lower()
                
                # 如果都匹配，添加到结果列表
                if title_match and class_match:
                    windows.append({
                        'hwnd': hwnd,
                        'title': title,
                        'class': class_name
                    })
            
            return True
        
        windows = []
        win32gui.EnumWindows(enum_windows_callback, windows)
        
        logger.info(f"找到 {len(windows)} 个匹配的窗口")
        return windows
    
    def move_window(self, hwnd, x, y, width=None, height=None):
        """移动窗口到指定位置并调整大小
        
        Args:
            hwnd: 窗口句柄
            x: 新的左边距
            y: 新的上边距
            width: 新的宽度（可选）
            height: 新的高度（可选）
            
        Returns:
            bool: 操作是否成功
        """
        try:
            if width is None or height is None:
                # 如果没有指定宽度或高度，获取当前窗口大小
                rect = win32gui.GetWindowRect(hwnd)
                current_width = rect[2] - rect[0]
                current_height = rect[3] - rect[1]
                
                width = width if width is not None else current_width
                height = height if height is not None else current_height
            
            # 移动并调整窗口大小
            win32gui.SetWindowPos(
                hwnd, 
                win32con.HWND_TOP, 
                x, y, width, height, 
                win32con.SWP_SHOWWINDOW
            )
            
            logger.info(f"窗口移动成功: hwnd={hwnd}, 位置=({x},{y}), 大小={width}x{height}")
            return True
            
        except Exception as e:
            logger.error(f"窗口移动失败: {e}")
            return False
    
    def bring_to_front(self, hwnd):
        """将窗口置于前台
        
        Args:
            hwnd: 窗口句柄
            
        Returns:
            bool: 操作是否成功
        """
        try:
            # 检查窗口是否最小化
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            
            # 将窗口置于前台
            win32gui.SetForegroundWindow(hwnd)
            
            logger.info(f"窗口已置于前台: hwnd={hwnd}")
            return True
            
        except Exception as e:
            logger.error(f"将窗口置于前台失败: {e}")
            return False