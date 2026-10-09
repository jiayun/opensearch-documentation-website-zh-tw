---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "代理式上下文"
nav_order: 2
has_children: false
parent: Search processors
grand_parent: Search pipelines
---

# 代理式上下文處理器
**於 3.3 版推出**
{: .label .label-purple }

`agentic_context` 搜尋回應處理器會將代理程式執行上下文資訊新增至搜尋回應擴充項目。此處理器與[代理式查詢轉譯器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/)搭配運作，以呈現代理程式的查詢轉譯過程並維持對話連續性：

1. 處理器會從管線處理上下文擷取代理程式上下文資訊。
2. 根據處理器組態，選擇性地在回應中包含代理程式步驟摘要與查詢領域專用語言（DSL）查詢。
3. 若有記憶 ID，則一律包含，以維持對話連續性。
4. 上下文資訊會新增至搜尋回應擴充項目。
5. 類型驗證可確保所有上下文屬性都是字串。

此處理器可搭配對話式代理程式與流程代理程式運作，但可用的上下文資訊會因代理程式類型而異。流程代理程式僅提供 `dsl_query`（產生的 DSL），而對話式代理程式則提供 `dsl_query`、`memory_id` 和 `agent_steps_summary`。如需詳細資訊，請參閱[代理程式類型]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/#agent-types)。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`agent_steps_summary` | 布林值 | 是否在回應中包含代理程式的執行步驟摘要。僅適用於對話式代理程式。選用。預設為 `false`。 
`dsl_query` | 布林值 | 是否在回應中包含產生的 DSL 查詢。適用於對話式代理程式與流程代理程式。選用。預設為 `false`。 

## 回應欄位

啟用時，處理器會將下列欄位新增至搜尋回應擴充項目。

欄位 | 說明
:--- | :---
`agent_steps_summary` | 代理程式轉譯自然語言查詢時所採取的步驟摘要（當 `agent_steps_summary` 為 `true` 時包含）。僅適用於對話式代理程式。
`memory_id` | 用於在不同查詢之間維持上下文的對話記憶 ID。僅適用於對話式代理程式。只有在您想要繼續先前的對話時，才在 `agentic` 查詢中提供此值。
`dsl_query` | 已執行的產生之 DSL 查詢（當 `dsl_query` 為 `true` 時包含）。適用於對話式代理程式與流程代理程式。

## 範例

下列範例請求會建立具有 `agentic_context` 回應處理器的搜尋管線：

```json
PUT /_search/pipeline/agentic_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id"
      }
    }
  ],
  "response_processors": [
    {
      "agentic_context": {
        "agent_steps_summary": true,
        "dsl_query": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

使用設定好的管線執行搜尋：

```json
POST /your-index/_search?search_pipeline=agentic_search_pipeline
{
    "query": {
        "agentic": {
            "query_text": "Show me shoes in white color",
            "memory_id": "your memory id"
        }
    }
}
```
{% include copy-curl.html %}

回應包含代理程式轉譯查詢時所採取的步驟、記憶 ID，以及改寫後的 DSL 查詢：

```json
{
  "took": 15,
  "hits": {
    "_shards": {...},
    "hits": [...]
  },
   "ext": {
        "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\\nFirst I used: ListIndexTool — input: \"\"; context gained: \"Discovered products-index which seems relevant for products and pricing context\"\\nSecond I used: IndexMappingTool — input: \"products-index\"; context gained: \"Confirmed presence of category and price fields in products-index\"\\nThird I used: query_planner_tool — qpt.question: \"Show me shoes that cost exactly 100 dollars.\"; index_name_provided: \"products-index\"\\nValidation: qpt output is valid and accurately reflects the request for shoes priced at 100 dollars.",
        "memory_id": "WVhHiJkBnqovov2plcDH",
        "dsl_query": "{\"query\":{\"bool\":{\"filter\":[{\"term\":{\"category\":\"shoes\"}},{\"term\":{\"price\":100.0}}]}}}"
    }
}
```

## 相關文件

- [代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)
- [代理式查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/agentic/)
- [代理式查詢轉譯器處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-query-translator-processor/)