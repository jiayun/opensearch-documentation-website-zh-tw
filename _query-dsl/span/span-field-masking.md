---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Span 欄位遮罩"
parent: Span queries
grand_parent: Query DSL
nav_order: 20
---

# Span 欄位遮罩查詢

`field_masking_span` 查詢允許 span 查詢透過「遮罩」查詢的真實欄位，在不同欄位之間進行比對。當您處理多重欄位（相同內容以不同分析器編製索引）時，或當您需要在不同欄位之間執行 `span_near` 或 `span_or` 這類 span 查詢（這通常是不允許的）時，這特別有用。

舉例來說，您可以使用 `field_masking_span` 查詢來：
- 在原始欄位及其詞幹化版本之間比對詞彙。
- 在單一 span 操作中合併不同欄位上的 span 查詢。
- 處理以不同分析器編製索引的相同內容。

使用欄位遮罩時，相關性分數是使用被遮罩欄位的特性（norms）計算，而非實際搜尋的欄位。這表示如果被遮罩欄位的屬性（例如長度或 boost 值）與實際搜尋的欄位不同，您可能會得到非預期的評分結果。
{: .note}

## 範例

若要試用本節的範例，請完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

下列查詢會搜尋原始欄位中的「long」，以及詞幹化欄位中鄰近的「sleeve」變化形式：

```json
GET /clothing/_search
{
  "query": {
    "span_near": {
      "clauses": [
        {
          "span_term": {
            "description": "long"
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
      "slop": 1,
      "in_order": true
    }
  }
}

```
{% include copy-curl.html %}

此查詢會比對文件 1 和 4：
- 「long」這個詞彙同時出現在兩份文件的 `description` 欄位中。
- 文件 1 包含「sleeved」這個字，文件 4 包含「sleeves」這個字。
- `field_masking_span` 讓詞幹化欄位的比對結果看起來像是在原始欄位中。
- 這些詞彙出現在彼此相距 1 個位置內，且順序符合指定（「long」必須出現在「sleeve」之前）。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 7,
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
    "max_score": 0.7444251,
    "hits": [
      {
        "_index": "clothing",
        "_id": "1",
        "_score": 0.7444251,
        "_source": {
          "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
        }
      },
      {
        "_index": "clothing",
        "_id": "4",
        "_score": 0.4291246,
        "_source": {
          "description": "A set of two midi silk shirt dresses with long fluttered sleeves in black. "
        }
      }
    ]
  }
}
```

## 參數

下表列出 `field_masking_span` 查詢支援的所有最上層參數。所有參數皆為必要。

| 參數 | 資料類型 | 說明 |
|:----------|:-----|:------------|
| `query` | 物件 | 要在實際欄位上執行的 span 查詢。 |
| `field` | 字串 | 用來遮罩查詢的欄位名稱。其他 span 查詢會將此查詢視為在此欄位上執行。 |
