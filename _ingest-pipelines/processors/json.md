---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: JSON
parent: Ingest processors
nav_order: 170
---

# JSON 處理器

`json` 處理器會將字串值欄位序列化為巢狀對應表，這對於各種資料處理與擴充任務相當實用。

以下是 `json` 處理器的語法：

```json
{
  "processor": {
    "json": {
      "field": "<field_name>",
      "target_field": "<target_field_name>",
      "add_to_root": <boolean>
    }
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `json` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 包含要還原序列化之 JSON 格式字串的欄位名稱。
`target_field` | 選用 | 儲存還原序列化 JSON 資料的欄位名稱。未提供時，資料會儲存在 `field` 欄位中。若 `target_field` 已存在，其現有值會以新的 JSON 資料覆寫。
`add_to_root` | 選用 | 布林值旗標，決定還原序列化的 JSON 資料應加入文件根層級 (`true`) 或儲存在 target_field (`false`) 中。若 `add_to_root` 為 `true`，則 `target-field` 無效。預設值為 `false`。 
`description` | 選用 | 處理器用途或組態的說明。
`if` | 選用 | 指定以條件方式執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure`| 選用 | 指定處理器在執行期間失敗時要執行的一組處理器。這些處理器會依指定的順序執行。 
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `my-json-pipeline` 的管線，該管線使用 `json` 處理器來處理 JSON 資料，並以其他資訊擴充文件： 

```json
PUT _ingest/pipeline/my-json-pipeline
{
  "description": "Example pipeline using the JsonProcessor",
  "processors": [
    {
      "json": {
        "field": "raw_data",
        "target_field": "parsed_data"
        "on_failure": [
          {
            "set": {
              "field": "error_message",
              "value": "Failed to parse JSON data"
            }
          },
          {
            "fail": {
              "message": "Failed to process JSON data"
            }
          }
        ]
      }
    },
    {
      "set": {
        "field": "processed_timestamp",
        "value": "{{_ingest.timestamp}}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2 (選用)：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/my-json-pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "raw_data": "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}"
      }
    },
    {
      "_source": {
        "raw_data": "{\"name\":\"Jane\",\"age\":25,\"city\":\"Los Angeles\"}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "processed_timestamp": "2024-05-30T15:24:48.064472090Z",
          "raw_data": """{"name":"John","age":30,"city":"New York"}""",
          "parsed_data": {
            "name": "John",
            "city": "New York",
            "age": 30
          }
        },
        "_ingest": {
          "timestamp": "2024-05-30T15:24:48.06447209Z"
        }
      }
    },
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "processed_timestamp": "2024-05-30T15:24:48.064543006Z",
          "raw_data": """{"name":"Jane","age":25,"city":"Los Angeles"}""",
          "parsed_data": {
            "name": "Jane",
            "city": "Los Angeles",
            "age": 25
          }
        },
        "_ingest": {
          "timestamp": "2024-05-30T15:24:48.064543006Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3：匯入文件 

下列查詢會將文件匯入名為 `my-index` 的索引：

```json
POST my-index/_doc?pipeline=my-json-pipeline
{
  "raw_data": "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}"
}
```
{% include copy-curl.html %}

#### 回應

回應確認包含 `raw_data` 欄位中 JSON 資料的文件已成功編製索引：

```json
{
  "_index": "my-index",
  "_id": "mo8yyo8BwFahnwl9WpxG",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 3,
  "_primary_term": 2
}
```
{% include copy-curl.html %}

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET my-index/_doc/1
```
{% include copy-curl.html %}
