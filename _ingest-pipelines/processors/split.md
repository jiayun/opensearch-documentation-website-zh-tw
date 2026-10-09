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

## 組態參數

下表列出 `split` 處理器的必要與選用參數。

參數  | 必要／選用  | 說明 
:--- | :--- | :--- 
`field` | 必要 | 包含要分割字串的欄位。 
`separator` | 必要 | 用來分割字串的分隔符。可以是正規表示式模式。 
`preserve_trailing` | 選用 | 若設為 `true`，則會在結果陣列中保留空的結尾欄位 (例如 `''`)。若設為 `false`，則會從結果陣列中移除空的結尾欄位。預設為 `false`。 
`target_field` | 選用 | 儲存子字串陣列的欄位。若未指定，則會就地更新該欄位。 
`ignore_missing` | 選用	| 指定處理器是否應忽略不含指定欄位的文件。若設為 `true`，則處理器會忽略欄位中缺少的值，並保持 `target_field` 不變。預設為 `false`。  
`description` | 選用 | 處理器的簡短描述。 
`if` | 選用 | 執行處理器的條件。 
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤也繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。 

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

### 步驟 2 (選用)：測試管線

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

#### 回應

下列範例回應確認管線如預期運作：

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
{% include copy-curl.html %}

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=split_pipeline
{
  "log_message": "error,warning,info"
}
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引到索引 `testindex1`，並在編製索引前依逗號分隔符分割 `log_message` 欄位，如下列回應所示：

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

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 回應

回應顯示 `log_message` 欄位為依逗號分隔符分割後的值陣列：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 70,
  "_seq_no": 72,
  "_primary_term": 47,
  "found": true,
  "_source": {
    "log_message": "error,warning,info",
    "log_parts": [
      "error",
      "warning",
      "info"
    ]
  }
}
```
