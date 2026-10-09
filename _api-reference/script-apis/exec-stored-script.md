---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行已儲存指令碼"
parent: Script APIs
nav_order: 20
---

# 執行已儲存指令碼 API
**於 1.0 版引入**
{: .label .label-purple }

執行先前使用 Create Stored Script API 儲存至叢集狀態的已儲存指令碼。如需詳細資訊，請參閱 [Painless 指令碼語言]({{site.url}}{{site.baseurl}}/scripting/painless/)。 

OpenSearch 提供數種執行指令碼的方式；以下各節說明如何在 `GET <index>/_search` 請求的請求本文中傳遞指令碼資訊，以執行指令碼。

## 端點

```json
GET books/_search
{
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "my-first-script" 
      }
    }
  }
}
```

## 請求本文欄位

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `query` | 物件 | 指定要處理哪些文件的篩選器。 |
| `script_fields` | 物件 | 要包含在輸出中的欄位。 | 
| `script` | 物件 | 為欄位產生值的指令碼 ID。 |

## 請求範例
<!-- spec_insert_start
component: example_code
rest: GET /books/_search
body: |
{
   "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "multiplier-script",
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
-->
{% capture step1_rest %}
GET /books/_search
{
  "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "multiplier-script",
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "books",
  body =   {
    "query": {
      "match_all": {}
    },
    "script_fields": {
      "total_ratings": {
        "script": {
          "id": "multiplier-script",
          "params": {
            "multiplier": 2
          }
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

下列請求會執行在[建立或更新已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/)中建立的已儲存指令碼。此指令碼會加總每本書的評分，並在輸出的 `total_ratings` 欄位中顯示總和。

* 指令碼的目標是 `books` 索引。

* `"match_all": {}` 屬性值為空物件，表示要處理索引中的每份文件。

* `total_ratings` 欄位值是執行 `my-first-script` 的結果。請參閱  [建立或更新已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/)。

<!-- spec_insert_start
component: example_code
rest: GET /books/_search
body: |
{
   "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "my-first-script"
      }
    }
  }
}
-->
{% capture step1_rest %}
GET /books/_search
{
  "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "my-first-script"
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "books",
  body =   {
    "query": {
      "match_all": {}
    },
    "script_fields": {
      "total_ratings": {
        "script": {
          "id": "my-first-script"
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

#### 回應範例

`GET books/_search` 請求會傳回下列欄位：

````json
{
  "took" : 2,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "books",
        "_id" : "1",
        "_score" : 1.0,
        "fields" : {
          "total_ratings" : [
            12
          ]
        }
      },
      {
        "_index" : "books",
        "_id" : "2",
        "_score" : 1.0,
        "fields" : {
          "total_ratings" : [
            15
          ]
        }
      },
      {
        "_index" : "books",
        "_id" : "3",
        "_score" : 1.0,
        "fields" : {
          "total_ratings" : [
            8
          ]
        }
      }
    ]
  }
}
````

## 回應本文欄位

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `took` | 整數 | 作業所花費的時間，以毫秒為單位。 |
| `timed_out` | 布林值 | 作業是否逾時。 |
| `_shards` | 物件 | 已處理的分片總數，以及成功、略過和未處理的分片各自的總數。 |
| `hits` | 物件 | 包含已處理文件的概略資訊，以及由 `hits` 物件組成的陣列。請參閱[命中物件](#hits-object)。 | 

#### 命中物件

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `total` | 物件 | 已處理的文件總數，以及此總數與 `match` 請求欄位的關係。 |
| `max_score` | 雙精度浮點數 | 所有命中結果中傳回的最高相關性分數。 |
| `hits` | 陣列 | 每份已處理文件的資訊。請參閱[文件物件](#Document-object)。 |

#### 文件物件

| 欄位 | 資料類型 | 說明 | 
:--- | :--- | :---
| `_index` | 字串 | 包含該文件的索引。 |
| `_id` | 字串 | 文件 ID。 |
| `_score` | 浮點數 | 文件的相關性分數。 |
| `fields` | 物件 | 指令碼傳回的欄位及其值。 |

## 使用參數執行 Painless 已儲存指令碼

若要在每次執行查詢時將不同的參數傳遞給指令碼，請在 `script_fields` 中定義 `params`。

下列請求會執行在[建立或更新已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/)中建立的已儲存指令碼。此指令碼會加總每本書的評分，將總和值乘以 `multiplier` 參數，並在輸出中顯示結果。

* 指令碼的目標是 `books` 索引。

* `"match_all": {}` 屬性值為空物件，表示它會處理索引中的每份文件。

* `total_ratings` 欄位值是執行 `multiplier-script` 的結果。請參閱[使用參數建立或更新已儲存指令碼]({{site.url}}{{site.baseurl}}/api-reference/script-apis/create-stored-script/)。

* `params` 欄位中的 `"multiplier": 2` 是傳遞給已儲存指令碼 `multiplier-script` 的變數：

<!-- spec_insert_start
component: example_code
rest: GET /books/_search
body: |
{
   "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "multiplier-script",
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
-->
{% capture step1_rest %}
GET /books/_search
{
  "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "multiplier-script",
        "params": {
          "multiplier": 2
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.search(
  index = "books",
  body =   {
    "query": {
      "match_all": {}
    },
    "script_fields": {
      "total_ratings": {
        "script": {
          "id": "multiplier-script",
          "params": {
            "multiplier": 2
          }
        }
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

回應包含符合條件的文件：

```json
{
  "took" : 12,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : 1.0,
        "fields" : {
          "total_ratings" : [
            16
          ]
        }
      },
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : 1.0,
        "fields" : {
          "total_ratings" : [
            30
          ]
        }
      },
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : 1.0,
        "fields" : {
          "total_ratings" : [
            24
          ]
        }
      }
    ]
  }
}
```

## 使用 Painless 已儲存指令碼排序結果

下列範例使用 Painless 已儲存指令碼排序結果：

```json
GET books/_search
{
   "query": {
    "match_all": {}
  },
  "script_fields": {
    "total_ratings": {
      "script": {
        "id": "multiplier-script",
        "params": {
          "multiplier": 2
        }
      }
    }
  },
  "sort": {
    "_script": {
       "type": "number",
       "script": {
         "id": "multiplier-script",
         "params": {
           "multiplier": 2
          }
       },
       "order": "desc"
    }
  }
}
```

#### 回應範例

```json
{
  "took" : 90,
  "timed_out" : false,
  "_shards" : {
    "total" : 5,
    "successful" : 5,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 3,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "2",
        "_score" : null,
        "fields" : {
          "total_ratings" : [
            30
          ]
        },
        "sort" : [
          30.0
        ]
      },
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "1",
        "_score" : null,
        "fields" : {
          "total_ratings" : [
            24
          ]
        },
        "sort" : [
          24.0
        ]
      },
      {
        "_index" : "books",
        "_type" : "_doc",
        "_id" : "3",
        "_score" : null,
        "fields" : {
          "total_ratings" : [
            16
          ]
        },
        "sort" : [
          16.0
        ]
      }
    ]
  }
}
```
