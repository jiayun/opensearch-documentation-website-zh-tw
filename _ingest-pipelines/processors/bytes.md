---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Bytes
parent: Ingest processors
nav_order: 20
redirect_from:
   - /api-reference/ingest-apis/processors/bytes/
---

# Bytes 處理器

`bytes` 處理器會將人類可讀的位元組值轉換為其對應的位元組數值。該欄位可以是純量或陣列。若欄位為純量，則轉換該值並儲存於欄位中。若欄位為陣列，則轉換陣列中的所有值。

### 語法

以下是 `bytes` 處理器的語法：

```json
{
    "bytes": {
        "field": "your_field_name"
    }
}
```
{% include copy.html %}

## 組態參數

下表列出 `bytes` 處理器的必要與選用參數。

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含要轉換之資料的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則忽略失敗。預設為 `false`。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不包含所指定欄位的文件。若設為 `true`，則當欄位不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。 |
`target_field`  | 選用  | 儲存解析後資料的欄位名稱。若未指定，則該值會就地儲存於 `field` 欄位中。預設為 `field`。  |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `file_upload` 的管線，其中包含一個 `bytes` 處理器。它會將 `file_size` 轉換為其對應的位元組數值，並儲存於名為 `file_size_bytes` 的新欄位中：

```json
PUT _ingest/pipeline/file_upload
{
  "description": "Pipeline that converts file size to bytes",
  "processors": [
    {
      "bytes": {
        "field": "file_size",
        "target_field": "file_size_bytes"
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
POST _ingest/pipeline/file_upload/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "file_size_bytes": "10485760",
        "file_size":
          "10MB"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "event_types": [
            "event_type"
          ],
          "file_size_bytes": "10485760",
          "file_size": "10MB"
        },
        "_ingest": {
          "timestamp": "2023-08-22T16:09:42.771569211Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=file_upload
{
  "file_size": "10MB"
}
```
{% include copy-curl.html %}

**步驟 4 (選用)：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
