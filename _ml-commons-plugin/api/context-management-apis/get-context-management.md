---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得上下文管理"
parent: Context management APIs
grand_parent: ML Commons APIs
nav_order: 20
---

# 取得上下文管理 API
**於 3.5 版推出**
{: .label .label-purple }

使用此 API 依名稱擷取上下文管理組態。

## 端點

```json
GET /_plugins/_ml/context_management/{context_management_name}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 必要／選用 | 說明
:--- | :--- | :--- | :---
`context_management_name` | 字串 | 必要 | 要擷取的上下文管理名稱。

## 範例請求

```json
GET /_plugins/_ml/context_management/token-aware-truncation
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "description": "Context management that truncates tool outputs longer than 100,000 characters and applies sliding window to keep last 6 messages when tokens exceed 200,000",
  "hooks": {
    "post_tool": [
      {
        "type": "ToolsOutputTruncateManager",
        "config": {
          "max_output_length": 100000
        }
      }
    ],
    "pre_llm": [
      {
        "type": "SlidingWindowManager",
        "config": {
          "max_messages": 6,
          "activation": {
            "tokens_exceed": 200000
          }
        }
      }
    ]
  },
  "created_time": 1754943902286,
  "last_modified": 1754943902286,
  "created_by": "admin"
}
```

## 相關文件

如需更多資訊，請參閱[上下文管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。