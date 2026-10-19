---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "URL 解碼"
parent: Ingest processors
nav_order: 320
---

# URL 解碼處理器

`urldecode` 處理器適合用來解碼記錄資料或其他文字欄位中經 URL 編碼的字串。這能讓資料更易讀、更容易分析，尤其是在處理含有特殊字元或空格的 URL 或查詢參數時。對於陣列欄位，處理器會逐一解碼每個字串元素。百分比編碼字元和加號都會被解碼；例如 `wireless+mouse%21` 會變成 `wireless mouse!`。

以下是 `urldecode` 處理器的語法：

```json
{
  "urldecode": {
    "field": "field_to_decode",
    "target_field": "decoded_field"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `urldecode` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含待解碼 URL 編碼字串的欄位。 |
`target_field`  | 選用  | 儲存解碼後字串的欄位。若未指定，則解碼後的字串會儲存在與原始編碼字串相同的欄位中。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略未包含所指定 `field` 的文件。若設為 `true`，則處理器會忽略 `field` 中缺少的值，並讓 `target_field` 保持不變。預設值為 `false`。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設值為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於偵錯時區分相同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |

## 使用處理器

依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `urldecode_pipeline` 的管線，使用 `urldecode` 處理器解碼 `encoded_url` 欄位中經過 URL 編碼的字串，並將解碼後的字串儲存在 `decoded_url` 欄位中：

```json
PUT _ingest/pipeline/urldecode_pipeline
{
  "description": "Decode URL-encoded strings",
  "processors": [
    {
      "urldecode": {
        "field": "encoded_url",
        "target_field": "decoded_url"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2（選用）：測試管線

建議您在匯入文件前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/urldecode_pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "encoded_url": "https://example.com/search?q=hello%20world"
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
          "decoded_url": "https://example.com/search?q=hello world",
          "encoded_url": "https://example.com/search?q=hello%20world"
        },
        "_ingest": {
          "timestamp": "2024-04-25T23:16:44.886165001Z"
        }
      }
    }
  ]
}
```

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=urldecode_pipeline
{
  "encoded_url": "https://example.com/search?q=url%20decode%20test"
}
```
{% include copy-curl.html %}

#### 回應

上述請求會將文件編製索引到 `testindex1` 索引中。`urldecode_pipeline` 會解碼 `encoded_url` 值，並將結果儲存在 `decoded_url` 欄位中，如下列回應所示：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 67,
  "result": "updated",
  "_shards": {
    "total": 2,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 68,
  "_primary_term": 47
}
```

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

#### 回應

回應包含原始 `encoded_url` 欄位與 `decoded_url` 欄位：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 67,
  "_seq_no": 68,
  "_primary_term": 47,
  "found": true,
  "_source": {
    "decoded_url": "https://example.com/search?q=url decode test",
    "encoded_url": "https://example.com/search?q=url%20decode%20test"
  }
}
```
