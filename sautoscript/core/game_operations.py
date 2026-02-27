#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
from loguru import logger


class GameStuckError(Exception):
    """游戏卡死异常，当检测到游戏可能卡死时抛出"""
    pass


class GameTooManyClickError(Exception):
    """点击次数过多异常，当检测到可能陷入无限点击循环时抛出"""
    pass


class GameOperations:
    """游戏操作模块，实现基于图像识别的循环模式，替代sleep()语句"""
    
    def __init__(self, image_recognition, input_controller, screen_capture, config=None):
        self.image_recognition = image_recognition
        self.input_controller = input_controller
        self.screen_capture = screen_capture
        self.config = config or {}
        
        # 默认配置
        self.default_timeout = self.config.get("default_timeout", 30)  # 默认超时时间(秒)
        self.default_interval = self.config.get("default_interval", 0.1)  # 默认检查间隔(秒)
        self.max_clicks = self.config.get("max_clicks", 10)  # 最大点击次数
        self.stuck_threshold = self.config.get("stuck_threshold", 5)  # 卡死检测阈值
        
        # 状态跟踪
        self.click_count = {}  # 记录每个模板的点击次数
        self.last_positions = {}  # 记录上次点击的位置，用于检测卡死
        
        logger.info("游戏操作模块初始化完成")
    
    def appear(self, template_name, timeout=None, interval=None, threshold=None):
        """等待图像出现，返回匹配结果
        
        Args:
            template_name: 模板图像名称
            timeout: 超时时间(秒)，None表示使用默认值
            interval: 检查间隔(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            
        Returns:
            匹配结果字典，包含found、position等信息
        """
        timeout = timeout if timeout is not None else self.default_timeout
        interval = interval if interval is not None else self.default_interval
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 捕获屏幕
            screenshot = self.screen_capture.capture()
            if screenshot is None:
                time.sleep(interval)
                continue
            
            # 查找模板
            result = self.image_recognition.find_template(screenshot, template_name, threshold)
            if result["found"]:
                logger.debug(f"图像 {template_name} 出现")
                return result
            
            time.sleep(interval)
        
        logger.debug(f"超时：未找到图像 {template_name}")
        return {"found": False}
    
    def disappear(self, template_name, timeout=None, interval=None, threshold=None):
        """等待图像消失
        
        Args:
            template_name: 模板图像名称
            timeout: 超时时间(秒)，None表示使用默认值
            interval: 检查间隔(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            
        Returns:
            bool: 图像是否消失
        """
        timeout = timeout if timeout is not None else self.default_timeout
        interval = interval if interval is not None else self.default_interval
        
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 捕获屏幕
            screenshot = self.screen_capture.capture()
            if screenshot is None:
                time.sleep(interval)
                continue
            
            # 查找模板
            result = self.image_recognition.find_template(screenshot, template_name, threshold)
            if not result["found"]:
                logger.debug(f"图像 {template_name} 消失")
                return True
            
            time.sleep(interval)
        
        logger.debug(f"超时：图像 {template_name} 未消失")
        return False
    
    def appear_then_click(self, template_name, timeout=None, threshold=None, click_delay=0.5):
        """等待图像出现并点击
        
        Args:
            template_name: 模板图像名称
            timeout: 超时时间(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            click_delay: 点击后的延迟时间(秒)
            
        Returns:
            bool: 是否成功点击
        """
        # 等待图像出现
        result = self.appear(template_name, timeout, threshold=threshold)
        
        if result["found"]:
            # 检查点击次数，防止无限点击
            if template_name not in self.click_count:
                self.click_count[template_name] = 0
            
            self.click_count[template_name] += 1
            
            if self.click_count[template_name] > self.max_clicks:
                logger.error(f"点击次数过多: {template_name}")
                raise GameTooManyClickError(f"模板 {template_name} 点击次数超过限制")
            
            # 检查是否卡死（位置没有变化）
            if template_name in self.last_positions:
                last_pos = self.last_positions[template_name]
                current_pos = result["position"]
                
                if abs(last_pos[0] - current_pos[0]) < 5 and abs(last_pos[1] - current_pos[1]) < 5:
                    # 位置基本没变，可能卡死了
                    self.click_count[template_name] += 1
                    if self.click_count[template_name] > self.stuck_threshold:
                        logger.error(f"游戏可能卡死: {template_name}")
                        raise GameStuckError(f"模板 {template_name} 可能导致游戏卡死")
            
            # 更新上次点击位置
            self.last_positions[template_name] = result["position"]
            
            # 点击图像位置
            x, y = result["position"]
            self.input_controller.click(x, y)
            
            # 点击后延迟
            time.sleep(click_delay)
            
            logger.debug(f"点击图像 {template_name} 位置: ({x}, {y})")
            return True
        
        return False
    
    def click_at(self, x, y, button='left', clicks=1, interval=0.0):
        """点击指定坐标
        
        Args:
            x: x坐标
            y: y坐标
            button: 鼠标按钮，默认左键
            clicks: 点击次数
            interval: 点击间隔
            
        Returns:
            bool: 是否成功点击
        """
        return self.input_controller.click(x, y, button, clicks, interval)
    
    def drag(self, start_x, start_y, end_x, end_y, duration=0.5):
        """拖拽操作
        
        Args:
            start_x: 起始x坐标
            start_y: 起始y坐标
            end_x: 结束x坐标
            end_y: 结束y坐标
            duration: 拖拽持续时间
            
        Returns:
            bool: 是否成功拖拽
        """
        return self.input_controller.drag(start_x, start_y, end_x, end_y, duration)
    
    def scroll(self, x, y, clicks=1, direction='down'):
        """滚动操作
        
        Args:
            x: x坐标
            y: y坐标
            clicks: 滚动次数
            direction: 滚动方向，'up'或'down'
            
        Returns:
            bool: 是否成功滚动
        """
        return self.input_controller.scroll(x, y, clicks, direction)
    
    def press_key(self, key, press_duration=0.1):
        """按键操作
        
        Args:
            key: 按键名称
            press_duration: 按键持续时间
            
        Returns:
            bool: 是否成功按键
        """
        return self.input_controller.key_press(key, press_duration=press_duration)
    
    def hotkey(self, *keys):
        """组合键操作
        
        Args:
            *keys: 按键名称列表
            
        Returns:
            bool: 是否成功按下组合键
        """
        return self.input_controller.hotkey(*keys)
    
    def type_text(self, text, interval=0.1):
        """输入文本
        
        Args:
            text: 要输入的文本
            interval: 字符间隔时间
            
        Returns:
            bool: 是否成功输入文本
        """
        return self.input_controller.typewrite(text, interval)
    
    def reset_click_count(self, template_name=None):
        """重置点击计数
        
        Args:
            template_name: 模板名称，如果为None则重置所有模板的点击计数
        """
        if template_name:
            if template_name in self.click_count:
                del self.click_count[template_name]
                logger.debug(f"重置模板 {template_name} 的点击计数")
        else:
            self.click_count.clear()
            logger.debug("重置所有模板的点击计数")
    
    def reset_last_positions(self, template_name=None):
        """重置上次点击位置
        
        Args:
            template_name: 模板名称，如果为None则重置所有模板的上次点击位置
        """
        if template_name:
            if template_name in self.last_positions:
                del self.last_positions[template_name]
                logger.debug(f"重置模板 {template_name} 的上次点击位置")
        else:
            self.last_positions.clear()
            logger.debug("重置所有模板的上次点击位置")
