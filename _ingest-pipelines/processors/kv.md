---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: KV
parent: Ingest processors
nav_order: 200
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `kv` 處理器。如果您的使用案例涉及大型或複雜的資料集，請考慮使用在 OpenSearch 叢集上執行的 [Data Prepper `key_value` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/key-value/)。
{: .note}

# KV 處理器

`kv` 處理器會自動擷取採用 `key=value` 格式的特定事件欄位或訊息。這種結構化格式會根據鍵和值將資料分組，以組織您的資料。這有助於分析、視覺化及運用資料，例如使用者行為分析、效能最佳化或安全性調查。 

## 範例

以下是 `kv` 處理器的語法： 

```json
{
  "kv": {
    "field": "message",
    "field_split": " ",
    "value_split": " "
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `kv` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
`field`  | 必要  | 包含待剖析資料的欄位名稱。 |
`field_split` | 必要 | 用於分割鍵值組的正規表示式模式。 |
`value_split` | 必要 | 用於在鍵值組內分隔鍵和值的正規表示式模式，例如等號 `=` 或冒號 `:`。
`exclude_keys` | 選用 | 要從文件中排除的鍵。預設為 `null`。 |
`include_keys` | 選用 | 用於篩選和插入的鍵。預設包含所有鍵。 |
`prefix` | 選用 | 要新增至擷取之鍵的前綴。預設為 `null`。 |
`strip_brackets` | 選用 | 若設為 `true`，會從擷取的值中移除括號（`()`、`<>,` 或 `[]`）和引號（`'` 或 `"`）。預設為 `false`。
`trim_key` | 選用 | 要從擷取的鍵中修剪掉的字元字串。 | 
`trim value` | 選用 | 要從擷取的值中修剪掉的字元字串。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 若設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不含指定欄位的文件。預設為 `false`。  |
`tag` | 選用 | 處理器的識別標籤。有助於在偵錯時區分相同類型的處理器。 |
`target_field`  | 選用  | 要插入擷取之鍵的欄位名稱。預設為 `null`。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `kv-pipeline` 的管線，使用 `kv` 處理器擷取文件的 `message` 欄位：

```json
PUT _ingest/pipeline/kv-pipeline
{
  "description" : "Pipeline that extracts user profile data",
  "processors" : [
    {
      "kv" : {
        "field" : "message",
        "field_split": " ",
        "value_split": "="
      }
    }
  ]
}
```
{% include copy-curl.html %}

**步驟 2（選用）：測試管線**

建議您在匯入文件之前測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/kv-pipeline/_simulate
{  
  "docs": [  
    {  
      "_index": "testindex1",  
      "_id": "1",  
      "_source":{  
         "message": "goodbye=everybody hello=world"  
      }  
    }  
  ]  
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認，除了原始的 `message` 欄位之外，文件還包含從鍵值組產生的欄位：

```json
{  
  "docs": [  
    {  
      "doc": {  
        "_index": "testindex1",  
        "_id": "1",  
        "_source": {  
          "hello": "world",  
          "message": "goodbye=everybody hello=world",  
          "goodbye": "everybody"  
        },  
        "_ingest": {  
          "timestamp": "2023-12-06T09:59:21.823292Z"  
        }  
      }  
    }  
  ]  
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=kv-pipeline
{  
  "message": "goodbye=everybody hello=world"  
}  
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
