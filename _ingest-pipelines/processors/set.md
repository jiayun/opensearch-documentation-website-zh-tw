---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Set
parent: Ingest processors
nav_order: 240
---

# Set 處理器

`set` 處理器會新增或更新文件中的欄位。它會設定一個欄位並將其關聯至指定的值。若該欄位已存在，則其值會被提供的值取代，除非 `override` 參數設為 `false`。當 `override` 為 `false` 且指定的欄位存在且不是 `null` 時，該欄位的值會維持不變。值為 `null` 的欄位一律會被覆寫。

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

參數 | 必要/選用 | 說明 |
|-----------|-----------|-----------|
`field` | 必要 | 要設定或更新的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。
`value` | 必要 | 指派給欄位的值。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。
`override` | 選用 | 決定處理器是否應覆寫欄位現有值的布林值旗標。預設為 `true`。
`ignore_empty_value` | 選用 | 決定處理器是否應忽略 `null` 值或空字串的布林值旗標。預設為 `false`。
`description`  | 選用  | 處理器用途或組態的說明。
`if` | 選用 | 指定依條件執行處理器。
`ignore_failure` | 選用 | 指定忽略處理器失敗。請參閱[處理管線失敗]({{site.url}}{{site.baseurl}}/ingest-pipelines/pipeline-failures/)。
`on_failure` | 選用 | 指定處理器執行失敗時要執行的處理器清單。這些處理器會依指定的順序執行。
`tag` | 選用 | 處理器的識別標籤。有助於在偵錯時區分相同類型的處理器。如需詳細資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。

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

下列範例回應確認管線運作符合預期：

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

此請求會將文件編製索引至 `testindex1` 索引，並將 `new_field` 欄位設為 `some_value`，如下列回應所示：

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

### 步驟 4（選用）：擷取文件

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}

## 從另一個欄位複製值

若要將值從一個欄位複製到另一個欄位，請使用範本片段在 `value` 中參照來源欄位。下列請求會將 `customer.address.city` 欄位的值複製到 `shipping.city` 欄位：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      {
        "set": {
          "field": "shipping.city",
          "value": "{% raw %}{{{customer.address.city}}}{% endraw %}"
        }
      }
    ]
  },
  "docs": [
    {
      "_source": {
        "customer": {
          "address": {
            "city": "Portland"
          }
        }
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應顯示 `shipping.city` 欄位包含複製的值：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "shipping": {
            "city": "Portland"
          },
          "customer": {
            "address": {
              "city": "Portland"
            }
          }
        },
        "_ingest": {
          "timestamp": "2026-10-14T19:44:03.269176256Z"
        }
      }
    }
  ]
}
```

範本片段一律會產生字串。例如，複製數值欄位值 `24.99` 會產生字串 `"24.99"`。若要在複製值時保留其資料類型，或複製整個物件，請使用 [`copy` 處理器]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/copy/)。
