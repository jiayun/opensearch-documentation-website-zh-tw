---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立脈絡管理"
parent: Context management APIs
grand_parent: ML Commons APIs
nav_order: 10
---

# Create Context Management API
**於 3.5 版推出**
{: .label .label-purple }

使用此 API 設定[脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)，定義脈絡管理器團隊，以在特定執行點最佳化代理程式的脈絡。

## 端點

```json
POST /_plugins/_ml/context_management/{context_management_name}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`context_management_name` | 字串 | 必要 | 脈絡管理的唯一名稱。

## 請求本文欄位

下表列出可用的請求本文欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`description` | 字串 | 選用 | 以人類可讀的方式描述此脈絡管理的功能。
`hooks` | 物件 | 必要 | 將掛鉤名稱對應至脈絡管理器組態清單的對應關係。請參閱 [`hooks` 物件](#the-hooks-object)。

### hooks 物件

`hooks` 物件將掛鉤名稱對應至脈絡管理器組態陣列。支援下列掛鉤。

掛鉤 | 說明
:--- | :---
`pre_llm` | 在傳送請求至大型語言模型（LLM）之前執行。
`post_tool` | 在工具執行完成後執行。

每個掛鉤都包含一個脈絡管理器組態陣列，其中具有下列欄位。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`type` | 字串 | 必要 | 脈絡管理器類型。有效值為 `SlidingWindowManager`、`SummarizationManager` 和 `ToolsOutputTruncateManager`。
`config` | 物件 | 必要 | 脈絡管理器類型專用的組態。請參閱[脈絡管理器組態](#context-manager-configurations)。

### 脈絡管理器組態

依據脈絡管理器類型，支援下列脈絡管理器組態。

#### SlidingWindowManager

`SlidingWindowManager` 支援 `config` 物件中的下列參數。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`max_messages` | 整數 | 選用 | 要保留的訊息數量上限。預設為 `20`。
`activation` | 物件 | 選用 | 啟動規則。預設為一律啟動。請參閱[啟動規則](#activation-rules)。

#### SummarizationManager

`SummarizationManager` 支援 `config` 物件中的下列參數。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`summary_ratio` | 雙精度浮點數 | 選用 | 要摘要的訊息比例（0.1--0.8）。預設為 `0.3`。
`preserve_recent_messages` | 整數 | 選用 | 要保留的近期訊息數量。預設為 `10`。
`summarization_model_id` | 字串 | 選用 | 用於摘要的模型 ID。若未指定，則使用代理程式的模型。
`summarization_system_prompt` | 字串 | 選用 | 用於摘要的系統提示。若未指定，則使用預設系統提示。
`activation` | 物件 | 選用 | 啟動規則。預設為一律啟動。請參閱[啟動規則](#activation-rules)。

#### ToolsOutputTruncateManager

`ToolsOutputTruncateManager` 支援 `config` 物件中的下列參數。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`max_output_length` | 整數 | 選用 | 要保留的工具輸出長度上限。預設為 `40000`。
`activation` | 物件 | 選用 | 啟動規則。預設為一律啟動。請參閱[啟動規則](#activation-rules)。

### 啟動規則

啟動規則決定脈絡管理器應於何時執行。若省略，管理器會一律執行。多個規則使用 `AND` 邏輯，必須滿足所有規則才會啟動。如需更多資訊與範例，請參閱[啟動規則]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/#activation-rules)。

欄位 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`rule_type` | 字串 | 選用 | 設為 `always`，即可一律啟動管理器。
`message_count_exceed` | 整數 | 選用 | 當訊息數量超過此閾值時啟動。
`tokens_exceed` | 整數 | 選用 | 當詞元數量超過此閾值時啟動。

## 請求範例：基本滑動視窗脈絡管理

```json
POST /_plugins/_ml/context_management/basic-sliding-window
{
  "description": "Basic sliding window context management",
  "hooks": {
    "pre_llm": [
      {
        "type": "SlidingWindowManager",
        "config": {
          "max_messages": 6,
          "activation": {
            "message_count_exceed": 12
          }
        }
      }
    ]
  }
}
```
{% include copy-curl.html %}

## 回應範例

```json
{
  "context_management_name": "basic-sliding-window",
  "status": "created"
}
```

## 相關文件

如需更多資訊，請參閱[脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。

