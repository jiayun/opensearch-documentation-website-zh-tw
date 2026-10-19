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

若要移除多個欄位，請指定欄位名稱的陣列：

```json
{
    "remove": {
        "field": ["field_name_1", "field_name_2"]
    }
}
```
{% include copy.html %}

`exclude_field` 參數也接受要保留的欄位名稱陣列。

## 組態參數

下表列出 `remove` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
|---|---|---|
`field`  | 選用  | 包含要移除資料的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。中繼資料欄位 `_index`、`_version` 與 `_version_type` 無法移除。若請求指定外部版本類型，則 `_id` 欄位無法移除。必須指定 `field` 或 `exclude_field` 其中之一。 |
`exclude_field`  | 選用  | 要保留的欄位名稱。除中繼資料欄位外的所有其他欄位都會被移除。`exclude_field` 與 `field` 選項互斥。僅支援頂層欄位名稱。若指定巢狀欄位（例如 `user.name`），它不會符合任何頂層欄位，因此處理器會移除所有欄位，包括整個 `user` 物件。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。  |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不含指定欄位的文件。若設為 `true`，當欄位不存在時，處理器不會修改文件。預設為 `false`。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤仍繼續執行。若設為 `true`，將忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與除錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |

## 使用處理器

依照下列步驟在管線中使用處理器。

**步驟 1：建立管線** 

下列查詢會建立一個名為 `remove_ip` 的管線，用來從文件中移除 `ip_address` 欄位： 

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

**步驟 2（選用）：測試管線**

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

下列範例回應確認管線如預期運作：

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

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

## 移除多個欄位

下列請求會從文件中移除 `internal_sku` 和 `warehouse_code` 欄位：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "remove": {
          "field": ["internal_sku", "warehouse_code"]
        }
      }
    ]
  },
  "docs": [
    {
      "_source": {
        "product": "Wireless mouse",
        "internal_sku": "WM-4471",
        "warehouse_code": "SEA-02",
        "price": 24.99
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應顯示兩個欄位皆已移除：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "product": "Wireless mouse",
          "price": 24.99
        },
        "_ingest": {
          "timestamp": "2026-10-14T19:44:03.195795881Z"
        }
      }
    }
  ]
}
```
