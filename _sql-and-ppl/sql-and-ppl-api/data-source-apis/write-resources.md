---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "寫入資源"
parent: Data source APIs
nav_order: 30
grand_parent: SQL and PPL API
---

# 寫入資源 API

這是實驗性功能，不建議在正式環境中使用。如需此功能的最新進展，或想提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/)的討論。    
{: .warning}

在外部資料來源中建立或修改資源。支援在 Prometheus Alertmanager 中建立警示靜音。

使用此 API 之前，您必須設定資料來源。如需設定資料來源的相關資訊，請參閱[資料來源]({{site.url}}{{site.baseurl}}/dashboards/management/data-sources/)。
{: .note}

## 端點

```http
POST /_plugins/_directquery/_resources/{dataSource}/alertmanager/api/v2/{resourceType}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`dataSource` | 字串 | 已設定資料來源的名稱。必要。
`resourceType` | 字串 | 要建立的資源類型。唯一支援的值為 `silences`。必要。

## Alertmanager 靜音請求本文欄位

請求本文會傳遞至外部資料來源 API。下列欄位適用於建立 Alertmanager 靜音時。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`matchers` | 陣列 | 一組標籤比對規則的陣列，用於決定靜音套用的警示。必要。
`matchers[].name` | 字串 | 要比對的標籤名稱。必要。
`matchers[].value` | 字串 | 要比對的標籤值。必要。
`matchers[].isRegex` | 布林值 | 此值是否為正規表示式。預設為 `false`。選用。
`matchers[].isEqual` | 布林值 | 要比對相等（`true`）或不相等（`false`）。預設為 `true`。選用。
`startsAt` | 字串 | 靜音的開始時間，採用 ISO 8601 格式。必要。
`endsAt` | 字串 | 靜音的結束時間，採用 ISO 8601 格式。必要。
`createdBy` | 字串 | 靜音的作者。必要。
`comment` | 字串 | 描述靜音原因的註解。必要。

## 範例請求：建立警示靜音

```json
POST /_plugins/_directquery/_resources/my_prometheus/alertmanager/api/v2/silences
{
  "matchers": [
    {
      "name": "alertname",
      "value": "HighMemoryUsage",
      "isRegex": false,
      "isEqual": true
    },
    {
      "name": "instance",
      "value": "server1:9100",
      "isRegex": false,
      "isEqual": true
    }
  ],
  "startsAt": "2024-01-01T12:00:00.000Z",
  "endsAt": "2024-01-01T14:00:00.000Z",
  "createdBy": "admin",
  "comment": "Scheduled maintenance window"
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "silenceID": "a1b2c3d4-e5f6-7890-abcd-ef1234567890"
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`silenceID` | 字串 | 所建立靜音的唯一識別碼。
