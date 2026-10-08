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

## 建立搜尋範本

搜尋範本有兩個組成部分：查詢和參數。參數是放入變數中的使用者輸入值。變數在 Mustache 記號中以雙大括號表示。當在查詢中遇到 `{% raw %}{{var}}{% endraw %}` 這類變數時，OpenSearch 會前往 `params` 部分，尋找名為 `var` 的參數，並以指定的值取代它。

您可以編寫應用程式詢問使用者想要搜尋什麼，然後在執行階段將該值插入 `params` 物件中。

此命令定義一個搜尋範本，依名稱尋找劇作。查詢中的 `{% raw %}{{play_name}}{% endraw %}` 會被值 `Henry IV` 取代：

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

此範本會在整個叢集上執行搜尋。若要在特定索引上執行此搜尋，請在請求中加入索引名稱：

<!-- spec_insert_start
component: example_code
rest: GET /shakespeare/_search/template
-->
{% capture step1_rest %}
GET /shakespeare/_search/template
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  index = "shakespeare",
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

指定 `from` 和 `size` 參數：

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

為了改善搜尋體驗，您可以定義預設值，讓使用者不必指定每個可能的參數。如果參數未在 `params` 部分中定義，OpenSearch 會使用預設值。

定義變數 `var` 預設值的語法如下：

```
{% raw %}{{var}}{{^var}}default value{{/var}}{% endraw %}
```
{% include copy.html %}

此命令將 `from` 的預設值設為 10，`size` 的預設值設為 10：

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

在搜尋範本符合您的需求後，您可以將該範本的來源儲存為指令碼，使其可重複用於不同的輸入參數。

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
    },
    "params": {
      "play_name": "Henry IV"
    }
  }
}
```

現在您可以透過參照其 `id` 參數來重複使用此範本。您可以將此來源範本重複用於不同的輸入值：

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
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
GET /_search/template
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

## 回應範例

```json
{
  "took": 7,
  "timed_out": false,
  "_shards": {
    "total": 6,
    "successful": 6,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 3205,
      "relation": "eq"
    },
    "max_score": 3.641852,
    "hits": [
      {
        "_index": "shakespeare",
        "_type": "_doc",
        "_id": "4",
        "_score": 3.641852,
        "_source": {
          "type": "line",
          "line_id": 5,
          "play_name": "Henry IV",
          "speech_number": 1,
          "line_number": "1.1.2",
          "speaker": "KING HENRY IV",
          "text_entry": "Find we a time for frighted peace to pant,"
        }
      }
    ]
  }
}
```

如果您有已儲存的範本並想驗證它，請使用 `render` 操作：

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

當 `var` 是布林值時，此語法會作為 `if` 條件。只有當 `var` 的求值結果為 `true` 時，`{% raw %}{{#var}}{% endraw %}` 和 `{% raw %}{{/var}}{% endraw %}` 標籤才會插入位於兩者之間的值。

使用區段標籤會使您的 JSON 無效，因此您必須改以字串格式撰寫查詢。

此命令只有在 `limit` 參數設為 `true` 時，才會在查詢中包含 `size` 參數。
在下列範例中，`limit` 參數為 `true`，因此會啟用 `size` 參數。結果只會傳回兩份文件。

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

您也可以設計 `if-else` 條件。如果 `limit` 為 `true`，此命令會將 `size` 設為 `2`。否則，會將 `size` 設為 `10`：

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

您也可以使用區段標籤來實作 for-each 迴圈：

```
{% raw %}{{#var}}{{.}}{{/var}}{% endraw %}
```
{% include copy.html %}

當 `var` 是陣列時，搜尋範本會逐一走訪其中的元素，並建立 `terms` 查詢。

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
body: |
{
  "source": "{% raw %}{\"query\":{\"terms\":{\"play_name\":[\"{{#play_name}}\",\"{{.}}\",\"{{/play_name}}\"]}}}{% endraw %}",
  "params": {
    "play_name": [
      "Henry IV",
      "Othello"
    ]
  }
}
-->
{% capture step1_rest %}
GET /_search/template
{
  "source": "{% raw %}{\"query\":{\"terms\":{\"play_name\":[\"{{#play_name}}\",\"{{.}}\",\"{{/play_name}}\"]}}}{% endraw %}",
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
  body =   {
    "source": "{% raw %}{\"query\":{\"terms\":{\"play_name\":[\"{{#play_name}}\",\"{{.}}\",\"{{/play_name}}\"]}}}{% endraw %}",
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

此範本會呈現為：

```json
GET _search/template
{
  "source": {
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

您可以使用 `join` 標籤來串接陣列中的值（以逗號分隔）：

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
body: |
{
  "source": {
    "query": {
      "match": {
        "text_entry": "{% raw %}{{#join}}{{text_entry}}{{/join}}{% endraw %}"
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
GET /_search/template
{
  "source": {
    "query": {
      "match": {
        "text_entry": "{% raw %}{{#join}}{{text_entry}}{{/join}}{% endraw %}"
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
  body =   {
    "source": {
      "query": {
        "match": {
          "text_entry": "{% raw %}{{#join}}{{text_entry}}{{/join}}{% endraw %}"
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

呈現為：

```json
GET _search/template
{
  "source": {
    "query": {
      "match": {
        "text_entry": "{0=To be, 1=or not to be}"
      }
    }
  }
}
```

### 轉換為 JSON

您可以使用 `toJson` 標籤將參數轉換為其 JSON 表示形式：

<!-- spec_insert_start
component: example_code
rest: GET /_search/template
body: |
{
  "source": "{\"query\":{\"bool\":{\"must\":[{\"terms\": {\"text_entries\": {% raw %}{{#toJson}}text_entries{{/toJson}}{% endraw %} }}] }}}",
  "params": {
    "text_entries": [
        { "term": { "text_entry" : "love" } },
        { "term": { "text_entry" : "soldier" } }
    ]
  }
}
-->
{% capture step1_rest %}
GET /_search/template
{
  "source": "{\"query\":{\"bool\":{\"must\":[{\"terms\": {\"text_entries\": {% raw %}{{#toJson}}text_entries{{/toJson}}{% endraw %} }}] }}}",
  "params": {
    "text_entries": [
      {
        "term": {
          "text_entry": "love"
        }
      },
      {
        "term": {
          "text_entry": "soldier"
        }
      }
    ]
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search_template(
  body =   {
    "source": "{\"query\":{\"bool\":{\"must\":[{\"terms\": {\"text_entries\": {% raw %}{{#toJson}}text_entries{{/toJson}}{% endraw %} }}] }}}",
    "params": {
      "text_entries": [
        {
          "term": {
            "text_entry": "love"
          }
        },
        {
          "term": {
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

呈現結果如下：

```json
GET _search/template
{
  "source": {
    "query": {
      "bool": {
        "must": [
          {
            "terms": {
              "text_entries": [
                {
                  "term": {
                    "text_entry": "love"
                  }
                },
                {
                  "term": {
                    "text_entry": "soldier"
                  }
                }
              ]
            }
          }
        ]
      }
    }
  }
}
```

## 多個搜尋範本

您可以使用 `msearch` 操作，將多個搜尋範本合併在單一請求中，傳送至您的 OpenSearch 叢集。
這可節省網路往返時間，因此相較於個別請求，您可以更快收到回應。

```json
GET _msearch/template
{"index":"shakespeare"}
{"id":"if_search_template","params":{"play_name":"Henry IV","limit":false,"size":2}}
{"index":"shakespeare"}
{"id":"play_search_template","params":{"play_name":"Henry IV"}}
```

如需詳細資訊，請參閱[多重搜尋範本 API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/msearch-template/)。

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
