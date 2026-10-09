---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢規劃工具"
has_children: false
has_toc: false
nav_order: 50
parent: Tools
grand_parent: Agents and tools
---

<!-- vale off -->
# 查詢規劃工具
**於 3.3 版推出**
{: .label .label-purple }
<!-- vale on -->

`QueryPlanningTool` 會從自然語言問題產生 OpenSearch 查詢領域特定語言 (DSL) 查詢。它是 [代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/) 的核心元件，可透過代理程式驅動的工作流程進行自然語言查詢處理。

`QueryPlanningTool` 支援兩種從自然語言問題產生 DSL 查詢的方法：

- **僅使用 LLM 知識 (預設)**：大型語言模型 (LLM) 僅使用其訓練知識以及您提供的任何系統/使用者提示來產生查詢。此方法完全仰賴模型對 DSL 語法的理解以及您特定的提示指示。

- **使用搜尋範本**：LLM 在產生查詢時，會使用預先定義的搜尋範本作為額外的上下文。您提供一組附有說明的搜尋範本，LLM 會將這些範本當作範例和指引，以建立更精確的查詢。如果 LLM 判斷提供的範本都不適合使用者的問題，LLM 會嘗試自行產生查詢。

當您已為特定使用案例或領域建立查詢模式時，使用搜尋範本特別有用：它有助於 LLM 產生遵循您偏好結構的查詢，並使用您索引對應中適當的欄位名稱。

## 步驟 1：建立索引並匯入範例資料

首先，為 `iris` 資料集建立索引：

```json
PUT /iris-index
{
  "mappings": {
    "properties": {
      "petal_length_in_cm": {
        "type": "float"
      },
      "petal_width_in_cm": {
        "type": "float"
      },
      "sepal_length_in_cm": {
        "type": "float"
      },
      "sepal_width_in_cm": {
        "type": "float"
      },
      "species": {
        "type": "text",
        "fields": {
          "keyword": {
            "type": "keyword",
            "ignore_above": 256
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，將範例文件匯入索引：

```json
POST _bulk
{ "index": { "_index": "iris-index", "_id": "1" } }
{ "petal_length_in_cm": 1.4, "petal_width_in_cm": 0.2, "sepal_length_in_cm": 5.1, "sepal_width_in_cm": 3.5, "species": "setosa" }
{ "index": { "_index": "iris-index", "_id": "2" } }
{ "petal_length_in_cm": 4.5, "petal_width_in_cm": 1.5, "sepal_length_in_cm": 6.4, "sepal_width_in_cm": 2.9, "species": "versicolor" }
{ "index": { "_index": "iris-index", "_id": "3" } }
{ "petal_length_in_cm": 6.0, "petal_width_in_cm": 2.5, "sepal_length_in_cm": 5.9, "sepal_width_in_cm": 3.0, "species": "virginica" }
```
{% include copy-curl.html %}

## 步驟 2：註冊並部署模型

下列請求會從 Amazon Bedrock 註冊遠端模型，並將其部署到您的叢集。此 API 呼叫會一步建立連接器和模型。請將 `region`、`access_key`、`secret_key` 和 `session_token` 替換為您自己的值。您可以使用任何支援 `converse` API 的模型，例如 [Anthropic Claude 4](https://www.anthropic.com/news/claude-4) 或 [GPT 5](https://openai.com/index/introducing-gpt-5)。您也可以建立此模型的連接器，以使用其他模型供應商 (請參閱 [連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/))。

**重要**：為 `QueryPlanningTool` 建立連接器時，請求本文必須包含 `system_prompt` 和 `user_prompt` 參數。此工具需要這些參數，才能將系統和使用者提示正確注入模型的請求中。

下列範例會註冊並部署 Anthropic Claude 4 模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Claude 4 Sonnet Query Planner Tool Model",
  "function_name": "remote",
  "description": "Claude 4 sonnet for Query Planning",
  "connector": {
    "name": "Bedrock Claude 4 Sonnet Connector",
    "description": "Amazon Bedrock connector for Claude 4 Sonnet",
    "version": 1,
    "protocol": "aws_sigv4",
    "parameters": {
      "region": "us-east-1",
      "service_name": "bedrock",
      "model": "us.anthropic.claude-sonnet-4-20250514-v1:0"
    },
    "credential": {
      "access_key": "your-aws-access-key",
      "secret_key": "your-aws-secret-key",
      "session_token": "your-aws-session-token"
    },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
        "headers": {
          "content-type": "application/json"
        },
        "request_body": "{ \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": [${parameters._chat_history:-}{\"role\":\"user\",\"content\":[{\"text\":\"${parameters.user_prompt}\"}]}${parameters._interactions:-}]${parameters.tool_configs:-} }"
      }
    ]
  }
}
```
{% include copy-curl.html %}

下列範例會註冊並部署 OpenAI GPT 5 模型：

```json
POST /_plugins/_ml/models/_register
{
    "name": "My OpenAI model: gpt-5",
    "function_name": "remote",
    "description": "test model",
    "connector": {
        "name": "My openai connector: gpt-5",
        "description": "The connector to openai chat model",
        "version": 1,
        "protocol": "http",
        "parameters": {
            "model": "gpt-5"
        },
        "credential": {
            "openAI_key": "your-openai-api-key"
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

OpenSearch 會回應模型 ID：

```json
{
  "task_id": "_9iSxJgBOh0h20Y9XYTH",
  "status": "CREATED",
  "model_id": "ANiSxJgBOh0h20Y9XYXl"
}
```

## 步驟 3：註冊代理程式

您可以使用任何 [OpenSearch 代理程式類型]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/agents/) 來執行 `QueryPlanningTool`。下列範例使用 `flow` 代理程式，它會依序執行一連串工具，並傳回最後一個工具的輸出。

### 僅使用 LLM 知識

若只要使用提示，請不要指定 `generation_type`，如此一來它會預設為 `llmGenerated`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Agentic Search with Claude 4",
  "type": "flow",
  "description": "A test agent for query planning.",
  "tools": [
    {
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "ANiSxJgBOh0h20Y9XYXl"
      }
    }
  ]
}
```
{% include copy-curl.html %}

註冊代理程式時，您可以覆寫在模型註冊期間指定的參數，例如 `system_prompt` 和 `user_prompt`。

### 使用搜尋範本

您可以新增[搜尋範本]({{site.url}}{{site.baseurl}}/api-reference/search-apis/search-template/index/)作為額外的上下文，協助 LLM 產生 OpenSearch DSL。

首先，建立搜尋範本：

```json
POST /_scripts/flower_species_search_template
{
  "script": {
    "lang": "mustache",
    "source": {
      "from": "{% raw %} {{from}}{{^from}}0{{/from}} {% endraw %} ",
      "size": "{% raw %} {{size}}{{^size}}10{{/size}} {% endraw %} ",
      "query": {
        "match": {
          "species": "{% raw %} {{species}} {% endraw %} "
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
POST /_scripts/flower_petal_length_range_template
{
  "script": {
    "lang": "mustache",
    "source": {
      "from": "{% raw %} {{from}}{{^from}}0{{/from}} {% endraw %} ",
      "size": "{% raw %} {{size}}{{^size}}10{{/size}} {% endraw %} ",
      "query": {
        "range": {
          "petal_length_in_cm": {
            "gte": "{% raw %} {{min_length}} {% endraw %} ",
            "lte": "{% raw %} {{max_length}} {% endraw %} "
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

接著，註冊代理程式，將 `generation_type` 設為 `user_templates`，並在 `search_templates` 參數中提供每個範本的 `template_id` 和 `template_description`：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Agentic Search with Claude 4",
  "type": "flow",
  "description": "A test agent for query planning.",
  "tools": [
    {
      "type": "QueryPlanningTool",
      "description": "A general tool to answer any question",
      "parameters": {
        "model_id": "ANiSxJgBOh0h20Y9XYXl",
        "generation_type": "user_templates",
        "search_templates": [
          {
            "template_id": "flower_species_search_template",
            "template_description": "This template searches for flowers that match the given species using a match query."
          },
          {
            "template_id": "flower_petal_length_range_template",
            "template_description": "This template searches for flowers within a specific petal length range using a range query."
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

LLM 僅使用 `template_description` 作為上下文，協助它在根據使用者提供的 `question` 產生 OpenSearch DSL 查詢時，選擇最適合的範本。請務必提供清楚的範本說明，協助 LLM 做出適當的選擇。請注意，LLM 不會直接填入範本變數或呈現範本；它會分析範本的查詢結構，並以此為指引，產生符合上下文的新 OpenSearch DSL 查詢。

如需參數說明，請參閱[註冊參數](#register-parameters)。

OpenSearch 會回應代理程式 ID：

```json
{
  "agent_id": "RNjQi5gBOh0h20Y9-RX1"
}
```

## 步驟 4：執行代理程式

傳送下列請求以執行代理程式：

```json
POST /_plugins/_ml/agents/RNjQi5gBOh0h20Y9-RX1/_execute
{
  "parameters": {
    "question": "How many iris flowers of type setosa are there?",
    "index_name": "iris-index"
  }
}
```
{% include copy-curl.html %}

OpenSearch 會傳回推論結果，其中包含產生的 Query DSL：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": "{'query':{'term':{'species':'setosa'}}}"
        }
      ]
    }
  ]
}
```

## 註冊參數

下表列出註冊代理程式時可用的所有工具參數。

參數	| 類型 | 必要/選用 | 說明	
:--- | :--- | :--- | :---
`model_id` | 字串 | 必要 | 用於產生 Query DSL 的 LLM 模型 ID。在 `conversational` 代理程式中使用時，若未提供此值，預設會使用代理程式本身的 `llm.model_id`。
`response_filter` | 字串 | 選用 | 用於從 LLM 回應中擷取所產生查詢的 JSONPath 運算式。
`generation_type` | 字串 | 選用 | 決定如何產生查詢。使用 `llmGenerated` 可僅依賴 LLM 的內建知識，或使用 `user_templates` 提供預先定義的搜尋範本，引導查詢產生以取得一致的結果。預設為 `llmGenerated`。
`query_planner_system_prompt` | 字串 | 選用 | 向 LLM 提供高層級指示的系統提示。
`query_planner_user_prompt` | 字串 | 選用 | 定義如何將自然語言問題和上下文呈現給 LLM，以產生查詢的使用者提示範本。
`search_templates` | 陣列 | 選用 | 僅在 `generation_type` 為 `user_templates` 時適用。搜尋範本清單，為 LLM 提供預先定義的查詢模式，以產生 Query DSL。每個範本都必須包含 `template_id`（唯一識別碼）和 `template_description`（說明範本的用途與使用案例，協助 LLM 做出適當的選擇）。
`fallback_query` | 字串 | 選用 | 當 LLM 無法針對指定的查詢文字產生有效的 DSL 查詢時，所使用的 OpenSearch Query DSL 查詢。請參閱[備援行為](#fallback-behavior)。

在連接器或代理程式註冊中設定的所有參數，都可以在執行代理程式時覆寫。
{: .note}

## 回應篩選器組態

`response_filter` 參數使用 JSONPath 運算式，從 LLM 回應中擷取所產生的查詢。不同模型提供者傳回的回應格式不同，因此您需要為您的模型類型指定適當的篩選器。

**OpenAI 模型**：

```json
"response_filter": "$.choices[0].message.content"
```
{% include copy.html %}

**Anthropic Claude 模型（Amazon Bedrock Converse API）**：

```json
"response_filter": "$.output.message.content[0].text"
```
{% include copy.html %}

## 執行參數

`QueryPlanningTool` 接受下列執行參數。

參數 | 類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`question` | 字串 | 必要 | 完整的自然語言查詢，包含產生 OpenSearch DSL 所需的所有上下文。請包含問題、任何特定需求、篩選條件或限制。範例：`Find all products with price greater than 100 dollars`、`Show me documents about machine learning published in 2023`、`Search for users with status active and age between 25 and 35`。
`index_name` | 字串 | 必要 | 需要為其產生查詢的索引名稱。
`embedding_model_id` | 字串 | 選用 | 用於執行語意搜尋的模型 ID。

## 自訂提示

您可以提供自己的 `query_planner_system_prompt` 和 `query_planner_user_prompt`，自訂 LLM 產生 OpenSearch DSL 查詢的方式。

建立自訂提示時，請確保其中包含明確的輸出格式規則，讓提示能與代理式搜尋正常搭配運作。系統提示應指定 LLM 必須僅傳回有效的 JSON 物件，不得包含任何額外文字、程式碼圍欄或說明。
{: .important}

**自訂提示組態**：
在代理程式中註冊工具時，請依下列方式提供您的自訂提示：
```json
POST /_plugins/_ml/agents/_register
{
  "name": "Flow Agent for Agentic Search",
  "type": "flow",
  "description": "Flow agent for agentic search",
  "tools": [
    {
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "your_model_id",
        "response_filter": "<response-filter-based-on-model-type>",
        "query_planner_system_prompt": "<YOUR CUSTOM SYSTEM PROMPT>",
        "query_planner_user_prompt": "<YOUR CUSTOM USER PROMPT>"
      }
    }
  ]
}
```
{% include copy-curl.html %}

請根據您的模型類型使用適當的 `response_filter`。如需更多資訊與範例，請參閱[回應篩選器組態](#response-filter-configuration)。
{: .note}

以下是預設的系統提示：

<details open markdown="block">
<summary>
    提示
</summary>
{: .text-delta}

```json
==== PURPOSE ====
You are an OpenSearch DSL expert. Convert a natural-language question into a strict JSON OpenSearch query body.

==== RULES ====
Use only fields present in the provided mapping; never invent names.
Choose query types based on user intent and field types:

match: single-token full-text on analyzed text fields.

match_phrase: multi-token phrases on analyzed text fields (search string contains spaces, hyphens, commas, etc.).

multi_match: when multiple analyzed text fields are equally relevant.

term / terms: exact match on keyword, numeric, boolean.

range: numeric/date comparisons (gt, lt, gte, lte).

bool with must, should, must_not, filter: AND/OR/NOT logic.

wildcard / prefix on keyword: "starts with" / pattern matching.

exists: field presence/absence.

nested query / nested agg: ONLY if the mapping for that exact path (or a parent) has "type":"nested".

neural: semantic similarity on a 'semantic' or 'knn_vector' field (dense). Use "query_text" and "k"; include "model_id" unless bound in mapping.

neural (top-level): allowed when it's the only relevance clause needed; otherwise wrap in a bool when combining with filters/other queries.

Mechanics:

Put exact constraints (term, terms, range, exists, prefix, wildcard) in bool.filter (non-scoring). Put full-text relevance (match, match_phrase, multi_match) in bool.must.

Top N items/products/documents: return top hits (set "size": N as an integer) and sort by the relevant metric(s). Do not use aggregations for item lists.

Neural retrieval size: set "k" ≥ "size" (e.g. heuristic, k = max(size*5, 100) and k<=ef_search).

Spelling tolerance: match_phrase does NOT support fuzziness; use match or multi_match with "fuzziness": "AUTO" when tolerant matching is needed.

Text operators (OR vs AND): default to OR for natural-language queries; to tighten, use minimum_should_match (e.g., "75%"). Use AND only when every token is essential; if order/adjacency matters, use match_phrase.

Numeric note: use ONLY integers for size and k (not floats).

Aggregations (counts, averages, grouped summaries, distributions):

Use aggregations when the user asks for grouped summaries (e.g., counts by category, averages by brand, or top N categories/brands).

terms on field.keyword or numeric for grouping / top N groups (not items).

Metric aggs (avg, min, max, sum, stats, cardinality) on numeric fields.

date_histogram, histogram, range for distributions.

Always set "size": 0 when only aggregations are needed.

Use sub-aggregations + order for "top N groups by metric".

If grouping/filtering exactly on a text field, use its .keyword sub-field when present.

DATE RULES

Use range on date/date_nanos in bool.filter.

Emit ISO 8601 UTC ('Z') bounds; don't set time_zone for explicit UTC. (now is UTC)

Date math: now±N{y|M|w|d|h|m|s}.

Rounding: "/UNIT" floors to start (now/d, now/w, now/M, now/y).

End boundaries: prefer the next unit’s start.

Formats: only add "format" when inputs aren’t default; epoch_millis allowed.

Buckets: use date_histogram with calendar_interval or fixed_interval.

NEURAL / SEMANTIC SEARCH
When to use: conceptual/semantic intent, or when user asks for semantic/neural/vector/embedding search.
When not to use: purely structured/exact queries, or when no semantic/knn_vector field or model_id is available.
How to query:

Use the "neural" clause against the chosen field.

Required: "query_text" and "k".

Model rules:

For "semantic" fields, omit model_id unless overriding.

For "knn_vector", include model_id unless default is bound.

If no model id, do not generate neural clause.

Top-level allowed if no filters/other queries. Otherwise wrap in bool with filters in bool.filter.

Size: set "k" ≥ "size" (heuristic: k = max(size*5, 100)).

FIELD SELECTION & PROXYING
Goal: pick the smallest set of mapping fields that best capture the user's intent.

When provided, and present in the mapping, prioritize query_fields.

Proxy Rule: If at least one field is loosely related, proceed with the best proxy; do NOT fallback to match_all due to ambiguity.

Steps: harvest candidates, pick mapping fields, ignore irrelevant ones.

Micro Self-Check: verify fields exist; if not, swap to proxies. Only if no relevant fields exist at all, fallback to match_all.

==== OUTPUT FORMAT ====

Return EXACTLY ONE JSON object (valid OpenSearch request body).

No escapes, no code fences, no quotes around the whole object.

If nothing relevant exists, return exactly:
{"size":10,"query":{"match_all":{}}}

==== EXAMPLES ====
(Then follows Examples 1–13 exactly as in your original text, but without escapes.)

==== TEMPLATE USE ====
Use this search template provided by the user as reference to generate the query: ${parameters.template}
Note that this template might contain terms that are not relevant to the question at hand; in that case ignore the template.
```

</details>

以下是預設的使用者提示：

```json
Question: ${parameters.question}
Mapping: ${parameters.index_mapping:-}
Query Fields: ${parameters.query_fields:-}
Sample Document from index: ${parameters.sample_document:-}
In UTC: ${parameters.current_time:-} format: yyyy-MM-dd'T'HH:mm:ss'Z'
Embedding Model ID for Neural Search: ${parameters.embedding_model_id:- not provided}

==== OUTPUT ====
GIVE THE OUTPUT PART ONLY IN YOUR RESPONSE (a single JSON object)
Output:
```

## 備援行為

當 LLM 無法產生有效的 Query DSL 時，`QueryPlanningTool` 會使用備援查詢。根據預設，備援查詢為 `{"size":10,"query":{"match_all":{}}}`。您可以在註冊代理程式時指定自訂的 `fallback_query` 參數，以覆寫此預設值。

此工具會自動從 LLM 回應中擷取第一個有效的 JSON 物件，即使該 JSON 周圍有其他文字、Markdown 程式碼區塊標記、說明或其他內容也是如此。但是，如果無法從回應中擷取任何有效的 JSON（例如，回應完全空白、只包含非 JSON 文字，或只包含格式錯誤的 JSON），此工具會傳回備援查詢（預設查詢或您的自訂查詢）。

觸發備援時不會擲回錯誤，而是在系統記錄檔中顯示一筆偵錯記錄。這可確保即使 LLM 提供非預期的輸出，查詢規劃作業仍可繼續運作。

### 覆寫預設備援查詢

以下範例示範備援查詢的運作方式。

若要按照此範例操作，請先完成[代理式搜尋教學]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index/)中的步驟 1 至 3：建立索引、匯入資料並註冊模型。

接著，使用步驟 3 中的模型 ID 註冊代理程式。加入自訂的 `fallback_query` 參數以示範備援行為：

```json
POST _plugins/_ml/agents/_register
{
  "name": "Iris Search Agent with Fallback",
  "type": "flow",
  "tools": [
    {
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "<your-model-id>",
        "fallback_query": "{\"size\":10,\"query\":{\"bool\":{\"should\":[{\"match\":{\"species\":{\"query\":\"${parameters.question}\",\"fuzziness\":\"AUTO\"}}},{\"match_all\":{\"boost\":0.1}}],\"minimum_should_match\":1}}}"
      }
    }
  ]
}
```
{% include copy-curl.html %}

接著，使用上一個步驟中的代理程式 ID 建立搜尋管線：

```json
PUT _search/pipeline/agentic_search_pipeline
{
  "request_processors": [
    {
      "agentic_query_translator": {
        "agent_id": "<your-agent-id>"
      }
    }
  ],
  "response_processors": [
    {
      "agentic_context": {
        "dsl_query": true
      }
    }
  ]
}
```
{% include copy-curl.html %}

若要測試備援行為，請傳送搜尋請求，並提出與 `iris-index` 無關的問題：

```json
POST /iris-index/_search?search_pipeline=agentic_search_pipeline&pretty
{
  "query": {
    "agentic": {
      "query_text": "Find all employees hired in 2023 with salary above 100000"
    }
  }
}
```
{% include copy-curl.html %}

回應的 `ext` 區段中包含 `dsl_query` 欄位，其中含有備援查詢：

```json
{
  "took" : 5396,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 2,
      "relation" : "eq"
    },
    "max_score" : 0.1,
    "hits" : [
      {
        "_index" : "iris-index",
        "_id" : "1",
        "_score" : 0.1,
        "_source" : {
          "petal_length_in_cm" : 1.4,
          "petal_width_in_cm" : 0.2,
          "sepal_length_in_cm" : 5.1,
          "sepal_width_in_cm" : 3.5,
          "species" : "setosa"
        }
      },
      {
        "_index" : "iris-index",
        "_id" : "2",
        "_score" : 0.1,
        "_source" : {
          "petal_length_in_cm" : 4.5,
          "petal_width_in_cm" : 1.5,
          "sepal_length_in_cm" : 6.4,
          "sepal_width_in_cm" : 2.9,
          "species" : "versicolor"
        }
      }
    ]
  },
  "ext" : {
    "dsl_query" : "{\"size\":10,\"query\":{\"bool\":{\"should\":[{\"match\":{\"species\":{\"query\":\"Find all employees hired in 2023 with salary above 100000\",\"fuzziness\":\"AUTO\"}}},{\"match_all\":{\"boost\":0.1}}],\"minimum_should_match\":1}}}"
  }
}
```

接著，提出與 `iris-index` 相關的問題：

```json
POST /iris-index/_search?search_pipeline=agentic_search_pipeline
{
  "query": {
    "agentic": {
      "query_text": "Find all setosa species"
    }
  }
}
```
{% include copy-curl.html %}

回應中包含由 LLM 正確產生的查詢，而不是使用備援查詢：

```json
{
  "took" : 4037,
  "timed_out" : false,
  "_shards" : {
    "total" : 1,
    "successful" : 1,
    "skipped" : 0,
    "failed" : 0
  },
  "hits" : {
    "total" : {
      "value" : 1,
      "relation" : "eq"
    },
    "max_score" : 0.0,
    "hits" : [
      {
        "_index" : "iris-index",
        "_id" : "1",
        "_score" : 0.0,
        "_source" : {
          "petal_length_in_cm" : 1.4,
          "petal_width_in_cm" : 0.2,
          "sepal_length_in_cm" : 5.1,
          "sepal_width_in_cm" : 3.5,
          "species" : "setosa"
        }
      }
    ]
  },
  "ext" : {
    "dsl_query" : "{\"query\":{\"bool\":{\"filter\":[{\"term\":{\"species.keyword\":\"setosa\"}}]}}}"
  }
}
```

## 測試工具

您可以在代理程式工作流程中執行此工具，也可以使用 [Execute Tool API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/execute-tool/) 獨立執行。Execute Tool API 適合用來測試個別工具或執行獨立作業。

## 相關文件

- [代理式搜尋]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/index)