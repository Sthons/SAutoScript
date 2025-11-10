#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import time
import threading
import yaml
from loguru import logger

# 添加核心模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), 'core'))

from image_recognition import ImageRecognition
from input_controller import InputController
from screen_capture import ScreenCapture
from core import log_exception


class GameAutoScript:
    """游戏自动脚本主类"""
    
    def __init__(self):
        self.config = self._load_config()
        self.running = False
        
        # 配置日志
        self._setup_logger()
        
        # 初始化组件
        self._init_components()
        
    def _load_config(self):
        """加载配置文件"""
        config_path = os.path.join(os.path.dirname(__file__), 'config', 'settings.yaml')
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {config_path} 不存在，使用默认配置")
            return self._get_default_config()
        except Exception as e:
            logger.error(f"加载配置文件失败: {e}")
            # 记录错误到以时间命名的日志文件
            log_exception(f"在GameAutoScript的_load_config方法中加载配置文件{config_path}时发生错误", "GameAutoScript")
            return self._get_default_config()
    
    def _get_default_config(self):
        """获取默认配置"""
        return {
            "screen": {
                "capture_interval": 0.1,  # 屏幕捕获间隔(秒)
                "region": null,  # 捕获区域，null表示全屏
                "resolution": [1920, 1080]  # 屏幕分辨率
            },
            "recognition": {
                "threshold": 0.8,  # 图像匹配阈值
                "method": "cv2.TM_CCOEFF_NORMED"  # 匹配方法
            },
            "input": {
                "delay": 0.1,  # 输入延迟(秒)
                "move_duration": 0.2  # 鼠标移动持续时间(秒)
            },
            "logging": {
                "level": "INFO",
                "file": "logs/dnaas.log",
                "rotation": "10 MB"
            }
        }
    
    def _setup_logger(self):
        """配置日志系统"""
        try:
            log_config = self.config.get("logging", {})
            log_level = log_config.get("level", "INFO")
            log_file = log_config.get("file", "logs/dnaas.log")
            log_rotation = log_config.get("rotation", "10 MB")
            
            # 确保日志目录存在
            os.makedirs(os.path.dirname(log_file), exist_ok=True)
            
            # 配置loguru
            logger.remove()  # 移除默认处理器
            logger.add(sys.stdout, level=log_level)  # 控制台输出
            logger.add(log_file, level=log_level, rotation=log_rotation)  # 文件输出
        except Exception as e:
            logger.error(f"设置日志记录器失败: {e}")
            # 记录错误到以时间命名的日志文件
            log_exception("在GameAutoScript的_setup_logger方法中设置日志记录器时发生错误", "GameAutoScript")
    
    def start(self):
        """启动自动脚本"""
        logger.info("启动游戏自动脚本系统")
        self.running = True
        
        try:
            # 启动主循环
            self._main_loop()
        except KeyboardInterrupt:
            logger.info("接收到中断信号，正在停止...")
        except Exception as e:
            logger.error(f"运行时错误: {e}")
            # 记录错误到以时间命名的日志文件
            log_exception("在GameAutoScript的start方法中发生错误", "GameAutoScript")
        finally:
            self.stop()
    
    def stop(self):
        """停止自动脚本"""
        logger.info("停止游戏自动脚本系统")
        self.running = False
    
    def _main_loop(self):
        """主循环"""
        while self.running:
            try:
                # 捕获屏幕
                screenshot = self.screen_capture.capture()
                
                # 在这里添加具体的游戏逻辑
                # 例如：识别特定图像并执行相应操作
                
                # 控制循环频率
                time.sleep(self.config["screen"]["capture_interval"])
            except Exception as e:
                logger.error(f"主循环错误: {e}")
                # 记录错误到以时间命名的日志文件
                log_exception("在GameAutoScript的主循环中发生错误", "GameAutoScript")
                time.sleep(1)  # 出错时等待1秒再继续


if __name__ == "__main__":
    # 创建并启动自动脚本
    auto_script = GameAutoScript()
    auto_script.start()