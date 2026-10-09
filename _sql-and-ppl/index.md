---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "SQL 與 PPL"
nav_order: 230
has_children: true
has_toc: false
nav_exclude: true
permalink: /sql-and-ppl/
redirect_from:
  - /search-plugins/sql/
  - /search-plugins/sql/index/
---

# SQL 與 PPL

OpenSearch 提供兩種強大的查詢語言，可作為 [OpenSearch 查詢領域特定語言 (DSL)]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/full-text/) 的替代方案：**SQL** 與 **Piped Processing Language (PPL)**。這兩種語言都能讓您使用熟悉的語法，更輕鬆地查詢和分析資料。

## SQL

OpenSearch 中的 SQL 彌補了傳統關聯式資料庫概念與 OpenSearch 以文件為導向的資料儲存之間的落差。當您想運用既有的 SQL 知識，使用熟悉的 `SELECT`、`WHERE`、`GROUP BY` 及其他標準 SQL 作業來查詢、篩選和彙總 OpenSearch 資料時，請使用 SQL。

**最適合**：具有 SQL 經驗、想使用熟悉的關聯式資料庫語法查詢 OpenSearch 資料的使用者。

## PPL

PPL 是一種查詢語言，以循序、逐步的方式處理資料，並使用管線 (`|`) 運算子將命令串連起來。PPL 擅長分析記錄檔、指標和追蹤等可觀測性資料，對於探索性資料分析與轉換特別有效。

**最適合**：記錄檔分析、可觀測性工作流程，以及偏好以管線方式處理資料的使用者。

## 入門

- 了解 [SQL 與 PPL API]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql-ppl-api/)。
- 了解[在 OpenSearch 中使用 SQL]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql/)。
- 了解[在 OpenSearch 中使用 PPL]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/)。
- 了解[在 OpenSearch Dashboards 中使用 Query Workbench 執行 SQL 與 PPL 查詢]({{site.url}}{{site.baseurl}}/dashboards/query-workbench/)。
- 在[開發人員指南](https://github.com/opensearch-project/sql/blob/main/DEVELOPER_GUIDE.rst)中進一步了解 OpenSearch SQL。