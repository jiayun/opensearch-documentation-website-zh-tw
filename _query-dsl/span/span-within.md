---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Span within 查詢"
parent: Span queries
grand_parent: Query DSL
nav_order: 90
---

# Span within 查詢

`span_within` 查詢會比對被另一個 span 查詢所包圍的 span。它與 [`span_containing`]({{site.url}}{{site.baseurl}}/query-dsl/span/span-containing/) 相反：`span_containing` 會傳回包含較小 span 的較大 span，而 `span_within` 則會傳回被較大 span 包圍的較小 span。

例如，您可以使用 `span_within` 查詢來：
- 尋找出現在較長片語內的較短片語。
- 比對出現在特定情境內的詞彙。
- 找出被較大模式包圍的較小模式。

## 範例

若要試用本節的範例，請完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

下列查詢會搜尋 "dress" 這個字，當它出現在包含 "shirt" 與 "long" 的 span 內時：

```json
GET /clothing/_search
{
  "query": {
    "span_within": {
      "little": {
        "span_term": {
          "description": "dress"
        }
      },
      "big": {
        "span_near": {
          "clauses": [
            {
              "span_term": {
                "description": "shirt"
              }
            },
            {
              "span_term": {
                "description": "long"
              }
            }
          ],
          "slop": 2,
          "in_order": false
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢會比對文件 1，因為：
- "dress" 這個字出現在較大的 span 內（"Long-sleeved dress shirt..."）。
- 較大的 span 包含 "shirt" 與 "long"，且兩者相距 2 個字以內（它們之間有 2 個字）。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 3,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.4677674,
    "hits": [
      {
        "_index": "clothing",
        "_id": "1",
        "_score": 1.4677674,
        "_source": {
          "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
        }
      }
    ]
  }
}
```
</details>

## 參數

下表列出 `span_within` 查詢支援的所有最上層參數。所有參數皆為必要。

| 參數 | 資料類型 | 說明 |
|:----------|:-----|:------------|
| `little` | 物件 | 必須包含在 `big` span 內的 span 查詢。這會定義您在較大情境中搜尋的 span。 |
| `big` | 物件 | 定義 `little` span 必須出現之範圍的包含 span 查詢。這會為您的搜尋建立情境。 |