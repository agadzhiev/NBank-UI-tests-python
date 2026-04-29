#!/usr/bin/env bash
set -euo pipefail

CHART_DIR="$(cd "$(dirname "$0")/nbank-app" && pwd)"
RELEASE_NAME="nbank"
NAMESPACE="default"

echo "============================================="
echo "  NBank Kubernetes Deployment via Helm"
echo "============================================="

# --- 1. Проверка зависимостей ---
echo ""
echo "[1/7] Проверка зависимостей..."
for cmd in minikube kubectl helm; do
  if ! command -v "$cmd" &>/dev/null; then
    echo "ОШИБКА: $cmd не установлен. Установите его перед запуском."
    exit 1
  fi
done
echo "  minikube, kubectl, helm — OK"

# --- 2. Запуск Minikube ---
echo ""
echo "[2/7] Запуск Minikube..."
if minikube status --format='{{.Host}}' 2>/dev/null | grep -q "Running"; then
  echo "  Minikube уже запущен"
else
  minikube start --driver=docker --memory=4096 --cpus=2
  echo "  Minikube запущен"
fi

# --- 3. Деплой через Helm ---
echo ""
echo "[3/7] Установка/обновление Helm-релиза '$RELEASE_NAME'..."
helm upgrade --install "$RELEASE_NAME" "$CHART_DIR" \
  --namespace "$NAMESPACE" \
  --wait \
  --timeout 5m
echo "  Helm-релиз '$RELEASE_NAME' установлен"

# --- 4. Проверка подов ---
echo ""
echo "[4/7] Список подов (kubectl get pods):"
kubectl get pods -o wide

# --- 5. Проверка сервисов ---
echo ""
echo "[5/7] Список сервисов (kubectl get svc):"
kubectl get svc

# --- 6. Описание сервисов и портов ---
echo ""
echo "[6/7] Описание сервисов и портов:"
echo "============================================="
echo "  Сервис       | Внутренний порт | NodePort"
echo "  -------------|-----------------|----------"
echo "  postgres      | 5432            | 30432"
echo "  backend       | 4111            | 30411"
echo "  frontend      | 80              | 30000"
echo "  selenoid      | 4444            | 30444"
echo "  selenoid-ui   | 8080            | 30808"
echo "============================================="

# --- 7. Проброс портов ---
echo ""
echo "[7/7] Получение URL сервисов через Minikube:"
echo ""
MINIKUBE_IP=$(minikube ip)
echo "  Backend:      http://$MINIKUBE_IP:30411"
echo "  Frontend:     http://$MINIKUBE_IP:30000"
echo "  Selenoid:     http://$MINIKUBE_IP:30444"
echo "  Selenoid UI:  http://$MINIKUBE_IP:30808"
echo "  PostgreSQL:   $MINIKUBE_IP:30432"
echo ""
echo "  Или используйте port-forward для доступа через localhost:"
echo "    kubectl port-forward svc/frontend 3000:80 &"
echo "    kubectl port-forward svc/backend 4111:4111 &"
echo "    kubectl port-forward svc/selenoid 4444:4444 &"
echo "    kubectl port-forward svc/selenoid-ui 8080:8080 &"
echo ""
echo "============================================="
echo "  Деплой завершён успешно!"
echo "============================================="
