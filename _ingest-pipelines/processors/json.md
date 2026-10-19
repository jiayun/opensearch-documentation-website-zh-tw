---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: JSON
parent: Ingest processors
nav_order: 170
---

# JSON 處理器

`json` 處理器會將 JSON 格式的字串解析為結構化資料，這對於各種資料處理與擴充任務相當有用。此處理器會解析所有 JSON 資料類型：物件、陣列、字串、數字、布林值以及 `null`。例如，字串 `"[1,2,3]"` 會解析為陣列，而字串 `"42"` 會解析為數字。

以下是 `json` 處理器的語法：

```json
{
  "json": {
    "field": "<field_name>",
    "target_field": "<target_field_name>",
    "add_to_root": <boolean>
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `json` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 包含要還原序列化之 JSON 格式字串的欄位名稱。
`target_field` | 選用 | 儲存還原序列化後 JSON 資料的欄位名稱。若未提供，資料會儲存在 `field` 欄位。若 `target_field` 已存在，其現有值會被新的 JSON 資料覆寫。
`add_to_root` | 選用 | 布林值旗標，決定還原序列化後的 JSON 資料應加入文件根層級 (`true`)，還是儲存在 target_field 中 (`false`)。若 `add_to_root` 為 `true`，則 `target_field` 無效。解析出的欄位會覆寫同名根欄位。若 `add_to_root` 為 `true` 且解析出的值不是 JSON 物件，處理器會失敗。預設值為 `false`。
`description` | 選用 | 處理器用途或組態的描述。
`if` | 選用 | 指定要有條件地執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure`| 選用 | 指定當處理器在執行期間失敗時要執行的處理器清單。這些處理器會依指定順序執行。
`tag` | 選用 | 處理器的識別標籤。在偵錯時可用於區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `my-json-pipeline` 的管線，該管線使用 `json` 處理器來處理 JSON 資料，並以額外資訊擴充文件：

```json
PUT _ingest/pipeline/my-json-pipeline
{
  "description": "Example pipeline using the JsonProcessor",
  "processors": [
    {
      "json": {
        "field": "raw_data",
        "target_field": "parsed_data",
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
        "value": "{% raw %}{{_ingest.timestamp}}{% endraw %}"
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

以下範例回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "processed_timestamp": "2024-05-30T15:24:48.064472090Z",
          "raw_data": "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}",
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
          "raw_data": "{\"name\":\"Jane\",\"age\":25,\"city\":\"Los Angeles\"}",
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

### 步驟 3：匯入文件 

以下查詢會將文件匯入名為 `my-index` 的索引：

```json
PUT my-index/_doc/1?pipeline=my-json-pipeline
{
  "raw_data": "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}"
}
```
{% include copy-curl.html %}

#### 回應

回應會確認包含 `raw_data` 欄位 JSON 資料的文件已成功編製索引：

```json
{
  "_index": "my-index",
  "_id": "1",
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

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET my-index/_doc/1
```
{% include copy-curl.html %}
