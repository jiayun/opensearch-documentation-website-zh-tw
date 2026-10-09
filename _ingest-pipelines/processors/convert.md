---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換"
parent: Ingest processors
nav_order: 30
redirect_from:
   - /api-reference/ingest-apis/processors/convert/
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `convert` 處理器。如果您的使用情境涉及大型或複雜的資料集，建議考慮使用在 OpenSearch 叢集上執行的 [Data Prepper `convert_entry_type` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/convert-entry-type/)。
{: .note}

# Convert 處理器

`convert` 處理器會將文件中的欄位轉換為不同的類型，例如將字串轉換為整數，或將整數轉換為字串。對於陣列欄位，陣列中的所有值都會被轉換。

## 語法

以下是 `convert` 處理器的語法：

```json
{
    "convert": {
        "field": "field_name",
        "type": "type-value"
    }
}
```
{% include copy.html %}

## 組態參數

下表列出 `convert` 處理器的必要與選用參數。   

參數 | 必要／選用 | 說明 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含要轉換之資料的欄位名稱。支援[範本片段]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#template-snippets)。 |
`type`  | 必要  | 要將欄位值轉換成的類型。支援的類型為 `integer`、`long`、`float`、`double`、`string`、`boolean`、`ip` 與 `auto`。如果 `type` 設為 `boolean`，則當欄位值為字串 `true`（不分大小寫）時，值會設為 `true`；當欄位值為字串 `false`（不分大小寫）時，值會設為 `false`。如果類型設為 `ip`，則此處理器會驗證欄位值是否符合 IPv4 或 IPv6 位址的正確格式；如果值無效，將會產生錯誤。如果值不是允許的值之一，將會發生錯誤。  |
`description`  | 選用  | 處理器的簡要描述。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器是否即使遇到錯誤也繼續執行。如果設為 `true`，則會忽略失敗。預設值為 `false`。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不包含指定欄位的文件。如果設為 `true`，當欄位不存在或為 `null` 時，處理器不會修改文件。預設值為 `false`。 |
`on_failure` | 選用 | 當處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於除錯，以區分相同類型的處理器。 |
`target_field`  | 選用  | 用來儲存已剖析資料的欄位名稱。如果未指定，值將儲存在 `field` 欄位中。預設值為 `field`。  |

## 使用處理器

依照下列步驟在管線中使用處理器。

**步驟 1：建立管線**

下列查詢會建立一個名為 `convert-price` 的管線，將 `price` 轉換為浮點數，將轉換後的值儲存在 `price_float` 欄位中，並在值小於 `0` 時將其設為 `0`：

```json
PUT _ingest/pipeline/convert-price
{
  "description": "Pipeline that converts price to floating-point number and sets value to zero if price less than zero",
  "processors": [
    {
      "convert": {
        "field": "price",
        "type": "float",
        "target_field": "price_float"
      }
    },
    {
      "set": {
        "field": "price",
        "value": "0",
        "if": "ctx.price_float < 0"
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
POST _ingest/pipeline/convert-price/_simulate
{
  "docs": [
    {
      "_index": "testindex1",
      "_id": "1",
       "_source": {
        "price": "-10.5"
      }
    }
  ]
}
```
{% include copy-curl.html %}

**回應**

下列範例回應確認管線如預期運作：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "testindex1",
        "_id": "1",
        "_source": {
          "price_float": -10.5,
          "price": "0"
        },
        "_ingest": {
          "timestamp": "2023-08-22T15:38:21.180688799Z"
        }
      }
    }
  ]
}
```

**步驟 3：匯入文件**

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=convert-price
{
  "price": "10.5"
}
```
{% include copy-curl.html %}

**步驟 4（選用）：擷取文件**

若要擷取文件，請執行下列查詢：

```json
GET testindex1/_doc/1
```
{% include copy-curl.html %}
