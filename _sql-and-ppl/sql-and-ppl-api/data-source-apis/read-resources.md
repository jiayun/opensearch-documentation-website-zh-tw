---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "讀取資源"
parent: Data source APIs
nav_order: 20
grand_parent: SQL and PPL API
---

# Read Resources API

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的進度或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/) 的討論。    
{: .warning}

從外部資料來源擷取中繼資料與資源。此 API 提供對 Prometheus 與 Alertmanager 的標籤、時間序列、警示及其他中繼資料的存取。

使用此 API 之前，您必須先設定資料來源。關於設定資料來源的資訊，請參閱 [資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。
{: .note}

## 端點

Read Resources API 針對不同的資源類型支援多個端點：

```json
GET /_plugins/_directquery/_resources/{dataSource}/api/v1/{resourceType}
GET /_plugins/_directquery/_resources/{dataSource}/api/v1/{resourceType}/{resourceName}/values
GET /_plugins/_directquery/_resources/{dataSource}/alertmanager/api/v2/{resourceType}
GET /_plugins/_directquery/_resources/{dataSource}/alertmanager/api/v2/alerts/groups
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`dataSource` | 字串 | 已設定的資料來源名稱。必要。
`resourceType` | 字串 | 要擷取的資源類型。請參閱 [支援的資源類型](#supported-resource-types)。必要。
`resourceName` | 字串 | 特定資源的名稱（例如擷取標籤值時的標籤名稱）。使用標籤值端點時為必要參數。

## 支援的資源類型

Prometheus 資料來源支援下列資源類型。

資源類型 | 端點 | 說明
:--- | :--- | :---
`labels` | `/api/v1/labels` | 擷取所有標籤名稱。
`label` | `/api/v1/label/{labelName}/values` | 擷取特定標籤的值。
`metadata` | `/api/v1/metadata` | 擷取指標中繼資料。
`series` | `/api/v1/series` | 擷取符合選擇器的時間序列。
`alerts` | `/alertmanager/api/v2/alerts` | 從 Alertmanager 擷取作用中的警示。
`silences` | `/alertmanager/api/v2/silences` | 從 Alertmanager 擷取警示靜默。
`receivers` | `/alertmanager/api/v2/receivers` | 擷取 Alertmanager 接收器。

## Prometheus 查詢參數

下列查詢參數專屬於 Prometheus 與 Alertmanager 資料來源。這些參數會傳遞至底層的資料來源 API。

參數   | 資料類型 | 說明
:---|:---|:---
`start`     | 字串    | 用於篩選結果的起始時間戳記，採 ISO 8601 格式。選用。
`end`       | 字串    | 用於篩選結果的結束時間戳記，採 ISO 8601 格式。選用。
`match[]`   | 字串    | 用於篩選結果的時間序列選擇器（僅適用於 series 端點）。選用。
`active`    | 布林值   | 依作用中狀態篩選警示（僅適用於 Alertmanager）。選用。
`silenced`  | 布林值   | 依靜默狀態篩選警示（僅適用於 Alertmanager）。選用。
`filter`    | 字串    | 用於比對靜默的篩選運算式（僅適用於 Alertmanager）。選用。

## 範例請求：取得所有標籤

```http
GET /_plugins/_directquery/_resources/my_prometheus/api/v1/labels
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "status": "success",
  "data": [
    "__name__",
    "instance",
    "job",
    "mode",
    "cpu"
  ]
}
```

## 範例請求：取得特定標籤的值

```http
GET /_plugins/_directquery/_resources/my_prometheus/api/v1/label/job/values
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "status": "success",
  "data": [
    "prometheus",
    "node_exporter",
    "alertmanager"
  ]
}
```

## 範例請求：取得作用中的警示

```http
GET /_plugins/_directquery/_resources/my_prometheus/alertmanager/api/v2/alerts?active=true&silenced=false
```
{% include copy-curl.html %}

## 範例回應

```json
[
  {
    "labels": {
      "alertname": "HighMemoryUsage",
      "instance": "server1:9100",
      "severity": "warning"
    },
    "annotations": {
      "summary": "High memory usage detected"
    },
    "startsAt": "2024-01-01T10:00:00.000Z",
    "status": {
      "state": "active"
    }
  }
]
```

## 範例請求：取得警示靜默

```http
GET /_plugins/_directquery/_resources/my_prometheus/alertmanager/api/v2/silences
```
{% include copy-curl.html %}
