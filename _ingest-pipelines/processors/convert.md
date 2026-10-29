---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換"
parent: Ingest processors
nav_order: 30
redirect_from:
   - /api-reference/ingest-apis/processors/convert/
---

本文件說明如何在 OpenSearch 資料匯入管線中使用 `convert` 處理器。若您的使用情境涉及大型或複雜的資料集，建議改用 [Data Prepper `convert_entry_type` 處理器]({{site.url}}{{site.baseurl}}/data-prepper/pipelines/configuration/processors/convert-entry-type/)，其於 OpenSearch 叢集外執行。
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

## 參數

下表列出 `convert` 處理器的必要與選用參數。   

參數 | 必要/選用 | 描述 |
|-----------|-----------|-----------|
`field`  | 必要  | 包含要轉換資料之欄位的名稱。 |
`type`  | 必要  | 欄位值要轉換成的資料類型。支援的類型為 `integer`、`long`、`float`、`double`、`string`、`boolean`、`ip` 與 `auto`。若 `type` 為 `boolean`，則當欄位值是字串 `true`（忽略大小寫）時，值會設為 `true`；當欄位值是字串 `false`（忽略大小寫）時，值會設為 `false`。其他任何字串值都會導致處理器失敗。若類型設為 `ip`，則此處理器會驗證欄位值是否符合 IPv4 或 IPv6 位址的正確格式；若值無效，則會引發錯誤。若類型設為 `auto`，則處理器會依下列順序將字串值轉換為第一個符合的類型：`boolean`、`integer`、`long`、`float` 與 `double`。由於 `float` 會在 `double` 之前嘗試，十進位字串一律會轉換為 `float`，這可能會降低精確度。若字串不符合上述任何類型，或值不是字串，則值不會變更。若有指定 `target_field`，未變更的值仍會複製到 `target_field`。若 `type` 不是支援的類型之一，管線將被拒絕。  |
`description`  | 選用  | 處理器的簡短描述。  |
`if` | 選用 | 執行處理器的條件。 |
`ignore_failure` | 選用 | 指定處理器即使遇到錯誤是否仍繼續執行。若設為 `true`，則會忽略失敗。預設為 `false`。 |
`ignore_missing`  | 選用  | 指定處理器是否應忽略不含指定欄位的文件。若設為 `true`，當欄位不存在或為 `null` 時，處理器不會修改文件。預設為 `false`。 |
`on_failure` | 選用 | 處理器失敗時要執行的處理器清單。 |
`tag` | 選用 | 處理器的識別標籤。有助於偵錯時區分相同類型的處理器。如需更多資訊，請參閱[使用處理器標籤進行監控與偵錯]({{site.url}}{{site.baseurl}}/ingest-pipelines/create-ingest/#using-processor-tags-for-monitoring-and-debugging)。 |
`target_field`  | 選用  | 用於儲存已解析資料的欄位名稱。若未指定，值將儲存在 `field` 欄位。預設為 `field`。  |

## 使用處理器

請依照下列步驟，在管線中使用處理器。

### 步驟 1：建立管線

下列查詢會建立一個名為 `convert-price` 的管線，將 `price` 轉換為浮點數，把轉換後的值儲存在 `price_float` 欄位，並在該值小於 `0` 時將其設為 `0`：

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

### 步驟 2（選用）：測試管線

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

### 步驟 3：匯入文件

下列查詢會將文件匯入名為 `testindex1` 的索引：

```json
PUT testindex1/_doc/1?pipeline=convert-price
{
  "price": "-10.5"
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

## 自動轉換值

下列請求使用 `auto` 類型來轉換數個字串欄位：

```json
POST _ingest/pipeline/_simulate
{
  "pipeline": {
    "processors": [
      { "convert": { "field": "in_stock", "type": "auto" } },
      { "convert": { "field": "quantity", "type": "auto" } },
      { "convert": { "field": "weight_kg", "type": "auto" } },
      { "convert": { "field": "color", "type": "auto" } }
    ]
  },
  "docs": [
    {
      "_source": {
        "in_stock": "TRUE",
        "quantity": "42",
        "weight_kg": "1.23456789",
        "color": "dark gray"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應顯示 `in_stock` 已轉換為布林值，`quantity` 已轉換為整數。`weight_kg` 值已轉換為 `float`，因此其精確度降低了。`color` 值不符合任何類型，因此仍為字串：

```json
{
  "docs": [
    {
      "doc": {
        "_index": "_index",
        "_id": "_id",
        "_source": {
          "in_stock": true,
          "quantity": 42,
          "weight_kg": 1.2345679,
          "color": "dark gray"
        },
        "_ingest": {
          "timestamp": "2026-10-14T19:42:37.458135758Z"
        }
      }
    }
  ]
}
```
