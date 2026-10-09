---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Append
parent: Ingest processors
nav_order: 10
redirect_from:
   - /api-reference/ingest-apis/processors/append/
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `append` 處理器。如果您的使用情境涉及大型或複雜的資料集，建議考慮使用在 OpenSearch 叢集上執行的 [Data Prepper `add_entries` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/add-entries/)。
{: .note}

# Append 處理器

`append` 處理器用於將值新增至欄位：

- 如果該欄位是陣列，`append` 處理器會將指定的值附加到該陣列。
- 如果該欄位是純量欄位，`append` 處理器會將其轉換為陣列，並將指定的值附加到該陣列。
- 如果該欄位不存在，`append` 處理器會建立一個包含指定值的陣列。

### 語法 

以下是 `append` 處理器的語法： 

```json
{
  "append": {
    "field": "your_target_field",
    "value": ["your_appended_value"]
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `append` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含要附加資料的欄位名稱。支援[範本程式碼片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。|
`value`  | 必要  | 要附加的值。可以是靜態值，或從現有欄位衍生的動態值。支援[範本程式碼片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 | 
`description`  | 選用  | 處理器的簡短描述。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器遇到錯誤時是否繼續執行。若設為 `true`，則會忽略失敗。預設值為 `false`。 |
`allow_duplicates` | 選用 | 指定是否附加欄位中已存在的值。若為 `true`，則會附加重複的值；否則會略過。 |
`on_failure` | 選用 | 當處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於除錯時區分相同類型的處理器。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線** 

下列查詢會建立一個名為 `user-behavior` 的管線，其中包含一個 append 處理器。它會將每個匯入 OpenSearch 的新文件的 `page_view` 附加到名為 `event_types` 的陣列欄位：

```json
PUT _ingest/pipeline/user-behavior
{
  "description": "Pipeline that appends event type",
  "processors": [
    {
      "append": {
        "field": "event_types",
        "value": ["page_view"]
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
POST _ingest/pipeline/user-behavior/_simulate
{
  "docs":[
    {
      "_source":{
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "event_types": [
            "page_view"
          ]
        },
        "_ingest": {
          "timestamp": "2023-08-28T16:55:10.621805166Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=user-behavior
{
}
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

由於文件不包含 `event_types` 欄位，因此會建立一個陣列欄位，並將事件附加到該陣列：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": 2,
  "_seq_no": 1,
  "_primary_term": 1,
  "found": true,
  "_source": {
    "event_types": [
      "page_view"
    ]
  }
}
```
