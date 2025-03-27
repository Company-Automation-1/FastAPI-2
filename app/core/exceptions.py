"""
核心异常模块

定义应用程序中使用的所有自定义异常
"""

class AppException(Exception):
    """应用程序基础异常类"""
    def __init__(self, message: str = None, code: int = None):
        self.message = message
        self.code = code
        super().__init__(self.message)

class DeviceError(AppException):
    """设备操作相关错误"""
    pass

class ADBError(DeviceError):
    """ADB 操作错误"""
    pass

class AutomationError(DeviceError):
    """自动化操作错误"""
    pass

class TaskError(AppException):
    """任务执行错误"""
    pass

class ConfigError(AppException):
    """配置错误"""
    pass 