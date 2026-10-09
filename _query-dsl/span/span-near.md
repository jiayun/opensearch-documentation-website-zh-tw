---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Span near 查詢"
parent: Span queries
grand_parent: Query DSL
nav_order: 50
---

# Span near 查詢

`span_near` 查詢會比對彼此相近的跨度 (span)。您可以指定跨度之間允許的距離，以及它們是否需要以特定順序出現。

例如，您可以使用 `span_near` 查詢來：
- 尋找彼此在特定距離內出現的詞彙。
- 比對單字以特定順序出現的片語。
- 尋找在文字中彼此相近出現的相關概念。

## 範例

若要嘗試本節中的範例，請先完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

下列查詢會搜尋以任意順序彼此接近的「sleeve」與「long」的各種詞形：

```json
GET /clothing/_search
{
  "query": {
    "span_near": {
      "clauses": [
        {
          "span_term": {
            "description.stemmed": "sleev"
          }
        },
        {
          "span_term": {
            "description.stemmed": "long"
          }
        }
      ],
      "slop": 1,
      "in_order": false
    }
  }
}
```
{% include copy-curl.html %}

此查詢會比對文件 1（「Long-sleeved...」）與文件 2（「...long fluttered sleeves...」）。在文件 1 中，這些單字彼此相鄰；而在文件 2 中，它們位於指定的 slop 距離 `1` 之內（兩者之間有 1 個單字）。

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
      "value": 2,
      "relation": "eq"
    },
    "max_score": 0.36496973,
    "hits": [
      {
        "_index": "clothing",
        "_id": "1",
        "_score": 0.36496973,
        "_source": {
          "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
        }
      },
      {
        "_index": "clothing",
        "_id": "4",
        "_score": 0.25312424,
        "_source": {
          "description": "A set of two midi silk shirt dresses with long fluttered sleeves in black. "
        }
      }
    ]
  }
}
```

## 參數

下表列出 `span_near` 查詢支援的所有頂層參數。

| 參數 | 資料類型 | 說明 | 
|:----------|:-----|:------------|
| `clauses` | 由跨度查詢組成的陣列，定義要比對的詞彙或片語。所有指定的詞彙都必須出現在定義的 slop 距離內。必要。 |
| `slop` | 整數 | 跨度之間未比對位置的最大數量。必要。 |
| `in_order` | 布林值 | 跨度是否需要以與 `clauses` 陣列相同的順序出現。選用。預設為 `false`。 |
