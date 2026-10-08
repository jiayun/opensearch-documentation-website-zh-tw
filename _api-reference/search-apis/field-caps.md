---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "欄位功能"
parent: Search APIs
nav_order: 45
---

# 欄位功能 API
**1.0 版推出**
{: .label .label-purple }

`_field_caps` API 提供一個或多個索引中欄位功能的資訊。用戶端通常使用此 API 判斷欄位如何對應，以及是否可用於跨多個索引的搜尋、排序和彙總。

當索引具有不同的對應，且查詢需要評估這些索引之間的欄位相容性時，此 API 特別實用。

## 端點

```json
GET  /_field_caps
POST /_field_caps
GET  /{index}/_field_caps
POST /{index}/_field_caps
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 清單或字串 | 以逗號分隔的資料串流、索引和別名清單，用於限制請求範圍。支援萬用字元 (*)。若要以所有資料串流和索引為目標，請省略此參數，或使用 * 或 `_all`。_選用_。 |

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `allow_no_indices` | 布林值 | 若為 `false`，當任何萬用字元運算式、索引別名或 `_all` 值僅以不存在或已關閉的索引為目標時，請求會傳回錯誤。即使請求也以其他開啟的索引為目標，此行為仍適用。例如，以 `foo*,bar*` 為目標的請求，若有索引名稱以 foo 開頭，但沒有索引名稱以 bar 開頭，就會傳回錯誤。預設為 `true`。 |
| `expand_wildcards` | 清單或字串 | 萬用字元模式可比對的索引類型。若請求可以資料串流為目標，此引數會決定萬用字元運算式是否比對隱藏的資料串流。支援以逗號分隔的值，例如 `open,hidden`。<br> 有效值為：<br> - `all`：比對任何索引，包括隱藏的索引。<br> - `closed`：比對已關閉且非隱藏的索引。<br> - `hidden`：比對隱藏的索引。必須搭配 `open`、`closed` 或兩者使用。<br> - `none`：不接受萬用字元運算式。<br> - `open`：比對開啟且非隱藏的索引。<br> 預設為 `open`。 |
| `fields` | 清單或字串 | 以逗號分隔的欄位清單，用於指定要擷取功能資訊的欄位。支援萬用字元（`*`）運算式。 |
| `ignore_unavailable` | 布林值 | 若為 `true`，回應不會包含不存在或已關閉的索引。預設為 `false`。 |
| `include_unmapped` | 布林值 | 若為 `true`，回應會包含未對應的欄位。預設為 `false`。 |

## 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位          | 資料類型 | 說明                                                             |
| :------------- | :-------- | :---------------------------------------------------------------------- |
| `index_filter` | 物件 | 用於篩選請求所包含索引的 Query DSL 物件。請參閱[範例：使用索引篩選器](#example-using-an-index-filter)。_選用_。|

## 請求範例

建立兩個索引，對同一欄位使用不同的對應：

```json
PUT /store-west
{
  "mappings": {
    "properties": {
      "product": { "type": "text" },
      "price": { "type": "float" }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /store-east
{
  "mappings": {
    "properties": {
      "product": { "type": "keyword" },
      "price": { "type": "float" }
    }
  }
}
```
{% include copy-curl.html %}

查詢這兩個索引中的欄位功能：

<!-- spec_insert_start
component: example_code
rest: GET /store-west,store-east/_field_caps?fields=product,price
-->
{% capture step1_rest %}
GET /store-west,store-east/_field_caps?fields=product,price
{% endcapture %}

{% capture step1_python %}


response = client.field_caps(
  index = "store-west,store-east",
  params = { "fields": "product,price" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 回應範例

回應提供可用欄位的功能資訊：

```json
{
  "indices": [
    "store-east",
    "store-west"
  ],
  "fields": {
    "product": {
      "text": {
        "type": "text",
        "searchable": true,
        "aggregatable": false,
        "indices": [
          "store-west"
        ]
      },
      "keyword": {
        "type": "keyword",
        "searchable": true,
        "aggregatable": true,
        "indices": [
          "store-east"
        ]
      }
    },
    "price": {
      "float": {
        "type": "float",
        "searchable": true,
        "aggregatable": true
      }
    }
  }
}
```

## 範例：使用索引篩選器

您可以使用 `index_filter` 限制納入考量的索引。`index_filter` 根據欄位層級的中繼資料篩除索引，而非實際的文件內容。下列請求將索引選取範圍限制為對應中包含 `product` 欄位的索引，即使其中沒有已編製索引的文件也適用：

<!-- spec_insert_start
component: example_code
rest: POST /_field_caps?fields=product,price
body: |
{
  "index_filter": {
    "term": {
      "product": "notebook"
    }
  }
}
-->
{% capture step1_rest %}
POST /_field_caps?fields=product,price
{
  "index_filter": {
    "term": {
      "product": "notebook"
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.field_caps(
  params = { "fields": "product,price" },
  body =   {
    "index_filter": {
      "term": {
        "product": "notebook"
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 回應範例

回應僅包含來自 `product` 欄位值為 `notebook` 的索引的欄位：

```json
{
  "indices": [
    "store-east",
    "store-west"
  ],
  "fields": {
    "product": {
      "text": {
        "type": "text",
        "searchable": true,
        "aggregatable": false,
        "indices": [
          "store-west"
        ]
      },
      "keyword": {
        "type": "keyword",
        "searchable": true,
        "aggregatable": true,
        "indices": [
          "store-east"
        ]
      }
    },
    "price": {
      "float": {
        "type": "float",
        "searchable": true,
        "aggregatable": true
      }
    }
  }
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位                                            | 資料類型    | 說明                                                                                                              |
| :----------------------------------------------- | :----------- | :----------------------------------------------------------------------------------------------------------------------- |
| `indices` | 清單 | 回應所包含的索引清單。                                                                            |
| `fields` | 物件 | 類型與欄位功能的對照表，其中每個鍵是欄位名稱，其值是一個物件。                  |
| `fields.<field>.<type>.type` | 字串 | 欄位的資料類型（例如 `float`、`text`、`keyword`）。                                                           |
| `fields.<field>.<type>.searchable` | 布林值 | 欄位是否已編製索引且可供搜尋。對於使用可插拔資料格式的索引，下列類型的欄位此值為 `false`：數值、`date`、`date_nanos`、`ip` 和 `boolean`。這些類型的欄位未編製索引，但 OpenSearch 仍會使用 doc values 對這些欄位執行 `range`、`term` 和 `terms` 查詢。如需詳細資訊，請參閱[可插拔資料格式索引]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/#pluggable-data-format-indexes)。 |
| `fields.<field>.<type>.aggregatable` | 布林值 | 欄位是否可用於 `sum` 或 `terms` 等彙總。                                                  |
| `fields.<field>.<type>.indices` | 清單 | 此欄位以對應類型出現的索引清單。                                                  |
| `fields.<field>.<type>.non_searchable_indices` | 清單或 null | 此欄位*無法*搜尋的索引清單。`null` 表示此欄位在任何索引中皆無法搜尋。                                   |
| `fields.<field>.<type>.non_aggregatable_indices` | 清單或 null | 此欄位*無法*彙總的索引清單。`null` 表示此欄位在任何索引中皆無法彙總。                               |
| `fields.<field>.<type>.meta` | 物件 | 從所有對應合併而來的中繼資料值。鍵為自訂中繼資料鍵，值為跨索引的值陣列。 |

## 必要權限

若您使用 Security 外掛程式，請確認您具有適當的權限：`indices:data/read/field_caps` 和 `indices:data/read/field_caps*`。
