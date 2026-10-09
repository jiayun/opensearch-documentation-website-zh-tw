---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期索引名稱"
parent: Ingest processors
nav_order: 55
---

# 日期索引名稱處理器

`date_index_name` 處理器用於根據文件內的日期或時間戳記欄位，將文件指向正確的時間型索引。此處理器會將 `_index` 中繼資料欄位設定為[日期運算]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#date-math)索引名稱運算式。接著，處理器會從正在處理的文件中的 `field` 欄位擷取日期或時間戳記，並將其格式化為日期運算索引名稱運算式。擷取的日期、`index_name_prefix` 值與 `date_rounding` 值隨後會合併以建立日期運算索引運算式。例如，若 `field` 欄位包含值 `2023-10-30T12:43:29.000Z`，且 `index_name_prefix` 設定為 `week_index-`、`date_rounding` 設定為 `w`，則日期運算索引名稱運算式為 `week_index-2023-10-30`。您可以使用 `date_formats` 欄位來指定日期運算索引運算式中的日期應如何格式化。

以下是 `date_index_name` 處理器的語法：

```json
{
  "date_index_name": {
    "field": "your_date_field or your_timestamp_field",
    "date_rounding": "rounding_value"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `date_index_name` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 傳入文件中的日期或時間戳記欄位。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`date_rounding`  | 必要 | 索引名稱中日期的捨入單位。有效值為 `y`（年）、`M`（月）、`w`（週）、`d`（日）、`h`（小時）、`m`（分鐘）與 `s`（秒）。 |
`date_formats` | 選用 | 用於剖析日期或時間戳記欄位的日期格式陣列。有效選項包括 Java 時間模式，或下列格式之一：ISO8601、UNIX、UNIX_MS 或 TAI64N。預設為 `yyyy-MM-dd'T'HH:mm:ss.SSSXX`。 |
`index_name_format` | 選用 | 日期格式。預設為 `yyyy-MM-dd`。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`index_name_prefix` | 選用 | 要附加在日期之前的索引名稱前置詞。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。
`description`  | 選用  | 處理器的簡短描述。  |
`if` | 選用 | 執行此處理器的條件。 |
`ignore_failure` | 選用 | 若設定為 `true`，則會忽略失敗。預設為 `false`。 |
`locale` | `locale`  | 選用  | 剖析日期的月份名稱與星期幾時使用的地區設定。預設為 `ENGLISH`。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。  |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。在偵錯時有助於區分相同類型的處理器。 |
`timezone`  | 選用  | 剖析日期時使用的時區。預設為 `UTC`。 |

## 使用處理器

依照下列步驟在管線中使用此處理器。

**步驟 1：建立管線。**

下列查詢會建立名為 `date-index-name1` 的管線，使用 `date_index_name` 處理器將記錄檔編製索引至每月索引：

```json
PUT /_ingest/pipeline/date-index-name1
{
  "description": "Create weekly index pipeline",
  "processors": [
    {
      "date_index_name": {
        "field": "date_field",
        "index_name_prefix": "week_index-",
        "date_rounding": "w",
        "date_formats": ["YYYY-MM-DD"]
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2 (選用)：測試管線。**

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/date-index-name1/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "date_field": "2023-10-30"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "<week_index-{2023-10-01||/w{yyyy-MM-dd|UTC}}>",
        "_id": "1",
        "_source": {
          "date_field": "2023-10-30"
        },
        "_ingest": {
          "timestamp": "2023-11-13T18:23:10.408593092Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件。**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=date-index-name1
{
  "date_field": "2023-10-30"
}
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引至索引 `week_index-2023-10-23`，並且因為管線會以週為單位捨入日期，所有時間戳記落在該週內的文件都會編製索引至同一個索引。

```json
{
  "_index": "week_index-2023-10-30",
  "_id": "1",
  "_version": 4,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 3,
  "_primary_term": 1
}
```

**步驟 4（選用）：擷取文件。**

若要擷取文件，請執行下列查詢：

```json
GET week_index-2023-10-30/_doc/1
```
{% include copy-curl.html %}
