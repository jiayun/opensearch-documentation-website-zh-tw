---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: Rules API
nav_order: 20
parent: Rule-based auto-tagging
grand_parent: Availability and recovery
---

# Rules API

Rules API 可讓您建立、更新、擷取及刪除規則。每條規則都與特定的功能類型相關聯，並包含一個功能值以及至少一個屬性。
這些規則旨在根據指定的屬性，自動為傳入的查詢指派功能值，協助自動分類及管理查詢。

## 端點

下列章節說明可用於管理不同功能類型之規則的 API 端點。

### 建立規則

使用下列端點為特定功能類型新增規則：

```json
PUT /_rules/{feature_type}
POST /_rules/{feature_type}
```

### 更新規則

使用下列端點，在路徑參數中同時指定功能類型與規則 ID，以修改現有規則：

```json
PUT /_rules/{feature_type}/{id}
POST /_rules/{feature_type}/{id}
```

### 取得規則

使用下列端點，依 ID 擷取特定規則，或列出某功能類型的所有規則：

```json
GET /_rules/{feature_type}/{id}
GET /_rules/{feature_type}
```

### 刪除規則

使用下列端點，同時指定功能類型與規則 ID 來移除規則：

```json
DELETE /_rules/{feature_type}/{id}
```

## 路徑參數

下表列出可用的路徑參數。

| 參數      | 資料類型 | 說明  |
|:---------------| :--- | :--- |
| `feature_type` | 字串    | 規則的類別，定義功能類型，例如 `workload_group`。 |
| `id`           | 字串    | 規則的唯一識別碼。`UPDATE`、`GET` 與 `DELETE` 作業需要此參數。 |

## 查詢參數

下表列出可用的查詢參數。

| 參數 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `search_after` | 字串 | 用於分頁時擷取下一頁結果的權杖。 |
| `<attribute_key>` | 字串 | 篩選結果，只保留 `<attribute_key>` 符合其中一個指定值的規則。 |

## 請求本文欄位

下表列出請求本文中可用的欄位。

| 欄位 | 資料類型 | 說明 |
| :--- | :--- | :--- |
| `description` | 字串 | 規則的易讀說明或用途。 |
| `<attribute_key>` | 陣列 | 必須與查詢相符的屬性值清單，規則才會套用。 |
| `<feature_type>` | 字串 | 規則相符時所指派的功能值。 |


## 範例請求

下列範例示範如何使用 Rules API 建立規則。

### 建立規則

下列請求會建立一條規則，根據相符的 `index_pattern` 與主體屬性指派 `workload_group` 值：

```json
PUT _rules/workload_group
{
  "description": "description for rule",
  "index_pattern": ["log*", "event*"],
  "principal": {
    "username": ["admin"],
    "role": ["all_access"]
  },
  "workload_group": "EITBzjFkQ6CA-semNWGtRQ"
}
```
{% include copy-curl.html %}

### 更新規則

下列請求會更新 ID 為 `0A6RULxkQ9yLqn4r8LPrIg` 的規則：

```json
PUT _rules/workload_group/0A6RULxkQ9yLqn4r8LPrIg
{
  "description": "updated_description for rule",
  "index_pattern": ["log*"],
  "principal": {
    "username": ["admin"],
    "role": ["all_access"]
  },
  "workload_group": "EITBzjFkQ6CA-semNWGtRQ"
}
```
{% include copy-curl.html %}

您無法變更 `feature_type`。未更新的欄位可以省略。
{: .note }

### 擷取規則

下列請求會依 ID 擷取規則：

```json
GET /_rules/{feature_type}/{id}
```
{% include copy-curl.html %}

下列請求會擷取某功能類型的所有規則：

```json
GET /_rules/{feature_type}
```
{% include copy-curl.html %}

下列請求會傳回 `workload_group` 功能類型中，包含值為 `a` 或 `b` 的 `index_pattern` 屬性，且 `principal.username` 設為 `admin` 的所有規則：

```json
GET /_rules/workload_group?index_pattern=a,b&principal.username=admin
```
{% include copy-curl.html %}

如果 `GET` 請求傳回的結果超過單一回應可容納的數量，系統會將結果分頁，並在回應中包含 `search_after` 欄位。  
若要擷取下一頁，請使用相同的篩選條件向同一端點傳送另一個請求，並將上一個回應中的 `search_after` 值作為查詢參數一併傳入。

下列範例接續搜尋 `workload_group` 功能類型中 `index_pattern` 屬性包含 `a` 或 `b` 值的所有規則：

```json
GET /_rules/workload_group?index_pattern=a,b&search_after=z1MJApUB0zgMcDmz-UQq
```
{% include copy-curl.html %}

## 範例回應

<details open markdown="block">
<summary>
    回應：建立或更新規則 
</summary>
{: .text-delta }

```json
{
  "id": "wi6VApYBoX5wstmtU_8l",
  "description": "description for rule",
  "index_pattern": ["log*", "event*"],
  "principal": {
    "username": ["admin"],
    "role": ["all_access"]
  },
  "workload_group": "EITBzjFkQ6CA-semNWGtRQ",
  "updated_at": "2025-04-04T20:54:22.406Z"
}
```

</details>


<details markdown="block">
<summary>
    回應：取得規則 
</summary>
{: .text-delta }

```json
{
  "rules": [
    {
      "id": "z1MJApUB0zgMcDmz-UQq",
      "description": "Rule for tagging workload_group_id to index123",
      "index_pattern": ["index123"],
      "principal": {
        "username": ["admin"],
        "role": ["all_access"]
      },
      "workload_group": "workload_group_id",
      "updated_at": "2025-02-14T01:19:22.589Z"
    },
    ...
  ],
  "search_after": ["z1MJApUB0zgMcDmz-UQq"]
}
```

如果回應中有 `search_after` 欄位，表示還有更多結果。  
若要擷取下一頁，請在下一個 `GET` 請求中將 `search_after` 值作為查詢參數傳入，例如 `GET /_rules/{feature_type}?search_after=z1MJApUB0zgMcDmz-UQq`。

</details>


## 回應本文欄位

| 欄位             | 資料類型 | 說明 |
|:------------------| :--- | :--- |
| `id`              | 字串 | 規則的唯一識別碼。 |
| `description`     | 字串 | 規則的說明或用途。 |
| `updated_at`      | 字串 | 規則最近一次更新的時間戳記，採 UTC 格式。 |
| `<attribute_key>` | 陣列 | 用於比對傳入查詢的屬性值。 |
| `<feature_type>`  | 字串 | 規則相符時指派給功能類型的值。 |
| `search_after`    | 陣列 | 用於分頁更多結果的權杖。只有在還有更多結果時才會出現。 |
