---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋範本"
parent: Search APIs
has_children: true
nav_order: 90
redirect_from:
  - /opensearch/search-template/
  - /search-plugins/search-template/
  - /api-reference/search-template/
  - /api-reference/search-apis/search-template/
---

# 搜尋範本 API

您可以將全文查詢轉換為搜尋範本，以接受使用者輸入並將其動態插入查詢中。

例如，如果您使用 OpenSearch 作為應用程式或網站的後端搜尋引擎，您可以從搜尋列或表單欄位接收使用者查詢，並將其作為參數傳入搜尋範本。如此一來，建立 OpenSearch 查詢的語法便對終端使用者抽象化。

當您撰寫程式碼將使用者輸入轉換為 OpenSearch 查詢時，可以使用搜尋範本簡化程式碼。如果您需要在搜尋查詢中新增欄位，可以修改範本而無需變更程式碼。

搜尋範本使用 Mustache 語言。如需所有語法選項的清單，請參閱 [Mustache 手冊](https://mustache.github.io/mustache.5.html)。
{: .note }

## 查詢參數

`_search/template` 端點接受與 Search API 相同的查詢參數，包括 `typed_keys` 和 `rest_total_hits_as_int`。如需更多資訊，請參閱 [Search API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search/)。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`id` | 字串 | 要執行的已儲存搜尋範本 ID。若未指定 `source`，則為必要。
`source` | 物件或字串 | 內嵌搜尋範本。若範本包含會使 JSON 無效的 Mustache 標籤，請將範本指定為字串。若未指定 `id`，則為必要。
`params` | 物件 | 用來取代範本中變數的值。
`explain` | 布林值 | 是否傳回每個命中結果分數計算方式的詳細資訊。預設為 `false`。
`profile` | 布林值 | 是否傳回查詢執行的時間資訊。預設為 `false`。
`search_pipeline` | 字串 | 要套用至搜尋請求的搜尋管線名稱。

## 建立搜尋範本

搜尋範本包含兩個部分：查詢與參數。參數是使用者輸入的值，會被放入變數中。變數以 Mustache 標記法中的雙大括號表示。當 OpenSearch 在查詢中遇到像 `{% raw %}{{var}}{% endraw %}` 這樣的變數時，會前往 `params` 區段，尋找名為 `var` 的參數，並將其取代為指定的值。

您可以撰寫應用程式，詢問使用者想要搜尋的內容，然後在執行階段將該值填入 `params` 物件。

本頁的範例使用 `shakespeare` 索引。若要試用這些範例，請先建立索引：

```json
PUT /shakespeare
{
  "mappings": {
    "properties": {
      "line_id": { "type": "integer" },
      "play_name": { "type": "keyword" },
      "speech_number": { "type": "integer" },
      "speaker": { "type": "keyword" },
      "text_entry": { "type": "text" }
    }
  }
}
```
{% include copy-curl.html %}

接著將劇作中的幾行台詞新增至索引：

```json
POST /_bulk
{ "index": { "_index": "shakespeare", "_id": "1" } }
{ "line_id": 1, "play_name": "Henry IV", "speech_number": 1, "speaker": "KING HENRY IV", "text_entry": "So shaken as we are, so wan with care," }
{ "index": { "_index": "shakespeare", "_id": "2" } }
{ "line_id": 2, "play_name": "Henry IV", "speech_number": 1, "speaker": "KING HENRY IV", "text_entry": "Find we a time for frighted peace to pant," }
{ "index": { "_index": "shakespeare", "_id": "3" } }
{ "line_id": 3, "play_name": "Henry IV", "speech_number": 1, "speaker": "KING HENRY IV", "text_entry": "And breathe short-winded accents of new broils" }
{ "index": { "_index": "shakespeare", "_id": "4" } }
{ "line_id": 4, "play_name": "Othello", "speech_number": 1, "speaker": "IAGO", "text_entry": "I am not what I am." }
{ "index": { "_index": "shakespeare", "_id": "5" } }
{ "line_id": 5, "play_name": "Hamlet", "speech_number": 1, "speaker": "HAMLET", "text_entry": "To be, or not to be: that is the question:" }
{ "index": { "_index": "shakespeare", "_id": "6" } }
{ "line_id": 6, "play_name": "Romeo and Juliet", "speech_number": 1, "speaker": "ROMEO", "text_entry": "Did my heart love till now? forswear it, sight!" }
{ "index": { "_index": "shakespeare", "_id": "7" } }
{ "line_id": 7, "play_name": "As You Like It", "speech_number": 1, "speaker": "JAQUES", "text_entry": "Then a soldier, full of strange oaths," }
```
{% include copy-curl.html %}

此命令定義了一個依劇名尋找劇作的搜尋範本。查詢中的 `{% raw %}{{play_name}}{% endraw %}` 會被取代為值 `Henry IV`：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search/template
body: |
{
  "source": {
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
-->
{% capture step1_rest %}
GET /shakespeare/_search/template
{
  "source": {
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  index = "shakespeare",
  body =   {
    "source": {
      "query": {
        "match": {
          "play_name": "{% raw %}{{play_name}}{% endraw %}"
        }
      }
    },
    "params": {
      "play_name": "Henry IV"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

此範本會在 `shakespeare` 索引上執行搜尋。若要在叢集中的所有索引上執行搜尋，請在請求中省略索引名稱：

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
body: |
{
  "source": {
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
-->
{% capture step1_rest %}
GET /_search/template
{
  "source": {
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  body =   {
    "source": {
      "query": {
        "match": {
          "play_name": "{% raw %}{{play_name}}{% endraw %}"
        }
      }
    },
    "params": {
      "play_name": "Henry IV"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

指定 `from` 與 `size` 參數：

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
body: |
{
  "source": {
    "from": "{% raw %}{{from}}{% endraw %}",
    "size": "{% raw %}{{size}}{% endraw %}",
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV",
    "from": 10,
    "size": 10
  }
}
-->
{% capture step1_rest %}
GET /_search/template
{
  "source": {
    "from": "{% raw %}{{from}}{% endraw %}",
    "size": "{% raw %}{{size}}{% endraw %}",
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV",
    "from": 10,
    "size": 10
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  body =   {
    "source": {
      "from": "{% raw %}{{from}}{% endraw %}",
      "size": "{% raw %}{{size}}{% endraw %}",
      "query": {
        "match": {
          "play_name": "{% raw %}{{play_name}}{% endraw %}"
        }
      }
    },
    "params": {
      "play_name": "Henry IV",
      "from": 10,
      "size": 10
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

為了改善搜尋體驗，您可以定義預設值，讓使用者不必指定每個可能的參數。如果參數未在 `params` 區段中定義，OpenSearch 會使用預設值。

為變數 `var` 定義預設值的語法如下：

```
{% raw %}{{var}}{{^var}}default value{{/var}}{% endraw %}
```
{% include copy.html %}

此命令將 `from` 的預設值設為 10，並將 `size` 的預設值設為 10：

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
body: |
{
  "source": {
    "from": "{% raw %}{{from}}{{^from}}10{{/from}}{% endraw %}",
    "size": "{% raw %}{{size}}{{^size}}10{{/size}}{% endraw %}",
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
-->
{% capture step1_rest %}
GET /_search/template
{
  "source": {
    "from": "{% raw %}{{from}}{{^from}}10{{/from}}{% endraw %}",
    "size": "{% raw %}{{size}}{{^size}}10{{/size}}{% endraw %}",
    "query": {
      "match": {
        "play_name": "{% raw %}{{play_name}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Henry IV"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  body =   {
    "source": {
      "from": "{% raw %}{{from}}{{^from}}10{{/from}}{% endraw %}",
      "size": "{% raw %}{{size}}{{^size}}10{{/size}}{% endraw %}",
      "query": {
        "match": {
          "play_name": "{% raw %}{{play_name}}{% endraw %}"
        }
      }
    },
    "params": {
      "play_name": "Henry IV"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->


## 儲存並執行搜尋範本

當搜尋範本如您預期般運作後，您可以將該範本的來源儲存為指令碼，使其可針對不同的輸入參數重複使用。

將搜尋範本儲存為指令碼時，您需要將 `lang` 參數指定為 `mustache`：

```json
POST _scripts/play_search_template
{
  "script": {
    "lang": "mustache",
    "source": {
      "from": "{% raw %}{{from}}{{^from}}0{{/from}}{% endraw %}",
      "size": "{% raw %}{{size}}{{^size}}10{{/size}}{% endraw %}",
      "query": {
        "match": {
          "play_name": "{% raw %}{{play_name}}{% endraw %}"
        }
      }
    }
  }
}
```

已儲存的指令碼不會保留預設參數值。若您在儲存指令碼時包含 `params` 物件，OpenSearch 會將其捨棄。若要在已儲存的範本中設定預設值，請在範本來源中使用 `{% raw %}{{var}}{{^var}}default value{{/var}}{% endraw %}` 語法，如前述請求中的 `from` 與 `size` 所示。

現在您可以透過參照範本的 `id` 參數來重複使用該範本。您可以針對不同的輸入值重複使用此來源範本：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search/template
body: |
{
  "id": "play_search_template",
  "params": {
    "play_name": "Henry IV",
    "from": 0,
    "size": 1
  }
}
-->
{% capture step1_rest %}
GET /shakespeare/_search/template
{
  "id": "play_search_template",
  "params": {
    "play_name": "Henry IV",
    "from": 0,
    "size": 1
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  index = "shakespeare",
  body =   {
    "id": "play_search_template",
    "params": {
      "play_name": "Henry IV",
      "from": 0,
      "size": 1
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含第一個相符的文件：

```json
{
  "took": 6,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3,
      "relation": "eq"
    },
    "max_score": 1.0,
    "hits": [
      {
        "_index": "shakespeare",
        "_id": "1",
        "_score": 1.0,
        "_source": {
          "line_id": 1,
          "play_name": "Henry IV",
          "speech_number": 1,
          "speaker": "KING HENRY IV",
          "text_entry": "So shaken as we are, so wan with care,"
        }
      }
    ]
  },
  "status": 200
}
```

若您有已儲存的範本並想加以驗證，請使用 `render` 操作：

<!-- spec_insert_start
component: example_code
rest: POST /_render/template
body: |
{
  "id": "play_search_template",
  "params": {
    "play_name": "Henry IV"
  }
}
-->
{% capture step1_rest %}
POST /_render/template
{
  "id": "play_search_template",
  "params": {
    "play_name": "Henry IV"
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.render_search_template(
  body =   {
    "id": "play_search_template",
    "params": {
      "play_name": "Henry IV"
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

如需更多資訊，請參閱 [Render Template API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/render-template/)。

## 使用搜尋範本進行進階參數轉換

Mustache 提供許多不同的語法選項，可將輸入參數轉換為查詢。
您可以指定條件、執行迴圈、串接陣列、將陣列轉換為 JSON 等。

### 條件

使用 Mustache 中的區段標籤來表示條件：

```json
{% raw %}{{#var}}var{{/var}}{% endraw %}
```
{% include copy.html %}

當 `var` 為布林值時，此語法的作用如同 `if` 條件。只有在 `var` 的評估結果為 `true` 時，`{% raw %}{{#var}}{% endraw %}` 與 `{% raw %}{{/var}}{% endraw %}` 標籤才會插入兩者之間的值。

使用區段標籤會使您的 JSON 無效，因此您必須改以字串格式撰寫查詢。

此命令只會在 `limit` 參數設為 `true` 時，才在查詢中加入 `size` 參數。
在下列範例中，`limit` 參數為 `true`，因此轉譯後的查詢會包含設為 `2` 的 `size`：

<!-- spec_insert_start
component: example_code
rest: POST /_render/template
body: |
{
  "source": "{% raw %}{ {{#limit}} \"size\": \"{{size}}\", {{/limit}}  \"query\":{\"match\":{\"play_name\": \"{{play_name}}\"}}}{% endraw %}",
  "params": {
    "play_name": "Henry IV",
    "limit": true,
    "size": 2
  }
}
-->
{% capture step1_rest %}
POST /_render/template
{
  "source": "{% raw %}{ {{#limit}} \"size\": \"{{size}}\", {{/limit}}  \"query\":{\"match\":{\"play_name\": \"{{play_name}}\"}}}{% endraw %}",
  "params": {
    "play_name": "Henry IV",
    "limit": true,
    "size": 2
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.render_search_template(
  body =   {
    "source": "{% raw %}{ {{#limit}} \"size\": \"{{size}}\", {{/limit}}  \"query\":{\"match\":{\"play_name\": \"{{play_name}}\"}}}{% endraw %}",
    "params": {
      "play_name": "Henry IV",
      "limit": true,
      "size": 2
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

您也可以設計 `if-else` 條件。如果 `limit` 為 `true`，此命令會將 `size` 設為 `2`；否則，會將 `size` 設為 `10`：

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
body: |
{
  "source": "{% raw %}{ {{#limit}} \"size\": \"2\", {{/limit}} {{^limit}} \"size\": \"10\", {{/limit}} \"query\":{\"match\":{\"play_name\": \"{{play_name}}\"}}}{% endraw %}",
  "params": {
    "play_name": "Henry IV",
    "limit": true
  }
}
-->
{% capture step1_rest %}
GET /_search/template
{
  "source": "{% raw %}{ {{#limit}} \"size\": \"2\", {{/limit}} {{^limit}} \"size\": \"10\", {{/limit}} \"query\":{\"match\":{\"play_name\": \"{{play_name}}\"}}}{% endraw %}",
  "params": {
    "play_name": "Henry IV",
    "limit": true
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  body =   {
    "source": "{% raw %}{ {{#limit}} \"size\": \"2\", {{/limit}} {{^limit}} \"size\": \"10\", {{/limit}} \"query\":{\"match\":{\"play_name\": \"{{play_name}}\"}}}{% endraw %}",
    "params": {
      "play_name": "Henry IV",
      "limit": true
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

### 迴圈

您也可以使用 section 標籤來實作 for-each 迴圈：

```
{% raw %}{{#var}}{{.}}{{/var}}{% endraw %}
```
{% include copy.html %}

當 `var` 是陣列時，標籤之間的內容會針對每個陣列元素重複一次，而 `{% raw %}{{.}}{% endraw %}` 代表目前的元素。如果迴圈在寫入每個元素後都加上逗號，最後一個元素後面會留下多餘的逗號，使查詢成為無效的 JSON。若要將值的陣列傳遞給 `terms` 查詢，請使用 `toJson` 標籤，它會將陣列轉換為 JSON 陣列：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search/template
body: |
{
  "source": "{% raw %}{\"query\":{\"terms\":{\"play_name\":{{#toJson}}play_name{{/toJson}}}}}{% endraw %}",
  "params": {
    "play_name": [
      "Henry IV",
      "Othello"
    ]
  }
}
-->
{% capture step1_rest %}
GET /shakespeare/_search/template
{
  "source": "{% raw %}{\"query\":{\"terms\":{\"play_name\":{{#toJson}}play_name{{/toJson}}}}}{% endraw %}",
  "params": {
    "play_name": [
      "Henry IV",
      "Othello"
    ]
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  index = "shakespeare",
  body =   {
    "source": "{% raw %}{\"query\":{\"terms\":{\"play_name\":{{#toJson}}play_name{{/toJson}}}}}{% endraw %}",
    "params": {
      "play_name": [
        "Henry IV",
        "Othello"
      ]
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

當您將此範本傳送至 [Render Template API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/render-template/) 時，回應會包含下列查詢：

```json
{
  "template_output": {
    "query": {
      "terms": {
        "play_name": [
          "Henry IV",
          "Othello"
        ]
      }
    }
  }
}
```

### 串接

使用 `join` 標籤來串接陣列中的值。根據預設，各個值會以逗號分隔，且不含空格：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search/template
body: |
{
  "source": {
    "query": {
      "match": {
        "text_entry": "{% raw %}{{#join}}text_entry{{/join}}{% endraw %}"
      }
    }
  },
  "params": {
    "text_entry": [
      "To be",
      "or not to be"
    ]
  }
}
-->
{% capture step1_rest %}
GET /shakespeare/_search/template
{
  "source": {
    "query": {
      "match": {
        "text_entry": "{% raw %}{{#join}}text_entry{{/join}}{% endraw %}"
      }
    }
  },
  "params": {
    "text_entry": [
      "To be",
      "or not to be"
    ]
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  index = "shakespeare",
  body =   {
    "source": {
      "query": {
        "match": {
          "text_entry": "{% raw %}{{#join}}text_entry{{/join}}{% endraw %}"
        }
      }
    },
    "params": {
      "text_entry": [
        "To be",
        "or not to be"
      ]
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

此範本會轉譯為下列查詢：

```json
{
  "template_output": {
    "query": {
      "match": {
        "text_entry": "To be,or not to be"
      }
    }
  }
}
```

若要使用不同的分隔符號，請在開始標籤與結束標籤中都指定該分隔符號。下列標籤會以空格分隔各個值，並轉譯為 `To be or not to be`：

```
{% raw %}{{#join delimiter=' '}}text_entry{{/join delimiter=' '}}{% endraw %}
```
{% include copy.html %}

### 轉換為 JSON

使用 `toJson` 標籤將參數轉換為其 JSON 表示法。下列請求將一個 `match` 查詢陣列作為 `bool` 查詢的 `should` 子句傳入：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search/template
body: |
{
  "source": "{\"query\":{\"bool\":{\"should\":{% raw %}{{#toJson}}clauses{{/toJson}}{% endraw %}}}}",
  "params": {
    "clauses": [
      { "match": { "text_entry": "love" } },
      { "match": { "text_entry": "soldier" } }
    ]
  }
}
-->
{% capture step1_rest %}
GET /shakespeare/_search/template
{
  "source": "{\"query\":{\"bool\":{\"should\":{% raw %}{{#toJson}}clauses{{/toJson}}{% endraw %}}}}",
  "params": {
    "clauses": [
      {
        "match": {
          "text_entry": "love"
        }
      },
      {
        "match": {
          "text_entry": "soldier"
        }
      }
    ]
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  index = "shakespeare",
  body =   {
    "source": "{\"query\":{\"bool\":{\"should\":{% raw %}{{#toJson}}clauses{{/toJson}}{% endraw %}}}}",
    "params": {
      "clauses": [
        {
          "match": {
            "text_entry": "love"
          }
        },
        {
          "match": {
            "text_entry": "soldier"
          }
        }
      ]
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

此範本會轉譯為下列查詢：

```json
{
  "template_output": {
    "query": {
      "bool": {
        "should": [
          {
            "match": {
              "text_entry": "love"
            }
          },
          {
            "match": {
              "text_entry": "soldier"
            }
          }
        ]
      }
    }
  }
}
```

### URL 編碼

使用 `url` 標籤，對標籤之間的內容進行 URL 編碼。當範本根據使用者輸入建構 URL 時，這項功能非常實用：

```json
POST /_render/template
{
  "source": {
    "query": {
      "term": {
        "source_url": "https://example.com/plays?name={% raw %}{{#url}}{{play_name}}{{/url}}{% endraw %}"
      }
    }
  },
  "params": {
    "play_name": "Romeo and Juliet"
  }
}
```
{% include copy-curl.html %}

此範本會轉譯出以下查詢：

```json
{
  "template_output": {
    "query": {
      "term": {
        "source_url": "https://example.com/plays?name=Romeo+and+Juliet"
      }
    }
  }
}
```

## 多個搜尋範本

您可以使用 `msearch` 操作，將多個搜尋範本打包，並在單一請求中傳送至您的 OpenSearch 叢集。
這可以節省網路往返時間，因此與個別傳送的請求相比，您可以更快取得回應。

以下範例會執行兩個已儲存的範本。首先，將[條件](#conditions)一節中的條件式範本儲存為 `if_search_template`：

```json
POST _scripts/if_search_template
{
  "script": {
    "lang": "mustache",
    "source": "{% raw %}{ {{#limit}} \"size\": \"{{size}}\", {{/limit}}  \"query\":{\"match\":{\"play_name\": \"{{play_name}}\"}}}{% endraw %}"
  }
}
```
{% include copy-curl.html %}

接著，在單一請求中同時執行 `if_search_template` 和 `play_search_template`：

```json
GET _msearch/template
{"index":"shakespeare"}
{"id":"if_search_template","params":{"play_name":"Henry IV","limit":false,"size":2}}
{"index":"shakespeare"}
{"id":"play_search_template","params":{"play_name":"Henry IV"}}
```

如需更多資訊，請參閱[多重搜尋範本 API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/msearch-template/)。

## 管理搜尋範本

若要列出所有指令碼，請執行下列命令：

<!-- spec_insert_start
component: example_code
rest: GET /_cluster/state/metadata?pretty&filter_path=**.stored_scripts
-->
{% capture step1_rest %}
GET /_cluster/state/metadata?pretty&filter_path=**.stored_scripts
{% endcapture %}

{% capture step1_python %}


response = client.cluster.state(
  metric = "metadata",
  params = { "pretty": "true", "filter_path": "**.stored_scripts" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要擷取特定搜尋範本，請執行下列命令：

<!-- spec_insert_start
component: example_code
rest: GET /_scripts/<name_of_search_template>
-->
{% capture step1_rest %}
GET /_scripts/<name_of_search_template>
{% endcapture %}

{% capture step1_python %}


response = client.get_script(
  id = "<name_of_search_template>"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

若要刪除搜尋範本，請執行下列命令：

<!-- spec_insert_start
component: example_code
rest: DELETE /_scripts/<name_of_search_template>
-->
{% capture step1_rest %}
DELETE /_scripts/<name_of_search_template>
{% endcapture %}

{% capture step1_python %}


response = client.delete_script(
  id = "<name_of_search_template>"
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

## 搜尋範本 API 操作

可使用下列搜尋範本 API 操作：

- [多重搜尋範本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/msearch-template/)
- [呈現範本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/render-template/)

## 必要權限

如果您使用 Security 外掛程式，請確保您具備適當的權限：`indices:data/read/search/template`。
