import os
import shutil
from app.core.config import settings

def delete_device_album(device_name: str, album_name: str) -> bool:
    """
    根据配置中的设备路径删除指定设备的指定相册文件夹
    
    Args:
        device_name (str): 设备名称（对应配置中的设备名）
        album_name (str): 相册文件夹名称
        
    Returns:
        bool: 删除成功返回True，失败返回False
    """
    try:
        # 检查设备是否在配置中
        if device_name not in settings.DEVICE_CONFIG:
            print(f"设备 {device_name} 未在配置中找到")
            return False
            
        # 获取设备存储路径
        device_storage = settings.DEVICE_CONFIG[device_name]["storage_path"]
        
        # 构建完整的相册路径
        album_path = os.path.join(device_storage, album_name)
        
        # 检查路径是否存在
        if not os.path.exists(album_path):
            print(f"相册路径不存在: {album_path}")
            return False
            
        # 删除文件夹及其所有内容
        shutil.rmtree(album_path)
        print(f"成功删除相册: {album_path}")
        return True
        
    except Exception as e:
        print(f"删除相册时发生错误: {str(e)}")
        return False
