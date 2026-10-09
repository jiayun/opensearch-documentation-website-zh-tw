---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期"
parent: Ingest processors
nav_order: 50
redirect_from:
   - /api-reference/ingest-apis/processors/date/
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `date` 處理器。如果您的使用情境涉及大型或複雜的資料集，請考慮使用 [Data Prepper `date` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/date/)，其執行於 OpenSearch 叢集上。
{: .note}

# 日期處理器

`date` 處理器用於從文件欄位剖析日期，並將剖析後的資料新增至新欄位。根據預設，剖析後的資料會儲存在 `@timestamp` 欄位中。

## 語法範例

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

## 組態參數

下表列出 `date` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含要轉換之資料的欄位名稱。支援 [範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`formats`  | 必要 | 預期日期格式的陣列。可以是 [日期格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#formats) 或下列其中一種格式：ISO8601、UNIX、UNIX_MS 或 TAI64N。  |
`description`  | 選用  | 處理器的簡短描述。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |
`locale`  | 選用  | 剖析日期時要使用的地區設定。預設為 `ENGLISH`。支援 [範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。  |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`output_format` | 選用 | 要用於目標欄位的 [日期格式]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#formats)。預設為 `yyyy-MM-dd'T'HH:mm:ss.SSSZZ`。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。 |
`target_field`  | 選用  | 用來儲存剖析後資料的欄位名稱。預設目標欄位為 `@timestamp`。 | 
`timezone`  | 選用  | 剖析日期時要使用的時區。預設為 `UTC`。支援 [範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `date-output-format` 的管線，其使用 `date` 處理器將歐洲日期格式轉換為美國日期格式，並新增具有所需 `output_format` 的新欄位 `date_us`：

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

**步驟 2 (選用)：測試管線**

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
        "date_us": "06/30/2023",
        "date_european": "30/06/2023"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認管線運作正常：

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

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=date-output-format
{
  "date_european": "30/06/2023"
}
```
{% include copy-curl.html %}

**步驟 4 (選用)：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
