#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os

# 添加项目根目录到Python路径
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from core.screen_capture import ScreenCapture
import yaml

def test_capture_methods():
    """测试不同的截图方法"""
    
    # 加载配置文件
    config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        config = yaml.safe_load(f)
    
    screen_capture_config = config.get('screen_capture', {})
    
    # 测试配置中的截图方法
    capture_method = screen_capture_config.get('capture_method', 'mss')
    print(f"当前配置的截图方法: {capture_method}")
    
    # 创建屏幕捕获对象
    screen_capture = ScreenCapture(screen_capture_config)
    
    # 测试获取屏幕尺寸
    try:
        screen_size = screen_capture.get_screen_size()
        print(f"屏幕尺寸: {screen_size}")
    except Exception as e:
        print(f"获取屏幕尺寸失败: {e}")
    
    # 测试截图
    try:
        screenshot = screen_capture.capture(as_numpy=False)
        if screenshot:
            print(f"截图成功，尺寸: {screenshot.size}, 模式: {screenshot.mode}")
            
            # 保存测试截图
            test_filename = f"test_capture_{capture_method}.png"
            if screen_capture.save_screenshot(test_filename):
                print(f"测试截图已保存: {test_filename}")
            else:
                print("保存截图失败")
        else:
            print("截图失败")
    except Exception as e:
        print(f"截图测试失败: {e}")
    
    # 测试区域截图
    try:
        region_screenshot = screen_capture.capture_region(0, 0, 100, 100, as_numpy=False)
        if region_screenshot:
            print(f"区域截图成功，尺寸: {region_screenshot.size}")
        else:
            print("区域截图失败")
    except Exception as e:
        print(f"区域截图测试失败: {e}")

if __name__ == "__main__":
    test_capture_methods()