"""
日志配置模块

配置应用程序的日志系统，包括：
1. 控制台日志
2. 文件日志
3. 日志格式化
4. 日志级别控制
"""

import logging
import sys
from pathlib import Path
from logging.handlers import RotatingFileHandler
from app.core.config import Settings

def setup_logging():
    """配置日志系统"""
    
    # 创建日志目录
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    
    # 基础配置
    logging.basicConfig(
        level=logging.DEBUG if Settings.DEBUG else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    
    # 创建文件处理器
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10*1024*1024,  # 10MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    )
    
    # 添加处理器到根日志记录器
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    
    # 设置第三方库的日志级别
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO) 