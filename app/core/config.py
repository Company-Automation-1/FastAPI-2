"""
核心配置模块

配置优先级：
1. .env文件配置（开发环境）
2. 系统环境变量（生产环境）
3. 默认值
"""

from pathlib import Path
from datetime import datetime, timedelta, timezone
from typing import Dict, Any
import os
from dotenv import load_dotenv

# 定义一些常量
DEFAULT_MAX_FILE_SIZE = 100 * 1024 * 1024  # 100MB

# 优先加载.env文件（如果存在），不存在则使用系统环境变量
load_dotenv(override=False)  # override=False 表示不覆盖已存在的系统环境变量

# 项目路径配置
PROJECT_DIR = Path(__file__).parent.parent.parent
UPLOAD_DIR = PROJECT_DIR / os.getenv('UPLOAD_DIR', 'uploads')
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

class Settings:
    """
    应用程序配置类

    属性:
        DEBUG (bool): 调试模式开关
        TIMEZONE (timezone): 应用程序时区（上海，UTC+8）
        SCHEDULER_TIMEZONE (timezone): 调度器时区设置
        MAX_FILE_SIZE (int): 最大文件大小限制（100MB）
    """
    # 基础配置
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    TIMEZONE = timezone(timedelta(hours=8))  # 上海时区
    SCHEDULER_TIMEZONE = TIMEZONE
    
    # 文件配置
    MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', DEFAULT_MAX_FILE_SIZE))
    
    # ADB配置
    ADB_PATH = os.getenv('ADB_PATH', 'adb')  # 如果 adb 在系统 PATH 中
    # 或者使用绝对路径
    # ADB_PATH = r"E:\Program Files (x86)\adb\adb.exe"  # Windows 示例

    # 设备映射配置
    DEVICE_MAPPING: Dict[str, str] = {
        "deviceA": os.getenv('DEVICE_A', 'XPL5T19A28003051'),
        "deviceA_sys2": os.getenv('DEVICE_A_SYS2', 'XPL5T19A28003051'), # 同一设备的第二个系统
        "deviceB": os.getenv('DEVICE_B', 'r8yhge69x8u8lzv8'),
        "deviceC": os.getenv('DEVICE_C', 'IJKL9012')
    }

    # 设备配置详情
    DEVICE_CONFIG: Dict[str, Dict[str, Any]] = {
        "deviceA": {
            "storage_path": os.getenv('DEVICE_A_STORAGE', '/storage/emulated/0/Pictures/'),
            "lock_password": os.getenv('DEVICE_A_PASSWORD', '000000'),
            "app_package": os.getenv('DEVICE_A_APP_PACKAGE', 'com.xingin.xhs'),
            "wait_timeout": int(os.getenv('DEVICE_A_TIMEOUT', '10'))
        },
        "deviceA_sys2": {  # 同一设备的第二个系统配置
            "storage_path": os.getenv('DEVICE_A_SYS2_STORAGE', '/storage/emulated/0/Pictures/'),
            "lock_password": os.getenv('DEVICE_A_SYS2_PASSWORD', '123456'),
            "app_package": os.getenv('DEVICE_A_SYS2_APP_PACKAGE', 'com.xingin.xhs'),
            "wait_timeout": int(os.getenv('DEVICE_A_SYS2_TIMEOUT', '10'))
        },
        "deviceB": {
            "storage_path": os.getenv('DEVICE_B_STORAGE', "/storage/emulated/0/DCIM/Camera/"),
            "lock_password": os.getenv('DEVICE_B_PASSWORD', "666666"),
            "app_package": os.getenv('DEVICE_B_APP_PACKAGE', "com.xingin.xhs"),
            "wait_timeout": int(os.getenv('DEVICE_B_TIMEOUT', '10'))
        },
        "deviceC": {
            "storage_path": os.getenv('DEVICE_C_STORAGE', "/storage/emulated/0/Pictures"),
            "lock_password": os.getenv('DEVICE_C_PASSWORD', "888888"),
            "app_package": os.getenv('DEVICE_C_APP_PACKAGE', "com.xingin.xhs"),
            "wait_timeout": int(os.getenv('DEVICE_C_TIMEOUT', '10'))
        }
    }

    # 基础自动化配置（默认值）
    AUTOMATION_CONFIG = {
        'APP_PACKAGE': os.getenv('AUTOMATION_APP_PACKAGE', 'com.xingin.xhs'),
        'WAIT_TIMEOUT': 10
    }

    # 其他配置参数
    # ... 保留其他配置参数 ...

    # 添加其他方法
    # ... 保留其他方法 ...

# 创建全局配置实例
settings = Settings() 