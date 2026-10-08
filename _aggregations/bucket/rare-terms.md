---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "罕見詞彙"
parent: Bucket aggregations
nav_order: 155
---

# 罕見詞彙彙總

`rare_terms` 彙總是一種桶 (bucket) 彙總，可識別資料集中不常出現的詞彙。`terms` 彙總會找出最常見的詞彙，而 `rare_terms` 彙總則相反，會找出出現頻率最低的詞彙。`rare_terms` 彙總適用於異常偵測、長尾分析和例外狀況報告等應用。

您可以使用 `terms`，並依計數遞增排序傳回的值 (`"order": {"count": "asc"}`)，藉此搜尋不常出現的值。不過，我們強烈建議您不要這麼做，因為涉及多個分片時，可能會導致結果不準確。在全域上不常出現的詞彙，在個別分片上不一定都顯得不常出現，也可能完全不在某些分片傳回的最低頻率結果中。反之，在某個分片上不常出現的詞彙，在另一個分片上可能很常見。在這兩種情況下，分片層級的彙總都可能遺漏罕見詞彙，導致整體結果不正確。我們建議您改用 `rare_terms` 彙總來取代 `terms` 彙總，因為前者是專為更準確地處理這些情況而設計。
{: .warning}

## 近似結果

若要計算 `rare_terms` 彙總的精確結果，必須彙整所有分片上的值的完整對照表，這會耗用過多的執行階段記憶體。因此，`rare_terms` 彙總的結果是近似值。

`rare_terms` 計算中的大多數錯誤都是「偽陰性」(_false negatives_) 或「遺漏」的值，這些錯誤定義了彙總偵測測試的「敏感度」(_sensitivity_)。`rare_terms` 彙總使用 CuckooFilter 演算法，在適當的敏感度與可接受的記憶體用量之間取得平衡。如需 CuckooFilter 演算法的說明，請參閱[這篇論文](https://www.cs.cmu.edu/~dga/papers/cuckoo-conext2014.pdf)。

## 控制敏感度

`rare_terms` 彙總演算法的敏感度誤差，是以遺漏的罕見值所占比例來衡量，即 `false negatives/target values`。例如，如果彙總在含有 5,000 個罕見值的資料集中遺漏了 100 個罕見值，則敏感度誤差為 `100/5000 = 0.02`，即 2%。 

您可以調整 `rare_terms` 彙總中的 `precision` 參數，以控制敏感度與記憶體用量之間的取捨。

下列因素也會影響敏感度與記憶體之間的取捨：

- 唯一值的總數
- 資料集中罕見項目所占的比例

下列準則可協助您決定要使用哪個 `precision` 值。

### 計算記憶體用量

執行階段記憶體用量以絕對值表示，通常以 MB 的 RAM 為單位。

記憶體用量會隨唯一項目的數量線性增加。視 `precision` 參數而定，線性縮放係數約為每 100 萬個唯一值 1.0 至 2.5 MB。若使用預設的 `precision` 值 `0.001`，記憶體成本約為每 100 萬個唯一值 1.75 MB。

### 管理敏感度誤差

敏感度誤差會隨唯一值的總數線性增加。如需估算唯一值數量的相關資訊，請參閱[基數彙總]({{site.url}}{{site.baseurl}}/aggregations/metric/cardinality/)。

在預設的 `precision` 下，即使資料集含有 1,000 萬至 2,000 萬個唯一值，敏感度誤差也很少超過 2.5%。若 `precision` 為 `0.00001`，敏感度誤差很少高於 0.6%。不過，罕見值的絕對數量非常少時，可能會造成誤差率大幅變動 (如果只有兩個罕見值，遺漏其中一個就會產生 50% 的誤差率)。


## 與其他彙總的相容性

`rare_terms` 彙總使用廣度優先收集模式，在某些子彙總和巢狀組態中，與需要深度優先收集模式的彙總不相容。 

如需 OpenSearch 中廣度優先搜尋的詳細資訊，請參閱[收集模式]({{site.url}}{{site.baseurl}}/aggregations/bucket/terms#collect-mode)。


## 參數

`rare_terms` 彙總接受下列參數。

| 參數             | 必要/選用 | 資料類型       | 說明 |
| :--                   | :--               | :--             | :--         |
| `field`               | 必要          | 字串          | 要分析罕見詞彙的欄位。必須是數值類型，或是具有 `keyword` 對應的文字類型。 |
| `max_doc_count`       | 選用          | 整數         | 詞彙被視為罕見所需的最大文件計數。預設值為 `1`。最大值為 `100`。 |
| `precision`           | 選用          | 整數         | 控制用於識別罕見詞彙之演算法的精確度。值越高，結果越精確，但會耗用更多記憶體。預設值為 `0.001`。最小值 (允許的最高精確度) 為 `0.00001`。 |
| `include`             | 選用          | 陣列/regex     | 要納入結果的詞彙。可以是規則運算式或值的陣列。 |
| `exclude`             | 選用          | 陣列/regex     | 要從結果中排除的詞彙。可以是規則運算式或值的陣列。 |
| `missing`             | 選用          | 字串          | 用於沒有被彙總欄位值之文件的值。 |


## 範例

下列請求會傳回 OpenSearch Dashboards 範例航班資料中只出現一次的所有目的地機場代號：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "rare_destination": {
      "rare_terms": {
        "field": "DestAirportID",
        "max_doc_count": 1
      }
    }
  }
}
```
{% include copy-curl.html %}

## 範例回應

回應顯示有兩個機場符合在資料中只出現一次的條件：

```json
{
  "took": 12,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "rare_destination": {
      "buckets": [
        {
          "key": "ADL",
          "doc_count": 1
        },
        {
          "key": "BUF",
          "doc_count": 1
        }
      ]
    }
  }
}
```


## 文件計數上限

使用 `max_doc_count` 參數指定 `rare_terms` 彙總可傳回的最大文件計數。`rare_terms` 傳回的詞彙數量沒有限制，因此較大的 `max_doc_count` 值可能會傳回非常大的結果集。因此，`100` 是允許的最大 `max_doc_count`。

下列請求會傳回 OpenSearch Dashboards 範例航班資料中最多出現兩次的所有目的地機場代號：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "rare_destination": {
      "rare_terms": {
        "field": "DestAirportID",
        "max_doc_count": 2
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示有七個目的地機場代號符合出現在兩份以下文件中的條件，其中包括上一個範例中的兩個：

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
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "rare_destination": {
      "buckets": [
        {
          "key": "ADL",
          "doc_count": 1
        },
        {
          "key": "BUF",
          "doc_count": 1
        },
        {
          "key": "ABQ",
          "doc_count": 2
        },
        {
          "key": "AUH",
          "doc_count": 2
        },
        {
          "key": "BIL",
          "doc_count": 2
        },
        {
          "key": "BWI",
          "doc_count": 2
        },
        {
          "key": "MAD",
          "doc_count": 2
        }
      ]
    }
  }
}
```


## 篩選 (include 與 exclude)

使用 `include` 和 `exclude` 參數篩選 `rare_terms` 彙總傳回的值。這兩個參數可以同時用於同一個彙總中。`exclude` 篩選條件的優先順序較高；任何被排除的值都會從結果中移除，無論這些值是否已明確納入。

`include` 和 `exclude` 的引數可以是規則運算式 (regex，包括字串常值) 或陣列。混用 regex 與陣列引數會導致錯誤。例如，不允許下列組合：

```json
"rare_terms": {
  "field": "DestAirportID",
  "max_doc_count": 2,
  "exclude": ["ABQ", "AUH"],
  "include": "A.*"
}
```


### 範例：篩選

下列範例修改了上一個範例，納入所有以「A」開頭的機場代號，但排除「ABQ」機場代號：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "rare_destination": {
      "rare_terms": {
        "field": "DestAirportID",
        "max_doc_count": 2,
        "include": "A.*",
        "exclude": "ABQ"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應顯示符合篩選要求的兩個機場代號：

```json
{
  "took": 4,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "rare_destination": {
      "buckets": [
        {
          "key": "ADL",
          "doc_count": 1
        },
        {
          "key": "AUH",
          "doc_count": 2
        }
      ]
    }
  }
}
```


### 範例：使用陣列輸入進行篩選

下列範例會傳回 OpenSearch Dashboards 範例航班資料中最多出現兩次的所有目的地機場代號，但指定了要排除的機場代號陣列：

```json
GET /opensearch_dashboards_sample_data_flights/_search
{
  "size": 0,
  "aggs": {
    "rare_destination": {
      "rare_terms": {
        "field": "DestAirportID",
        "max_doc_count": 2,
        "exclude": ["ABQ", "BIL", "MAD"]
      }
    }
  }
}
```
{% include copy-curl.html %}

回應省略了被排除的機場代號：

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
      "value": 10000,
      "relation": "gte"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "rare_destination": {
      "buckets": [
        {
          "key": "ADL",
          "doc_count": 1
        },
        {
          "key": "BUF",
          "doc_count": 1
        },
        {
          "key": "AUH",
          "doc_count": 2
        },
        {
          "key": "BWI",
          "doc_count": 2
        }
      ]
    }
  }
}
```