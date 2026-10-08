---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
nav_order: 10
has_children: true
has_toc: false
redirect_from:
  - /dashboards/getting-started/
  - /dashboards/get-started/quickstart-dashboards/
  - /dashboards/quickstart-dashboards/
  - /dashboards/browser-compatibility/
  - /dashboards/quickstart/
install_items:
- heading: 安裝 OpenSearch Dashboards
  link: /dashboards/getting-started/install/
- heading: 存取 OpenSearch Dashboards
  link: /dashboards/getting-started/access/
- heading: 準備您的資料
  link: /dashboards/getting-started/data-setup/
learn_items:
- heading: 了解主要應用程式
  description: 探索每個應用程式的功能及使用時機。
  link: /dashboards/getting-started/learn-dashboards/
- heading: 探索 Discover 應用程式
  description: 搜尋及篩選資料。
  link: /dashboards/getting-started/explore-discover/
- heading: 探索 Visualize 應用程式
  description: 建立視覺化。
  link: /dashboards/getting-started/explore-visualize/
- heading: 探索 Dashboards 應用程式
  description: 檢視及篩選儀表板。
  link: /dashboards/getting-started/explore-dashboards/
- heading: 在 Dev Tools 主控台中執行查詢
  description: 使用 Query DSL 傳送 OpenSearch API 請求。
  link: /dashboards/getting-started/explore-dev-tools/
workflow_items:
- heading: 使用 Discover 探索資料
  description: 以互動方式搜尋、篩選及檢查您的資料。了解有哪些可用欄位、資料隨時間的分布情形，以及存在哪些模式。
  link: /dashboards/discover/index-discover/
- heading: 建置視覺化
  description: 了解如何為您的資料建立圖表、地圖、表格及其他視覺化呈現方式。
  link: /dashboards/visualize/
- heading: 組合儀表板
  description: 將多個視覺化組合到單一頁面中，以進行監控與分析。
  link: /dashboards/dashboard/
---

# OpenSearch Dashboards 入門

OpenSearch Dashboards 是 OpenSearch 的網頁介面。您可以使用它來探索資料、建置視覺化、組合儀表板及執行查詢。

開始之前，請確認您已熟悉文件和索引等 OpenSearch 基本概念。如需詳細資訊，請參閱 [OpenSearch 簡介]({{site.url}}{{site.baseurl}}/getting-started/intro/)。
{: .note}

## 步驟 1：設定 OpenSearch Dashboards

請選擇下列其中一個選項。

### 選項 1：使用 OpenSearch Playground

在瀏覽器中開啟 [OpenSearch Playground](https://playground.opensearch.org/app/home#/)。Playground 為唯讀，且已包含範例航班資料，因此您可以直接從[步驟 2](#step-2-explore-opensearch-dashboards-applications) 開始了解 OpenSearch Dashboards 應用程式。

### 選項 2：使用您自己的安裝

若要安裝 OpenSearch Dashboards 並新增範例資料，請依照下列步驟操作：

{% include list.html list_items=page.install_items %}

## 步驟 2：探索 OpenSearch Dashboards 應用程式

{% include list.html list_items=page.learn_items %}

## 後續步驟

熟悉這些應用程式後，建置儀表板的標準做法包含三個步驟：探索您的資料、建置個別視覺化，然後將這些視覺化組合成儀表板。若要詳細了解每個步驟，請使用下列連結瀏覽完整文件。

{% include list.html list_items=page.workflow_items %}
