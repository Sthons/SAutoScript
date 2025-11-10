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
        
        try:
            # 获取完整的错误堆栈信息
            if isinstance(error, Exception):
                error_type = type(error).__name__
                error_message = str(error)
                stack_trace = traceback.format_exc()
            else:
                error_type = "Error"
                error_message = str(error)
                stack_trace = traceback.format_stack()
            
            # 写入错误日志文件
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(f"错误时间: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"脚本名称: {script_name}\n")
                f.write(f"错误类型: {error_type}\n")
                f.write(f"错误信息: {error_message}\n")
                f.write(f"上下文信息: {context}\n")
                f.write("\n堆栈跟踪:\n")
                f.write(stack_trace)
            
            logger.info(f"错误日志已保存到: {filepath}")
            return filepath
        except Exception as e:
            logger.error(f"保存错误日志失败: {e}")
            return None
    
    def log_exception(self, context="", script_name=""):
        """
        记录当前异常到以时间命名的日志文件
        
        Args:
            context: 错误上下文信息
            script_name: 脚本名称
        """
        # 获取当前异常信息
        exc_type, exc_value, exc_traceback = sys.exc_info()
        
        if exc_type is not None:
            return self.log_error(exc_value, context, script_name)
        else:
            logger.warning("没有当前异常可以记录")
            return None


# 全局错误日志记录器实例
error_logger = ErrorLogger()


def log_error(error, context="", script_name=""):
    """
    便捷函数：记录错误到以时间命名的日志文件
    
    Args:
        error: 错误对象或错误信息
        context: 错误上下文信息
        script_name: 脚本名称
    """
    return error_logger.log_error(error, context, script_name)


def log_exception(context="", script_name=""):
    """
    便捷函数：记录当前异常到以时间命名的日志文件
    
    Args:
        context: 错误上下文信息
        script_name: 脚本名称
    """
    return error_logger.log_exception(context, script_name)