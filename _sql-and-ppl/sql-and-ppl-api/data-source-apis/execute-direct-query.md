---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行直接查詢"
parent: Data source APIs
nav_order: 10
grand_parent: SQL and PPL API
---

# 執行直接查詢 API

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的最新進度或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/) 的討論。    
{: .warning}

使用資料來源的原生查詢語言，對外部資料來源執行查詢。

使用此 API 之前，您必須先設定資料來源。有關設定資料來源的資訊，請參閱 [資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。
{: .note}

## 端點

```json
POST /_plugins/_directquery/_query/{dataSource}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`dataSource` | 字串 | 要查詢之已設定資料來源的名稱。必要。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 以資料來源的原生查詢語言執行的查詢（例如 Prometheus 的 PromQL）。必要。
`language` | 字串 | 查詢語言。對於 Prometheus 資料來源，請使用 `PROMQL`。必要。
`options` | 物件 | 資料來源專屬的查詢選項。請參閱 [Prometheus 選項](#prometheus-options)。選用。
`maxResults` | 整數 | 要傳回的最大結果數量。僅適用於 Prometheus。選用。
`timeout` | 整數 | 查詢逾時時間（秒）。僅適用於 Prometheus。選用。
`sessionId` | 字串 | 用於追蹤查詢的工作階段識別碼。若未提供，將自動產生 UUID。選用。

### Prometheus 選項

下列選項專屬於 Prometheus 資料來源，應在 `options` 物件中提供。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`options.queryType` | 字串 | 查詢類型。有效值為 `instant` 或 `range`。預設為 `instant`。選用。
`options.time` | 字串 | 即時查詢的評估時間戳記，以 Unix 時間戳記指定。即時查詢時為必要。
`options.start` | 字串 | `range` 查詢的開始時間戳記，以 Unix 時間戳記指定。`range` 查詢時為必要。
`options.end` | 字串 | `range` 查詢的結束時間戳記，以 Unix 時間戳記指定。`range` 查詢時為必要。
`options.step` | 字串 | `range` 查詢的查詢解析步幅，以時間長度格式指定（例如 `15s`、`1m`、`1h`）。`range` 查詢時為必要。

## 範例請求：即時查詢

下列請求對 Prometheus 資料來源執行即時 PromQL 查詢：

```json
POST /_plugins/_directquery/_query/my_prometheus
{
  "query": "up",
  "language": "PROMQL",
  "options": {
    "queryType": "instant"
  }
}
```
{% include copy-curl.html %}

## 範例請求：範圍查詢

下列請求執行範圍查詢，以擷取一段時間內的 CPU 使用率：

```json
POST /_plugins/_directquery/_query/my_prometheus
{
  "query": "rate(node_cpu_seconds_total{mode=\"user\"}[5m])",
  "language": "PROMQL",
  "options": {
    "queryType": "range",
    "start": "2024-01-01T00:00:00Z",
    "end": "2024-01-01T01:00:00Z",
    "step": "60s"
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "queryId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "sessionId": "session-uuid-here",
  "results": {
    "status": "success",
    "data": {
      "resultType": "vector",
      "result": [
        {
          "metric": {
            "__name__": "up",
            "instance": "localhost:9090",
            "job": "prometheus"
          },
          "value": [1704067200, "1"]
        }
      ]
    }
  }
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`queryId` | 字串 | 已執行查詢的唯一識別碼。
`sessionId` | 字串 | 用於追蹤相關查詢的工作階段識別碼。
`results` | 物件 | 來自資料來源的查詢結果，以資料來源的原生回應格式傳回。
