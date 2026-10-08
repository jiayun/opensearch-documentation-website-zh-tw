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
**於 1.0 版推出**
{: .label .label-purple }

Analyze API 可讓您執行[文字分析]({{site.url}}{{site.baseurl}}/analyzers/)，這是將非結構化文字轉換為個別詞元（通常是單字），並針對搜尋最佳化的程序。如需字元篩選器、斷詞器、詞元篩選器和正規化器等常見分析元件的詳細資訊，請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/#analyzers)。

Analyze API 會分析文字字串，並傳回產生的詞元。

如果您使用 Security 外掛程式，則必須具有 `manage index` 權限。如果您只想分析文字，則必須具有 `manage cluster` 權限。
{: .note}

## 端點

```json
GET /_analyze
GET /{index}/_analyze
POST /_analyze
POST /{index}/_analyze
```

雖然您可以使用 `GET` 和 `POST` 請求來發出分析請求，但兩者有重要的差異。`GET` 請求會將資料快取在索引中，以便下次請求該資料時能更快擷取。`POST` 請求會將尚不存在的字串傳送至分析器，以便與索引中已有的資料進行比較。`POST` 請求不會被快取。
{: .note}

## 路徑參數

您可以在請求中包含下列選用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`index` | 字串 | 用於取得分析器的索引。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`text` | 字串或字串陣列 | 要分析的文字。如果您提供字串陣列，文字會以多值欄位的形式進行分析。必要。
`analyzer` | 字串 | 要套用至 `text` 欄位的分析器名稱。分析器可在索引中建立或設定。<br /><br />如果未指定 `analyzer`，Analyze API 會使用 `field` 欄位對應中定義的分析器。<br /><br />如果未指定 `field` 欄位，Analyze API 會使用索引的預設分析器。<br /><br > 如果未指定索引，或索引沒有預設分析器，Analyze API 會使用[標準分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/standard/)。選用。請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/index/)。
`attributes` | 字串陣列 | 用於篩選 `explain` 欄位輸出的詞元屬性陣列。
`char_filter` | 字串陣列 | 在 `tokenizer` 欄位處理之前，用於預先處理字元的字元篩選器陣列。選用。請參閱[字元篩選器]({{site.url}}{{site.baseurl}}/analyzers/character-filters/index/)。
`explain` | 布林值 | 如果為 `true`，回應會包含詞元屬性和其他詳細資訊。選用。預設為 `false`。
`field` | 字串 | 用於取得分析器的欄位。<br /><br > 如果您指定 `field`，也必須指定 `index` 路徑參數。<br /><br > 如果您指定 `analyzer` 欄位，它會覆寫 `field` 的值。<br /><br > 如果您未指定 `field`，Analyze API 會使用索引的預設分析器。<br /><br > 如果您未指定 `index` 欄位，或索引沒有預設分析器，Analyze API 會使用標準分析器。選用。
`filter` | 字串陣列 | 在 `tokenizer` 欄位處理之後套用的詞元篩選器陣列。選用。請參閱[詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/index/)。
`normalizer` | 字串 | 用於將文字轉換為單一詞元的正規化器。選用。請參閱[正規化器]({{site.url}}{{site.baseurl}}/analyzers/normalizers/)。 
`tokenizer` | 字串 | 用於將 `text` 欄位轉換為詞元的斷詞器。選用。請參閱[斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/index/)。

## 請求範例

[分析文字字串陣列](#analyze-array-of-text-strings)

[套用內建分析器](#apply-a-built-in-analyzer)

[套用自訂分析器](#apply-a-custom-analyzer)

[套用自訂暫時分析器](#apply-a-custom-transient-analyzer)

[指定索引](#specify-an-index)

[從索引欄位取得分析器](#derive-the-analyzer-from-an-index-field)

[指定正規化器](#specify-a-normalizer)

[取得詞元詳細資訊](#get-token-details)

[設定詞元數量上限](#set-a-token-limit)

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

如果您省略 `index` 路徑參數，便可以將任何內建分析器套用至文字字串。

下列請求使用 `standard` 內建分析器來分析文字：

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

在此情境中，已建立自訂分析器 `lowercase_ascii_folding`，並將其與 `books2` 索引建立關聯。此分析器會將文字轉換為小寫，並將非 ASCII 字元轉換為 ASCII。

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

您可以使用斷詞器、詞元篩選器或字元篩選器建置自訂暫時性分析器。請使用 `filter` 參數指定詞元篩選器。

下列請求使用 `uppercase` 字元篩選器將文字轉換為大寫：

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

下列請求使用 `html_strip` 篩選器移除文字中的 HTML 字元：

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

```` json
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

您可以使用索引的預設分析器來分析文字，也可以指定其他分析器。

下列請求使用與 `books` 索引相關聯的預設分析器分析提供的文字：

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

下列請求使用 `keyword` 分析器分析提供的文字，此分析器會將整個文字值當作單一詞元傳回：

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

### 從索引欄位取得分析器

您可以傳入文字和索引中的欄位。API 會查找該欄位的分析器，並使用它來分析文字。

如果對應不存在，API 會使用標準分析器，將所有文字轉換為小寫，並根據空白字元進行斷詞。

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

您可以使用與索引關聯的正規化器，取代使用關鍵字欄位。正規化器會讓分析轉換產生單一詞元。

在此範例中，`books2` 索引包含名為 `to_lower_fold_ascii` 的正規化器，會將文字轉換為小寫，並將非 ASCII 文字轉換為 ASCII。

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

您可以使用詞元篩選器和字元篩選器建立自訂的暫時性正規化器。

下列請求使用 `uppercase` 字元篩選器，將指定的文字全部轉換為大寫：

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

您可以將 `explain` 屬性設為 `true`，以取得所有詞元的額外詳細資訊。

下列請求提供與 `standard` 斷詞器搭配使用的 `reverse` 篩選器的詳細詞元資訊：

<!-- spec_insert_start
component: example_code
rest: GET /_analyze
body: |
{
  "tokenizer" : "standard",
  "filter" : ["reverse"],
  "text" : "OpenSearch analyze test",
  "explain" : true,
  "attributes" : ["keyword"]
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
    "keyword"
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
      "keyword"
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
            "position" : 0
          },
          {
            "token" : "ezylana",
            "start_offset" : 11,
            "end_offset" : 18,
            "type" : "<ALPHANUM>",
            "position" : 1
          },
          {
            "token" : "tset",
            "start_offset" : 19,
            "end_offset" : 23,
            "type" : "<ALPHANUM>",
            "position" : 2
          }
        ]
      }
    ]
  }
}
````

### 設定詞元數量上限

您可以設定產生的詞元數量上限。設定較低的值可減少節點的記憶體用量。預設值為 10000。

下列請求將詞元數量限制為四個：

````json
PUT /books2
{
  "settings" : {
    "index.analyze.max_token_count" : 4
  }
}
````
{% include copy-curl.html %}

上述請求使用的是索引 API，而非 Analyze API。請參閱[動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)，以瞭解更多詳細資訊。
{: .note}

## 回應本文欄位

文字分析端點會傳回下列回應欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`tokens` | 陣列 | 從 `text` 取得的詞元陣列。請參閱[詞元物件](#token-object)。
`detail` | 物件 | 分析及各個詞元的詳細資訊。僅在您請求詞元詳細資訊時包含。請參閱[詳細資訊物件](#detail-object)。

#### 詞元物件

欄位 | 資料類型 | 說明
:--- | :--- | :---
`token`  | 字串 | 詞元的文字。
`start_offset` | 整數 | 詞元在原始文字字串中的起始位置。位移量從零開始計算。
`end_offset` | 整數 | 詞元在原始文字字串中的結束位置。
type | 字串 | 詞元的分類：`<ALPHANUM>`、`<NUM>` 等。類型通常由斷詞器設定，但有些篩選器會定義自己的類型。例如，同義詞篩選器會定義 `<SYNONYM>` 類型。
`position` |  整數 | 詞元在 `tokens` 陣列中的位置。

#### 詳細資訊物件

欄位 | 資料類型 | 說明
:--- | :--- | :---
`custom_analyzer` | 布林值 | 套用至文字的分析器是自訂分析器還是內建分析器。
`charfilters` | 陣列 | 套用至文字的字元篩選器清單。
`tokenizer` | 物件 | 套用至文字的斷詞器名稱，以及套用詞元篩選器之前的詞元<sup>*</sup>清單。
`tokenfilters` | 陣列 | 套用至文字的詞元篩選器清單。每個詞元篩選器都包含篩選器名稱，以及套用篩選器之後的詞元<sup>*</sup>清單。詞元篩選器依照請求中指定的順序列出。 

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
