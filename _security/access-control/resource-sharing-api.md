---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "資源共用 API"
parent: Resource sharing and access control
grand_parent: Access control
nav_order: 10
---

# 資源共用 API
**3.3 版新增**
{: .label .label-purple }

資源共用 API 提供程式化存取，用於管理外掛程式所定義資源的細微文件層級存取控制。這些 API 可讓您共用資源、管理存取權限，並自動化資源共用工作流程。

您可以直接使用這些 REST API 來管理資源共用。只有當您是資源擁有者、超級管理員，或對該資源具有共用存取權時，才能執行相關操作。

## 遷移舊版共用中繼資料

匯入舊版由外掛程式管理的共用中繼資料。此 API 旨在系統遷移期間由管理員執行一次。

### 端點

```json
POST _plugins/_security/api/resources/migrate
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `source_index` | 字串 | 包含舊版共用中繼資料的來源索引。必要。 |
| `username_path` | 字串 | 指向擁有者名稱的 JSON 路徑 (例如 `/owner/name`)。必要。 |
| `backend_roles_path` | 字串 | 指向後端角色的 JSON 路徑 (例如 `/owner/backend_roles`)。必要。 |
| `default_owner` | 字串 | 未明確指定擁有者之資源的預設擁有者。必要。 |
| `default_access_level` | 物件 | 依資源類型區分的預設存取層級。若資源索引包含多種資源類型，請新增其他項目。必要。 |

### 範例請求

```json
POST _plugins/_security/api/resources/migrate
{
  "source_index": "legacy-sharing-index",
  "username_path": "/owner/name",
  "backend_roles_path": "/owner/backend_roles",
  "default_owner": "admin",
  "default_access_level": {
    "ml-model-group": "read_only",
    "anomaly-detector": "read_write"
  }
}
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
  "summary": "Migration complete. migrated 10; skippedNoType 1; skippedExisting 0; failed 1",
  "resourcesWithDefaultOwner": ["doc-17"],
  "skippedResources": ["doc-22"]
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `summary` | 字串 | 描述遷移結果的摘要訊息，包括已遷移、已略過及失敗的資源數量。 |
| `resourcesWithDefaultOwner` | 陣列 | 因找不到擁有者資訊而被指派預設擁有者的資源 ID 清單。 |
| `skippedResources` | 陣列 | 遷移期間被略過的資源 ID 清單 (例如缺少類型資訊或已遷移)。 |

### 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`restapi:admin/resource_sharing/migrate`。

## 取得共用組態

擷取特定資源目前的共用組態。

### 端點

```json
GET _plugins/_security/api/resource/share
```

### 查詢參數

下表列出可用的查詢參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `resource_id` | 字串 | 資源的唯一識別碼。必要。 |
| `resource_type` | 字串 | 資源的類型 (例如 `ml-model-group`)。必要。 |

### 範例請求

```json
GET _plugins/_security/api/resource/share?resource_id=model-group-123&resource_type=ml-model-group
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
  "sharing_info": {
    "resource_id": "model-group-123",
    "created_by": {
      "user": "admin"
    },
    "share_with": {
      "read_only": {
        "users": ["bob"],
        "roles": ["data_viewer"],
        "backend_roles": []
      },
      "read_write": {
        "users": ["charlie"],
        "roles": [],
        "backend_roles": ["ml_team"]
      }
    }
  }
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `sharing_info` | 物件 | 包含該資源的完整共用組態。 |
| `sharing_info.resource_id` | 字串 | 資源的唯一識別碼。 |
| `sharing_info.created_by` | 物件 | 資源建立者的相關資訊。 |
| `sharing_info.created_by.user` | 字串 | 資源建立者的使用者名稱。 |
| `sharing_info.share_with` | 物件 | 依存取層級組織的共用組態。 |
| `sharing_info.share_with.<access_level>` | 物件 | 一個存取層級 (例如 `read_only`、`read_write`)，包含主體清單。 |
| `sharing_info.share_with.<access_level>.users` | 陣列 | 具有此存取層級的使用者名稱清單。 |
| `sharing_info.share_with.<access_level>.roles` | 陣列 | 具有此存取層級的角色清單。 |
| `sharing_info.share_with.<access_level>.backend_roles` | 陣列 | 具有此存取層級的後端角色清單。 |

### 必要權限

如果您使用 Security 外掛程式，請確認您具備適當的權限：`cluster:admin/security/resource/share`。

## 取代資源共用組態

完全取代資源的共用組態。此操作會覆寫所有現有的共用設定。

### 端點

```json
PUT _plugins/_security/api/resource/share
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `resource_id` | 字串 | 資源的唯一識別碼。必要。 |
| `resource_type` | 字串 | 資源的類型。必要。 |
| `share_with` | 物件 | 依存取層級組織的共用組態。每個存取層級可包含 `users`、`roles` 和 `backend_roles` 陣列。必要。 |

### 範例請求：與特定使用者和角色共用

```json
PUT _plugins/_security/api/resource/share
{
  "resource_id": "model-group-123",
  "resource_type": "ml-model-group",
  "share_with": {
    "read_only": {
      "users": ["bob"],
      "roles": ["data_viewer"]
    },
    "read_write": {
      "users": ["charlie"],
      "backend_roles": ["ml_team"]
    }
  }
}
```
{% include copy-curl.html security=true %}

### 範例請求：將資源設為私人

```json
PUT _plugins/_security/api/resource/share
{
  "resource_id": "model-group-123",
  "resource_type": "ml-model-group",
  "share_with": {}
}
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
  "sharing_info": {
    "resource_id": "model-group-123",
    "created_by": {
      "user": "admin"
    },
    "share_with": {
      "read_only": {
        "users": ["bob"],
        "roles": ["data_viewer"],
        "backend_roles": []
      },
      "read_write": {
        "users": ["charlie"],
        "roles": [],
        "backend_roles": ["ml_team"]
      }
    }
  }
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `sharing_info` | 物件 | 包含該資源的完整共用組態。 |
| `sharing_info.resource_id` | 字串 | 資源的唯一識別碼。 |
| `sharing_info.created_by` | 物件 | 資源建立者的相關資訊。 |
| `sharing_info.created_by.user` | 字串 | 資源建立者的使用者名稱。 |
| `sharing_info.share_with` | 物件 | 依存取層級組織的共用組態。 |
| `sharing_info.share_with.<access_level>` | 物件 | 一個存取層級 (例如 `read_only`、`read_write`)，包含主體清單。 |
| `sharing_info.share_with.<access_level>.users` | 陣列 | 具有此存取層級的使用者名稱清單。 |
| `sharing_info.share_with.<access_level>.roles` | 陣列 | 具有此存取層級的角色清單。 |
| `sharing_info.share_with.<access_level>.backend_roles` | 陣列 | 具有此存取層級的後端角色清單。 |

### 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/security/resource/share`。

## 更新資源共用組態

在不影響現有共用組態的情況下新增或移除存取權。此操作為非破壞性，並會保留目前的存取設定。

### 端點

```json
PATCH _plugins/_security/api/resource/share
```

### 請求本文欄位

下表列出可用的請求本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `resource_id` | 字串 | 資源的唯一識別碼。必要。 |
| `resource_type` | 字串 | 資源的類型。必要。 |
| `add` | 物件 | 要新增的存取權，依存取層級分類。選用。 |
| `revoke` | 物件 | 要移除的存取權，依存取層級分類。選用。 |

### 範例請求：同時新增與撤銷存取權

```json
PATCH _plugins/_security/api/resource/share
{
  "resource_id": "model-group-123",
  "resource_type": "ml-model-group",
  "add": {
    "read_only": { "users": ["dave"] }
  },
  "revoke": {
    "read_write": { "users": ["charlie"] }
  }
}
```
{% include copy-curl.html security=true %}

### 範例請求：將資源設為公開

```json
PATCH _plugins/_security/api/resource/share
{
  "resource_id": "model-group-123",
  "resource_type": "ml-model-group",
  "add": {
    "read_only": { "users": ["*"] }
  }
}
```
{% include copy-curl.html security=true %}

### 範例請求：移除特定存取權

```json
PATCH _plugins/_security/api/resource/share
{
  "resource_id": "model-group-123",
  "resource_type": "ml-model-group",
  "revoke": {
    "read_write": { "users": ["charlie"] }
  }
}
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
  "sharing_info": {
    "resource_id": "model-group-123",
    "created_by": {
      "user": "admin"
    },
    "share_with": {
      "read_only": {
        "users": ["bob", "dave"],
        "roles": ["data_viewer"],
        "backend_roles": []
      },
      "read_write": {}
    }
  }
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `sharing_info` | 物件 | 包含修改後資源的完整共用組態。 |
| `sharing_info.resource_id` | 字串 | 資源的唯一識別碼。 |
| `sharing_info.created_by` | 物件 | 資源建立者的相關資訊。 |
| `sharing_info.created_by.user` | 字串 | 資源建立者的使用者名稱。 |
| `sharing_info.share_with` | 物件 | 更新後的共用組態，依存取層級分類。 |
| `sharing_info.share_with.<access_level>` | 物件 | 一個存取層級，包含新增/撤銷操作後的主體清單。 |
| `sharing_info.share_with.<access_level>.users` | 陣列 | 具有此存取層級的使用者名稱清單。 |
| `sharing_info.share_with.<access_level>.roles` | 陣列 | 具有此存取層級的角色清單。 |
| `sharing_info.share_with.<access_level>.backend_roles` | 陣列 | 具有此存取層級的後端角色清單。 |

### 必要權限

如果您使用 Security 外掛程式，請確認您具有適當的權限：`cluster:admin/security/resource/share`。

## 列出可存取的資源

傳回您有權檢視或管理的特定類型的所有資源。

### 端點

```json
GET _plugins/_security/api/resource/list
```

### 查詢參數

下表列出可用的查詢參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `resource_type` | 字串 | 要列出的資源類型。必要。 |

### 範例請求

```json
GET _plugins/_security/api/resource/list?resource_type=ml-model-group
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
  "resources": [
    {
      "resource_id": "model-group-123",
      "created_by": {
        "user": "admin",
        "tenant": "default"
      },
      "share_with": {
        "read_only": {
          "users": ["bob"]
        }
      },
      "can_share": true
    },
    {
      "resource_id": "model-group-456",
      "created_by": {
        "user": "alice",
        "tenant": "default"
      },
      "can_share": false
    }
  ]
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `resources` | 陣列 | 已驗證使用者可存取的資源清單。 |
| `resources[].resource_id` | 字串 | 資源的唯一識別碼。 |
| `resources[].created_by` | 物件 | 資源建立者的相關資訊。 |
| `resources[].created_by.user` | 字串 | 資源建立者的使用者名稱。 |
| `resources[].created_by.tenant` | 字串 | 與資源建立者相關聯的租用戶（若適用）。 |
| `resources[].share_with` | 物件 | 此資源的共用組態。若資源尚未共用，則可能不會有此欄位。 |
| `resources[].share_with.<access_level>` | 物件 | 一個存取層級，包含主體清單。 |
| `resources[].share_with.<access_level>.users` | 陣列 | 具有此存取層級的使用者名稱清單。 |
| `resources[].can_share` | 布林值 | 指出已驗證使用者是否具有共用此資源的權限。 |

### 必要權限

此 API 需要已驗證的存取權，但不需要特定的叢集權限。

## 列出資源類型

傳回所有可用的可共用資源類型及其支援的存取層級。OpenSearch Dashboards 會使用此 API 來判斷每種資源類型所支援的存取層級。

### 端點

```json
GET _plugins/_security/api/resource/types
```

### 範例請求

```json
GET _plugins/_security/api/resource/types
```
{% include copy-curl.html security=true %}

### 範例回應

```json
{
  "types": [
    {
      "type": "ml-model-group",
      "action_groups": ["ml_read_only", "ml_read_write", "ml_full_access"]
    },
    {
      "type": "anomaly-detector",
      "action_groups": ["ad_read_only", "ad_full_access"]
    }
  ]
}
```

### 回應本文欄位

下表列出所有回應本文欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `types` | 陣列 | 系統中可用資源類型的清單。 |
| `types[].type` | 字串 | 資源類型的名稱。 |
| `types[].action_groups` | 陣列 | 此資源類型可用動作群組（存取層級）的清單。 |

### 必要權限

此 API 需要已驗證的存取權，但不需要特定的叢集權限。

## 相關文件

- [資源共用與存取控制]({{site.url}}{{site.baseurl}}/security/access-control/resources/) -- 後端概念、組態與設定
- [資源存取管理]({{site.url}}{{site.baseurl}}/dashboards/management/resource-sharing/) -- UI 工作流程與使用者指引