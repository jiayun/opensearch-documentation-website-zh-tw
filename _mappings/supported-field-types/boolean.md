---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "布林值"
nav_order: 15
has_children: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/boolean/
  - /opensearch/supported-field-types/boolean/
  - /field-types/boolean/
---

# 布林值欄位類型
**於 1.0 版推出**
{: .label .label-purple }

布林值欄位類型接受 `true` 或 `false` 值，或 `"true"` 或 `"false"` 字串。您也可以傳遞空字串（`""`）來取代 `false` 值。

## 範例

建立一個對應，其中 a、b 和 c 為布林值欄位：

```json
PUT testindex
{
  "mappings" : {
    "properties" :  {
      "a" : {
        "type" : "boolean"
      },
      "b" : {
        "type" : "boolean"
      },
      "c" : {
        "type" : "boolean"
      }
    }
  }
}
```
{% include copy-curl.html %}

將含有布林值的文件編製索引：

```json
PUT testindex/_doc/1 
{
  "a" : true,
  "b" : "true",
  "c" : ""
}
```
{% include copy-curl.html %}

結果，`a` 和 `b` 會設為 `true`，而 `c` 會設為 `false`。

搜尋所有 `c` 為 false 的文件：

```json
GET testindex/_search 
{
  "query": {
      "term" : {
        "c" : false
    }
  }
}
```
{% include copy-curl.html %}

## 參數

下表列出布林值欄位類型接受的參數。所有參數皆為選用。

參數 | 說明 
:--- | :--- 
`boost` | 一個浮點數值，指定此欄位對相關性分數的權重。大於 1.0 的值會提高欄位的相關性。介於 0.0 和 1.0 之間的值會降低欄位的相關性。預設為 1.0。可動態更新。
`doc_values` | 一個布林值，指定是否應將欄位儲存在磁碟上，以便用於彙總、排序或指令碼。預設為 `true`。
`index` | 一個布林值，指定欄位是否應可供搜尋。預設為 `true`。對於使用可插拔資料格式的索引，預設為 `false`，且不支援 `true`。如需更多資訊，請參閱[可插拔資料格式索引]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/index-parameter/#pluggable-data-format-indexes)。
`meta` | 接受此欄位的中繼資料。
[`null_value`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/index#null-value) | 用來取代 `null` 的值。必須與欄位類型相同。若未指定此參數，當欄位值為 `null` 時，該欄位會被視為缺少。預設為 `null`。
`store` | 一個布林值，指定是否應儲存欄位值，且可與 `_source` 欄位分開擷取。預設為 `false`。 

## 彙總和指令碼中的布林值

在布林值欄位的彙總中，`key` 會傳回數值（`true` 為 1，`false` 為 0），而 `key_as_string` 會傳回字串（`"true"` 或 `"false"`）。指令碼會針對布林值傳回 `true` 和 `false`。

### 範例

對欄位 `a` 執行詞彙彙總查詢：

```json
GET testindex/_search
{
  "aggs": {
    "agg1": {
      "terms": {
        "field": "a"
      }
    }
  },
  "script_fields": {
    "a": {
      "script": {
        "lang": "painless",
        "source": "doc['a'].value"
      }
    }
  }
}
```
{% include copy-curl.html %}

指令碼會將 `a` 的值傳回為 `true`，`key` 會將 `a` 的值傳回為 `1`，而 `key_as_string` 會將 `a` 的值傳回為 `"true"`：

```json
{
  "took" : 1133,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "testindex",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "fields" : {
          "a" : [
            true
          ]
        }
      }
    ]
  },
  "aggregations" : {
    "agg1" : {
      "doc_count_error_upper_bound" : 0,
      "sum_other_doc_count" : 0,
      "buckets" : [
        {
          "key" : 1,
          "key_as_string" : "true",
          "doc_count" : 1
        }
      ]
    }
  }
}
```

## 衍生的來源

當索引使用[衍生的來源]({{site.url}}{{site.baseurl}}/field-types/metadata-fields/source/#derived-source)時，OpenSearch 可能會在來源重建期間對多值 `boolean` 欄位中的值進行排序。下列範例顯示 OpenSearch 如何處理混合的 `boolean` 輸入。

建立一個啟用衍生的來源並設定名為 `a` 之 `boolean` 欄位的索引：

```json
PUT /sample-index1
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "a":  {"type": "boolean"}
    }
  }
}
```

將文件編製索引至該索引：

```json
PUT sample-index1/_doc/1
{
  "a": [false, "true", "false", true, ""]
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 如下：

```json
{
  "a": [false, false, false, true, true]
}
```

若欄位對應定義了[`null_value`]({{site.url}}{{site.baseurl}}/field-types/mapping-parameters/null-value/)，則在重建期間，任何匯入的 null 值都會被取代為該值。下列範例示範 `null_value` 如何影響衍生的來源輸出。

建立一個啟用衍生的來源並為 `boolean` 欄位 `a` 設定 `null_value` 的索引：

```json
PUT sample-index2
{
  "settings": {
    "index": {
      "derived_source": {
        "enabled": true
      }
    }
  },
  "mappings": {
    "properties": {
      "a":  {"type": "boolean", "null_value": true}
    }
  }
}
```

將文件編製索引至該索引：

```json
PUT sample-index2/_doc/1
{
  "a": [null, true, "false"]
}
```

在 OpenSearch 重建 `_source` 之後，衍生的 `_source` 如下：

```json
{
  "a": [false, true, true]
}
```
