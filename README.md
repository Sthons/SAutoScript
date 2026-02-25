# SAutoScript - 游戏自动脚本系统

基于图像识别技术的游戏自动脚本系统（支持使用DirectX的游戏），支持Windows平台的鼠标键盘仿真输入。

## 功能特点

- 基于OpenCV的图像识别和模板匹配
- 直接调用Windows API的鼠标键盘控制
- 可配置的脚本系统
- 实时屏幕捕获和分析
- 多线程处理，提高响应速度

## 安装依赖

```bash
pip install -r requirements.txt
```

## 项目结构

```
SAutoScript/
├── .gitignore           # Git忽略文件
├── README.md            # 项目说明文档
├── install.py           # 安装脚本
├── requirements.txt     # 依赖包列表
├── config/              # 配置文件目录
│   └── settings.yaml    # 全局配置
├── core/                # 核心功能模块
│   ├── base_game_script.py     # 基础游戏脚本类
│   ├── error_logger.py         # 错误日志记录模块
│   ├── game_operations.py      # 游戏操作模块
│   ├── image_recognition.py    # 图像识别模块
│   ├── input_controller.py     # 输入控制模块
│   ├── screen_capture.py       # 屏幕捕获模块
│   └── window_locator.py       # 窗口定位模块
├── docs/                # 文档目录
│   ├── BaseGameScript_Guide.md  # BaseGameScript 使用指南
│   └── Error_Logging_Guide.md   # 错误日志记录指南
└── logs/                # 日志目录
```

## 快速开始

1. 安装依赖：`pip install -r requirements.txt`
2. 运行安装脚本：`python install.py`
3. 根据提示配置游戏脚本

## 核心模块说明

### 核心功能模块

- **base_game_script.py**: 游戏脚本基类，所有游戏脚本都应继承此类，实现通用的初始化、配置加载和主循环功能。子类需要实现game_logic方法来定义具体的游戏逻辑。
- **error_logger.py**: 错误日志记录器，用于在发生错误时将完整的错误信息保存到以时间命名的日志文件中，便于调试和问题定位。
- **game_operations.py**: 游戏操作模块，实现基于图像识别的循环模式，替代sleep()语句，提供等待图像出现、消失、点击等功能，并包含游戏卡死和点击次数过多的异常处理。
- **image_recognition.py**: 图像识别模块，包含NumpyArrayPool类用于减少内存分配和释放的开销，提高图像处理性能。
- **input_controller.py**: 输入控制模块，负责处理鼠标和键盘的仿真输入，支持多种输入方式和配置选项。
- **screen_capture.py**: 屏幕捕获模块，负责高效地捕获屏幕内容，支持多种捕获方法（mss、PIL、pyautogui）和质量设置。
- **window_locator.py**: 窗口定位模块，用于获取窗口位置和大小，支持根据窗口标题、类名或句柄查找窗口。

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

- **BaseGameScript 使用指南** (`docs/BaseGameScript_Guide.md`): 详细介绍如何使用 BaseGameScript 基类创建游戏自动化脚本，包括核心功能、使用方法和最佳实践。
- **错误日志记录指南** (`docs/Error_Logging_Guide.md`): 介绍项目的错误日志记录功能，包括如何查看和分析错误日志，以及如何在自定义脚本中集成错误记录。

## 注意事项

- 运行脚本时请确保游戏窗口处于活动状态
- 某些游戏可能有反作弊机制，使用自动脚本需谨慎
- 建议在测试环境中先验证脚本功能