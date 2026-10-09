---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "修補允許清單"
parent: Allow list APIs
grand_parent: Security APIs
nav_order: 20
---

# 修補允許清單 API
**於 2.1 版推出**
{: .label .label-purple }

更新允許清單組態。

此 API 僅供超級管理員使用。請使用管理員憑證進行驗證，而非使用使用者名稱和密碼。如需詳細資訊，請參閱 [API 的存取控制]({{site.url}}{{site.baseurl}}/security/access-control/api/#access-control-for-the-api)。
{: .note}

<!-- spec_insert_start
api: security.patch_allowlist
component: endpoints
-->
## 端點
```json
PATCH /_plugins/_security/api/allowlist
```
<!-- spec_insert_end -->

## 請求本文欄位

請求本文為必要項目。它是由 JSON 物件組成的陣列。每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 | 必要 |
| :--- | :--- | :--- | :--- |
| `op` | 字串 | 要執行的操作。有效值為 `add`、`remove`、`replace`、`move`、`copy` 和 `test`。 | 是 |
| `path` | 字串 | 要修改的路徑，例如 `/config/enabled` 或 `/config/requests`。由於路徑使用 JSON Pointer 語法，請將請求路徑中的任何正斜線跳脫為 `~1`。例如，`/_cat/shards` 項目的路徑為 `/config/requests/~1_cat~1shards`。 | 是 |
| `value` | 物件或陣列 | 新的值。`add`、`replace` 和 `test` 操作必須提供此值。 | 否 |

## 請求範例

下列請求會將 `/_cat/shards` 端點新增至允許清單：

```json
PATCH _plugins/_security/api/allowlist
[
  {
    "op": "add",
    "path": "/config/requests/~1_cat~1shards",
    "value": [
      "GET"
    ]
  }
]
```
{% include copy-curl.html security=true %}

## 回應範例

```json
{
  "status": "OK",
  "message": "Resource updated."
}
```
