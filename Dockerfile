# ===== banksys_sy_lijunke 运行时镜像 =====
# 容器内固定 8888;PIP_INDEX_URL 可配置(国内服务器用清华源)。
# 训练在构建阶段执行(模型不进 Git);验证集 AUC 低于 0.75 时构建失败。

ARG PYTHON_VERSION=3.11
FROM python:${PYTHON_VERSION}-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

ARG PIP_INDEX_URL=https://pypi.org/simple

# 1) 运行依赖(先复制依赖文件,利用层缓存)
COPY requirements.txt ./
RUN pip install --no-cache-dir --timeout 120 -i "${PIP_INDEX_URL}" -r requirements.txt

# 2) 源码 + 安装包
COPY pyproject.toml ./
COPY src/ ./src/
RUN pip install --no-cache-dir -i "${PIP_INDEX_URL}" -e .

# 3) 数据 + 训练脚本 → 构建时训练生成模型
COPY data/ ./data/
COPY scripts/ ./scripts/
RUN python scripts/train.py --out models/pipeline.joblib

# 4) Streamlit 应用页面
COPY app/ ./app/

EXPOSE 8888

HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
  CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8888/_stcore/health', timeout=3)" || exit 1

CMD ["streamlit", "run", "app/main.py", \
     "--server.port=8888", "--server.address=0.0.0.0", "--server.headless=true"]
