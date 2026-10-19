---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除管線"
nav_order: 13
redirect_from:
  - /opensearch/rest-api/ingest-apis/delete-ingest/
  - /api-reference/ingest-apis/delete-ingest/
---

# 刪除管線 API
**於 1.0 版推出**
{: .label .label-purple }

刪除管線 API 會刪除一或多個資料匯入管線。若某個索引將已刪除的管線作為其預設或最終管線，則在您更新該索引的設定之前，對該索引的編製索引請求都會失敗。

## 端點

```json
DELETE /_ingest/pipeline/{pipeline-id}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 必要 | 資料類型 | 說明
:--- | :--- | :--- | :---
`pipeline-id` | 必要 | 字串 | 要刪除的管線 ID。支援萬用字元運算式，例如 `logs-*`。若要刪除叢集中的所有管線，請使用 `*`。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | Time | 等待與叢集管理員節點建立連線的時間長度。預設為 `30s`。
`timeout` | Time | 等待回應的時間長度。預設為 `30s`。

## 範例請求

下列請求會刪除 `my-pipeline` 管線：

```json
DELETE /_ingest/pipeline/my-pipeline
```
{% include copy-curl.html %}

下列請求會刪除所有 ID 以 `logs-` 開頭的管線：

```json
DELETE /_ingest/pipeline/logs-*
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "acknowledged": true
}
```

如果沒有管線符合指定的 ID，API 會傳回 `404` 錯誤。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/ingest/pipeline/delete`。
