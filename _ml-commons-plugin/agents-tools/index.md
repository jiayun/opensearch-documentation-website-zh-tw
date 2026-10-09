---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理程式與工具"
has_children: true
has_toc: false
nav_order: 20
redirect_from:
  - /ml-commons-plugin/agents-tools/
---

# 代理程式與工具
**於 2.13 版推出**
{: .label .label-purple }

您可以使用代理程式與工具自動化機器學習 (ML) 任務。

_代理程式_ 會協調並執行 ML 模型與工具。如需支援的代理程式清單，請參閱[代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/)。

<!-- vale off -->
_工具_ 會執行一組特定任務。工具的範例包括支援向量搜尋的 [`VectorDBTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/vector-db-tool/)，以及執行 List Indices API 的 [`ListIndexTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/list-index-tool/)。如需支援的工具清單，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
<!-- vale on -->

您可以使用[處理器鏈]({{site.url}}{{site.baseurl}}/ml-commons-plugin/processor-chain/)修改及轉換工具輸出。
本節說明在 OpenSearch 叢集內執行，並執行常見 OpenSearch 作業 (例如列出索引及執行查詢) 的 OpenSearch 代理程式與工具。

## 相關功能

OpenSearch 也提供工具，讓外部 AI 助理連線至您的叢集並進行查詢。這些工具在您的 OpenSearch 叢集外部執行。如需更多資訊，請參閱 [AI 代理程式整合]({{site.url}}{{site.baseurl}}/ai-agent-integrations/)。
