---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: gsub
parent: Ingest processors
nav_order: 125
---

<!-- vale off -->
# Gsub 處理器
<!-- vale on -->

`gsub` 處理器會對傳入文件中的字串欄位執行正規表示式搜尋並取代的操作。如果欄位包含字串陣列，該操作會套用至陣列中的所有元素。不過，如果欄位包含非字串的值，處理器會擲回例外狀況。`gsub` 處理器的使用案例包括從記錄訊息或使用者產生的內容中移除敏感資訊、將資料格式或慣例標準化（例如轉換日期格式、移除特殊字元），以及從欄位值中擷取或轉換子字串以進行後續處理或分析。

以下是 `gsub` 處理器的語法：

```json
"gsub": {
  "field": "field_name",
  "pattern": "regex_pattern",
  "replacement": "replacement_string"
}
```
{% include copy.html %}

## 組態參數

下表列出 `gsub` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 要套用取代作業的欄位。
`pattern` | 必要 | 要被取代的模式。
`replacement` | 必要 | 用來取代符合模式的字串。
`target_field` | 選用 | 用來儲存解析資料的欄位名稱。如果未指定 `target_field`，解析後的資料會取代 `field` 欄位中的原始資料。預設為 `field`。
`if` | 選用 | 執行處理器的條件。
`ignore_missing` | 選用 | 指定處理器是否應忽略不含指定欄位的文件。預設為 `false`。
`ignore_failure` | 選用 | 指定處理器遇到錯誤時是否仍繼續執行。如果設定為 `true`，則會忽略失敗。預設為 `false`。
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。

## 使用處理器

依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `gsub_pipeline` 的管線，該管線使用 `gsub` 處理器將 `message` 欄位中所有出現的 `error` 一詞取代為 `warning`：

```json
PUT _ingest/pipeline/gsub_pipeline
{
  "description": "Replaces 'error' with 'warning' in the 'message' field",
  "processors": [
    {
      "gsub": {
        "field": "message",
        "pattern": "error",
        "replacement": "warning"
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
POST _ingest/pipeline/gsub_pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "This is an error message"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "This is an warning message"
        },
        "_ingest": {
          "timestamp": "2024-05-22T19:47:00.645687211Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `logs` 的索引：

```json
PUT logs/_doc/1?pipeline=gsub_pipeline
{
  "message": "This is an error message"
}
```
{% include copy-curl.html %}

#### 回應

下列回應顯示請求已將文件編製索引至名為 `logs` 的索引，且 `gsub` 處理器已將 `message` 欄位中所有出現的 `error` 一詞取代為 `warning`：

```json
{
  "_index": "logs",
  "_id": "1",
  "_version": 1,
  "result": "created",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 0,
  "_primary_term": 1
}
```
{% include copy-curl.html %}

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET logs/_doc/1
```
{% include copy-curl.html %}

#### 回應

下列回應顯示 `message` 欄位值已修改的文件：

```json
{
  "_index": "logs",
  "_id": "1",
  "_version": 1,
  "_seq_no": 0,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "message": "This is an warning message"
  }
}
```
{% include copy-curl.html %}


