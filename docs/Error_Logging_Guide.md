# 错误日志记录指南

## 概述

本项目提供了强大的错误日志记录功能，当程序运行过程中发生错误时，系统会自动将完整的错误信息（包括堆栈跟踪和上下文信息）保存到以时间命名的日志文件中。这有助于开发者快速定位和解决问题。

## 功能特点

- **自动错误记录**：在关键位置自动捕获和记录错误
- **时间戳命名**：每个错误日志文件都以时间戳命名，便于查找和管理
- **完整错误信息**：包含错误消息、堆栈跟踪和自定义上下文信息
- **分类存储**：错误日志文件存储在专门的目录中，与常规日志分离
- **便捷API**：提供简单的API，方便在自定义代码中记录错误

## 错误日志文件位置

错误日志文件默认保存在以下位置：
```
项目根目录/logs/errors/
```

每个错误日志文件名格式为：`error_YYYY-MM-DD_HH-MM-SS.log`

## 使用方法

### 1. 自动错误记录

在以下情况下，系统会自动记录错误日志：

- **BaseGameScript子类**：在`start()`、`_main_loop()`、`_load_config()`和`_init_components()`方法中发生错误时
- **GameAutoScript类**：在`start()`、`_main_loop()`、`_load_config()`、`_init_components()`和`_setup_logger()`方法中发生错误时

### 2. 手动记录错误

您可以在自己的代码中使用以下函数手动记录错误：

#### 记录普通错误信息

```python
from core import log_error

# 记录普通错误信息
log_error("这是一个错误信息", "MyScript", {"key": "value"})
```

#### 记录异常信息

```python
from core import log_exception

try:
    # 可能出错的代码
    result = 1 / 0
except Exception as e:
    # 记录异常信息
    log_exception("发生除零错误", "MyScript", {"additional_info": "some data"})
```

### 3. 在自定义脚本中集成错误记录

如果您创建了自己的脚本类，建议继承`BaseGameScript`类，这样就能自动获得错误记录功能。

```python
from core import BaseGameScript

class MyCustomScript(BaseGameScript):
    def __init__(self):
        super().__init__()
        self.max_loops = 10
        self.loop_delay = 1
    
    def game_logic(self):
        # 您的游戏逻辑
        # 如果这里发生错误，BaseGameScript会自动记录
        pass
```

## 错误日志文件内容

每个错误日志文件包含以下信息：

1. **时间戳**：错误发生的精确时间
2. **错误消息**：描述错误的信息
3. **脚本名称**：发生错误的脚本或类名
4. **堆栈跟踪**：完整的错误堆栈信息
5. **上下文信息**：与错误相关的额外数据

示例错误日志内容：
```
===== 错误日志 =====
时间: 2023-11-15 14:30:45
错误消息: 在第 2 次循环中发生除零错误
脚本名称: ErrorLoggingExample
上下文信息:
  loop_count: 2

堆栈跟踪:
Traceback (most recent call last):
  File "error_logging_example.py", line 42, in game_logic
    result = 1 / 0
ZeroDivisionError: division by zero
====================
```

## 查看错误日志

### 1. 通过命令行查看

您可以使用以下命令查看最新的错误日志文件：

```bash
# Windows PowerShell
Get-ChildItem -Path "logs/errors" -Filter "*.log" | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | Get-Content

# 或者使用更简单的命令
type "logs/errors\error_$(Get-Date -Format 'yyyy-MM-dd')*.log" | more
```

### 2. 通过文本编辑器查看

直接打开`logs/errors`目录，找到对应的错误日志文件，使用任何文本编辑器查看。

### 3. 通过程序查看

您也可以编写程序来读取和分析错误日志：

```python
import os
import glob
from datetime import datetime

# 获取最新的错误日志文件
error_log_dir = "logs/errors"
log_files = glob.glob(os.path.join(error_log_dir, "error_*.log"))

if log_files:
    # 按修改时间排序，获取最新的
    latest_log = max(log_files, key=os.path.getmtime)
    
    # 读取并打印内容
    with open(latest_log, 'r', encoding='utf-8') as f:
        print(f.read())
```

## 运行示例

您可以通过以下方式运行错误日志记录示例：

1. 使用启动脚本：
   ```
   运行 start.bat
   选择选项 6 (Run error logging example)
   ```

2. 直接运行：
   ```
   python scripts/error_logging_example.py
   ```

示例将演示不同类型的错误记录，并在结束后显示生成的错误日志文件位置。

## 最佳实践

1. **提供有意义的错误消息**：错误消息应清楚地描述问题
2. **包含相关上下文**：添加与错误相关的数据，便于调试
3. **不要记录敏感信息**：避免在错误日志中记录密码、密钥等敏感数据
4. **定期清理旧日志**：定期删除旧的错误日志文件，节省磁盘空间
5. **使用适当的日志级别**：根据错误严重程度选择合适的日志级别

## 配置选项

错误日志记录功能可以通过配置文件进行自定义。相关配置项位于`config/settings.yaml`中：

```yaml
logging:
  level: INFO
  file: logs/SAutoScript.log
  rotation: "10 MB"
  
# 错误日志特定配置
error_logging:
  enabled: true
  directory: logs/errors
  max_files: 100  # 最大保留的错误日志文件数
```

## 故障排除

### 问题：错误日志文件未生成

**可能原因**：
- 错误日志目录权限不足
- 磁盘空间不足
- 错误日志功能被禁用

**解决方案**：
1. 检查`logs/errors`目录是否存在且有写入权限
2. 检查磁盘空间
3. 确认配置文件中错误日志功能已启用

### 问题：错误日志内容不完整

**可能原因**：
- 错误发生在日志记录功能初始化之前
- 系统资源不足

**解决方案**：
1. 确保在代码中正确导入和使用错误日志功能
2. 检查系统资源使用情况

## 总结

错误日志记录功能是项目调试和维护的重要工具。通过合理使用这一功能，您可以更快速地定位和解决问题，提高开发效率和代码质量。

如果您有任何问题或建议，请随时反馈给开发团队。