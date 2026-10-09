---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Agentic 查詢轉譯器"
nav_order: 5
has_children: false
parent: Search processors
grand_parent: Search pipelines
---

# Agentic 查詢轉譯處理器
**3.2 版新增**
{: .label .label-purple }

`agentic_query_translator` 搜尋請求處理器透過機器學習 (ML) 代理程式，將使用者的查詢轉譯為 OpenSearch 查詢領域特定語言 (DSL) 查詢，以啟用自然語言搜尋。它可與 [agentic 搜尋查詢]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)搭配，提供對話式搜尋功能：

1. 處理器將使用者的自然語言查詢傳送至指定的 ML 代理程式。
2. 代理程式將查詢轉譯為 OpenSearch DSL。
3. 原始查詢會被產生的 DSL 查詢取代。

此處理器僅支援 `agentic` 查詢類型作為頂層查詢。
{: .note}

## 必要條件

使用 `agentic_query_translator` 處理器之前，您必須先設定對話代理程式或流程代理程式。如需更多資訊，請參閱 [代理程式]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/index/)。

## 請求本文欄位

下表列出所有可用的請求欄位。

欄位 | 資料類型 | 必要／選用 | 說明
:--- | :--- | :--- | :---
`agent_id` | 字串 | 必要 | 將自然語言查詢轉譯為 DSL 查詢的 ML 代理程式 ID。
`embedding_model_id` | 字串 | 選用 | 使用 `neural` 查詢為語意搜尋產生向量嵌入的嵌入模型 ID。此參數的優先順序高於代理程式組態中指定的 `embedding_model_id`。如需更多資訊，請參閱 [設定代理程式以進行語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/neural-search/)。


## 範例

以下範例請求建立一個包含 `agentic_query_translator` 處理器的搜尋管線：

```json
PUT /_search/pipeline/agentic_search_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id-here"
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要啟用語意搜尋功能，您可以選擇性地為將查詢轉換為向量嵌入的文字嵌入模型指定 `embedding_model_id`：

```json
PUT /_search/pipeline/agentic_search_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "your-agent-id-here",
        "embedding_model_id": "your-embedding-model-id"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 使用方式

若要使用此處理器，請執行 `agentic` 查詢：

```json
POST /your-index/_search?search_pipeline=agentic_search_pipeline
{
    "query": {
        "agentic": {
            "query_text": "Show me shoes in white color"
        }
    }
}
```
{% include copy-curl.html %}

回應包含符合的文件：

```json
{
    "took": 6031,
    "timed_out": false,
    "_shards": {
        "total": 8,
        "successful": 8,
        "skipped": 0,
        "failed": 0
    },
    "hits": {
        "total": {
            "value": 8,
            "relation": "eq"
        },
        "max_score": 0.0,
        "hits": [
            {
                "_index": "products-index",
                "_id": "43",
                "_score": 0.0,
                "_source": {
                    "product_name": "Nike Air Max white",
                    "description": "Red cushioned sneakers",
                    "price": 140.0,
                    "currency": "USD",
                    "in_stock": true,
                    "color": "white",
                    "size": "10",
                    "product_id": "P6001",
                    "category": "shoes",
                    "brand": "Nike"
                }
            },
            {
                "_index": "products-index",
                "_id": "45",
                "_score": 0.0,
                "_source": {
                    "product_name": "Adidas Superstar white",
                    "description": "Classic black sneakers",
                    "price": 100.0,
                    "currency": "USD",
                    "in_stock": true,
                    "color": "white",
                    "size": "8",
                    "product_id": "P6003",
                    "category": "shoes",
                    "brand": "Adidas"
                }
            }
        ]
    }
}
```

## 相關文件

- [Agentic 搜尋查詢]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)
- [Agentic 查詢]({{site.url}}{{site.baseurl}}/query-dsl/specialized/agentic/)
- [設定代理程式以進行語意搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/neural-search/)
- [Agentic 脈絡處理器]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/agentic-context-processor/)