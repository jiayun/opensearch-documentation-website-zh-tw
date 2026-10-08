---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "分析器"
nav_order: 40
has_children: true
has_toc: false
redirect_from:
    - /analyzers/supported-analyzers/
---

# 分析器

分析器會在編製索引和搜尋期間將文字轉換為詞元。OpenSearch 為常見使用案例提供內建分析器，並支援結合字元篩選器、斷詞器和詞元篩選器的自訂分析器。

## 內建分析器

下表列出 OpenSearch 提供的內建分析器。表格的最後一欄包含將分析器套用至字串 `It’s fun to contribute a brand-new PR or 2 to OpenSearch!` 的結果。

分析器 | 執行的分析 | 分析器輸出 
:--- | :--- | :---
[**Standard**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/standard/)（預設） | - 在字詞邊界將字串剖析為詞元 <br> - 移除大部分標點符號 <br> - 將詞元轉換為小寫 | [`it’s`, `fun`, `to`, `contribute`, `a`,`brand`, `new`, `pr`, `or`, `2`, `to`, `opensearch`]
[**Simple**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/simple/) | - 在任何非字母字元處將字串剖析為詞元 <br> - 移除非字母字元 <br> - 將詞元轉換為小寫  | [`it`, `s`, `fun`, `to`, `contribute`, `a`,`brand`, `new`, `pr`, `or`, `to`, `opensearch`]
[**White space**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/whitespace/) | - 在空白字元處將字串剖析為詞元 | [`It’s`, `fun`, `to`, `contribute`, `a`,`brand-new`, `PR`, `or`, `2`, `to`, `OpenSearch!`]
[**Stop**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/stop/) | - 在任何非字母字元處將字串剖析為詞元 <br> - 移除非字母字元 <br> - 移除停用詞 <br> - 將詞元轉換為小寫 | [`s`, `fun`, `contribute`, `brand`, `new`, `pr`, `opensearch`]
[**Keyword**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/keyword/)（不執行任何操作） | - 原封不動地輸出整個字串 | [`It’s fun to contribute a brand-new PR or 2 to OpenSearch!`]
[**Pattern**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/pattern/)| - 使用規則運算式將字串剖析為詞元 <br> - 支援將字串轉換為小寫 <br> - 支援移除停用詞 | [`it`, `s`, `fun`, `to`, `contribute`, `a`,`brand`, `new`, `pr`, `or`, `2`, `to`, `opensearch`]
[**Language**]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/index/) | 執行特定語言專屬的分析（例如 `english`）。 | [`fun`, `contribut`, `brand`, `new`, `pr`, `2`, `opensearch`]
[**Fingerprint**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/fingerprint/) | - 在任何非字母字元處剖析字串 <br> - 將字元轉換為 ASCII 以進行正規化 <br> - 將詞元轉換為小寫 <br> - 將詞元排序、去除重複並串連成單一詞元 <br> - 支援移除停用詞 | [`2 a brand contribute fun it's new opensearch or pr to`] <br> 請注意，撇號已轉換為對應的 ASCII 字元。
[**DL model**]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/dl-model-analyzers/) | 使用 ML 模型斷詞規則進行[神經稀疏搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/neural-sparse-search/)。 | 以模型為基礎的詞元

## 語言分析器

OpenSearch 支援多種語言分析器。如需詳細資訊，請參閱[語言分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/index/)。

## 其他分析器

下表列出 OpenSearch 支援的其他分析器。

| 分析器       | 執行的分析                                                                                       |
|:---------------|:---------------------------------------------------------------------------------------------------------|
| [`phone`]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/phone-analyzers/#the-phone-analyzer)       | 用於剖析電話號碼的[索引分析器]({{site.url}}{{site.baseurl}}/analyzers/index-analyzers/)。  |
| [`phone-search`]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/phone-analyzers/#the-phone-search-analyzer) | 用於剖析電話號碼的[搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)。 |

