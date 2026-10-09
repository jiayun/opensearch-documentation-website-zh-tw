---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除記憶"
parent: Memory APIs
grand_parent: ML Commons APIs
nav_order: 30
---

# 刪除記憶 API
**於 2.12 版導入**
{: .label .label-purple }

使用此 API 根據 `memory_id` 刪除記憶。

啟用 Security 外掛程式時，所有記憶都存在於 `private` 安全性模式中。只有建立記憶的使用者才能與該記憶及其訊息互動。
{: .important}

## 端點

```json
DELETE /_plugins/_ml/memory/{memory_id}
```

## 路徑參數

下表列出可用的路徑參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`memory_id` | 字串 | 要刪除之記憶的 ID。

## 範例請求

```json
DELETE /_plugins/_ml/memory/MzcIJX8BA7mbufL6DOwl
```
{% include copy-curl.html %}

## 範例回應

```json
{
  "success": true
}
```

## 錯誤回應

如果您嘗試刪除不存在的記憶，OpenSearch 會傳回 404 錯誤：

```json
{
  "error": {
    "root_cause": [
      {
        "type": "resource_not_found_exception",
        "reason": "Memory [MzcIJX8BA7mbufL6DOwl] not found"
      }
    ],
    "type": "resource_not_found_exception",
    "reason": "Memory [MzcIJX8BA7mbufL6DOwl] not found"
  },
  "status": 404
}
```