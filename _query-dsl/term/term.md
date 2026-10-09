---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Term
parent: Term-level queries
nav_order: 10
---

# Term 查詢

使用 `term` 查詢來搜尋欄位中的精確詞彙。例如，下列查詢會搜尋具有精確行號的一行：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "line_id": {
        "value": "61809"
      }
    }
  }
}
```
{% include copy-curl.html %}

當文件被編製索引時，`text` 欄位會經過[分析]({{site.url}}{{site.baseurl}}/analyzers/index/)。分析包括對文字進行斷詞、轉為小寫以及移除標點符號。與會分析查詢文字的 `match` 查詢不同，`term` 查詢只會比對精確的詞彙，因此可能不會傳回相關的結果。請避免在 `text` 欄位上使用 `term` 查詢。如需更多資訊，請參閱[詞彙層級查詢與全文查詢的比較]({{site.url}}{{site.baseurl}}/query-dsl/term-vs-full-text/)。

您可以在 `case_insensitive` 參數中指定查詢不區分大小寫：

```json
GET shakespeare/_search
{
  "query": {
    "term": {
      "speaker": {
        "value": "HAMLET",
        "case_insensitive": true
      }
    }
  }
}
```
{% include copy-curl.html %}

在 OpenSearch 2.x 及更早的版本中，複雜度可能會隨著字元數量呈指數級增加，導致堆積記憶體使用量偏高並降低效能。為避免此情況，請勿使用不區分大小寫的搜尋。改為在已編製索引欄位的分析器中套用[lowercase 詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/lowercase/)，並使用小寫的查詢詞彙。
{: .warning}

回應會包含符合的文件，即使大小寫有所差異：

```json
"hits": {
  "total": {
    "value": 1582,
    "relation": "eq"
  },
  "max_score": 2,
  "hits": [
    {
      "_index": "shakespeare",
      "_id": "32700",
      "_score": 2,
      "_source": {
        "type": "line",
        "line_id": 32701,
        "play_name": "Hamlet",
        "speech_number": 9,
        "line_number": "1.2.66",
        "speaker": "HAMLET",
        "text_entry": "[Aside]  A little more than kin, and less than kind."
      }
    },
  ...
}
```

## 參數

此查詢接受欄位名稱 (`<field>`) 作為頂層參數：

```json
GET _search
{
  "query": {
    "term": {
      "<field>": {
        "value": "sample",
        ...
      }
    }
  }
}
```
{% include copy-curl.html %}

`<field>` 接受下列參數。除了 `value` 以外，所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`value` | 字串 | 要在 `<field>` 所指定欄位中搜尋的詞彙。只有當文件的欄位值與該詞彙完全相符（包括正確的空格與大小寫）時，該文件才會出現在結果中。
`boost` | 浮點數 | 一個浮點數值，用於指定此欄位對相關性分數的權重。高於 1.0 的值會提高該欄位的相關性；介於 0.0 與 1.0 之間的值會降低該欄位的相關性。預設為 1.0。
`_name` | 字串 | 用於查詢標記的查詢名稱。選用。
`case_insensitive` | 布林值 | 若為 `true`，允許該值與已編製索引的欄位值進行不區分大小寫的比對。預設為 `false`（是否區分大小寫由該欄位的對應決定）。
