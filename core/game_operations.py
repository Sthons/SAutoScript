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
        self.click_count = {}
        self.last_positions = {}
        
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
                logger.warning("屏幕捕获失败，重试中...")
                time.sleep(interval)
                continue
            
            # 查找模板
            result = self.image_recognition.find_template(screenshot, template_name, threshold)
            
            if result and result.get("found", False):
                logger.debug(f"找到模板: {template_name}，位置: {result['position']}")
                return result
            
            # 等待指定间隔
            time.sleep(interval)
        
        logger.warning(f"等待模板出现超时: {template_name}")
        return {"found": False, "template_name": template_name}
    
    def disappear(self, template_name, timeout=None, interval=None, threshold=None):
        """等待图像消失，返回是否成功
        
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
                logger.warning("屏幕捕获失败，重试中...")
                time.sleep(interval)
                continue
            
            # 查找模板
            result = self.image_recognition.find_template(screenshot, template_name, threshold)
            
            if not result or not result.get("found", False):
                logger.debug(f"模板已消失: {template_name}")
                return True
            
            # 等待指定间隔
            time.sleep(interval)
        
        logger.warning(f"等待模板消失超时: {template_name}")
        return False
    
    def appear_then_click(self, template_name, button="left", clicks=1, timeout=None, interval=None, threshold=None, click_delay=None):
        """等待图像出现并点击，返回是否成功
        
        Args:
            template_name: 模板图像名称
            button: 鼠标按钮，默认为左键
            clicks: 点击次数，默认为1次
            timeout: 超时时间(秒)，None表示使用默认值
            interval: 检查间隔(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            click_delay: 点击后延迟(秒)，None表示使用默认值
            
        Returns:
            bool: 是否成功点击
        """
        # 等待图像出现
        result = self.appear(template_name, timeout, interval, threshold)
        
        if not result.get("found", False):
            logger.warning(f"模板未出现，无法点击: {template_name}")
            return False
        
        # 获取位置
        x, y = result["position"]
        
        # 检查点击次数
        if self.input_controller.overlimit_detection:
            self._check_click_count(template_name)
        
        # 点击
        success = self.input_controller.click(x, y, button, clicks)
        
        if success:
            # 更新点击计数
            self.click_count[template_name] = self.click_count.get(template_name, 0) + clicks
            # 记录最后位置
            self.last_positions[template_name] = (x, y)
            logger.debug(f"成功点击模板: {template_name}，位置: ({x}, {y})")
            
            # 点击后延迟
            if click_delay is not None:
                time.sleep(click_delay)
        
        return success
    
    def appear_then_drag(self, template_name, end_x, end_y, button="left", timeout=None, interval=None, threshold=None):
        """等待图像出现并拖动到指定位置，返回是否成功
        
        Args:
            template_name: 模板图像名称
            end_x: 目标X坐标
            end_y: 目标Y坐标
            button: 鼠标按钮，默认为左键
            timeout: 超时时间(秒)，None表示使用默认值
            interval: 检查间隔(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            
        Returns:
            bool: 是否成功拖动
        """
        # 等待图像出现
        result = self.appear(template_name, timeout, interval, threshold)
        
        if not result.get("found", False):
            logger.warning(f"模板未出现，无法拖动: {template_name}")
            return False
        
        # 获取位置
        x, y = result["position"]
        
        # 拖动
        success = self.input_controller.drag(x, y, end_x, end_y)
        
        if success:
            logger.debug(f"成功拖动模板: {template_name}，从({x}, {y})到({end_x}, {end_y})")
        
        return success
    
    def appear_then_type(self, template_name, text, interval=0.01, timeout=None, check_interval=None, threshold=None):
        """等待图像出现并输入文本，返回是否成功
        
        Args:
            template_name: 模板图像名称
            text: 要输入的文本
            interval: 输入间隔(秒)
            timeout: 超时时间(秒)，None表示使用默认值
            check_interval: 检查间隔(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            
        Returns:
            bool: 是否成功输入文本
        """
        # 等待图像出现
        result = self.appear(template_name, timeout, check_interval, threshold)
        
        if not result.get("found", False):
            logger.warning(f"模板未出现，无法输入文本: {template_name}")
            return False
        
        # 获取位置
        x, y = result["position"]
        
        # 点击以激活输入框
        self.input_controller.click(x, y)
        
        # 输入文本
        success = self.input_controller.typewrite(text, interval)
        
        if success:
            logger.debug(f"成功在模板位置输入文本: {template_name}，文本: {text}")
        
        return success
    
    def appear_then_hotkey(self, template_name, *keys, timeout=None, interval=None, threshold=None):
        """等待图像出现并按下组合键，返回是否成功
        
        Args:
            template_name: 模板图像名称
            keys: 组合键列表
            timeout: 超时时间(秒)，None表示使用默认值
            interval: 检查间隔(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            
        Returns:
            bool: 是否成功按下组合键
        """
        # 等待图像出现
        result = self.appear(template_name, timeout, interval, threshold)
        
        if not result.get("found", False):
            logger.warning(f"模板未出现，无法按下组合键: {template_name}")
            return False
        
        # 按下组合键
        success = self.input_controller.hotkey(*keys)
        
        if success:
            logger.debug(f"成功按下组合键: {' + '.join(keys)}，当模板出现: {template_name}")
        
        return success
    
    def wait_and_click(self, template_name, button="left", clicks=1, timeout=None, interval=None, threshold=None):
        """等待图像出现并点击，与appear_then_click功能相同，提供更直观的名称
        
        Args:
            template_name: 模板图像名称
            button: 鼠标按钮，默认为左键
            clicks: 点击次数，默认为1次
            timeout: 超时时间(秒)，None表示使用默认值
            interval: 检查间隔(秒)，None表示使用默认值
            threshold: 匹配阈值，None表示使用默认值
            
        Returns:
            bool: 是否成功点击
        """
        return self.appear_then_click(template_name, button, clicks, timeout, interval, threshold)
    
    def reset_click_count(self, template_name=None):
        """重置点击计数
        
        Args:
            template_name: 模板名称，None表示重置所有
        """
        if template_name is None:
            self.click_count.clear()
            self.last_positions.clear()
            logger.debug("已重置所有模板的点击计数")
        else:
            if template_name in self.click_count:
                del self.click_count[template_name]
            if template_name in self.last_positions:
                del self.last_positions[template_name]
            logger.debug(f"已重置模板的点击计数: {template_name}")
    
    def _check_click_count(self, template_name):
        """检查点击次数，防止无限点击
        
        Args:
            template_name: 模板名称
            
        Raises:
            GameTooManyClickError: 点击次数过多
            GameStuckError: 可能卡死
        """
        count = self.click_count.get(template_name, 0)
        
        # 检查点击次数是否过多
        if count >= self.max_clicks:
            raise GameTooManyClickError(f"模板 {template_name} 点击次数过多: {count}")
        
        # 检查是否可能卡死
        if count >= self.stuck_threshold:
            # 检查位置是否变化
            current_pos = self.last_positions.get(template_name)
            if current_pos:
                # 捕获屏幕
                screenshot = self.screen_capture.capture()
                if screenshot is not None:
                    result = self.image_recognition.find_template(screenshot, template_name)
                    if result and result.get("found", False):
                        new_pos = result["position"]
                        # 如果位置没有变化，可能卡死
                        if new_pos == current_pos:
                            raise GameStuckError(f"模板 {template_name} 可能卡死，位置未变化: {new_pos}")


    def back(self):
        """
        返回上一级
        """
        return self.input_controller.key_press('esc')