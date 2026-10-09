---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "處理器鏈"
has_children: false
nav_order: 30
---

# 處理器鏈
**於 3.3 版推出**
{: .label .label-purple }

處理器鏈能建立彈性的資料轉換管線，可同時處理輸入與輸出資料。將多個處理器串接在一起，即可建立循序轉換，讓每個處理器的輸出成為下一個處理器的輸入。

處理器提供下列功能：

- **轉換資料格式**：在不同資料結構（字串、JSON、陣列）之間轉換。
- **擷取特定資訊**：使用 JSONPath 或正規表示式模式擷取相關資料。
- **清理與篩選內容**：移除不需要的欄位或套用格式化規則。
- **標準化資料**：確保不同元件之間的資料格式一致。

處理器會依照其在陣列中出現的順序執行。每個處理器都會接收前一個處理器的輸出。
{: .note}

處理器鏈專為機器學習工作流程而設計，與資料匯入管線和搜尋管線中的處理器不同：

- [**資料匯入管線**]({{site.url}}{{site.baseurl}}/ingest-pipelines/)：在將文件編製索引至 OpenSearch 的過程中轉換文件。
- [**搜尋管線**]({{site.url}}{{site.baseurl}}/search-plugins/search-pipelines/)：在搜尋作業期間轉換查詢與搜尋結果。
- **處理器鏈**：在 ML Commons 工作流程（代理程式工具、模型輸入/輸出）中轉換資料。

處理器鏈提供專為 AI/ML 使用情境量身打造的資料轉換功能，例如清理模型回應、從 LLM 輸出中擷取結構化資料，以及準備模型推論的輸入。

## 組態

處理器可以在不同的情境中設定：

- **工具輸出**：在工具的 `parameters` 區段中新增 `output_processors` 陣列。
- **模型輸出**：在 `_predict` 呼叫時，於模型的 `parameters` 區段中新增 `output_processors` 陣列。
- **模型輸入**：在 `_predict` 呼叫時，於模型的 `parameters` 區段中新增 `input_processors` 陣列。

完整範例請參閱 [搭配代理程式的使用範例](#example-usage-with-agents) 與 [搭配模型的使用範例](#example-usage-with-models)。

## 支援的處理器類型

下表列出所有支援的處理器。

處理器 | 說明
:--- | :---
[`conditional`](#conditional) | 依據條件套用不同的處理器鏈。
[`extract_json`](#extract_json) | 從文字字串中擷取 JSON 物件或陣列。
[`for_each`](#for_each) | 逐一迭代陣列元素，並對每個元素套用一連串處理器。
[`jsonpath_filter`](#jsonpath_filter) | 使用 JSONPath 運算式擷取資料。
[`process_and_set`](#process_and_set) | 對輸入套用一連串處理器，並將結果設定在指定的 JSONPath 位置。
[`regex_capture`](#regex_capture) | 從正規表示式比對結果中擷取特定群組。
[`regex_replace`](#regex_replace) | 使用正規表示式模式取代文字。
[`remove_jsonpath`](#remove_jsonpath) | 使用 JSONPath 從 JSON 物件中移除欄位。
[`set_field`](#set_field) | 將欄位設定為指定的靜態值，或從另一個欄位複製值。
[`to_string`](#to_string) | 將輸入轉換為 JSON 字串表示法。

### 條件式處理器

依據條件套用不同的處理器鏈。

**參數**：

- `path`（字串，選用）：用於擷取條件評估所需值的 JSONPath 運算式。
- `routes`（陣列，必要）：條件與處理器對應的陣列。
- `default`（陣列，選用）：沒有任何條件符合時使用的預設處理器。

**支援的條件**：

- 精確值比對：`"value"`
- 數值比較：`">10"`、`"<5"`、`">="`、`"<="`、`"==5"`
- 存在性檢查：`"exists"`、`"null"`、`"not_exists"`
- 正規表示式比對：`"regex:pattern"`
- 包含文字：`"contains:substring"`

**組態範例**：

```json
{
  "type": "conditional",
  "path": "$.status",
  "routes": [
    {
      "green": [
        {"type": "regex_replace", "pattern": "status", "replacement": "healthy"}
      ]
    },
    {
      "red": [
        {"type": "regex_replace", "pattern": "status", "replacement": "unhealthy"}
      ]
    }
  ],
  "default": [
    {"type": "regex_replace", "pattern": "status", "replacement": "unknown"}
  ]
}
```

**輸入範例**：

```json
{"index": "test-index", "status": "green", "docs": 100}
```

**輸出範例**：

```json
{"index": "test-index", "healthy": "green", "docs": 100}
```

### extract_json

從文字字串中擷取 JSON 物件或陣列。

**參數**：

- `extract_type`（字串，選用）：要擷取的 JSON 類型：`"object"`、`"array"` 或 `"auto"`。預設為 `"auto"`。
- `default`（任意類型，選用）：JSON 擷取失敗時使用的預設值。

**組態範例**：

```json
{
  "type": "extract_json",
  "extract_type": "object",
  "default": {}
}
```

**輸入範例**：

```json
"The result is: {\"status\": \"success\", \"count\": 5} - processing complete"
```

**輸出範例**：

```json
{"status": "success", "count": 5}
```

### for_each

逐一迭代陣列元素，並對每個元素套用一連串處理器。適合用來一致地轉換陣列元素，例如新增缺少的欄位、篩選內容或將資料結構標準化。

**參數**：

- `path`（字串，必要）：指向要迭代之陣列的 JSONPath 運算式。必須使用 `[*]` 標記法來表示陣列元素。
- `processors`（陣列，必要）：要套用至每個陣列元素的處理器組態清單。

**行為**：

- 每個元素都會使用設定的處理器鏈獨立處理。
- 處理器鏈的輸出會取代原始元素。
- 如果路徑不存在或未指向陣列，則原樣傳回輸入。
- 如果某個元素的處理失敗，則保留原始元素。

**組態範例**：

```json
{
  "type": "for_each",
  "path": "$.items[*]",
  "processors": [
    {
      "type": "set_field",
      "path": "$.processed",
      "value": true
    }
  ]
}
```

**輸入範例**：

```json
{
  "items": [
    {"name": "item1", "value": 10},
    {"name": "item2", "value": 20}
  ]
}
```

**輸出範例**：

```json
{
  "items": [
    {"name": "item1", "value": 10, "processed": true},
    {"name": "item2", "value": 20, "processed": true}
  ]
}
```

### jsonpath_filter

使用 JSONPath 運算式擷取資料。

**參數**：

- `path`（字串，必要）：用於擷取資料的 JSONPath 運算式。
- `default`（任意類型，選用）：找不到路徑時使用的預設值。

**組態範例**：

```json
{
  "type": "jsonpath_filter",
  "path": "$.data.items[*].name",
  "default": []
}
```

**輸入範例**：

```json
{"data": {"items": [{"name": "item1"}, {"name": "item2"}]}}
```

**輸出範例**：

```json
["item1", "item2"]
```

### process_and_set

對輸入套用一連串處理器，並將結果設定在指定的 JSONPath 位置。

**參數**：

- `path`（字串，必要）：指定處理結果設定位置的 JSONPath 運算式。
- `processors`（陣列，必要）：要依序套用的處理器組態清單。

**路徑行為**：

- 如果路徑存在，將以處理後的值更新該路徑。
- 如果路徑不存在，處理器鏈會嘗試建立該路徑（適用於簡單的巢狀欄位）。
- 父路徑必須存在，新欄位的建立才會成功。

**組態範例**：

```json
{
  "type": "process_and_set",
  "path": "$.summary.clean_name",
  "processors": [
    {
      "type": "to_string"
    },
    {
      "type": "regex_replace",
      "pattern": "[^a-zA-Z0-9]",
      "replacement": "_"
    }
  ]
}
```

**輸入範例**：

```json
{"name": "Test Index!", "status": "active"}
```

**輸出範例**：

```json
{"name": "Test Index!", "status": "active", "summary": {"clean_name": "Test_Index_"}}
```

### regex_capture

從 regex 比對結果中擷取特定群組。如需 regex 語法詳細資訊，請參閱 [Java regex 語法](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。

**參數**：

- `pattern`（字串，必要）：含有擷取群組的規則運算式模式。
- `groups`（字串或陣列，選用）：要擷取的群組編號。可以是單一數字，例如 `"1"`，或陣列，例如 `"[1, 2, 4]"`。預設為 `"1"`。

**範例組態**：

```json
{
  "type": "regex_capture",
  "pattern": "(\\d+),(\\w+),(\\w+),([^,]+)",
  "groups": "[1, 4]"
}
```

**範例輸入**：

```json
"1,green,open,.plugins-ml-model-group,DCJHJc7pQ6Gid02PaSeXBQ,1,0"
```

**範例輸出**：

```json
["1", ".plugins-ml-model-group"]
```

### regex_replace

使用規則運算式模式取代文字。如需 regex 語法詳細資訊，請參閱 [Java regex 語法](https://docs.oracle.com/javase/8/docs/api/java/util/regex/Pattern.html)。

**參數**：
- `pattern`（字串，必要）：要比對的規則運算式模式。
- `replacement`（字串，選用）：取代文字。預設為 `""`。
- `replace_all`（布林值，選用）：要取代所有符合項目或僅取代第一個。預設為 `true`。

**範例組態**：

```json
{
  "type": "regex_replace",
  "pattern": "^.*?\n",
  "replacement": ""
}
```

**範例輸入**：

```json
"row,health,status,index\n1,green,open,.plugins-ml-model\n2,red,closed,test-index"
```

**範例輸出**：

```json
"1,green,open,.plugins-ml-model\n2,red,closed,test-index"
```

### remove_jsonpath

使用 JSONPath 從 JSON 物件中移除欄位。

**參數**：

- `paths`（陣列，必要）：識別要移除之欄位的 JSONPath 運算式陣列。

**範例組態**：

```json
{
  "type": "remove_jsonpath",
  "paths": ["$.sensitive_data"]
}
```

**範例輸入**：

```json
{"name": "user1", "sensitive_data": "secret", "public_info": "visible"}
```

**範例輸出**：

```json
{"name": "user1", "public_info": "visible"}
```

### set_field

將欄位設定為指定的靜態值，或從其他欄位複製值。

**參數**：

- `path`（字串，必要）：指定要在何處設定值的 JSONPath 運算式。
- `value`（任意類型，依條件必要）：要設定的靜態值。必須提供 `value` 或 `source_path`。
- `source_path`（字串，依條件必要）：要從中複製值的 JSONPath 運算式。必須提供 `value` 或 `source_path`。
- `default`（任意類型，選用）：`source_path` 不存在時的預設值。僅與 `source_path` 搭配使用。

**路徑行為**：

- 如果路徑存在，將會以新值更新。
- 如果路徑不存在，處理器鏈會嘗試建立它（適用於簡單的巢狀欄位）。
- 父路徑必須存在，才能成功建立新欄位。

**範例組態（靜態值）**：

```json
{
  "type": "set_field",
  "path": "$.metadata.processed_at",
  "value": "2024-03-15T10:30:00Z"
}
```

**範例組態（複製欄位）**：

```json
{
  "type": "set_field",
  "path": "$.userId",
  "source_path": "$.user.id",
  "default": "unknown"
}
```

**範例輸入**：

```json
{"user": {"id": 123}, "name": "John"}
```

**範例輸出**：

```json
{"user": {"id": 123}, "name": "John", "userId": 123, "metadata": {"processed_at": "2024-03-15T10:30:00Z"}}
```

### to_string

將輸入轉換為 JSON 字串表示法。

**參數**：

- `escape_json`（布林值，選用）：是否逸出 JSON 字元。預設為 `false`。

**範例組態**：

```json
{
  "type": "to_string",
  "escape_json": true
}
```

**範例輸入**：

```json
{"name": "test", "value": 123}
```

**範例輸出**：

```json
"{\"name\":\"test\",\"value\":123}"
```

## 搭配代理程式使用的範例

下列範例示範如何搭配代理程式使用處理器鏈。

### 步驟 1：註冊具有輸出處理器的流程代理程式

```json
POST /_plugins/_ml/agents/_register
{
  "name": "Index Summary Agent",
  "type": "flow",
  "description": "Agent that provides clean index summaries",
  "tools": [
    {
      "type": "ListIndexTool",
      "parameters": {
        "output_processors": [
          {
            "type": "regex_replace",
            "pattern": "^.*?\n",
            "replacement": ""
          },
          {
            "type": "regex_capture",
            "pattern": "(\\d+,\\w+,\\w+,([^,]+))"
          }
        ]
      }
    }
  ]
}
```
{% include copy-curl.html %}

### 步驟 2：執行代理程式

使用前一個步驟傳回的 `agent_id`：

```json
POST /_plugins/_ml/agents/{agent_id}/_execute
{
  "parameters": {
    "question": "List the indices"
  }
}
```
{% include copy-curl.html %}

若沒有輸出處理器，原始 `ListIndexTool` 會傳回冗長的 CSV 輸出，其中包含標頭與額外資料欄：

```cs
row,health,status,index,uuid,pri,rep,docs.count,docs.deleted,store.size,pri.store.size
1,green,open,.plugins-ml-model-group,DCJHJc7pQ6Gid02PaSeXBQ,1,0,1,0,12.7kb,12.7kb
2,green,open,.plugins-ml-memory-message,6qVpepfRSCi9bQF_As_t2A,1,0,7,0,53kb,53kb
3,green,open,.plugins-ml-memory-meta,LqP3QMaURNKYDZ9p8dTq3Q,1,0,2,0,44.8kb,44.8kb
```

輸出處理器會以下列方式將冗長的 CSV 輸出轉換為簡潔、易讀的格式：

1. **`regex_replace`**：移除 CSV 標頭列。
2. **`regex_capture`**：僅擷取必要資訊 (列號、健康狀態、狀態及索引名稱)。

有了輸出處理器，代理程式會傳回簡潔、格式化的資料，其中僅包含必要的索引資訊：

```cs
1,green,open,.plugins-ml-model-group
2,green,open,.plugins-ml-memory-message
3,green,open,.plugins-ml-memory-meta
```

## 搭配模型使用的範例

下列範例示範如何在 Predict API 呼叫期間搭配模型使用處理器鏈。

### 範例：輸入處理器

此範例示範如何使用 `input_processors` 修改模型輸入，以在處理前取代文字：

```json
POST _plugins/_ml/models/{model_id}/_predict
{
  "parameters": {
    "system_prompt": "You are a helpful assistant.",
    "prompt": "Can you summarize Prince Hamlet of William Shakespeare in around 100 words?",
    "input_processors": [
      {
        "type": "regex_replace",
        "pattern": "100",
        "replacement": "20"
      }
    ]
  }
}
```
{% include copy-curl.html %}

在此範例中，`regex_replace` 處理器會在提示傳送至模型前加以修改，將「100 words」變更為「20 words」。

### 範例：輸出處理器

此範例示範如何使用 `output_processors` 處理模型輸出，以擷取並格式化 JSON 資料。在此範例中，輸出處理器會先使用 JSONPath 從模型回應中擷取內容。接著，它們會從文字回應中剖析並擷取 JSON 物件：

```json
POST _plugins/_ml/models/{model_id}/_predict
{
  "parameters": {
    "messages": [
      {
        "role": "system",
        "content": [
          {
            "type": "text",
            "text": "${parameters.system_prompt}"
          }
        ]
      },
      {
        "role": "user",
        "content": [
          {
            "type": "text",
            "text": "Can you convert this into a json object: user name is Bob, he likes swimming"
          }
        ]
      }
    ],
    "system_prompt": "You are a helpful assistant",
    "output_processors": [
      {
        "type": "jsonpath_filter",
        "path": "$.choices[0].message.content"
      },
      {
        "type": "extract_json",
        "extract_type": "auto"
      }
    ]
  }
}
```
{% include copy-curl.html %}

若沒有輸出處理器，原始回應會包含完整的模型輸出，其中含有大量中繼資料與巢狀結構：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "id": "test-id",
            "object": "chat.completion",
            "created": 1.759580469E9,
            "model": "gpt-4o-mini-2024-07-18",
            "choices": [
              {
                "index": 0.0,
                "message": {
                  "role": "assistant",
                  "content": "Sure! Here is the information you provided converted into a JSON object:\n\n```json\n{\n  \"user\": {\n    \"name\": \"Bob\",\n    \"likes\": \"swimming\"\n  }\n}\n```",
                  "refusal": null,
                  "annotations": []
                },
                "logprobs": null,
                "finish_reason": "stop"
              }
            ],
            "usage": {
              "prompt_tokens": 33.0,
              "completion_tokens": 42.0,
              "total_tokens": 75.0,
              "prompt_tokens_details": {
                "cached_tokens": 0.0,
                "audio_tokens": 0.0
              },
              "completion_tokens_details": {
                "reasoning_tokens": 0.0,
                "audio_tokens": 0.0,
                "accepted_prediction_tokens": 0.0,
                "rejected_prediction_tokens": 0.0
              }
            },
            "service_tier": "default",
            "system_fingerprint": "test-fingerprint"
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```

有了輸出處理器，回應會簡化為僅包含所擷取並剖析的 JSON 資料：

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "dataAsMap": {
            "user": {
              "name": "Bob",
              "likes": "swimming"
            }
          }
        }
      ],
      "status_code": 200
    }
  ]
}
```
