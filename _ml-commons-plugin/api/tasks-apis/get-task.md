---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得 ML 任務"
parent: ML Tasks APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# 取得 ML 任務 API

您可以使用 `task_id` 擷取機器學習 (ML) 任務的相關資訊 (例如模型訓練、部署或預測任務)。

此 API 與[一般 Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/get-tasks/) 不同，後者用於追蹤一般 OpenSearch 作業，且回應格式不同。
{: .important }

## 端點

```json
GET /_plugins/_ml/tasks/{task_id}
```

## 範例請求

```json
GET /_plugins/_ml/tasks/MsBi1YsB0jLkkocYjD5f
```
{% include copy-curl.html %}

## 範例回應

回應格式取決於任務狀態。不同的 ML 作業 (例如模型訓練、部署或註冊) 會根據其目前狀態傳回不同的回應格式。

### 任務進行中

當任務仍在執行時，回應會包含任務詳細資料，但不包含 `model_id`：

```json
{
  "task_type": "DEPLOY_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "CREATED",
  "worker_node": ["KfEEGG7_SsKZVFqI4ko2FA"],
  "create_time": 1767030135146,
  "last_update_time": 1767030135771,
  "is_async": true
}
```

### 任務已完成

當任務順利完成時，回應會包含 `model_id` 及完整的任務詳細資料：

**模型部署任務**：

```json
{
  "model_id": "Qr1YbogBYOqeeqR7sI9L",
  "task_type": "DEPLOY_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "N77RInqjTSq_UaLh1k0BUg"
  ],
  "create_time": 1685478486057,
  "last_update_time": 1685478491090,
  "is_async": true
}
```

**模型註冊任務**：

```json
{
  "model_id": "aVeif4oB5Vm0Tdw8zYO2",
  "task_type": "REGISTER_MODEL",
  "function_name": "TEXT_EMBEDDING",
  "state": "COMPLETED",
  "worker_node": [
    "4p6FVOmJRtu3wehDD74hzQ"
  ],
  "create_time": 1694358489722,
  "last_update_time": 1694358499139,
  "is_async": true
}
```

**模型訓練任務**：

```json
{
  "model_id" : "l7lamX8BO5w8y8Ra2oty",
  "task_type" : "TRAINING",
  "function_name" : "KMEANS",
  "state" : "COMPLETED",
  "input_type" : "SEARCH_QUERY",
  "worker_node" : "54xOe0w8Qjyze00UuLDfdA",
  "create_time" : 1647545342556,
  "last_update_time" : 1647545342587,
  "is_async" : true
}
```

## 回應欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `model_id` | 字串 | ML 模型的唯一識別碼。任務完成時可使用。 |
| `task_type` | 字串 | ML 作業類型 (例如 `REGISTER_MODEL`、`DEPLOY_MODEL` 或 `TRAINING`)。 |
| `function_name` | 字串 | ML 函式類型 (例如 `TEXT_EMBEDDING` 或 `KMEANS`)。 |
| `state` | 字串 | 目前的任務狀態。有效值為 `CREATED` (已建立任務)、`RUNNING` (任務正在執行)、`COMPLETED` (任務順利完成)、`FAILED` (任務發生錯誤)、`CANCELLED` (任務已取消)、`COMPLETED_WITH_ERROR` (任務完成但有錯誤)、`CANCELLING` (任務正在取消)、`EXPIRED` (任務已過期)，以及 `UNREACHABLE` (任務節點無法連線)。 |
| `worker_node` | 陣列 | 執行任務之節點的節點 ID 陣列。 |
| `create_time` | Long | 建立任務時的時間戳記，以自 epoch 起算的毫秒為單位。 |
| `last_update_time` | Long | 上次狀態更新的時間戳記，以自 epoch 起算的毫秒為單位。 |
| `is_async` | 布林值 | 任務是否以非同步方式執行。ML 任務通常為 `true`。 |
| `input_type` | 字串 | 訓練任務的輸入類型 (例如 `SEARCH_QUERY`)。 |
