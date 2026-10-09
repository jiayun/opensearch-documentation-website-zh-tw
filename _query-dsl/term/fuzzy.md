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

查詢接受欄位名稱（`<field>`）作為頂層參數：

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

`<field>` 接受下列參數。除 `value` 以外，所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`value` | 字串 | 要在 `<field>` 所指定欄位中搜尋的詞彙。
`boost` | 浮點數 | 指定此欄位對相關性分數權重的浮點數值。高於 1.0 的值會提高該欄位的相關性；介於 0.0 與 1.0 之間的值會降低該欄位的相關性。預設為 1.0。
`fuzziness` | `AUTO`、`0` 或正整數 | 在判斷詞彙是否符合某個值時，將一個單字變更為另一個單字所需的字元編輯次數（插入、刪除、替換）。例如，`wined` 與 `wind` 之間的距離為 1。預設值 `AUTO` 會根據搜尋詞彙的長度動態選取編輯距離。您可以使用 `AUTO:[low],[high]` 語法自訂門檻，其中 `low` 和 `high` 定義字元長度邊界。若省略，OpenSearch 會使用 `AUTO:3,6` 作為預設值，並套用下列規則：<br>- 包含 0--2 個字元的詞彙：需要完全相符（0 次編輯）。<br>- 包含 3--5 個字元的詞彙：允許最多 1 次編輯。<br>- 包含 6 個以上字元的詞彙：允許最多 2 次編輯。<br>例如，`AUTO:4,7` 要求包含 0--3 個字元的詞彙必須完全相符，包含 4--6 個字元的詞彙允許最多 1 次編輯，包含 7 個以上字元的詞彙允許最多 2 次編輯。大多數情境建議使用 `AUTO`。
`max_expansions` | 正整數 | 查詢可展開的最大詞彙數量。模糊查詢會「展開至」多個在 `fuzziness` 所指定距離內的相符詞彙，然後 OpenSearch 會嘗試比對這些詞彙。預設為 `50`。
`prefix_length` | 非負整數 | 不納入模糊比對考量的前置字元數量。預設為 `0`。
`rewrite` | 字串 | 決定 OpenSearch 如何改寫多詞彙查詢並計分。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。預設為 `constant_score`。
`transpositions` | 布林值 | 指定是否允許將兩個相鄰字元的交換（`ab` 變成 `ba`）視為一次編輯。預設為 `true`。

在 `max_expansions` 中指定過大的值可能導致效能不佳，尤其是當 `prefix_length` 設為 `0` 時，因為 OpenSearch 會嘗試比對該單字的大量變化形式。
{: .warning}

如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `false`，則不會執行模糊查詢。
{: .important}
