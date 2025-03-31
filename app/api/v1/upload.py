"""
设备数据上传API模块

该模块提供设备数据上传的API接口，主要功能包括：
1. 接收并处理设备上传的文件和文本数据
2. 创建相应的定时任务进行后续处理
3. 处理上传过程中的异常情况
"""

from fastapi import APIRouter, HTTPException, status
from app.scheduler.tasks import execute_immediate_tasks, execute_scheduled_tasks
from app.models.request import UploadRequest
from app.services.upload_service import process_upload
from app.scheduler.scheduler import add_job
from datetime import datetime, timezone, timedelta
import logging
from app.device.del_img import delete_device_album
from app.core.config import format_folder_name, get_shanghai_time, SHANGHAI_TIMEZONE, get_current_timestamp, debug_time_info

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/api/v1/upload",
    tags=["Device Upload"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def upload_endpoint(request: UploadRequest):
    """
    设备上传数据接口
    
    处理流程：
    1. 检查任务时间是否有效
    2. 处理文件上传请求
    3. 执行立即任务
    4. 创建定时任务
    """
    try:
        # 添加详细的时间调试信息
        time_info = debug_time_info(request.timestamp)
        logger.info(f"时间处理信息: {time_info}")
        
        # 检查任务时间是否已过期
        current_timestamp = get_current_timestamp()
        if request.timestamp <= current_timestamp:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"任务时间已过期，只能设置未来的任务。设定时间：{time_info['shanghai_time']}"
            )
        
        # 处理上传
        response_data = await handle_upload(request)
        
        # 执行立即任务
        await execute_immediate_task(request)
        
        # 创建定时任务
        await create_scheduled_task(request)
        
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"上传处理失败: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"上传处理失败: {str(e)}"
        )

async def handle_upload(request: UploadRequest) -> dict:
    """处理文件上传请求"""
    try:
        # 使用统一的文件夹名称格式化函数
        folder_name = format_folder_name(request.timestamp)
        
        # 如果有旧文件夹，先删除
        delete_result = await delete_device_album(request.device_name, folder_name)
        if not delete_result:
            logger.warning(f"清理旧文件夹失败: {folder_name}")
        
        # 继续处理上传
        return await process_upload(request)
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Upload failed: {str(e)}"
        )

async def execute_immediate_task(request: UploadRequest):
    """执行立即任务"""
    try:
        await execute_immediate_tasks(
            device_name=request.device_name,
            upload_time=request.timestamp
        )
    except Exception as e:
        logger.error(f"Immediate task failed: {str(e)}")
        # 这里我们不抛出异常，因为这是次要任务，不应影响上传响应
        
async def create_scheduled_task(request: UploadRequest):
    """创建定时任务"""
    try:
        # 直接使用时间戳创建触发时间
        trigger_time = get_shanghai_time(request.timestamp)
        
        add_job(
            execute_scheduled_tasks,
            trigger_time,
            device_name=request.device_name,
            task_time=request.timestamp
        )
    except Exception as e:
        logger.error(f"Task scheduling failed: {str(e)}")
        # 这里我们不抛出异常，因为这是次要任务，不应影响上传响应 