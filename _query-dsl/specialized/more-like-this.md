---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更多相似內容"
parent: Specialized queries
nav_order: 45
has_math: false
---

# 更多相似內容

使用 `more_like_this` 查詢來尋找與一或多份指定文件相似的文件。這對推薦引擎、內容探索，以及識別資料集中的相關項目非常有用。

`more_like_this` 查詢會分析輸入的文件或文字，並選出最能代表其特性的詞彙，然後搜尋包含這些重要詞彙的其他文件。

## 必要條件

使用 `more_like_this` 查詢之前，請確定目標欄位已編製索引，且其資料類型為 [`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 或 [`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/)。

如果您在 `like` 區段中參照文件，OpenSearch 需要能夠存取其內容。這通常是透過 `_source` 欄位完成，該欄位預設為啟用。如果 `_source` 已停用，您必須個別儲存這些欄位，或將它們設定為儲存 [`term_vector`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/term-vector/) 資料。

在為文件編製索引時儲存 [`term_vector`]({{site.url}}{{site.baseurl}}/mappings/mapping-parameters/term-vector/) 資訊，可以大幅加速 `more_like_this` 查詢，因為引擎可以直接擷取重要詞彙，而不必在查詢時重新分析欄位文字。
{: .note}

## 範例：無詞彙向量最佳化

使用下列對應建立名為 `articles-basic` 的索引：

```json
PUT /articles-basic
{
  "mappings": {
    "properties": {
      "title": { "type": "text" },
      "content": { "type": "text" }
    }
  }
}
```
{% include copy-curl.html %}

新增範例文件：

```json
POST /articles-basic/_bulk
{ "index": { "_id": 1 }}
{ "title": "Exploring the Sahara Desert", "content": "Sand dunes and vast landscapes." }
{ "index": { "_id": 2 }}
{ "title": "Amazon Rainforest Tour", "content": "Dense jungle and exotic wildlife." }
{ "index": { "_id": 3 }}
{ "title": "Mountain Adventures", "content": "Snowy peaks and hiking trails." }
```
{% include copy-curl.html %}

使用下列請求進行查詢：

```json
GET /articles-basic/_search
{
  "query": {
    "more_like_this": {
      "fields": ["content"],
      "like": "jungle wildlife",
      "min_term_freq": 1,
      "min_doc_freq": 1
    }
  }
}
```
{% include copy-curl.html %}

`more_like_this` 查詢會在 `content` 欄位中搜尋詞彙 `jungle` 和 `wildlife`，結果只符合一份文件：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.9616582,
    "hits": [
      {
        "_index": "articles-basic",
        "_id": "2",
        "_score": 1.9616582,
        "_source": {
          "title": "Amazon Rainforest Tour",
          "content": "Dense jungle and exotic wildlife."
        }
      }
    ]
  }
}
```

## 範例：詞彙向量最佳化

使用下列對應建立名為 `articles-optimized` 的索引：

```json
PUT /articles-optimized
{
  "mappings": {
    "properties": {
      "name": {
        "type": "text",
        "term_vector": "with_positions_offsets"
      },
      "alias": {
        "type": "text",
        "term_vector": "with_positions_offsets"
      },
      "quote": {
        "type": "text",
        "term_vector": "with_positions_offsets"
      }
    }
  }
}
```
{% include copy-curl.html %}

將範例文件插入已最佳化的索引：

```json
POST /articles-optimized/_bulk
{ "index": { "_id": "a1" } }
{ "name": "Diana", "alias": "Wonder Woman", "quote": "Justice will come when it is deserved." }
{ "index": { "_id": "a2" } }
{ "name": "Clark", "alias": "Superman", "quote": "Even in the darkest times, hope cuts through." }
{ "index": { "_id": "a3" } }
{ "name": "Bruce", "alias": "Batman", "quote": "I am vengeance. I am the night. I am Batman!" }
```
{% include copy-curl.html %}

尋找 `quote` 欄位中包含與 "dark" 和 "night" 相似詞彙的文件：

```json
GET /articles-optimized/_search
{
  "query": {
    "more_like_this": {
      "fields": ["quote"],
      "like": "dark night",
      "min_term_freq": 1,
      "min_doc_freq": 1
    }
  }
}
```
{% include copy-curl.html %}

`more_like_this` 查詢會搜尋詞彙 `dark` 和 `night`，並傳回下列命中結果：

```json
{
  ...
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.2363393,
    "hits": [
      {
        "_index": "articles-optimized",
        "_id": "a3",
        "_score": 1.2363393,
        "_source": {
          "name": "Bruce",
          "alias": "Batman",
          "quote": "I am vengeance. I am the night. I am Batman!"
        }
      }
    ]
  }
}
```

## 範例：使用多份文件與文字輸入

`more_like_this` 查詢允許您在 `like` 參數中提供多個來源。您可以將自由文字與索引中的文件結合。當您希望搜尋結合多個範例的相關性訊號時，這非常有用。

在下列範例中，直接提供了一份自訂文件。此外，也包含了 `heroes` 索引中 ID 為 `5` 的現有文件：

```json
GET /articles-optimized/_search
{
  "query": {
    "more_like_this": {
      "fields": ["name", "alias"],
      "like": [
        {
          "doc": {
            "name": "Diana",
            "alias": "Wonder Woman",
            "quote": "Courage is not the absence of fear, but the triumph over it."
          }
        },
        {
          "_index": "heroes",
          "_id": "5"
        }
      ],
      "min_term_freq": 1,
      "min_doc_freq": 1,
      "max_query_terms": 25
    }
  }
}
```
{% include copy-curl.html %}

傳回的結果包含與查詢中提供的 `name` 和 `alias` 欄位最相似的文章：

```json
{
  ...
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 2.140194,
    "hits": [
      {
        "_index": "articles-optimized",
        "_id": "a1",
        "_score": 2.140194,
        "_source": {
          "name": "Diana",
          "alias": "Wonder Woman",
          "quote": "Justice will come when it is deserved."
        }
      },
      {
        "_index": "articles-optimized",
        "_id": "a2",
        "_score": 1.1596459,
        "_source": {
          "name": "Clark",
          "alias": "Superman",
          "quote": "Even in the darkest times, hope cuts through."
        }
      }
    ]
  }
}
```

當您想根據尚未完全編製索引的新概念來提升結果，同時又想將其與現有已編製索引文件的知識結合時，可以使用此模式。
{: .note}

# 參數

`more_like_this` 查詢唯一必要的參數是 `like`。其餘參數都有預設值，但允許進行微調。以下是主要的參數類別。

## 文件輸入參數

下表列出文件輸入參數。

| 參數 | 必要／選用 | 資料類型 | 說明 |
| :--- |  :--- |  :--- |  :--- | 
| `like`| 必要| 字串或物件陣列 | 定義要為其尋找相似文件的文字或文件。您可以輸入自由文字、索引中的實際文件，或人工建立的文件。除非另行覆寫，否則文字會由與該欄位關聯的分析器處理。 |
| `unlike`| 選用| 字串或物件陣列 | 提供其詞彙應*排除*在影響查詢之外的文字或文件。適合用於指定負面範例。|
| `fields`| 選用| 字串陣列| 列出分析文字時要使用的欄位。如果未指定，則使用所有欄位。 |

## 詞彙選取參數

| 參數 | 必要／選用 | 資料類型| 說明|
| :--- |  :--- |  :--- |  :--- | 
| `max_query_terms` | 選用| 整數| 設定從輸入中選取的詞彙數量上限。較高的值會提高精確度，但會降低執行速度。預設為 `25`。 |
| `min_term_freq` | 選用| 整數| 在輸入中出現次數少於此值的詞彙將被忽略。預設為 `2`。|
| `min_doc_freq`| 選用| 整數| 出現的文件數少於此值的詞彙將被忽略。預設為 `5`。|
| `max_doc_freq`| 選用| 整數| 出現的文件數超過此上限的詞彙將被忽略。有助於避免非常常見的字詞。預設為無上限 (2<sup>31</sup> - 1)。 |
| `min_word_length` | 選用| 整數| 忽略長度短於此值的字詞。預設為 `0`。|
| `max_word_length` | 選用| 整數| 忽略長度長於此值的字詞。預設為無上限。 |
| `stop_words`| 選用| 字串陣列 | 定義在選取詞彙時完全忽略的字詞清單。|
| `analyzer`| 選用| 字串 | 用於處理輸入文字的自訂分析器。預設為 `fields` 中所列第一個欄位的分析器。|

## 查詢建構參數

| 參數 | 必要／選用 | 資料類型 | 說明 |
| :--- |  :--- |  :--- |  :--- |
| `minimum_should_match`| 選用 | 字串 | 指定最終查詢中必須符合的詞彙數量下限。此值可以是百分比或固定數字。有助於微調召回率與精確度之間的平衡。預設為 `30%` |
| `fail_on_unsupported_field` | 選用 | 布林值 | 決定當任一目標欄位不是相容類型（`text` 或 `keyword`）時，是否擲回錯誤。設為 `false` 可靜默略過不支援的欄位。預設為 `true`。 |
| `boost_terms` | 選用 | 浮點數 | 根據詞彙的詞頻–反文件頻率 (TF–IDF) 權重，對選取的詞彙套用加權。任何大於 `0` 的值都會啟用使用指定因子的詞彙加權。預設為 `0`。 |
| `include` | 選用 | 布林值 | 若為 `true`，`like` 中提供的來源文件會包含在結果的命中項目中。預設為 `false`。 |
| `boost` | 選用 | 浮點數 | 將整個 `more_like_this` 查詢的相關性分數乘以指定值。預設為 `1.0`。 |
