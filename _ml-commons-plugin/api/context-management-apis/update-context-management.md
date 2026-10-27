---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "更新脈絡管理"
parent: Context management APIs
grand_parent: ML APIs
nav_order: 30
---

# 更新脈絡管理 API
**於 3.5 版推出**
{: .label .label-purple }

使用此 API 更新現有的脈絡管理組態。您可以修改描述、掛鉤組態以及脈絡管理員設定。

## 端點

```json
PUT /_plugins/_ml/context_management/{context_management_name}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`context_management_name` | 字串 | 必要 | 要更新的脈絡管理名稱。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`description` | 字串 | 選用 | 此脈絡管理用途的易讀說明。
`hooks` | 物件 | 選用 | 將掛鉤名稱對應至脈絡管理員組態清單的對應表。請參閱[`hooks` 物件]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/#the-hooks-object)。

請求本文的結構與[建立脈絡管理 API]({{site.url}}{{site.baseurl}}/ml-commons-plugin/api/context-management-apis/create-context-management/)相同。省略的欄位會保留現有值。在 `hooks` 物件中，您指定的每個掛鉤都會取代該掛鉤的現有組態，省略的掛鉤則維持不變。

## 範例請求：更新描述

```json
PUT /_plugins/_ml/context_management/advanced-context-management
{
  "description": "Updated description for advanced context management with multiple strategies"
}
```
{% include copy-curl.html %}

## 範例請求：更新 hooks 組態

```json
PUT /_plugins/_ml/context_management/sliding_window_max_40000_tokens_managers
{
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
  }
}
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "_index": ".plugins-ml-context-management-templates",
  "_id": "sliding_window_max_40000_tokens_managers",
  "_version": 2,
  "result": "updated",
  "forced_refresh": true,
  "_shards": {
    "total": 1,
    "successful": 1,
    "failed": 0
  },
  "_seq_no": 4,
  "_primary_term": 1
}
```

## 相關文件

如需更多資訊，請參閱[脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。