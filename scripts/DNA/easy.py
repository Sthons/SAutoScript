#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
from loguru import logger

# 添加核心模块路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.base_game_script import BaseGameScript

class MyGameScript(BaseGameScript):

    def __init__(self, config_path=None):
        # 调用父类初始化方法
        super().__init__(config_path)
        
        
        self.game_window_rect = {} # 初始化游戏窗口信息
        self.game_window_center_point = {} # 初始化游戏窗口中心坐标
        

    def on_start(self):
        logger.info("游戏窗口定位中...")

        logger.info("目前所有窗口：")
        # logger.info(self.window_locator.list_windows())
        
        game_window = self.window_locator.get_window_rect(window_title="二重螺旋")

        
        # if not game_window:
        #     logger.error("未找到游戏窗口")
        #     return
            
        # 确保游戏窗口在前台
        self.window_locator.bring_to_front(game_window['hwnd'])

        logger.info("游戏窗口定位成功！")
        self.game_window_rect = game_window
        # 计算游戏窗口中心坐标
        self.game_window_center_point = {
            'left': game_window['left'] + game_window['width'] // 2,
            'top': game_window['top'] + game_window['height'] // 2
        }
        

        return 

    def game_logic(self):
        """
        游戏逻辑，子类必须实现此方法
        """
        
        # 结束状态识别 
        result = self.game_ops.appear(
            "mod\\general\\finish.png",  # 模板名称
            timeout=10,        # 超时时间(秒)
            threshold=0.8,    # 匹配阈值
        )
        if not result.get('found', False):
            # 点击 开始挑战 按钮 
            self.game_ops.appear_then_click(
                "mod\\general\\raid_start.png",  # 模板名称
                timeout=10,        # 超时时间(秒)
                threshold=0.6,    # 匹配阈值
                click_delay=random.randint(8, 15)   # 点击后延迟
            )

    
    def on_stop(self):
        # self.input_controller.key_up('w') # 松开 w 键
        pass
    
        
if __name__ == "__main__":

    logger.info("启动自定义游戏脚本...")
    
    # 创建脚本实例
    script = MyGameScript()
    
    # 启动脚本
    script.start(100000)