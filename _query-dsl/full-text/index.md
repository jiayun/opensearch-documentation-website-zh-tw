---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "全文查詢"
has_children: true
has_toc: false
nav_order: 30
redirect_from:
  - /opensearch/query-dsl/full-text/
  - /opensearch/query-dsl/full-text/index/
  - /query-dsl/query-dsl/full-text/
  - /query-dsl/full-text/
---

# 全文查詢

全文查詢會在搜尋前先分析查詢字串，因此適合對文字欄位進行自然語言搜尋。有許多選用欄位可用來建立細緻的搜尋行為，因此我們建議您先針對具代表性的索引測試一些基本查詢類型並驗證輸出，再使用多個選項執行更進階或更複雜的搜尋。

OpenSearch 使用 Apache Lucene 搜尋程式庫，為資料匯入、編製索引、搜尋與彙總提供高效的資料結構與演算法。

若要進一步了解搜尋查詢類別，請參閱 [Lucene 查詢的 JavaDoc 文件](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/search/Query.html)。

本節所示的全文查詢類型皆使用標準分析器，會在提交查詢時自動分析文字。

下表列出所有全文查詢類型。

查詢類型 | 說明
:--- | :---
[`match`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/) | 預設的全文查詢，可用於模糊比對以及詞組或鄰近搜尋。
[`match_phrase`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/) | 類似 `match` 查詢，但會比對整個詞組，並允許設定的 slop。
[`match_phrase_prefix`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase-prefix/) | 類似 `match_phrase` 查詢，但會將詞彙作為整個詞組比對，並將最後一個詞彙視為字首。
[`match_bool_prefix`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-bool-prefix/) | 建立 [布林查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/)，比對任意位置的所有詞彙，並將最後一個詞彙視為字首。
[`multi_match`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/) | 類似 `match` 查詢，但用於多個欄位。
[`combined_fields`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/combined-fields/) | 將多個文字欄位視為單一欄位，以使用 BM25F 取得更好的相關性分數。
[`simple_query_string`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/simple-query-string/) | `query_string` 查詢的較簡單、較寬鬆版本。
[`query_string`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/) | 使用嚴格語法在單一查詢字串中指定布林條件與多欄位搜尋。
[`intervals`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/intervals/) | 允許對比對詞彙的鄰近性與順序進行細緻控制。 
