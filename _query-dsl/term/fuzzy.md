---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "模糊查詢"
parent: Term-level queries
nav_order: 80
---

# 模糊查詢

模糊查詢會搜尋包含與搜尋詞彙相似、且在允許的最大 [Damerau–Levenshtein 距離](https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance)範圍內之詞元的文件。Damerau–Levenshtein 距離衡量將一個詞元變更為另一個詞元所需的單一字元變更次數。這些變更包括：

- 替換：**c**at 變成 **b**at
- 插入：cat 變成 cat**s**
- 刪除：**c**at 變成 at
- 交換：**ca**t 變成 **ac**t

模糊查詢會建立一份清單，列出在 Damerau-Levenshtein 距離範圍內搜尋詞彙的所有可能展開形式。您可以在 `max_expansions` 欄位中指定此類展開形式的最大數量。查詢接著會搜尋符合任何展開形式的文件。如果您將 `transpositions` 參數設為 `false`，則您的搜尋將使用經典的 [Levenshtein 距離](https://en.wikipedia.org/wiki/Levenshtein_distance)。 

以下範例查詢搜尋講者 `HALET`（`HAMLET` 的誤拼）。由於未指定最大編輯距離，因此使用預設的 `AUTO` 編輯距離：

```json
GET shakespeare/_search
{
  "query": {
    "fuzzy": {
      "speaker": {
        "value": "HALET"
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含所有 `HAMLET` 為講者的文件。

以下範例查詢使用進階參數搜尋單字 `HALET`：

```json
GET shakespeare/_search
{
  "query": {
    "fuzzy": {
      "speaker": {
        "value": "HALET",
        "fuzziness": "2",
        "max_expansions": 40,
        "prefix_length": 0,
        "transpositions": true,
        "rewrite": "constant_score"
      }
    }
  }
}
```
{% include copy-curl.html %}

## 參數

此查詢接受欄位名稱（`<field>`）作為最上層參數：

```json
GET _search
{
  "query": {
    "fuzzy": {
      "<field>": {
        "value": "sample",
        ...
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除了 `value` 之外，所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`value` | 字串 | 要在 `<field>` 所指定的欄位中搜尋的詞彙。
`boost` | 浮點數 | 指定此欄位對相關性分數之權重的浮點數值。大於 1.0 的值會提高此欄位的相關性。介於 0.0 與 1.0 之間的值會降低此欄位的相關性。預設為 1.0。
`fuzziness` | `AUTO`、`0` 或正整數 | 比對詞彙時允許的編輯次數上限，指定為 `0`、`1`、`2`、`AUTO` 或 `AUTO:<low>,<high>`。預設為 `AUTO`。如需詳細資訊，請參閱[模糊程度]({{site.url}}{{site.baseurl}}/query-dsl/fuzziness/)。
`max_expansions` | 正整數 |  查詢可擴展的詞彙數量上限。模糊查詢會「擴展為」多個符合的詞彙，這些詞彙都在 `fuzziness` 所指定的距離範圍內。接著，OpenSearch 會嘗試比對這些詞彙。預設為 `50`。
`prefix_length` | 非負整數 | 不納入模糊比對考量的開頭字元數。預設為 `0`。
`rewrite` | 字串 | 決定 OpenSearch 如何改寫多詞彙查詢並評分。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。預設為 `constant_score`。
`transpositions` | 布林值 | 指定是否允許將兩個相鄰字元互換（`ab` 變為 `ba`）視為一次編輯。預設為 `true`。

在 `max_expansions` 中指定較大的值可能導致效能不佳，尤其是當 `prefix_length` 設為 `0` 時，因為 OpenSearch 會嘗試比對該單字的大量變體。
{: .warning}

如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `false`，則不會執行模糊查詢。
{: .important}
