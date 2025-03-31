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

# 定义上海时区
SHANGHAI_TIMEZONE = timezone(timedelta(hours=8))

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

def get_shanghai_time(utc_timestamp: int) -> datetime:
    """
    将UTC时间戳转换为上海时间
    注意：输入的时间戳虽然是UTC格式，但实际表示的是上海时间
    
    Args:
        utc_timestamp (int): UTC时间戳（但表示的是上海时间）
        
    Returns:
        datetime: 上海时区的datetime对象
    """
    # 将UTC时间戳转换为datetime对象（不带时区信息）
    utc_dt = datetime.utcfromtimestamp(utc_timestamp)
    
    # 将UTC时间转换为上海时间（减去8小时时差）
    # shanghai_dt = utc_dt - timedelta(hours=8)
    shanghai_dt = utc_dt
    # 添加时区信息
    return shanghai_dt.replace(tzinfo=SHANGHAI_TIMEZONE)

def format_folder_name(utc_timestamp: int) -> str:
    """
    格式化文件夹名称
    
    Args:
        utc_timestamp (int): UTC时间戳（但表示的是上海时间）
        
    Returns:
        str: 格式化的文件夹名称 (YYYYMMDDHHmmss)
    """
    shanghai_time = get_shanghai_time(utc_timestamp)
    return shanghai_time.strftime("%Y%m%d%H%M%S")

def get_current_timestamp() -> int:
    """
    获取当前的UTC时间戳
    
    Returns:
        int: UTC时间戳
    """
    return int(datetime.now(timezone.utc).timestamp())

def debug_time_info(timestamp: int) -> dict:
    """
    用于调试的时间信息函数
    
    Args:
        timestamp (int): UTC时间戳
        
    Returns:
        dict: 包含各种时间信息的字典
    """
    utc_time = datetime.utcfromtimestamp(timestamp)
    shanghai_time = get_shanghai_time(timestamp)
    folder_name = format_folder_name(timestamp)
    
    return {
        "timestamp": timestamp,
        "utc_time": utc_time.strftime("%Y-%m-%d %H:%M:%S"),
        "shanghai_time": shanghai_time.strftime("%Y-%m-%d %H:%M:%S"),
        "folder_name": folder_name
    }

# 创建全局配置实例
settings = Settings() 