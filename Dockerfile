# 使用Python 3.10基础镜像
FROM python:3.10-slim

# 设置工作目录
WORKDIR /app

# 设置环境变量
ENV PYTHONUNBUFFERED=1
# ENV API_TOKEN=your-default-token-here

# 复制项目文件
COPY . /app/

# 创建必要的目录
RUN mkdir -p /app/uploads /app/logs

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 暴露端口
EXPOSE 8000

# 启动命令
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"] 