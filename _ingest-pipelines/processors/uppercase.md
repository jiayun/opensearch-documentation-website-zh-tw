---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "大寫"
parent: Ingest processors
nav_order: 310
redirect_from:
   - /api-reference/ingest-apis/processors/uppercase/
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `uppercase` 處理器。如果您的使用案例涉及大型或複雜的資料集，請考慮使用在 OpenSearch 叢集上執行的 [Data Prepper `uppercase_string` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/uppercase-string/)。
{: .note}

# 大寫處理器

`uppercase` 處理器會將特定欄位中的所有文字轉換為大寫字母。 

## 語法

以下是 `uppercase` 處理器的語法： 

```json
{
  "uppercase": {
    "field": "field_name"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `uppercase` 處理器的必要與選用參數。

| 參數  | 必要／選用  | 說明  |
|---|---|---|
`field`  | 必要  | 包含要附加之資料的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 |  指定處理器是否在遇到錯誤時仍繼續執行。如果設為 `true`，則會忽略失敗。預設為 `false`。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不含指定欄位的文件。如果設為 `true`，當欄位不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。  |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於在偵錯時區分相同類型的處理器。 |
`target_field`  | 選用  | 儲存剖析後資料的欄位名稱。預設為 `field`。依預設，`field` 會就地更新。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線** 

下列查詢會建立名為 `uppercase` 的管線，將 `field` 欄位中的文字轉換為大寫：

```json
PUT _ingest/pipeline/uppercase
{
  "processors": [
    {
      "uppercase": {
        "field": "name"
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
POST _ingest/pipeline/uppercase/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "name": "John"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認管線如預期般運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "name": "JOHN"
        },
        "_ingest": {
          "timestamp": "2023-08-28T19:54:42.289624792Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=uppercase
{
  "name": "John"
}
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
