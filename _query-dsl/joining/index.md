---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "聯結查詢"
has_children: true
nav_order: 70
has_toc: false
redirect_from:
  - /query-dsl/joining/
---

# 聯結查詢

OpenSearch 是一個分散式系統，資料分布在多個節點上。因此，在 OpenSearch 中執行類似 SQL 的 JOIN 操作會消耗大量資源。作為替代方案，OpenSearch 提供下列查詢來執行聯結操作，並針對跨多個節點的擴充進行最佳化：

| 查詢類型 | 說明 |
| :--- | :--- |
| [`nested`]({{site.url}}{{site.baseurl}}/query-dsl/joining/nested/) | 作為其他查詢的包裝器，用於搜尋 [nested]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/) 欄位。巢狀欄位物件會被搜尋，就像它們被編製索引為個別文件一樣。 |
| [`has_child`]({{site.url}}{{site.baseurl}}/query-dsl/joining/has-child/) | 搜尋其子文件符合查詢的父文件。需要 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位類型。 |
| [`has_parent`]({{site.url}}{{site.baseurl}}/query-dsl/joining/has-parent/) | 搜尋其父文件符合查詢的子文件。需要 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位類型。 |
| [`parent_id`]({{site.url}}{{site.baseurl}}/query-dsl/joining/parent-id/) | 搜尋與特定父文件聯結的子文件。需要 [join]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/join/) 欄位類型。 |

如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設定為 `false`，則不會執行聯結查詢。
{: .important}