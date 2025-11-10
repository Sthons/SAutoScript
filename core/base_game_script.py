#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import random
import yaml
from abc import ABC, abstractmethod
from loguru import logger

from image_recognition import ImageRecognition
from input_controller import InputController
from screen_capture import ScreenCapture
from game_operations import GameOperations, GameStuckError, GameTooManyClickError
from window_locator import WindowLocator
from error_logger import log_exception


class BaseGameScript(ABC):
    """
    游戏脚本基类
    
    所有游戏脚本都应继承此类，实现通用的初始化、配置加载和主循环功能。
    子类需要实现game_logic方法来定义具体的游戏逻辑。
    """
    
    def __init__(self, config_path=None):
        """
        初始化游戏脚本
        
        Args:
            config_path: 配置文件路径，默认为../config/settings.yaml
        """
        # 加载配置
        self.config = self._load_config(config_path)
        
        # 初始化组件
        self._init_components()
        
        # 运行状态
        self.running = False

        # 成功执行次数
        self.success_num = 0
        
        # 循环控制
        self.max_loops = self.config.get("script", {}).get("max_loops", 100)  # 默认最多执行100次循环
        self.loop_delay = self.config.get("script", {}).get("loop_delay", 1)  # 默认循环间隔1秒
        
        logger.info(f"{self.__class__.__name__}初始化完成")
    
    def _load_config(self, config_path=None):
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            dict: 配置字典
        """
        if config_path is None:
            # 默认配置文件路径
            config_path = os.path.join(os.path.dirname(__file__), '..', 'config', 'settings.yaml')
        
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            # 记录错误到以时间命名的日志文件
            script_name = self.__class__.__name__
            log_exception(f"在{script_name}的_load_config方法中加载配置文件{config_path}时发生错误", script_name)
            return {}
    
    def _init_components(self):
        """
        初始化组件
        """
        try:
            # 初始化屏幕捕获组件
            screen_capture_config = self.config.get("screen", {})
            self.screen_capture = ScreenCapture(screen_capture_config)
            
            # 初始化输入控制组件
            input_controller_config = self.config.get("input", {})
            self.input_controller = InputController(input_controller_config)
            
            # 初始化图像识别组件
            self.image_recognition = ImageRecognition(self.config.get("recognition", {}))

            # 初始化窗口定位组件
            self.window_locator = WindowLocator()
            
            # 初始化游戏操作组件
            self.game_ops = GameOperations(
                self.image_recognition, 
                self.input_controller, 
                self.screen_capture, 
                self.config
            )
        except Exception as e:
            logger.error(f"组件初始化失败: {e}")
            # 记录错误到以时间命名的日志文件
            script_name = self.__class__.__name__
            log_exception(f"在{script_name}的_init_components方法中初始化组件时发生错误", script_name)
            raise
    
    def start(self, max_loops=1, loop_delay=1):
        """
        启动脚本
        """
        logger.info(f"启动{self.__class__.__name__}")

        # 设置循环次数和延迟
        self.max_loops = max_loops  # 最多执行 x 次循环
        self.loop_delay = loop_delay  # 循环间隔 x 秒

        self.running = True
        
        try:
            # 调用启动前钩子
            self.on_start()
            
            # 主循环
            self._main_loop()
        except KeyboardInterrupt:
            logger.info("接收到中断信号，正在停止...")
        except Exception as e:
            logger.error(f"运行时错误: {e}")
            # 记录错误到以时间命名的日志文件
            script_name = self.__class__.__name__
            log_exception(f"在{script_name}的start方法中发生错误", script_name)
        finally:
            self.stop()
    
    def stop(self):
        """
        停止脚本
        """
        logger.info(f"停止{self.__class__.__name__}")
        self.running = False
        
        # 调用停止后钩子
        self.on_stop()
    
    def _main_loop(self):
        """
        主循环
        """
        loop_count = 0
        
        while self.running and loop_count < self.max_loops:
            try:
                # 调用游戏逻辑
                self.game_logic()
                loop_count += 1
                logger.info(f"循环执行次数: {loop_count}/{self.max_loops}")
                if self.success_num:
                    logger.info(f"当前执行成功次数: {self.success_num}/{loop_count}")

                
                # 每次循环后添加延迟
                time.sleep(self.loop_delay)
            except Exception as e:
                logger.error(f"主循环错误: {e}，脚本将退出")
                # 记录错误到以时间命名的日志文件
                script_name = self.__class__.__name__
                log_exception(f"在{script_name}的主循环第{loop_count+1}次迭代中发生错误", script_name)
                break
        
        logger.info(f"已完成{loop_count}次循环，脚本将退出")
    
    @abstractmethod
    def game_logic(self):
        """
        游戏逻辑，子类必须实现此方法
        """
        pass
    
    def on_start(self):
        """
        启动前钩子，子类可以重写此方法来执行启动前的操作
        """
        pass
    
    def on_stop(self):
        """
        停止后钩子，子类可以重写此方法来执行停止后的操作
        """
        pass
    
    def create_template_from_screenshot(self, region, filename):
        """
        从截图区域创建模板
        
        Args:
            region: 截图区域 (x, y, width, height)
            filename: 模板文件名
            
        Returns:
            bool: 是否成功创建模板
        """
        # 捕获屏幕
        screenshot = self.screen_capture.capture()
        
        if screenshot is not None:
            # 保存指定区域为模板
            success = self.image_recognition.save_screenshot_region(screenshot, region, filename)
            
            if success:
                logger.info(f"模板已创建: {filename}")
                return True
        
        logger.error("创建模板失败")
        return False
    
    def random_event(self):
        """
        随机事件，子类可以重写此方法来实现随机事件
        """

        random_type = random.choice(["jump", "left_right", "squat_down", "rotating_perspective"])
        
        if random_type == "jump":
            # 跳跃
            self.input_controller.key_press('space')
            time.sleep(9)
            self.input_controller.key_press('space')
        elif random_type == "left_right":
            # 左右移动 
            self.input_controller.key_press('a')
            time.sleep(9)
            self.input_controller.key_press('d')
        elif random_type == "squat_down":
            # 蹲下
            self.input_controller.key_down('ctrl')
            time.sleep(9)
            self.input_controller.key_up('ctrl')
        elif random_type == "rotating_perspective":
            # 旋转视角 2 次
            self.input_controller.move_mouse(random.randint(0, 3440), random.randint(0, 2560), 3)
            time.sleep(3)
            self.input_controller.move_mouse(random.randint(0, 3440), random.randint(0, 2560), 3)


        pass
