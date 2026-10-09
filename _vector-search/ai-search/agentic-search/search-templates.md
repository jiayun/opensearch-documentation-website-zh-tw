---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "新增搜尋範本"
parent: Agentic search
grand_parent: AI search
nav_order: 100
has_children: false
---

# 新增搜尋範本

`QueryPlanningTool` 在註冊時可以接受一份[搜尋範本]({{site.url}}{{site.baseurl}}/search-plugins/search-template/)清單。在搜尋期間，`QueryPlanningTool` 會根據使用者的問題與範本描述選擇合適的搜尋範本，並由大型語言模型 (LLM) 根據所選的搜尋範本產生查詢。

這種做法讓您能解決原本單靠 LLM 難以處理的複雜使用情境：

- 提升代理程式搜尋中查詢回應的一致性。Query DSL 查詢的大部分內容由搜尋範本提供，LLM 僅提供少部分內容或填入預留位置。
- 處理 LLM 難以產生正確查詢的複雜使用情境。
- 確保查詢結構與命名慣例可預期。

## 最佳做法

為代理程式搜尋建立搜尋範本時，請遵循下列準則：

- 為每個範本撰寫詳細的描述，協助 LLM 做出適當選擇。
- 使用具描述性的預留位置名稱，清楚指出應填入的內容。
- 為您常用的不同查詢模式建立範本。
- 在部署前驗證範本在各種輸入下皆能正確運作。

## 步驟 1：建立索引

建立一個包含巢狀庫存資料的 stores 索引，以示範複雜的彙總情境：

```json
PUT /stores
{
  "mappings": {
    "properties": {
      "store_id": { "type": "keyword" },
      "name": { "type": "text", "fields": { "keyword": { "type": "keyword", "ignore_above": 256 } } },
      "address": {
        "properties": {
          "city": { "type": "keyword" },
          "state": { "type": "keyword" }
        }
      },
      "location": { "type": "geo_point" },
      "inventory": {
        "type": "nested",
        "properties": {
          "sku": { "type": "keyword" },
          "qty": { "type": "integer" }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 2：匯入文件

新增包含不同城市與產品庫存資料的範例商店文件：

```json
POST /_bulk
{ "index": { "_index": "stores", "_id": "S-SEA-001" } }
{ "store_id": "S-SEA-001", "name": "Downtown Seattle", "address": { "city": "Seattle", "state": "WA" }, "location": { "lat": 47.608, "lon": -122.335 }, "inventory": [ { "sku": "iphone_17_air", "qty": 12 }, { "sku": "iphone_17", "qty": 11 }, { "sku": "vision_pro", "qty": 3 } ] }
{ "index": { "_index": "stores", "_id": "S-SEA-002" } }
{ "store_id": "S-SEA-002", "name": "Capitol Hill", "address": { "city": "Seattle", "state": "WA" }, "location": { "lat": 47.623, "lon": -122.319 }, "inventory": [ { "sku": "iphone_17_air", "qty": 5 }, { "sku": "iphone_17", "qty": 25 }, { "sku": "vision_pro", "qty": 4 } ] }
{ "index": { "_index": "stores", "_id": "S-SEA-003" } }
{ "store_id": "S-SEA-003", "name": "South Lake Union", "address": { "city": "Seattle", "state": "WA" }, "location": { "lat": 47.626, "lon": -122.338 }, "inventory": [ { "sku": "iphone_17_air", "qty": 6 }, { "sku": "iphone_17", "qty": 9 }, { "sku": "vision_pro", "qty": 20 } ] }
{ "index": { "_index": "stores", "_id": "S-BEL-001" } }
{ "store_id": "S-BEL-001", "name": "Bellevue Square", "address": { "city": "Bellevue", "state": "WA" }, "location": { "lat": 47.616, "lon": -122.203 }, "inventory": [ { "sku": "iphone_17_air", "qty": 14 }, { "sku": "iphone_17", "qty": 4 }, { "sku": "vision_pro", "qty": 1 } ] }
{ "index": { "_index": "stores", "_id": "S-SEA-004" } }
{ "store_id": "S-SEA-004", "name": "Ballard", "address": { "city": "Seattle", "state": "WA" }, "location": { "lat": 47.668, "lon": -122.382 }, "inventory": [ { "sku": "iphone_17_air", "qty": 9 }, { "sku": "iphone_17", "qty": 7 }, { "sku": "vision_pro", "qty": 12 } ] }

```
{% include copy-curl.html %}

## 步驟 3：註冊搜尋範本

註冊一個搜尋範本，用於傳回某城市中三個 SKU 合計庫存達到最低門檻的商店：

```json
POST /_scripts/store_sum_skus
{
  "script": {
    "lang": "mustache",
    "source": {
      "size": 0,
      "query": { "term": { "address.city": "{% raw %}{{city}}{% endraw %}" } },
      "aggs": {
        "by_store": {
          "terms": {
            "field": "store_id",
            "size": "{% raw %}{{bucket_size}}{{^bucket_size}}200{{/bucket_size}}{% endraw %}",
            "order": { "inv>skus>q": "desc" }
          },
          "aggs": {
            "inv": {
              "nested": { "path": "inventory" },
              "aggs": {
                "skus": {
                  "filter": { "terms": { "inventory.sku": ["{% raw %}{{sku1}}{% endraw %}","{% raw %}{{sku2}}{% endraw %}","{% raw %}{{sku3}}{% endraw %}"] } },
                  "aggs": { "q": { "sum": { "field": "inventory.qty" } } }
                }
              }
            },
            "keep": {
              "bucket_selector": {
                "buckets_path": { "t": "inv>skus>q" },
                "script": { "source": "params.t >= {% raw %}{{min_total}}{{^min_total}}30{{/min_total}}{% endraw %}" }
              }
            },
            "store": {
              "top_hits": {
                "size": 1,
                "_source": { "includes": ["store_id","name","address.city"] }
              }
            }
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

註冊一個搜尋範本，用於計算某城市中特定 SKU 數量至少達到最低數量的商店數：

```json
POST /_scripts/stores_with_give_sku
{
  "script": {
    "lang": "mustache",
    "source": {
      "size": 0,
      "query": { "term": { "address.city": "{% raw %}{{city}}{% endraw %}" } },
      "aggs": {
        "s": {
          "terms": {
            "field": "store_id",
            "size": "{% raw %}{{bs}}{{^bs}}200{{/bs}}{% endraw %}"
          },
          "aggs": {
            "i": {
              "nested": { "path": "inventory" },
              "aggs": {
                "f": {
                  "filter": { "term": { "inventory.sku": "{% raw %}{{sku}}{% endraw %}" } },
                  "aggs": { "q": { "sum": { "field": "inventory.qty" } } }
                }
              }
            },
            "m": {
              "bucket_script": {
                "buckets_path": { "x": "i>f>q" },
                "script": { "source": "{% raw %}params.x >= {{min}}{{^min}}10{{/min}} ? 1 : 0{% endraw %}" }
              }
            }
          }
        },
        "cnt": { "sum_bucket": { "buckets_path": "s>m" } }
      }
    }
  }
}
```
{% include copy-curl.html %}

## 步驟 4：使用 QueryPlanningTool 註冊代理程式

接下來，使用 `QueryPlanningTool` 註冊一個代理程式，並設定該工具使用您的搜尋範本。

### 步驟 4(a)：為代理程式與 QueryPlanningTool 建立模型

為對話式代理程式與 `QueryPlanningTool` 註冊一個模型：

```json
POST /_plugins/_ml/models/_register
{
  "name": "My OpenAI model: gpt-5",
  "function_name": "remote",
  "description": "Model for agentic search with templates",
  "connector": {
    "name": "My openai connector: gpt-5",
    "description": "The connector to openai chat model",
    "version": 1,
    "protocol": "http",
    "parameters": {
      "model": "gpt-5"
    },
    "credential": {
      "openAI_key": "<OPEN AI KEY>"
    },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "headers": {
          "Authorization": "Bearer ${credential.openAI_key}"
        },
        "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\":\"developer\",\"content\":\"${parameters.system_prompt}\"},${parameters._chat_history:-}{\"role\":\"user\",\"content\":\"${parameters.user_prompt}\"}${parameters._interactions:-}], \"reasoning_effort\":\"low\"${parameters.tool_configs:-}}"
      }
    ]
  }
}
```
{% include copy-curl.html %}

### 步驟 4(b)：使用搜尋範本註冊代理程式

使用已設定為使用您搜尋範本的 `QueryPlanningTool` 註冊代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Store Search Agent with Templates",
  "type": "conversational",
  "description": "Agent for store inventory searches using templates",
  "llm": {
    "model_id": "your-model-id-from-step-4a",
    "parameters": {
      "max_iteration": 15
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "openai/v1/chat/completions"
  },
  "tools": [
    {
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "your-model-id-from-step-4a",
        "generation_type": "user_templates",
        "search_templates": [
          {
            "template_id": "store_sum_skus",
            "template_description": "Return stores in a given city where the combined quantity across a list of SKUs meets or exceeds a threshold."
          },
          {
            "template_id": "stores_with_give_sku",
            "template_description": "List stores in a given city that have at least min_qty units of a specific SKU."
          }
        ]
      }
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy-curl.html %}

## 步驟 5：建立搜尋管線

建立使用您代理程式與搜尋範本的搜尋管線：

```json
PUT _search/pipeline/agentic-pipeline
{
    "request_processors": [
        {
            "agentic_query_translator": {
                "agent_id": "your-agent-id-from-step-4b"
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

## 步驟 6：測試複雜問題

傳送需要進階彙總的複雜查詢：

```json
POST /stores/_search?search_pipeline=agentic-pipeline
{
  "query": {
    "agentic": {
      "query_text": "List all stores in Seattle that have at least 30 combined units across these SKUs: iphone_17_air, iphone_17, and vision_pro."
    }
  }
}
```
{% include copy-curl.html %}

若沒有搜尋範本，涉及進階彙總與指令碼的複雜查詢經常會失敗，因為 LLM 難以產生正確的語法。例如，如果您在步驟 4(b) 建立代理程式時未新增搜尋範本，前述請求會傳回類似以下的指令碼執行錯誤：

<details markdown="block">
  <summary>
    錯誤回應
  </summary>
  {: .text-delta}

```json
{
  "error": {
    "root_cause": [
      {
        "type": "script_exception",
        "reason": "runtime error",
        "script_stack": [
          "for (item in params._source.inventory) { ",
          "                           ^---- HERE"
        ],
        "script": "int total = 0; for (item in params._source.inventory) { if (params.skus.contains(item.sku)) { if (item.qty instanceof Integer || item.qty instanceof Long) { total += (int)item.qty; } else if (item.qty instanceof String) { try { total += Integer.parseInt(it ...",
        "lang": "painless",
        "position": {
          "offset": 42,
          "start": 15,
          "end": 56
        }
      }
    ],
    "type": "search_phase_execution_exception",
    "reason": "all shards failed",
    "phase": "query",
    "grouped": true,
    "failed_shards": [
      {
        "shard": 0,
        "index": "stores",
        "node": "u3NEXA8PS8W8EJcT_9suGg",
        "reason": {
          "type": "script_exception",
          "reason": "runtime error",
          "script_stack": [
            "for (item in params._source.inventory) { ",
            "                           ^---- HERE"
          ],
          "script": "int total = 0; for (item in params._source.inventory) { if (params.skus.contains(item.sku)) { if (item.qty instanceof Integer || item.qty instanceof Long) { total += (int)item.qty; } else if (item.qty instanceof String) { try { total += Integer.parseInt(it ...",
          "lang": "painless",
          "position": {
            "offset": 42,
            "start": 15,
            "end": 56
          },
          "caused_by": {
            "type": "null_pointer_exception",
            "reason": "Cannot invoke \"Object.getClass()\" because \"callArgs[0]\" is null"
          }
        }
      }
    ]
  },
  "status": 400
}
```

</details>

然而，有了搜尋範本，代理程式便能藉由選取適當的範本並填入參數來處理精密的查詢。LLM 會正確識別並使用 `store_sum_skus` 範本，填入範本參數（例如 `city: "Seattle"` 和 `sku1: "iphone_17_air"`），並產生含有巢狀彙總與桶選取器的有效查詢。回應包含庫存合計 ≥ 30 個單位的商店（`S-SEA-002` 和 `S-SEA-003`）：

```json
{
  "took": 21658,
  "timed_out": false,
  "terminated_early": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 4,
      "relation": "eq"
    },
    "max_score": null,
    "hits": []
  },
  "aggregations": {
    "by_store": {
      "doc_count_error_upper_bound": 0,
      "sum_other_doc_count": 0,
      "buckets": [
        {
          "key": "S-SEA-002",
          "doc_count": 1,
          "inv": {
            "doc_count": 3,
            "skus": {
              "doc_count": 3,
              "sum_qty": {
                "value": 34.0
              }
            }
          },
          "store": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 1.0,
              "hits": [
                {
                  "_index": "stores",
                  "_id": "S-SEA-002",
                  "_score": 1.0,
                  "_source": {
                    "store_id": "S-SEA-002",
                    "address": {
                      "city": "Seattle"
                    },
                    "name": "Capitol Hill"
                  }
                }
              ]
            }
          }
        },
        {
          "key": "S-SEA-003",
          "doc_count": 1,
          "inv": {
            "doc_count": 3,
            "skus": {
              "doc_count": 3,
              "sum_qty": {
                "value": 35.0
              }
            }
          },
          "store": {
            "hits": {
              "total": {
                "value": 1,
                "relation": "eq"
              },
              "max_score": 1.0,
              "hits": [
                {
                  "_index": "stores",
                  "_id": "S-SEA-003",
                  "_score": 1.0,
                  "_source": {
                    "store_id": "S-SEA-003",
                    "address": {
                      "city": "Seattle"
                    },
                    "name": "South Lake Union"
                  }
                }
              ]
            }
          }
        }
      ]
    }
  },
  "ext": {
    "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\nFirst I used: query_planner_tool — qpt.question: \"List all stores in Seattle that have at least a combined total of 30 units across the following SKUs: \\\"iphone_17_air\\\", \\\"iphone_17\\\", and \\\"vision_pro\\\". The location must be Seattle. Sum the inventory counts for only these three SKUs per store and return stores where the sum is greater than or equal to 30.\"; index_name_provided: \"stores\"\nValidation: qpt output is valid JSON; adjusted numeric literals to integers and sizes to integers.",
    "memory_id": "-BxpmJkB-5P992SCQ-qU",
    "dsl_query":"{\"size\":0.0,\"query\":{\"term\":{\"address.city\":\"Seattle\"}},\"aggs\":{\"by_store\":{\"terms\":{\"field\":\"store_id\",\"size\":200.0},\"aggs\":{\"inv\":{\"nested\":{\"path\":\"inventory\"},\"aggs\":{\"skus\":{\"filter\":{\"terms\":{\"inventory.sku\":[\"iphone_17_air\",\"iphone_17\",\"vision_pro\"]}},\"aggs\":{\"sum_qty\":{\"sum\":{\"field\":\"inventory.qty\"}}}}}},\"keep\":{\"bucket_selector\":{\"buckets_path\":{\"total\":\"inv\>skus\>sum_qty\"},\"script\":{\"source\":\"params.total \>\= 30\"}}},\"store\":{\"top_hits\":{\"size\":1.0,\"_source\":{\"includes\":[\"store_id\",\"name\",\"address.city\"]}}}}}}}"
  }
}
```

## 相關文件

- [搜尋範本]({{site.url}}{{site.baseurl}}/search-plugins/search-template/)
