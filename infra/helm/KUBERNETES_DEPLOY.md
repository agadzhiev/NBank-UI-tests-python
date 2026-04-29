# NBank — Развёртывание в Kubernetes (Minikube + Helm)

## Установка зависимостей (macOS)

```bash
brew install minikube helm kubectl
```

## Быстрый старт

```bash
# 1. Запустить Minikube
minikube start --driver=docker --memory=4096 --cpus=2

# 2. Развернуть приложение через Helm
cd infra/helm
./deploy.sh
```

## Описание сервисов

| Сервис       | Описание                      | Внутренний порт | NodePort (внешний) |
|-------------|-------------------------------|-----------------|-------------------|
| postgres    | PostgreSQL 15 (Alpine)         | 5432            | 30432             |
| backend     | NBank Backend (Spring Boot)    | 4111            | 30411             |
| frontend    | NBank Frontend (nginx)         | 80              | 30000             |
| selenoid    | Selenoid (запуск браузеров)    | 4444            | 30444             |
| selenoid-ui | Selenoid UI (мониторинг)       | 8080            | 30808             |

## Доступ к сервисам

### Через Minikube IP

```bash
MINIKUBE_IP=$(minikube ip)
# Frontend:     http://$MINIKUBE_IP:30000
# Backend:      http://$MINIKUBE_IP:30411
# Selenoid:     http://$MINIKUBE_IP:30444
# Selenoid UI:  http://$MINIKUBE_IP:30808
```

### Через port-forward (localhost)

```bash
kubectl port-forward svc/frontend 3000:80 &
kubectl port-forward svc/backend 4111:4111 &
kubectl port-forward svc/selenoid 4444:4444 &
kubectl port-forward svc/selenoid-ui 8080:8080 &

# Frontend:     http://localhost:3000
# Backend:      http://localhost:4111
# Selenoid:     http://localhost:4444
# Selenoid UI:  http://localhost:8080
```

## Поды (Pods)

```bash
# Список всех подов
kubectl get pods -o wide

# Описание конкретного пода
kubectl describe pod <pod-name>

# Логи пода
kubectl logs <pod-name>
kubectl logs <pod-name> --tail=50 -f  # последние 50 строк + follow
```

## ConfigMap и Secrets

### ConfigMaps

**postgres-config** — конфигурация базы данных:
- `POSTGRES_DB: nbank` — имя базы данных

**backend-config** — конфигурация бэкенда:
- `SPRING_DATASOURCE_URL: jdbc:postgresql://postgres:5432/nbank` — строка подключения к БД

**selenoid-config** — конфигурация Selenoid:
- `browsers.json` — описание браузеров и их версий (Chrome 131.0, Firefox 133.0)

```bash
# Просмотр ConfigMaps
kubectl get configmaps
kubectl describe configmap postgres-config
kubectl describe configmap backend-config
kubectl describe configmap selenoid-config
```

### Secrets

**postgres-secret** — секреты доступа к PostgreSQL:
- `POSTGRES_USER` — имя пользователя БД (base64-encoded)
- `POSTGRES_PASSWORD` — пароль БД (base64-encoded)

Секреты используются:
- PostgreSQL-подом для инициализации пользователя
- Backend-подом для подключения к БД

```bash
# Просмотр секретов (без данных)
kubectl get secrets
kubectl describe secret postgres-secret
```

## Проверка работы сервисов

```bash
# Запуск полной проверки
./verify.sh

# Или вручную:
kubectl get svc
kubectl get pods
kubectl logs -l app=backend --tail=20
kubectl logs -l app=frontend --tail=20
kubectl logs -l app=postgres --tail=20
```

## Масштабирование

```bash
# Масштабировать backend до 3 реплик
./scale.sh backend 3

# Масштабировать frontend до 4 реплик
./scale.sh frontend 4

# Или вручную:
kubectl scale deployment backend --replicas=3
kubectl scale deployment frontend --replicas=4

# Проверить статус
kubectl get pods -l app=backend
kubectl rollout status deployment/backend
```

## Деплой через Helm

```bash
# Установка
helm install nbank infra/helm/nbank-app/

# Обновление
helm upgrade nbank infra/helm/nbank-app/

# Установка с переопределением значений
helm upgrade --install nbank infra/helm/nbank-app/ \
  --set backend.replicas=3 \
  --set frontend.replicas=2

# Удаление
helm uninstall nbank

# Статус релиза
helm status nbank
helm list
```

## Удаление

```bash
# Удалить Helm-релиз
helm uninstall nbank

# Остановить Minikube
minikube stop

# Удалить кластер полностью
minikube delete
```
