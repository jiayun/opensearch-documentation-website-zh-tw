---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "概念"
parent: Getting started
nav_order: 60
---

# OpenSearch Dashboards 概念

本頁定義 OpenSearch Dashboards 文件中通用的關鍵術語。

## OpenSearch Dashboards 術語

- **_OpenSearch Dashboards_**：OpenSearch 的 Web 使用者介面。這是您在瀏覽器中存取的應用程式。
- **Dashboards** 應用程式：OpenSearch Dashboards 中用於將多個視覺化組合到單一頁面的應用程式。請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
- _dashboard_（小寫）：在 **Dashboards** 應用程式中建立的單一資料視覺化頁面。
- **Visualize** 應用程式：OpenSearch Dashboards 中用於建立個別圖表、地圖和表格的應用程式。請參閱[在 Visualize 應用程式中建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/)。
- _visualization_（視覺化）：包含圖形、圖表、地圖或其他資料視覺呈現方式的單一面板。
- **Discover** 應用程式：OpenSearch Dashboards 中用於搜尋、篩選和檢視資料的應用程式。請參閱[使用 Discover 探索資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。
- [**OpenSearch Playground**](https://playground.opensearch.org/app/home#/)：預先載入範例資料的唯讀網頁版 OpenSearch Dashboards 執行個體。您無須安裝任何項目，即可使用它探索 OpenSearch Dashboards。

## 資料概念

- _index_（索引）：儲存在 OpenSearch 中的相關文件集合。請參閱[索引]({{site.url}}{{site.baseurl}}/getting-started/intro/#index)。
- _document_（文件）：OpenSearch 中的基本資訊單位，以 JSON 物件的形式儲存。請參閱[文件]({{site.url}}{{site.baseurl}}/getting-started/intro/#document)。
- _index pattern_（索引模式）：一或多個索引的檢視，您可將其作為 OpenSearch Dashboards 中的資料來源。在某些情境中也稱為 _data source_（資料來源）。請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。
- _field_（欄位）：文件中單一具名的值，相當於關聯式資料庫資料表中的欄。
- _bucket_（桶）：根據彙總將欄位值分組的結果。桶可以是類別型（根據文字值）、範圍型（使用者定義的數值範圍）、直方圖型（自動決定大小的數值區間）或時間型（時間戳記欄位的區段）。
- _aggregation_（彙總）：跨文件摘要資料的運算，例如計算計數、平均值、總和，或將文件分組到桶中。請參閱[彙總]({{site.url}}{{site.baseurl}}/aggregations/)。
- _saved object_（已儲存物件）：您在 OpenSearch Dashboards 中儲存的任何項目，包括視覺化、儀表板、索引模式和已儲存的搜尋。

## 工作區

_workspace_（工作區）是 OpenSearch Dashboards 中的隔離環境，可依使用案例（例如 Analytics 或 Observability）整理應用程式和已儲存物件。請參閱[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)。

## 查詢語言

OpenSearch Dashboards 支援多種查詢語言：

- [**Dashboards Query Language (DQL)**]({{site.url}}{{site.baseurl}}/dashboards/dql/)：一種簡單的文字型語言，用於在 Discover 和 Dashboards 搜尋列中篩選資料。
- [**Piped Processing Language (PPL)**]({{site.url}}{{site.baseurl}}/sql-and-ppl/ppl/)：一種以管道為基礎的語言，用於資料處理和分析。可在 Query Workbench 和視覺化編輯器中使用。
- [**Query DSL**]({{site.url}}{{site.baseurl}}/query-dsl/)：完整的 OpenSearch 查詢語言，用於 Dev Tools 主控台和 API 請求。
- [**SQL**]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql/)：用於查詢 OpenSearch 資料的標準 SQL 語法。可在 Query Workbench 中使用。

## 後續步驟

探索各應用程式的完整文件：

- [使用 Discover 探索資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)
- [建立資料視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/)
- [建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)
