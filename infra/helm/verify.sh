#!/usr/bin/env bash
set -euo pipefail

echo "============================================="
echo "  NBank — Проверка работы сервисов"
echo "============================================="

# --- Поды ---
echo ""
echo "[1/6] Все поды в кластере:"
kubectl get pods -o wide
echo ""

# --- Сервисы ---
echo "[2/6] Все сервисы:"
kubectl get svc
echo ""

# --- Describe подов ---
echo "[3/6] Описание подов:"
for pod in $(kubectl get pods -o jsonpath='{.items[*].metadata.name}'); do
  echo "--- Pod: $pod ---"
  kubectl describe pod "$pod" | grep -A5 "Conditions:"
  echo ""
done

# --- Логи ---
echo "[4/6] Логи сервисов (последние 20 строк):"
for deploy in postgres backend frontend; do
  echo "--- Логи: $deploy ---"
  POD=$(kubectl get pods -l app="$deploy" -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || echo "")
  if [ -n "$POD" ]; then
    kubectl logs "$POD" --tail=20 2>/dev/null || echo "  (логи недоступны)"
  else
    echo "  (под не найден)"
  fi
  echo ""
done

# --- ConfigMaps ---
echo "[5/6] ConfigMaps:"
kubectl get configmaps
echo ""
echo "--- postgres-config ---"
kubectl describe configmap postgres-config 2>/dev/null || echo "  (не найден)"
echo ""
echo "--- backend-config ---"
kubectl describe configmap backend-config 2>/dev/null || echo "  (не найден)"
echo ""
echo "--- selenoid-config ---"
kubectl describe configmap selenoid-config 2>/dev/null || echo "  (не найден)"
echo ""

# --- Secrets ---
echo "[6/6] Secrets:"
kubectl get secrets
echo ""
echo "--- postgres-secret (описание без данных) ---"
kubectl describe secret postgres-secret 2>/dev/null || echo "  (не найден)"
echo ""

echo "============================================="
echo "  Проверка завершена"
echo "============================================="
