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
        
        logger.info("密函线索 初始化完成")


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

        # 判断起点类型
        spawn_check_result = self.game_ops.appear(
            "mod\\entrust\\letter_clues\\spawn1.png",  # 起点 1
            timeout=5,        # 超时时间(秒)
            threshold=0.7,    # 匹配阈值
        )
        if not spawn_check_result.get('found', False):
            spawn_check_result = self.game_ops.appear(
                "mod\\entrust\\letter_clues\\spawn2.png",  # 起点 2
                timeout=5,        # 超时时间(秒)
                threshold=0.7,    # 匹配阈值
            )

            logger.info("已确认当前区域为起点 2")

            # 按住 ctrl space 键 已实现游戏人物飞跃
            self.input_controller.hotkey('ctrl', 'space') 
            time.sleep(0.3)
            # 按住 ctrl space 键 已实现游戏人物飞跃
            self.input_controller.hotkey('ctrl', 'space') 
            time.sleep(0.3)
            # 按住 ctrl space 键 已实现游戏人物飞跃
            self.input_controller.hotkey('ctrl', 'space') 
            time.sleep(0.3)
            # 按住 ctrl space 键 已实现游戏人物飞跃
            self.input_controller.hotkey('ctrl', 'space') 
            time.sleep(0.3)
            # 按住 ctrl space 键 已实现游戏人物飞跃
            self.input_controller.hotkey('ctrl', 'space') 
            time.sleep(0.3)

            # 按住 a 键 向左移动
            self.input_controller.key_press('a', 4)

            self.input_controller.key_press('s')
            # 松开 a 键 停止向左移动
            self.input_controller.key_press('f', random.randint(5, 9), 0.03)

        

            round = 12

            for num in range(round):
                # 判断当前轮次是否完成
                if not self.game_ops.appear_then_click(
                    "mod\\general\\choice.png",  # 模板名称
                    timeout=120,        # 超时时间(秒)
                    threshold=0.6,    # 匹配阈值
                    click_delay=3   # 点击后延迟
                ):
                    # 卡关
                    # 输入 esc 呼出菜单
                    self.input_controller.key_press('esc')

                    # 点击放弃挑战
                    self.game_ops.appear_then_click(
                        "mod\\pause\\give_up_the_challenge.png",  # 模板名称
                        timeout=5,        # 超时时间(秒)
                        threshold=0.8,    # 匹配阈值
                        click_delay=3   # 点击后延迟
                    )

                    # 在出现的弹窗中点击确定
                    self.game_ops.appear_then_click(
                        "mod\\general\\entry.png",  # 模板名称
                        timeout=5,        # 超时时间(秒)
                        threshold=0.8,    # 匹配阈值
                        click_delay=5   # 点击后延迟
                    )
                else:
                    self.success_num += 1
                    if num < round - 1:
                        self.game_ops.appear_then_click(
                            "mod\\general\\keep_going.png",  # 模板名称
                            timeout=5,        # 超时时间(秒)
                            threshold=0.8,    # 匹配阈值
                            click_delay=random.randint(1, 3)   # 点击后延迟
                        )
                        self.game_ops.appear_then_click(
                            "mod\\general\\raid_start.png",  # 模板名称
                            timeout=5,        # 超时时间(秒)
                            threshold=0.6,    # 匹配阈值
                            click_delay=random.randint(1, 3)   # 点击后延迟
                        )

                    else:
                        self.game_ops.appear_then_click(
                            "mod\\general\\runaway.png",  # 模板名称
                            timeout=5,        # 超时时间(秒)
                            threshold=0.8,    # 匹配阈值
                            click_delay=random.randint(1, 3)   # 点击后延迟
                        )

        else:
            self.input_controller.key_press('esc')

            # 点击放弃挑战
            self.game_ops.appear_then_click(
                "mod\\pause\\give_up_the_challenge.png",  # 模板名称
                timeout=5,        # 超时时间(秒)
                threshold=0.8,    # 匹配阈值
                click_delay=3   # 点击后延迟
            )

            # 在出现的弹窗中点击确定
            self.game_ops.appear_then_click(
                "mod\\general\\entry.png",  # 模板名称
                timeout=5,        # 超时时间(秒)
                threshold=0.8,    # 匹配阈值
                click_delay=5   # 点击后延迟
            )
        
        # 点击再次进行 
        self.game_ops.appear_then_click(
            "mod\\general\\again.png",  # 模板名称
            timeout=150,        # 超时时间(秒)
            threshold=0.6,    # 匹配阈值
            click_delay=5   # 点击后延迟
        )

        # 点击 开始挑战 按钮 
        self.game_ops.appear_then_click(
            "mod\\general\\raid_start.png",  # 模板名称
            timeout=10,        # 超时时间(秒)
            threshold=0.6,    # 匹配阈值
            click_delay=random.randint(2, 6)   # 点击后延迟
        )
        time.sleep(10)

    
    def on_stop(self):
        # self.input_controller.key_up('w') # 松开 w 键
        pass
    
        
if __name__ == "__main__":

    logger.info("启动自定义游戏脚本...")
    
    # 创建脚本实例
    script = MyGameScript()
    
    # 启动脚本
    script.start(100)