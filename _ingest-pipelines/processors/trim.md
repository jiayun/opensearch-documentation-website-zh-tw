---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Trim
parent: Ingest processors
nav_order: 300
---

# Trim 處理器

`trim` 處理器可用來移除指定欄位開頭與結尾的空白字元。值內部的空白不會被移除。對於陣列欄位，處理器會修剪每個字串元素。

以下是 `trim` 處理器的語法：

```json
{
  "trim": {
    "field": "field_to_trim",
    "target_field": "trimmed_field"
  }
}
```
{% include copy.html %}

## 參數

下表列出 `trim` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明
:---|:---|:---
`field` | 必要 | 包含要修剪文字之欄位。
`target_field` | 選用 | 儲存修剪後文字的欄位。若未指定，則會就地更新該欄位。
`ignore_missing` | 選用 | 指定處理器是否應忽略不包含指定欄位的文件。若設為 `true`，則處理器會忽略欄位中缺少的值，並保持 `target_field` 不變。預設為 `false`。
`description` | 選用 | 處理器的簡短說明。
`if` | 選用 | 執行處理器的條件。
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `trim_pipeline` 的管線，該管線使用 `trim` 處理器移除 `raw_text` 欄位開頭與結尾的空白，並將修剪後的文字儲存在 `trimmed_text` 欄位中： 

```json
PUT _ingest/pipeline/trim_pipeline
{
  "description": "Trim leading and trailing white space",
  "processors": [
    {
      "trim": {
        "field": "raw_text",
        "target_field": "trimmed_text"
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
POST _ingest/pipeline/trim_pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "raw_text": "   Hello, world!   "
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
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "raw_text": "   Hello, world!   ",
          "trimmed_text": "Hello, world!"
        },
        "_ingest": {
          "timestamp": "2024-04-26T20:58:17.418006805Z"
        }
      }
    }
  ]
}
```

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=trim_pipeline
{
  "raw_text": "   Hello, world!   "
}
```
{% include copy-curl.html %}

此請求會將文件編製索引至 `testindex1` 索引。`trim_pipeline` 會修剪 `raw_text` 值，並將結果儲存在 `trimmed_text` 欄位中，如下列回應所示：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 68,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 70,
  "_primary_term": 47
}
```

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

回應包含已匯入的文件，其轉換結果如步驟 2 的回應所示。
