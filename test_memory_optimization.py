#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import os
import time
import numpy as np
from loguru import logger

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.base_game_script import BaseGameScript


class TestMemoryScript(BaseGameScript):
    """
    测试内存优化功能的脚本
    模拟高频图像处理场景
    """
    
    def __init__(self, config_path=None):
        super().__init__(config_path)
        self.large_data_list = []  # 用于模拟内存累积
    
    def game_logic(self):
        """
        模拟游戏逻辑，包含大量图像处理操作
        """
        try:
            # 模拟屏幕捕获（创建大量临时数组）
            for i in range(5):
                # 模拟屏幕截图数组
                fake_screenshot = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
                
                # 模拟图像处理（创建更多临时对象）
                gray_image = np.mean(fake_screenshot, axis=2)
                resized_image = np.resize(gray_image, (540, 960))
                
                # 模拟模板匹配结果
                match_result = np.random.random((100, 100))
                
                # 故意保留一些对象以模拟内存累积
                if i % 10 == 0:
                    self.large_data_list.append({
                        'screenshot': fake_screenshot.copy(),
                        'processed': resized_image.copy(),
                        'timestamp': time.time()
                    })
                
                # 清理部分内存
                del fake_screenshot, gray_image, resized_image, match_result
            
            # 模拟游戏操作（使用图像识别）
            self._simulate_game_operations()
            
            # 记录成功
            self.success_num += 1
            
            # 每20次循环报告一次内存状态
            if self.success_num % 20 == 0:
                current_memory = self._get_memory_usage()
                logger.info(f"当前内存使用: {current_memory:.1f}MB, 保留对象数: {len(self.large_data_list)}")
            
        except Exception as e:
            logger.error(f"游戏逻辑执行错误: {e}")
    
    def _simulate_game_operations(self):
        """
        模拟游戏操作，使用图像识别功能
        """
        try:
            # 模拟图像识别操作
            template = np.random.randint(0, 255, (50, 50), dtype=np.uint8)
            
            # 模拟多次模板匹配
            for _ in range(3):
                screenshot = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
                gray_screen = np.mean(screenshot, axis=2)
                gray_template = np.mean(template, axis=2) if len(template.shape) == 3 else template
                
                # 模拟cv2.matchTemplate操作
                result = np.random.random((gray_screen.shape[0] - gray_template.shape[0] + 1,
                                         gray_screen.shape[1] - gray_template.shape[1] + 1))
                
                # 模拟找到最佳匹配
                min_val, max_val = np.min(result), np.max(result)
                min_loc, max_loc = np.unravel_index(np.argmin(result)), np.unravel_index(np.argmax(result))
                
                logger.debug(f"模拟匹配结果: min={min_val:.3f} at {min_loc}, max={max_val:.3f} at {max_loc}")
                
                del screenshot, gray_screen, gray_template, result
            
            del template
            
        except Exception as e:
            logger.warning(f"模拟游戏操作出错: {e}")
    
    def on_start(self):
        """
        启动前的初始化
        """
        logger.info("=== 开始测试智能垃圾回收功能 ===")
        logger.info(f"配置参数:")
        logger.info(f"  - GC频率: {self.gc_frequency}")
        logger.info(f"  - 内存阈值: {self.memory_threshold_mb}MB")
        logger.info(f"  - 启用智能GC: {self.enable_smart_gc}")
        logger.info(f"  - 启用内存监控: {self.enable_memory_monitoring}")
        logger.info(f"  - 内存检查频率: {self.memory_check_frequency}")
        
        # 记录初始内存
        initial_memory = self._get_memory_usage()
        logger.info(f"初始内存使用: {initial_memory:.1f}MB")
    
    def on_stop(self):
        """
        停止后的清理
        """
        # 清理累积的数据
        self.large_data_list.clear()
        
        # 记录最终内存
        final_memory = self._get_memory_usage()
        logger.info(f"最终内存使用: {final_memory:.1f}MB")
        
        logger.info("=== 测试完成 ===")


def main():
    """
    主函数
    """
    # 配置日志
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}")
    logger.add("logs/memory_test.log", level="DEBUG", rotation="10 MB", retention="7 days")
    
    try:
        # 创建测试脚本
        script = TestMemoryScript()
        
        # 运行测试（执行100次循环，每循环间隔0.1秒）
        script.start(max_loops=100, loop_delay=0.1)
        
    except KeyboardInterrupt:
        logger.info("测试被用户中断")
    except Exception as e:
        logger.error(f"测试执行出错: {e}")


if __name__ == "__main__":
    main()