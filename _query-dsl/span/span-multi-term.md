---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Span multi-term
parent: Span queries
grand_parent: Query DSL
nav_order: 40
---

# Span multi-term 查詢

`span_multi` 查詢可讓您將多詞彙查詢 (例如 `wildcard`、`fuzzy`、`prefix`、`range` 或 `regexp`) 包裝為 span 查詢。這可讓您在其他 span 查詢中使用這些更有彈性的比對查詢。

例如，您可以使用 `span_multi` 查詢來：
- 尋找與其他詞彙鄰近且具有共同前置字元的詞彙。
- 在 span 內比對詞彙的模糊變化。
- 在 span 查詢中使用規則運算式。

>`span_multi` 查詢可能比對到許多詞彙。為避免過度使用記憶體，您可以：
>- 為多詞彙查詢設定 `rewrite` 參數。
>- 使用 `top_terms_*` 重寫方法。
>- 若您僅將 `span_multi` 用於 `prefix` 查詢，請考慮為文字欄位啟用 `index_prefixes` 選項。這會自動將該欄位上的任何 `prefix` 查詢重寫為符合已編製索引前置字元的單一詞彙查詢。
{: .note}

## 範例

若要試用本節的範例，請完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/index/#setup)。
{: .tip}

`span_multi` 查詢使用下列語法來包裝 `prefix` 查詢：

```json
"span_multi": {
  "match": {
    "prefix": {
      "description": {
        "value": "flutter"
      }
    }
  }
}
```

下列查詢會搜尋以「dress」開頭的詞彙，以及任何形式的「sleeve」，且兩者相距最多 5 個詞彙：

```json
GET /clothing/_search
{
  "query": {
    "span_near": {
      "clauses": [
        {
          "span_multi": {
            "match": {
              "prefix": {
                "description": {
                  "value": "dress"
                }
              }
            }
          }
        },
        {
          "field_masking_span": {
            "query": {
              "span_term": {
                "description.stemmed": "sleev"
              }
            },
            "field": "description"
          }
        }
      ],
      "slop": 5,
      "in_order": false
    }
  }
}
```
{% include copy-curl.html %}

此查詢會比對文件 1 (「Long-sleeved dress...」) 和文件 4 (「...dresses with long fluttered sleeves...」)，因為「dress」和「long」在兩份文件中都出現在最大距離內。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 5,
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
    "max_score": 1.7590723,
    "hits": [
      {
        "_index": "clothing",
        "_id": "1",
        "_score": 1.7590723,
        "_source": {
          "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
        }
      },
      {
        "_index": "clothing",
        "_id": "4",
        "_score": 0.84792376,
        "_source": {
          "description": "A set of two midi silk shirt dresses with long fluttered sleeves in black. "
        }
      }
    ]
  }
}
```
</details>

## 參數

下表列出 `span_multi` 查詢支援的所有最上層參數。所有參數皆為必要。

| 參數 | 資料類型 | 說明 |
|:----------|:-----|:------------|
| `match` | 物件 | 要包裝的多詞彙查詢 (可為 `prefix`、`wildcard`、`fuzzy`、`range` 或 `regexp`)。 |
