#!/usr/bin/env bash
set -euo pipefail

SERVICE="${1:-backend}"
REPLICAS="${2:-3}"

echo "============================================="
echo "  Масштабирование $SERVICE до $REPLICAS реплик"
echo "============================================="

echo ""
echo "[1/3] Текущее состояние подов $SERVICE:"
kubectl get pods -l app="$SERVICE"

echo ""
echo "[2/3] Масштабирование..."
kubectl scale deployment "$SERVICE" --replicas="$REPLICAS"

echo ""
echo "[3/3] Ожидание готовности..."
kubectl rollout status deployment/"$SERVICE" --timeout=120s

echo ""
echo "Поды $SERVICE после масштабирования:"
kubectl get pods -l app="$SERVICE"

echo ""
echo "============================================="
echo "  $SERVICE масштабирован до $REPLICAS реплик"
echo "============================================="
