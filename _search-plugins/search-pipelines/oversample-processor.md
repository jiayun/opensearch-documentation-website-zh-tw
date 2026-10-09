---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Oversample
nav_order: 80
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# Oversample 處理器
於 2.12 版推出
{: .label .label-purple }

`oversample` 請求處理器會將搜尋請求的 `size` 參數乘以指定的 `sample_factor` (>= 1.0)，並將原始值儲存在 `original_size` 管線變數中。`oversample` 處理器設計上與 [`truncate_hits` 回應處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/truncate-hits-processor/) 搭配使用，但也可以單獨使用。

## 請求本文欄位

下表列出所有請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`sample_factor` | 浮點數 | 在處理搜尋請求之前，將套用至 `size` 參數的乘數 (>= 1.0)。必要。
`context_prefix` | 字串 | 可用來限定 `original_size` 變數的範圍，以避免衝突。選用。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的描述。選用。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch 會[忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中其餘的處理器。選用。預設為 `false`。


## 範例

下列範例示範如何使用帶有 `oversample` 處理器的搜尋管線。

### 設定

建立一個名為 `my_index` 且包含許多文件的索引：

```json
POST /_bulk
{ "create":{"_index":"my_index","_id":1}}
{ "doc": { "title" : "document 1" }}
{ "create":{"_index":"my_index","_id":2}}
{ "doc": { "title" : "document 2" }}
{ "create":{"_index":"my_index","_id":3}}
{ "doc": { "title" : "document 3" }}
{ "create":{"_index":"my_index","_id":4}}
{ "doc": { "title" : "document 4" }}
{ "create":{"_index":"my_index","_id":5}}
{ "doc": { "title" : "document 5" }}
{ "create":{"_index":"my_index","_id":6}}
{ "doc": { "title" : "document 6" }}
{ "create":{"_index":"my_index","_id":7}}
{ "doc": { "title" : "document 7" }}
{ "create":{"_index":"my_index","_id":8}}
{ "doc": { "title" : "document 8" }}
{ "create":{"_index":"my_index","_id":9}}
{ "doc": { "title" : "document 9" }}
{ "create":{"_index":"my_index","_id":10}}
{ "doc": { "title" : "document 10" }}
```
{% include copy-curl.html %}

### 建立搜尋管線

下列請求會建立一個名為 `my_pipeline` 的搜尋管線，其中包含一個 `oversample` 請求處理器，該處理器要求的結果數比 `size` 中指定的多 50%：

```json
PUT /_search/pipeline/my_pipeline 
{
  "request_processors": [
    {
      "oversample" : {
        "tag" : "oversample_1",
        "description" : "This processor will multiply `size` by 1.5.",
        "sample_factor" : 1.5
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

在不使用搜尋管線的情況下搜尋 `my_index` 中的文件：

```json
POST /my_index/_search
{
  "size": 5
}
```
{% include copy-curl.html %}

回應包含五筆結果：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took" : 3,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 1"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 2"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 3"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "4",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 4"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "5",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 5"
          }
        }
      }
    ]
  }
}
```
</details>

若要使用管線進行搜尋，請在 `search_pipeline` 查詢參數中指定管線名稱：

```json
POST /my_index/_search?search_pipeline=my_pipeline
{
  "size": 5
}
```
{% include copy-curl.html %}

回應包含 8 筆文件（5 * 1.5 = 7.5，無條件進位為 8）：

<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}
  
```json
{
  "took" : 13,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 10,
      "relation" : "eq"
    },
    "max_score" : 1.0,
    "hits" : [
      {
        "_index" : "my_index",
        "_id" : "1",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 1"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "2",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 2"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 3"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "4",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 4"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "5",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 5"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "6",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 6"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "7",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 7"
          }
        }
      },
      {
        "_index" : "my_index",
        "_id" : "8",
        "_score" : 1.0,
        "_source" : {
          "doc" : {
            "title" : "document 8"
          }
        }
      }
    ]
  }
}
```
</details>
