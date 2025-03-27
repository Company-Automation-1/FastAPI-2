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
        # 检查任务时间是否已过期
        current_time = datetime.now(timezone.utc).timestamp()
        if request.timestamp <= current_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="任务时间已过期，只能设置未来的任务"
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
        # 如果有旧文件夹，先删除
        delete_device_album(request.device_name, request.folder_name)
        
        # 继续处理上传
        return await process_upload(request)
    except Exception as e:
        logger.error(f"Upload failed: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Upload failed"
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
        # 使用上海时区
        shanghai_tz = timezone(timedelta(hours=8))
        trigger_time = datetime.fromtimestamp(request.timestamp, tz=timezone.utc)
        trigger_time_shanghai = trigger_time.astimezone(shanghai_tz)
        
        add_job(
            execute_scheduled_tasks,
            trigger_time_shanghai,
            device_name=request.device_name,
            task_time=request.timestamp
        )
    except Exception as e:
        logger.error(f"Task scheduling failed: {str(e)}")
        # 这里我们不抛出异常，因为这是次要任务，不应影响上传响应 