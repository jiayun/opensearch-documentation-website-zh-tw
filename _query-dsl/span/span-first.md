---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Span first 查詢"
parent: Span queries
grand_parent: Query DSL
nav_order: 30
---

# Span first 查詢

`span_first` 查詢會比對從欄位開頭起始，並在指定位置數內結束的跨度 (span)。當您想找出出現在文件開頭附近的詞彙或片語時，此查詢非常實用。

例如，您可以使用 `span_first` 查詢執行下列搜尋：

- 找出特定詞彙出現在欄位開頭幾個字詞中的文件。
- 確保某些片語出現在文字的開頭或開頭附近
- 僅在模式出現在距離開頭指定距離內時進行比對

## 範例

若要嘗試本節中的範例，請先完成[設定步驟]({{site.url}}{{site.baseurl}}/query-dsl/span/#setup)。
{: .tip}

下列查詢會搜尋出現在 description 前 4 個位置內的詞幹化單字 "dress"：

```json
GET /clothing/_search
{
  "query": {
    "span_first": {
      "match": {
        "span_term": {
          "description.stemmed": "dress"
        }
      },
      "end": 4
    }
  }
}
```
{% include copy-curl.html %}

查詢比對到文件 1 和 2：
- 文件 1 和 2 在第三個位置包含 `dress` 這個字（"Long-sleeved dress..." 和 "Beautiful long dress"）。字詞的位置編號從 0 開始，因此 "dress" 位於位置 2。
- `dress` 這個字的位置必須小於 `4`，這是由 `end` 參數指定的。

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 13,
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
    "max_score": 0.110377684,
    "hits": [
      {
        "_index": "clothing",
        "_id": "1",
        "_score": 0.110377684,
        "_source": {
          "description": "Long-sleeved dress shirt with a formal collar and button cuffs. "
        }
      },
      {
        "_index": "clothing",
        "_id": "2",
        "_score": 0.110377684,
        "_source": {
          "description": "Beautiful long dress in red silk, perfect for formal events."
        }
      }
    ]
  }
}
```

</details>

`match` 參數可以包含任何類型的 span 查詢，因此可以在欄位開頭比對更複雜的模式。

## 參數

下表列出 `span_first` 查詢支援的所有頂層參數。所有參數皆為必要。

| 參數 | 資料類型 | 說明 |
|:----------|:-----|:------------|
| `match` | 物件 | 要比對的 span 查詢。這定義了您要在欄位開頭搜尋的模式。 |
| `end` | 整數 | span 查詢比對允許的最大結束位置（不含）。例如，`end: 4` 會比對位置 0--3 的詞彙。 |
