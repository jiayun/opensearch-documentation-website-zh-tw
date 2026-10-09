---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "字串欄位類型"
nav_order: 20
has_children: true
has_toc: false
parent: Supported field types
redirect_from:
  - /field-types/supported-field-types/string/
  - /opensearch/supported-field-types/string/
  - /field-types/string/
---

# 字串欄位類型

字串欄位類型包含文字值或由文字衍生的值。下表列出 OpenSearch 支援的所有字串欄位類型。

欄位資料類型 | 描述
:--- | :---
[`text`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/text/) | 經過分析的字串。適用於全文搜尋。
[`keyword`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/keyword/) | 未經分析的字串。適用於精確值搜尋。
[`match_only_text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/match-only-text/) | `text` 欄位的節省空間版本。
[`wildcard`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/wildcard/)  | `keyword` 的變體，具備高效率的子字串與規則運算式比對。
[`token_count`]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/token-count/)  | 計算字串中的詞元數量。
[`constant_keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/constant-keyword/)  | 類似於 `keyword`，但對所有文件使用單一值。
