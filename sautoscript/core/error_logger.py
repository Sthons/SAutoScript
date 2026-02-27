#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
import traceback
import datetime
from loguru import logger


class ErrorLogger:
    """
    错误日志记录器
    
    用于在发生错误时将完整的错误信息保存到以时间命名的日志文件中
    """
    
    def __init__(self, log_dir="logs/errors"):
        """
        初始化错误日志记录器
        
        Args:
            log_dir: 错误日志目录
        """
        self.log_dir = log_dir
        
        # 确保错误日志目录存在
        os.makedirs(self.log_dir, exist_ok=True)
    
    def log_error(self, error, context="", script_name=""):
        """
        记录错误到以时间命名的日志文件
        
        Args:
            error: 错误对象或错误信息
            context: 错误上下文信息
            script_name: 脚本名称
        """
        # 生成时间戳作为文件名
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # 添加脚本名称到文件名（如果有）
        if script_name:
            filename = f"{script_name}_{timestamp}.log"
        else:
            filename = f"error_{timestamp}.log"
        
        # 完整文件路径
        filepath = os.path.join(self.log_dir, filename)
        
        # 构建错误信息
        error_message = f"===== 错误日志 =====\n"
        error_message += f"时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        error_message += f"错误消息: {str(error)}\n"
        
        if script_name:
            error_message += f"脚本名称: {script_name}\n"
        
        if context:
            error_message += f"上下文信息:\n{context}\n"
        
        # 获取堆栈跟踪
        error_message += "\n堆栈跟踪:\n"
        error_message += traceback.format_exc()
        error_message += "\n===================="
        
        # 写入错误日志文件
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(error_message)
            
            logger.info(f"错误日志已保存到: {filepath}")
        except Exception as e:
            logger.error(f"保存错误日志失败: {e}")


# 全局错误日志记录器实例
error_logger = ErrorLogger()


def log_error(error, script_name="", context={}):
    """
    记录普通错误信息
    
    Args:
        error: 错误信息
        script_name: 脚本名称
        context: 上下文信息（字典）
    """
    # 格式化上下文信息
    context_str = ""
    if context:
        for key, value in context.items():
            context_str += f"  {key}: {value}\n"
    
    error_logger.log_error(str(error), context_str, script_name)


def log_exception(error, script_name="", context={}):
    """
    记录异常信息
    
    Args:
        error: 异常对象或错误信息
        script_name: 脚本名称
        context: 上下文信息（字典）
    """
    # 格式化上下文信息
    context_str = ""
    if context:
        for key, value in context.items():
            context_str += f"  {key}: {value}\n"
    
    error_logger.log_error(str(error), context_str, script_name)
