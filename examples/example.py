#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from loguru import logger

# 导入 SAutoScript 库
from sautoscript import BaseGameScript

class ExampleScript(BaseGameScript):
    """示例游戏脚本"""
    
    def __init__(self, config_path=None):
        # 调用父类初始化方法
        super().__init__(config_path)
        
        # 设置循环次数和延迟
        self.max_loops = 10  # 最多执行10次循环
        self.loop_delay = 2  # 循环间隔2秒
        
        # 添加自定义属性
        self.custom_counter = 0
        
        logger.info("示例脚本初始化完成")
    
    def on_start(self):
        """启动前钩子"""
        logger.info("执行启动前操作...")
        
        # 示例：确保游戏窗口处于前台
        # self.input_controller.key_press('esc')  # 按ESC键确保游戏窗口激活
        
        logger.info("启动前操作完成")
    
    def game_logic(self):
        """
        实现具体的游戏逻辑
        
        这个方法会在主循环中被调用，每次调用代表一次游戏操作
        """
        # 捕获屏幕
        screenshot = self.screen_capture.capture()
        
        if screenshot is None:
            logger.warning("屏幕捕获失败，跳过本次循环")
            return
        
        # 示例：随机事件
        if self.custom_counter % 3 == 0:
            self.random_event()
        
        # 示例：模拟按键操作
        self.input_controller.key_press('space')
        logger.info("按下空格键")
        
        # 增加计数器
        self.custom_counter += 1
        self.success_num += 1
        
        logger.info(f"第 {self.custom_counter} 次循环执行完成")
    
    def on_stop(self):
        """停止后钩子"""
        logger.info("执行停止后操作...")
        
        # 示例：记录统计信息
        logger.info(f"脚本执行完成，共执行了{self.custom_counter}次循环")
        logger.info(f"成功执行次数: {self.success_num}")
        
        logger.info("停止后操作完成")

if __name__ == "__main__":
    # 创建脚本实例
    script = ExampleScript()
    
    # 启动脚本
    script.start()
