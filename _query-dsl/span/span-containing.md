---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "跨度包含查詢"
parent: Span queries
grand_parent: Query DSL
nav_order: 10
---

# 跨度包含查詢

`span_containing` 查詢會找出較大文字模式 (例如片語或一組詞彙) 在其邊界內包含較小文字模式的比對結果。您可以將它想成尋找某個詞彙或片語，但只有在它出現於特定較大上下文中時才會找到。

例如，您可以使用 `span_containing` 查詢執行以下搜尋：

- 尋找「quick」一詞，但只有在它出現於同時提及狐狸和行為的句子中時。
- 確保特定詞彙出現在其他詞彙的上下文中---而不是在文件的任何地方。
- 搜尋出現在較大有意義片語中的特定詞彙。

## 範例

若要嘗試本節中的範例，請完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

以下查詢會搜尋 "red" 一詞的出現位置，該詞必須出現在包含 "silk" 和 "dress" (順序不限) 且兩者相距 5 個詞以內的較大跨度中：

```json
GET /clothing/_search
{
  "query": {
    "span_containing": {
      "little": {
        "span_term": {
          "description": "red"
        }
      },
      "big": {
        "span_near": {
          "clauses": [
            {
              "span_term": {
                "description": "silk"
              }
            },
            {
              "span_term": {
                "description": "dress"
              }
            }
          ],
          "slop": 5,
          "in_order": false
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢比對文件 1，因為：

- 它找到一個跨度，其中 "silk" 和 "dress" 彼此相距最多 5 個詞 ("...dress in red silk...")。"silk" 和 "dress" 兩詞彼此相距 2 個詞 (中間有 2 個詞)。
- 在這個較大跨度中，它找到 "red" 一詞。

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
      "value": 1,
      "relation": "eq"
    },
    "max_score": 1.1577396,
    "hits": [
      {
        "_index": "clothing",
        "_id": "2",
        "_score": 1.1577396,
        "_source": {
          "description": "Beautiful long dress in red silk, perfect for formal events."
        }
      }
    ]
  }
}
```

</details>

`little` 和 `big` 兩個參數都可以包含任何類型的 span 查詢，必要時可組成複雜的巢狀 span 查詢。

## 參數

下表列出 `span_containing` 查詢支援的所有頂層參數。所有參數皆為必要。

| 參數 | 資料類型 | 描述 |
|:-----------|:------|:-------------|
| `little` | 物件 | 必須包含在 `big` 跨度內的 span 查詢。這定義了您在較大上下文中要搜尋的跨度。 |
| `big` | 物件 | 定義邊界的包含 span 查詢，`little` 跨度必須出現在該邊界內。這為您的搜尋建立上下文。 |