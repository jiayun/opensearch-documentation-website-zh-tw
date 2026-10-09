---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "萬用字元"
parent: Term-level queries
nav_order: 90
---

# 萬用字元查詢

使用萬用字元查詢來搜尋符合萬用字元模式的詞彙。萬用字元查詢支援下列運算子。

運算子 | 說明
:--- | :---
`*` | 符合零個或多個字元。
`?` | 符合任何單一字元。
`case_insensitive` | 若為 `true`，萬用字元查詢不區分大小寫。若為 `false`，萬用字元查詢區分大小寫。預設為 `false`（區分大小寫）。

若要區分大小寫地搜尋以 `H` 開頭並以 `Y` 結尾的詞彙，請使用下列請求：

```json
GET shakespeare/_search
{
  "query": {
    "wildcard": {
      "speaker": {
        "value": "H*Y",
        "case_insensitive": false
      }
    }
  }
}
```
{% include copy-curl.html %}

如果您將 `*` 改為 `?`，將不會有任何符合結果，因為 `?` 代表單一字元。

萬用字元查詢通常較慢，因為需要迭代大量詞彙。請避免將萬用字元放在查詢的開頭，因為這在資源和時間上都可能是非常昂貴的操作。

[wildcard 欄位類型]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/)會建立一個專門設計為對萬用字元與正規表示式查詢非常有效率的索引。

## 參數

此查詢接受欄位名稱（`<field>`）作為頂層參數：

```json
GET _search
{
  "query": {
    "wildcard": {
      "<field>": {
        "value": "patt*rn",
        ...
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除 `value` 以外的所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`value` | 字串 | 用於比對 `<field>` 所指定欄位中詞彙的萬用字元模式。
`boost` | 浮點數 | 一個浮點數值，指定此欄位對相關性分數的權重。高於 1.0 的值會提高該欄位的相關性；介於 0.0 與 1.0 之間的值會降低該欄位的相關性。預設為 1.0。
`case_insensitive` | 布林值 | 若為 `true`，允許以不區分大小寫的方式比對該值與已編製索引的欄位值。預設為 `false`（是否區分大小寫由欄位的對應決定）。
`rewrite` | 字串 | 決定 OpenSearch 如何改寫與評分多重詞彙查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 與 `top_terms_blended_freqs_N`。預設為 `constant_score`。

若 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/#expensive-queries) 設定為 `false`，則不會執行萬用字元查詢。
{: .important}
