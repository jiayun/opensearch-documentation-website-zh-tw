---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Analyze API
nav_order: 5
redirect_from:
  - /api-reference/analyze-apis/perform-text-analysis/
  - /opensearch/rest-api/analyze-apis/
  - /api-reference/analyze-apis/terminology/
  - /api-reference/analyze-apis/index/
---

# Analyze API
**1.0 版推出**
{: .label .label-purple }

Analyze API 可讓您執行[文字分析]({{site.url}}{{site.baseurl}}/analyzers/)，也就是將非結構化文字轉換為針對搜尋最佳化的個別詞元（通常是單字）的過程。如需字元篩選器、斷詞器、詞元篩選器及正規化器等常見分析元件的詳細資訊，請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/#analyzers)。

Analyze API 會分析文字字串，並傳回產生的詞元。

## 端點

```json
GET /_analyze
GET /{index}/_analyze
POST /_analyze
POST /{index}/_analyze
```

## 路徑參數

您可以在請求中包含下列選用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`index` | 字串 | 用於取得分析器的索引。

## 查詢參數

您可以在請求中包含下列選用查詢參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`index` | 字串 | 用於衍生分析器的索引。請使用此參數作為 `index` 路徑參數的替代方案。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`text` | 字串或字串陣列 | 要分析的文字。如果您提供字串陣列，文字會以多值欄位的方式進行分析。必要。
`analyzer` | 字串 | 要套用至 `text` 欄位的分析器名稱。分析器可以在索引中建立或設定。<br /><br />如果未指定 `analyzer`，Analyze API 會使用 `field` 欄位對應中定義的分析器。<br /><br />如果未指定 `field` 欄位，Analyze API 會使用索引的預設分析器。<br /><br /> 如果未指定索引，或索引沒有預設分析器，Analyze API 會使用[標準分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/standard/)。選用。請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/index/)。
`attributes` | 字串陣列 | 要包含在 `detail` 輸出中的詞元屬性陣列。僅在 `explain` 為 `true` 時適用。
`char_filter` | 字串或物件陣列 | 在 `tokenizer` 欄位之前用於預先處理字元的字元篩選器陣列。每個陣列元素可以是字元篩選器的名稱，或是內嵌的字元篩選器定義。選用。請參閱[字元篩選器]({{site.url}}{{site.baseurl}}/analyzers/character-filters/index/)。
`explain` | 布林值 | 若為 `true`，回應會包含詞元屬性及其他詳細資訊。選用。預設為 `false`。
`field` | 字串 | 用於推導分析器的欄位。<br /><br /> 如果您指定 `field`，則也必須在 `index` 路徑參數或查詢參數中指定索引。<br /><br /> 如果您指定 `analyzer` 欄位，它會覆寫 `field` 的值。<br /><br /> 如果該欄位沒有對應，Analyze API 會使用索引的預設分析器。選用。
`filter` | 字串或物件陣列 | 在 `tokenizer` 欄位之後套用的詞元篩選器陣列。每個陣列元素可以是詞元篩選器的名稱，或是內嵌的詞元篩選器定義。選用。請參閱[詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/index/)。
`normalizer` | 字串 | 用於將文字轉換為單一詞元的正規化器。如果您指定 `normalizer`，則也必須在 `index` 路徑參數或查詢參數中指定索引。選用。請參閱[正規化器]({{site.url}}{{site.baseurl}}/analyzers/normalizers/)。 
`tokenizer` | 字串或物件 | 用於將 `text` 欄位轉換為詞元的斷詞器。請指定斷詞器的名稱或內嵌的斷詞器定義。選用。請參閱[斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/index/)。

`analyzer`、`normalizer` 和 `field` 欄位不能與 `tokenizer`、`filter` 或 `char_filter` 欄位合併使用。`analyzer` 和 `normalizer` 欄位不能彼此合併使用。如果您指定 `filter` 或 `char_filter` 但未指定 `tokenizer`，Analyze API 會從這些篩選器建立自訂正規化器，因此您只能使用正規化器支援的篩選器。

## 請求範例

[分析文字字串陣列](#analyze-array-of-text-strings)

[套用內建分析器](#apply-a-built-in-analyzer)

[套用自訂分析器](#apply-a-custom-analyzer)

[套用自訂暫時性分析器](#apply-a-custom-transient-analyzer)

[指定索引](#specify-an-index)

[從索引欄位衍生分析器](#derive-the-analyzer-from-an-index-field)

[指定正規化器](#specify-a-normalizer)

[取得詞元詳細資料](#get-token-details)

[設定詞元數量上限](#set-a-token-limit)

以下部分範例使用 `books` 和 `books2` 索引。若要執行這些範例，請先使用預設設定建立 `books` 索引：

```json
PUT /books
```
{% include copy-curl.html %}

接著建立 `books2` 索引。此索引定義了名為 `lowercase_ascii_folding` 的自訂分析器，以及名為 `to_lower_fold_ascii` 的自訂正規化器，兩者都會將文字轉換為小寫，並將非 ASCII 字元轉換為 ASCII 字元。此索引也將 `name` 欄位對應為 `text` 欄位：

```json
PUT /books2
{
  "settings": {
    "analysis": {
      "analyzer": {
        "lowercase_ascii_folding": {
          "type": "custom",
          "tokenizer": "standard",
          "filter": ["lowercase", "asciifolding"]
        }
      },
      "normalizer": {
        "to_lower_fold_ascii": {
          "type": "custom",
          "filter": ["lowercase", "asciifolding"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "name": {
        "type": "text"
      }
    }
  }
}
```
{% include copy-curl.html %}

### 分析文字字串陣列

當您將字串陣列傳入 `text` 欄位時，它會以多值欄位的形式進行分析。

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "analyzer" : "standard",
  "text" : ["first array element", "second array element"]
}
-->
{% capture step1_rest %}
GET /_analyze
{
  "analyzer": "standard",
  "text": [
    "first array element",
    "second array element"
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  body =   {
    "analyzer": "standard",
    "text": [
      "first array element",
      "second array element"
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "first",
      "start_offset" : 0,
      "end_offset" : 5,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "array",
      "start_offset" : 6,
      "end_offset" : 11,
      "type" : "<ALPHANUM>",
      "position" : 1
    },
    {
      "token" : "element",
      "start_offset" : 12,
      "end_offset" : 19,
      "type" : "<ALPHANUM>",
      "position" : 2
    },
    {
      "token" : "second",
      "start_offset" : 20,
      "end_offset" : 26,
      "type" : "<ALPHANUM>",
      "position" : 3
    },
    {
      "token" : "array",
      "start_offset" : 27,
      "end_offset" : 32,
      "type" : "<ALPHANUM>",
      "position" : 4
    },
    {
      "token" : "element",
      "start_offset" : 33,
      "end_offset" : 40,
      "type" : "<ALPHANUM>",
      "position" : 5
    }
  ]
}
````

### 套用內建分析器

您可以將任何內建分析器套用至文字字串，而無需指定索引。

下列請求使用 `standard` 內建分析器分析文字：

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "analyzer" : "standard",
  "text" : "OpenSearch text analysis"
}
-->
{% capture step1_rest %}
GET /_analyze
{
  "analyzer": "standard",
  "text": "OpenSearch text analysis"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  body =   {
    "analyzer": "standard",
    "text": "OpenSearch text analysis"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "opensearch",
      "start_offset" : 0,
      "end_offset" : 10,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "text",
      "start_offset" : 11,
      "end_offset" : 15,
      "type" : "<ALPHANUM>",
      "position" : 1
    },
    {
      "token" : "analysis",
      "start_offset" : 16,
      "end_offset" : 24,
      "type" : "<ALPHANUM>",
      "position" : 2
    }
  ]
}
````

### 套用自訂分析器

您可以建立自己的分析器，並在分析請求中指定該分析器。

`books2` 索引定義了自訂的 `lowercase_ascii_folding` 分析器，此分析器會將文字轉換為小寫，並將非 ASCII 字元轉換為 ASCII。

下列請求會將自訂分析器套用至提供的文字：

<!-- spec_insert_start
component: example_code
rest: GET /books2/_analyze
body: |
{
  "analyzer": "lowercase_ascii_folding",
  "text" : "Le garçon m'a SUIVI."
}
-->
{% capture step1_rest %}
GET /books2/_analyze
{
  "analyzer": "lowercase_ascii_folding",
  "text": "Le garçon m'a SUIVI."
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  index = "books2",
  body =   {
    "analyzer": "lowercase_ascii_folding",
    "text": "Le garçon m'a SUIVI."
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "le",
      "start_offset" : 0,
      "end_offset" : 2,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "garcon",
      "start_offset" : 3,
      "end_offset" : 9,
      "type" : "<ALPHANUM>",
      "position" : 1
    },
    {
      "token" : "m'a",
      "start_offset" : 10,
      "end_offset" : 13,
      "type" : "<ALPHANUM>",
      "position" : 2
    },
    {
      "token" : "suivi",
      "start_offset" : 14,
      "end_offset" : 19,
      "type" : "<ALPHANUM>",
      "position" : 3
    }
  ]
}
````

### 套用自訂暫時性分析器

您可以使用斷詞器、詞元篩選器或字元篩選器建立自訂暫時性分析器。使用 `filter` 參數指定詞元篩選器，並使用 `char_filter` 參數指定字元篩選器。

下列請求使用 `uppercase` 詞元篩選器將文字轉換為大寫：

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "tokenizer" : "keyword",
  "filter" : ["uppercase"],
  "text" : "OpenSearch filter"
}
-->
{% capture step1_rest %}
GET /_analyze
{
  "tokenizer": "keyword",
  "filter": [
    "uppercase"
  ],
  "text": "OpenSearch filter"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  body =   {
    "tokenizer": "keyword",
    "filter": [
      "uppercase"
    ],
    "text": "OpenSearch filter"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "OPENSEARCH FILTER",
      "start_offset" : 0,
      "end_offset" : 17,
      "type" : "word",
      "position" : 0
    }
  ]
}
````
<hr />

下列請求使用 `html_strip` 字元篩選器移除文字中的 HTML 標籤：

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "tokenizer" : "keyword",
  "filter" : ["lowercase"],
  "char_filter" : ["html_strip"],
  "text" : "<b>Leave</b> right now!"
}
-->
{% capture step1_rest %}
GET /_analyze
{
  "tokenizer": "keyword",
  "filter": [
    "lowercase"
  ],
  "char_filter": [
    "html_strip"
  ],
  "text": "<b>Leave</b> right now!"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  body =   {
    "tokenizer": "keyword",
    "filter": [
      "lowercase"
    ],
    "char_filter": [
      "html_strip"
    ],
    "text": "<b>Leave</b> right now!"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "leave right now!",
      "start_offset" : 3,
      "end_offset" : 23,
      "type" : "word",
      "position" : 0
    }
  ]
}
````

<hr />

您可以使用陣列組合多個篩選器。

下列請求將 `lowercase` 轉換與 `stop` 篩選器組合使用，後者會移除 `stopwords` 陣列中的字詞：

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "tokenizer" : "whitespace",
  "filter" : ["lowercase", {"type": "stop", "stopwords": [ "to", "in"]}],
  "text" : "how to train your dog in five steps"
}
-->
{% capture step1_rest %}
GET /_analyze
{
  "tokenizer": "whitespace",
  "filter": [
    "lowercase",
    {
      "type": "stop",
      "stopwords": [
        "to",
        "in"
      ]
    }
  ],
  "text": "how to train your dog in five steps"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  body =   {
    "tokenizer": "whitespace",
    "filter": [
      "lowercase",
      {
        "type": "stop",
        "stopwords": [
          "to",
          "in"
        ]
      }
    ],
    "text": "how to train your dog in five steps"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "how",
      "start_offset" : 0,
      "end_offset" : 3,
      "type" : "word",
      "position" : 0
    },
    {
      "token" : "train",
      "start_offset" : 7,
      "end_offset" : 12,
      "type" : "word",
      "position" : 2
    },
    {
      "token" : "your",
      "start_offset" : 13,
      "end_offset" : 17,
      "type" : "word",
      "position" : 3
    },
    {
      "token" : "dog",
      "start_offset" : 18,
      "end_offset" : 21,
      "type" : "word",
      "position" : 4
    },
    {
      "token" : "five",
      "start_offset" : 25,
      "end_offset" : 29,
      "type" : "word",
      "position" : 6
    },
    {
      "token" : "steps",
      "start_offset" : 30,
      "end_offset" : 35,
      "type" : "word",
      "position" : 7
    }
  ]
}
````

### 指定索引

您可以使用索引的預設分析器來分析文字，也可以指定不同的分析器。

下列請求使用與 `books` 索引相關聯的預設分析器來分析所提供的文字：

<!-- spec_insert_start
component: example_code
rest: GET /books/_analyze
body: |
{
  "text" : "OpenSearch analyze test"
}
-->
{% capture step1_rest %}
GET /books/_analyze
{
  "text": "OpenSearch analyze test"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  index = "books",
  body =   {
    "text": "OpenSearch analyze test"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "opensearch",
      "start_offset" : 0,
      "end_offset" : 10,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "analyze",
      "start_offset" : 11,
      "end_offset" : 18,
      "type" : "<ALPHANUM>",
      "position" : 1
    },
    {
      "token" : "test",
      "start_offset" : 19,
      "end_offset" : 23,
      "type" : "<ALPHANUM>",
      "position" : 2
    }
  ]
}
````

<hr />

下列請求使用 `keyword` 分析器來分析所提供的文字，此分析器會將整個文字值作為單一詞元傳回：

<!-- spec_insert_start
component: example_code
rest: GET /books/_analyze
body: |
{
  "analyzer" : "keyword",
  "text" : "OpenSearch analyze test"
}
-->
{% capture step1_rest %}
GET /books/_analyze
{
  "analyzer": "keyword",
  "text": "OpenSearch analyze test"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  index = "books",
  body =   {
    "analyzer": "keyword",
    "text": "OpenSearch analyze test"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "OpenSearch analyze test",
      "start_offset" : 0,
      "end_offset" : 23,
      "type" : "word",
      "position" : 0
    }
  ]
}
````

### 從索引欄位推導分析器

您可以傳入文字以及索引中的欄位。API 會查詢該欄位的分析器，並使用它來分析文字。

如果該欄位未建立對應，API 會使用索引的預設分析器。

下列請求會根據 `name` 的對應進行分析：

<!-- spec_insert_start
component: example_code
rest: GET /books2/_analyze
body: |
{
  "field" : "name",
  "text" : "OpenSearch analyze test"
}
-->
{% capture step1_rest %}
GET /books2/_analyze
{
  "field": "name",
  "text": "OpenSearch analyze test"
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  index = "books2",
  body =   {
    "field": "name",
    "text": "OpenSearch analyze test"
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "opensearch",
      "start_offset" : 0,
      "end_offset" : 10,
      "type" : "<ALPHANUM>",
      "position" : 0
    },
    {
      "token" : "analyze",
      "start_offset" : 11,
      "end_offset" : 18,
      "type" : "<ALPHANUM>",
      "position" : 1
    },
    {
      "token" : "test",
      "start_offset" : 19,
      "end_offset" : 23,
      "type" : "<ALPHANUM>",
      "position" : 2
    }
  ]
}
````

### 指定正規化器

您可以使用索引中定義的正規化器 (normalizer) 來分析文字。正規化器會從文字產生單一詞元。

`books2` 索引定義了自訂的 `to_lower_fold_ascii` 正規化器，此正規化器會將文字轉換為小寫，並將非 ASCII 字元轉換為 ASCII。

下列請求會將 `to_lower_fold_ascii` 套用至文字：

<!-- spec_insert_start
component: example_code
rest: GET /books2/_analyze
body: |
{
  "normalizer" : "to_lower_fold_ascii",
  "text" : "C'est le garçon qui m'a suivi."
}
-->
{% capture step1_rest %}
GET /books2/_analyze
{
  "normalizer": "to_lower_fold_ascii",
  "text": "C'est le garçon qui m'a suivi."
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  index = "books2",
  body =   {
    "normalizer": "to_lower_fold_ascii",
    "text": "C'est le garçon qui m'a suivi."
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "c'est le garcon qui m'a suivi.",
      "start_offset" : 0,
      "end_offset" : 30,
      "type" : "word",
      "position" : 0
    }
  ]
}
````

<hr />

您可以在不指定斷詞器的情況下，指定詞元篩選器或字元篩選器，以建立自訂的暫時性正規化器。只能使用正規化器支援的篩選器。

下列請求使用 `uppercase` 詞元篩選器，將指定的文字全部轉換為大寫：

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "filter" : ["uppercase"],
  "text" : "That is the boy who followed me."
}
-->
{% capture step1_rest %}
GET /_analyze
{
  "filter": [
    "uppercase"
  ],
  "text": "That is the boy who followed me."
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  body =   {
    "filter": [
      "uppercase"
    ],
    "text": "That is the boy who followed me."
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "tokens" : [
    {
      "token" : "THAT IS THE BOY WHO FOLLOWED ME.",
      "start_offset" : 0,
      "end_offset" : 32,
      "type" : "word",
      "position" : 0
    }
  ]
}
````

### 取得詞元詳細資訊

您可以將 `explain` 欄位設定為 `true`，以取得所有詞元的額外詳細資訊。若要限制輸出中的詞元屬性，請在 `attributes` 陣列中指定這些屬性。

下列請求會提供搭配 `standard` 斷詞器使用的 `reverse` 篩選器的詳細詞元資訊，且僅包含 `bytes` 屬性：

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "tokenizer" : "standard",
  "filter" : ["reverse"],
  "text" : "OpenSearch analyze test",
  "explain" : true,
  "attributes" : ["bytes"]
}
-->
{% capture step1_rest %}
GET /_analyze
{
  "tokenizer": "standard",
  "filter": [
    "reverse"
  ],
  "text": "OpenSearch analyze test",
  "explain": true,
  "attributes": [
    "bytes"
  ]
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.analyze(
  body =   {
    "tokenizer": "standard",
    "filter": [
      "reverse"
    ],
    "text": "OpenSearch analyze test",
    "explain": true,
    "attributes": [
      "bytes"
    ]
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

上述請求會傳回下列欄位：

````json
{
  "detail" : {
    "custom_analyzer" : true,
    "charfilters" : [ ],
    "tokenizer" : {
      "name" : "standard",
      "tokens" : [
        {
          "token" : "OpenSearch",
          "start_offset" : 0,
          "end_offset" : 10,
          "type" : "<ALPHANUM>",
          "position" : 0,
          "bytes" : "[4f 70 65 6e 53 65 61 72 63 68]"
        },
        {
          "token" : "analyze",
          "start_offset" : 11,
          "end_offset" : 18,
          "type" : "<ALPHANUM>",
          "position" : 1,
          "bytes" : "[61 6e 61 6c 79 7a 65]"
        },
        {
          "token" : "test",
          "start_offset" : 19,
          "end_offset" : 23,
          "type" : "<ALPHANUM>",
          "position" : 2,
          "bytes" : "[74 65 73 74]"
        }
      ]
    },
    "tokenfilters" : [
      {
        "name" : "reverse",
        "tokens" : [
          {
            "token" : "hcraeSnepO",
            "start_offset" : 0,
            "end_offset" : 10,
            "type" : "<ALPHANUM>",
            "position" : 0,
            "bytes" : "[68 63 72 61 65 53 6e 65 70 4f]"
          },
          {
            "token" : "ezylana",
            "start_offset" : 11,
            "end_offset" : 18,
            "type" : "<ALPHANUM>",
            "position" : 1,
            "bytes" : "[65 7a 79 6c 61 6e 61]"
          },
          {
            "token" : "tset",
            "start_offset" : 19,
            "end_offset" : 23,
            "type" : "<ALPHANUM>",
            "position" : 2,
            "bytes" : "[74 73 65 74]"
          }
        ]
      }
    ]
  }
}
````

### 設定詞元數量上限

使用 `index.analyze.max_token_count` 設定來限制分析請求可為索引產生的詞元數量。預設值為 `10000`。未指定索引的請求會受限於預設值。

下列請求將 `books2` 索引產生的詞元數量限制為四個：

```json
PUT /books2/_settings
{
  "index.analyze.max_token_count": 4
}
```
{% include copy-curl.html %}

下列請求會產生五個詞元，超過上限，因此 OpenSearch 會拒絕該請求：

```json
GET /books2/_analyze
{
  "text": "how to train your dog"
}
```
{% include copy-curl.html %}

如需動態索引設定的詳細資訊，請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。

## 回應本文欄位

文字分析端點會傳回下列回應欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`tokens` | 陣列 | 從 `text` 衍生的詞元陣列。當 `explain` 為 `false` 時傳回。請參閱 [詞元物件](#token-object)。
`detail` | 物件 | 關於分析及每個詞元的詳細資訊。當 `explain` 為 `true` 時，會傳回此欄位而非 `tokens`。請參閱 [詳細資訊物件](#detail-object)。

#### 詞元物件

欄位 | 資料類型 | 說明
:--- | :--- | :---
`token`  | 字串 | 詞元的文字。
`start_offset` | 整數 | 詞元在原始文字字串中的起始位置。位移從零開始計算。
`end_offset` | 整數 | 詞元在原始文字字串中的結束位置。結束位移不包含在範圍內。
`type` | 字串 | 詞元的分類：`<ALPHANUM>`、`<NUM>` 等。類型通常由斷詞器設定，但部分篩選器會定義自己的類型。例如，同義詞篩選器會定義 `SYNONYM` 類型。
`position` | 整數 | 詞元在詞元串流中的位置。位置值可能會跳號，例如篩選器移除詞元時。
`bytes` | 字串 | 以十六進位表示的詞元位元組。僅在 `explain` 為 `true` 時傳回。
`positionLength` | 整數 | 詞元所跨越的位置數。僅在 `explain` 為 `true` 時傳回。
`termFrequency` | 整數 | 詞元的詞彙頻率。僅在 `explain` 為 `true` 時傳回。

#### 詳細資料物件

欄位 | 資料類型 | 說明
:--- | :--- | :---
`custom_analyzer` | 布林值 | 套用至文字的分析器是自訂分析器還是內建分析器。
`analyzer` | 物件 | 套用至文字的分析器名稱，以及該分析器產生的詞元<sup>*</sup>清單。當 `custom_analyzer` 為 `false` 時傳回，也就是使用內建分析器（包括索引預設分析器）分析文字時傳回。
`charfilters` | 陣列 | 套用至文字的字元篩選器清單。當 `custom_analyzer` 為 `true` 時傳回。
`tokenizer` | 物件 | 套用至文字的斷詞器名稱，以及套用詞元篩選器之前內容的詞元<sup>*</sup>清單。當 `custom_analyzer` 為 `true` 時傳回。
`tokenfilters` | 陣列 | 套用至文字的詞元篩選器清單。每個詞元篩選器都包含篩選器名稱，以及套用篩選器之後內容的詞元<sup>*</sup>清單。詞元篩選器會依照請求中指定的順序列出。當 `custom_analyzer` 為 `true` 時傳回。

如需詞元欄位的說明，請參閱[詞元物件](#token-object)。
{: .note}

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`indices:admin/analyze`。

## 相關文件

- [文字分析]({{site.url}}{{site.baseurl}}/analyzers/)
- [分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/index/)
- [斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/index/)
- [詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/index/)
- [正規化器]({{site.url}}{{site.baseurl}}/analyzers/normalizers/)
