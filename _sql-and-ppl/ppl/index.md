---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: PPL
nav_order: 5
has_children: true
has_toc: false
redirect_from:
  - /sql-and-ppl/ppl/
  - /search-plugins/sql/ppl/
  - /search-plugins/sql/ppl/index/
  - /search-plugins/ppl/
  - /observability-plugin/ppl/
  - /search-plugins/ppl/index/
  - /search-plugins/ppl/endpoint/
  - /search-plugins/ppl/protocol/
  - /observability-plugin/ppl/index/
---

# PPL

Piped Processing Language (PPL) 是一種查詢語言，著重於以循序漸進、逐步的方式處理資料。PPL 使用管道 (`|`) 運算子來組合命令，以尋找並擷取資料。由於 PPL 能有效率地處理半結構化資料，因此特別適合分析可觀測性資料，例如記錄檔、指標和追蹤。

## PPL 語法

下列範例顯示基本的 PPL 語法：

```sql
search source=<index-name> | <command_1> | <command_2> | ... | <command_n>
```
{% include copy.html %}


請參閱[語法]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/commands/syntax/)以取得具體的 PPL 語法範例。

## PPL 命令

PPL 使用一系列命令來篩選、轉換及彙總資料。請參閱[命令]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/functions/)以取得每個命令的說明和範例。

## 在 OpenSearch 中使用 PPL

在 OpenSearch 中執行 PPL 查詢需要 SQL 外掛程式。如果您執行的是 OpenSearch 的最小發行版，可能必須先[安裝 SQL 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)，才能使用 PPL。
{: .note}

您可以在 OpenSearch Dashboards 中以互動方式執行 PPL 查詢，或使用 `_ppl` 端點以程式設計方式執行。

在 OpenSearch Dashboards 中，[Query Workbench 工具](https://playground.opensearch.org/app/opensearch-query-workbench#/)提供互動式測試環境，相關說明請參閱[使用 Query Workbench]({{site.url}}{{site.baseurl}}/dashboards/query-workbench/)。

若要使用 API 執行 PPL 查詢，請參閱[SQL 和 PPL API]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql-ppl-api/)。


## 開發人員文件

開發人員可以在下列資源中找到相關資訊：

- [Piped Processing Language](https://github.com/opensearch-project/piped-processing-language) 規格
- [OpenSearch PPL 參考手冊](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/index.md)
- 使用 [PPL 視覺化](https://github.com/opensearch-project/dashboards-observability#event-analytics)的[可觀測性](https://github.com/opensearch-project/dashboards-observability/)
- PPL [資料類型](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/general/datatypes.md)
- PPL 中的[跨叢集搜尋](https://github.com/opensearch-project/sql/blob/main/docs/user/ppl/admin/cross_cluster_search.md#using-cross-cluster-search-in-ppl)
