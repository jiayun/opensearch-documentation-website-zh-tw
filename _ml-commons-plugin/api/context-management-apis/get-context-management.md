---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得脈絡管理"
parent: Context management APIs
grand_parent: ML APIs
nav_order: 20
---

# 取得脈絡管理 API
**於 3.5 版推出**
{: .label .label-purple }

使用此 API 依名稱擷取脈絡管理組態。

## 端點

```json
GET /_plugins/_ml/context_management/{context_management_name}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 必要／選用 | 說明
:--- | :--- | :--- | :---
`context_management_name` | 字串 | 必要 | 要擷取的脈絡管理名稱。

## 範例請求

```json
GET /_plugins/_ml/context_management/token-aware-truncation
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "name": "token-aware-truncation",
  "description": "Context management that truncates tool outputs longer than 100,000 characters and applies sliding window to keep last 6 messages when tokens exceed 200,000",
  "hooks": {
    "PRE_LLM": [
      {
        "type": "SlidingWindowManager",
        "config": {
          "max_messages": 6,
          "activation": {
            "tokens_exceed": 200000
          }
        }
      }
    ],
    "POST_TOOL": [
      {
        "type": "ToolsOutputTruncateManager",
        "config": {
          "max_output_length": 100000
        }
      }
    ]
  },
  "created_time": 1754943902286,
  "last_modified": 1754943902286,
  "created_by": "admin"
}
```

## 回應本文欄位

下表列出所有回應本文欄位。

欄位 | 資料類型 | 說明
:--- | :--- | :---
`name` | 字串 | 脈絡管理的名稱。
`description` | 字串 | 脈絡管理的描述。
`hooks` | 物件 | hook 名稱與其脈絡管理員組態清單的對應。如需更多資訊，請參閱 [`hooks` 物件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/#the-hooks-object)。
`created_time` | 長整數 | 脈絡管理的建立時間，以 epoch 毫秒表示。
`last_modified` | 長整數 | 脈絡管理最後更新的時間，以 epoch 毫秒表示。
`created_by` | 字串 | 建立脈絡管理的使用者。僅在啟用 Security 外掛程式時才會出現。

## 相關文件

如需更多資訊，請參閱 [脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。