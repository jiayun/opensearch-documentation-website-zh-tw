---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除情境管理"
parent: Context management APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# 刪除情境管理 API
**於 3.5 版推出**
{: .label .label-purple }

使用此 API 刪除情境管理組態。刪除後，代理程式即無法再使用該情境管理。

刪除情境管理組態不會影響目前正在使用它的代理程式。不過，新的代理程式註冊或執行將無法參照已刪除的情境管理。
{: .note}

## 端點

```json
DELETE /_plugins/_ml/context_management/{context_management_name}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`context_management_name` | 字串 | 必要 | 要刪除的情境管理名稱。

## 範例請求

```json
DELETE /_plugins/_ml/context_management/advanced-context-management
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "context_management_name": "advanced-context-management",
  "status": "deleted"
}
```

## 錯誤回應

如果您嘗試刪除不存在的情境管理組態，API 會傳回 404 錯誤，指出找不到該資源：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "status_exception",
        "reason": "Context management template not found: sliding_window_max_40000_tokens_managers123"
      }
    ],
    "type": "status_exception",
    "reason": "Context management template not found: sliding_window_max_40000_tokens_managers123"
  },
  "status": 404
}
```

## 相關文件

如需更多資訊，請參閱[情境管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。