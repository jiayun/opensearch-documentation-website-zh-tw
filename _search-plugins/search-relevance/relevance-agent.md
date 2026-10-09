---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "相關性代理程式"
nav_order: 100
parent: Search Relevance Workbench
grand_parent: Optimizing search quality
has_toc: false
---

# 相關性代理程式
**於 3.6 版導入**
{: .label .label-purple }

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的進度或提供意見回饋，請參閱相關的 [GitHub 議題](https://github.com/opensearch-project/OpenSearch/issues/20602)。
{: .warning}

OpenSearch 相關性代理程式透過自然語言對話協助您識別並解決搜尋相關性問題。透過內嵌於 OpenSearch Dashboards 的聊天介面，您可以互動式地診斷問題、取得逐步調校指引，並執行複雜的工作流程。此代理程式運用 [Search Relevance Workbench]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/) 提供的工具。

此代理程式是 [OpenSearch Agent Server](https://github.com/opensearch-project/opensearch-agent-server) 的一部分，後者是一項獨立服務，用於託管並協調 OpenSearch 工作流程中的 AI 驅動代理程式。

## 運作方式

當您透過聊天介面送出訊息時，**路由器**會分析情境，並在適當時將請求導向相關性代理程式。當您位於 Search Relevance Workbench 頁面或搜尋工作區首頁時，路由器會啟用相關性代理程式。

相關性代理程式以多代理程式系統運作。內部協調器會解讀您的意圖，並將工作委派給專門的子代理程式，每個子代理程式負責相關性調校流程中的特定部分。協調器會彙整子代理程式的結果，並即時串流回傳給您。

## 專門代理程式

相關性代理程式協調器會協調三個專門的子代理程式。這些子代理程式會根據您的問題自動叫用，不需要另外設定。

### 使用者行為分析代理程式

使用者行為分析代理程式會分析 [User Behavior Insights (UBI)]({{site.url}}{{site.baseurl}}/search-plugins/ubi/) 資料，以檢視互動模式與點閱率。它會識別表現良好與表現不佳的查詢，將使用者行為與搜尋品質問題建立關聯，並提供以指標為依據的洞察，作為調校決策的參考。

### 假設產生代理程式

假設產生代理程式會檢視查詢結構與 DSL 組態，以分析搜尋品質問題。它會使用 UBI 資料識別模式，並產生可測試的改進假設，例如欄位權重調整或查詢加權策略。在建議組態變更之前，它會使用[成對比較實驗]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/comparing-search-results/)驗證假設。

### 評估代理程式

評估代理程式會設計並執行離線相關性評估實驗。當事件資料充足時，它會從 UBI 點擊資料建立[判斷清單]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/judgments/)；當點擊資料有限時，則使用 LLM 產生的相關性評分。接著，代理程式會使用您的[搜尋組態]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/search-configurations/)執行實驗，並計算搜尋品質指標 (NDCG、MAP 與 Precision@K) 以比較其效能。

## 必要條件

使用相關性代理程式之前，請確定您具備下列元件：

- **OpenSearch Agent Server** -- 代理程式伺服器必須正在執行並連線至您的 OpenSearch 叢集。設定說明請參閱 [OpenSearch Agent Server 儲存庫](https://github.com/opensearch-project/opensearch-agent-server)。
- **OpenSearch Dashboards** -- 聊天介面內嵌於 OpenSearch Dashboards。您必須設定 OpenSearch Dashboards 指向執行中的代理程式伺服器。
- **大型語言模型 (LLM) 供應商** -- 為代理程式伺服器設定 LLM。唯一支援的供應商是 [Amazon Bedrock](https://aws.amazon.com/bedrock/)。
- **User Behavior Insights (UBI)** (選用) -- 若要進行行為驅動的分析，並從點擊資料產生判斷，請[啟用 UBI]({{site.url}}{{site.baseurl}}/search-plugins/ubi/)，並將其設定為在您的叢集上收集事件。

## 存取代理程式

代理程式伺服器開始執行並完成 Dashboards 設定後，選取 OpenSearch Dashboards 標頭中的聊天圖示即可存取相關性代理程式。前往 Search Relevance Workbench 頁面或搜尋工作區首頁以啟用代理程式。

代理程式會即時回應，並可能在執行實驗步驟前要求您確認。

## 後續步驟

- [設定 OpenSearch Agent Server](https://github.com/opensearch-project/opensearch-agent-server)
- [Search Relevance Workbench]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/using-search-relevance-workbench/)
- [User Behavior Insights]({{site.url}}{{site.baseurl}}/search-plugins/ubi/)
- [實驗]({{site.url}}{{site.baseurl}}/search-plugins/search-relevance/experiments/)
