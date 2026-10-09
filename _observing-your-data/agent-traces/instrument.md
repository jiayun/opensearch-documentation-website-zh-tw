---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "為您的應用程式進行檢測"
parent: Agent traces
nav_order: 10
---

# 為您的應用程式進行檢測
**於 3.6 版推出**
{: .label .label-purple }

`opensearch-genai-observability-sdk-py` 套件使用 [OpenTelemetry](https://opentelemetry.io/) 為 Python AI 代理程式進行檢測。此 SDK 提供兩種檢測方式：

- **自動檢測**：不需變更程式碼，即可自動擷取支援的供應商 (OpenAI、Anthropic、Amazon Bedrock、LangChain、LlamaIndex) 的 LLM 呼叫。
- **手動檢測**：使用 `@observe` 裝飾器來追蹤自訂的代理程式邏輯、工具呼叫及協調程式碼。

對大多數應用程式而言，請合併使用這兩種方式：為 LLM 呼叫啟用自動檢測，並使用 `@observe` 處理應用程式特定的操作。

## 先決條件

開始之前，請確認您具備下列項目：

- Python 3.10 或更新版本。
- 一個已設定 [Data Prepper]({{site.url}}{{site.baseurl}}/data-prepper/index/) 以進行追蹤匯入的 OpenSearch 叢集。
- 一個 [OpenTelemetry Collector](https://opentelemetry.io/docs/collector/)，用以使用生成式 AI 語意慣例來正規化 span。

## 安裝

安裝基礎套件：

```bash
pip install opensearch-genai-observability-sdk-py
```
{% include copy.html %}

若要為特定供應商啟用自動檢測，請安裝對應的選用相依套件。例如，若要檢測 OpenAI 和 LangChain：

```bash
pip install opensearch-genai-observability-sdk-py[openai,langchain]
```
{% include copy.html %}

下列供應商支援自動檢測：

| 供應商 | 套件名稱 |
| :--- | :--- |
| OpenAI | `openai` |
| Anthropic | `anthropic` |
| Amazon Bedrock | `bedrock` |
| Google | `google` |
| LangChain | `langchain` |
| LlamaIndex | `llamaindex` |

## 核心 API

下列各節說明核心 API 函式。

<!-- vale off -->
### register()
<!-- vale on -->

`register()` 函式會設定 OpenTelemetry 追蹤器與匯出工具。請在應用程式啟動時呼叫一次：

```python
from opentelemetry_genai_sdk import register

register(
    endpoint="http://localhost:4318",
    service_name="my-agent-app",
    protocol="http",
    auto_instrument=True
)
```
{% include copy.html %}

下表說明 `register()` 參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `endpoint` | 字串 | OpenTelemetry Protocol (OTLP) 端點 URL。OpenTelemetry Collector 的預設值為 `http://localhost:4318`。 |
| `service_name` | 字串 | 您的應用程式在追蹤資料中的識別碼。 |
| `protocol` | 字串 | 傳輸通訊協定。有效值為 `http` 和 `grpc`。 |
| `auto_instrument` | 布林值 | 當設為 `true` 時，會自動探索並啟用已安裝的供應商檢測套件。預設值為 `false`。 |

<!-- vale off -->
### @observe 裝飾器
<!-- vale on -->

`@observe` 裝飾器會包裝函式以自動建立 span。使用它來追蹤代理程式叫用、工具呼叫及其他操作：

```python
from opentelemetry_genai_sdk import observe, Op

@observe(op=Op.INVOKE_AGENT)
def run_agent(prompt: str):
    # Agent logic here
    return response

@observe(op=Op.EXECUTE_TOOL)
def search_database(query: str):
    # Tool logic here
    return results
```
{% include copy.html %}

此裝飾器支援同步函式、非同步函式、產生器及非同步產生器。Span 名稱會自動由函式名稱產生，您也可以使用 `name_from` 參數提供自訂名稱。

<!-- vale off -->
### enrich()
<!-- vale on -->

`enrich()` 函式會將 GenAI 語意屬性新增至作用中的 span：

```python
from opentelemetry_genai_sdk import enrich

enrich(
    model="gpt-4o-mini",
    provider="openai",
    input_tokens=150,
    output_tokens=50,
    finish_reason="stop"
)
```
{% include copy.html %}

<!-- vale off -->
### score()
<!-- vale on -->

`score()` 函式會將評估指標附加至追蹤或個別 span：

```python
from opentelemetry_genai_sdk import score

score(
    trace_id="abc123",
    name="relevance",
    value=0.95,
    explanation="Response directly addresses the query"
)
```
{% include copy.html %}

## 操作類型

`Op` 類別提供標準化的操作名稱，對應至 [GenAI 語意慣例](https://opentelemetry.io/docs/specs/semconv/gen-ai/)。這些操作類型會決定 span 在 **Agent Traces** 頁面中的分類與顯示方式。

| 操作 | 常數 | 說明 |
| :--- | :--- | :--- |
| 叫用代理程式 | `Op.INVOKE_AGENT` | 根層級的代理程式叫用。 |
| 執行工具 | `Op.EXECUTE_TOOL` | 代理程式內的工具或函式呼叫。 |
| 聊天 | `Op.CHAT` | LLM 聊天補全請求。 |
| 建立代理程式 | `Op.CREATE_AGENT` | 代理程式初始化。 |
| 擷取 | `Op.RETRIEVAL` | 文件或資料擷取操作。 |
| 產生嵌入 | `Op.EMBEDDINGS` | 嵌入產生請求。 |
| 文字補全 | `Op.TEXT_COMPLETION` | 文字補全請求。 |

## 架構整合

此 SDK 可與熱門的代理程式架構整合。一般模式是合併使用自動檢測 (用於 LLM 呼叫) 與手動 `@observe` 裝飾器 (用於代理程式特定的邏輯)。

### Strands Agents

Strands 支援這兩種方式：
- **原生 OpenTelemetry**：使用 `StrandsTelemetry` 自動為代理程式叫用、工具執行及 LLM 互動發出 span。
- **手動裝飾**：在自訂函式上使用 `@observe` 以進行額外的檢測。

### LangGraph

使用 `@observe` 包裝 LangGraph 節點與協調層。啟用自動檢測以自動擷取節點內的模型呼叫。

<!-- vale off -->
### CrewAI
<!-- vale on -->

使用 `@observe` 包裝 crew 執行函式。安裝適當的供應商套件 (例如 `[openai]`) 以自動擷取 crew 成員發出的 LLM 呼叫。

<!-- vale off -->
### OpenAI Agents SDK
<!-- vale on -->

啟用自動檢測以獲得完整的 LLM 涵蓋範圍。搭配使用 `@observe` 以處理頂層協調邏輯與自訂操作。

### Amazon Bedrock

安裝 `[bedrock]` 以自動擷取 `converse` 和 `invoke_model` 呼叫。使用 `@observe` 進行代理程式協調與自訂工具實作。

## 後續步驟

為您的應用程式進行檢測後，請設定 OpenSearch Dashboards 以檢視您的追蹤。如需組態與視覺化選項，請參閱[檢視代理程式追蹤]({{site.url}}{{site.baseurl}}/observing-your-data/agent-traces/agent-tracing/)。
