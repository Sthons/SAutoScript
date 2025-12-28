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

        x, y = self.game_window_center_point['left'], self.game_window_center_point['top']
        
        # 设置鼠标位置到游戏窗口中心
        self.input_controller.set_mouse_position(x, y)

        # 点击鼠标中键 重置鼠标信号
        self.input_controller.click(button='middle')

        # 向左移动人物视角
        self.input_controller.move_mouse(x - 220, y, duration=0.3)

        # 按住 w 键 保持前进
        self.input_controller.key_down('w')
        
        # 设置鼠标位置到游戏窗口中心
        self.input_controller.set_mouse_position(x, y)

        # 点击鼠标中键 重置鼠标信号
        self.input_controller.click(button='middle')

        # 向下移动人物视角
        self.input_controller.move_mouse(x, y+400, duration=0.3)

        # 按住 ctrl space 键 已实现游戏人物飞跃
        self.input_controller.hotkey('ctrl', 'space') 

        # 按住鼠标右键 触发射击悬空
        self.input_controller.mouse_down('right')
        time.sleep(3)

        # 松开鼠标右键
        self.input_controller.mouse_up('right')

        # 按住鼠标左键触发下落攻击
        self.input_controller.click('left', clicks=2)

        # 设置鼠标位置到游戏窗口中心
        self.input_controller.set_mouse_position(x, y)

        # 点击鼠标中键 重置鼠标信号
        self.input_controller.click(button='middle')
        time.sleep(0.1)

        # 向左移动人物视角
        self.input_controller.move_mouse(x - 280, y, duration=0.3)
        
        # 按住 shift 键 进入奔跑状态
        self.input_controller.key_down('shift')

        time.sleep(5)

        # 按住 ctrl space 键 已实现游戏人物飞跃
        self.input_controller.hotkey('ctrl', 'space') 

        time.sleep(2)

        # 按住 ctrl space 键 已实现游戏人物飞跃
        self.input_controller.hotkey('ctrl', 'space') 

        time.sleep(3.5)

        # 设置鼠标位置到游戏窗口中心
        self.input_controller.set_mouse_position(x, y)

        # 点击鼠标中键 重置鼠标信号
        self.input_controller.click(button='middle')
        time.sleep(0.1)

        # 向下移动人物视角
        self.input_controller.move_mouse(x, y+450)

        # 按住 ctrl space 键 已实现游戏人物飞跃
        self.input_controller.hotkey('ctrl', 'space') 

        # 按住鼠标右键 触发射击悬空
        self.input_controller.mouse_down('right')
        time.sleep(random.choice([2.7, 2.9, 3.1]))
        
        # 松开鼠标右键
        self.input_controller.mouse_up('right')

        # 松开 shift 键 离开奔跑状态
        self.input_controller.key_up('shift')

        # 松开 w 键 停止前进
        self.input_controller.key_up('w')

        time.sleep(10)

        # 插入 默认 随机事件
        self.random_event()

        # 插入 默认 随机事件
        self.random_event()

        # 用 二命 赛琪时额外按下q键
        self.input_controller.key_press('q')

        # 判断是否通关
        if not self.game_ops.appear_then_click(
            "mod\\general\\again.png",  # 模板名称
            timeout=150,        # 超时时间(秒)
            threshold=0.7,    # 匹配阈值
            click_delay=20   # 点击后延迟
        ):
            # 卡关

            # 输入 esc 呼出菜单
            self.input_controller.key_press('esc')

            # 点击放弃挑战
            self.game_ops.appear_then_click(
                "mod\\pause\\give_up_the_challenge.png",  # 模板名称
                timeout=5,        # 超时时间(秒)
                threshold=0.7,    # 匹配阈值
                click_delay=3   # 点击后延迟
            )

            # 在出现的弹窗中点击确定
            self.game_ops.appear_then_click(
                "mod\\general\\entry.png",  # 模板名称
                timeout=5,        # 超时时间(秒)
                threshold=0.6,    # 匹配阈值
                click_delay=5   # 点击后延迟
            )
            
            # 点击 再次进行
            self.game_ops.appear_then_click(
                "mod\\general\\again.png",  # 模板名称
                timeout=5,        # 超时时间(秒)
                threshold=0.7,    # 匹配阈值
                click_delay=5   # 点击后延迟
            )

            

        else:
            # 成功执行次数+1
            self.success_num += 1

        # 使用 委托手册·一
        self.input_controller.click(
            x=self.game_window_rect['left']+ int(788/1920*self.game_window_rect['width']), 
            y=self.game_window_rect['top']+ int(580/1080*self.game_window_rect['height']),
            button='left', 
            clicks=1
        )

        # 点击 开始挑战 按钮
        self.game_ops.appear_then_click(
            "mod\\general\\raid_start.png",  # 模板名称
            timeout=5,        # 超时时间(秒)
            threshold=0.7,    # 匹配阈值
            click_delay=random.randint(2, 6)   # 点击后延迟
        )
        time.sleep(8)

        # # 重进副本后呼出 esc 菜单
        # self.input_controller.key_press('esc') 

    
    def on_stop(self):
        # self.input_controller.key_up('w') # 松开 w 键
        pass
    
        
if __name__ == "__main__":

    logger.info("启动脚本 夜航手册 65 级...")
    
    # 创建脚本实例
    script = MyGameScript()
    
    # 启动脚本
    script.start(300)