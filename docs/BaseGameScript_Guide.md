# BaseGameScript 使用指南

## 概述

`BaseGameScript` 是一个基础游戏脚本类，提供了创建游戏自动化脚本所需的核心功能。通过继承这个基类，您可以快速开发自己的游戏脚本，而无需重复实现常见的功能。

## 主要功能

- 配置文件加载和管理
- 核心组件初始化（图像识别、输入控制、屏幕捕获、窗口定位）
- 主循环管理
- 游戏操作封装（点击、等待、键盘输入等）
- 模板创建和管理
- 测试模式支持
- 智能内存优化和垃圾回收
- 随机事件支持
- 成功执行次数统计

## 如何使用

### 1. 创建新脚本

创建一个新的Python文件，继承`BaseGameScript`类：

```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from loguru import logger
from sautoscript import BaseGameScript

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
    self.input_controller.key_press('esc')  # 按ESC键确保游戏窗口激活
    
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

#### random_event() 方法

在脚本中实现随机事件，可以用于模拟真实玩家的随机行为：

```python
def random_event(self):
    """
    随机事件，子类可以重写此方法来实现随机事件
    """
    import random
    
    # 随机选择事件类型
    random_type = random.choice(["jump", "left_right", "squat_down"])
    
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
```

在游戏逻辑中调用随机事件：

```python
def game_logic(self):
    # 执行主要游戏逻辑
    
    # 随机触发随机事件（例如每10次循环触发一次）
    if random.random() < 0.1:
        self.random_event()
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
- `self.window_locator`: 窗口定位对象
- `self.running`: 运行状态标志
- `self.success_num`: 成功执行次数
- `self.max_loops`: 最大循环次数
- `self.loop_delay`: 循环间隔时间（秒）

### 内存优化配置

BaseGameScript 内置了智能内存优化功能，可通过配置文件进行设置：

- `gc_frequency`: 垃圾回收频率（默认：50次循环）
- `memory_threshold_mb`: 内存阈值（MB，默认：400MB）
- `enable_smart_gc`: 启用智能垃圾回收（默认：true）
- `enable_memory_monitoring`: 启用内存监控（默认：true）
- `memory_check_frequency`: 内存检查频率（默认：20次循环）

配置示例（`config/settings.yaml`）：

```yaml
loop_control:
  max_iterations: 100
  iteration_delay: 1

memory_optimization:
  gc_frequency: 50
  memory_threshold_mb: 400
  enable_smart_gc: true
  enable_memory_monitoring: true
  memory_check_frequency: 20
```

### 主要方法

- `start(max_loops=None, loop_delay=None)`: 启动脚本，可指定最大循环次数和循环延迟
- `stop()`: 停止脚本
- `create_template_from_screenshot(region, filename)`: 从屏幕截图创建模板
- `random_event()`: 随机事件，子类可重写实现自定义随机行为

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

### 输入控制方法

通过`self.input_controller`对象，您可以使用以下方法：

#### 鼠标控制
- `set_mouse_position(x, y, delay=None, duration=None)`: 设置鼠标位置
- `move_mouse(x, y, duration=None)`: 移动鼠标到指定位置
- `click(x=None, y=None, button="left", clicks=1, interval=0.2, duration=0.2)`: 点击鼠标
- `mouse_down(button="left")`: 按下鼠标按钮
- `mouse_up(button="left")`: 释放鼠标按钮
- `drag(start_x, start_y, end_x, end_y, duration=None)`: 拖动鼠标
- `scroll(x=None, y=None, clicks=1, direction="down")`: 滚动鼠标滚轮
- `get_mouse_position()`: 获取当前鼠标位置

#### 键盘控制
- `key_press(key, presses=1, interval=0.1)`: 按下键盘按键
- `key_down(key)`: 按下按键不释放
- `key_up(key)`: 释放按键
- `hotkey(*keys, interval=0.1)`: 按下组合键
- `typewrite(text, interval=0.05)`: 输入文本
- `is_key_pressed(key)`: 检查按键是否被按下

#### 窗口控制
- `get_active_window()`: 获取当前活动窗口信息
- `set_window_foreground(window_title=None, window_handle=None)`: 将指定窗口设置为前台窗口

#### 其他方法
- `get_screen_size()`: 获取屏幕尺寸（已废弃，多显示器设置不适用）
- `get_screen_shot()`: 获取屏幕截图

### 屏幕捕获方法

通过`self.screen_capture`对象，您可以使用以下方法：

- `capture()`: 捕获屏幕内容

### 窗口定位方法

通过`self.window_locator`对象（需要手动初始化），您可以使用以下方法：

- `get_window_rect(window_title=None, window_class=None, hwnd=None)`: 获取窗口的位置和大小

## 配置

脚本会自动加载`config/settings.yaml`配置文件。您也可以在初始化时指定自定义配置路径：

```python
script = MyGameScript("path/to/your/config.yaml")
```

### 配置项说明

#### 循环控制配置
```yaml
loop_control:
  max_iterations: 100  # 最大循环次数
  iteration_delay: 1   # 循环间隔（秒）
```

#### 内存优化配置
```yaml
memory_optimization:
  gc_frequency: 50              # 垃圾回收频率（每N次循环执行一次）
  memory_threshold_mb: 400      # 内存阈值（MB），超过时执行垃圾回收
  enable_smart_gc: true         # 启用智能垃圾回收
  enable_memory_monitoring: true # 启用内存监控
  memory_check_frequency: 20     # 内存检查频率（每N次循环检查一次）
```

#### 输入控制配置
```yaml
input_control:
  delay: 0.1              # 默认延迟（秒）
  use_delay: true         # 是否使用延迟
  move_duration: 0.2       # 鼠标移动持续时间（秒）
  click_duration: 0.1      # 鼠标点击持续时间（秒）
  key_duration: 0.05       # 键盘按键持续时间（秒）
  overlimit_detection: false # 是否开启超量识别检测
```

#### 屏幕捕获配置
```yaml
screen_capture:
  region: null          # 捕获区域，null表示全屏
  monitor: 0           # 显示器编号
  resolution: [1920, 1080]  # 分辨率
  use_delay: true       # 是否使用延迟
  capture_delay: 0.01   # 捕获延迟（秒）
  capture_method: "mss" # 捕获方法：mss、pil、pyautogui
  quality: "medium"     # 捕获质量：low、medium、high
```

#### 图像识别配置
```yaml
image_recognition:
  template_dir: "assets/templates"  # 模板目录
  default_threshold: 0.8           # 默认匹配阈值
```

## 示例

完整示例请参考：
- `scripts/example.py`: 使用BaseGameScript重写的示例脚本

## 最佳实践

1. **合理设置循环次数和延迟**：避免过度占用CPU资源
2. **使用适当的超时和阈值**：提高图像识别的可靠性
3. **添加日志记录**：便于调试和监控脚本运行状态
4. **处理异常情况**：确保脚本在遇到错误时能够优雅地退出
5. **使用测试模式**：在正式运行前测试脚本功能
6. **合理配置内存优化**：根据脚本复杂度和系统资源调整内存优化参数
7. **使用随机事件**：在需要模拟真实玩家行为时，合理使用随机事件功能
8. **监控成功执行次数**：通过 `self.success_num` 跟踪脚本执行效果
9. **正确使用输入控制方法**：根据游戏需求选择合适的输入控制方法（如 `key_press` vs `key_down/key_up`）
10. **窗口管理**：在脚本开始前确保游戏窗口处于前台状态

## 常见问题

### Q: 如何添加自定义配置？

A: 您可以在`config/settings.yaml`中添加自定义配置项，然后在脚本中通过`self.config`访问它们。

### Q: 如何处理游戏窗口定位？

A: 可以使用`WindowLocator`类来定位和操作游戏窗口：

```python
# 在游戏逻辑中使用
rect = self.window_locator.get_window_rect("游戏窗口标题")
if rect:
    x, y, width, height = rect
    # 使用窗口位置信息
```

或者使用输入控制器的窗口管理功能：

```python
# 获取当前活动窗口信息
window_info = self.input_controller.get_active_window()
logger.info(f"当前窗口: {window_info['title']}")

# 将指定窗口设置为前台窗口
self.input_controller.set_window_foreground("游戏窗口标题")
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

### Q: 如何优化内存使用？

A: BaseGameScript 内置了智能内存优化功能，您可以通过配置文件调整相关参数：

```yaml
memory_optimization:
  gc_frequency: 50              # 垃圾回收频率
  memory_threshold_mb: 400      # 内存阈值
  enable_smart_gc: true         # 启用智能垃圾回收
  enable_memory_monitoring: true # 启用内存监控
  memory_check_frequency: 20     # 内存检查频率
```

系统会自动在内存使用超过阈值时执行垃圾回收，并定期进行内存检查。

### Q: 如何使用随机事件功能？

A: 重写 `random_event()` 方法来实现自定义的随机行为：

```python
def random_event(self):
    import random
    
    # 随机选择事件类型
    random_type = random.choice(["jump", "move", "attack"])
    
    if random_type == "jump":
        self.input_controller.key_press('space')
    elif random_type == "move":
        self.input_controller.key_press('w')
    elif random_type == "attack":
        self.input_controller.key_press('e')
```

然后在游戏逻辑中调用：

```python
def game_logic(self):
    # 主要游戏逻辑
    
    # 随机触发事件（10%概率）
    if random.random() < 0.1:
        self.random_event()
```

### Q: 如何跟踪脚本执行效果？

A: 使用 `self.success_num` 属性来跟踪成功执行的次数：

```python
def game_logic(self):
    if self.game_ops.appear_then_click("target"):
        self.success_num += 1
        logger.info(f"成功执行次数: {self.success_num}")
```

脚本会在每次循环和停止时显示执行统计信息。

### Q: 如何选择合适的输入控制方法？

A: 根据具体需求选择：

- `key_press(key)`: 用于单次按键（如按下空格键跳跃）
- `key_down(key)` + `key_up(key)`: 用于长按按键（如按住W键移动）
- `hotkey('ctrl', 's')`: 用于组合键操作
- `typewrite(text)`: 用于输入文本
- `move_mouse(x, y, duration=None)`: 用于鼠标移动
- `click(x, y)`: 用于鼠标点击
- `drag(start_x, start_y, end_x, end_y)`: 用于拖拽操作

## 总结

`BaseGameScript`提供了一个强大而灵活的基础框架，使您能够专注于实现游戏逻辑，而不必担心底层细节。通过继承这个基类，您可以快速创建可靠的游戏自动化脚本。