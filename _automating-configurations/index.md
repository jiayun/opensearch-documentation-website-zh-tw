---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "自動化組態"
nav_order: 1
has_children: false
nav_exclude: true
redirect_from:
  - /automating-configurations/
---

# 自動化組態
**於 2.13 版推出**
{: .label .label-purple }

您可以提供常見使用案例的範本，將複雜的 OpenSearch 設定與前處理工作自動化。例如，將機器學習 (ML) 設定工作自動化，可以簡化 OpenSearch ML 功能的使用方式。

在 OpenSearch 2.12 中，組態自動化僅限於 ML 工作。
{: .info}

OpenSearch 使用案例範本以 JSON 或 YAML 文件精簡描述設定流程。這些範本描述了自動化工作流程組態，涵蓋對話式聊天或查詢產生、AI 連接器、工具、代理程式，以及其他將 OpenSearch 準備為生成式模型後端的元件。如需自訂範本範例，請參閱[範例範本](https://github.com/opensearch-project/flow-framework/tree/main/sample-templates)。如需 OpenSearch 提供的範本，請參閱[工作流程範本]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-templates/)。

## 主要功能

工作流程自動化提供下列優點：

* **使用案例範本**：使用預先定義的範本快速入門，這些範本概述了一般使用案例的設定流程。
* **可自訂的工作流程**：依照您的特定使用案例自訂工作流程範本。
* **設定自動化**：只需一次 API 呼叫，即可輕鬆設定 AI 連接器、工具、代理程式及其他元件。

## 範本結構

**範本**在 OpenSearch 中實作工作流程自動化。您可以 JSON 或 YAML 格式提供這些範本。您可以用特定使用案例所需的一系列步驟來描述一或多個範本。每個範本皆由下列元素組成：

* **中繼資料**：名稱、描述、使用案例類別、範本版本，以及相容的 OpenSearch 版本範圍。
* **使用者輸入**：預期由使用者提供、且適用於所有工作流程中所有自動化步驟的共用參數，例如索引名稱。
* **工作流程**：一或多個工作流程，包含下列元素：
    * **使用者輸入**：預期由使用者提供、且專屬於此工作流程中步驟的參數。
    * **工作流程步驟**：以有向無環圖 (DAG) 描述的工作流程步驟：  
        * ***節點***描述流程的步驟，這些步驟可以平行執行。如需工作流程步驟的語法，請參閱[工作流程步驟]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-steps/)。 
        * ***邊***用來排序節點，使其在前一個步驟完成後執行，並可使用前一個步驟的輸出欄位。當節點在 `previous_node_input` 對應中包含參照前一個節點工作流程步驟的鍵時，系統會在剖析期間自動將對應的邊加入範本，因此為求簡潔可以省略。

## 後續步驟

- 如需支援的 API，請參閱[工作流程 API]({{site.url}}{{site.baseurl}}/automating-configurations/api/index/)。
- 如需工作流程步驟語法，請參閱[工作流程步驟]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-steps/)。  
- 如需完整範例，請參閱[工作流程教學]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-tutorial/)。
- 如需可設定的設定，請參閱[工作流程設定]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-settings/)。
- 如需工作流程存取控制的相關資訊，請參閱[工作流程範本安全性]({{site.url}}{{site.baseurl}}/automating-configurations/workflow-security/)。