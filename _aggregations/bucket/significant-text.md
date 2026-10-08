---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Significant text
parent: Bucket aggregations
nav_order: 190
redirect_from:
  - /query-dsl/aggregations/bucket/significant-text/
---

# Significant text 彙總

`significant_text` 彙總透過將前景集（您的查詢結果）中的詞元頻率與背景集（整個索引）進行比較，來識別自由文本欄位中不尋常或有趣的詞元。與在已編製索引的 keyword 欄位上運作的 [`significant_terms`]({{site.url}}{{site.baseurl}}/aggregations/bucket/significant-terms/) 不同，`significant_text` 會即時重新分析來源文本，並能篩選掉否則會使結果偏差的重複內容。

重新分析大型結果集會消耗大量 CPU。請在 [`sampler`]({{site.url}}{{site.baseurl}}/aggregations/bucket/sampler/) 或 [`diversified_sampler`]({{site.url}}{{site.baseurl}}/aggregations/bucket/diversified-sampler/) 彙總中使用 `significant_text`，將分析限制在少數最符合的文件（例如 100--200 份）中。
{: .note}

## 參數

`significant_text` 彙總使用以下參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `field` | 必要 | String | 要分析的文本欄位。 |
| `size` | 選用 | Integer | 要回傳的詞元桶數量。預設值為 `10`。 |
| `shard_size` | 選用 | Integer | 從每個分片收集的候選詞元數量。較高值可提高準確性，但會降低效能。預設值為 `-1`（自動估算）。 |
| `min_doc_count` | 選用 | Integer | 要包含某個詞元，該詞元必須出現的最少文件數量。預設值為 `3`。設定為 `1` 傾向於回傳打字錯誤和拼寫錯誤。 |
| `shard_min_doc_count` | 選用 | Integer | 詞元被視為候選詞元的最小本機分片頻率。預設值為 `1`。 |
| `background_filter` | 選用 | Object | 用於縮小比較時所使用的背景集的查詢。預設情況下，整個索引被用作背景。 |
| `filter_duplicate_text` | 選用 | Boolean | 當為 `true` 時，會篩選掉已經出現過的 6 個或更多詞元的序列，從而減少剪貼內容產生的雜訊。預設值為 `false`。 |
| `source_fields` | 選用 | Array | 要分析文本的 JSON 來源欄位名稱列表。當已編製索引的欄位名稱與來源欄位不同時使用（例如使用 `copy_to`）。 |
| `include` | 選用 | String 或 Array | 要包含的正規表達式模式或精確詞元列表。 |
| `exclude` | 選用 | String 或 Array | 要從結果中排除的正規表達式模式或精確詞元列表。 |

## 範例

以下範例假設有一個 `shakespeare` 索引，其中包含莎士比亞的完整作品以及一個 `text_entry` 文本欄位。該查詢搜尋包含 "breathe" 的文件，然後在 `sampler` 中使用 `significant_text`，以發現相較於整個語料庫，與這些段落最密切相關的詞元：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "breathe"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "text_entry",
            "min_doc_count": 4
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應將「air」、「dead」和「life」等詞元識別為與有關呼吸的段落顯著相關：

```json
{
  "took" : 44,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 59,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "sample" : {
      "doc_count" : 59,
      "keywords" : {
        "doc_count" : 59,
        "bg_count" : 111396,
        "buckets" : [
          {
            "key" : "breathe",
            "doc_count" : 59,
            "score" : 1887.0677966101694,
            "bg_count" : 59
          },
          {
            "key" : "air",
            "doc_count" : 4,
            "score" : 2.641295376716233,
            "bg_count" : 189
          },
          {
            "key" : "dead",
            "doc_count" : 4,
            "score" : 0.9665839666414213,
            "bg_count" : 495
          },
          {
            "key" : "life",
            "doc_count" : 5,
            "score" : 0.9090787433467572,
            "bg_count" : 805
          }
        ]
      }
    }
  }
}
```

## 範例：使用篩選器縮小背景

預設情況下，詞元頻率會與整個索引進行比較。`background_filter` 參數可縮小比較集，這能揭露在特定情境中具有顯著意義的詞元。以下範例將 "breathe" 段落僅與來自 "Henry IV" 的行數（而非整個語料庫）進行比較：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "breathe"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "text_entry",
            "min_doc_count": 3,
            "background_filter": {
              "term": {
                "play_name": "Henry IV"
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

當背景縮小至 3,205 行（僅 Henry IV）時，`bg_count` 值會較小，且分數也會隨之改變：

```json
{
  "took" : 83,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 59,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "sample" : {
      "doc_count" : 59,
      "keywords" : {
        "doc_count" : 59,
        "bg_count" : 3205,
        "buckets" : [
          {
            "key" : "breathe",
            "doc_count" : 59,
            "score" : 533.1666666666666,
            "bg_count" : 6
          },
          {
            "key" : "air",
            "doc_count" : 4,
            "score" : 4.842669730920234,
            "bg_count" : 3
          },
          {
            "key" : "dead",
            "doc_count" : 4,
            "score" : 1.0653879300819835,
            "bg_count" : 13
          }
        ]
      }
    }
  }
}
```

## 回應本文欄位

下表列出回應本文的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | Integer | 樣本中的文件數量（在 sampler 層級）或前景集中的文件數量（在 significant_text 層級）。 |
| `bg_count` | Integer | 用於比較的背景集中的文件總數。 |
| `buckets` | Array | 顯著詞元桶，依 `score` 降冪排序。 |
| `buckets.key` | String | 顯著詞元。 |
| `buckets.doc_count` | Integer | 前景集中包含此詞元的文件數量。 |
| `buckets.score` | Double | 顯著性分數，代表此詞元在前景中出現的頻率比在背景中高出多少。 |
| `buckets.bg_count` | Integer | 背景集中包含此詞元的文件數量。 |

## 顯著性啟發式演算法

預設情況下，顯著性分數使用 Johnson-Laird 和 Hinkley (JLH) 啟發式演算法。您可以透過在 `field` 旁新增名稱作為參數來選擇替代的分數計算演算法。支援以下啟發式演算法：

| 啟發式演算法 | 參數 | 說明 |
| :--- | :--- | :--- |
| JLH | `jlh: {}` | 預設值。衡量前景與背景之間流行度的相對變化。 |
| Mutual information | `mutual_information: {}` | 衡量詞元的出現為其屬於前景集提供了多少資訊。支援 `include_negatives` 和 `background_is_superset` 選項。 |
| Chi-square | `chi_square: {}` | 詞元與前景集之間獨立性的標準統計檢定。支援 `include_negatives` 和 `background_is_superset` 選項。 |
| GND | `gnd: {}` | Google Normalized Distance。使用共現比率衡量統計關聯性。支援 `background_is_superset` 選項。 |

以下範例使用 chi-square 分數而非預設的 JLH：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "breathe"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "keywords": {
          "significant_text": {
            "field": "text_entry",
            "min_doc_count": 4,
            "chi_square": {}
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示識別出相同的詞元，但分數量表不同：

```json
{
  "took" : 19,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 59,
      "relation" : "eq"
    },
    "max_score" : null,
    "hits" : [ ]
  },
  "aggregations" : {
    "sample" : {
      "doc_count" : 59,
      "keywords" : {
        "doc_count" : 59,
        "bg_count" : 111396,
        "buckets" : [
          {
            "key" : "breathe",
            "doc_count" : 59,
            "score" : 111396.0,
            "bg_count" : 59
          },
          {
            "key" : "air",
            "doc_count" : 4,
            "score" : 152.27540220402065,
            "bg_count" : 189
          },
          {
            "key" : "dead",
            "doc_count" : 4,
            "score" : 53.556852313941825,
            "bg_count" : 495
          },
          {
            "key" : "life",
            "doc_count" : 5,
            "score" : 49.44532193700098,
            "bg_count" : 805
          }
        ]
      }
    }
  }
}
```

## 限制

`significant_text` 彙總有以下限制：

- 由於記憶體成本高，不支援子彙總。若要進一步分析特定詞元，請執行另一個包含 `terms` 彙總和包含初始結果中顯著詞元的 `include` 子句的查詢。
- 不支援巢狀物件，因為它直接處理文件的 JSON 來源。
- 文件計數可能存在輕微誤差，因為每個分片獨立回報，且計數在協調節點進行合併。增加 `shard_size` 可提高精確度，但會降低效能。預設情況下，`shard_size` 設定為 -1，以自動估算分片數量和 `size` 參數。
