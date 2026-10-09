---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "設定代理程式"
parent: Agentic search
grand_parent: AI search
nav_order: 10
has_children: false
---

# 設定代理式搜尋代理程式

您可以透過自訂模型、工具和提示來設定代理式搜尋代理程式：

- [模型設定](#model-configuration)：選擇針對各種工作最佳化的不同大型語言模型 (LLM)。
- [工具協調](#tool-orchestration)：結合多個工具以實現自動化工作流程。
- [提示工程](#prompt-engineering-and-customization)：使用自訂提示微調代理程式行為。

## 模型設定

根據您的效能需求和用途選擇合適的語言模型。

您也可以為對話代理程式和 `QueryPlanningTool` 設定不同的模型。透過指定 `llm.model_id` 來設定代理程式的模型，並在 `QueryPlanningTool` 中指定 `parameters.model_id` 來設定查詢規劃器模型：

```json
{
  "name": "Agentic Search Agent",
  "type": "conversational",
  "description": "Agent using separate models for conversation and query planning",
  "llm": {
    "model_id": "your-conversational-model-id",
    "parameters": {
      "max_iteration": 15
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "<llm_interface>"  
  },
  "tools": [
    {
      "type": "QueryPlanningTool",
      "parameters": {
        "model_id": "your-query-planner-model-id"
      }
    }
  ],
  "app_type": "os_chat"
}
```
{% include copy.html %}

將 `<llm_interface>` 設定為您的供應商介面 (例如 `openai/v1/chat/completions`)，然後從下列選項中選擇特定模型。

### OpenAI GPT 模型

支援下列 OpenAI GPT 模型。

<!-- vale off -->

#### GPT-5 (建議使用)

<!-- vale on -->

GPT-5 提供進階推理能力，建議用於正式環境的用途。

**模型註冊**：

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

**推理模式**：

- `minimal`：回應時間最快，適合簡單的用途
- `low`(建議使用)：推理稍多，適合大多數查詢
- `medium`：增強推理能力，適合複雜的工作
- `high`：最大推理能力，適合最複雜的情境

當您選擇更高的推理模式時，整體延遲會增加。請選擇符合您準確度需求的最低模式。
{: .tip}

### Anthropic Claude 模型

Anthropic Claude 模型可透過 Amazon Bedrock 整合取得，並為複雜的搜尋情境提供分析能力。

<!-- vale off -->
#### Claude 4 Sonnet
<!-- vale on -->

**Amazon Bedrock 連接器設定**：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Bedrock Claude 4 Sonnet Connector",
    "description": "Amazon Bedrock connector for Claude 4 Sonnet",
    "version": 1,
    "protocol": "aws_sigv4",
    "parameters": {
        "region": "your-aws-region",
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
```
{% include copy-curl.html %}

### 代理程式介面設定

註冊代理程式時，請設定 `_llm_interface` 參數，以指定代理程式在使用函式呼叫時如何解析 LLM 輸出。選擇符合您模型類型的介面：

- `"bedrock/converse/claude"`：託管於 Amazon Bedrock 的 Anthropic Claude 模型
- `"openai/v1/chat/completions"`：OpenAI 聊天完成模型

每個介面都會定義針對該模型系列最佳化的預設回應結構描述和函式呼叫解析器。

## 工具協調

您必須為代理式搜尋設定 `QueryPlanningTool`。您可以設定其他工具來擴充代理程式的功能。

### QueryPlanningTool

代理式搜尋功能需要 [`QueryPlanningTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/query-planning-tool/)。它會將自然語言查詢轉譯為 OpenSearch Query DSL。

### 其他工具

除了必要的 `QueryPlanningTool` 之外，您還可以設定其他工具來擴充代理程式的功能。OpenSearch 為各種用途提供內建工具，包括搜尋作業、資料分析、異常偵測和網路整合。如需所有可用工具的完整清單，請參閱 [工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。

對話代理程式會根據查詢情境自動選擇並協調適當的工具。

#### 完整代理程式設定

下列範例顯示如何註冊具有多個工具的代理程式：

```json
POST /_plugins/_ml/agents/_register
{
    "name": "Advanced Agentic Search Agent",
    "type": "conversational",
    "description": "Multi-tool agentic search with index discovery and web integration",
    "llm": {
        "model_id": "your-conversational-model-id",
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
            "type": "ListIndexTool",
            "name": "ListIndexTool"
        },
        {
            "type": "IndexMappingTool",
            "name": "IndexMappingTool"
        },
        {
            "type": "WebSearchTool",
            "name": "DuckduckgoWebSearchTool",
            "parameters": {
                "engine": "duckduckgo"
            }
        },
        {
            "type": "QueryPlanningTool",
            "parameters": {
                "model_id": "your-query-planner-model-id"
            }
        }
    ],
    "app_type": "os_chat"
}
```
{% include copy-curl.html %}

### 智慧索引選取

當您加入 `ListIndexTool`、`IndexMappingTool` 或其他相關工具時，您的代理程式就能自動選擇正確的索引，並為該索引產生查詢。

若要在不指定索引的情況下進行搜尋，請傳送下列請求：

```json
GET /_search?search_pipeline=agentic-pipeline
{
    "query": {
        "agentic": {
            "query_text": "Find products with high ratings and low prices"
        }
    }
}
```
{% include copy-curl.html %}

代理程式會自動探索產品索引、分析其結構，並產生適當的查詢。

如果您未在搜尋查詢中指定索引，搜尋就會在叢集中的所有分片上執行，這可能耗費大量資源。為了提升效能，請盡可能指定目標索引。
{: .tip}

## 提示詞工程與自訂

使用自訂提示詞引導模型的推理過程，設定代理程式的行為與輸出格式。

若要自訂 `QueryPlanningTool` 提示詞，請參閱 [`QueryPlanningTool`]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/query-planning-tool/)。

### 系統提示詞最佳化

使用符合您特定使用案例的專屬系統提示詞，設定代理程式的行為。

### 代理程式輸出格式

代理程式必須使用下列輸出格式：

```json
{
    "dsl_query": "<OpenSearch DSL Object>",
    "agent_steps_summary": "<chronological steps taken by the agent>"
}
```
{% include copy.html %}

**自訂提示詞組態**：

自訂提示詞時，請確保您的系統提示詞與使用者提示詞都會引導模型一律以上述代理程式輸出格式傳回結果。適當的提示詞工程對於維持一致的輸出格式至關重要。

註冊代理程式時，請依下列方式提供您的自訂提示詞：

```json
POST /_plugins/_ml/agents/_register
{
    "name": "Custom Prompt Agent",
    "type": "conversational",
    "description": "Agent with custom system and user prompts",
    "llm": {
        "model_id": "your-model-id",
        "parameters": {
            "max_iteration": 15,
            "system_prompt": "<YOUR CUSTOM SYSTEM PROMPT>",
            "user_prompt": "<YOUR CUSTOM USER PROMPT>"
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
                "model_id": "your-query-planner-model-id"
            }
        }
    ],
    "app_type": "os_chat"
}
```
{% include copy-curl.html %}

### 提示詞最佳實務

請遵循下列準則，建立有效的提示詞，以產生一致且準確的結果：

- **具體明確**：清楚定義預期的代理程式輸出格式，其中包含 `dsl_query` 和 `agent_steps_summary` 欄位。
- **加入範例**：提供查詢範例，以及採用正確代理程式輸出格式的預期回應。
- **設定限制**：指定欄位名稱、資料類型與查詢限制。
- **針對 JSON 最佳化**：確保您的提示詞會引導模型產生有效的 JSON，並具備必要的代理程式輸出結構。

### 預設系統提示詞

預設會使用下列系統提示詞。您可以自訂此提示詞，以修改代理程式的行為：

<details open markdown="block">
  <summary>
    提示詞
  </summary>
  {: .text-delta}

```json
==== PURPOSE ====
Produce correct OpenSearch DSL by orchestrating tools. You MUST call the Query Planner Tool (query_planner_tool, "qpt") to author the DSL.
Your job: (a) gather only essential factual context, (b) compose a self-contained natural-language question for qpt, (c) validate coverage of qpt's DSL and iterate if needed, then (d) return a strict JSON result with the DSL and a brief step trace.

==== OUTPUT CONTRACT (STRICT) ====
Return ONLY a valid JSON object with exactly these keys:
{"dsl_query": <OpenSearch DSL Object>, "agent_steps_summary": "<chronological steps taken by the agent>"}
- No markdown, no extra text, no code fences. Double-quote all keys/strings.
- Escape quotes that appear inside values (including inside agent_steps_summary and inside the inlined qpt.question you report there).
- The output MUST parse as JSON.

==== OPERATING LOOP (QPT-CENTRIC) ====
1) PLAN (minimal): Identify the smallest set of facts truly required: entities, IDs/names, values, explicit time windows, disambiguations, definitions, normalized descriptors.
2) COLLECT (as needed): Use tools to fetch ONLY those facts. Do NOT mention schema fields, analyzers, or DSL constructs to the qpt.
3) SELECT index_name:
   - If provided by the caller, use it as-is.
   - Otherwise, discover and choose a single best index (e.g., list indices, inspect names/mappings) WITHOUT copying schema terms into qpt.question.
4) COMPOSE qpt.question: One concise, clear, self-contained natural-language question containing:
   - The user's request (no schema/DSL hints), and
   - The factual context you resolved (verbatim values, IDs, names, explicit date ranges, normalized descriptors).
   This question is the ONLY context (besides index_name) that qpt relies on.
5) CALL qpt with {question, index_name, embedding_model_id(if available)}.
6) VALIDATE qpt response and ensure it answers user's question else iterate by providing more context
7) FINALIZE when qpt produces a plausible, fully covered DSL.

==== CONTEXT RULES ====
- Use tools to resolve needed facts.
- When tools return user-specific values, RESTATE them verbatim in qpt.question in pure natural language.
- NEVER mention schema/field names, analyzers, or DSL constructs in qpt.question.
- Resolve ambiguous references BEFORE the final qpt call.

==== TRACE FORMAT (agent_steps_summary) ====
- First entry EXACTLY: "I have these tools available: [ToolA, ToolB, ...]"
- Then one entry per step:
  "First I used: <ToolName> — input: <short input>; context gained: <concise result>"
  "Second I used: …"
  …
  "N-th I used: query_planner_tool — qpt.question: <exact text with escaped quotes>; index_name_provided: <index-name>"
- Keep brief and factual. Do NOT restate the DSL. After the final qpt step you may add a short validation note.

==== FAILURE MODE ====
If required context is unavailable or qpt cannot produce a valid DSL
- Set "dsl_query" to {"query":{"match_all":{}}}
- Append a brief error note to agent_steps_summary, e.g., "error: missing relevant indices", "error: unresolved entity ID", "error: qpt failed to converge".

==== STYLE & SAFETY ====
- qpt.question must be purely natural-language and context-only.
- Be minimal and deterministic; avoid speculation.
- Use only the concise step summary.
- Always produce valid JSON per the contract.

==== END-TO-END EXAMPLE RUN (NON-EXECUTABLE, FOR SHAPE ONLY) ====
User question:
"Find shoes under 500 dollars. I am so excited for shoes yay!"

Process (brief):
- Index name not provided → use ListIndexTool to enumerate indices: "products", "machine-learning-training-data", …
- Choose "products" as most relevant for items/footwear.
- Confirm with IndexMappingTool that "products" index has expected data (do not copy schema terms into qpt.question).
- Compose qpt.question with natural-language constraints only.
- Call qpt and validate.

qpt.question (self-contained, no schema terms):
"Find shoes under 500 dollars."

qpt.output:
"{\"query\":{\"bool\":{\"must\":[{\"match\":{\"category\":\"shoes\"}}],\"filter\":[{\"range\":{\"price\":{\"lte\":500}}}]}}}"

Final response JSON:
{
  "dsl_query": {\"query\":{\"bool\":{\"must\":[{\"match\":{\"category\":\"shoes\"}}],\"filter\":[{\"range\":{\"price\":{\"lte\":500}}}]}}}},
  "agent_steps_summary": "I have these tools available: [ListIndexTool, IndexMappingTool, query_planner_tool]\nFirst I used: ListIndexTool — input: \"\"; context gained: \"Of the available indices, products index seems promising\"\nSecond I used: IndexMappingTool — input: \"products\"; context gained: \"index contains relevant fields\"\nThird I used: query_planner_tool — qpt.question: \"Find shoes under 500 dollars.\"; index_name_provided: \"products\"\nValidation: qpt output is valid JSON and reflects the user request."
}
```

</details>

### 預設使用者提示

預設使用者提示範本會將自然語言問題與可用的參數傳遞給代理程式：

```json
"NLQ is: ${parameters.question} and index_name is: ${parameters.index_name:-}, model ID for neural search is: ${parameters.embedding_model_id:-}"
```

## 後續步驟

- 如需在實務中使用自訂代理程式的完整範例，請參閱 [檢查代理式搜尋並繼續對話]({{site.url}}{{site.baseurl}}/vector-search/ai-search/agentic-search/agent-converse/)。 

- 如需可用工具的清單，請參閱 [工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。