---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Drop
parent: Ingest processors
nav_order: 70
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `drop` 處理器。如果您的使用情境涉及大型或複雜的資料集，請考慮使用在 OpenSearch 叢集上執行的 [Data Prepper `drop_events` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/drop-events/)。
{: .note}

# Drop 處理器

`drop` 處理器用於捨棄文件而不將其編製索引。這對於根據特定條件防止文件被編製索引非常有用。例如，您可以使用 `drop` 處理器來防止缺少重要欄位或包含敏感資訊的文件被編製索引。

`drop` 處理器在捨棄文件時不會引發任何錯誤，因此可以在避免索引問題的同時，不讓錯誤訊息充斥您的 OpenSearch 記錄檔。

## 語法範例

以下是 `drop` 處理器的語法：

```json
{
  "drop": {
    "if": "ctx.foo == 'bar'"
  }
}
```
{% include copy.html %}

## 組態參數

下表列出 `drop` 處理器的必要與選用參數。

參數 | 必要 | 說明 |
|-----------|-----------|-----------|
`description`  | 選用  | 處理器的簡短描述。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 若設為 `true`，則忽略失敗。預設為 `false`。如需更多資訊，請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。如需更多資訊，請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。 |
`tag` | 選用 | 處理器的識別標籤。在除錯時，有助於區分相同類型的處理器。 |

## 使用處理器

依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立一個名為 `drop-pii` 的管線，使用 `drop` 處理器來防止包含個人識別資訊 (PII) 的文件被編製索引：

```json
PUT /_ingest/pipeline/drop-pii
{
  "description": "Pipeline that prevents PII from being indexed",
  "processors": [
    {
      "drop": {
        "if" : "ctx.user_info.contains('password') || ctx.user_info.contains('credit card')"
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
POST _ingest/pipeline/drop-pii/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
      "_source": {
        "user_info": "Sensitive information including credit card"
      }
    }
  ]
}
```
{% include copy-curl.html %}

#### 回應

下列範例回應確認管線如預期運作 (文件已被捨棄)：

```json
{
  "docs": [
    null
  ]
}
```
{% include copy-curl.html %}

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=drop-pii
{
  "user_info": "Sensitive information including credit card"
}
```
{% include copy-curl.html %}

下列回應確認 ID 為 `1` 的文件未被編製索引：

```json
{
  "_index": "testindex1",
  "_id": "1",
  "_version": -3,
  "result": "noop",
  "_shards": {
    "total": 0,
    "successful": 0,
    "failed": 0
  }
}
```
