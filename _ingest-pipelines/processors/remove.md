---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "移除"
parent: Ingest processors
nav_order: 222
redirect_from:
   - /api-reference/ingest-apis/processors/remove/
---

# Remove 處理器

`remove` 處理器用於從文件中移除欄位。

## 語法

以下是 `remove` 處理器的語法：

```json
{
    "remove": {
        "field": "field_name"
    }
}
```
{% include copy.html %}

## 組態參數

下表列出 `remove` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
|---|---|---|
`field`  | 選用  | 包含要移除之資料的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。中繼資料欄位 `_index`、`_version`、`_version_type` 和 `_id` 無法移除。若指定 `version`，則無法從匯入的文件中移除 `_id`。 |
`exclude_field`  | 選用  | 要保留的欄位名稱。除了中繼資料欄位外，所有其他欄位都會被移除。`exclude_field` 與 `field` 選項互斥。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。  |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `remove_ip` 的管線，該管線會從文件中移除 `ip_address` 欄位：

```json
PUT /_ingest/pipeline/remove_ip
{
  "description": "Pipeline that excludes the ip_address field.",
  "processors": [
    {
      "remove": {
        "field": "ip_address"
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
POST _ingest/pipeline/remove_ip/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source":{
         "ip_address": "203.0.113.1",
         "name": "John Doe"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "name": "John Doe"
        },
        "_ingest": {
          "timestamp": "2023-08-24T18:02:13.218986756Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=remove_ip
{
  "ip_address": "203.0.113.1",
  "name": "John Doe"
}
```
{% include copy-curl.html %}

**步驟 4 (選用)：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
