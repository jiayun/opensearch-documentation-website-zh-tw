---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙向量"
parent: Document APIs
nav_order: 70
---

# 詞彙向量 API
**1.0 版引入**
{: .label .label-purple }

`_termvectors` API 會擷取單一文件的詞彙向量資訊。詞彙向量提供文件中詞彙（字詞）的詳細資訊，包括詞彙頻率、位置、位移和酬載。這對於相關性評分、醒目提示或相似度計算等應用程式很有用。如需更多資訊，請參閱[詞彙向量參數]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/#term-vector-parameter)。

<!-- spec_insert_start
api: termvectors
component: endpoints
-->
## 端點
```json
GET  /{index}/_termvectors
POST /{index}/_termvectors
GET  /{index}/_termvectors/{id}
POST /{index}/_termvectors/{id}
```
<!-- spec_insert_end -->

<!-- spec_insert_start
api: termvectors
component: path_parameters
-->
## 路徑參數

下表列出可用的路徑參數。

| 參數 | 必要 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `index` | **必要** | 字串 | 包含該文件的索引名稱。 |
| `id` | _選用_ | 字串 | 文件的唯一識別碼。 |

<!-- spec_insert_end -->

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `field_statistics` | 布林值 | 若為 `true`，回應會包含文件計數、文件頻率總和及總詞彙頻率總和。*（預設：`true`）* |
| `fields` | 清單或字串 | 以逗號分隔的清單或萬用字元運算式，指定要納入統計資料的欄位。除非在 `completion_fields` 或 `fielddata_fields` 參數中提供特定的欄位清單，否則會作為預設清單使用。 |
| `offsets` | 布林值 | 若為 `true`，回應會包含詞彙位移。*（預設：`true`）* |
| `payloads` | 布林值 | 若為 `true`，回應會包含詞彙酬載。*（預設：`true`）* |
| `positions` | 布林值 | 若為 `true`，回應會包含詞彙位置。*（預設：`true`）* |
| `preference` | 字串 | 指定應執行此操作的節點或分片。如需可用選項清單，請參閱 [preference 查詢參數]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#the-preference-query-parameter)。預設會將請求隨機路由至可用的分片副本（主要分片或副本分片），不保證重複查詢之間的一致性。 |
| `realtime` | 布林值 | 若為 `true`，請求為即時，而非近乎即時。*（預設：`true`）* |
| `routing` | 清單或字串 | 用於將操作路由至特定分片的自訂值。 |
| `term_statistics` | 布林值 | 若為 `true`，回應會包含詞彙頻率和文件頻率。*（預設：`false`）* |
| `version` | 整數 | 若為 `true`，會在命中結果中傳回文件版本。 |
| `version_type` | 字串 | 特定的版本類型。<br> 有效值為：<br> - `external`：版本號碼必須大於目前版本。<br> - `external_gte`：版本號碼必須大於或等於目前版本。<br> - `force`：版本號碼會強制設為指定的值。<br> - `internal`：版本號碼由 OpenSearch 在內部管理。 |

## 請求本文欄位

下表列出可在請求本文中指定的欄位。

| 欄位 | 資料類型 | 說明 |
| `doc` | 物件 | 要分析的文件。若有提供，API 不會從索引擷取現有文件，而是使用所提供的內容。 |
| `fields` | 字串陣列 | 要傳回詞彙向量的欄位名稱清單。 |
| `offsets` | 布林值 | 若為 `true`，回應會包含每個詞彙的字元位移。*（預設：`true`）* |
| `payloads` | 布林值 | 若為 `true`，回應會包含每個詞彙的酬載。*（預設：`true`）* |
| `positions` | 布林值 | 若為 `true`，回應會包含詞元位置。*（預設：`true`）* |
| `field_statistics` | 布林值 | 若為 `true`，回應會包含統計資料，例如文件計數、文件頻率總和及總詞彙頻率總和。*（預設：`true`）* |
| `term_statistics` | 布林值 | 若為 `true`，回應會包含詞彙頻率和文件頻率。*（預設：`false`）* |
| `routing` | 字串 | 用於識別分片的自訂路由值。若編製索引時使用了自訂路由，則為必要。 |
| `version` | 整數 | 要擷取的文件特定版本。 |
| `version_type` | 字串 | 要使用的版本控制類型。有效值：`internal`、`external`、`external_gte`、`force`。 |
| `filter` | 物件 | 允許篩選回應中傳回的詞元（例如依頻率或位置）。如需可用選項，請參閱[篩選詞彙]({{site.url}}{{site.baseurl}}/api-reference/document-apis/termvector/#filtering-terms)。 |
| `per_field_analyzer` | 物件 | 指定每個欄位要使用的自訂分析器。格式：`{ "field_name": "analyzer_name" }`。 | 
| `preference` | 字串 | 指定分片或節點路由偏好設定。請參閱 [preference 查詢參數]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/#the-preference-query-parameter)。|

## 篩選詞彙

請求本文中的 `filter` 物件可讓您篩選要納入詞彙向量回應的詞元。`filter` 物件支援下列欄位。

| 欄位 | 資料類型 | 說明 |
| `max_num_terms` | 整數 | 要傳回的詞彙數目上限。 |
| `min_term_freq` | 整數 | 詞彙要被納入時，在文件中所需的最低詞彙頻率。 |
| `max_term_freq` | 整數 | 詞彙要被納入時，在文件中所需的最高詞彙頻率。 |
| `min_doc_freq` | 整數 | 詞彙要被納入時，在整個索引中所需的最低文件頻率。 |
| `max_doc_freq` | 整數 | 詞彙要被納入時，在整個索引中所需的最高文件頻率。 |
| `min_word_length` | 整數 | 要納入的詞彙最小長度。 |
| `max_word_length` | 整數 | 要納入的詞彙最大長度。 |

## 範例請求

建立索引：

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

將文件編製索引：

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

### 範例請求

擷取詞彙向量：

<!-- spec_insert_start
component: example_code
rest: GET /my-index/_termvectors/1
body: |
{
  "fields": ["text"],
  "term_statistics": true
}
-->
{% capture step1_rest %}
GET /my-index/_termvectors/1
{
  "fields": [
    "text"
  ],
  "term_statistics": true
}
{% endcapture %}

{% capture step1_python %}


response = client.termvectors(
  index = "my-index",
  id = "1",
  body =   {
    "fields": [
      "text"
    ],
    "term_statistics": true
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

或者，您可以將 `fields` 和 `term_statistics` 作為查詢參數提供：

<!-- spec_insert_start
component: example_code
rest: GET /my-index/_termvectors/1?fields=text&term_statistics=true
-->
{% capture step1_rest %}
GET /my-index/_termvectors/1?fields=text&term_statistics=true
{% endcapture %}

{% capture step1_python %}


response = client.termvectors(
  index = "my-index",
  id = "1",
  params = { "fields": "text", "term_statistics": "true" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 回應範例

回應會顯示詞項向量資訊：

```json
{
  "_index": "my-index",
  "_id": "1",
  "_version": 1,
  "found": true,
  "took": 1,
  "term_vectors": {
    "text": {
      "field_statistics": {
        "sum_doc_freq": 5,
        "doc_count": 1,
        "sum_ttf": 5
      },
      "terms": {
        "a": {
          "doc_freq": 1,
          "ttf": 1,
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
          "doc_freq": 1,
          "ttf": 1,
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
          "doc_freq": 1,
          "ttf": 1,
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
          "doc_freq": 1,
          "ttf": 1,
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
          "doc_freq": 1,
          "ttf": 1,
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
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| `term_vectors` | 物件 | 包含每個指定欄位的詞項向量資料。 |
| `term_vectors.text` | 物件 | 包含 `text` 欄位的詞項向量詳細資訊。 |
| `term_vectors.text.field_statistics` | 物件 | 包含整個欄位的統計資料。僅在 `field_statistics` 為 `true` 時出現。 |
| `term_vectors.text.field_statistics.doc_count` | 整數 | 在指定欄位中包含至少一個詞項的文件數量。 |
| `term_vectors.text.field_statistics.sum_doc_freq` | 整數 | 欄位中所有詞項的文件頻率總和。 |
| `term_vectors.text.field_statistics.sum_ttf` | 整數 | 欄位中所有詞項的總詞項頻率（包含重複出現次數）總和。 |
| `term_vectors.text.terms` | 物件 | 一個對應表，其中每個鍵都是一個詞項，每個值都包含該詞項的詳細資訊。 |
| `term_vectors.text.terms.<term>.term_freq` | 整數 | 詞項在文件中出現的次數。 |
| `term_vectors.text.terms.<term>.doc_freq` | 整數 | 包含該詞項的文件數量。僅在 `term_statistics` 為 `true` 時出現。 |
| `term_vectors.text.terms.<term>.ttf` | 整數 | 所有文件中的總詞項頻率。僅在 `term_statistics` 為 `true` 時出現。 |
| `term_vectors.text.terms.<term>.tokens` | 陣列 | 詞元物件清單，提供個別詞項實例的資訊。 |
| `term_vectors.text.terms.<term>.tokens[].position` | 整數 | 詞元在文字中的位置。僅在 `positions` 為 `true` 時出現。 |
| `term_vectors.text.terms.<term>.tokens[].start_offset` | 整數 | 詞元的起始字元位移。僅在 `offsets` 為 `true` 時出現。 |
| `term_vectors.text.terms.<term>.tokens[].end_offset` | 整數 | 詞元的結束字元位移。僅在 `offsets` 為 `true` 時出現。 |
| `term_vectors.text.terms.<term>.tokens[].payload` | 字串（Base64） | 與詞元相關聯的選用承載資料。僅在 `payloads` 為 `true` 且有可用資料時出現。 |

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:data/read/tv`。
