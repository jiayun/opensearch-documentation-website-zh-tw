---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "詞彙層級查詢"
has_children: true
has_toc: false
nav_order: 40
redirect_from:
  - /opensearch/query-dsl/term/
  - /query-dsl/term/
---

# 詞彙層級查詢

詞彙層級查詢會在索引中搜尋包含精確搜尋詞彙的文件。詞彙層級查詢所回傳的文件不會依相關性分數排序。

處理文字資料時，請僅對對應為 `keyword` 的欄位使用詞彙層級查詢。

詞彙層級查詢不適合搜尋經過分析的文字欄位。若要回傳經過分析的欄位，請使用[全文查詢]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/)。

## 詞彙層級查詢類型

下表列出所有詞彙層級查詢類型。

查詢類型 | 說明
:--- | :--- 
[`term`]({{site.url}}{{site.baseurl}}/query-dsl/term/term/) | 搜尋在特定欄位中包含精確詞彙的文件。
[`terms`]({{site.url}}{{site.baseurl}}/query-dsl/term/terms/) | 搜尋在特定欄位中包含一或多個詞彙的文件。
[`terms_set`]({{site.url}}{{site.baseurl}}/query-dsl/term/terms-set/) | 搜尋在特定欄位中符合最少詞彙數量的文件。
[`ids`]({{site.url}}{{site.baseurl}}/query-dsl/term/ids/) | 依文件 ID 搜尋文件。
[`range`]({{site.url}}{{site.baseurl}}/query-dsl/term/range/) | 搜尋欄位值在特定範圍內的文件。
[`prefix`]({{site.url}}{{site.baseurl}}/query-dsl/term/prefix/) | 搜尋包含以特定字首開頭之詞彙的文件。
[`exists`]({{site.url}}{{site.baseurl}}/query-dsl/term/exists/) | 搜尋在特定欄位中具有任何已編製索引值的文件。
[`fuzzy`]({{site.url}}{{site.baseurl}}/query-dsl/term/fuzzy/) | 搜尋包含在允許的最大 [Damerau–Levenshtein 距離](https://en.wikipedia.org/wiki/Damerau–Levenshtein_distance)內與搜尋詞彙相似之詞彙的文件。Damerau–Levenshtein 距離衡量將一個詞彙變更為另一個詞彙所需的單一字元變更次數。
[`wildcard`]({{site.url}}{{site.baseurl}}/query-dsl/term/wildcard/) | 搜尋包含符合萬用字元模式之詞彙的文件。
[`regexp`]({{site.url}}{{site.baseurl}}/query-dsl/term/regexp/) | 搜尋包含符合正規表示式之詞彙的文件。
