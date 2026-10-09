---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "截斷命中結果"
nav_order: 150
has_children: false
parent: User-defined search processors
grand_parent: Search pipelines
---

# 截斷命中結果處理器
於 2.12 版推出
{: .label .label-purple }

`truncate_hits` 回應處理器會在達到指定的命中數後捨棄傳回的搜尋命中結果。`truncate_hits` 處理器設計上可搭配 [`oversample` 請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/oversample-processor/) 使用，但也可以單獨使用。

`target_size` 參數（指定要從何處截斷）為選用。若未指定，OpenSearch 會使用由
`oversample` 處理器設定的 `original_size` 變數（若有提供）。

以下是常見的使用模式：

1. 將 `oversample` 處理器加入請求管線，以取得更大的一組結果。
1. 在回應管線中，套用重新排序處理器（可能會將超出原先要求前 N 名的結果提升）或 `collapse` 處理器（可能會在去除重複後捨棄結果）。
1. 套用 `truncate` 處理器，以傳回（最多）原先要求的命中數。

## 請求本文欄位

下表列出所有請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`target_size` | 整數 | 要傳回的搜尋命中數上限（>=0）。若未指定，處理器會嘗試讀取 `original_size` 變數，若無法取得則會失敗。選用。
`context_prefix` | 字串 | 可用來從特定範圍讀取 `original_size` 變數，以避免衝突。選用。
`tag` | 字串 | 處理器的識別碼。選用。
`description` | 字串 | 處理器的說明。選用。
`ignore_failure` | 布林值 | 若為 `true`，OpenSearch [會忽略此處理器的任何失敗]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/creating-search-pipeline/#ignoring-processor-failures)，並繼續執行搜尋管線中其餘的處理器。選用。預設為 `false`。

## 範例

以下範例示範如何使用含有 `truncate` 處理器的搜尋管線。

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

以下請求會建立一個名為 `my_pipeline` 的搜尋管線，其中的 `truncate_hits` 回應處理器會捨棄前五筆以外的命中結果：

```json
PUT /_search/pipeline/my_pipeline 
{
  "response_processors": [
    {
      "truncate_hits" : {
        "tag" : "truncate_1",
        "description" : "This processor will discard results after the first 5.",
        "target_size" : 5
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 使用搜尋管線

在 `my_index` 中搜尋文件，不使用搜尋管線：

```json
POST /my_index/_search
{
  "size": 8
}
```
{% include copy-curl.html %}

回應包含八筆命中結果：

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

若要使用管線搜尋，請在 `search_pipeline` 查詢參數中指定管線名稱：

```json
POST /my_index/_search?search_pipeline=my_pipeline
{
  "size": 8
}
```
{% include copy-curl.html %}

回應只包含 5 筆命中結果，即使要求了 8 筆且可取得 10 筆：

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

## 過度取樣、收合與截斷命中結果

以下是一個更貼近實務的範例，您使用 `oversample` 要求許多候選文件，使用 `collapse` 移除特定欄位重複的文件（以取得更多樣化的結果），然後使用 `truncate` 傳回原先要求的文件數（以避免叢集傳回大量結果資料）。


### 設定

建立許多包含您將用於收合之欄位的文件：

```json
POST /_bulk
{ "create":{"_index":"my_index","_id":1}}
{ "title" : "document 1", "color":"blue" }
{ "create":{"_index":"my_index","_id":2}}
{ "title" : "document 2", "color":"blue" }
{ "create":{"_index":"my_index","_id":3}}
{ "title" : "document 3", "color":"red" }
{ "create":{"_index":"my_index","_id":4}}
{ "title" : "document 4", "color":"red" }
{ "create":{"_index":"my_index","_id":5}}
{ "title" : "document 5", "color":"yellow" }
{ "create":{"_index":"my_index","_id":6}}
{ "title" : "document 6", "color":"yellow" }
{ "create":{"_index":"my_index","_id":7}}
{ "title" : "document 7", "color":"orange" }
{ "create":{"_index":"my_index","_id":8}}
{ "title" : "document 8", "color":"orange" }
{ "create":{"_index":"my_index","_id":9}}
{ "title" : "document 9", "color":"green" }
{ "create":{"_index":"my_index","_id":10}}
{ "title" : "document 10", "color":"green" }
``` 
{% include copy-curl.html %}

建立一個只依 `color` 欄位收合的管線：

```json
PUT /_search/pipeline/collapse_pipeline
{
  "response_processors": [
    {
      "collapse" : {
        "field": "color"
      }
    }
  ]
}
```
{% include copy-curl.html %}

建立另一個會過度取樣、收合，然後截斷結果的管線：

```json
PUT /_search/pipeline/oversampling_collapse_pipeline
{
  "request_processors": [
    {
      "oversample": {
        "sample_factor": 3
      }
    }
  ],
  "response_processors": [
    {
      "collapse" : {
        "field": "color"
      }
    },
    {
      "truncate_hits": {
        "description": "Truncates back to the original size before oversample increased it."
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 不進行過度取樣的收合

在此範例中，您在依 `color` 欄位收合之前要求前三份文件。由於前兩份文件具有相同的 `color`，第二份會被捨棄，請求會傳回第一份與第三份文件：

```json
POST /my_index/_search?search_pipeline=collapse_pipeline
{
  "size": 3
}
```
{% include copy-curl.html %}


<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
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
          "title" : "document 1",
          "color" : "blue"
        }
      },
      {
        "_index" : "my_index",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "title" : "document 3",
          "color" : "red"
        }
      }
    ]
  },
  "profile" : {
    "shards" : [ ]
  }
}
```
</details>


### 過度取樣、收合與截斷

現在您將使用 `oversampling_collapse_pipeline`，它會要求前 9 份文件（將大小乘以 3），依 `color` 去除重複，然後傳回前 3 筆命中結果：

```json
POST /my_index/_search?search_pipeline=oversampling_collapse_pipeline
{
  "size": 3
}
```
{% include copy-curl.html %}


<details open markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
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
          "title" : "document 1",
          "color" : "blue"
        }
      },
      {
        "_index" : "my_index",
        "_id" : "3",
        "_score" : 1.0,
        "_source" : {
          "title" : "document 3",
          "color" : "red"
        }
      },
      {
        "_index" : "my_index",
        "_id" : "5",
        "_score" : 1.0,
        "_source" : {
          "title" : "document 5",
          "color" : "yellow"
        }
      }
    ]
  },
  "profile" : {
    "shards" : [ ]
  }
}
```
</details>


