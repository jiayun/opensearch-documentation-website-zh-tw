---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作區入門"
parent: Workspaces
nav_order: 0
redirect_from:
  - /dashboards/workspace/
---

# 工作區入門
**於 2.18 版引入**
{: .label .label-purple }

OpenSearch Dashboards 2.18 引入了強化版首頁，提供您所有工作區的完整檢視。

新首頁包含下列功能：

1. **Create workspace** 按鈕，供 [OpenSearch Dashboards 管理員]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#configuring-dashboard-administrators)前往[建立工作區]({{site.url}}{{site.baseurl}}/dashboards/workspace/create-workspace/)頁面。
2. 工作區存取時間資訊，以及工作區概觀頁面的連結。
3. 使用案例資訊圖示，顯示工作區用途的相關資訊。
4. **View all workspaces** 按鈕，可前往[工作區管理]({{site.url}}{{site.baseurl}}/dashboards/workspace/manage-workspace/#navigating-the-workspaces-list)頁面。
5. 透過 **Learn more from documentation** 按鈕連結至最新的 OpenSearch 文件，並透過 **Explore live demo environment at playground.opensearch.org** 按鈕連結至 [OpenSearch Playground](https://playground.opensearch.org/app/home#/)。

導覽邏輯會根據您的工作區存取層級，將您導向適當的頁面，以確保流暢的使用者體驗：

- 如果您已設定預設工作區，系統會將您導向該工作區的概觀頁面。
- 如果您只有一個工作區，系統會將您導向該工作區的概觀頁面。
- 如果您有多個工作區，系統會將您導向新首頁。
- 如果您沒有任何工作區，系統會將您導向新首頁。
