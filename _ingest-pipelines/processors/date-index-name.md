---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日期索引名稱"
parent: Ingest processors
nav_order: 55
---

# 日期索引名稱處理器

`date_index_name` 處理器用於根據文件中的日期或時間戳記欄位，將文件導向正確的時間型索引。此處理器會將 `_index` 中繼資料欄位設為[日期數學]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/#date-math)索引名稱運算式。接著，處理器會從正在處理的文件中的 `field` 欄位擷取日期或時間戳記，並將其格式化為日期數學索引名稱運算式。然後，將擷取的日期、`index_name_prefix` 值與 `date_rounding` 值組合，以建立日期數學索引運算式。例如，如果 `field` 欄位包含值 `2023-10-30T12:43:29.000Z`，且 `index_name_prefix` 設為 `week_index-`，而 `date_rounding` 設為 `w`，則日期數學索引名稱運算式為 `<week_index-{2023-10-30||/w{yyyy-MM-dd|UTC}}>`，會解析為 `week_index-2023-10-30` 索引。使用 `date_formats` 參數指定如何剖析文件中的日期，並使用 `index_name_format` 參數指定如何格式化索引名稱中的日期。

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

Parameter | Required/Optional | Description |
|-----------|-----------|-----------|
`field`  | Required  | 傳入文件中的日期或時間戳記欄位。 |
`date_rounding`  | Required | 索引名稱中日期捨入的時間單位。有效值為 `y` (年)、`M` (月)、`w` (週)、`d` (日)、`h` (小時)、`m` (分鐘) 與 `s` (秒)。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`date_formats` | Optional | 用於解析日期或時間戳記欄位的日期格式陣列。有效選項包括 Java 時間模式，或下列格式之一：ISO8601、UNIX、UNIX_MS 或 TAI64N。預設為 `yyyy-MM-dd'T'HH:mm:ss.SSSXX`。 |
`index_name_format` | Optional | 索引名稱中日期的格式。預設為 `yyyy-MM-dd`。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`index_name_prefix` | Optional | 在索引名稱中加在日期前面的前置詞。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。
`description`  | Optional  | 處理器的簡短描述。  |
`if` | Optional | 執行此處理器的條件。 |
`ignore_failure` | Optional | 若設為 `true`，則忽略失敗。預設為 `false`。 |
`locale`  | Optional  | 解析日期的月份名稱與星期幾時使用的地區設定。預設為 `ENGLISH`。  |
`on_failure` | Optional | 處理器失敗時要執行的處理器清單。 |
`tag` | Optional | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與除錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |
`timezone`  | Optional  | 用於解析日期，以及從日期數學運算式計算具體索引名稱時使用的時區。預設為 `UTC`。 |

## 使用處理器

請依照下列步驟在管線中使用此處理器。

**步驟 1：建立管線。**

下列查詢會建立一個名為 `date-index-name1` 的管線，該管線使用 `date_index_name` 處理器將記錄檔編製索引到每週索引中：

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
        "date_formats": ["yyyy-MM-dd"]
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2（選用）：測試管線。**

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

下列範例回應確認管線運作符合預期：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "<week_index-{2023-10-30||/w{yyyy-MM-dd|UTC}}>",
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

此請求會將文件編製索引到索引 `week_index-2023-10-30` 中，並且由於管線以週為單位進行捨入，所有時間戳記落在同一週內的文件都會被編製索引到同一個索引。

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
