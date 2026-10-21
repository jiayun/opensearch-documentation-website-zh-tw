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
`size` | 整數 | 選用 | 要傳回的結果數量上限。有效值為 1--1000。預設值為 `10`。
`from` | 整數 | 選用 | 分頁的起始索引。預設值為 `0`。

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

## 回應範例

```json
{
  "total": 1,
  "templates": [
    {
      "name": "sliding_window_max_40000_tokens_managers",
      "description": "Context management for truncating tool outputs to prevent input length issues",
      "hooks": {
        "PRE_LLM": [
          {
            "type": "SlidingWindowManager",
            "config": {
              "max_messages": 8
            }
          }
        ],
        "POST_TOOL": [
          {
            "type": "ToolsOutputTruncateManager",
            "config": {
              "max_output_length": 40000
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

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`total` | 整數 | 此回應中傳回的脈絡管理組態數量。
`templates` | 陣列 | 脈絡管理組態的清單。欄位說明請參閱 [Get Context Management API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/get-context-management/#response-body-fields)。

## 相關文件

如需更多資訊，請參閱[脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。