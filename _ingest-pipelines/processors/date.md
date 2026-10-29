---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期"
parent: Ingest processors
nav_order: 50
redirect_from:
   - /api-reference/ingest-apis/processors/date/
---

本文件說明在 OpenSearch 資料匯入管線中使用 `date` 處理器的方法。如果您的使用情境涉及大型或複雜的資料集，請考慮使用在 OpenSearch 叢集外部執行的 [Data Prepper `date` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/date/)。
{: .note}

# 日期處理器

`date` 處理器用於從文件欄位剖析日期，並將剖析後的資料新增至新欄位。根據預設，剖析後的資料會儲存在 `@timestamp` 欄位中。

## 語法

以下是 `date` 處理器的語法：

```json
{
  "date": {
    "field": "date_field",
    "formats": ["yyyy-MM-dd'T'HH:mm:ss.SSSZZ"]
  }
}
```
{% include copy.html %}

## 參數

下表列出 `date` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含待轉換資料的欄位名稱。 |
`formats`  | 必要 | 預期日期格式的陣列。處理器會依指定順序嘗試每種格式。如果有多種格式可解析該日期，則由最後一個符合的格式決定結果。可以是[日期格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#formats)或下列其中一種格式：ISO8601、UNIX、UNIX_MS 或 TAI64N。  |
`description`  | 選用  | 處理器的簡要說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器遇到錯誤時是否仍繼續執行。若設為 `true`，則忽略失敗。預設為 `false`。 |
`locale`  | 選用  | 解析日期時使用的地區設定。若未指定，則使用根語系 (root locale)，以解析英文的月份與星期名稱。支援[範本程式碼片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。  |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`output_format` | 選用 | 目標欄位使用的[日期格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#formats)。預設為 `yyyy-MM-dd'T'HH:mm:ss.SSSXXX`，例如 `2023-06-30T00:00:00.000Z`。 |
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與除錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |
`target_field`  | 選用  | 儲存已解析資料的欄位名稱。預設目標欄位為 `@timestamp`。 | 
`timezone`  | 選用  | 解析日期時使用的時區。預設為 `UTC`。支援[範本程式碼片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |

## 使用處理器

依照下列步驟，在管線中使用此處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `date-output-format` 的管線，使用 `date` 處理器將歐洲日期格式轉換為美國日期格式，並新增欄位 `date_us`，其 `output_format` 為所需值：

```json
PUT /_ingest/pipeline/date-output-format
{
  "description": "Pipeline that converts European date format to US date format",
  "processors": [
    {
      "date": {
        "field" : "date_european",
        "formats" : ["dd/MM/yyyy", "UNIX"],
        "target_field": "date_us",
        "output_format": "MM/dd/yyy",
        "timezone" : "UTC"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/date-output-format/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "date_european": "30/06/2023"
      }
    }
  ]
}
```
{% include copy-curl.html %}

下列範例回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "date_us": "06/30/2023",
          "date_european": "30/06/2023"
        },
        "_ingest": {
          "timestamp": "2023-08-22T17:08:46.275195504Z"
        }
      }
    }
  ]
}
```

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=date-output-format
{
  "date_european": "30/06/2023"
}
```
{% include copy-curl.html %}

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

回應中包含已匯入的文件，其轉換結果如步驟 2 的回應所示。

## 使用文件中的時區與地區設定

由於 `timezone` 和 `locale` 參數支援範本片段，您可以從正在處理的文件欄位中讀取這些值。當文件來自不同地區的來源時，這項功能非常實用。下列請求會使用儲存在 `store` 物件中的時區與地區設定，剖析法文日期字串：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "date": {
          "field": "order_date",
          "formats": ["dd MMMM yyyy HH:mm"],
          "timezone": "{% raw %}{{{store.timezone}}}{% endraw %}",
          "locale": "{% raw %}{{{store.locale}}}{% endraw %}"
        }
      }
    ]
  },
  "docs": [
    {
      "_source": {
        "order_date": "14 octobre 2026 09:30",
        "store": {
          "timezone": "Europe/Paris",
          "locale": "fr"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應顯示，日期是使用法文月份名稱和巴黎時區剖析的：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "order_date": "14 octobre 2026 09:30",
          "store": {
            "locale": "fr",
            "timezone": "Europe/Paris"
          },
          "@timestamp": "2026-10-14T09:30:00.000+02:00"
        },
        "_ingest": {
          "timestamp": "2026-10-14T20:32:15.764960761Z"
        }
      }
    }
  ]
}
```
