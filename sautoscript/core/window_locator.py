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
            left, top, right, bottom = win32gui.GetWindowRect(target_hwnd)
            
            # 计算宽度和高度
            width = right - left
            height = bottom - top
            
            # 获取窗口标题
            title = win32gui.GetWindowText(target_hwnd)
            
            return {
                'hwnd': target_hwnd,
                'title': title,
                'left': left,
                'top': top,
                'right': right,
                'bottom': bottom,
                'width': width,
                'height': height
            }
        except Exception as e:
            logger.error(f"获取窗口信息失败: {e}")
            return None
    
    def _find_window(self, window_title=None, window_class=None):
        """根据标题或类名查找窗口
        
        Args:
            window_title: 窗口标题（部分匹配）
            window_class: 窗口类名
            
        Returns:
            int: 窗口句柄，或 0（如果未找到）
        """
        if window_title:
            # 尝试精确匹配
            hwnd = win32gui.FindWindow(window_class, window_title)
            if hwnd:
                return hwnd
            
            # 尝试部分匹配
            def callback(hwnd, extra):
                title = win32gui.GetWindowText(hwnd)
                if window_title in title:
                    extra.append(hwnd)
                return True
            
            matching_windows = []
            win32gui.EnumWindows(callback, matching_windows)
            
            if matching_windows:
                return matching_windows[0]
        else:
            # 只根据类名查找
            return win32gui.FindWindow(window_class, None)
        
        return 0
    
    def get_all_windows(self):
        """获取所有可见窗口
        
        Returns:
            list: 窗口信息列表
        """
        def callback(hwnd, extra):
            if win32gui.IsWindowVisible(hwnd):
                title = win32gui.GetWindowText(hwnd)
                if title:
                    rect = self.get_window_rect(hwnd=hwnd)
                    if rect:
                        extra.append(rect)
            return True
        
        windows = []
        win32gui.EnumWindows(callback, windows)
        return windows
    
    def set_window_foreground(self, window_title=None, window_class=None, hwnd=None):
        """将窗口设置为前台窗口
        
        Args:
            window_title: 窗口标题
            window_class: 窗口类名
            hwnd: 窗口句柄
            
        Returns:
            bool: 是否成功
        """
        if not hwnd:
            hwnd = self._find_window(window_title, window_class)
            if not hwnd:
                logger.error(f"未找到窗口: title={window_title}, class={window_class}")
                return False
        
        try:
            # 检查窗口是否最小化
            if win32gui.IsIconic(hwnd):
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            
            # 设置为前台窗口
            win32gui.SetForegroundWindow(hwnd)
            logger.debug(f"窗口已设置为前台: {win32gui.GetWindowText(hwnd)}")
            return True
        except Exception as e:
            logger.error(f"设置前台窗口失败: {e}")
            return False
    
    def close_window(self, window_title=None, window_class=None, hwnd=None):
        """关闭窗口
        
        Args:
            window_title: 窗口标题
            window_class: 窗口类名
            hwnd: 窗口句柄
            
        Returns:
            bool: 是否成功
        """
        if not hwnd:
            hwnd = self._find_window(window_title, window_class)
            if not hwnd:
                logger.error(f"未找到窗口: title={window_title}, class={window_class}")
                return False
        
        try:
            # 发送关闭消息
            win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
            logger.debug(f"已发送关闭消息到窗口: {win32gui.GetWindowText(hwnd)}")
            return True
        except Exception as e:
            logger.error(f"关闭窗口失败: {e}")
            return False
