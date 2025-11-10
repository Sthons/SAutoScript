#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
from loguru import logger

# 添加核心模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from base_game_script import BaseGameScript

class MyGameScript(BaseGameScript):

    def __init__(self, config_path=None):
        # 调用父类初始化方法
        super().__init__(config_path)
        
        
        self.game_window_rect = {} # 初始化游戏窗口信息
        self.game_window_center_point = {} # 初始化游戏窗口中心坐标
        
        logger.info("夜航手册-65 初始化完成")


    def on_start(self):
        logger.info("游戏窗口定位中...")

        logger.info("目前所有窗口：")
        # logger.info(self.window_locator.list_windows())
        
        game_window = self.window_locator.get_window_rect(window_title="二重螺旋")

        
        if not game_window:
            logger.error("未找到游戏窗口")
            return
            
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
        
            # 判断当前轮次是否完成
        logger.info(self.game_ops.appear(
            "mod\\entrust\\efficiency_props\\default_choice_2.png",  # 模板名称
            timeout=5,        # 超时时间(秒)
            threshold=0.8,    # 匹配阈值
        ))
        logger.info(self.game_ops.appear(
            "mod\\entrust\\efficiency_props\\choice_1.png",  # 模板名称
            timeout=5,        # 超时时间(秒)
            threshold=0.8,    # 匹配阈值
        ))
        logger.info(self.game_ops.appear(
            "mod\\entrust\\efficiency_props\\choice_2.png",  # 模板名称
            timeout=5,        # 超时时间(秒)
            threshold=0.8,    # 匹配阈值
        ))
        logger.info(self.game_ops.appear(
            "mod\\entrust\\efficiency_props\\choice_3.png",  # 模板名称
            timeout=5,        # 超时时间(秒)
            threshold=0.8,    # 匹配阈值
        ))

        # 点击 788 547

        self.input_controller.click(
            x=self.game_window_rect['left']+ int(788/1920*self.game_window_rect['width']), 
            y=self.game_window_rect['top']+ int(580/1080*self.game_window_rect['height']),
            button='left', 
            clicks=1
        )
                


    
    def on_stop(self):
        # self.input_controller.key_up('w') # 松开 w 键
        pass
    
        
if __name__ == "__main__":

    logger.info("启动自定义游戏脚本...")
    
    # 创建脚本实例
    script = MyGameScript()
    
    # 启动脚本
    script.start(1)