---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "瀏覽 OpenSearch Dashboards"
nav_order: 20
has_children: false
---

# 瀏覽 OpenSearch Dashboards

您可以從[首頁](#the-opensearch-dashboards-home-page)和[左側導覽面板](#the-left-navigation-panel)瀏覽 OpenSearch Dashboards，左側導覽面板可讓您存取所有 OpenSearch Dashboards 應用程式。

## OpenSearch Dashboards 首頁

OpenSearch Dashboards 首頁有兩種形式：傳統首頁和工作區首頁。

### 傳統首頁

下圖顯示傳統導覽中的首頁，且導覽面板為開啟狀態。

![OpenSearch Dashboards 首頁]({{site.url}}{{site.baseurl}}/images/dashboards/osd-homepage.png)

- _標頭列_ (A) 由左至右包含下列元素：
  - {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/menu-icon.png" class="inline-icon" alt="menu icon"/>{:/} (menu) 選單圖示。
  - {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/home-icon.png" class="inline-icon" alt="home icon"/>{:/} (home) 首頁圖示。
  - 階層式導覽 (breadcrumb) 顯示區。在首頁上，它只包含一個標籤「Home」。
  - 選單區域 (B)。此區域位於標頭列的右側部分，當主面板中有應用程式處於使用中狀態時，會包含一個隨情境而變的_應用程式選單_。
  - {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/help-icon.png" class="inline-icon" alt="help icon"/>{:/} (help) 說明圖示。
- 導覽面板 (C) 是瀏覽 OpenSearch Dashboards 的主要方式。它包含依功能分組的可摺疊選單 (**Recently viewed**、**OpenSearch Dashboards** 應用程式、**Observability** 等)。請參閱[左側導覽面板](#the-left-navigation-panel)。
- _面板_或_主面板_ (D) 包含目前的應用程式或 UI 頁面。

### 工作區導覽
**於 2.18.0 版推出**
{: .label .label-purple }

OpenSearch Dashboards 提供另一種稱為工作區導覽的導覽模式。工作區會將應用程式分組到聚焦的環境中，例如 Analytics、Observability 或 Security Analytics。在工作區導覽中，首頁會列出您的工作區，如下圖所示，您必須先選取一個工作區才能存取應用程式。

![已啟用工作區的 OpenSearch Dashboards 首頁]({{site.url}}{{site.baseurl}}/images/dashboards/getting-started-workspaces-nav.png)

選取工作區後，左側導覽面板會提供該工作區應用程式的存取方式，與傳統導覽類似，如下圖所示。部分功能 (例如[使用查詢建立視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualization-editor/)) 僅能在工作區中使用。

![工作區中的概觀頁面和左側導覽面板]({{site.url}}{{site.baseurl}}/images/dashboards/workspace-overview-nav.png)

工作區由 OpenSearch Dashboards 管理員啟用。如需更多資訊，請參閱[工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/)。

## 左側導覽面板

使用 UI 左側的_左側導覽面板_，選取您要使用的任何應用程式或設定頁面。若要開啟導覽面板，請選取頁面頂端的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/menu-icon.png" class="inline-icon" alt="menu icon"/>{:/} (menu) 圖示。

下圖顯示傳統導覽和工作區導覽中最常使用的功能。

傳統導覽面板 | 工作區導覽面板
:--: | :--:
![傳統導覽面板]({{site.url}}{{site.baseurl}}/images/dashboards/os-nav-panel.png){: width="60%" } | ![工作區導覽面板]({{site.url}}{{site.baseurl}}/images/dashboards/os-new-nav-panel.png){: width="57%" }

- _選單圖示_ (A) 可開啟和關閉導覽面板。
- **Discover** (B) 會在主面板中開啟 Discover 應用程式。請參閱[使用 Discover 探索資料]({{site.url}}{{site.baseurl}}/dashboards/discover/index-discover/)。
- **Dashboards** (C) 會在主面板中開啟 Dashboards 應用程式。請參閱[建立儀表板]({{site.url}}{{site.baseurl}}/dashboards/dashboard/)。
- **Visualize** (D) 會在主面板中開啟 Visualize 應用程式。請參閱[建置資料視覺化]({{site.url}}{{site.baseurl}}/dashboards/visualize/visualize-app/)。
- **Observability** (E) 會在導覽面板中開啟 Observability 選單。請參閱[可觀測性]({{site.url}}{{site.baseurl}}/observing-your-data/)。

## 相關文件

- [存取 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/getting-started/access/)