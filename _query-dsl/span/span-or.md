---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Span or
parent: Span queries
grand_parent: Query DSL
nav_order: 70
---

# Span or 查詢

`span_or` 查詢會結合多個 span 查詢，並比對其跨度的聯集。只要其中至少一個 span 查詢符合，就會產生相符結果。

例如，您可以使用 `span_or` 查詢來：
- 尋找符合多種模式中任一模式的跨度。
- 結合不同的跨度模式，作為替代選項。
- 在單一查詢中比對多種跨度變化。

## 範例

若要試用本節的範例，請完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

下列查詢會搜尋「formal collar」或「button collar」，其中兩個詞彼此相距不超過 2 個字詞：

```json
GET /clothing/_search
{
  "query": {
    "span_or": {
      "clauses": [
        {
          "span_near": {
            "clauses": [
              {
                "span_term": {
                  "description": "formal"
                }
              },
              {
                "span_term": {
                  "description": "collar"
                }
              }
            ],
            "slop": 0,
            "in_order": true
          }
        },
        {
          "span_near": {
            "clauses": [
              {
                "span_term": {
                  "description": "button"
                }
              },
              {
                "span_term": {
                  "description": "collar"
                }
              }
            ],
            "slop": 2,
            "in_order": true
          }
        }
      ]
    }
  }
}
```
{% include copy-curl.html %}

此查詢會比對到文件 1（「...formal collar...」）和文件 3（「...button-down collar...」），兩者均在指定的 slop 距離內。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 2.170027,
    "hits": [
      {
        "_index": "clothing",
        "_id": "1",
        "_score": 2.170027,
        "_source": {
          "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
        }
      },
      {
        "_index": "clothing",
        "_id": "3",
        "_score": 1.2509141,
        "_source": {
          "description": "Short-sleeved shirt with a button-down collar, can be dressed up or down."
        }
      }
    ]
  }
}
```
</details>

## 參數

下表列出 `span_or` 查詢支援的所有最上層參數。

| 參數 | 資料類型 | 說明 |
|:----------|:-----|:------------|
| `clauses` | 陣列 | 要比對的 span 查詢陣列。只要其中任一 span 查詢符合，此查詢就會符合。必須包含至少一個 span 查詢。必要。 |
