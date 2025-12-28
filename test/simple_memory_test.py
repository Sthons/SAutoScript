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


class SimpleMemoryTest(BaseGameScript):
    """
    简化的内存测试脚本，专门测试智能垃圾回收功能
    """
    
    def game_logic(self):
        """
        模拟简单的内存分配操作
        """
        # 创建大量临时数组来模拟图像处理
        temp_arrays = []
        for i in range(10):
            # 创建不同大小的数组来模拟不同尺寸的图像
            arr = np.random.randint(0, 255, (100 + i*10, 100 + i*10, 3), dtype=np.uint8)
            temp_arrays.append(arr)
        
        # 模拟一些图像处理操作
        for arr in temp_arrays[:5]:
            gray = np.mean(arr, axis=2)
            resized = np.resize(gray, (50, 50))
            # 这些临时对象将在方法结束时自动释放
        
        self.success_num += 1
        
        # 每10次循环报告内存状态
        if self.success_num % 10 == 0:
            current_memory = self._get_memory_usage()
            logger.info(f"第{self.success_num}次循环，当前内存: {current_memory:.1f}MB")
    
    def on_start(self):
        logger.info("开始简化内存测试")
        initial_memory = self._get_memory_usage()
        logger.info(f"初始内存: {initial_memory:.1f}MB")
    
    def on_stop(self):
        final_memory = self._get_memory_usage()
        logger.info(f"最终内存: {final_memory:.1f}MB")
        logger.info("简化内存测试完成")


def main():
    # 配置日志
    logger.remove()
    logger.add(sys.stdout, level="INFO", format="{time:HH:mm:ss} | {level} | {message}")
    
    try:
        # 创建并运行测试
        script = SimpleMemoryTest()
        script.start(max_loops=50, loop_delay=0.2)
        
    except KeyboardInterrupt:
        logger.info("测试被中断")
    except Exception as e:
        logger.error(f"测试出错: {e}")


if __name__ == "__main__":
    main()