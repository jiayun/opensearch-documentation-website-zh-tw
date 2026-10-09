---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "執行工具"
parent: ML Commons APIs
nav_order: 100
---

# Execute Tool API
**於 3.3 版推出**
{: .label .label-purple }

Execute Tool API 讓您無須先建立代理程式，即可直接執行個別工具。此 API 特別適合需要快速執行單一工具操作的應用程式，這類應用程式不需要建立及管理代理程式所帶來的額外負擔。

## 使用案例

Execute Tool API 適合以下用途：

- **直接執行工具**：無須設定代理程式，即可執行搜尋、資料分析或擷取作業等特定工具。
- **測試與偵錯**：在開發期間快速測試工具功能。
- **輕量整合**：將特定 OpenSearch 功能整合至應用程式，無須使用完整的代理程式工作流程。
- **獨立作業**：執行不需要對話記憶或複雜協調的單一任務。

## 支援的工具

此 API 支援所有可用的 OpenSearch 工具。每個工具都可以使用其特定參數獨立執行。

如需可用工具清單的詳細資訊，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)。

## 端點

```json
POST /_plugins/_ml/tools/_execute/{tool_name}
```

`<tool_name>` 參數是指預先定義的工具類型名稱，例如 `PPLTool`、`SearchIndexTool` 或 `VectorDBTool`，而非您定義的自訂工具名稱。
{: .note}

## 請求本文欄位

下表列出所有請求本文欄位。

| 欄位 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `parameters` | 物件 | 是 | 包含工具專屬的參數，這些參數會依執行的工具而異。每個工具會根據其功能需要不同的參數。 |

### 參數結構

`parameters` 物件結合了工具註冊與工具執行期間使用的參數。具體欄位取決於執行的工具。

若要確定特定工具所需的參數，請參閱[工具]({{site.url}}{{site.baseurl}}/ml-commons-plugin/agents-tools/tools/index/)一節中的個別工具文件。

| 元件                | 說明                                    |
|:-------------------------|:-----------------------------------------------|
| 工具註冊參數 | 工具註冊期間指定的參數。 |
| 工具執行參數  | 工具執行期間指定的參數。    |

## 請求範例

以下提供簡單與複雜工具執行的範例。

### 範例 1：簡單工具執行

```json
POST /_plugins/_ml/tools/_execute/ListIndexTool
{
  "parameters": {
    "question": "How many indices do I have?"
  }
}
```
{% include copy-curl.html %}

### 回應範例

```json
{
  "inference_results": [
    {
      "output": [
        {
          "name": "response",
          "result": """row,health,status,index,uuid,pri(number of primary shards),rep(number of replica shards),docs.count(number of available documents),docs.deleted(number of deleted documents),store.size(store size of primary and replica shards),pri.store.size(store size of primary shards)
1,yellow,open,movies,kKcJKu2aT0C9uwJIPP4hxw,2,1,2,0,7.8kb,7.8kb
2,green,open,.plugins-ml-config,h8ovp_KFTq6_zvcBEn2kvg,1,0,1,0,4kb,4kb
3,green,open,.plugins-ml-agent,1oGlUBCIRAGXLbLv27Qg8w,1,0,1,0,8kb,8kb
"""
        }
      ]
    }
  ]
}
```

### 範例 2：複雜工具執行

```json
POST /_plugins/_ml/tools/_execute/PPLTool
{
  "parameters": {
    "question": "what's the population of Seattle in 2021?",
    "index": "test-population",
    "model_id": "1TuQQ5gBMJhRgCqgSV79"
  }
}

```
{% include copy-curl.html %}

### 回應範例

```json
{
    "inference_results": [
        {
            "output": [
                {
                    "name": "response",
                    "dataAsMap": {
                        "result":"{\"ppl\":\"source\=test-population | where QUERY_STRING([\'population_description\'], \'Seattle\') AND QUERY_STRING([\'population_description\'], \'2021\')\",\"executionResult\":\"{\\n  \\\"schema\\\": [\\n    {\\n      \\\"name\\\": \\\"population_description\\\",\\n      \\\"type\\\": \\\"string\\\"\\n    }\\n  ],\\n  \\\"datarows\\\": [],\\n  \\\"total\\\": 0,\\n  \\\"size\\\": 0\\n}\"}"
                    }
                }
            ]
        }
    ]
}
```