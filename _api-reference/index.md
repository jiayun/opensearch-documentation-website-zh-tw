---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "API 參考"
nav_order: 1
has_toc: false
has_children: true
nav_exclude: true
description: "OpenSearch REST API 與 gRPC API 的完整 API 參考，涵蓋叢集、索引、搜尋、文件及其他操作。"
permalink: /api-reference/
redirect_from:
  - /opensearch/rest-api/index/
  - /api-reference/index/
---

# API 參考

OpenSearch 中的每個 API 操作都可以使用 [REST API](#rest-apis)。您也可以改用實驗性的 [gRPC API](#grpc-apis) 呼叫其中一部分操作。

本頁列出的是 API 系列而非個別操作。若要尋找特定操作，請開啟其所屬的系列，並使用該頁面上的 API 清單。

## REST API
**於 1.0 版導入**
{: .label .label-purple }

OpenSearch 提供下列 REST API。

### 核心 REST API

本節說明下列核心 REST API。

| API | 用途 |
| :--- | :--- |
| [Analyze API]({{site.url}}{{site.baseurl}}/api-reference/analyze-apis/) | 檢視分析器從文字字串產生的詞元。 |
| [CAT API]({{site.url}}{{site.baseurl}}/api-reference/cat/) | 以對齊欄位的純文字讀取叢集統計資料。 |
| [List API]({{site.url}}{{site.baseurl}}/api-reference/list/) | 以分頁純文字讀取索引與分片統計資料。 |
| [Cluster API]({{site.url}}{{site.baseurl}}/api-reference/cluster-api/) | 檢查叢集健康狀態、變更叢集設定，以及擷取叢集統計資料。 |
| [Data stream API]({{site.url}}{{site.baseurl}}/api-reference/data-stream/) | 建立、刪除、修改資料串流，以及擷取其相關資訊。 |
| [Document API]({{site.url}}{{site.baseurl}}/api-reference/document-apis/) | 單獨或大量編製索引、擷取、更新及刪除文件。 |
| [Index API]({{site.url}}{{site.baseurl}}/api-reference/index-apis/) | 建立、設定、維護及刪除索引、別名與索引範本。 |
| [Ingest API]({{site.url}}{{site.baseurl}}/api-reference/ingest-apis/) | 定義在文件編製索引時轉換文件的資料匯入管線與處理器。 |
| [Nodes API]({{site.url}}{{site.baseurl}}/api-reference/nodes-apis/) | 擷取個別節點的資訊、統計資料與熱執行緒。 |
| [Script API]({{site.url}}{{site.baseurl}}/api-reference/script-apis/) | 儲存、擷取及執行 Painless 指令碼。 |
| [Search API]({{site.url}}{{site.baseurl}}/api-reference/search-apis/) | 執行查詢，並使用搜尋範本、捲動情境與搜尋效能分析。 |
| [Snapshot API]({{site.url}}{{site.baseurl}}/api-reference/snapshots/) | 管理快照儲存庫，以及建立與還原快照。 |
| [Tasks API]({{site.url}}{{site.baseurl}}/api-reference/tasks/) | 追蹤及取消長時間執行的操作。 |

本頁所列其餘 API 則在各自的章節中說明。

### 搜尋功能與查詢語言 API

下列 API 為核心搜尋 API 提供額外的方式來提交查詢、處理結果及衡量相關性。

| API | 用途 |
| :--- | :--- |
| [Asynchronous Search API]({{site.url}}{{site.baseurl}}/search-plugins/async/) | 在背景執行搜尋，並在完成過程中擷取部分結果。 |
| [Search Pipeline API]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/) | 定義轉換搜尋請求與結果的搜尋管線與處理器。 |
| [Search Relevance Workbench API]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/) | 建立用於衡量搜尋品質的查詢集、搜尋組態、判斷與實驗。 |
| [SQL 與 PPL API]({{site.url}}{{site.baseurl}}/sql-and-ppl/sql-and-ppl-api/) | 執行 SQL 與 Piped Processing Language 查詢，並管理它們讀取的資料來源。 |

### 向量搜尋與機器學習 API

下列 API 管理支援向量搜尋與機器學習的模型、代理程式與工作流程。

| API | 用途 |
| :--- | :--- |
| [ML Commons API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/) | 註冊、部署及執行機器學習模型、代理程式與連接器。 |
| [Vector Search API]({{site.url}}{{site.baseurl}}/vector-search/api/) | 管理支援向量搜尋的模型，並讀取其統計資料。 |
| [Workflow API]({{site.url}}{{site.baseurl}}/automating-configurations/api/) | 建立、佈建及管理可自動化複雜設定任務的工作流程範本。 |

### 索引管理 API

下列 API 可自動化索引及其資料的維護作業。

| API | 用途 |
| :--- | :--- |
| [Index Rollups API]({{site.url}}{{site.baseurl}}/im-plugin/index-rollups/rollup-api/) | 建立及管理將歷史資料彙整為較小索引的 rollup 工作。 |
| [Index State Management API]({{site.url}}{{site.baseurl}}/im-plugin/ism/api/) | 建立及管理可自動化索引生命週期操作的政策。 |
| [ISM Error Prevention API]({{site.url}}{{site.baseurl}}/im-plugin/ism/error-prevention/api/) | 開啟 Index State Management 錯誤防護，並讀取其驗證結果。 |
| [Refresh Search Analyzer API]({{site.url}}{{site.baseurl}}/im-plugin/refresh-analyzer/) | 在不關閉開啟中索引的情況下重新載入其搜尋分析器。 |
| [Transforms API]({{site.url}}{{site.baseurl}}/im-plugin/index-transforms/transforms-apis/) | 建立及管理將資料重塑至新索引的 transform 工作。 |

### 叢集管理 API

下列 API 可保護叢集可用性，並控制叢集使用資源的方式。

| API | 用途 |
| :--- | :--- |
| [Cross-Cluster Replication (CCR) API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/replication-plugin/api/) | 將索引從領導者叢集複寫至追隨者叢集。 |
| [Remote Store Stats API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/remote-store/remote-store-stats-api/) | 讀取遠端備份儲存空間的上傳與下載統計資料。 |
| [Rules API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/rule-lifecycle-api/) | 建立及管理將傳入請求指派至工作負載群組的自動標籤規則。 |
| [Shard Indexing Backpressure Stats API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/stats-api/) | 監視分片索引寫入回壓。 |
| [Snapshot Management API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/snapshots/sm-api/) | 依排程建立及刪除快照。 |
| [Workload Management API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/workload-groups/) | 建立限制資源用量的工作負載群組，並讀取其統計資料。 |

### 可觀測性與監控 API

下列 API 會回報叢集狀態，並在狀態變更時通知您。

| API | 用途 |
| :--- | :--- |
| [Alerting API]({{site.url}}{{site.baseurl}}/observing-your-data/alerting/api/) | 建立及管理監視器、觸發條件與警示。 |
| [Anomaly Detection API]({{site.url}}{{site.baseurl}}/observing-your-data/ad/api/) | 建立及管理異常偵測器，並讀取其發現的異常。 |
| [Forecasting API]({{site.url}}{{site.baseurl}}/observing-your-data/forecast/api/) | 建立及管理預測器，並讀取其產生的預測。 |
| [Job Scheduler API]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/job-scheduler/index/#job-scheduler-apis) | 監視叢集上的排程工作與鎖定。 |
| [Notifications API]({{site.url}}{{site.baseurl}}/observing-your-data/notifications/api/) | 定義傳遞通知的頻道，以及傳送通知的來源。 |
| [Performance Analyzer API]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/pa/api/) | 擷取節點或叢集的效能指標。 |
| [Query Insights API]({{site.url}}{{site.baseurl}}/observing-your-data/query-insights/) | 讀取前 N 名查詢、即時查詢與查詢洞察健康狀態統計資料，並變更查詢洞察設定。 |
| [Reporting API]({{site.url}}{{site.baseurl}}/reporting/api/) | 定義報告，並從儀表板、視覺化、已儲存的搜尋與筆記本產生報告。下載已轉譯的內容會使用 OpenSearch Dashboards 端點。 |
| [Root Cause Analysis API]({{site.url}}{{site.baseurl}}/monitoring-your-cluster/pa/rca/api/) | 擷取叢集的根本原因分析結果。 |

### 安全性與安全分析 API

下列 API 為叢集提供存取控制，並偵測其資料中的安全威脅。

| API | 用途 |
| :--- | :--- |
| [Resource Sharing API]({{site.url}}{{site.baseurl}}/security/access-control/resource-sharing-api/) | 與其他使用者和角色共用外掛程式資源，例如模型與偵測器。 |
| [Security API]({{site.url}}{{site.baseurl}}/security/api/) | 管理使用者、角色、角色對應、動作群組與租用戶，並讀取或取代安全性組態。 |
| [Security Analytics API]({{site.url}}{{site.baseurl}}/security-analytics/api-tools/index/) | 管理用於識別安全事件的偵測器、規則、發現與警示。 |

### OpenSearch Dashboards API

下列 API 管理 OpenSearch Dashboards 已儲存的物件與工作區，並讀取使用量統計資料。與先前預設傳送至連接埠 9200 上 OpenSearch REST 層的 REST API 請求不同，這些請求預設會傳送至連接埠 5601 上的 OpenSearch Dashboards。

| API | 用途 |
| :--- | :--- |
| [Maps Stats API]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/maps-stats-api/) | 讀取地圖及其圖層的使用量統計資料。 |
| [Saved Objects API]({{site.url}}{{site.baseurl}}/dashboards/management/saved-objects-api/) | 列出、建立、更新、匯出及匯入已儲存的物件，例如索引模式、視覺化與儀表板。 |
| [Search Relevance Stats API]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/stats-api/) | 讀取搜尋相關性操作的使用量統計資料。 |
| [Workspace API]({{site.url}}{{site.baseurl}}/dashboards/workspace/apis/) | 建立、更新、列出及刪除工作區。 |

## gRPC API
**於 3.0 版導入**
{: .label .label-purple }

您可以使用 gRPC API 作為 REST 介面的替代方案。這些 API 使用 gRPC 通訊協定，與 OpenSearch 叢集進行更有效率的通訊。如需更多資訊與支援的 API，請參閱 [gRPC API]({{site.url}}{{site.baseurl}}/api-reference/grpc-apis/)。

## 參考

下列頁面提供額外的 API 參考資訊：

- [通用 REST 參數]({{site.url}}{{site.baseurl}}/api-reference/common-parameters/)
- [支援的單位]({{site.url}}{{site.baseurl}}/api-reference/units/)
- [常用 API]({{site.url}}{{site.baseurl}}/api-reference/popular-api/)
