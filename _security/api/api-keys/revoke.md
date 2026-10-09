---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "撤銷 API 金鑰"
parent: API key APIs
grand_parent: Security APIs
nav_order: 30
redirect_from:
  - /api-reference/security/api-keys/revoke/
---

# 撤銷 API 金鑰 API
**推出於 3.7**
{: .label .label-purple }

撤銷 API 金鑰，使其立即無法用於驗證。這是軟刪除：金鑰仍會出現在清單回應中，並帶有 `revoked_at` 時間戳記。

撤銷 API 金鑰時請注意下列事項：

- 撤銷為同步作業：在回應傳回之前，金鑰會以無效狀態廣播至所有節點。
- 已撤銷的金鑰無法重新啟用。
- 撤銷後無法重複使用該金鑰名稱。

## 端點

```json
DELETE /_plugins/_security/api/apitokens/{id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `id` | 字串 | 是 | 要撤銷之金鑰的唯一識別碼。 |

## 範例請求

```json
DELETE _plugins/_security/api/apitokens/_ofOi6ABkhwU_cGa4M3v
```
{% include copy-curl.html security=true %}

## 範例回應

```json
{
  "message": "Token _ofOi6ABkhwU_cGa4M3v revoked successfully."
}
```

## 回應本文欄位

回應本文是含有下列欄位的 JSON 物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `message` | 字串 | 確認金鑰已撤銷的訊息。 |
