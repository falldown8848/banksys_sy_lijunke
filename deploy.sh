#!/usr/bin/env bash
# 部署脚本:构建镜像 → 端口回退 → 幂等重启 → 健康检查。
# 遵循 standards/05 §4;由 cd.yml 通过 SSH 在服务器上执行。
set -euo pipefail

APP="banksys_sy_lijunke"
DEPLOY_DIR="/opt/${APP}"
HOST="${SSH_HOST:-}"
PORT=8888
PORT_MAX=8892
CONTAINER_PORT=8888
PIP_INDEX_URL="${PIP_INDEX_URL:-https://pypi.tuna.tsinghua.edu.cn/simple}"

cd "${DEPLOY_DIR}"

echo ">> docker build(镜像源:${PIP_INDEX_URL})"
docker build --build-arg PIP_INDEX_URL="${PIP_INDEX_URL}" -t "${APP}:latest" .

# 端口:容器内固定;主机端口优先 8888,被占用则在 8888-8892 找空闲端口
port_in_use() {
  ss -ltnH 2>/dev/null | grep -q ":$1 " && return 0
  docker ps --format "{{.Ports}}" 2>/dev/null | grep -q ":$1->" && return 0
  return 1
}

HOST_PORT=""
for p in $(seq "${PORT}" "${PORT_MAX}"); do
  if ! port_in_use "${p}"; then HOST_PORT="${p}"; break; fi
done
[ -n "${HOST_PORT}" ] || {
  echo ">> 预留端口区间 ${PORT}-${PORT_MAX} 已全部占用,部署中止"
  exit 1
}
echo ">> 部署到主机端口 ${HOST_PORT}"

docker rm -f "${APP}" 2>/dev/null || true  # 一步停删自身旧容器,幂等可重跑
docker run -d --name "${APP}" --restart unless-stopped \
  -p "${HOST_PORT}:${CONTAINER_PORT}" "${APP}:latest"

sleep 5
curl -fsS "http://localhost:${HOST_PORT}/_stcore/health"
echo ""
if [ -n "${HOST}" ]; then
  echo ">> 部署成功:http://${HOST}:${HOST_PORT}/_stcore/health"
else
  echo ">> 部署成功:http://<服务器IP>:${HOST_PORT}/_stcore/health"
fi
