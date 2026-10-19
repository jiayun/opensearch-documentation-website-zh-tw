---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得管線"
nav_order: 12
redirect_from:
  - /opensearch/rest-api/ingest-apis/get-ingest/
  - /api-reference/ingest-apis/get-ingest/
---

# Get Pipeline API
**1.0 版推出**
{: .label .label-purple }

Get Pipeline API 會傳回一或多個資料匯入管線的定義。

## 端點

```json
GET /_ingest/pipeline
GET /_ingest/pipeline/{pipeline-id}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`pipeline-id` | 字串 | 要擷取的管線 ID 清單，以逗號分隔。支援萬用字元運算式。若未指定，API 會傳回叢集中的所有管線。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`cluster_manager_timeout` | 時間 | 等待連線至叢集管理員節點的時間。預設值為 `30s`。

## 請求範例

下列請求會傳回 `my-pipeline` 管線的定義：

```json
GET /_ingest/pipeline/my-pipeline
```
{% include copy-curl.html %}

下列請求會傳回 ID 以 `logs-` 開頭的所有管線，以及 `orders-pipeline` 管線的定義：

```json
GET /_ingest/pipeline/logs-*,orders-pipeline
```
{% include copy-curl.html %}

若只要擷取管線的版本，請使用 `filter_path` 查詢參數篩選回應。如需詳細資訊，請參閱[管線版本管理]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#pipeline-versioning)。

```json
GET /_ingest/pipeline/my-pipeline?filter_path=*.version
```
{% include copy-curl.html %}

## 回應範例

回應包含每個所請求管線的定義，以管線 ID 作為鍵值：

```json
{
  "my-pipeline": {
    "description": "This pipeline processes student data",
    "processors": [
      {
        "set": {
          "description": "Sets the graduation year to 2023",
          "field": "grad_year",
          "value": 2023
        }
      },
      {
        "set": {
          "description": "Sets graduated to true",
          "field": "graduated",
          "value": true
        }
      },
      {
        "uppercase": {
          "field": "name"
        }
      }
    ]
  }
}
```

如果沒有管線符合指定的 ID，API 會傳回空物件以及 `404` 狀態碼。

## 回應本文欄位

回應中針對每個傳回的管線包含一個物件，並以管線 ID 命名。每個管線物件包含下列欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`description` | 字串 | 管線的描述。僅在管線有描述時傳回。
`version` | 整數 | 管線的版本。僅在管線有版本時傳回。
`processors` | 物件陣列 | 管線中的處理器，依其執行順序排列。
`on_failure` | 物件陣列 | 當管線中的處理器失敗時執行的處理器。僅在管線定義了管線層級的失敗處理時傳回。

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/ingest/pipeline/get`。
