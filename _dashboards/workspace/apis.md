---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作區 API"
parent: Workspaces
nav_order: 10
---

# 工作區 API
**2.18 版推出**
{: .label .label-purple }

使用工作區 API 來管理 OpenSearch Dashboards 中的工作區。

這些端點由 OpenSearch Dashboards 提供，因此請將請求傳送至 OpenSearch Dashboards 的主機和連接埠（預設為 `5601`）。使用 `POST`、`PUT` 或 `DELETE` 的請求需要 `osd-xsrf: true` 標頭。為 Kibana OSS 撰寫的指令碼會改為傳送 `kbn-xsrf: true` 標頭，而 OpenSearch Dashboards 會拒絕這些請求，並傳回錯誤 `Request must contain a osd-xsrf header`。若要修正此錯誤，請將指令碼中的 `kbn-xsrf` 替換為 `osd-xsrf`。

## 列出工作區

您可以使用下列端點擷取工作區清單：

```json
POST {osd_host}:{port}/api/workspaces/_list
```
{% include copy.html %}

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `search` | 字串 | 選用 | 用於以簡單查詢語法篩選工作區的查詢字串，例如 `simple_query_string`。 |
| `searchFields` | 陣列 | 選用 | 指定要對哪些欄位執行搜尋查詢。 |
| `sortField` | 字串 | 選用 | 用於排序結果的欄位名稱。 |
| `sortOrder` | 字串 | 選用 | 指定遞增或遞減的排序順序。 |
| `perPage` | 數字 | 選用 | 每頁的工作區結果數量。 |
| `page` | 數字 | 選用 | 要擷取的結果頁數。 |
| `permissionModes` | 陣列 | 選用 | 用於篩選的權限清單。 |

#### 請求範例

```json
curl -k -u admin:admin \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -X POST 'https://localhost:5601/api/workspaces/_list' \
  -d '{}'
```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
  "success": true,
  "result": {
    "page": 1,
    "per_page": 20,
    "total": 1,
    "workspaces": [
      {
        "name": "test4",
        "description": "test4",
        "features": [
          "use-case-all"
        ],
        "lastUpdatedTime": "2025-09-10T14:47:04.741Z",
        "id": "B9Le1w",
        "permissionMode": "read"
      }
    ]
  }
}
```

## 取得工作區

您可以使用下列端點擷取單一工作區：

```json
GET {osd_host}:{port}/api/workspaces/{id}
```
{% include copy.html %}

下表列出可用的路徑參數。所有路徑參數皆為必要。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `<id>` | 字串 | 必要 | 識別要擷取的唯一工作區。 |

#### 請求範例

```json
curl -k -u admin:admin -X GET 'https://localhost:5601/api/workspaces/B9Le1w'
```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
  "success": true,
  "result": {
    "name": "test4",
    "description": "test4",
    "features": [
      "use-case-all"
    ],
    "lastUpdatedTime": "2025-09-10T14:47:04.741Z",
    "id": "B9Le1w"
  }
}
```

## 建立工作區

您可以使用下列端點建立工作區：

```json
POST {osd_host}:{port}/api/workspaces
```
{% include copy.html %}

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `attributes` | 物件 | 必要 | 定義工作區屬性。 |
| `attributes.id` | 字串 | 選用 | 工作區的 ID。 |
| `permissions` | 物件 | 選用 | 指定工作區的權限。 |
| `settings` | 物件 | 選用 | 指定工作區的設定。 |

#### 請求範例

```json
curl -k -XPOST "https://localhost:5601/api/workspaces" \
  -H "Content-Type: application/json" \
  -H "osd-xsrf: true" \
  -d '{
    "attributes": {
      "id": "my_workspace",
      "name": "test4",
      "description": "test4",
      "features": ["use-case-all"]
    }
  }' -u admin:admin
```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
    "success": true,
    "result": {
        "id": "B9Le1w"
    }
}
```

## 更新工作區

您可以使用下列端點更新工作區的屬性和權限：

```json
PUT {osd_host}:{port}/api/workspaces/{id}
```
{% include copy.html %}

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `<id>` | 字串 | 必要 | 識別要擷取的唯一工作區。 |
| `attributes` | 物件 | 必要 | 定義工作區屬性。 |
| `permissions` | 物件 | 選用 | 指定工作區的權限。 |

#### 不含權限物件的請求範例

```json
curl -k -XPUT "https://localhost:5601/api/workspaces/B9Le1w" \
  -H "Content-Type: application/json" \
  -H "osd-xsrf: true" \
  -d '{
    "attributes": {
      "name": "test5",
      "description": "Updated description"
    }
  }' -u admin:admin
```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
    "success": true,
    "result": true
}
```

#### 包含權限物件的請求範例

當請求包含 `permissions` 物件時，必須為每個使用者或群組指派所需存取層級要求的一組權限模式。例如，唯讀存取需要同時具備 `library_read` 和 `read` 權限模式：

```json
curl -k -u admin:admin \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -X PUT 'https://localhost:5601/api/workspaces/B9Le1w' \
  -d '{
    "attributes": {},
    "settings": {
      "permissions": {
        "library_write": { "users": ["obs-admin-user"] },
        "write": { "users": ["obs-admin-user"] },
        "library_read": { "groups": ["obs-read-users"] },
        "read": { "groups": ["obs-read-users"] }
      }
    }
  }'
```
{% include copy.html %}

如需權限模式及其提供之存取層級的完整清單，請參閱[定義工作區協作者]({{site.url}}{{site.baseurl}}/dashboards/workspace/workspace-acl/#defining-workspace-collaborators)。

## 刪除工作區

您可以使用下列端點刪除工作區：

```json
DELETE {osd_host}:{port}/api/workspaces/{id}
```
{% include copy.html %}

下表列出可用的路徑參數。所有路徑參數皆為必要。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `<id>` | 字串 | 必要 | 識別要擷取的唯一工作區。 |

#### 請求範例

```json
curl -k -u admin:admin \
  -H 'osd-xsrf: true' \
  -X DELETE 'https://localhost:5601/api/workspaces/B9Le1w'
```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
    "success": true,
    "result": true
}
```

## 複製已儲存物件

您可以使用下列端點在工作區之間複製已儲存物件：

```json
POST {osd_host}:{port}/api/workspaces/_duplicate_saved_objects
```
{% include copy.html %}

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `objects` | 陣列 | 必要 | 指定要複製的已儲存物件。 |
| `targetWorkspace` | 字串 | 必要 | 識別複製的目的地工作區。 |
| `includeReferencesDeep` | 布林值 | 選用 | 決定是否將所有參照的物件複製到目標工作區。預設為 `true`。 |

下表列出 `objects` 參數中物件的屬性。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `type` | 字串 | 必要 | 定義已儲存物件的分類，例如 `index-pattern`、`config` 或 `dashboard`。 |
| `id` | 字串 | 必要 | 已儲存物件的 ID。 |

#### 請求範例

```json
curl -k -u admin:admin \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -X POST 'https://localhost:5601/api/workspaces/_duplicate_saved_objects' \
  -d '{
    "objects": [
      { "type": "index-pattern", "id": "619cc200-ecd0-11ee-95b1-e7363f9e289d" }
    ],
    "targetWorkspace": "9gt4lB"
  }'
```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
    "successCount": 1,
    "success": true,
    "successResults": [
        {
            "type": "index-pattern",
            "id": "619cc200-ecd0-11ee-95b1-e7363f9e289d",
            "meta": {
                "title": "test*",
                "icon": "indexPatternApp"
            },
            "destinationId": "f4b724fd-9647-4bbf-bf59-610b43a62c75"
        }
    ]
}
```

## 關聯已儲存物件

您可以使用下列端點將已儲存物件與工作區建立關聯：

```json
POST {osd_host}:{port}/api/workspaces/_associate
```
{% include copy.html %}

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `workspaceId` | 字串 | 必要 | 識別物件關聯的目標工作區。 |
| `savedObjects` | 陣列 | 必要 | 指定要複製的已儲存物件清單。 |

下表列出 `savedObjects` 參數中物件的屬性。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `type` | 字串 | 必要 | 定義已儲存物件的分類，例如 `index-pattern`、`config` 或 `dashboard`。 |
| `id` | 字串 | 必要 | 已儲存物件的 ID。 |

#### 請求範例

```json
curl -k -u admin:admin \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -X POST 'https://localhost:5601/api/workspaces/_associate' \
  -d '{
    "savedObjects": [
      { "type": "index-pattern", "id": "619cc200-ecd0-11ee-95b1-e7363f9e289d" }
    ],
    "workspaceId": "9gt4lB"
  }'
```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
    "success": true,
    "result": [
        {
            "id": "619cc200-ecd0-11ee-95b1-e7363f9e289d",
        }
    ]
}
```

## 解除關聯已儲存物件

您可以使用下列端點解除已儲存物件與工作區的關聯：

```json
POST {osd_host}:{port}/api/workspaces/_dissociate
```
{% include copy.html %}

下表列出可用的路徑參數。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `workspaceId` | 字串 | 必要 | 要與物件建立關聯的目標工作區。 |
| `savedObjects` | 陣列 | 必要 | 要複製的已儲存物件清單。 |

下表列出 `savedObjects` 參數的屬性。

| 參數 | 資料類型 | 必要 | 說明 |
| :--- | :--- | :--- | :--- |
| `type` | 字串 | 必要 | 已儲存物件的類型，例如 `index-pattern`、`config` 或 `dashboard`。 |
| `id` | 字串 | 必要 | 已儲存物件的 ID。 |

#### 請求範例

```json
curl -k -u admin:admin \
  -H 'osd-xsrf: true' \
  -H 'Content-Type: application/json' \
  -X POST 'https://localhost:5601/api/workspaces/_dissociate' \
  -d '{
    "savedObjects": [
      { "type": "index-pattern", "id": "619cc200-ecd0-11ee-95b1-e7363f9e289d" }
    ],
    "workspaceId": "9gt4lB"
  }'

```
{% include copy.html %}

下列範例回應顯示成功的 API 呼叫：

```json
{
    "success": true,
    "result": [
        {
            "id": "619cc200-ecd0-11ee-95b1-e7363f9e289d",
        }
    ]
}
```
