# -*- coding: utf-8 -*-

"""
SAutoScript - 游戏自动脚本系统
基于图像识别技术的动作游戏自动脚本系统，支持Windows平台的鼠标键盘仿真输入。
"""

__version__ = "0.1.1"
__author__ = "SAutoScript Team"
__license__ = "MIT"

from sautoscript.core.base_game_script import BaseGameScript
from sautoscript.core.input_controller import InputController
from sautoscript.core.screen_capture import ScreenCapture
from sautoscript.core.image_recognition import ImageRecognition
from sautoscript.core.game_operations import GameOperations
from sautoscript.core.window_locator import WindowLocator
from sautoscript.core.error_logger import log_exception

__all__ = [
    "BaseGameScript",
    "InputController",
    "ScreenCapture",
    "ImageRecognition",
    "GameOperations",
    "WindowLocator",
    "log_exception"
]
