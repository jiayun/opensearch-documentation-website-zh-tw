---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "多重詞彙向量"
parent: Document APIs
nav_order: 80
---

# 多重詞彙向量 API
**於 1.0 版引入**
{: .label .label-purple }

`_mtermvectors` API 可在單一請求中擷取多份文件的詞彙向量資訊。詞彙向量提供文件中詞彙（單字）的詳細資訊，包括詞彙頻率、位置、位移和承載資料。這些資訊可用於相關性評分、醒目標示或相似度計算等應用。如需詳細資訊，請參閱[詞彙向量參數]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/#term-vector-parameter)。

<!-- spec_insert_start
api: mtermvectors
component: endpoints
-->
## 端點
```json
GET  /_mtermvectors
POST /_mtermvectors
GET  /{index}/_mtermvectors
POST /{index}/_mtermvectors
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: mtermvectors
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `index` | 字串 | 包含該文件的索引名稱。 |

<!-- spec_insert_end -->

<!-- spec_insert_start
api: mtermvectors
component: query_parameters
columns: Parameter, Data type, Description
-->
## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `field_statistics` | 布林值 | 若為 `true`，回應會包含文件數、文件頻率總和，以及詞彙總頻率的總和。 _（預設：`true`）_ |
| `fields` | 清單或字串 | 以逗號分隔的清單或萬用字元運算式，用來指定統計資料要包含的欄位。除非在 `completion_fields` 或 `fielddata_fields` 參數中提供特定欄位清單，否則會使用此清單作為預設清單。 |
| `ids` | 清單 | 以逗號分隔的文件 ID 清單。您必須在請求本文中提供 `docs` 欄位，或將 `ids` 指定為查詢參數或放在請求本文中。 |
| `offsets` | 布林值 | 若為 `true`，回應會包含詞彙位移。 _（預設：`true`）_ |
| `payloads` | 布林值 | 若為 `true`，回應會包含詞彙承載資料。 _（預設：`true`）_ |
| `positions` | 布林值 | 若為 `true`，回應會包含詞彙位置。 _（預設：`true`）_ |
| `preference` | 字串 | 指定應執行操作的節點或分片。如需可用選項清單，請參閱 [preference 查詢參數]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#the-preference-query-parameter)。依預設，請求會隨機路由至可用的分片複本（主要分片或副本分片），且不保證重複查詢時的一致性。 |
| `realtime` | 布林值 | 若為 `true`，請求會以即時而非近即時方式執行。 _（預設：`true`）_ |
| `routing` | 清單或字串 | 用來將操作路由至特定分片的自訂值。 |
| `term_statistics` | 布林值 | 若為 `true`，回應會包含詞彙頻率和文件頻率。 _（預設：`false`）_ |
| `version` | 整數 | 若為 `true`，會將文件版本作為命中結果的一部分回傳。 |
| `version_type` | 字串 | 特定的版本類型。<br> 有效值如下：<br> - `external`：版本號碼必須大於目前版本。<br> - `external_gte`：版本號碼必須大於或等於目前版本。<br> - `internal`：版本號碼由 OpenSearch 內部管理。 |

<!-- spec_insert_end -->

## 請求本文欄位

下表列出可在請求本文中指定的欄位。

| 欄位 | 資料類型 | 說明 |
| `docs` | 陣列 | 文件規格的陣列。 |
| `ids` | 字串陣列 | 要擷取的文件 ID 清單。僅在所有文件皆屬於請求路徑或查詢中指定的同一個索引時使用。 |
| `fields` | 字串陣列 | 要回傳詞彙向量的欄位名稱清單。 |
| `offsets` | 布林值 | 若為 `true`，回應會包含每個詞彙的字元位移。 *（預設：`true`）* |
| `payloads` | 布林值 | 若為 `true`，回應會包含每個詞彙的承載資料。 *（預設：`true`）* |
| `positions` | 布林值 | 若為 `true`，回應會包含詞元位置。 *（預設：`true`）* |
| `field_statistics` | 布林值 | 若為 `true`，回應會包含文件數、文件頻率總和，以及詞彙總頻率的總和等統計資料。 *（預設：`true`）* |
| `term_statistics` | 布林值 | 若為 `true`，回應會包含詞彙頻率和文件頻率。 *（預設：`false`）* |
| `routing` | 字串 | 用來識別分片的自訂路由值。若在編製索引時使用自訂路由，則此欄位為必要。 |
| `version` | 整數 | 要擷取的文件特定版本。 |
| `version_type` | 字串 | 要使用的版本控制類型。有效值：`internal`、`external`、`external_gte`。 |
| `filter` | 物件 | 篩選回應中回傳的詞元（例如依頻率或位置篩選）。如需支援的欄位，請參閱[篩選詞彙]({{site.url}}{{site.baseurl}}/api-reference/document-apis/mtermvectors/#filtering-terms)。 |
| `per_field_analyzer` | 物件 | 指定各欄位要使用的自訂分析器。格式：`{ "field_name": "analyzer_name" }`。 |

## 篩選詞彙

請求本文中的 `filter` 物件可讓您篩選要納入詞彙向量回應的詞元。`filter` 物件支援下列欄位。

| 欄位 | 資料類型 | 說明 |
| `max_num_terms` | 整數 | 要回傳的詞彙數量上限。 |
| `min_term_freq` | 整數 | 詞彙要被納入時，其在文件中的詞彙頻率下限。 |
| `max_term_freq` | 整數 | 詞彙要被納入時，其在文件中的詞彙頻率上限。 |
| `min_doc_freq` | 整數 | 詞彙要被納入時，其在整個索引中的文件頻率下限。 |
| `max_doc_freq` | 整數 | 詞彙要被納入時，其在整個索引中的文件頻率上限。 |
| `min_word_length` | 整數 | 要納入的詞彙長度下限。 |
| `max_word_length` | 整數 | 要納入的詞彙長度上限。 |

## 請求範例


建立已啟用詞彙向量的索引：

```json
PUT /my-index
{
  "mappings": {
    "properties": {
      "text": {
        "type": "text",
        "term_vector": "with_positions_offsets_payloads"
      }
    }
  }
}
```
{% include copy-curl.html %}

將第一份文件編製索引：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/_doc/1
body: |
{
  "text": "OpenSearch is a search engine."
}
-->
{% capture step1_rest %}
POST /my-index/_doc/1
{
  "text": "OpenSearch is a search engine."
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "my-index",
  id = "1",
  body =   {
    "text": "OpenSearch is a search engine."
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

將第二份文件編製索引：

<!-- spec_insert_start
component: example_code
rest: POST /my-index/_doc/2
body: |
{
  "text": "OpenSearch provides powerful features."
}
-->
{% capture step1_rest %}
POST /my-index/_doc/2
{
  "text": "OpenSearch provides powerful features."
}
{% endcapture %}

{% capture step1_python %}


response = client.index(
  index = "my-index",
  id = "2",
  body =   {
    "text": "OpenSearch provides powerful features."
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 請求範例

取得多份文件的詞項向量：

<!-- spec_insert_start
component: example_code
rest: POST /_mtermvectors
body: |
{
  "docs": [
    {
      "_index": "my-index",
      "_id": "1",
      "fields": ["text"]
    },
    {
      "_index": "my-index",
      "_id": "2",
      "fields": ["text"]
    }
  ]
}
-->
{% capture step1_rest %}
POST /_mtermvectors
{
  "docs": [
    {
      "_index": "my-index",
      "_id": "1",
      "fields": [
        "text"
      ]
    },
    {
      "_index": "my-index",
      "_id": "2",
      "fields": [
        "text"
      ]
    }
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.mtermvectors(
  body =   {
    "docs": [
      {
        "_index": "my-index",
        "_id": "1",
        "fields": [
          "text"
        ]
      },
      {
        "_index": "my-index",
        "_id": "2",
        "fields": [
          "text"
        ]
      }
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

或者，您可以將 `ids` 和 `fields` 都指定為查詢參數：

<!-- spec_insert_start
component: example_code
rest: GET /my-index/_mtermvectors?ids=1,2&fields=text
-->
{% capture step1_rest %}
GET /my-index/_mtermvectors?ids=1,2&fields=text
{% endcapture %}

{% capture step1_python %}


response = client.mtermvectors(
  index = "my-index",
  params = { "ids": "1,2", "fields": "text" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

您也可以在 `ids` 陣列中提供文件 ID，而不指定 `docs`：

<!-- spec_insert_start
component: example_code
rest: GET /my-index/_mtermvectors?fields=text
body: |
{
  "ids": [
     "1", "2"
  ]
}
-->
{% capture step1_rest %}
GET /my-index/_mtermvectors?fields=text
{
  "ids": [
    "1",
    "2"
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.mtermvectors(
  index = "my-index",
  params = { "fields": "text" },
  body =   {
    "ids": [
      "1",
      "2"
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 回應範例

回應包含這兩份文件的詞項向量資訊：

```json
{
  "docs": [
    {
      "_index": "my-index",
      "_id": "1",
      "_version": 1,
      "found": true,
      "took": 10,
      "term_vectors": {
        "text": {
          "field_statistics": {
            "sum_doc_freq": 9,
            "doc_count": 2,
            "sum_ttf": 9
          },
          "terms": {
            "a": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 2,
                  "start_offset": 14,
                  "end_offset": 15
                }
              ]
            },
            "engine": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 4,
                  "start_offset": 23,
                  "end_offset": 29
                }
              ]
            },
            "is": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 1,
                  "start_offset": 11,
                  "end_offset": 13
                }
              ]
            },
            "opensearch": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 0,
                  "start_offset": 0,
                  "end_offset": 10
                }
              ]
            },
            "search": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 3,
                  "start_offset": 16,
                  "end_offset": 22
                }
              ]
            }
          }
        }
      }
    },
    {
      "_index": "my-index",
      "_id": "2",
      "_version": 1,
      "found": true,
      "took": 0,
      "term_vectors": {
        "text": {
          "field_statistics": {
            "sum_doc_freq": 9,
            "doc_count": 2,
            "sum_ttf": 9
          },
          "terms": {
            "features": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 3,
                  "start_offset": 29,
                  "end_offset": 37
                }
              ]
            },
            "opensearch": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 0,
                  "start_offset": 0,
                  "end_offset": 10
                }
              ]
            },
            "powerful": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 2,
                  "start_offset": 20,
                  "end_offset": 28
                }
              ]
            },
            "provides": {
              "term_freq": 1,
              "tokens": [
                {
                  "position": 1,
                  "start_offset": 11,
                  "end_offset": 19
                }
              ]
            }
          }
        }
      }
    }
  ]
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| -------- | --------- | ----------- |
| `docs` | 陣列 | 請求的文件清單，包含詞項向量。 |

`docs` 陣列中的每個元素都包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| -------- | --------- | ----------- |
| `term_vectors` | 物件 | 包含各欄位的詞項向量資料。 |
| `term_vectors.<field>.field_statistics` | 物件 | 包含欄位的統計資料。 |
| `term_vectors.<field>.field_statistics.doc_count` | 整數 | 在指定欄位中包含至少一個詞項的文件數量。 |
| `term_vectors.<field>.field_statistics.sum_doc_freq` | 整數 | 欄位中所有詞項的文件頻率總和。 |
| `term_vectors.<field>.field_statistics.sum_ttf` | 整數 | 欄位中所有詞項的總詞項頻率總和。 |
| `term_vectors.<field>.terms` | 物件 | 欄位中詞項的對應表，其中每個詞項都包含其頻率（`term_freq`）及相關的詞元資訊。 |
| `term_vectors.<field>.terms.<term>.tokens` | 陣列 | 每個詞項的詞元物件陣列，包含詞元在文字中的 `position` 及其字元位移（`start_offset` 和 `end_offset`）。 |

## 必要權限

如果您使用 Security 外掛程式，請確定您具備適當的權限：`indices:data/read/mtv` 和 `indices:data/read/mtv*`。
