---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "營運面板"
nav_order: 100
redirect_from:
  - /observability-plugin/operational-panels/
---

# 營運面板

OpenSearch Dashboards 中的營運面板是使用 [Piped Processing Language]({{site.url}}{{site.baseurl}}/search-plugins/sql/ppl/index/) (PPL) 查詢所產生的視覺化集合。

## 開始使用營運面板

如果您想在未新增任何資料的情況下開始使用營運面板，請展開 **Action** 功能表，選擇 **Add samples**，Dashboards 就會新增一組營運面板，其中包含可供您探索的已儲存視覺化。

## 建立營運面板

若要建立營運面板並新增視覺化：

1. 從 **Add Visualization** 下拉式功能表中，選擇 **Select Existing Visualization** 或 **Create New Visualization**，這會帶您前往 [事件分析]({{site.url}}{{site.baseurl}}/observing-your-data/event-analytics/) 探索器，您可以在其中使用 PPL 建立視覺化。
1. 如果您要新增既有的視覺化，請從下拉式功能表中選擇一個視覺化。
1. 選擇 **Add**。

![營運面板範例]({{site.url}}{{site.baseurl}}/images/operational-panel.png)

若要在營運面板中搜尋特定的視覺化，請使用 PPL 查詢來搜尋您已新增至面板的資料。
