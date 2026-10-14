---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Sampler
parent: Bucket aggregations
nav_order: 170
redirect_from:
  - /query-dsl/aggregations/bucket/sampler/
---

# Sampler 彙總

`sampler` 彙總會將子彙總的處理限制在每個分片上分數最高的文件。這會將焦點縮小到最相關的相符項目，而非處理整個結果集，因此可減少運算時間，並藉由排除長尾中相關性較低的文件，提升彙總結果的品質。

取樣在搭配 `significant_terms` 等子彙總時特別有價值。若沒有 sampler，完整結果集會包含一長串僅略微相關的文件，其通用詞彙在數量上占據主導地位，因而掩蓋了在分數最高之相符項目中真正獨特的詞彙。

如需可避免任何單一欄位值主導樣本的基於多樣性的取樣，請參閱 [`diversified_sampler` 彙總]({{site.url}}{{site.baseurl}}/aggregations/bucket/diversified-sampler/)。

## 參數

`sampler` 彙總採用下列參數。

| 參數 | 必要/選用 | 資料類型 | 說明 |
| :--- | :--- | :--- | :--- |
| `shard_size` | 選用 | 整數 | 從每個分片收集之分數最高文件的最大數量。預設為 `100`。 |

`sampler` 彙總可巢狀置於 `terms` 彙總之下。如果 `terms` 彙總使用 `breadth_first` 收集模式，OpenSearch 會重播延後文件的相關性分數，因此樣本仍以分數最高的文件為依據。
{: .note}

## 範例：取樣分數最高的文件

下列範例使用包含莎士比亞全集的 `shakespeare` 索引，其中每份文件是劇本的一行。`text_entry` 欄位包含該行的文字，而 `play_name` 欄位是 `keyword` 欄位。

查詢 `king falstaff` 會符合 1,545 行。其中大多數只包含常見詞彙 `king`，但同時包含較罕見詞彙 `falstaff` 的行會獲得最高分數。下列請求會取樣每個分片上分數最高的 100 行，並執行 `significant_terms` 子彙總，以找出與樣本最相關的劇本：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "king falstaff"
    }
  },
  "aggs": {
    "sample": {
      "sampler": {
        "shard_size": 100
      },
      "aggs": {
        "plays": {
          "significant_terms": {
            "field": "play_name",
            "size": 3
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

樣本包含 100 行，最顯著的劇本是 *The Merry Wives of Windsor* 和 *Henry IV*，也就是 Falstaff 出現的劇本：

```json
{
  ...
  "aggregations": {
    "sample": {
      "doc_count": 100,
      "plays": {
        "doc_count": 100,
        "bg_count": 111396,
        "buckets": [
          {
            "key": "Merry Wives of Windsor",
            "doc_count": 41,
            "score": 6.2045063935005285,
            "bg_count": 2831
          },
          {
            "key": "Henry IV",
            "doc_count": 31,
            "score": 3.0301421528861154,
            "bg_count": 3205
          },
          {
            "key": "Hamlet",
            "doc_count": 6,
            "score": 0.03449236569274269,
            "bg_count": 4244
          }
        ]
      }
    }
  }
}
```

## 範例：在沒有 sampler 的情況下執行彙總

下列請求會對所有 1,545 行相符項目執行相同的 `significant_terms` 彙總，而不使用 sampler：

```json
GET /shakespeare/_search
{
  "size": 0,
  "query": {
    "match": {
      "text_entry": "king falstaff"
    }
  },
  "aggs": {
    "plays": {
      "significant_terms": {
        "field": "play_name",
        "size": 3
      }
    }
  }
}
```
{% include copy-curl.html %}

由於僅包含 `king` 的長尾行數多於 Falstaff 的行數，最顯著的劇本是關於國王的歷史劇，例如 *Henry VI, Part 3* 和 *Richard II*。此彙總也會處理所有 1,545 份相符文件，而非 100 份：

```json
{
  ...
  "aggregations": {
    "plays": {
      "doc_count": 1545,
      "bg_count": 111396,
      "buckets": [
        {
          "key": "Henry VI Part 3",
          "doc_count": 168,
          "score": 0.31100010146873747,
          "bg_count": 3138
        },
        {
          "key": "Richard II",
          "doc_count": 143,
          "score": 0.23236659237692917,
          "bg_count": 2937
        },
        {
          "key": "Henry VI Part 2",
          "doc_count": 125,
          "score": 0.13780305490414782,
          "bg_count": 3334
        }
      ]
    }
  }
}
```

## 回應本文欄位

下表列出回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `doc_count` | 整數 | 所有分片樣本中的文件總數。 |
