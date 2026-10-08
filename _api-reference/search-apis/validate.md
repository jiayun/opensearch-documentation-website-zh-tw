---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "驗證查詢"
nav_order: 87
parent: Search APIs
redirect_from: 
 - /api-reference/validate/
---

# Validate Query API
**1.0 版推出**
{: .label .label-purple }

您可以使用 Validate Query API 在不執行查詢的情況下驗證查詢。查詢可以作為路徑參數傳送，也可以包含在請求本文中。

## 端點

Validate Query API 包含下列路徑：

```json
GET {index}/_validate/query
```

## 路徑參數

所有路徑參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`index` | 字串 | 要據以驗證查詢的索引。如果您未在 URL 中指定一個或多個索引（或想要覆寫個別搜尋的 URL 值），可以在此處加入。範例包括 `"logs-*"` 和 `["my-store", "sample_data_ecommerce"]`。
`query` | 查詢物件 | 使用 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 撰寫的查詢。

## 查詢參數

下表列出可用的查詢參數。所有查詢參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`all_shards` | 布林值 | 若為 `true`，則會針對[所有分片](#rewrite-and-all_shards)執行驗證，而非每個索引僅針對一個分片。預設為 `false`。
`allow_no_indices` | 布林值 | 是否忽略不符合任何索引的萬用字元。預設為 `true`。
`allow_partial_search_results` | 布林值 | 當請求發生錯誤或逾時時，是否傳回部分結果。預設為 `true`。
`analyzer` | 字串 | 查詢字串中要使用的分析器。此參數僅應與 `q` 選項搭配使用。
`analyze_wildcard` | 布林值 | 指定是否分析萬用字元查詢和前綴查詢。預設為 `false`。 
`default_operator` | 字串 | 指出字串查詢的預設運算子應為 `AND` 或 `OR`。預設為 `OR`。
`df` | 字串 | 查詢字串中未提供欄位前綴時使用的預設欄位。
`expand_wildcards` | 字串 | 指定萬用字元運算式可比對的索引類型。支援以逗號分隔的值。有效值為 `all`（比對任何索引）、`open`（比對開啟且非隱藏的索引）、`closed`（比對已關閉且非隱藏的索引）、`hidden`（比對隱藏索引）以及 `none`（拒絕萬用字元運算式）。預設為 `open`。
`explain` | 布林值 | 是否傳回 OpenSearch 如何計算[文件分數](#explain)的相關資訊。預設為 `false`。
`ignore_unavailable` |  布林值 | 指定是否在回應中包含遺失或已關閉的索引，並在搜尋請求期間忽略無法使用的分片。預設為 `false`。
`lenient` | 布林值 | 指定 OpenSearch 是否應忽略因格式造成的查詢失敗（例如，以整數查詢文字欄位所導致的失敗）。預設為 `false`。 
`rewrite` | 決定 OpenSearch 如何[重寫](#rewrite)多詞查詢並為其評分。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。預設為 `constant_score`。
`q` | 字串 | 以 Lucene 字串語法撰寫的查詢。

## 請求範例

下列請求範例使用名為 `Hamlet` 的索引，該索引是透過 `bulk` 請求建立的：

<!-- spec_insert_start
component: example_code
rest: PUT /hamlet/_bulk?refresh
body: |
{"index":{"_id":1}}
{"user" : { "id": "hamlet" }, "@timestamp" : "2099-11-15T14:12:12", "message" : "To Search or Not To Search"}
{"index":{"_id":2}}
{"user" : { "id": "hamlet" }, "@timestamp" : "2099-11-15T14:12:13", "message" : "My dad says that I'm such a ham."}
-->
{% capture step1_rest %}
PUT /hamlet/_bulk?refresh
{"index":{"_id":1}}
{"user" : { "id": "hamlet" }, "@timestamp" : "2099-11-15T14:12:12", "message" : "To Search or Not To Search"}
{"index":{"_id":2}}
{"user" : { "id": "hamlet" }, "@timestamp" : "2099-11-15T14:12:13", "message" : "My dad says that I'm such a ham."}
{% endcapture %}

{% capture step1_python %}


response = client.bulk(
  index = "hamlet",
  params = { "refresh": "true" },
  body = '''
{"index":{"_id":1}}
{"user" : { "id": "hamlet" }, "@timestamp" : "2099-11-15T14:12:12", "message" : "To Search or Not To Search"}
{"index":{"_id":2}}
{"user" : { "id": "hamlet" }, "@timestamp" : "2099-11-15T14:12:13", "message" : "My dad says that I'm such a ham."}
'''
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

接著，您可以使用 Validate Query API 驗證索引查詢，如下列範例所示：

<!-- spec_insert_start
component: example_code
rest: GET /hamlet/_validate/query?q=user.id:hamlet
-->
{% capture step1_rest %}
GET /hamlet/_validate/query?q=user.id:hamlet
{% endcapture %}

{% capture step1_python %}


response = client.indices.validate_query(
  index = "hamlet",
  params = { "q": "user.id:hamlet" },
  body = { "Insert body here" }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

查詢也可以作為請求本文傳送，如下列範例所示：

<!-- spec_insert_start
component: example_code
rest: GET /hamlet/_validate/query
body: |
{
  "query" : {
    "bool" : {
      "must" : {
        "query_string" : {
          "query" : "*:*"
        }
      },
      "filter" : {
        "term" : { "user.id" : "hamlet" }
      }
    }
  }
}
-->
{% capture step1_rest %}
GET /hamlet/_validate/query
{
  "query": {
    "bool": {
      "must": {
        "query_string": {
          "query": "*:*"
        }
      },
      "filter": {
        "term": {
          "user.id": "hamlet"
        }
      }
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.validate_query(
  index = "hamlet",
  body =   {
    "query": {
      "bool": {
        "must": {
          "query_string": {
            "query": "*:*"
          }
        },
        "filter": {
          "term": {
            "user.id": "hamlet"
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


## 回應範例

如果查詢通過驗證，回應會指出該查詢為 `true`，如下列回應範例所示，其中 `valid` 參數為 `true`：

```
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "valid": true
}
```

如果查詢未通過驗證，OpenSearch 會回應該查詢為 `false`。下列請求範例的查詢包含未在 `hamlet` 索引中設定的動態對應：

<!-- spec_insert_start
component: example_code
rest: GET /hamlet/_validate/query
body: |
{
  "query": {
    "query_string": {
      "query": "@timestamp:foo",
      "lenient": false
    }
  }
}
-->
{% capture step1_rest %}
GET /hamlet/_validate/query
{
  "query": {
    "query_string": {
      "query": "@timestamp:foo",
      "lenient": false
    }
  }
}
{% endcapture %}

{% capture step1_python %}


response = client.indices.validate_query(
  index = "hamlet",
  body =   {
    "query": {
      "query_string": {
        "query": "@timestamp:foo",
        "lenient": false
      }
    }
  }
)

{% endcapture %}

{% include code-block.html
    rest=step1_rest
    python=step1_python %}
<!-- spec_insert_end -->

OpenSearch 會傳回下列回應，其中 `valid` 參數為 `false`：

```
{
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "valid": false
}
```

某些查詢參數也會影響回應中包含的內容。下列範例說明 [Explain](#explain)、[Rewrite](#rewrite) 和 [all_shards](#rewrite-and-all_shards) 查詢選項如何影響回應。

### Explain 

`explain` 選項會在 `explanations` 欄位中傳回查詢失敗的相關資訊，如下列回應範例所示：

```
{
  "valid" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "failed" : 0
  },
  "explanations" : [ {
    "index" : "_shakespeare",
    "valid" : false,
    "error" : "shakespeare/IAEc2nIXSSunQA_suI0MLw] QueryShardException[failed to create query:...failed to parse date field [foo]"
  } ]
}
```


### Rewrite

當請求中的 `rewrite` 選項設定為 `true` 時，`explanations` 選項會以字串形式顯示所執行的 Lucene 查詢，如下列回應所示：

```
{
   "valid": true,
   "_shards": {
      "total": 1,
      "successful": 1,
      "failed": 0
   },
   "explanations": [
      {
         "index": "",
         "valid": true,
         "explanation": "((user:hamlet^4.256753 play:hamlet^6.863601 play:romeo^2.8415773 plot:puck^3.4193945 plot:othello^3.8244398 ... )~4) -ConstantScore(_id:2) #(ConstantScore(_type:_doc))^0.0"
      }
   ]
}
```


### Rewrite 和 all_shards

當 `rewrite` 和 `all_shards` 選項皆設定為 `true` 時，Validate Query API 會回應來自所有可用分片的詳細資訊，而非僅來自單一分片（預設），如下列回應所示：

```
{
  "valid": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "explanations": [
    {
      "index": "my-index-000001",
      "shard": 0,
      "valid": true,
      "explanation": "(user.id:hamlet)^0.6333333"
    }
  ]
}
```

## 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`indices:admin/validate/query`。
