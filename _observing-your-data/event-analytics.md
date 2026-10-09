---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "事件分析"
nav_order: 20
redirect_from:
  - /observability-plugin/event-analytics/
---

# 事件分析

OpenSearch Observability 中的事件分析可讓您使用 [Piped Processing Language]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) (PPL) 查詢建立資料視覺化。

## 事件分析入門

若要開始使用，請在 OpenSearch Dashboards 中選擇 **Observability**，然後選擇 **Logs**。如果您想在不新增自有資料的情況下開始探索，請選擇 **Add samples**。Dashboards 會新增可供您互動的範例視覺化。您也可以在 [OpenSearch Playground](https://playground.opensearch.org/app/observability-logs#/) 中試用預先設定的分析。

## 建立查詢

若要產生自訂視覺化，您必須先指定 PPL 查詢。接著，OpenSearch Dashboards 會根據您的查詢結果自動建立視覺化。

例如，下列 PPL 查詢會傳回您資料中目前有多少個主機位址的計數。

```
source = opensearch_dashboards_sample_data_logs | fields host | stats count()
```

根據預設，Dashboards 會顯示您資料中最近 15 分鐘的結果。若要查看不同時間範圍的資料，請使用日期與時間選擇器選擇所需的設定。

如需有關建立 PPL 查詢的詳細資訊，請參閱 [Piped Processing Language]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/)。

### OpenSearch Dashboards 查詢助理

請注意，機器學習模型具有機率性，且部分模型的表現可能優於其他模型，因此 OpenSearch Assistant 偶爾可能會產生不正確的資訊。我們建議您依據使用案例適當評估輸出的正確性，包括檢閱輸出內容或將其與其他驗證因素結合。
{: .important}

為了簡化查詢的建立，**OpenSearch Assistant** 工具組提供了一個可將自然語言查詢轉換為 PPL 的助理。下圖顯示了螢幕擷取畫面。

![OpenSearch Query Assist 範例畫面]({{site.url}}{{site.baseurl}}/images/log-explorer-query-assist.png)

#### 啟用查詢助理

根據預設，OpenSearch Dashboards 中已啟用 **Query Assistant**。若要啟用回應摘要功能，請找到您的 `opensearch_dashboards.yml` 檔案副本並設定下列選項：

```yaml
observability.summarize.enabled: true
observability.summarize.response_summary_agent_name: "Response summary agent"
observability.summarize.error_summary_agent_name: "Error summary agent"
```

若要停用 Query Assistant，請將 `observability.query_assist.enabled: false` 新增至您的 `opensearch_dashboards.yml`。

#### 設定查詢助理

若要設定 **Query Assistant**，請依照 GitHub 上 [入門指南](https://github.com/opensearch-project/dashboards-assistant/blob/main/GETTING_STARTED_GUIDE.md) 中的步驟操作。本指南提供 **OpenSearch Assistant** 與 **Query Assistant** 的逐步設定說明。若只要設定 **Query Assistant**，請使用指南中所附的 `query-assist-agent` 範本。

## 儲存視覺化

Dashboards 產生視覺化之後，如果您想再次查看它，或將它納入 [作業面板]({{site.url}}{{site.baseurl}}/observing-your-data/operational-panels/)，請將其儲存。若要儲存視覺化，請展開右上角的 **Save** 下拉式選單，輸入視覺化的名稱，然後選取 **Save** 按鈕。您可以在事件分析頁面上重新開啟已儲存的視覺化。

## 建立事件分析視覺化並將其新增至儀表板

此功能適用於 OpenSearch Dashboards 2.7 及更新版本。它適用於使用 PPL 從 OpenSearch 或聯合資料來源 (例如 Prometheus) 查詢資料的新視覺化。
{: .note}

若要建立 PPL 視覺化，請依照下列步驟操作：

1. 在主選單上，選擇 **Visualize** > **PPL**。
2. 在 **Observability** > **Logs** > **Explorer** 視窗中，於 **PPL query** 欄位輸入索引來源，例如 `source = opensearch_dashboards_sample_data_flights | stats count() by DestCountry`。您必須使用 PPL 語法輸入查詢。
3. 設定時間篩選條件，例如 **This week**，然後選取 **Refresh**。
4. 從右側的側邊欄下拉式選單中選擇視覺化類型，例如 **Pie**。
5. 選取 **Save** 並輸入視覺化的名稱。

您現在已建立一個新的視覺化，可將其新增至新的或現有的儀表板。若要將 PPL 查詢新增至儀表板，請依照下列步驟操作：

1. 從主選單選取 **Dashboards**。
2. 在 **Dashboards** 視窗中，選取 **Create** > **Dashboard**。
3. 在 **Editing New Dashboard** 視窗中，選擇 **Add an existing**。
4. 在 **Add panels** 視窗中，從 **Types** 下拉式選單選擇 **PPL**，然後選取視覺化。該視覺化現在會顯示在您的儀表板上。
5. 選取 **Save** 並輸入儀表板的名稱。
6. 若要將更多視覺化新增至儀表板，請選擇 **Select existing visualization** 並依照步驟 1--5 操作。或者，選擇 **Create new**，然後在 **New Visualization** 視窗中選取 **PPL**。您將返回事件分析頁面，並依照前述說明中的步驟 1--5 操作。

下列示範概述如何建立事件分析視覺化並將其新增至儀表板。

![建立事件分析視覺化並將其新增至儀表板的示範]({{site.url}}{{site.baseurl}}/images/dashboards/event-analytics-dashboard.gif)

### 事件分析視覺化的限制

事件分析視覺化不支援 [Dashboards Query Language (DQL)]({{site.url}}{{site.baseurl}}/dashboards/discover/dql/) 或 [查詢領域特定語言 (DSL)]({{site.url}}{{site.baseurl}}/query-dsl/index/)，且不使用索引模式。請注意下列限制：

- 事件分析視覺化僅使用透過下拉式介面建立的篩選條件。如果您的儀表板中有 DQL 查詢或 DSL 篩選條件，視覺化不會使用它們。
- **Dashboard** 篩選條件下拉式介面僅顯示預設索引模式中的欄位，或同一儀表板中其他視覺化所使用之索引模式中的欄位。

## 檢視記錄檔

以下是您可用來檢視記錄檔的方法。

### 關聯記錄檔與追蹤

如果您經常追蹤跨應用程式的事件，可以將記錄檔與追蹤建立關聯。若要檢視關聯，您必須依照 OpenTelemetry 標準為追蹤編製索引，與 [追蹤分析]({{site.url}}{{site.baseurl}}/observing-your-data/trace/index/) 類似。在記錄檔中新增 `TraceId` 欄位後，即可在事件總管的記錄檔詳細資料中檢視相關聯的追蹤資訊。此方法會將對應至相同執行內容的記錄檔與追蹤建立關聯。下列示範展示此功能的實際運作情形。

![追蹤與記錄檔關聯]({{site.url}}{{site.baseurl}}/images/trace_log_correlation.gif)

### 檢視周邊事件

如果您需要更多有關某個記錄檔事件的資訊，可以選取 **View surrounding events**，以更全面地了解所關注時間點前後的情境。下列示範展示此功能的實際運作情形。

![周邊事件]({{site.url}}{{site.baseurl}}/images/surrounding_events.gif)

### 即時串流記錄檔

如果您偏好即時監控，可以設定事件分析內容自動重新整理的間隔。透過 Live Tail，您可以使用指定的 PPL 查詢將記錄檔直接串流至 OpenSearch Observability 事件分析，同時運用篩選條件等強大功能。這可以改善您的偵錯流程，並讓您無須手動重新整理內容，即可順暢地即時監控記錄檔。

透過 Live Tail，您可以選取間隔並在各間隔之間順暢切換，以控制即時記錄檔串流的頻率。此功能類似於 `tail -f` CLI 命令，因為它只會擷取最新的即時記錄檔，可能會略過相當大一部分的即時記錄檔。Live Tail 會顯示 OpenSearch 在即時串流期間收到的即時記錄檔總數，讓您深入了解傳入流量的模式。下列示範展示此功能的實際運作情形。

![Live Tail]({{site.url}}{{site.baseurl}}/images/live_tail.gif)

## 相關文件

- [OpenSearch Assistant 工具組示範](https://www.youtube.com/watch?v=VTiJtGI2Sr4&t=152s)
- [OpenSearch Dashboards 中的 OpenSearch Assistant 入門指南](https://github.com/opensearch-project/dashboards-assistant/blob/main/GETTING_STARTED_GUIDE.md)
- 透過 REST API 進行 OpenSearch Assistant 組態
