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
        
        logger.info("皎皎币-60 初始化完成")


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
            "mod\\entrust\\jiaojiaobi\\level60\\spawn1.png",  # 模板名称
            timeout=5,        # 超时时间(秒)
            threshold=0.7,    # 匹配阈值
        )
        if not spawn_check_result.get('found', False):
            spawn_check_result = self.game_ops.appear(
                "mod\\entrust\\jiaojiaobi\\level60\\spawn2.png",  # 模板名称
                timeout=5,        # 超时时间(秒)
                threshold=0.7,    # 匹配阈值
            )
            if not spawn_check_result.get('found', False):
                logger.error("未找到目标图片")
                return
            else:
                logger.info("已确认当前区域为起点 2")


                # 向右移动视角 60°
                self.input_controller.move_mouse(x + 300, y)

                self.input_controller.key_down('w')
                self.input_controller.key_down('shift') 
                time.sleep(0.3)

                # 设置鼠标位置到游戏窗口中心
                self.input_controller.set_mouse_position(x, y)
                # 点击鼠标中键 重置鼠标信号
                self.input_controller.click(button='middle')
                time.sleep(0.1)
                # 视角回正
                self.input_controller.move_mouse(x - 300, y)

                time.sleep(6.5)

                # 设置鼠标位置到游戏窗口中心
                self.input_controller.set_mouse_position(x, y)
                # 点击鼠标中键 重置鼠标信号
                self.input_controller.click(button='middle')
                time.sleep(0.1)
                # 向左移动视角 30°
                self.input_controller.move_mouse(x - 300, y)

                time.sleep(1)


                # 设置鼠标位置到游戏窗口中心
                self.input_controller.set_mouse_position(x, y)
                # 点击鼠标中键 重置鼠标信号
                self.input_controller.click(button='middle')
                time.sleep(0.1)
                # 向右移动视角 30°
                self.input_controller.move_mouse(x + 300, y)        

                time.sleep(0.5)

                # 松开 w + shift 组合键
                self.input_controller.key_up('shift') 
                self.input_controller.key_up('w')


                # 判断是否是 关卡 2-1
                level_2_check_result = self.game_ops.appear(
                    "mod\\entrust\\jiaojiaobi\\level60\\level_2_1.png",  # 模板名称
                    timeout=3,        # 超时时间(秒)
                    threshold=0.6,    # 匹配阈值
                )

                level2_type = 1

                if not level_2_check_result.get('found', False):
                    _level_2_check_result = self.game_ops.appear(
                        "mod\\entrust\\jiaojiaobi\\level60\\level_2_1t2.png",  # 模板名称
                        timeout=3,        # 超时时间(秒)
                        threshold=0.6,    # 匹配阈值
                    )
                    if not _level_2_check_result.get('found', False): 
                        level2_type = 2
                    else:
                        self.input_controller.key_press('a', 3)
                

                if level2_type == 1:
                    logger.info("已确认当前区域为关卡 2_1")
                    self.input_controller.key_down('w')
                    self.input_controller.key_down('shift') 
                    time.sleep(22)
                    self.input_controller.key_up('shift') 
                    self.input_controller.key_up('w')
                else:
                    logger.info("已确认当前区域为关卡 2_2")
                    self.input_controller.key_down('w')
                    self.input_controller.key_down('shift') 
                    time.sleep(1.8)

                    # 设置鼠标位置到游戏窗口中心
                    self.input_controller.set_mouse_position(x, y)
                    # 点击鼠标中键 重置鼠标信号
                    self.input_controller.click(button='middle')
                    time.sleep(0.1)
                    # 向左移动视角 45°
                    self.input_controller.move_mouse(x - 240, y)

                    time.sleep(2.5)

                    # 设置鼠标位置到游戏窗口中心
                    self.input_controller.set_mouse_position(x, y)
                    # 点击鼠标中键 重置鼠标信号
                    self.input_controller.click(button='middle')
                    time.sleep(0.1)
                    # 向右移动视角 45°
                    self.input_controller.move_mouse(x + 240, y)
                    
                    time.sleep(15.5)
                    self.input_controller.key_up('shift') 
                    self.input_controller.key_up('w')

                time.sleep(10)

                # 插入 默认 随机事件
                self.random_event()

                time.sleep(10)

                # 插入 默认 随机事件
                self.random_event()

                # 用 二命 赛琪时额外按下q键
                self.input_controller.key_press('q')

                round = 3

                for num in range(round):
                    # 判断当前轮次是否完成
                    if not self.game_ops.appear_then_click(
                        "mod\\general\\choice.png",  # 模板名称
                        timeout=180,        # 超时时间(秒)
                        threshold=0.7,    # 匹配阈值
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
                        
                        break

                    else:
                        self.success_num += 1
                        if num < round - 1:
                            self.game_ops.appear_then_click(
                                "mod\\general\\keep_going.png",  # 模板名称
                                timeout=5,        # 超时时间(秒)
                                threshold=0.8,    # 匹配阈值
                                click_delay=random.randint(2, 6)   # 点击后延迟
                            )
                            if num == round - 2:
                                
                                # 使用 委托手册·一
                                self.input_controller.click(
                                    x=self.game_window_rect['left']+ int(788/1920*self.game_window_rect['width']), 
                                    y=self.game_window_rect['top']+ int(580/1080*self.game_window_rect['height']),
                                    button='left', 
                                    clicks=1
                                )


                            self.game_ops.appear_then_click(
                                "mod\\general\\raid_start.png",  # 模板名称
                                timeout=5,        # 超时时间(秒)
                                threshold=0.6,    # 匹配阈值
                                click_delay=random.randint(2, 6)   # 点击后延迟
                            )

                        else:
                            self.game_ops.appear_then_click(
                                "mod\\general\\runaway.png",  # 模板名称
                                timeout=5,        # 超时时间(秒)
                                threshold=0.8,    # 匹配阈值
                                click_delay=random.randint(2, 6)   # 点击后延迟
                            )

        else:
                logger.info("已确认当前区域为起点 1")
                logger.info("尝试重开")
                
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

 
        

        # 点击再次进行 1386/1920 952/1080
        # self.game_ops.appear_then_click(
        #     "mod\\general\\again.png",  # 模板名称
        #     timeout=150,        # 超时时间(秒)
        #     threshold=0.8,    # 匹配阈值
        #     click_delay=5   # 点击后延迟
        # )
        time.sleep(2)
        self.input_controller.click(
            x=self.game_window_rect['left']+ int(1386/1920*self.game_window_rect['width']), 
            y=self.game_window_rect['top']+ int(952/1080*self.game_window_rect['height']),
            button='left', 
            clicks=2
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