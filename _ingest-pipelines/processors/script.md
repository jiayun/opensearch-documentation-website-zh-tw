---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "指令碼"
parent: Ingest processors
nav_order: 230
---

# Script 資料匯入處理器

`script` 處理器會執行內嵌與已儲存的指令碼，在匯入過程中修改或轉換 OpenSearch 文件中的資料。此處理器使用指令碼快取來提升效能，因為指令碼可能會依每份文件重新編譯。有關在 OpenSearch 中使用指令碼的資訊，請參閱 [Script APIs]({{site.url}}{{site.baseurl}}/api-reference/script-apis/index/)。

以下是 `script` 處理器的語法：

```json
{
  "script": {
    "source": "<script_source>",
    "lang": "<script_language>",
    "params": {
      "<param_name>": "<param_value>"
    }
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `script` 處理器的必要與選用參數。

| 參數  | 必要/選用  | 說明  |
|---|---|---|
`source`  | 選用  | 要執行的 Painless 指令碼。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。必須指定 `id` 或 `source` 其中之一，但不能同時指定兩者。若指定 `source`，則會使用提供的原始碼執行指令碼。
`id` | 選用 | 先前使用 [Create Stored Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/) 建立之已儲存指令碼的 ID。必須指定 `id` 或 `source` 其中之一，但不能同時指定兩者。若指定 `id`，則會從具有所指定 ID 的已儲存指令碼擷取指令碼原始碼。 
`lang`  | 選用  | 指令碼的程式設計語言。預設為 `painless`。
`params` | 選用 |  可傳遞至指令碼的參數。
`description`  | 選用  | 處理器用途或組態的說明。
`if` | 選用 | 指定是否要依條件執行處理器。
`ignore_failure` | 選用 | 指定是否要忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理器在執行期間失敗時要執行的處理器清單。這些處理器會依指定的順序執行。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`tag` | 選用 | 處理器的識別碼標籤。有助於偵錯，以便區分相同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

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

下列範例回應確認管線如預期運作：

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

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=my-script-pipeline
{
  "message": "hello, world!"
}
```
{% include copy-curl.html %}

#### 回應

回應確認文件已編製索引至 `testindex1`，且所有文件皆已編製索引，其中 `message` 欄位已轉換為大寫：

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

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

## 使用參數與修改中繼資料

在指令碼中，`ctx` 變數可讓您存取文件欄位與中繼資料欄位，例如 `_index`。在 `params` 中傳入的參數可在指令碼中以 `params.<name>` 取得。當值以參數形式傳入時，指令碼原始碼會維持不變，即使值有所變動，因此 OpenSearch 可以重複使用已編譯的指令碼。如需詳細資訊，請參閱[如何使用指令碼]({{site.url}}{{site.baseurl}}/scripting/using-scripts/)。

下列請求使用以參數傳入的折扣來計算總價，並變更文件的目標索引：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "script": {
          "source": "ctx.total_price = ctx.unit_price * ctx.quantity * (1 - params.discount); ctx._index = params.target_index;",
          "params": {
            "discount": 0.1,
            "target_index": "orders-processed"
          }
        }
      }
    ]
  },
  "docs": [
    {
      "_index": "orders-raw",
      "_source": {
        "unit_price": 20.0,
        "quantity": 3
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應會顯示計算出的 `total_price` 以及變更後的 `_index`：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "orders-processed",
        "_id": "_id",
        "_source": {
          "quantity": 3,
          "unit_price": 20.0,
          "total_price": 54.0
        },
        "_ingest": {
          "timestamp": "2026-10-14T20:10:38.9908023Z"
        }
      }
    }
  ]
}
```
