---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "建立 API 金鑰"
parent: API key APIs
grand_parent: Security APIs
nav_order: 10
redirect_from:
  - /api-reference/security/api-keys/create/
---

# Create API Key API
**3.7 版新增**
{: .label .label-purple }

建立具有指定權限與有效期間的新 API 金鑰。

## 端點

```json
POST /_plugins/_security/api/apitokens
```

## 請求本文欄位

請求本文為必要內容。它是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `name` | 字串 | 金鑰的唯一名稱。必須符合 `[a-zA-Z0-9_-]+` 模式。 | 是 |
| `cluster_permissions` | 字串陣列 | 授與金鑰的叢集層級權限或動作群組。預設為空陣列。 | 否 |
| `index_permissions` | 物件陣列 | 授與金鑰的索引層級權限。預設為空陣列。 | 否 |
| `duration_seconds` | Long | 金鑰的有效期間，以秒為單位。最大值由 `max_duration_seconds` 設定，預設為 7,776,000（90 天）。若省略，金鑰的有效期間為 `max_duration_seconds`。 | 否 |

`index_permissions` 物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `index_pattern` | 字串陣列 | 權限適用的索引。支援萬用字元模式，例如 `logs-*`。 | 是 |
| `allowed_actions` | 字串陣列 | 在符合的索引上允許的動作或動作群組。 | 是 |

## 範例請求

```json
POST _plugins/_security/api/apitokens
{
  "name": "test-token",
  "duration_seconds": 86400,
  "cluster_permissions": [
    "cluster_monitor"
  ],
  "index_permissions": [
    {
      "index_pattern": [
        "logs*"
      ],
      "allowed_actions": [
        "read"
      ]
    }
  ]
}
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "id": "_ofOi6ABkhwU_cGa4M3v",
  "token": "os_7EoHbn6PVeBwnqFGFDT0g-NBSI46Nq5PutcHHsmCFHg"
}
```

`token` 值只會回傳一次，之後無法再次取得。請妥善保存。
{: .warning}

## 回應本文欄位

回應本文是一個包含下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `id` | 字串 | 金鑰的唯一識別碼（用於撤銷）。 |
| `token` | 字串 | 用於 `Authorization: ApiKey <token>` 標頭的純文字權杖。 |
