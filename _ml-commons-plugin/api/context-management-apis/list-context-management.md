---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "列出脈絡管理"
parent: Context management APIs
grand_parent: ML Commons APIs
nav_order: 50
---

# List Context Management API
**3.5 版新增**
{: .label .label-purple }

使用此 API 擷取叢集中所有脈絡管理組態的清單。

## 端點

```json
GET /_plugins/_ml/context_management
```

## 查詢參數

下表列出可用的查詢參數。

參數 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`size` | 整數 | 選用 | 要傳回的最大結果數量。預設為 `10`。
`from` | 整數 | 選用 | 分頁的起始索引。預設為 `0`。

## 範例請求

```json
GET /_plugins/_ml/context_management
```
{% include copy-curl.html %}

## 含分頁的範例請求

```json
GET /_plugins/_ml/context_management?size=20&from=0
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "total": 1,
  "context_management": [
    {
      "name": "sliding_window_max_40000_tokens_managers",
      "description": "Context management for truncating tool outputs to prevent input length issues",
      "hooks": {
        "pre_llm": [
          {
            "type": "SlidingWindowManager",
            "config": {
              "max_messages": 8,
              "activation": {
                "rule_type": "always"
              }
            }
          }
        ],
        "post_tool": [
          {
            "type": "ToolsOutputTruncateManager",
            "config": {
              "max_output_length": 40000,
              "activation": {
                "rule_type": "always"
              }
            }
          }
        ]
      },
      "created_time": 1769457277774,
      "last_modified": 1769457277774
    }
  ]
}
```

## 相關文件

如需更多資訊，請參閱[脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。