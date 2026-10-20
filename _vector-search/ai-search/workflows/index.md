---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "AI 搜尋工作流程"
parent: AI search
nav_order: 80
has_children: true
redirect_from:
  - /automating-configurations/
  - /automating-configurations/index/
  - /vector-search/ai-search/workflows/
---

# AI 搜尋工作流程
**於 2.13 版導入**
{: .label .label-purple }

您可以透過提供常見使用情境的範本，自動化複雜的 OpenSearch 設定與前置處理工作。例如，將機器學習 (ML) 設定工作自動化，可以簡化 OpenSearch ML 功能的使用。工作流程自動化僅限於 ML 與向量搜尋工作。

OpenSearch 使用情境範本以 JSON 或 YAML 文件提供設定程序的精簡描述。這些範本描述用於對話式聊天或查詢產生、AI 連接器、工具、代理程式，以及其他將 OpenSearch 準備為生成式模型後端的元件之自動化工作流程組態。如需自訂範本範例，請參閱[範例範本](https://github.com/opensearch-project/flow-framework/tree/main/sample-templates)。如需 OpenSearch 提供的範本，請參閱[工作流程範本]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-templates/)。

工作流程自動化提供下列優點：

* **使用情境範本**：使用預先定義的範本快速入門，這些範本概述一般使用情境的設定程序。
* **可自訂的工作流程**：將工作流程範本自訂為您的特定使用情境。
* **設定自動化**：透過單一 API 呼叫輕鬆設定 AI 連接器、工具、代理程式及其他元件。

## 範本結構

**範本**在 OpenSearch 中實作工作流程自動化。您可以以 JSON 或 YAML 格式提供這些範本。您可以使用特定使用情境所需的一連串步驟來描述一或多個範本。每個範本由下列元素組成：

* **中繼資料**：名稱、描述、使用情境類別、範本版本，以及 OpenSearch 版本相容性範圍。
* **使用者輸入**：預期由使用者提供的參數，這些參數為所有工作流程中所有自動化步驟共通，例如索引名稱。
* **工作流程**：一或多個工作流程，包含下列元素：
    * **使用者輸入**：預期由使用者提供的參數，這些參數專屬於此工作流程中的步驟。
    * **工作流程步驟**：以有向非循環圖 (DAG) 描述的工作流程步驟：  
        * ***節點*** 描述程序的步驟，這些步驟可能會平行執行。如需工作流程步驟的語法，請參閱[工作流程步驟]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-steps/)。 
        * ***邊*** 將節點排序為在前一個步驟完成後執行，並可能使用先前步驟的輸出欄位。當節點在 `previous_node_input` 對應中包含參照先前節點工作流程步驟的鍵時，剖析期間會自動在範本中加入對應的邊，因此為了簡化可以省略。

## 後續步驟

若要了解組成工作流程之步驟的語法，請參閱[工作流程步驟]({{site.url}}{{site.baseurl}}/vector-search/ai-search/workflows/workflow-steps/)。
