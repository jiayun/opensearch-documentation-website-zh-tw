---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "對應"
nav_order: 1
nav_exclude: true
permalink: /mappings/
redirect_from: 
  - /opensearch/mappings/
  - /field-types/mappings/
  - /mappings/index/
  - /field-types/
  - /field-types/index/
  - /field-types/mappings-use-cases/
---

# 對應

對應會告訴 OpenSearch 如何儲存您的文件及其欄位並編製索引。您可以為每個欄位指定資料類型（例如，將 `year` 指定為 `date`），讓儲存與查詢更有效率。

雖然[動態對應](#dynamic-mapping)會自動新增資料與欄位，但仍建議使用明確對應。明確對應可讓您預先定義確切的結構與資料類型，有助於維持資料一致性並最佳化效能，尤其是在處理大型資料集或大量編製索引作業時。

例如，使用明確對應時，您可以確保 `year` 被視為文字，而 `age` 被視為整數，而不是兩者都被動態對應解讀為整數。

## 對應結構與概念

在學習如何建立對應之前，請先了解對應的結構，以及本文件中使用的關鍵術語。

### 對應結構與範例

OpenSearch 對應遵循階層式 JSON 結構。下列範例示範如何使用 `text` 與 `date` 欄位及其對應參數。此外，其中還包含一個具有自身屬性的巢狀 `director` 物件：

```json
PUT /movies
{
  "mappings": {                    // Overall mappings object
    "properties": {                // Properties container
      "title": {                   // Field name
        "type": "text",            // Field type
        "analyzer": "standard"     // Mapping parameter
      },
      "year": {                    // Field name
        "type": "date",            // Field type
        "format": "yyyy"           // Mapping parameter
      },
      "director": {                // Field name (object type)
        "type": "object",          // Field type
        "properties": {            // Properties container for nested fields
          "name": {                // Field name (nested)
            "type": "text"         // Field type
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

### 關鍵術語

- **對應**：索引的整體結構描述定義。
- **屬性**：對應中所有欄位定義的容器。
- **欄位**：個別的資料元素（例如 `title` 或 `year`）。
- **欄位類型**：定義欄位資料如何儲存與編製索引（例如 `text`、`integer`、`date`）。如需更多資訊，請參閱[支援的欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/)。
- **對應參數**：修改欄位行為的組態選項（例如 `analyzer`、`coerce`、`format`）。如需更多資訊，請參閱[對應參數]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/)。

## 明確對應

如果您確切知道需要使用哪些欄位資料類型，就可以在建立索引時於請求本文中指定，如下列範例請求所示：

```json
PUT sample-index1
{
  "mappings": {
    "properties": {
      "year":    { "type" : "text" },
      "age":     { "type" : "integer" },
      "director":{ "type" : "text" }
    }
  }
}
```
{% include copy-curl.html %}

您無法變更現有欄位的對應；只能修改該欄位的對應參數。
{: .note}

若要為現有的索引或資料串流新增對應，您可以向 `_mapping` 端點傳送請求，並使用 `PUT` 或 `POST` HTTP 方法，如下列範例請求所示：

```json
POST sample-index1/_mapping
{
  "properties": {
    "year":    { "type" : "text" },
    "age":     { "type" : "integer" },
    "director":{ "type" : "text" }
  }
}
```
{% include copy-curl.html %}

如需 Mapping API 的更多資訊，請參閱[更新對應]({{site.url}}{{site.baseurl}}/api-reference/index-apis/put-mapping/)。

## 動態對應

當您將文件編製索引時，OpenSearch 可以使用動態對應自動偵測並新增欄位。此行為與明確對應不同，後者需要您預先定義欄位類型。

### 動態對應規則

當 OpenSearch 在編製索引時遇到新欄位，會使用下列規則來判斷欄位類型：

JSON 資料類型 | OpenSearch 欄位類型 | 說明
:--- | :--- | :---
`null` | 不會新增欄位 | `null` 欄位無法編製索引或搜尋。當欄位設定為 null 時，OpenSearch 的行為如同該欄位沒有值。
`true` 或 `false` | [`boolean`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/boolean/) 欄位 | OpenSearch 接受 `true` 與 `false` 作為布林值。空字串等於 `false`。
雙精度浮點數（例如 `1.5`） | [`float`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/) 欄位 | 單精度 32 位元 IEEE 754 浮點數，僅限有限值。JSON 浮點數會對應至此類型。
長整數（例如 `1`）| [`long`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/) 欄位 | 帶正負號的 64 位元數字。JSON 整數會對應至此類型。
物件（`{}`） | [`object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/object/) 欄位 | 物件是標準 JSON 物件，可以擁有自己的欄位與對應。例如，`movies` 物件可以擁有 `title`、`year` 與 `director` 等其他屬性。
陣列（`[]`）| 取決於陣列中第一個非 null 值 | OpenSearch 沒有特定的陣列資料類型。陣列是以與欄位關聯的一組相同資料類型的值（例如整數或字串）來表示。編製索引時，您可以為一個欄位傳遞多個值，OpenSearch 會將其視為陣列。空陣列是有效的，會被辨識為零個元素的陣列欄位---而不是沒有值的欄位。
字串（`""`） | 帶有 [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/) 子欄位的 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位、[`date`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/) 欄位，或數值欄位 | 字元組成的字串序列。預設情況下，字串會對應為帶有 `keyword` 子欄位的 `text` 欄位。不過，如果字串符合日期格式（且已啟用日期偵測），則會變成 `date` 欄位。如果已啟用數值偵測且字串代表數字，則會變成適當的數值欄位類型。

這些是唯一會自動偵測的欄位類型。所有其他欄位類型都必須明確對應。

### 動態範本

動態範本用於根據資料類型、欄位名稱或欄位路徑，為動態新增的欄位定義自訂對應。它們可讓您為資料定義彈性的結構描述，自動適應輸入資料結構或格式的變化。

您可以使用下列語法來定義動態對應範本：

```json
PUT index
{
  "mappings": {
    "dynamic_templates": [
        {
          "fields": {
            "mapping": {
              "type": "short"
            },
            "match_mapping_type": "string",
            "path_match": "status*"
          }
        }
    ]
  }
}
```
{% include copy-curl.html %}

此對應組態會將任何名稱以 `status` 開頭的欄位（例如 `status_code`）動態對應至 `short` 資料類型（前提是編製索引時提供的初始值為字串）。

### 動態對應參數

`dynamic_templates` 支援下列參數，用於比對條件與對應規則。預設值為 `null`。

參數 | 說明 |
----------|-------------|
`match_mapping_type` | 指定觸發對應的 JSON 資料類型（例如字串、長整數、雙精度浮點數、物件、二進位資料、布林值、日期）。
`match` | 用於比對欄位名稱並套用對應的正規表示式。
`unmatch` | 用於從對應中排除欄位名稱的正規表示式。
`match_pattern` | 決定模式比對行為，可為 `regex` 或 `simple`。預設為 `simple`。
`path_match` | 可讓您使用正規表示式比對巢狀欄位路徑。
`path_unmatch` | 使用正規表示式從對應中排除巢狀欄位路徑。
`mapping` | 要套用的對應組態。

### 動態對應設定

OpenSearch 提供數個設定，用來控制動態對應在處理新欄位時的行為。

#### 日期偵測

根據預設，OpenSearch 會自動偵測日期格式的字串並建立 `date` 欄位。當 `date_detection` 啟用時 (預設)，新的字串欄位會依據 `dynamic_date_formats` 中指定的日期模式進行檢查。若找到相符項目，便會建立具有對應格式的新 `date` 欄位。

`dynamic_date_formats` 的預設值為：
```
["strict_date_optional_time", "yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z"]
```

當您執行下列範例請求時，`create_date` 欄位會自動對應為格式為 `yyyy/MM/dd HH:mm:ss Z||yyyy/MM/dd Z` 的 `date` 欄位：

```json
PUT sample-index/_doc/1
{
  "create_date": "2025/05/26"
}
```
{% include copy-curl.html %}

您可以將 `date_detection` 設為 `false`，以停用自動日期偵測：

```json
PUT sample-index
{
  "mappings": {
    "date_detection": false
  }
}
```
{% include copy-curl.html %}

停用日期偵測後，日期格式的字串會改為對應為 `text` 欄位。

您可以指定自己的 `dynamic_date_formats`，自訂用於偵測的日期模式：

```json
PUT sample-index
{
  "mappings": {
    "dynamic_date_formats": ["MM/dd/yyyy", "dd-MM-yyyy"]
  }
}
```
{% include copy-curl.html %}

#### 數值偵測

雖然 JSON 支援原生數值資料類型，但有些應用程式可能會以字串形式傳送數字。當 `numeric_detection` 啟用時，OpenSearch 可以自動偵測數值字串，並將其對應為數值欄位。

數值偵測預設為停用。建議的做法是針對數值欄位使用明確對應。
{: .note}

若要啟用數值偵測，請傳送下列請求：

```json
PUT sample-index
{
  "mappings": {
    "numeric_detection": true
  }
}
```
{% include copy-curl.html %}

接著將包含數值欄位的文件編製索引至該索引：

```json
PUT sample-index/_doc/1
{
  "price": "19.99",
  "quantity": "5"
}
```
{% include copy-curl.html %}

啟用數值偵測後：
- `price` 欄位會對應為 `float` 欄位
- `quantity` 欄位會對應為 `long` 欄位

## 擷取對應

若要取得一或多個索引的所有對應，請使用下列請求：

```json
GET {index}/_mapping
```
{% include copy-curl.html %}

在上述請求中，`<index>` 可以是索引名稱，或以逗號分隔的索引名稱清單。

若要取得所有索引的所有對應，請使用下列請求：

```json
GET _mapping
```
{% include copy-curl.html %}

若要取得特定欄位的對應，請提供索引名稱與欄位名稱：

```json
GET _mapping/field/{fields}
GET /{index}/_mapping/field/{fields}
```

`<index>` 與 `<fields>` 都可指定為單一值或以逗號分隔的清單。例如，下列請求會擷取 `sample-index1` 中 `year` 與 `age` 欄位的對應：

```json
GET sample-index1/_mapping/field/year,age
```
{% include copy-curl.html %}

回應會包含指定的欄位：

```json
{
  "sample-index1" : {
    "mappings" : {
      "year" : {
        "full_name" : "year",
        "mapping" : {
          "year" : {
            "type" : "text"
          }
        }
      },
      "age" : {
        "full_name" : "age",
        "mapping" : {
          "age" : {
            "type" : "integer"
          }
        }
      }
    }
  }
}
```

如需更多資訊，請參閱 [Get Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/get-index/)。

## 範例

下列範例示範 OpenSearch 對應在不同情境中的實際應用。

### 忽略格式錯誤的 IP 位址

下列範例說明如何建立對應，指定 OpenSearch 應忽略任何包含不符合 [`ip`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/ip/) 資料類型之格式錯誤 IP 位址的文件。您可以將 `ignore_malformed` 參數設為 `true` 來達成此目的。

若要建立具有 `ip` 對應的索引，請使用 PUT 請求：

```json
PUT /test-index
{
  "mappings" : {
    "properties" :  {
      "ip_address" : {
        "type" : "ip",
        "ignore_malformed": true
      }
    }
  }
}
```
{% include copy-curl.html %}

接著新增含有格式錯誤 IP 位址的文件：

```json
PUT /test-index/_doc/1
{
  "ip_address" : "malformed ip address"
}
```
{% include copy-curl.html %}

當您查詢該索引時，`ip_address` 欄位會被忽略。您可以使用下列請求查詢該索引：

```json
GET /test-index/_search
```
{% include copy-curl.html %}

回應顯示文件已成功編製索引，但格式錯誤的 IP 位址欄位會列在 `_ignored` 陣列中：

```json
{
  "took": 14,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "test-index",
        "_id": "1",
        "_score": 1,
        "_ignored": [
          "ip_address"
        ],
        "_source": {
          "ip_address": "malformed ip address"
        }
      }
    ]
  }
}
```

### 將字串欄位對應至 `text` 與 `keyword` 類型

若要建立名為 `movies1` 的索引，並使用動態範本將所有字串欄位同時對應至 `text` 與 `keyword` 類型，您可以使用下列請求：

```json
PUT movies1
{
  "mappings": {
    "dynamic_templates": [
      {
        "strings": {
          "match_mapping_type": "string",
          "mapping": {
            "type": "text",
            "fields": {
              "keyword": {
                "type":  "keyword",
                "ignore_above": 256
              }
            }
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

此動態範本可確保您文件中的任何字串欄位都會同時編製為全文 `text` 類型與 `keyword` 類型的索引。

## 對應參數

對應參數用於設定索引欄位的行為。如需所有可用對應參數的詳細資訊，請參閱 [對應參數]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/)。

## 中繼資料欄位

OpenSearch 會自動為每份文件管理數個中繼資料欄位，例如 `_source`、`_id` 與 `_index`。如需所有可用中繼資料欄位及其組態選項的資訊，請參閱 [中繼資料欄位]({{site.url}}{{site.baseurl}}/mappings/metadata-fields/)。

## 對應限制設定

OpenSearch 提供多項設定，以防止對應爆炸並控制對應的成長。這些設定有助於維持叢集效能，並避免因建立過多欄位而造成的記憶體問題。

如需所有對應限制設定的詳細資訊（包括預設值與有效範圍），請參閱 [對應限制設定]({{site.url}}{{site.baseurl}}/mappings/mapping-explosion/#mapping-limit-settings)。


## 相關文件

- [支援的欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/)