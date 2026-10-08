---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "使用 Dev Tools"
parent: Exploring data
nav_order: 20
has_children: true
has_toc: false
redirect_from:
  - /dashboards/run-queries/
  - /dashboards/dev-tools/run-queries/
  - /dashboards/dev-tools/index-dev/
  - /dashboards/visualize/run-queries/
  - /dashboards/discover/run-queries/
  - /dashboards/dev-tools/
---

# 使用 Dev Tools

OpenSearch Dashboards 中的 **Dev Tools** 應用程式提供了用於查詢叢集以及測試查詢和匯入模式的工具。

如果您是第一次使用 Dev Tools 應用程式，請參閱 [在 Dev Tools 主控台執行查詢]({{site.url}}{{site.baseurl}}/dashboards/getting-started/explore-dev-tools/) 以獲取實作入門介紹。
{: .tip}

## 導覽至 Dev Tools

若要開啟 Dev Tools，請在 OpenSearch Dashboards 主頁面上選取 **Dev Tools**，如下圖所示。

![從主頁面進入 Dev Tools 主控台]({{site.url}}{{site.baseurl}}/images/dev-tools/dev-tools-main.png)

您也可以從任何其他頁面透過導覽至主選單並選取 **Management** > **Dev Tools** 來開啟 Dev Tools，如下圖所示。

![從所有頁面進入 Dev Tools 主控台]({{site.url}}{{site.baseurl}}/images/dev-tools/dev-tools-left.png){: width="200" }

在啟用了工作區 (workspaces) 的安裝環境中，請選取導覽面板左下角的程式碼圖示 ({::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/code-icon.png" class="inline-icon" alt="code icon"/>{:/})。

## 使用 Dev Tools

**Dev Tools** 應用程式如下圖所示。

![Dev Tools 主控台應用程式]({{site.url}}{{site.baseurl}}/images/dev-tools/dev-tools-console.png)

Dev Tools 包含以下應用程式：

- [**Console**]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/console/) 可將 [Query DSL]({{site.url}}{{site.baseurl}}/query-dsl/) 查詢和其他 REST API 請求發送到 OpenSearch 並顯示回應。
- [**Grok Debugger**]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/grok-debugger/) 可在您將 [Grok 模式]({{site.url}}{{site.baseurl}}/ingest-pipelines/processors/grok/) 用於資料匯入管線之前，針對範例記錄資料建立並測試該模式。
- [**Query Profiler**]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/query-profiler/) 可測量搜尋查詢中每個部分的執行時間，以便您識別效能緩慢的元件。
