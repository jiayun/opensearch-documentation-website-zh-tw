---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指紋"
parent: Ingest processors
nav_order: 105
---

# 指紋處理器
於 2.16 版推出
{: .label .label-purple }

`fingerprint` 處理器用於針對文件中的特定指定欄位或所有欄位產生雜湊值。此雜湊值可用於移除索引中的重複文件，以及摺疊搜尋結果。

針對每個欄位，會將欄位名稱、欄位值的長度及欄位值本身串接起來，並以豎線字元 `|` 分隔。例如，如果欄位名稱為 `field1`，值為 `value1`，則串接後的字串為 `|field1|3:value1|field2|10:value2|`。對於物件欄位，會以句點 `.` 連接巢狀欄位名稱，將欄位名稱攤平。例如，如果物件欄位為 `root_field`，其中子欄位 `sub_field1` 的值為 `value1`，另一個子欄位 `sub_field2` 的值為 `value2`，則串接後的字串為 `|root_field.sub_field1|1:value1|root_field.sub_field2|100:value2|`。

以下是 `fingerprint` 處理器的語法：

```json
{
  "community_id": {
    "fields": ["foo", "bar"],
    "target_field": "fingerprint",
    "hash_method": "SHA-1@2.16.0"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `fingerprint` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`fields`  | 選用  | 用於產生雜湊值的欄位清單。  |
`exclude_fields`  | 選用  | 指定產生雜湊值時要排除的欄位。此參數與 `fields` 參數互斥；如果 `exclude_fields` 和 `fields` 皆為空或 null，則計算雜湊值時會納入所有欄位。 |
`hash_method`  | 選用  | 指定要使用的雜湊演算法，可選擇 `MD5@2.16.0`、`SHA-1@2.16.0`、`SHA-256@2.16.0` 或 `SHA3-256@2.16.0`。預設為 `SHA-1@2.16.0`。附加版本號碼是為了確保各個 OpenSearch 版本的雜湊運算一致，而新版本將支援新的雜湊方法。 |
`target_field`  | 選用  | 指定用於儲存所產生雜湊值的欄位名稱。如果未提供，則雜湊值預設會儲存在 `fingerprint` 欄位中。 |
`ignore_missing`  | 選用  | 指定當其中一個必要欄位遺失時，處理器是否應無提示地結束。預設為 `false`。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 如果設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。可在偵錯時用於區分相同類型的處理器。 |

## 使用處理器

依照下列步驟，在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `fingerprint_pipeline` 的管線，使用 `fingerprint` 處理器針對文件中的指定欄位產生雜湊值： 

```json
PUT /_ingest/pipeline/fingerprint_pipeline
{
  "description": "generate hash value for some specified fields the document",
  "processors": [
    {
      "fingerprint": {
        "fields": ["foo", "bar"]
     }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2（選用）：測試管線**

建議您在匯入文件前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/fingerprint_pipeline/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "foo": "foo",
        "bar": "bar"
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
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "foo": "foo",
          "bar": "bar",
          "fingerprint": "SHA-1@2.16.0:fYeen7hTJ2zs9lpmUnk6nvH54sM="
        },
        "_ingest": {
          "timestamp": "2024-03-11T02:17:22.329823Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=fingerprint_pipeline
{
  "foo": "foo",
  "bar": "bar"
}
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引至 `testindex1` 索引：

```json
{
  "_index": "testindex1",
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

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
