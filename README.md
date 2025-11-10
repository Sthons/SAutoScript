# DNAAS - 游戏自动脚本系统

基于图像识别技术的动作游戏自动脚本系统，支持Windows平台的鼠标键盘仿真输入。

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
DNAAS/
├── main.py              # 主程序入口
├── config/              # 配置文件目录
│   └── settings.yaml    # 全局配置
├── core/                # 核心功能模块
│   ├── image_recognition.py  # 图像识别模块
│   ├── input_controller.py   # 输入控制模块
│   └── screen_capture.py     # 屏幕捕获模块
├── scripts/             # 游戏脚本目录
│   └── example.py       # 示例脚本
├── assets/              # 资源目录
│   └── templates/       # 图像模板
└── logs/                # 日志目录
```

## 快速开始

1. 安装依赖
2. 运行主程序：`python main.py`
3. 根据提示配置游戏脚本

## 核心库说明

- **OpenCV**: 用于图像识别和模板匹配
- **pyautogui**: 提供跨平台的鼠标键盘控制
- **pywin32**: 直接调用Windows API，提供更底层的控制
- **pywinauto**: Windows应用程序自动化工具
- **pynput**: 监听和控制输入设备
- **mss**: 高性能屏幕捕获

## 注意事项

- 运行脚本时请确保游戏窗口处于活动状态
- 某些游戏可能有反作弊机制，使用自动脚本需谨慎
- 建议在测试环境中先验证脚本功能