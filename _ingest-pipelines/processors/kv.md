---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: KV
parent: Ingest processors
nav_order: 200
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `kv` 處理器。若您的使用情境涉及大型或複雜的資料集，建議改用 [Data Prepper `key_value` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/key-value/)，該處理器在 OpenSearch 叢集之外執行。
{: .note}

# KV 處理器

`kv` 處理器會自動擷取採用 `key=value` 格式的特定事件欄位或訊息。這種結構化格式會依據鍵和值將資料分組，以組織您的資料。這有助於分析、視覺化及運用資料，例如進行使用者行為分析、效能最佳化或安全性調查。

`kv` 處理器會為每個擷取的鍵建立一個欄位，因此資料中的鍵會決定索引中的欄位名稱。如果鍵的差異很大，對應中的欄位數量可能會快速增加。若要將所有擷取的鍵儲存在單一欄位中，請設定 `target_field`，並將該欄位對應為 [`flat_object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/)。
{: .tip} 

## 語法

以下是 `kv` 處理器的語法：

```json
{
  "kv": {
    "field": "message",
    "field_split": " ",
    "value_split": "="
  }
}
```
{% include copy.html %}

## 參數

下表列出 `kv` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
|-----------|-----------|-----------|
`field`  | 必要  | 包含待剖析資料的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`field_split` | 必要 | 用於分割鍵值對的 regex 模式。 |
`value_split` | 必要 | 在鍵值對中將鍵與值分開的 regex 模式，例如等號 `=` 或冒號 `:`。
`exclude_keys` | 選用 | 要從文件中排除的鍵清單。預設為 `null`。 |
`include_keys` | 選用 | 要擷取的鍵清單。其他鍵會被忽略。預設包含所有鍵。 |
`prefix` | 選用 | 要加到擷取鍵前面的字首。預設為 `null`。 |
`strip_brackets` | 選用 | 若設為 `true`，則會從擷取的值中移除括號（`()`、`<>,` 或 `[]`）與引號（`'` 或 `"`）。預設為 `false`。
`trim_key` | 選用 | 要從擷取的鍵中修剪的字元字串。 | 
`trim_value` | 選用 | 要從擷取的值中修剪的字元字串。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 若設為 `true`，則會忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不包含指定欄位或欄位為 `null` 的文件。預設為 `false`。  |
`tag` | 選用 | 處理器的識別標籤。有助於偵錯時區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |
`target_field`  | 選用  | 要插入擷取鍵的欄位名稱。若未指定，鍵會加入文件的根層級。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |

## 使用處理器

請依照下列步驟在管線中使用此處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `kv-pipeline` 的管線，並使用 `kv` 處理器擷取文件的 `message` 欄位：

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

### 步驟 2（選用）：測試管線

建議您在匯入文件之前先測試管線。
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

下列範例回應確認文件除了原始的 `message` 欄位之外，還包含由鍵值對產生的欄位：

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

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=kv-pipeline
{  
  "message": "goodbye=everybody hello=world"  
}  
```
{% include copy-curl.html %}

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

回應會包含已匯入的文件，其轉換結果如步驟 2 的回應所示。
