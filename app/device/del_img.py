import os
import shutil
from app.core.config import settings
from app.core.config import UPLOAD_DIR
import logging
import asyncio
from pathlib import Path
from app.device.adb import adb

logger = logging.getLogger(__name__)

async def delete_device_album(device_name: str, album_name: str) -> bool:
    """
    删除指定设备的本地相册文件夹和设备端文件夹
    
    Args:
        device_name (str): 设备名称
        album_name (str): 相册文件夹名称
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    try:
        success = True
        
        # 1. 删除本地文件夹
        # 构建本地上传目录的路径
        local_album_path = UPLOAD_DIR / device_name / album_name
        logger.info(f"准备删除本地文件夹: {local_album_path}")
        
        # 删除本地上传目录
        if local_album_path.exists():
            shutil.rmtree(local_album_path)
            logger.info(f"成功删除本地文件夹: {local_album_path}")
        else:
            logger.info(f"本地文件夹不存在，无需删除: {local_album_path}")

        # 2. 删除设备端文件夹
        try:
            # 检查设备是否在配置中
            if device_name in settings.DEVICE_CONFIG:
                # 获取设备存储路径
                device_storage = settings.DEVICE_CONFIG[device_name]["storage_path"]
                device_album_path = os.path.join(device_storage, album_name)
                
                # 检查设备连接状态
                is_connected = await adb.is_device_connected_async(device_name)
                
                if is_connected:
                    # 执行删除命令
                    try:
                        await adb.execute_device_command_async(
                            device_name,
                            ["shell", f"rm -rf '{device_album_path}'"]
                        )
                        logger.info(f"成功删除设备端文件夹: {device_album_path}")
                    except Exception as e:
                        logger.error(f"删除设备端文件夹失败: {str(e)}")
                        success = False
                else:
                    logger.warning(f"设备 {device_name} 未连接，跳过设备端文件夹删除")
            else:
                logger.warning(f"设备 {device_name} 未在配置中找到，跳过设备端文件夹删除")
                
        except Exception as e:
            logger.error(f"处理设备端文件夹时发生错误: {str(e)}")
            success = False
            
        return success
            
    except Exception as e:
        logger.error(f"删除相册时发生错误: {str(e)}")
        return False
