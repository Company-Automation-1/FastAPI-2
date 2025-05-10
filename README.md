# 已废弃

# Device Automation API

基于 FastAPI 的设备自动化管理系统，提供设备管理、文件上传和自动化任务调度功能。

## 项目结构

```bash
project-1-back/
├── app/
│   ├── api/           # API 接口层
│   │   └── v1/
│   │       ├── device.py     # 设备相关接口
│   │       └── upload.py     # 上传相关接口
│   │
│   ├── core/          # 核心功能
│   │   └── config.py        # 核心配置
│   │
│   ├── device/        # 设备相关
│   │   ├── adb.py          # ADB 基础操作
│   │   └── automation.py   # UI 自动化
│   │
│   ├── models/        # 数据模型
│   │   └── request.py      # 请求数据模型
│   │
│   ├── scheduler/     # 调度相关
│   │   ├── scheduler.py    # 调度器
│   │   └── tasks.py       # 任务定义
│   │
│   ├── services/      # 业务逻辑层
│   │   └── upload_service.py # 上传处理服务
│   │
│   └── utils/         # 工具函数
│       └── file_utils.py   # 文件处理工具
│
├── logs/             # 日志目录
├── uploads/          # 上传文件目录
├── main.py          # 应用入口
├── requirements.txt  # 项目依赖
└── README.md        # 项目文档
```

## 环境要求

- Python 3.8+
- ADB 工具
- 安卓设备或模拟器

## 快速开始

1. **创建虚拟环境**
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows
```

2. **安装依赖**
```bash
pip install -r requirements.txt
```

3. **启动服务**
```bash
# 开发模式（支持热重载）
uvicorn main:app --reload --host 0.0.0.0 --port 8000
uvicorn main:app --reload --host 0.0.0.0 --port 8848
# 或直接运行
python main.py
```

## API 文档

启动服务后访问：
- Swagger UI: http://localhost:8000/api/docs
- ReDoc: http://localhost:8000/api/redoc

### 主要接口

1. **设备列表**
```http
GET /api/v1/devices/list
```

2. **文件上传**
```http
POST /api/v1/upload
```

## 配置说明

主要配置位于 `app/core/config.py`：
- 设备映射配置
- ADB 配置
- 自动化配置
- 时区设置

## 开发指南

1. **目录结构**
- `api/`: API 接口定义
- `core/`: 核心配置
- `device/`: 设备操作相关
- `models/`: 数据模型定义
- `scheduler/`: 任务调度相关
- `services/`: 业务逻辑服务
- `utils/`: 通用工具函数

## 常见问题

1. **ADB 连接问题**
- 确保 ADB 工具已正确安装
- 检查设备是否已授权
- 验证设备 ID 是否正确

2. **文件上传失败**
- 检查文件大小是否超限
- 验证设备存储路径是否正确
- 确认设备是否在线

## 许可证

[MIT License](LICENSE)
