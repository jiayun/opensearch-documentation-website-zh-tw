---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "前綴"
parent: Term-level queries
nav_order: 60
---

# 前綴查詢

使用 `prefix` 查詢來搜尋以特定前綴開頭的詞彙。例如，下列查詢會搜尋 `speaker` 欄位包含以 `KING H` 開頭之詞彙的文件：

```json
GET shakespeare/_search
{
  "query": {
    "prefix": {
      "speaker": "KING H"
    }
  }
}
```
{% include copy-curl.html %}

若要提供參數，您可以使用與前述查詢等效的查詢，並採用下列擴充語法：

```json
GET shakespeare/_search
{
  "query": {
    "prefix": {
      "speaker": {
        "value": "KING H"
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
    "prefix": {
      "<field>": {
        "value": "sample",
        ...
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除了 `value` 之外，所有參數都是選用的。

參數 | 資料類型 | 說明
:--- | :--- | :---
`value` | 字串 | 要在 `<field>` 中指定之欄位裡搜尋的詞彙。
`boost` | 浮點數 | 浮點數值，指定此欄位對相關性分數的權重。大於 1.0 的值會提高欄位的相關性。介於 0.0 與 1.0 之間的值會降低欄位的相關性。預設為 1.0。
`case_insensitive` | 布林值 | 若為 `true`，則允許值與已編製索引的欄位值進行不區分大小寫的比對。預設為 `false`（大小寫敏感度取決於欄位的對應）。
`rewrite` | 字串 | 決定 OpenSearch 如何改寫及評分多詞彙查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 及 `top_terms_blended_freqs_N`。預設為 `constant_score`。

如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `false`，則不會執行前綴查詢。如果啟用 `index_prefixes`，則會忽略 `search.allow_expensive_queries` 設定，並建構及執行最佳化查詢。
{: .important}
