---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Plan-execute-reflect 代理程式"
has_children: false
has_toc: false
nav_order: 40
parent: Agents
grand_parent: Agents and tools
---

# Plan-execute-reflect 代理程式
**3.0 版新增**
{: .label .label-purple }

Plan-execute-reflect 代理程式專為解決需要反覆推理與逐步執行的複雜任務而設計。這類代理程式使用一個大型語言模型 (LLM)——即 _planner_——來建立與更新計畫，並使用另一個 LLM（預設為同一個模型）透過內建的對話代理程式執行每個步驟。

Plan-execute-reflect 代理程式的運作分為三個階段：

- **規劃** – Planner LLM 使用可用的工具產生初始的逐步計畫。
- **執行** – 使用對話代理程式與可用的工具依序執行每個步驟。
- **重新評估** – 執行每個步驟後，Planner LLM 會使用中間結果重新評估計畫。LLM 可以根據新的情境動態調整計畫，以跳過、新增或變更步驟。

與對話代理程式類似，plan-execute-reflect 代理程式會將 LLM 與代理程式之間的互動儲存在記憶索引中。在以下範例中，代理程式使用 `conversation_index` 來保存執行歷程，包括使用者的問題、中間結果與最終輸出。

代理程式會根據工具描述與目前情境，自動為每個步驟選擇最合適的工具。

代理程式僅在每個步驟完成後支援重新評估。這讓代理程式能在進行下一個步驟之前，根據中間結果動態調整計畫。

## 建立 plan-execute-reflect 代理程式

以下範例請求會建立一個具有三個工具的 plan-execute-reflect 代理程式：

```json
POST /_plugins/_ml/agents/_register
{
  "name": "My Plan Execute Reflect Agent",
  "type": "plan_execute_and_reflect",
  "description": "Agent for dynamic task planning and reasoning",
  "llm": {
    "model_id": "YOUR_LLM_MODEL_ID",
    "parameters": {
      "prompt": "${parameters.question}"
    }
  },
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "YOUR_LLM_INTERFACE"
  },
  "tools": [
    { "type": "ListIndexTool" },
    { "type": "SearchIndexTool" },
    { "type": "IndexMappingTool" }
  ],
  "app_type": "os_chat"
}
```

請務必提供詳盡的工具描述，讓 LLM 能判斷在哪些情況下使用這些工具。
{: .tip}

如需 Register Agent API 請求欄位的詳細資訊，請參閱 [請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#request-body-fields)。

## 支援的 LLM

Plan-execute-reflect 代理程式為下列 LLM 提供內建的函式呼叫介面：

- [託管於 Amazon Bedrock 的 Anthropic Claude 3.7 模型](https://aws.amazon.com/bedrock/claude/)
- OpenAI GPT-4o 模型
- 託管於 Amazon Bedrock 的 DeepSeek-R1 模型

若要為某個 LLM 請求預設支援，請[在 ML Commons 儲存庫中建立功能請求 issue](https://github.com/opensearch-project/ml-commons/issues)。

如需使用 plan-execute-reflect 代理程式的逐步教學，請參閱 [建立 plan-execute-reflect 代理程式]({{site.url}}{{site.baseurl}}/tutorials/gen-ai/agents/build-plan-execute-reflect-agent/)。

若要使用特定模型設定 plan-execute-reflect 代理程式，您需要修改 [步驟 1(a)：建立連接器]({{site.url}}{{site.baseurl}}/tutorials/gen-ai/agents/build-plan-execute-reflect-agent/#step-1a-create-a-connector) 中的連接器，並在 [步驟 2：建立代理程式]({{site.url}}{{site.baseurl}}/tutorials/gen-ai/agents/build-plan-execute-reflect-agent/#step-2-create-an-agent) 中提供模型專屬的 `llm_interface` 參數： 

```json
"parameters": {
  "_llm_interface": "bedrock/converse/claude"
}
```

如需 `_llm_interface` 欄位的有效值，請參閱 [請求本文欄位]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/#request-body-fields)。

以下範例提供支援模型的連接器與代理程式建立請求。

### Amazon Bedrock 上的 Anthropic Claude

若要為託管於 Amazon Bedrock 的 Anthropic Claude 3.7 Sonnet 模型建立連接器，請使用以下請求：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "Amazon Bedrock Claude 3.7-sonnet connector",
    "description": "Connector to Amazon Bedrock service for the Claude model",
    "version": 1,
    "protocol": "aws_sigv4",
    "parameters": {
      "region": "your_aws_region",
      "service_name": "bedrock",
      "model": "us.anthropic.claude-3-7-sonnet-20250219-v1:0"
    },
    "credential": {
      "access_key": "your_aws_access_key",
      "secret_key": "your_aws_secret_key",
      "session_token": "your_aws_session_token"
    },
    "actions": [
      {
        "action_type": "predict",
        "method": "POST",
        "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
        "headers": {
          "content-type": "application/json"
        },
        "request_body": "{ \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": [${parameters._chat_history:-}{\"role\":\"user\",\"content\":[{\"text\":\"${parameters.prompt}\"}]}${parameters._interactions:-}]${parameters.tool_configs:-} }"
      }
    ]
}
```
{% include copy-curl.html %}

若要使用 Anthropic Claude 3.7 Sonnet 模型建立 plan-execute-reflect 代理程式，請使用以下請求：

```json
POST _plugins/_ml/agents/_register
{
  "name": "My Plan Execute and Reflect agent with Claude 3.7",
  "type": "plan_execute_and_reflect",
  "description": "this is a test agent",
  "llm": {
    "model_id": "your_llm_model_id",
    "parameters": {
      "prompt": "${parameters.question}"
  }},
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "bedrock/converse/claude"
  },
  "tools": [
    {
      "type": "ListIndexTool"
    },
    {
      "type": "SearchIndexTool"
    },
    {
      "type": "IndexMappingTool"
    }
  ]
}
```
{% include copy-curl.html %}

### OpenAI GPT-4o

若要為 OpenAI GPT-4o 模型建立連接器，請使用以下請求：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "My openai connector: gpt-4o-mini",
    "description": "The connector to openai chat model",
    "version": 1,
    "protocol": "http",
    "parameters": {
        "model": "gpt-4o"
    },
    "credential": {
        "openAI_key": "your_open_ai_key"
    },
    "actions": [
        {
        "action_type": "predict",
        "method": "POST",
        "url": "https://api.openai.com/v1/chat/completions",
        "headers": {
            "Authorization": "Bearer ${credential.openAI_key}"
        },
        "request_body": "{ \"model\": \"${parameters.model}\", \"messages\": [{\"role\":\"developer\",\"content\":\"${parameters.system_prompt}\"},${parameters._chat_history:-}{\"role\":\"user\",\"content\":\"${parameters.prompt}\"}${parameters._interactions:-}]${parameters.tool_configs:-} }"
        }
    ]
}
```
{% include copy-curl.html %}

接著註冊模型並註冊代理程式，在 `_llm_interface` 欄位中指定 `openai/v1/chat/completions`。

### Amazon Bedrock 上的 Deepseek-R1

若要為託管於 Amazon Bedrock 的 DeepSeek-R1 模型建立連接器，請使用以下請求：

```json
POST /_plugins/_ml/connectors/_create
{
    "name": "My DeepSeek R1 connector",
    "description": "my test connector",
    "version": 1,
    "protocol": "aws_sigv4",
    "parameters": {
        "region": "your_region",
        "service_name": "bedrock",
        "model": "us.deepseek.r1-v1:0"
    },
    "credential": {
        "access_key": "your_access_key",
        "secret_key": "your_secret_key",
        "session_token": "your_session_token"
    },
    "actions": [
        {
        "action_type": "predict",
        "method": "POST",
        "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/converse",
        "headers": {
            "content-type": "application/json"
        },
        "request_body": "{ \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": [${parameters._chat_history:-}{\"role\":\"user\",\"content\":[{\"text\":\"${parameters.prompt}\"}]}${parameters._interactions:-}] }"
        }
    ]
}
```
{% include copy-curl.html %}

接著註冊模型並註冊代理程式，在 `_llm_interface` 欄位中指定 `bedrock/converse/deepseek_r1`。
 
由於託管於 Amazon Bedrock 的 Deepseek-R1 模型缺乏預設的函式呼叫支援，請在註冊代理程式時提供以下提示作為 `executor_system_prompt`：

```json
"You are a helpful assistant. You can ask Human to use tools to look up information that may be helpful in answering the users original question. The tools the human can use are:\n[${parameters._tools.toString()}]\n\nIf need to use tool, return which tool should be used and the input to user is enough. User will run the tool to get information. To make it easier for user to parse the response to know whether they should invoke a tool or not, please also return \"stop_reason\", it only return one of two enum values: [end_turn, tool_use], add a random tool call id to differenciate in case same tool invoked multiple times. Tool call id follow this pattern \"tool_use_<random string>\". The random string should be some UUID.\n\nFor example, you should return a json like this if need to use tool:\n{\"stop_reason\": \"tool_use\", \"tool_calls\": [{\"id\":\"tool_use_IIHBxMgOTjGb6ascCiOILg\",tool_name\":\"search_opensearch_index\",\"input\": {\"index\":\"population_data\",\"query\":{\"query\":{\"match\":{\"city\":\"New York City\"}}}}}]}\n\nIf don't need to use tool, return a json like this:\n{\"stop_reason\": \"end_turn\", \"message\": {\"role\":\"user\",\"content\":[{\"text\":\"What is the most popular song on WZPZ?\"}]}}\n\nNOTE: Don't wrap response in markdown ```json<response>```. For example don't return ```json\\n{\"stop_reason\": \"end_turn\", \"message\": {\"role\":\"user\",\"content\":[{\"text\":\"What is the most popular song on WZPZ?\"}]}}```\n"
```
{% include copy.html %}

## 追蹤代理程式執行與記憶體

當您使用 [Agent Execute API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/) 以非同步方式執行 plan-execute-reflect 代理程式時，代理程式啟動後，API 會傳回規劃器代理程式的 `memory_id` 與 `parent_interaction_id`。

在最終回應中，API 也會傳回 `executor_agent_memory_id` 與 `executor_agent_parent_interaction_id`，其對應於負責執行計畫中每個步驟的內部執行器代理程式。`executor_agent_memory_id` 與 `executor_agent_parent_interaction_id` 會在可用時立即於任務中更新，甚至在代理程式完成執行之前就會更新。這可讓您即時追蹤執行程序。

如需完整範例，請參閱[建立 plan-execute-reflect 代理程式]({{site.url}}{{site.baseurl}}/tutorials/gen-ai/agents/build-plan-execute-reflect-agent/#test-the-agent)。

## 預設提示

plan-execute-reflect 代理程式使用下列預先定義的提示。您可以透過下列方式提供新的提示來自訂提示：

- 在註冊代理程式期間，於 `parameters` 物件中
- 在代理程式執行期間動態提供

### 規劃器範本與提示

若要建立自訂的規劃器提示範本，請修改 `planner_prompt_template` 參數。下列範本用於要求 LLM 為指定任務設計計畫：

```json
${parameters.tools_prompt} \n${parameters.planner_prompt} \nObjective: ${parameters.user_prompt} \n\nRemember: Respond only in JSON format following the required schema.
```

若要建立自訂的規劃器提示，請修改 `planner_prompt` 參數。
下列提示用於要求 LLM 為指定任務設計計畫：

```
For the given objective, generate a step-by-step plan composed of simple, self-contained steps. The final step should directly yield the final answer. Avoid unnecessary steps.
```

### 含歷史記錄範本的規劃器提示

若要建立含歷史記錄範本的自訂規劃器提示，請修改 `planner_with_history_template` 參數。當代理程式執行期間提供 `memory_id` 時，會使用下列範本，為 LLM 提供先前任務的相關內容：

```json
${parameters.tools_prompt} \n${parameters.planner_prompt} \nObjective: ```${parameters.user_prompt}``` \n\nYou have currently executed the following steps: \n[${parameters.completed_steps}] \n\nRemember: Respond only in JSON format following the required schema.
```

### 反思提示與範本

若要建立自訂的反思提示範本，請修改 `reflect_prompt_template` 參數。下列範本用於要求 LLM 根據已完成的步驟重新思考原始計畫：

```json
${parameters.tools_prompt} \n${parameters.planner_prompt} \n\nObjective: ```${parameters.user_prompt}```\n\nOriginal plan:\n[${parameters.steps}] \n\nYou have currently executed the following steps from the original plan: \n[${parameters.completed_steps}] \n\n${parameters.reflect_prompt} \n\n.Remember: Respond only in JSON format following the required schema.
```

若要建立自訂的反思提示，請修改 `reflect_prompt` 參數。
下列提示用於要求 LLM 重新思考原始計畫：

```
Update your plan based on the latest step results. If the task is complete, return the final answer. Otherwise, include only the remaining steps. Do not repeat previously completed steps.
```

### 規劃器系統提示

若要建立自訂的規劃器系統提示，請修改 `system_prompt` 參數。以下是規劃器系統提示：

```
You are a thoughtful and analytical planner agent in a plan-execute-reflect framework. Your job is to design a clear, step-by-step plan for a given objective.

Instructions:
- Break the objective into an ordered list of atomic, self-contained Steps that, if executed, will lead to the final result or complete the objective.
- Each Step must state what to do, where, and which tool/parameters would be used. You do not execute tools, only reference them for planning.
- Use only the provided tools; do not invent or assume tools. If no suitable tool applies, use reasoning or observations instead.
- Base your plan only on the data and information explicitly provided; do not rely on unstated knowledge or external facts.
- If there is insufficient information to create a complete plan, summarize what is known so far and clearly state what additional information is required to proceed.
- Stop and summarize if the task is complete or further progress is unlikely.
- Avoid vague instructions; be specific about data sources, indexes, or parameters.
- Never make assumptions or rely on implicit knowledge.
- Respond only in JSON format.

Step examples:
Good example: "Use Tool to sample documents from index: 'my-index'"
Bad example: "Use Tool to sample documents from each index"
Bad example: "Use Tool to sample documents from all indices"
Response Instructions: 
Only respond in JSON format. Always follow the given response instructions. Do not return any content that does not follow the response instructions. Do not add anything before or after the expected JSON. 
Always respond with a valid JSON object that strictly follows the below schema:
{
	"steps": array[string], 
	"result": string 
}
Use "steps" to return an array of strings where each string is a step to complete the objective, leave it empty if you know the final result. Please wrap each step in quotes and escape any special characters within the string. 
Use "result" return the final response when you have enough information, leave it empty if you want to execute more steps. Please escape any special characters within the result. 
Here are examples of valid responses following the required JSON schema:

Example 1 - When you need to execute steps:
{
	"steps": ["This is an example step", "this is another example step"],
	"result": ""
}

Example 2 - When you have the final result:
{
	"steps": [],
	"result": "This is an example result\n with escaped special characters"
}
Important rules for the response:
1. Do not use commas within individual steps 
2. Do not add any content before or after the JSON 
3. Only respond with a pure JSON object 

When you deliver your final result, include a comprehensive report. This report must:
1. List every analysis or step you performed.
2. Summarize the inputs, methods, tools, and data used at each step.
3. Include key findings from all intermediate steps — do NOT omit them.
4. Clearly explain how the steps led to your final conclusion. Only mention the completed steps.
5. Return the full analysis and conclusion in the 'result' field, even if some of this was mentioned earlier. Ensure that special characters are escaped in the 'result' field.
6. The final response should be fully self-contained and detailed, allowing a user to understand the full investigation without needing to reference prior messages and steps.
```

我們不建議修改回應格式指示。如果您打算修改任何提示，可以使用 `${parameters.plan_execute_reflect_response_format}` 參數來插入回應格式指示。
{: .tip}

### 執行者系統提示詞

若要建立自訂的執行者系統提示詞，請修改 `executor_system_prompt` 參數。以下是執行者系統提示詞：

```
You are a precise and reliable executor agent in a plan-execute-reflect framework. Your job is to execute the given instruction provided by the planner and return a complete, actionable result.

Instructions:
- Fully execute the given Step using the most relevant tools or reasoning.
- Include all relevant raw tool outputs (e.g., full documents from searches) so the planner has complete information; do not summarize unless explicitly instructed.
- Base your execution and conclusions only on the data and tool outputs available; do not rely on unstated knowledge or external facts.
- If the available data is insufficient to complete the Step, summarize what was obtained so far and clearly state the additional information or access required to proceed (do not guess).
- If unable to complete the Step, clearly explain what went wrong and what is needed to proceed.
- Avoid making assumptions and relying on implicit knowledge.
- Your response must be self-contained and ready for the planner to use without modification. Never end with a question.
- Break complex searches into simpler queries when appropriate.
```

## 修改預設提示詞

若要修改提示詞，請在註冊代理程式時提供提示詞：

```json
POST _plugins/_ml/agents/_register
{
  "name": "My Plan Execute and Reflect agent with Claude 3.7",
  "type": "plan_execute_and_reflect",
  "description": "this is a test agent",
  "llm": {
    "model_id": "your_llm_model_id_from_step1",
    "parameters": {
      "prompt": "${parameters.question}"
  }},
  "memory": {
    "type": "conversation_index"
  },
  "parameters": {
    "_llm_interface": "bedrock/converse/claude",
    "planner_prompt_template": "your_planner_prompt_template",
    "planner_prompt": "your_planner_prompt",
    "reflect_prompt_template": "your_reflect_prompt_template",
    "reflect_prompt": "your_reflect_prompt",
    "planner_with_history_template": "your_planner_with_history_template",
    "system_prompt": "your_planner_system_prompt",
    "executor_system_prompt": "your_executor_system_prompt"
  },
  "tools": [
    {
      "type": "ListIndexTool"
    },
    {
      "type": "SearchIndexTool"
    },
    {
      "type": "IndexMappingTool"
    }
  ],
}
```
{% include copy-curl.html %}

您也可以在代理程式執行時修改提示詞：

```json
POST _plugins/_ml/agents/your_agent_id/_execute?async=true
{
  "parameters": {
    "question": "How many flights from Beijing to Seattle?",
    "planner_prompt_template": "your_planner_prompt_template",
    "planner_prompt": "your_planner_prompt"
  }
}
```
{% include copy-curl.html %}

## 追蹤詞元使用量
**3.6 版新增**
{: .label .label-purple }

Plan-execute-reflect 代理程式支援詞元使用量追蹤，可提供代理程式執行期間每次 LLM 呼叫的詞元消耗詳細指標，包括規劃、執行（使用子代理程式）與反思的 LLM 呼叫。子代理程式的詞元資料會自動合併至父代理程式的詞元使用量報告中。

若要啟用詞元使用量追蹤，請在執行代理程式時將 `include_token_usage` 參數設為 `true`。回應將包含 `token_usage` 輸出，其中提供每輪與每個模型的彙總指標。有關詞元使用量欄位的詳細資訊，以及不同模型供應商如何計算詞元，請參閱 Execute Agent API 文件中的 [追蹤詞元使用量]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/execute-agent/#tracking-token-usage)。

## 後續步驟

- 若要進一步了解如何註冊代理程式，請參閱 [Register Agent API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/register-agent/)。
- 如需支援的工具清單，請參閱 [工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。
- 如需使用 plan-execute-reflect 代理程式的逐步教學，請參閱 [建立 plan-execute-reflect 代理程式]({{site.url}}{{site.baseurl}}/tutorials/gen-ai/agents/build-plan-execute-reflect-agent/)。
- 如需支援的 API，請參閱 [代理程式 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agent-apis/)。
- 若要在組態自動化中使用代理程式與工具，請參閱 [組態自動化]({{site.url}}{{site.baseurl}}/automating-configurations/index/)。