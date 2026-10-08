---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "入門"
nav_order: 1
has_children: false
has_toc: false
nav_exclude: true
description: "OpenSearch 與 OpenSearch Dashboards 的文件。這是一套開放原始碼的套件，可用於全文搜尋、應用程式監控、記錄檔分析及向量搜尋。"
permalink: /about/
redirect_from:
  - /docs/opensearch/
  - /opensearch/
  - /opensearch/index/
why_use:
- heading: 向量資料庫
  description: 將 OpenSearch 作為向量資料庫，結合傳統搜尋、分析與向量搜尋的強大功能
  link: /vector-search/
  image: /images/icons/vector-search-square.png
  image_alt: 向量搜尋圖示
- heading: 快速且可擴充的全文搜尋
  description: 協助使用者在您的應用程式、網站或資料湖目錄中找到正確的資訊
  link: /search-plugins/
  image: /images/icons/Icon_Lexical_Search-150x150.avif
  image_alt: 詞彙搜尋圖示
- heading: 應用程式與基礎架構監控
  description: 使用可觀測性記錄檔、指標與追蹤，即時監控您的應用程式
  link: /observing-your-data/
  image: /images/icons/Icon_Observability-150x150.avif
  image_alt: 可觀測性監控圖示
- heading: 資料分析
  description: 在 OpenSearch Dashboards 中分析資料並將其視覺化
  link: /dashboards/
  image: /images/icons/OpenSearch-Dashboards-Square.png
  image_alt: OpenSearch Dashboards 圖示
features:
- heading: 安裝與設定
  description: 在您偏好的平台上設定 OpenSearch 與 OpenSearch Dashboards
  link: /install-and-configure/
- heading: 安全性
  description: 為您的叢集設定驗證、存取控制與加密
  link: /security/
- heading: 索引管理
  description: 建立索引、管理範本，並自動化索引生命週期
  link: /im-plugin/
- heading: 對應
  description: 定義欄位類型，以控制資料編製索引的方式
  link: /mappings/
- heading: API 參考
  description: 所有 OpenSearch REST 與 gRPC API 的完整參考
  link: /api-reference/
- heading: Query DSL
  description: 使用 OpenSearch 查詢語言搜尋您的資料
  link: /query-dsl/
- heading: 向量搜尋
  description: 使用向量與 AI 驅動的搜尋，建置現代化的搜尋應用程式
  link: /vector-search/
- heading: 機器學習
  description: 部署模型、連線至 AI 平台，並建置 AI 代理程式與助理
  link: /ml-commons-plugin/
getting_started:
- heading: OpenSearch 入門
  description: 了解 OpenSearch，並開始匯入與搜尋資料
  link: /getting-started/
  image: /images/icons/OpenSearch-Core.png
  image_alt: OpenSearch Core 圖示
- heading: OpenSearch Dashboards 入門
  description: 了解用於將資料視覺化的 OpenSearch Dashboards 應用程式與工具
  link: /dashboards/getting-started/
  image: /images/icons/OpenSearch-Dashboards.png
  image_alt: OpenSearch Dashboards 圖示
- heading: 向量搜尋入門
  description: 了解向量搜尋選項，並建置您的第一個向量搜尋應用程式
  link: /vector-search/getting-started/
  image: /images/icons/Vector-search-icon.avif
  image_alt: 向量搜尋圖示
- heading: OpenSearch 安全性入門
  description: 了解 OpenSearch 中的安全性
  link: /security/getting-started/
  image: /images/icons/OpenSearch-Security.png
  image_alt: OpenSearch Security 圖示
---

{%- comment -%}The `/docs/opensearch/` redirect is specifically to support the UI links in OpenSearch Dashboards 1.0.0.{%- endcomment -%}

# ![OpenSearch 圖示]({{site.url}}{{site.baseurl}}/images/icons/OpenSearch-Core.png){: .heading-icon} OpenSearch 與 OpenSearch Dashboards
**版本 {{site.opensearch_major_minor_version}}**
{: .label .label-blue }

OpenSearch 是一套可擴充的開放原始碼搜尋與分析套件，可用於全文搜尋、應用程式監控、記錄檔分析及向量搜尋。OpenSearch Dashboards 則提供視覺化與管理介面。

## 入門

{% include cards.html cards=page.getting_started %}

## 使用案例

{% include cards.html cards=page.why_use documentation_link=true %}

## 熱門文件

{% include cards.html cards=page.features %}


## 參與貢獻

[OpenSearch](https://opensearch.org) 由 OpenSearch Software Foundation 支援。所有元件皆依 [Apache License 2.0 版](https://www.apache.org/licenses/LICENSE-2.0.html)於 [GitHub](https://github.com/opensearch-project/) 上提供。
本專案歡迎各種形式的貢獻，包括 GitHub issue、錯誤修正、功能、外掛程式、文件等等，任何內容皆可。若要參與，請參閱[貢獻](https://github.com/opensearch-project/.github/blob/main/CONTRIBUTING.md)。

---

<!-- vale off -->
<small>OpenSearch includes certain Apache-licensed Elasticsearch code from Elasticsearch B.V. and other source code. Elasticsearch B.V. is not the source of that other source code. ELASTICSEARCH is a registered trademark of Elasticsearch B.V.</small>
<!-- vale on -->