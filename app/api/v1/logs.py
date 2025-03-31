from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
import os

router = APIRouter(
    prefix="/api/v1/logs",
    tags=["Logs Info"]
)
@router.get("/", response_model=List[str])
async def get_logs(
    # page: Optional[int] = 1,  # 新增分页参数，默认第1页
    # page_size: Optional[int] = 10,  # 默认每页10条
    level: Optional[str] = None,
):
    try:
        log_file_path = "logs/app.log"
        if not os.path.exists(log_file_path):
            raise HTTPException(status_code=404, detail="日志文件不存在")
        
        with open(log_file_path, "r", encoding="utf-8") as f:
            all_logs = f.readlines()[::-1]  # 反转以获取最新日志

        # 根据级别过滤
        if level:
            filtered_logs = [log.strip() for log in all_logs if f" - {level.upper()} -" in log]
        else:
            filtered_logs = [log.strip() for log in all_logs]

        # 分页处理
        # start = (page - 1) * page_size
        # end = start + page_size
        # paginated_logs = filtered_logs[start:end]
        filtered_logs = [log.strip() for log in all_logs]
        
        return filtered_logs

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取日志失败: {str(e)}")