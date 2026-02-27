# -*- coding: utf-8 -*-

"""
SAutoScript 核心模块
"""

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
