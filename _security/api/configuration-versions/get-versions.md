---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "取得組態版本"
parent: Security configuration version APIs
grand_parent: Security APIs
nav_order: 10
---

# 取得安全性組態版本 API
**於 3.3 版導入**
{: .label .label-purple }

這是一項實驗性功能，不建議在正式環境中使用。若要了解此功能的進度或提供意見回饋，請加入 [OpenSearch 論壇](https://forum.opensearch.org/) 的討論。
{: .warning}

擷取安全性組態已儲存的版本。指定版本 ID 即可擷取單一版本，或省略該 ID 以擷取所有版本。

只有在啟用版本管理時，此 API 才會傳回結果。如需更多資訊，請參閱[安全性組態版本 API]({{site.url}}{{site.baseurl}}/security/api/configuration-versions/)。

## 端點

```json
GET /_plugins/_security/api/versions
GET /_plugins/_security/api/version/{version_id}
```

## 路徑參數

下表列出可用的路徑參數。所有路徑參數皆為選用。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `version_id` | 字串 | 要擷取的版本，指定為 `v` 加上數字，例如 `v1` 或 `v2`。若省略，回應會包含所有保留的版本。 |

## 範例請求

下列請求會擷取所有保留的版本：

```json
GET /_plugins/_security/api/versions
```
{% include copy-curl.html security=true %}

下列請求會擷取 `v2` 版本：

```json
GET /_plugins/_security/api/version/v2
```
{% include copy-curl.html security=true %}

## 範例回應

請求所有版本時，每個保留的版本會傳回一筆項目。下列回應中的 `security_configs` 物件已經過簡略：

```json
{
  "versions": [
    {
      "version_id": "v1",
      "timestamp": "2026-09-10T16:45:53.947225761Z",
      "modified_by": "system",
      "security_configs": { ... }
    },
    {
      "version_id": "v2",
      "timestamp": "2026-09-10T16:49:14.553429756Z",
      "modified_by": "system",
      "security_configs": { ... }
    }
  ]
}
```

請求單一版本時，只會傳回該版本。`security_configs` 中的每個鍵都是一種組態類型，而 `configData` 物件則保存該組態檔在版本建立當時的內容。下列回應已經過簡略：

```json
{
  "versions": [
    {
      "version_id": "v2",
      "timestamp": "2026-09-10T16:49:14.553429756Z",
      "modified_by": "system",
      "security_configs": {
        "internalusers": {
          "lastUpdated": "2026-09-10T16:49:14.553429756Z",
          "configData": {
            "_meta": {
              "type": "internalusers",
              "config_version": 2
            },
            "admin": {
              "backend_roles": [
                "admin"
              ],
              "opendistro_security_roles": [],
              "static": false,
              "hidden": false,
              "reserved": true,
              "description": "Demo admin user",
              "attributes": {},
              "hash": "$2y$12$cAO5zVKyJTyP7PuQ.cs4g.mxkwaPMmP76Ef8Uu2/l37BLgGzEQXZ2"
            }
          }
        },
        "roles": { ... },
        "rolesmapping": { ... },
        "actiongroups": { ... },
        "tenants": { ... },
        "config": { ... },
        "audit": { ... },
        "allowlist": { ... },
        "nodesdn": { ... }
      }
    }
  ]
}
```

若請求的版本不存在，OpenSearch 會傳回 `404 Not Found`：

```json
{
  "status": "NOT_FOUND",
  "message": "Version v99 not found"
}
```

## 回應本文欄位

回應本文是一個 JSON 物件，包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `versions` | 物件陣列 | 安全性組態保留的版本，由最舊到最新排序。 |

`versions` 中的每個物件包含下列欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `version_id` | 字串 | 版本識別碼，例如 `v1`。 |
| `timestamp` | 字串 | OpenSearch 建立該版本的時間，採 ISO 8601 格式。 |
| `modified_by` | 字串 | 進行組態變更的使用者，若 OpenSearch 無法將變更歸因於某位使用者，則為 `system`。 |
| `security_configs` | 物件 | 版本建立當時完整安全性組態的快照，以組態類型作為鍵。 |

<details markdown="block">
  <summary>
    回應本文欄位：<code>security_configs</code>
  </summary>
  {: .text-delta}

`security_configs` 中的每個鍵都是下列其中一種組態類型：`actiongroups`、`allowlist`、`audit`、`config`、`internalusers`、`nodesdn`、`roles`、`rolesmapping` 或 `tenants`。每種類型都對應到一個包含下列欄位的物件。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `lastUpdated` | 字串 | OpenSearch 擷取此組態類型的時間，採 ISO 8601 格式。 |
| `configData` | 物件 | 組態類型的內容，格式與對應 API 傳回的格式相同。例如，`internalusers` 項目會依名稱列出每位使用者，`roles` 項目則會依名稱列出每個角色。 |

</details>
