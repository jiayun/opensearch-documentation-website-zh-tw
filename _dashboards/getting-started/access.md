---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "存取 OpenSearch Dashboards"
parent: Getting started
nav_order: 15
---

# 存取 OpenSearch Dashboards

當 OpenSearch 與 OpenSearch Dashboards 正在執行時，請開啟瀏覽器並前往下列 URL：

- 本機安裝請使用 `http://localhost:5601` 或 `https://localhost:5601`。
- OpenSearch Playground 請使用 [https://playground.opensearch.org/app/home#/](https://playground.opensearch.org/app/home#/)。

如果您的叢集使用 Security 外掛程式，OpenSearch Dashboards 會開啟登入頁面。請以 `admin` 使用者身分登入，並使用安裝 OpenSearch 時在 `OPENSEARCH_INITIAL_ADMIN_PASSWORD` 中設定的密碼。如需更多資訊，請參閱[設定初始管理員密碼]({{site.url}}{{site.baseurl}}/security/configuration/passwords/#setting-the-initial-admin-password)。

>- _OpenSearch Dashboards_ 是指 OpenSearch 的網頁 UI，也就是您目前在瀏覽器中看到的應用程式。
>- **Dashboards** 應用程式是 OpenSearch Dashboards 內用來將視覺化組合到單一頁面的工具。
>- _dashboard_（小寫）是指在 **Dashboards** 應用程式中建立的個別視覺化頁面。
{: .note}

## 存取本節使用的應用程式

入門教學會使用 Discover、Visualize 和 Dashboards 應用程式，以及 Dev Tools 主控台。請使用 UI 左側的_左側導覽面板_，選取您要使用的任何應用程式或設定頁面。若要開啟導覽面板，請選取頁面頂端標題列中的 {::nomarkdown}<img src="{{site.url}}{{site.baseurl}}/images/icons/menu-icon.png" class="inline-icon" alt="menu icon"/>{:/}（選單）圖示。如需首頁和左側導覽面板的詳細資訊，請參閱[瀏覽 OpenSearch Dashboards]({{site.url}}{{site.baseurl}}/dashboards/navigating-ui/)。

### 傳統導覽

在未啟用工作區的安裝中，左側導覽面板會直接列出所有應用程式。下圖標示了教學中使用的應用程式。

![使用傳統導覽的 OpenSearch Dashboards 首頁]({{site.url}}{{site.baseurl}}/images/dashboards/getting-started-classic-nav.png)

1. 準備您的資料。
1. 探索 Discover 應用程式。
1. 探索 Dashboards 應用程式。
1. 探索 Visualize 應用程式。
1. 在 OpenSearch Dashboards 中執行查詢。

本文件中的範例使用傳統導覽。如果您已啟用工作區，選單結構會有所不同，但您的工作區中仍提供相同的應用程式。

### 工作區導覽

如果已啟用工作區，請先建立並選取工作區。如需詳細資訊，請參閱[工作區導覽]({{site.url}}{{site.baseurl}}/dashboards/navigating-ui/#workspaces-navigation)。下圖顯示範例 Analytics 工作區中的左側導覽，其中包含教學中使用的應用程式。

![Analytics 工作區中的左側導覽]({{site.url}}{{site.baseurl}}/images/dashboards/getting-started-workspace-interior-nav.png)

1. 準備您的資料。
1. 探索 Discover 應用程式。
1. 探索 Dashboards 應用程式。
1. 探索 Visualize 應用程式。
1. 在 OpenSearch Dashboards 中執行查詢。

## 後續步驟

- 若要了解各個應用程式的功能，請參閱[了解主要應用程式]({{site.url}}{{site.baseurl}}/dashboards/getting-started/learn-dashboards/)。
