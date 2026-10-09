---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複製"
parent: Ingest processors
nav_order: 35
redirect_from:
   - /api-reference/ingest-apis/processors/copy/
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `copy` 處理器。如果您的使用情境涉及大型或複雜的資料集，請考慮使用 [Data Prepper `copy_values` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/copy-values/)，該處理器在 OpenSearch 叢集上執行。
{: .note}

# Copy 處理器

`copy` 處理器會將現有欄位中的整個物件複製到另一個欄位。

## 語法

以下是 `copy` 處理器的語法：

```json
{
    "copy": {
      "source_field": "source_field", 
      "target_field": "target_field",
      "ignore_missing": true,
      "override_target": true,
      "remove_source": true
    }
}
```
{% include copy.html %}

## 組態參數

下表列出 `copy` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
|---|---|---|
`source_field`  | 必要  | 要複製的欄位名稱。支援 [範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`target_field`  | 必要  | 要複製到的欄位名稱。支援 [範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略未包含所指定 `source_field` 的文件。若設為 `true`，當 `source_field` 不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。 |
`override_target`  | 選用  | 指定處理器是否應覆寫文件中已存在的 `target_field`。若設為 `true`，當 `target_field` 已存在時，處理器會覆寫其值。預設為 `false`。 |
`remove_source`  | 選用  | 指定處理器是否應在複製後移除 `source_field`。若設為 `true`，處理器會從文件中移除 `source_field`。預設為 `false`。 |
`description`  | 選用  | 處理器的簡短說明。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則忽略失敗。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯時區分相同類型的處理器。 |

## 使用處理器

請依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立名為 `copy_object` 的管線，將巢狀物件從某個欄位複製到根層級：

```json
PUT /_ingest/pipeline/copy_object
{
  "description": "Pipeline that copies object.",
  "processors": [
    {
      "copy": {
        "source_field": "message.content", 
        "target_field":"content",
        "ignore_missing": true,
        "override_target": true,
        "remove_source": true
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
POST _ingest/pipeline/copy_object/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source":{
         "message": {
          "content": {
            "foo": "bar",
            "zoo": [1, 2, 3]
          }
         }
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
          "content": {
            "foo": "bar",
            "zoo": [1, 2, 3]
          }
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
PUT testindex1/_doc/1?pipeline=copy_object
{
  "content": {
    "foo": "bar",
    "zoo": [1, 2, 3]
  }
}
```
{% include copy-curl.html %}

**步驟 4 (選用)：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
