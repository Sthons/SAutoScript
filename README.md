# SAutoScript - 游戏自动脚本系统

基于图像识别技术的动作游戏自动脚本系统（支持使用DirectX的游戏），支持Windows平台的鼠标键盘仿真输入。

## 功能特点

- 基于OpenCV的图像识别和模板匹配
- 直接调用Windows API的鼠标键盘控制
- 可配置的脚本系统
- 实时屏幕捕获和分析
- 多线程处理，提高响应速度
- 智能内存优化和垃圾回收
- 随机事件支持
- 完善的错误日志记录

## 安装

### 从 PyPI 安装

```bash
pip install SAutoScript
```

### 从源码安装

```bash
# 克隆仓库
git clone https://github.com/Sthons/SAutoScript.git
cd SAutoScript

# 安装依赖
pip install -r requirements.txt

# 安装包
pip install -e .
```

## 项目结构

```
SAutoScript/
├── sautoscript/          # 主要包目录
│   ├── __init__.py       # 包初始化文件
│   └── core/             # 核心模块
│       ├── __init__.py
│       ├── base_game_script.py     # 基础游戏脚本类
│       ├── error_logger.py         # 错误日志记录模块
│       ├── game_operations.py      # 游戏操作模块
│       ├── image_recognition.py    # 图像识别模块
│       ├── input_controller.py     # 输入控制模块
│       ├── screen_capture.py       # 屏幕捕获模块
│       └── window_locator.py       # 窗口定位模块
├── examples/              # 示例脚本
│   └── example.py         # 使用示例
├── assets/                # 资源目录
│   └── templates/         # 图像模板
├── config/                # 配置文件目录
│   └── settings.yaml      # 全局配置
├── docs/                  # 文档目录
├── logs/                  # 日志目录
├── pyproject.toml         # 项目配置
├── setup.cfg              # 安装配置
├── setup.py               # 安装脚本
├── README.md              # 项目说明
├── LICENSE                # 许可证
└── requirements.txt       # 依赖包列表
```

## 快速开始

### 基本使用

```python
from sautoscript import BaseGameScript

class MyGameScript(BaseGameScript):
    def game_logic(self):
        # 捕获屏幕
        screenshot = self.screen_capture.capture()
        
        if screenshot is None:
            return
        
        # 查找并点击特定图像
        if self.game_ops.appear_then_click(
            "target_button",  # 模板名称
            timeout=3,        # 超时时间(秒)
            threshold=0.8,    # 匹配阈值
            click_delay=0.5   # 点击后延迟
        ):
            self.success_num += 1

if __name__ == "__main__":
    script = MyGameScript()
    script.start()
```

### 运行示例

```bash
python examples/example.py
```

## 核心模块说明

### 核心功能模块

- **base_game_script.py**: 游戏脚本基类，所有游戏脚本都应继承此类，实现通用的初始化、配置加载和主循环功能
- **error_logger.py**: 错误日志记录器，用于保存完整的错误信息到日志文件
- **game_operations.py**: 游戏操作模块，实现基于图像识别的循环模式
- **image_recognition.py**: 图像识别模块，包含NumpyArrayPool类提高性能
- **input_controller.py**: 输入控制模块，处理鼠标和键盘的仿真输入
- **screen_capture.py**: 屏幕捕获模块，支持多种捕获方法和质量设置
- **window_locator.py**: 窗口定位模块，用于获取窗口位置和大小

### 依赖库

- **OpenCV**: 用于图像识别和模板匹配
- **pyautogui**: 提供跨平台的鼠标键盘控制
- **pywin32**: 直接调用Windows API，提供更底层的控制
- **pydirectinput**: 基于**pywin32**，针对使用**DirectX**的游戏特化
- **mss**: 高性能屏幕捕获
- **PIL (Pillow)**: 图像处理和屏幕捕获
- **loguru**: 高级日志记录
- **pyyaml**: 配置文件解析
- **psutil**: 系统资源监控（用于内存监控）

## 文档

项目提供了详细的使用文档，帮助您快速上手：

- **BaseGameScript 使用指南** (`https://github.com/Sthons/SAutoScript/blob/dev/docs/BaseGameScript_Guide.md`): 详细介绍如何使用 BaseGameScript 基类创建游戏自动化脚本，包括核心功能、使用方法和最佳实践。
- **错误日志记录指南** (`https://github.com/Sthons/SAutoScript/blob/dev/docs/Error_Logging_Guide.md`): 介绍项目的错误日志记录功能，包括如何查看和分析错误日志，以及如何在自定义脚本中集成错误记录。

## 注意事项

- 运行脚本时请确保游戏窗口处于活动状态
- 某些游戏可能有反作弊机制，使用自动脚本需谨慎
- 建议在测试环境中先验证脚本功能
- 在Windows上，建议以管理员权限运行脚本，以确保输入控制功能正常工作

## 许可证

MIT License - 详见 LICENSE 文件
