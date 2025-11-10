# BaseGameScript 使用指南

## 概述

`BaseGameScript` 是一个基础游戏脚本类，提供了创建游戏自动化脚本所需的核心功能。通过继承这个基类，您可以快速开发自己的游戏脚本，而无需重复实现常见的功能。

## 主要功能

- 配置文件加载和管理
- 核心组件初始化（图像识别、输入控制、屏幕捕获）
- 主循环管理
- 游戏操作封装（点击、等待、键盘输入等）
- 模板创建和管理
- 测试模式支持

## 如何使用

### 1. 创建新脚本

创建一个新的Python文件，继承`BaseGameScript`类：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from loguru import logger

# 添加核心模块路径
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'core'))

from base_game_script import BaseGameScript

class MyGameScript(BaseGameScript):
    """自定义游戏脚本"""
    
    def __init__(self, config_path=None):
        # 调用父类初始化方法
        super().__init__(config_path)
        
        # 设置循环次数和延迟
        self.max_loops = 50  # 最多执行50次循环
        self.loop_delay = 1  # 循环间隔1秒
        
        # 添加自定义属性
        self.custom_counter = 0
        
        logger.info("自定义游戏脚本初始化完成")
    
    def game_logic(self):
        """
        实现具体的游戏逻辑
        
        这个方法会在主循环中被调用，每次调用代表一次游戏操作
        """
        # 捕获屏幕
        screenshot = self.screen_capture.capture()
        
        if screenshot is None:
            logger.warning("屏幕捕获失败，跳过本次循环")
            return
        
        # 示例：查找并点击特定图像
        if self.game_ops.appear_then_click(
            "target_button",  # 模板名称
            timeout=3,        # 超时时间(秒)
            threshold=0.8,    # 匹配阈值
            click_delay=0.5   # 点击后延迟
        ):
            logger.info("成功点击目标按钮")
            self.custom_counter += 1
        else:
            logger.info("未找到目标按钮")
```

### 2. 实现必要方法

#### game_logic() 方法

这是必须实现的方法，包含您的游戏逻辑。它会在主循环中被重复调用，直到达到最大循环次数或手动停止。

```python
def game_logic(self):
    """
    实现具体的游戏逻辑
    """
    # 捕获屏幕
    screenshot = self.screen_capture.capture()
    
    if screenshot is None:
        logger.warning("屏幕捕获失败，跳过本次循环")
        return
    
    # 您的游戏逻辑代码
    # ...
```

### 3. 可选重写方法

#### on_start() 方法

在脚本启动前执行，可以用于初始化游戏状态或执行其他准备工作：

```python
def on_start(self):
    """
    启动前钩子
    """
    logger.info("执行启动前操作...")
    
    # 示例：确保游戏窗口处于前台
    self.input_controller.press_key('esc')  # 按ESC键确保游戏窗口激活
    
    # 示例：等待游戏加载
    if self.game_ops.appear(
        "game_logo",  # 游戏标志模板
        timeout=10,    # 超时时间(秒)
        threshold=0.8  # 匹配阈值
    ):
        logger.info("游戏已加载")
    else:
        logger.warning("游戏未加载，但继续执行")
```

#### on_stop() 方法

在脚本停止后执行，可以用于清理资源或执行其他收尾工作：

```python
def on_stop(self):
    """
    停止后钩子
    """
    logger.info("执行停止后操作...")
    
    # 示例：保存游戏状态
    self.input_controller.hotkey('ctrl', 's')  # 保存游戏
    
    # 示例：记录统计信息
    logger.info(f"脚本执行完成，共执行了{self.custom_counter}次特殊操作")
```

### 4. 运行脚本

#### 正常模式

```python
if __name__ == "__main__":
    # 创建脚本实例
    script = MyGameScript()
    
    # 启动脚本
    script.start()
```

#### 测试模式

```python
if __name__ == "__main__":
    # 检查命令行参数
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # 测试模式
        logger.info("运行测试模式...")
        
        script = MyGameScript()
        
        # 测试输入控制
        script.test_input_controls()
        
        # 测试模板创建
        script.create_template_from_screenshot(
            (100, 100, 200, 50),  # 区域 (x, y, width, height)
            "test_template.png"    # 模板文件名
        )
        
        # 运行测试模式
        script.run_test_mode()
    else:
        # 正常模式
        script = MyGameScript()
        script.start()
```

## 可用属性和方法

### 核心组件

- `self.config`: 配置字典
- `self.screen_capture`: 屏幕捕获对象
- `self.input_controller`: 输入控制对象
- `self.image_recognition`: 图像识别对象
- `self.game_ops`: 游戏操作对象

### 主要方法

- `start()`: 启动脚本
- `stop()`: 停止脚本
- `test_input_controls()`: 测试输入控制
- `create_template_from_screenshot(region, filename)`: 从屏幕截图创建模板
- `run_test_mode()`: 运行测试模式

### 游戏操作方法

通过`self.game_ops`对象，您可以使用以下方法：

- `appear(template_name, timeout=5, threshold=0.8)`: 等待图像出现
- `disappear(template_name, timeout=5, threshold=0.8)`: 等待图像消失
- `appear_then_click(template_name, timeout=5, threshold=0.8, click_delay=0.5)`: 等待图像出现并点击
- `click_at(x, y, button='left', clicks=1, interval=0.0)`: 点击指定坐标
- `drag(start_x, start_y, end_x, end_y, duration=0.5)`: 拖拽操作
- `scroll(x, y, clicks=1, direction='down')`: 滚动操作
- `press_key(key, press_duration=0.1)`: 按键操作
- `hotkey(*keys)`: 组合键操作
- `type_text(text, interval=0.1)`: 输入文本

## 配置

脚本会自动加载`config/settings.yaml`配置文件。您也可以在初始化时指定自定义配置路径：

```python
script = MyGameScript("path/to/your/config.yaml")
```

## 示例

完整示例请参考：
- `scripts/example.py`: 使用BaseGameScript重写的示例脚本
- `scripts/template_example.py`: 展示如何使用BaseGameScript的详细示例

## 最佳实践

1. **合理设置循环次数和延迟**：避免过度占用CPU资源
2. **使用适当的超时和阈值**：提高图像识别的可靠性
3. **添加日志记录**：便于调试和监控脚本运行状态
4. **处理异常情况**：确保脚本在遇到错误时能够优雅地退出
5. **使用测试模式**：在正式运行前测试脚本功能

## 常见问题

### Q: 如何添加自定义配置？

A: 您可以在`config/settings.yaml`中添加自定义配置项，然后在脚本中通过`self.config`访问它们。

### Q: 如何处理游戏窗口定位？

A: 可以使用`WindowLocator`类来定位和操作游戏窗口：

```python
from window_locator import WindowLocator

# 在初始化中添加
self.window_locator = WindowLocator()

# 在游戏逻辑中使用
rect = self.window_locator.get_window_rect("游戏窗口标题")
if rect:
    x, y, width, height = rect
    # 使用窗口位置信息
```

### Q: 如何创建图像模板？

A: 可以使用`create_template_from_screenshot`方法从屏幕截图创建模板，或者手动截取游戏界面图像并保存到`templates`目录。

```python
# 创建模板
script.create_template_from_screenshot(
    (100, 100, 200, 50),  # 区域 (x, y, width, height)
    "my_template.png"     # 模板文件名
)
```

## 总结

`BaseGameScript`提供了一个强大而灵活的基础框架，使您能够专注于实现游戏逻辑，而不必担心底层细节。通过继承这个基类，您可以快速创建可靠的游戏自动化脚本。