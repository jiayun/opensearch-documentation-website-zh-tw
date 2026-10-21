---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "搭配 Strands Agents 使用代理記憶"
parent: Agentic AI
grand_parent: Generative AI
nav_order: 30
---

# 搭配 Strands Agents 使用代理記憶

除非您為 AI 代理程式提供記憶儲存區，否則它只會在單一對話中保留資訊。本教學說明如何使用 OpenSearch [代理記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)，作為以 [Strands Agents](https://strandsagents.com/)（一個開放原始碼的 Python 代理程式框架）建置之代理程式的長期記憶。您將建立一個記憶容器，使用 LLM 從對話中擷取事實與偏好，接著撰寫供代理程式呼叫的 Python 工具，用來新增、搜尋、更新及刪除記憶。由於記憶儲存在 OpenSearch 中，代理程式可以在之後的對話中回想這些記憶。

本教學使用下列託管於 Amazon Bedrock 的模型：

- [Amazon Titan Text Embeddings V2](https://docs.aws.amazon.com/bedrock/latest/userguide/titan-embedding-models.html)（`amazon.titan-embed-text-v2:0`），用於產生記憶嵌入。
- [Anthropic Claude Sonnet 4.6](https://aws.amazon.com/bedrock/claude/)（`us.anthropic.claude-sonnet-4-6`），同時用於 Strands 代理程式與記憶容器的事實擷取。

請將開頭為 `your_` 前綴的預留位置替換為您自己的值。
{: .note}

## 先決條件

開始之前，請確認您已具備下列項目：

- 一個 OpenSearch 3.7 或更新版本的叢集，且您的 Python 環境可以連線至該叢集。
- 可在 Amazon Bedrock 上叫用 Amazon Titan Text Embeddings V2 與 Anthropic Claude Sonnet 4.6 模型的 AWS 認證資訊。OpenSearch 會在連接器中使用這些認證資訊。Strands 代理程式會直接從 Python 呼叫 Amazon Bedrock，因此您的 Python 環境也必須設定 AWS 認證資訊，例如透過環境變數或 AWS 命令列介面（AWS CLI）設定。
- Python 3.10 或更新版本。

## 步驟 1：註冊嵌入模型

記憶容器使用嵌入模型為擷取出的記憶產生向量嵌入，讓您可以對這些記憶進行語意搜尋。

首先，為 Amazon Titan Text Embeddings V2 模型建立連接器：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock connector: Titan Text Embeddings V2",
  "description": "Connector to the Amazon Bedrock Titan Text Embeddings V2 model",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "your_aws_region",
    "service_name": "bedrock",
    "model": "amazon.titan-embed-text-v2:0",
    "dimensions": 1024,
    "normalize": true,
    "embeddingTypes": ["float"]
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
      "url": "https://bedrock-runtime.${parameters.region}.amazonaws.com/model/${parameters.model}/invoke",
      "headers": {
        "content-type": "application/json",
        "x-amz-content-sha256": "required"
      },
      "request_body": "{ \"inputText\": \"${parameters.inputText}\", \"dimensions\": ${parameters.dimensions}, \"normalize\": ${parameters.normalize}, \"embeddingTypes\": ${parameters.embeddingTypes} }",
      "pre_process_function": "connector.pre_process.bedrock.embedding",
      "post_process_function": "connector.post_process.bedrock.embedding"
    }
  ]
}
```
{% include copy-curl.html %}

請記下連接器 ID；您將使用它來註冊模型。

接著，註冊模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Amazon Bedrock Titan Text Embeddings V2",
  "function_name": "remote",
  "description": "Embedding model for agentic memory",
  "connector_id": "your_embedding_connector_id"
}
```
{% include copy-curl.html %}

請記下模型 ID；您將使用它來建立記憶容器。

## 步驟 2：註冊用於事實擷取的 LLM

記憶容器使用 LLM 從對話中擷取事實與使用者偏好，並判斷每項新事實要儲存為新記憶，還是要更新或刪除現有的記憶。

首先，使用 Amazon Bedrock Converse API 為 Anthropic Claude Sonnet 4.6 模型建立連接器。代理記憶會將 `system_prompt` 與 `user_prompt` 參數傳遞給連接器，因此請求本文必須同時包含這兩者：

```json
POST /_plugins/_ml/connectors/_create
{
  "name": "Amazon Bedrock connector: Claude Sonnet 4.6",
  "description": "Connector to the Amazon Bedrock Claude Sonnet 4.6 model using the Converse API",
  "version": 1,
  "protocol": "aws_sigv4",
  "parameters": {
    "region": "your_aws_region",
    "service_name": "bedrock",
    "model": "us.anthropic.claude-sonnet-4-6"
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
      "request_body": "{ \"system\": [{\"text\": \"${parameters.system_prompt}\"}], \"messages\": [{\"role\": \"user\", \"content\": [{\"text\": \"${parameters.user_prompt}\"}]}] }",
      "supports_structured_output": true
    }
  ]
}
```
{% include copy-curl.html %}

`supports_structured_output` 欄位會為事實擷取啟用受限解碼。當其值為 `true` 時，OpenSearch 會在事實擷取期間，於 Converse API 請求中加入 `toolConfig` 物件。`toolConfig` 物件會要求模型呼叫 `extract_facts` 工具，因此模型會以固定的 JSON 結構描述傳回事實。接著 OpenSearch 會從回應中的工具呼叫讀取事實，因此您不需要設定 `llm_result_path`。若省略此欄位，OpenSearch 會在事實擷取提示中加入格式指示，並讀取模型的文字回應。如需詳細資訊，請參閱[連接器藍圖]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/blueprints/#request-body-fields)。

請記下連接器 ID；您將使用它來註冊模型。

接著，註冊模型：

```json
POST /_plugins/_ml/models/_register?deploy=true
{
  "name": "Amazon Bedrock Claude Sonnet 4.6",
  "function_name": "remote",
  "description": "LLM for agentic memory fact extraction",
  "connector_id": "your_llm_connector_id"
}
```
{% include copy-curl.html %}

請記下模型 ID；您將使用它來建立記憶容器。

## 步驟 3：建立記憶容器

建立使用這兩個模型的記憶容器。此範例中的容器使用下列策略，兩者的範圍皆限定在 `user_id` 命名空間，讓每位使用者的記憶分開儲存：

- `SEMANTIC` 會擷取事實，例如使用者的姓名或工作。
- `USER_PREFERENCE` 會擷取使用者的偏好（例如嗜好或喜愛的食物），以及身分陳述（例如使用者的工作）。

每個策略會各自獨立擷取記憶，因此同時符合兩個策略的事實會儲存兩次，每個策略各一次。

由於已設定策略，OpenSearch 會為此容器建立工作階段、工作記憶、長期記憶與歷程記錄索引：

```json
POST /_plugins/_ml/memory_containers/_create
{
  "name": "strands-personal-assistant",
  "description": "Long-term memory for a Strands Agents personal assistant",
  "configuration": {
    "embedding_model_type": "TEXT_EMBEDDING",
    "embedding_model_id": "your_embedding_model_id",
    "embedding_dimension": 1024,
    "llm_id": "your_llm_model_id",
    "strategies": [
      {
        "type": "SEMANTIC",
        "namespace": ["user_id"]
      },
      {
        "type": "USER_PREFERENCE",
        "namespace": ["user_id"]
      }
    ]
  }
}
```
{% include copy-curl.html %}

回應中包含記憶容器 ID：

```json
{
  "memory_container_id": "xthvpZgBOh0h20Y9O3Sa",
  "status": "created"
}
```

請記下記憶容器 ID；您將在代理程式程式碼中使用它。如需容器組態的詳細資訊，請參閱 [Create Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)。

## 步驟 4：建立代理程式與記憶工具

代理記憶透過 REST API 存取，因此您可以在任何代理程式框架中使用它。在此步驟中，您會將每個記憶操作定義為 Strands Agents 工具。Strands Agents 會使用每個工具的 docstring 與型別提示向 LLM 描述該工具，讓代理程式能決定何時呼叫它。

安裝必要的 Python 套件：

```bash
pip install strands-agents requests
```
{% include copy.html %}

將下列程式碼儲存為 `memory_agent.py`。此程式碼定義了下列工具：

- `add_memory` 將一輪對話傳送至 [Add Agentic Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/add-memory/)，並將 `infer` 設定為 `true`，讓 LLM 從中擷取事實並存入長期記憶。
- `search_memories` 使用 [Semantic Search Agentic Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/semantic-search-memory/) 尋找相關的長期記憶。該 API 會擷取容器中與查詢最接近的 `k` 筆記憶，然後依命名空間篩選，因此當一個容器儲存多位使用者的記憶時，可能為某位使用者回傳少於 `k` 筆記憶。
- `list_memories` 使用 [Search Agentic Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory/) 回傳該使用者的所有長期記憶。
- `update_memory` 與 `delete_memory` 使用 [Update Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/update-memory/) 與 [Delete Agentic Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/delete-memory/)，依 ID 修改或移除長期記憶。當您更新記憶的文字時，OpenSearch 會重新產生其嵌入，因此語意搜尋能依新文字找到該記憶。

每次指令碼啟動時，都會使用 [Create Session API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-session/) 建立新的工作階段。工作階段 ID 會與每一輪對話一併儲存在工作記憶中。長期記憶僅限於 `user_id` 命名空間，因此在每個工作階段中都可使用：

```python
from typing import Any, Dict, List, Optional

import requests
from requests.auth import HTTPBasicAuth
from strands import Agent, tool
from strands.models import BedrockModel

OPENSEARCH_URL = "your_opensearch_endpoint"  # For example, https://localhost:9200
OPENSEARCH_USERNAME = "your_username"
OPENSEARCH_PASSWORD = "your_password"
# Set to False only for a local test cluster that uses self-signed certificates.
VERIFY_CERTS = True

MEMORY_CONTAINER_ID = "your_memory_container_id"
USER_ID = "your_user_id"
AWS_REGION = "your_aws_region"

MEMORIES_PATH = f"/_plugins/_ml/memory_containers/{MEMORY_CONTAINER_ID}/memories"
session_id: Optional[str] = None


def opensearch_request(method: str, path: str, body: Optional[Dict] = None) -> Dict[str, Any]:
    """Send a request to OpenSearch and return the JSON response."""
    response = requests.request(
        method,
        f"{OPENSEARCH_URL}{path}",
        json=body,
        auth=HTTPBasicAuth(OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD),
        verify=VERIFY_CERTS,
        timeout=30,
    )
    if not response.ok:
        print(f"OpenSearch returned {response.status_code}: {response.text}")
    response.raise_for_status()
    return response.json()


def create_session() -> str:
    """Create a session for this conversation and return its ID."""
    body = {
        "summary": "Strands Agents personal assistant conversation",
        "namespace": {"user_id": USER_ID},
    }
    return opensearch_request("POST", f"{MEMORIES_PATH}/sessions", body)["session_id"]


def to_memory_list(search_response: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Convert a search response into a compact list for the agent."""
    return [
        {
            "memory_id": hit["_id"],
            "memory": hit["_source"]["memory"],
            "strategy_type": hit["_source"]["strategy_type"],
        }
        for hit in search_response["hits"]["hits"]
    ]


@tool
def add_memory(user_message: str, assistant_message: Optional[str] = None) -> Dict[str, Any]:
    """Store a conversation turn so that facts and preferences in it are remembered.

    Call this tool when the user shares information about themselves that is worth
    remembering in future conversations, such as their name, job, or preferences.

    Args:
        user_message: The user's message that contains the information to remember.
        assistant_message: Your reply to the user's message, if any.
    """
    messages = [{"role": "user", "content": [{"text": user_message, "type": "text"}]}]
    if assistant_message:
        messages.append({"role": "assistant", "content": [{"text": assistant_message, "type": "text"}]})
    body = {
        "messages": messages,
        "namespace": {"user_id": USER_ID, "session_id": session_id},
        "payload_type": "conversational",
        "infer": True,
    }
    return opensearch_request("POST", MEMORIES_PATH, body)


@tool
def search_memories(query: str, k: int = 5) -> List[Dict[str, Any]]:
    """Find the user's long-term memories that are most relevant to a query.

    Args:
        query: A natural language description of the information you need.
        k: The maximum number of memories to return.
    """
    body = {"query": query, "k": k, "namespace": {"user_id": USER_ID}}
    response = opensearch_request("POST", f"{MEMORIES_PATH}/long-term/_semantic_search", body)
    return to_memory_list(response)


@tool
def list_memories(size: int = 50) -> List[Dict[str, Any]]:
    """List all of the user's long-term memories, newest first.

    Args:
        size: The maximum number of memories to return.
    """
    body = {
        "query": {"term": {"namespace.user_id": USER_ID}},
        "size": size,
        "_source": {"excludes": ["memory_embedding"]},
        "sort": [{"created_time": {"order": "desc"}}],
    }
    response = opensearch_request("GET", f"{MEMORIES_PATH}/long-term/_search", body)
    return to_memory_list(response)


@tool
def update_memory(memory_id: str, memory: str) -> Dict[str, Any]:
    """Replace the text of a long-term memory, for example, when the user corrects a fact.

    Args:
        memory_id: The ID of the memory to update, as returned by search_memories or list_memories.
        memory: The corrected memory text.
    """
    return opensearch_request("PUT", f"{MEMORIES_PATH}/long-term/{memory_id}", {"memory": memory})


@tool
def delete_memory(memory_id: str) -> Dict[str, Any]:
    """Delete a long-term memory, for example, when the user asks you to forget something.

    Args:
        memory_id: The ID of the memory to delete, as returned by search_memories or list_memories.
    """
    return opensearch_request("DELETE", f"{MEMORIES_PATH}/long-term/{memory_id}")


SYSTEM_PROMPT = """You are a personal assistant with long-term memory.
- When the user shares facts or preferences about themselves, call add_memory.
- Before answering a question that depends on what you know about the user, call search_memories.
  When the user asks what you know about them, call list_memories.
- When the user corrects a fact, find the memory and call update_memory.
- When the user asks you to forget something, find the memory and call delete_memory.
Facts are extracted in the background, so memories that you just added might not appear in results yet."""


def main():
    global session_id
    session_id = create_session()

    model = BedrockModel(model_id="us.anthropic.claude-sonnet-4-6", region_name=AWS_REGION)
    agent = Agent(
        model=model,
        tools=[add_memory, search_memories, list_memories, update_memory, delete_memory],
        system_prompt=SYSTEM_PROMPT,
    )

    print(f"Memory agent started. Container: {MEMORY_CONTAINER_ID}, session: {session_id}")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("\n> ")
        if user_input.strip().lower() == "exit":
            break
        try:
            agent(user_input)
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
```
{% include copy.html %}

## 步驟 5：與代理程式對話

執行指令碼：

```bash
python memory_agent.py
```
{% include copy.html %}

在第一個工作階段中，向代理程式介紹您自己。代理程式會針對每則訊息呼叫 `add_memory`，而記憶容器會在背景從訊息中擷取事實。代理程式的回覆每次執行可能不同；以下為範例對話：

```
Memory agent started. Container: xthvpZgBOh0h20Y9O3Sa, session: S-dqiJkB1SltqOcZ1cYO
Type 'exit' to quit.

> Hi, I'm Alex. I'm a software engineer and I live in Seattle.

Tool #1: add_memory
Nice to meet you, Alex! I've made a note that you're a software engineer living in Seattle. Feel free to ask me anything. I'm here to help!
> I like hiking and Thai food.

Tool #2: add_memory
Great interests! I've saved that you enjoy hiking and Thai food. Seattle is a fantastic place for both: you've got amazing trails like those in the Cascades right at your doorstep, and Seattle has a wonderful Thai food scene!
> exit
```

再次執行指令碼以開始第二個工作階段。代理程式沒有第一個工作階段的對話記錄，但可以取回從該工作階段擷取出的記憶。在此範例中，代理程式會針對每項變更更新並刪除兩筆記憶，因為兩種策略都儲存了地點與泰式料理的事實：

```
Memory agent started. Container: xthvpZgBOh0h20Y9O3Sa, session: jTYm35kBt8CyICnjxJl9
Type 'exit' to quit.

> What do you know about me?

Tool #1: list_memories
Here's what I know about you:

- **Name:** Alex
- **Occupation:** Software Engineer
- **Location:** Seattle
- **Interests/Hobbies:** Hiking
- **Food Preferences:** Thai food

Is there anything you'd like to add, correct, or have me forget?
> Actually, I moved to Portland last month.
Got it, let me update that for you!
Tool #2: update_memory

Tool #3: update_memory
Done! I've updated your location from Seattle to Portland. Welcome to your new city! Is there anything else you'd like to update?
> Can you suggest a plan for this weekend?

Tool #4: search_memories

Tool #5: search_memories
Here's a fun weekend plan tailored for you in Portland, Alex!

**Saturday:**
- **Morning Hike:** Head out to **Forest Park**, one of the largest urban forests in the US, right in Portland. The Wildwood Trail offers beautiful scenery for all levels.
- **Lunch/Dinner:** Check out some of Portland's great Thai restaurants!

**Sunday:**
- **Morning Hike:** If you're up for a bit more of a drive, **Multnomah Falls** and the surrounding trails in the Columbia River Gorge are stunning and definitely worth a visit.
...
> Please forget that I like Thai food.
Sure!
Tool #6: delete_memory

Tool #7: delete_memory
Done! I've forgotten that you like Thai food. Is there anything else you'd like to update or remove?
> exit
```

## 步驟 6：檢查已儲存的記憶

若要檢視記憶容器所擷取的長期記憶，請傳送下列請求：

```json
GET /_plugins/_ml/memory_containers/your_memory_container_id/memories/long-term/_search
{
  "query": {
    "term": {
      "namespace.user_id": "your_user_id"
    }
  },
  "_source": {
    "excludes": ["memory_embedding"]
  },
  "sort": [
    {
      "created_time": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

回應中會為每筆擷取的記憶包含一份文件。`strategy_type` 欄位會顯示擷取該記憶的策略。兩種策略都儲存了工作、地點與健行的事實，因此每項事實會出現兩次。代理程式在第二個工作階段中更新的兩筆地點記憶包含新的地點，而代理程式刪除的泰式料理記憶則不再儲存：

<details markdown="block">
  <summary>
    回應
  </summary>
  {: .text-delta}

```json
{
  "took": 14,
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
    "max_score": null,
    "hits": [
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "knfxQaEBH4GznK_vmeM7",
        "_version": 1,
        "_seq_no": 28,
        "_primary_term": 1,
        "_score": null,
        "_source": {
          "created_time": 1792107714677,
          "memory": "Alex likes hiking.",
          "last_updated_time": 1792107714677,
          "namespace_size": 1,
          "namespace": {
            "user_id": "your_user_id"
          },
          "strategy_id": "semantic_8f9ade02",
          "strategy_type": "SEMANTIC",
          "memory_container_id": "xthvpZgBOh0h20Y9O3Sa"
        },
        "sort": [1792107714677]
      },
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "jnfxQaEBH4GznK_vmOPV",
        "_version": 1,
        "_seq_no": 26,
        "_primary_term": 1,
        "_score": null,
        "_source": {
          "created_time": 1792107714561,
          "memory": "Alex likes hiking.",
          "last_updated_time": 1792107714561,
          "namespace_size": 1,
          "namespace": {
            "user_id": "your_user_id"
          },
          "strategy_id": "user_preference_5f897716",
          "strategy_type": "USER_PREFERENCE",
          "memory_container_id": "xthvpZgBOh0h20Y9O3Sa"
        },
        "sort": [1792107714561]
      },
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "c3fxQaEBH4GznK_vi-No",
        "_version": 1,
        "_seq_no": 16,
        "_primary_term": 1,
        "_score": null,
        "_source": {
          "created_time": 1792107710851,
          "memory": "Alex is a software engineer.",
          "last_updated_time": 1792107710851,
          "namespace_size": 1,
          "namespace": {
            "user_id": "your_user_id"
          },
          "strategy_id": "user_preference_5f897716",
          "strategy_type": "USER_PREFERENCE",
          "memory_container_id": "xthvpZgBOh0h20Y9O3Sa"
        },
        "sort": [1792107710851]
      },
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "dHfxQaEBH4GznK_vi-No",
        "_version": 2,
        "_seq_no": 34,
        "_primary_term": 1,
        "_score": null,
        "_source": {
          "created_time": 1792107710851,
          "memory": "Alex lives in Portland.",
          "last_updated_time": 1792107743470,
          "namespace_size": 1,
          "namespace": {
            "user_id": "your_user_id"
          },
          "strategy_id": "user_preference_5f897716",
          "strategy_type": "USER_PREFERENCE",
          "memory_container_id": "xthvpZgBOh0h20Y9O3Sa"
        },
        "sort": [1792107710851]
      },
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "cXfxQaEBH4GznK_vi-Ne",
        "_version": 1,
        "_seq_no": 12,
        "_primary_term": 1,
        "_score": null,
        "_source": {
          "created_time": 1792107710840,
          "memory": "Alex is a software engineer.",
          "last_updated_time": 1792107710840,
          "namespace_size": 1,
          "namespace": {
            "user_id": "your_user_id"
          },
          "strategy_id": "semantic_8f9ade02",
          "strategy_type": "SEMANTIC",
          "memory_container_id": "xthvpZgBOh0h20Y9O3Sa"
        },
        "sort": [1792107710840]
      },
      {
        "_index": ".plugins-ml-am-default-memory-long-term",
        "_id": "cnfxQaEBH4GznK_vi-Ne",
        "_version": 2,
        "_seq_no": 35,
        "_primary_term": 1,
        "_score": null,
        "_source": {
          "created_time": 1792107710840,
          "memory": "Alex lives in Portland.",
          "last_updated_time": 1792107743470,
          "namespace_size": 1,
          "namespace": {
            "user_id": "your_user_id"
          },
          "strategy_id": "semantic_8f9ade02",
          "strategy_type": "SEMANTIC",
          "memory_container_id": "xthvpZgBOh0h20Y9O3Sa"
        },
        "sort": [1792107710840]
      }
    ]
  }
}
```
</details>

history 記憶類型會記錄記憶容器在處理對話時新增、更新與刪除的長期記憶。使用 Update Memory 與 Delete Agentic Memory API 所做的變更（例如本教學中代理程式的更新與刪除）不會記錄在 history 中。若要檢閱記憶容器所擷取的記憶，請傳送下列請求：

```json
GET /_plugins/_ml/memory_containers/your_memory_container_id/memories/history/_search
{
  "query": {
    "match_all": {}
  },
  "sort": [
    {
      "created_time": {
        "order": "desc"
      }
    }
  ]
}
```
{% include copy-curl.html %}

## 後續步驟

- 如需記憶類型、策略與命名空間的詳細資訊，請參閱[代理記憶]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agentic-memory/)。
- 若要結合關鍵字搜尋與語意搜尋來搜尋記憶，請參閱 [Hybrid Search Agentic Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/hybrid-search-memory/)。
- 如需完整的記憶操作清單，請參閱 [Agentic Memory APIs]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/)。

## 相關文件

- [Create Memory Container API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/create-memory-container/)
- [Add Agentic Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/add-memory/)
- [Search Agentic Memory API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/agentic-memory-apis/search-memory/)
- [第三方機器學習平台的連接器]({{site.url}}{{site.baseurl}}/ml-commons-plugin/remote-models/connectors/)
