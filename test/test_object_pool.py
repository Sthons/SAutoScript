#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import cv2
import time
import os
import sys
from loguru import logger

# 添加项目根目录到路径
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

# 导入优化后的图像识别模块
from core.image_recognition import ImageRecognition, NumpyArrayPool


class ObjectPoolTest:
    """对象池性能测试类"""
    
    def __init__(self):
        self.test_iterations = 200  # 测试迭代次数
        self.image_size = (1920, 1080)  # 测试图像大小
        self.template_size = (100, 100)  # 模板大小
        
        # 创建测试图像
        self.test_image = np.random.randint(0, 255, (*self.image_size, 3), dtype=np.uint8)
        self.template_image = np.random.randint(0, 255, (*self.template_size, 3), dtype=np.uint8)
        
        # 保存模板图像用于测试
        os.makedirs("assets/templates", exist_ok=True)
        cv2.imwrite("assets/templates/test_template.png", self.template_image)
        
        logger.info(f"对象池性能测试初始化完成，迭代次数: {self.test_iterations}")
    
    def test_without_pool(self):
        """测试不使用对象池的性能"""
        logger.info("开始测试不使用对象池的性能...")
        
        # 配置禁用对象池
        config = {
            "threshold": 0.5,
            "method": "cv2.TM_CCOEFF_NORMED",
            "object_pool": {
                "enabled": False,
                "max_size": 0
            }
        }
        
        image_recognition = ImageRecognition(config)
        
        start_time = time.time()
        
        for i in range(self.test_iterations):
            # 执行模板匹配
            result = image_recognition.find_template(self.test_image, "test_template")
            
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                logger.info(f"无对象池测试进度: {i + 1}/{self.test_iterations}, 已用时: {elapsed:.2f}秒")
        
        total_time = time.time() - start_time
        logger.info(f"无对象池测试完成，总用时: {total_time:.2f}秒，平均每次: {total_time/self.test_iterations*1000:.2f}毫秒")
        
        return total_time
    
    def test_with_pool(self):
        """测试使用对象池的性能"""
        logger.info("开始测试使用对象池的性能...")
        
        # 配置启用对象池
        config = {
            "threshold": 0.5,
            "method": "cv2.TM_CCOEFF_NORMED",
            "object_pool": {
                "enabled": True,
                "max_size": 50
            }
        }
        
        image_recognition = ImageRecognition(config)
        
        start_time = time.time()
        
        for i in range(self.test_iterations):
            # 执行模板匹配
            result = image_recognition.find_template(self.test_image, "test_template")
            
            if (i + 1) % 50 == 0:
                elapsed = time.time() - start_time
                logger.info(f"有对象池测试进度: {i + 1}/{self.test_iterations}, 已用时: {elapsed:.2f}秒")
        
        total_time = time.time() - start_time
        logger.info(f"有对象池测试完成，总用时: {total_time:.2f}秒，平均每次: {total_time/self.test_iterations*1000:.2f}毫秒")
        
        # 显示对象池统计信息
        pool_stats = image_recognition.get_pool_stats()
        logger.info(f"对象池统计信息: {pool_stats}")
        
        return total_time
    
    def test_pool_efficiency(self):
        """测试对象池的效率"""
        logger.info("开始测试对象池效率...")
        
        pool = NumpyArrayPool(max_size=20)
        
        # 测试数组形状
        test_shapes = [
            (1920, 1080),
            (1000, 800),
            (500, 400),
            (200, 150)
        ]
        
        arrays = []
        
        # 获取数组
        start_time = time.time()
        for i in range(100):
            shape = test_shapes[i % len(test_shapes)]
            array = pool.get_array(shape)
            arrays.append(array)
        get_time = time.time() - start_time
        
        # 归还数组
        start_time = time.time()
        for array in arrays:
            pool.return_array(array)
        return_time = time.time() - start_time
        
        # 再次获取数组（应该从池中获取）
        start_time = time.time()
        for i in range(50):
            shape = test_shapes[i % len(test_shapes)]
            array = pool.get_array(shape)
            pool.return_array(array)
        pool_time = time.time() - start_time
        
        logger.info(f"获取100个数组用时: {get_time*1000:.2f}毫秒")
        logger.info(f"归还100个数组用时: {return_time*1000:.2f}毫秒")
        logger.info(f"池化操作50次用时: {pool_time*1000:.2f}毫秒")
        
        stats = pool.get_pool_stats()
        logger.info(f"对象池统计: {stats}")
    
    def run_comparison(self):
        """运行性能对比测试"""
        logger.info("开始对象池性能对比测试...")
        
        # 测试对象池效率
        self.test_pool_efficiency()
        
        # 测试不使用对象池
        time_without_pool = self.test_without_pool()
        
        # 等待一段时间让系统稳定
        time.sleep(2)
        
        # 测试使用对象池
        time_with_pool = self.test_with_pool()
        
        # 计算性能提升
        improvement = ((time_without_pool - time_with_pool) / time_without_pool) * 100
        
        logger.info("=" * 60)
        logger.info("性能对比结果:")
        logger.info(f"无对象池总用时: {time_without_pool:.2f}秒")
        logger.info(f"有对象池总用时: {time_with_pool:.2f}秒")
        logger.info(f"性能提升: {improvement:.2f}%")
        logger.info(f"平均每次节省时间: {(time_without_pool - time_with_pool)/self.test_iterations*1000:.2f}毫秒")
        logger.info("=" * 60)
        
        return {
            "time_without_pool": time_without_pool,
            "time_with_pool": time_with_pool,
            "improvement_percent": improvement,
            "iterations": self.test_iterations
        }
    
    def cleanup(self):
        """清理测试文件"""
        try:
            if os.path.exists("assets/templates/test_template.png"):
                os.remove("assets/templates/test_template.png")
                logger.info("测试文件已清理")
        except Exception as e:
            logger.error(f"清理测试文件失败: {e}")


def main():
    """主函数"""
    # 配置日志
    logger.remove()
    logger.add(
        sys.stderr,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        level="INFO"
    )
    
    logger.info("开始对象池优化性能测试")
    
    try:
        # 创建测试实例
        test = ObjectPoolTest()
        
        # 运行对比测试
        results = test.run_comparison()
        
        # 清理测试文件
        test.cleanup()
        
        logger.info("对象池优化性能测试完成")
        
        return results
        
    except Exception as e:
        logger.error(f"测试过程中发生错误: {e}")
        return None


if __name__ == "__main__":
    main()