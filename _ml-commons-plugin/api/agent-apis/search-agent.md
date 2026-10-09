---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搜尋代理程式"
parent: Agent APIs
grand_parent: ML Commons APIs
nav_order: 35
---

# Search Agent API
**於 2.13 版導入**
{: .label .label-purple }

使用此命令搜尋您已建立的代理程式。您可以在請求本文中提供任何 OpenSearch 搜尋查詢。

## 端點

```json
GET /_plugins/_ml/agents/_search
POST /_plugins/_ml/agents/_search
```

## 範例請求：搜尋所有代理程式

```json
POST /_plugins/_ml/agents/_search
{
  "query": {
    "match_all": {}
  },
  "size": 1000
}
```
{% include copy-curl.html %}

## 範例請求：搜尋特定類型的代理程式

```json
POST /_plugins/_ml/agents/_search
{
  "query": {
    "term": {
      "type": {
        "value": "flow"
      }
    }
  }
}
```
{% include copy-curl.html %}

#### 範例：依描述搜尋代理程式

```json
GET _plugins/_ml/agents/_search
{
  "query": {
    "bool": {
      "should": [
        {
          "match": {
            "description": "test agent"
          }
        }
      ]
    }
  },
  "size": 1000
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "took": 2,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 6,
      "relation": "eq"
    },
    "max_score": 0.15019803,
    "hits": [
      {
        "_index": ".plugins-ml-agent",
        "_id": "8HXlkI0BfUsSoeNTP_0P",
        "_version": 1,
        "_seq_no": 17,
        "_primary_term": 2,
        "_score": 0.13904166,
        "_source": {
          "created_time": 1707532959502,
          "last_updated_time": 1707532959502,
          "name": "Test_Agent_For_RagTool",
          "description": "this is a test flow agent",
          "type": "flow",
          "tools": [
            {
              "description": "A description of the tool",
              "include_output_in_agent_response": false,
              "type": "RAGTool",
              "parameters": {
                "inference_model_id": "gnDIbI0BfUsSoeNT_jAw",
                "embedding_model_id": "Yg7HZo0B9ggZeh2gYjtu_2",
                "input": "${parameters.question}",
                "source_field": """["text"]""",
                "embedding_field": "embedding",
                "index": "my_test_data",
                "query_type": "neural",
                "prompt": """

Human:You are a professional data analyst. You will always answer question based on the given context first. If the answer is not directly shown in the context, you will analyze the data and find the answer. If you don't know the answer, just say don't know. 

 Context:
${parameters.output_field}

Human:${parameters.question}

Assistant:"""
              }
            }
          ]
        }
      }
    ]
  }
}
```

## 回應本文欄位

回應欄位的說明請參閱 [Register Agent API 請求欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent#request-body-fields)。
