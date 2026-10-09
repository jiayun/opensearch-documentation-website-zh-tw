---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼"
parent: Ingest processors
nav_order: 230
---

# Script 匯入處理器

`script` 處理器會執行內嵌與已儲存的指令碼，可在匯入過程中修改或轉換 OpenSearch 文件中的資料。此處理器使用指令碼快取來提升效能，因為指令碼可能會依每份文件重新編譯。關於在 OpenSearch 中使用指令碼的資訊，請參閱 [Script APIs]({{site.url}}{{site.baseurl}}/api-reference/script-apis/index/)。

以下是 `script` 處理器的語法：

```json
{
  "processor": {
    "script": {
      "source": "<script_source>",
      "lang": "<script_language>",
      "params": {
        "<param_name>": "<param_value>"
      }
    }
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `script` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
|---|---|---|
`source`  | 選用  | 要執行的 Painless 指令碼。如需更多資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。必須指定 `id` 或 `source` 其中之一，但不能同時指定兩者。若指定 `source`，則會使用提供的原始碼執行指令碼。
`id` | 選用 | 先前使用 [Create Stored Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/) 建立之已儲存指令碼的 ID。必須指定 `id` 或 `source` 其中之一，但不能同時指定兩者。若指定 `id`，則會從具有指定 ID 的已儲存指令碼擷取指令碼原始碼。
`lang`  | 選用  | 指令碼的程式語言。預設為 `painless`。
`params` | 選用 |  可傳遞至指令碼的參數。
`description`  | 選用  | 處理器用途或組態的說明。
`if` | 選用 | 指定以條件方式執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱 [處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理器在執行期間失敗時要執行的一組處理器。這些處理器會依指定的順序執行。請參閱 [處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯，以區分相同類型的處理器。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `my-script-pipeline` 的管線，其使用 `script` 處理器將 `message` 欄位轉換為大寫：

```json
PUT _ingest/pipeline/my-script-pipeline
{
  "description": "Example pipeline using the ScriptProcessor",
  "processors": [
    {
      "script": {
        "source": "ctx.message = ctx.message.toUpperCase()",
        "lang": "painless",
        "description": "Convert message field to uppercase"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2 (選用)：測試管線

建議您在匯入文件之前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/my-script-pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "message": "hello, world!"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線運作正常：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "message": "HELLO, WORLD!"
        },
        "_ingest": {
          "timestamp": "2024-05-30T16:24:23.30265405Z"
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
POST testindex1/_doc?pipeline=my-script-pipeline
{
  "message": "hello, world!"
}
```
{% include copy-curl.html %}

#### 回應

回應確認文件已編製索引至 `testindex1`，且所有文件的 `message` 欄位值均已轉換為大寫後編製索引：

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
  "_seq_no": 6,
  "_primary_term": 2
}
```
{% include copy-curl.html %}

### 步驟 4 (選用)：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
