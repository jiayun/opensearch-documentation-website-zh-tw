---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "支援的欄位類型"
nav_order: 80
has_children: true
has_toc: false
redirect_from:
  - /opensearch/supported-field-types/
  - /opensearch/supported-field-types/index/
  - /field-types/supported-field-types/
  - /field-types/supported-field-types/index/
  - /mappings/supported-field-types/
---

# 支援的欄位類型

您可以在建立對應時為欄位指定資料類型。以下各節依用途或資料結構將支援的欄位類型分組。

## 核心欄位類型

| 欄位類型  | 說明 |
| [`alias`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/alias/)           | 現有欄位的替代名稱。                                 |
| [`boolean`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/boolean/)       | true/false 值。                                                      |
| [`binary`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/binary/)         | 以 Base64 編碼的二進位值。                                       |

## 字串類欄位類型

| 欄位類型  | 說明 |
| [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/)                       | 經過分析的全文字串。                                 |
| [`match_only_text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/match-only-text/) | `text` 的輕量版本，適用於僅供搜尋的使用情境。 |
| [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/)                 | 未經分析的字串，適合用於精確比對。           |
| [`constant_keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/constant-keyword/) | 對索引中的所有文件使用相同的值。      |
| [`icu_collation_keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/icu-collation-keyword/) | 特定語言的 keyword 欄位，可依定序規則排序。 |
| [`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/)               | 啟用高效率的子字串與正規表達式比對。            |
| [`token_count`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/token-count/)         | 儲存分析後的詞元數量。                |
| [`version`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/version/)                 | 遵循語意化版本規範的語意化版本字串。 |

## 數值欄位類型

| 欄位類型  | 說明 |
| [`byte`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)       | 帶正負號的 8 位元整數。最小值為 −128。最大值為 127。                                |
| [`short`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)      | 帶正負號的 16 位元整數。最小值為 −2¹⁵。最大值為 2¹⁵ − 1。                          |
| [`integer`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)    | 帶正負號的 32 位元整數。最小值為 −2³¹。最大值為 2³¹ − 1。                          |
| [`long`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)       | 帶正負號的 64 位元整數。最小值為 −2⁶³。最大值為 2⁶³ − 1。                          |
| [`unsigned_long`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/unsigned-long/) | 不帶正負號的 64 位元整數。最小值為 0。最大值為 2⁶⁴ − 1。          |
| [`half_float`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/) | 半精確度 16 位元 IEEE 754 浮點數值。最大量值為 65504。     |
| [`float`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)      | 單精確度 32 位元 IEEE 754 浮點數值。                                |
| [`double`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/)     | 雙精確度 64 位元 IEEE 754 浮點數值。                                |
| [`scaled_float`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/numeric/) | 浮點數值，會乘以 double 縮放係數並以 long 值儲存。 |

## 日期與時間欄位類型

| 欄位類型  | 說明 |
| [`date`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date/)             | 以毫秒儲存的日期或時間戳記。 |
| [`date_nanos`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/date-nanos/) | 以奈秒儲存的日期或時間戳記。  |

## IP 欄位類型

| 欄位類型  | 說明 |
| [`ip`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/ip/)               | 儲存 IPv4 或 IPv6 位址。  |

## 地理欄位類型

| 欄位類型  | 說明 |
| [`geo_point`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-point/) | 以緯度和經度指定的地理點。 |
| [`geo_shape`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/geo-shape/) | 地理形狀，例如多邊形或地理點的集合。 |

## 笛卡兒欄位類型

| 欄位類型  | 說明 |
| [`xy_point`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/xy-point/) | 二維笛卡兒座標系統中的點。 |
| [`xy_shape`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/xy-shape/) | 二維笛卡兒座標系統中的形狀。 |

## 範圍欄位類型

| 欄位類型  | 說明 |
| [`integer_range`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/) | 整數值的範圍。 |
| [`long_range`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/) | long 值的範圍。 |
| [`double_range`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/) | double 值的範圍。 |
| [`float_range`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/) | float 值的範圍。 |
| [`ip_range`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/) | IPv4 或 IPv6 格式的 IP 位址範圍。 |
| [`date_range`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/range/) | 日期值的範圍。 |

## 物件欄位類型

| 欄位類型  | 說明 |
| [`object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/object/)           | JSON 物件。                                           |
| [`nested`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)           | JSON 物件的陣列，會以個別文件編製索引。 |
| [`flat_object`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/) | 視為字串扁平對應的 JSON 物件。          |
| [`join`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/)               | 定義文件之間的父子關係。    |

## 自動完成欄位類型

| 欄位類型  | 說明 |
| [`completion`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/completion/)                 | 使用建議器支援自動完成功能。                                                                                    |
| [`search_as_you_type`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/search-as-you-type/) | 啟用前綴與中綴的隨打即搜查詢。                                                                                      |

## 向量欄位類型

| 欄位類型  | 說明 |
| [`knn_vector`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/knn-vector/)                 | 為 k-NN 搜尋與向量相似度作業編製稠密向量的索引。                                                                   |
| [`sparse_vector`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/sparse-vector/)               | 為[神經稀疏 ANN 搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-ann/)編製稀疏向量的索引。 |

## 特殊搜尋欄位類型

| 欄位類型  | 說明 |
| [`semantic`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/semantic/)                     | 包裝文字或二進位欄位，以簡化語意搜尋的設定。                                                                           |
| [`rank_feature`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/)                     | 提升或降低文件的相關性分數。                                                                                     |
| [`rank_features`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/rank/)                    | 提升或降低文件的相關性分數。用於特徵清單稀疏的情況。                                          |
| [`percolator`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/percolator/)                 | 一種欄位，可作為反向搜尋作業的預存查詢。                                                                        |
| [`star_tree`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/star-tree/)                   | 使用 [star-tree 索引](https://docs.pinot.apache.org/basics/indexing/star-tree-index) 預先計算彙總，以提升效能。 |
| [`derived`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/derived/)                       | 一種動態產生的欄位，透過指令碼從其他欄位計算而得。                                                                  |


## 陣列

OpenSearch 中沒有專用的陣列欄位類型。相反地，您可以將值陣列傳入任何欄位。陣列中的所有值必須具有相同的欄位類型。

```json
PUT testindex1/_doc/1
{
  "number": 1 
}

PUT testindex1/_doc/2
{
  "number": [1, 2, 3] 
}
```

`semantic` 欄位不能包含值陣列，因為它被對應至嵌入欄位（`rank_features` 或 `knn_vector`），而該欄位僅支援單一向量。
{: .note}

## 多重欄位

多重欄位用於以不同方式為同一欄位編製索引。字串通常會對應為 `text` 以進行全文查詢，並對應為 `keyword` 以進行精確值查詢。

多重欄位可以使用 `fields` 參數建立。例如，您可以將書籍的 `title` 對應為 `text` 類型，並保留一個 `title.raw` 子欄位，其類型為 `keyword`。

```json
PUT books
{
  "mappings" : {
    "properties" : {
      "title" : {
        "type" : "text",
        "fields" : {
          "raw" : {
            "type" : "keyword"
          }
        }
      }
    }
  }
}
```

## Null 值

將欄位的值設為 `null`、空陣列，或由 `null` 值組成的陣列，會使該欄位等同於空欄位。因此，您無法搜尋在該欄位中具有 `null` 的文件。

若要讓欄位可搜尋 `null` 值，您可以在索引的對應中指定其 `null_value` 參數。之後，所有傳入該欄位的 `null` 值都會被替換為指定的 `null_value`。

`null_value` 參數必須與欄位具有相同的類型。例如，如果您的欄位是字串，則該欄位的 `null_value` 也必須是字串。
{: .note}

### 範例

建立一個對應，將 `emergency_phone` 欄位中的 `null` 值替換為字串 "NONE"：

```json
PUT testindex
{
  "mappings": {
    "properties": {
      "name": {
        "type": "keyword"
      },
      "emergency_phone": {
        "type": "keyword",
        "null_value": "NONE" 
      }
    }
  }
}
```

將三份文件編製索引至 `testindex`。文件 1 和 3 的 `emergency_phone` 欄位包含 `null`，而文件 2 的 `emergency_phone` 欄位則是空陣列：

```json
PUT testindex/_doc/1
{
  "name": "Akua Mansa",
  "emergency_phone": null
}
```

```json
PUT testindex/_doc/2
{
  "name": "Diego Ramirez",
  "emergency_phone" : []
}
```

```json
PUT testindex/_doc/3 
{
  "name": "Jane Doe",
  "emergency_phone": [null, null]
}
```

搜尋沒有緊急電話的人：

```json
GET testindex/_search
{
  "query": {
    "term": {
      "emergency_phone": "NONE"
    }
  }
}
```

回應包含文件 1 和 3，但不包含文件 2，因為只有明確的 `null` 值會被替換為字串 "NONE"：

```json
{
  "took" : 1,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.18232156,
    "hits" : [
      {
        "_index" : "testindex",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 0.18232156,
        "_source" : {
          "name" : "Akua Mansa",
          "emergency_phone" : null
        }
      },
      {
        "_index" : "testindex",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 0.18232156,
        "_source" : {
          "name" : "Jane Doe",
          "emergency_phone" : [
            null,
            null
          ]
        }
      }
    ]
  }
}
```

`_source` 欄位仍包含明確的 `null` 值，因為它不受 `null_value` 影響。
{: .note}
