---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "OpenSearch 的 Migration Assistant"
nav_order: 30
has_children: true
has_toc: false
nav_exclude: true
permalink: /classic/migration-assistant/

items:
- heading: Migration Assistant 適合您嗎？
  description: 評估 Migration Assistant 是否適合您的使用情境。
  link: /classic/migration-assistant/is-migration-assistant-right-for-you/
- heading: 關鍵元件
  description: 熟悉 Migration Assistant 的關鍵元件。
  link: /classic/migration-assistant/key-components/
- heading: 架構
  description: 了解 Migration Assistant 如何整合至您的基礎架構。
  link: /classic/migration-assistant/architecture/
- heading: 分階段執行遷移
  description: 執行遷移的逐步指南。
  link: /classic/migration-assistant/migration-phases/
---

# ![Migration Assistant 圖示]({{site.url}}{{site.baseurl}}/images/icons/MigrationUpgrade_Color_Icon.svg){: .heading-icon} OpenSearch 的 Migration Assistant (Classic)

經典的 OpenSearch Migration Assistant 可協助您順利完成端對端、零停機的升級與遷移至 OpenSearch。遷移有三個必須了解的面向：

- **中繼資料遷移**：遷移叢集中繼資料，例如索引設定、別名和範本。
- **回填遷移**：將現有或歷史資料從來源叢集遷移至目標叢集。
- **即時流量遷移**：將持續進行的即時流量從來源叢集複寫至目標叢集。

本使用者指南著重於執行完整的遷移。

{% include list.html list_items=page.items%}