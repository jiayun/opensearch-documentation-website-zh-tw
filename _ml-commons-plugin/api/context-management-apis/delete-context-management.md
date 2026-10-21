---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除脈絡管理"
parent: Context management APIs
grand_parent: ML Commons APIs
nav_order: 40
---

# 刪除脈絡管理 API
**於 3.5 版導入**
{: .label .label-purple }

使用此 API 刪除脈絡管理組態。一旦刪除，代理程式便無法再使用該脈絡管理。

代理程式儲存的是脈絡管理組態的名稱，而非其副本。刪除組態後，執行以其名稱註冊的代理程式會失敗並回傳 404 錯誤，而以其名稱註冊新的代理程式也會失敗並回傳 400 錯誤。若要執行這類代理程式，請以相同名稱重新建立組態，或在執行代理程式時於 `context_management_name` 參數指定不同的組態。
{: .note}

## 端點

```json
DELETE /_plugins/_ml/context_management/{context_management_name}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 必要/選用 | 說明
:--- | :--- | :--- | :---
`context_management_name` | 字串 | 必要 | 要刪除的脈絡管理名稱。

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

如果您嘗試刪除不存在的脈絡管理組態，API 會傳回 404 錯誤，指出找不到該資源：

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

如需更多資訊，請參閱[脈絡管理]({{site.url}}{{site.baseurl}}/ml-commons-plugin/context-management/)。