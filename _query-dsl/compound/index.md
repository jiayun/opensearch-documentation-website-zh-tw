---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複合查詢"
has_children: true
has_toc: false
nav_order: 50
redirect_from:
  - /opensearch/query-dsl/compound/index/
  - /query-dsl/query-dsl/compound/
  - /query-dsl/compound/
---

# 複合查詢

複合查詢可作為多個葉子子句或複合子句的外層包裝，用來合併其結果或修改其行為。

下表列出所有複合查詢類型。

查詢類型 | 說明
:--- | :---
[`bool`]({{site.url}}{{site.baseurl}}/query-dsl/compound/bool/) (布林值)| 使用布林邏輯合併多個查詢子句。
[`boosting`]({{site.url}}{{site.baseurl}}/query-dsl/compound/boosting/) | 在不將文件從搜尋結果中移除的情況下變更其相關性分數。傳回符合 `positive` 查詢的文件，但會降低結果中符合 `negative` 查詢之文件的相關性。
[`constant_score`]({{site.url}}{{site.baseurl}}/query-dsl/compound/constant-score/) | 包裝一個查詢或篩選器，並為所有符合的文件指派一個常數分數。此分數等於 `boost` 的值。
[`dis_max`]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) (disjunction max) | 傳回符合一或多個查詢子句的文件。如果文件符合多個查詢子句，則會獲得較高的相關性分數。相關性分數的計算方式是取任何符合子句中的最高分數，並可選擇將其他符合子句的分數乘以 tiebreaker 值後一併計入。
[`function_score`]({{site.url}}{{site.baseurl}}/query-dsl/compound/function-score/) | 使用您定義的函式，重新計算查詢所傳回文件的相關性分數。
[`hybrid`]({{site.url}}{{site.baseurl}}/query-dsl/compound/hybrid/) | 將多個查詢的相關性分數合併為給定文件的一個分數。
