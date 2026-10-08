---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多詞彙"
parent: Bucket aggregations
nav_order: 130
redirect_from:
  - /query-dsl/aggregations/bucket/multi-terms/
  - /query-dsl/aggregations/multi-terms/
---

# 多詞彙彙總

`multi_terms` 彙總會根據多個欄位值的組合來建立桶 (bucket)。每個桶代表一個唯一的複合鍵，文件必須同時符合所有指定的詞彙值，才會分到同一組。當您需要找出依文件計數或指標子彙總排名的前幾名組合時，這項功能非常實用。

由於 `multi_terms` 彙總會跨多個欄位建立複合鍵，因此比單一 `terms` 彙總耗用更多記憶體。
{: .note}

## 參數

`multi_terms` 彙總接受下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `terms` | 必要 | 陣列 | 物件陣列，每個物件指定一個欄位或指令碼，用於提供複合鍵的其中一部分。 |
| `size` | 選用 | 整數 | 要傳回的複合桶數量。預設為 `10`。 |
| `shard_size` | 選用 | 整數 | 從每個分片收集的候選桶數量。數值越高可提升準確度，但會耗用更多記憶體。必須大於或等於 `size`。預設值高於 `size`，以提升準確度。 |
| `min_doc_count` | 選用 | 整數 | 桶出現在回應中所需的最低文件計數。預設為 `1`。 |
| `order` | 選用 | 物件 | 控制桶的排序方式。接受 `_count`、`_key` 或子彙總指標的名稱。預設為 `{"_count": "desc"}`。 |
| `show_term_doc_count_error` | 選用 | 布林值 | 若為 `true`，則包含每個詞彙文件計數的誤差估計值。預設為 `false`。 |

`terms` 陣列中的每個物件都支援下列參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `field` | 字串 | 要進行彙總的欄位。必須是 `keyword`、`numeric`、`ip`、`boolean` 或 `date` 欄位。必須提供 `field` 或 `script` 其中之一。 |
| `script` | 物件 | 產生要彙總之值的指令碼。必須提供 `field` 或 `script` 其中之一。與 `field` 搭配使用時，指令碼會作為值指令碼，並以 `_value` 接收欄位值。 |
| `missing` | 字串或數字 | 用於不含該欄位之文件的值。根據預設，不含該欄位的文件會從彙總中排除。 |
| `exclude` | 字串或字串陣列 | 要從彙總中排除的值。請指定確切值的陣列或規則運算式。 |
| `format` | 字串 | 詞彙在 `key_as_string` 中的格式，例如 `date` 欄位的日期格式。 |
| `time_zone` | 字串 | 用於格式化 `date` 值的時區，例如 `+05:00` 或 `America/New_York`。預設為 `UTC`。 |
| `value_type` | 字串 | 由 `script` 產生之值的資料類型，例如 `long` 或 `string`。 |

## 範例：依多個欄位分組

下列範例同時依 `customer_gender` 與 `category` 將訂單分組，找出各性別最熱門的產品類別。此查詢會顯示產生最多訂單的性別與類別組合：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "gender_category": {
      "multi_terms": {
        "terms": [
          { "field": "customer_gender" },
          { "field": "category.keyword" }
        ],
        "size": 5
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含依文件計數遞減排序的複合鍵桶：

```json
{
  ...
  "aggregations": {
    "gender_category": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 756,
      "buckets": [
        {
          "key": [
            "MALE",
            "Men's Clothing"
          ],
          "key_as_string": "MALE|Men's Clothing",
          "doc_count": 1963
        },
        {
          "key": [
            "FEMALE",
            "Women's Clothing"
          ],
          "key_as_string": "FEMALE|Women's Clothing",
          "doc_count": 1903
        },
        {
          "key": [
            "FEMALE",
            "Women's Shoes"
          ],
          "key_as_string": "FEMALE|Women's Shoes",
          "doc_count": 1136
        },
        {
          "key": [
            "MALE",
            "Men's Shoes"
          ],
          "key_as_string": "MALE|Men's Shoes",
          "doc_count": 921
        },
        {
          "key": [
            "FEMALE",
            "Women's Accessories"
          ],
          "key_as_string": "FEMALE|Women's Accessories",
          "doc_count": 730
        }
      ]
    }
  }
}
```

## 範例：依子彙總指標排序

下列範例會找出平均訂單金額最高的性別與類別組合：

```json
GET /opensearch_dashboards_sample_data_ecommerce/_search
{
  "size": 0,
  "aggs": {
    "gender_category": {
      "multi_terms": {
        "terms": [
          { "field": "customer_gender" },
          { "field": "category.keyword" }
        ],
        "size": 3,
        "order": { "avg_price": "desc" }
      },
      "aggs": {
        "avg_price": {
          "avg": { "field": "taxful_total_price" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應會依 `avg_price` 子彙總 (而非文件計數) 對桶進行排名：

```json
{
  ...
  "aggregations": {
    "gender_category": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 5252,
      "buckets": [
        {
          "key": [
            "MALE",
            "Women's Accessories"
          ],
          "key_as_string": "MALE|Women's Accessories",
          "doc_count": 100,
          "avg_price": {
            "value": 101.21328125
          }
        },
        {
          "key": [
            "MALE",
            "Men's Shoes"
          ],
          "key_as_string": "MALE|Men's Shoes",
          "doc_count": 921,
          "avg_price": {
            "value": 97.41267983170466
          }
        },
        {
          "key": [
            "FEMALE",
            "Women's Shoes"
          ],
          "key_as_string": "FEMALE|Women's Shoes",
          "doc_count": 1136,
          "avg_price": {
            "value": 92.8513836927817
          }
        }
      ]
    }
  }
}
```

## 範例：處理缺少欄位的文件

根據預設，若文件不含其中一個 `terms` 欄位，就會從彙總中排除。若要納入這些文件，請為該欄位指定 `missing` 值。

建立包含兩個 `keyword` 欄位的索引：

```json
PUT /products
{
  "mappings": {
    "properties": {
      "brand": { "type": "keyword" },
      "color": { "type": "keyword" }
    }
  }
}
```
{% include copy-curl.html %}

將三份文件編製索引。第二份文件不含 `color` 欄位，第三份文件不含 `brand` 欄位：

```json
POST /products/_bulk?refresh=true
{ "index": {} }
{ "brand": "Acme", "color": "red" }
{ "index": {} }
{ "brand": "Acme" }
{ "index": {} }
{ "color": "blue" }
```
{% include copy-curl.html %}

下列請求會依品牌與顏色將產品分組，並將值 `unknown` 指派給不含 `color` 欄位的文件：

```json
GET /products/_search
{
  "size": 0,
  "aggs": {
    "brand_color": {
      "multi_terms": {
        "terms": [
          { "field": "brand" },
          { "field": "color", "missing": "unknown" }
        ]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應中包含一個代表不含 `color` 欄位之文件的桶，並以 `unknown` 作為其顏色。由於未對 `brand` 指定 `missing` 值，因此不含 `brand` 欄位的文件不會出現在任何桶中：

```json
{
  ...
  "aggregations": {
    "brand_color": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": [
            "Acme",
            "red"
          ],
          "key_as_string": "Acme|red",
          "doc_count": 1
        },
        {
          "key": [
            "Acme",
            "unknown"
          ],
          "key_as_string": "Acme|unknown",
          "doc_count": 1
        }
      ]
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count_error_upper_bound` | 整數 | 未包含在回應中的任何桶，其文件計數的最大潛在誤差。 |
| `sum_other_doc_count` | 整數 | 未進入前 `size` 名結果之所有桶的文件總數。 |
| `buckets` | 陣列 | 複合鍵桶，依據 `order` 排序。 |
| `buckets.key` | 陣列 | 代表此桶複合鍵的值陣列，順序與 `terms` 清單相同。 |
| `buckets.key_as_string` | 字串 | 格式化為以直線符號分隔之字串的複合鍵。 |
| `buckets.doc_count` | 整數 | 符合此鍵組合的文件數量。 |
