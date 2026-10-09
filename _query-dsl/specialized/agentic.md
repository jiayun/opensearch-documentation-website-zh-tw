---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理式"
parent: AI and vector search queries
nav_order: 2
---

# 代理式查詢
**3.2 版新增**
{: .label .label-purple }

使用 `agentic` 查詢以自然語言提問，並讓 OpenSearch 自動規劃與執行檢索。`agentic` 查詢會與預先設定的代理程式搭配運作，該代理程式會讀取問題、規劃搜尋並傳回相關結果。如需代理式搜尋的更多資訊，請參閱 [代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)。

## 必要條件

使用 `agentic` 查詢之前，您必須符合下列必要條件：

1. 使用 [`QueryPlanningTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/query-planning-tool/) 設定代理程式。`QueryPlanningTool` 是從自然語言問題產生 Query DSL 查詢的必要工具。您也可以選擇為代理程式設定其他工具以增強功能。
1. 建立包含 [`agentic_query_translator` 搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/) 的搜尋管線。

如需詳細的設定說明，請參閱 [代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)。

## 請求本文欄位

`agentic` 查詢接受下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`query_text` | 字串 | 必要 | 要由代理程式回答的自然語言問題。
`query_fields` | 陣列 | 選用 | 代理程式在產生搜尋查詢時應考慮的索引欄位清單。若省略，代理程式會根據索引對應與內容推斷適用的欄位。
`memory_id` | 字串 | 選用 | 僅適用於 `conversational` 代理程式。提供先前回應中的對話記憶 ID，以便沿用先前的對話脈絡。請參閱 [使用對話式代理程式進行代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-converse/)。 |

## 範例

下列範例使用 `agentic` 查詢，針對 `iris` 資料集中的花卉提出自然語言問題。在此範例中，`query_text` 包含自然語言問題，`query_fields` 指定產生查詢時要使用的欄位，而 `search-pipeline` 查詢參數指定包含代理式查詢轉譯處理器的搜尋管線：

```json
GET /iris-index/_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "List all the flowers present",
      "query_fields": ["species", "petal_length_in_cm"]
    }
  }
}
```
{% include copy-curl.html %}

執行時，代理式搜尋請求會執行下列步驟：

1. 將自然語言問題連同索引對應與預設提示傳送至大型語言模型 (LLM)。
2. LLM 根據輸入產生 Query DSL 查詢。
3. 產生的 DSL 查詢會在 OpenSearch 中作為搜尋請求執行。
4. 根據產生的查詢傳回搜尋結果。

如需完整範例，請參閱 [代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)。

## 後續步驟

- 了解如何在 [代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/) 中設定代理式搜尋。
- 在 [代理程式類型]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/#agent-types) 中了解代理程式類型。
- 了解 [`QueryPlanningTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/query-planning-tool/)。
- 檢視 [`agentic_query_translator` 搜尋請求處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/) 的參考文件。