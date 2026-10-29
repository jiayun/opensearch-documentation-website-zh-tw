---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分割"
parent: Ingest processors
nav_order: 255
---

# Split 資料匯入處理器

`split` 處理器用來根據指定的分隔符，將字串欄位分割成子字串陣列。

以下是 `split` 處理器的語法：

```json
{
  "split": {
    "field": "field_to_split",
    "separator": "<delimiter>",
    "target_field": "split_field"
  }
}
```
{% include copy.html %}

## 參數

下表列出 `split` 處理器的必要與選用參數。

參數  | 必要/選用  | 描述 
:--- | :--- | :--- 
`field` | 必要 | 包含要分割字串的欄位。 
`separator` | 必要 | 符合分割字串所用分隔符號的規則運算式。若要依規則運算式中具有特殊意義的字元分割，例如 `.` 或 `+`，必須加以跳脫，例如 `\\.`。 
`preserve_trailing` | 選用 | 若設為 `true`，則在產生的陣列中保留空的結尾欄位（例如 `''`）。若設為 `false`，則會從產生的陣列中移除空的結尾欄位。預設為 `false`。 
`target_field` | 選用 | 儲存子字串陣列的欄位。若未指定，則會就地更新該欄位。 
`ignore_missing` | 選用	| 指定處理器是否應忽略不含指定欄位的文件。若設為 `true`，處理器會忽略欄位中缺少的值，並保持 `target_field` 不變。預設為 `false`。  
`description` | 選用 | 處理器的簡短描述。 
`if` | 選用 | 執行處理器的條件。 
`ignore_failure` | 選用 | 指定處理器在遇到錯誤時是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 
`tag` | 選用 | 處理器的識別標籤。有助於偵錯時區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

## 使用處理器

依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `split_pipeline` 的管線，使用 `split` 處理器依逗號字元分割 `log_message` 欄位，並將結果陣列儲存在 `log_parts` 欄位：

```json
PUT _ingest/pipeline/split_pipeline
{
  "description": "Split log messages by comma",
  "processors": [
    {
      "split": {
        "field": "log_message",
        "separator": ",",
        "target_field": "log_parts"
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
POST _ingest/pipeline/split_pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "log_message": "error,warning,info"
      }
    }
  ]
}
```
{% include copy-curl.html %}

下列範例回應可確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "log_message": "error,warning,info",
          "log_parts": [
            "error",
            "warning",
            "info"
          ]
        },
        "_ingest": {
          "timestamp": "2024-04-26T22:29:23.207849376Z"
        }
      }
    }
  ]
}
```

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=split_pipeline
{
  "log_message": "error,warning,info"
}
```
{% include copy-curl.html %}

此請求會將文件編製索引到 `testindex1` 索引中，並在編製索引前以逗號分隔符切割 `log_message` 欄位，再將結果儲存在 `log_parts` 欄位中，如下列回應所示：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 70,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 72,
  "_primary_term": 47
}
```

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

回應會包含已匯入的文件，並如步驟 2 的回應所示經過轉換。

## 保留尾端空欄位

根據預設，`split` 處理器會從產生的陣列中移除尾端的空元素。下列請求分別在有無 `preserve_trailing` 的情況下分割相同的值：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "split": {
          "field": "colors",
          "separator": ","
        }
      },
      {
        "split": {
          "field": "colors_preserved",
          "separator": ",",
          "preserve_trailing": true
        }
      }
    ]
  },
  "docs": [
    {
      "_source": {
        "colors": "red,green,,",
        "colors_preserved": "red,green,,"
      }
    }
  ]
}
```
{% include copy-curl.html %}

在回應中，`colors` 陣列只包含兩個非空元素，而 `colors_preserved` 陣列還包含兩個尾端空元素：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "colors": ["red", "green"],
          "colors_preserved": ["red", "green", "", ""]
        },
        "_ingest": {
          "timestamp": "2026-10-14T19:44:03.298240422Z"
        }
      }
    }
  ]
}
```
