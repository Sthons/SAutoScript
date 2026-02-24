#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import subprocess
import platform
import logging

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger(__name__)


def check_python_version():
    """检查Python版本"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        logger.error(f"Python版本过低: {version.major}.{version.minor}，需要Python 3.10 或更高版本")
        return False
    
    logger.info(f"Python版本检查通过: {version.major}.{version.minor}.{version.micro}")
    return True


def create_virtual_environment():
    """创建虚拟环境"""
    venv_path = os.path.join(os.path.dirname(__file__), ".venv")
    
    # 检查虚拟环境是否已存在
    if os.path.exists(venv_path):
        logger.info("虚拟环境已存在")
        return True
    
    logger.info("正在创建虚拟环境...")
    
    try:
        # 创建虚拟环境
        subprocess.check_call([sys.executable, "-m", "venv", venv_path])
        logger.info(f"虚拟环境创建成功: {venv_path}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"创建虚拟环境失败: {e}")
        return False


def get_venv_python():
    """获取虚拟环境中的Python路径"""
    venv_path = os.path.join(os.path.dirname(__file__), ".venv")
    
    if platform.system() == "Windows":
        python_path = os.path.join(venv_path, "Scripts", "python.exe")
    else:
        python_path = os.path.join(venv_path, "bin", "python")
    
    return python_path if os.path.exists(python_path) else None


def activate_venv_and_run(command):
    """在虚拟环境中运行命令"""
    venv_python = get_venv_python()
    
    if not venv_python:
        logger.error("找不到虚拟环境中的Python")
        return False
    
    try:
        # 在虚拟环境中运行命令
        subprocess.check_call([venv_python] + command)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"在虚拟环境中运行命令失败: {e}")
        return False


def install_requirements():
    """安装依赖包"""
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    
    if not os.path.exists(requirements_path):
        logger.error(f"找不到requirements.txt文件: {requirements_path}")
        return False
    
    logger.info("开始安装依赖包...")
    
    # 尝试直接读取requirements.txt并逐个安装包
    try:
        with open(requirements_path, 'r', encoding='utf-8') as f:
            packages = [line.strip() for line in f if line.strip() and not line.startswith('#')]
        
        for package in packages:
            logger.info(f"正在安装: {package}")
            if not activate_venv_and_run(["-m", "pip", "install", package]):
                logger.error(f"安装包失败: {package}")
                return False
        
        logger.info("所有依赖包安装完成")
        return True
    except Exception as e:
        logger.error(f"安装依赖包失败: {e}")
        return False


def create_directories():
    """创建必要的目录"""
    directories = [
        "assets/templates",
        "logs",
        "scripts"
    ]
    
    for directory in directories:
        dir_path = os.path.join(os.path.dirname(__file__), directory)
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"目录已创建: {dir_path}")
    
    return True


def check_windows_permissions():
    """检查Windows权限"""
    if platform.system() != "Windows":
        return True
    
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except:
        logger.warning("无法检查管理员权限，某些功能可能受限")
        return True


def main():
    """主安装流程"""
    logger.info("开始安装SAutoScript游戏自动脚本系统...")
    
    # 检查Python版本
    if not check_python_version():
        return False
    
    # 检查Windows权限
    if not check_windows_permissions():
        logger.warning("建议以管理员权限运行此脚本，以确保输入控制功能正常工作")
    
    # 创建虚拟环境
    if not create_virtual_environment():
        return False
    
    # 创建必要的目录
    if not create_directories():
        return False
    
    # 安装依赖包
    if not install_requirements():
        return False
    
    logger.info("SAutoScript游戏自动脚本系统安装完成！")
    logger.info("注意事项:")
    logger.info("1. 在Windows上，建议以管理员权限运行脚本")
    logger.info("2. 将游戏截图保存到assets/templates目录作为模板")
    logger.info("3. 根据需要修改config/settings.yaml配置文件")
    logger.info("4. 所有脚本都应在虚拟环境中运行")
    
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)