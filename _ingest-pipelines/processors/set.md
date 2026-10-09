---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Set
parent: Ingest processors
nav_order: 240
---

# Set 處理器

`set` 處理器會新增或更新文件中的欄位。它會設定一個欄位，並將該欄位與指定的值關聯。如果欄位已存在，其值會被提供的值取代，除非 `override` 參數設為 `false`。當 `override` 為 `false` 且指定的欄位已存在時，欄位的值會維持不變。

以下是 `set` 處理器的語法：

```json
{
  "description": "...",
  "processors": [
    {
      "set": {
        "field": "new_field",
        "value": "some_value"
      }
    }
  ]
}
```
{% include copy.html %}

## 組態參數

下表列出 `set` 處理器的必要與選用參數。

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 要設定或更新的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。
`value` | 必要 | 指派給欄位的值。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。
`override` | 選用 | 布林值旗標，用於決定處理器是否應覆寫欄位的現有值。
`ignore_empty_value` | 選用 | 布林值旗標，用於決定處理器是否應忽略 `null` 值或空字串。預設為 `false`。
`description`  | 選用  | 處理器用途或組態的說明。
`if` | 選用 | 指定依條件執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理器在執行期間失敗時要執行的處理器清單。這些處理器會依指定的順序執行。
`tag` | 選用 | 處理器的識別標籤。有助於在偵錯時區分相同類型的處理器。

## 使用處理器

請依照下列步驟在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立名為 `set-pipeline` 的管線，使用 `set` 處理器在文件中新增欄位 `new_field`，其值為 `some_value`： 

```json
PUT _ingest/pipeline/set-pipeline
{
  "description": "Adds a new field 'new_field' with the value 'some_value'",
  "processors": [
    {
      "set": {
        "field": "new_field",
        "value": "some_value"
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2（選用）：測試管線

建議您在匯入文件前先測試管線。
{: .tip}

若要測試管線，請執行下列查詢：

```json
POST _ingest/pipeline/set-pipeline/_simulate
{
  "docs": [
    {
      "_source": {
        "existing_field": "value"
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
          "existing_field": "value",
          "new_field": "some_value"
        },
        "_ingest": {
          "timestamp": "2024-05-30T21:56:15.066180712Z"
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
POST testindex1/_doc?pipeline=set-pipeline
{
  "existing_field": "value"
}
```
{% include copy-curl.html %}

#### 回應

此請求會將文件編製索引至索引 `testindex1`，接著將所有文件編製索引，並將 `new_field` 設為 `some_value`，如下列回應所示：

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
  "_seq_no": 0,
  "_primary_term": 1
}
```
{% include copy-curl.html %}

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
