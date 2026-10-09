---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作負載群組規則"
nav_order: 25
parent: Workload management
grand_parent: Availability and recovery
redirect_from:
  - /tuning-your-cluster/availability-and-recovery/workload-management/create-workload-group-rules-api/
---

# 工作負載群組規則

工作負載群組規則可讓您自動將工作負載群組 ID 指派給傳入的查詢。當查詢符合規則中指定的屬性時，OpenSearch 會以對應的工作負載群組 ID 標記該查詢。如此一來，用戶端便不必在每個請求中手動加入工作負載群組 ID。如需自動標記請求的詳細資訊，請參閱[以規則為基礎的自動標記]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/autotagging/)。

## 建立規則

若要為工作負載群組建立規則，請在 `workload_group` 參數中提供工作負載群組 ID。下列範例會建立一個規則，將指定的工作負載群組指派給同時符合 `index_pattern` 和 `principal.username` 屬性的請求：

```json
PUT _rules/workload_group
{
  "description": "description for rule",
  "index_pattern": ["test*"],
  "principal": {
    "username": ["admin"]
  },
  "workload_group": "wfbdJoDAS0mYiLbEAjd1sA"
}
```
{% include copy-curl.html %}

回應包含規則 ID：

```json
{
  "id": "176fd554-43e7-39eb-92cc-56615d287eae",
  "description": "description for rule",
  "index_pattern": ["test*"],
  "principal": {
    "username": ["admin"]
  },
  "workload_group": "wfbdJoDAS0mYiLbEAjd1sA",
  "updated_at": "2025-08-06T15:12:44.791Z"
}
```

## 屬性

`workload_group` 功能類型包含下列屬性。每個規則必須至少包含其中一個屬性。

下表依優先順序由高到低列出屬性。此優先順序已預先定義，使用者無法變更。當多個規則符合請求時，會套用包含最高優先順序屬性的規則。

| 屬性            | 資料類型 | 說明                                                                                                                                                                                                                   |
|:---------------------|:----------|:------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `principal.username` | 清單      | 要與此規則比對的使用者名稱清單。支援完全相符（例如，`user1`）及尾端萬用字元模式（例如，`user*`）。只有在網域上啟用 Security 外掛程式時，才能使用此屬性。                                 |
| `principal.role`     | 清單      | 要與此規則比對的角色清單。支援完全相符（例如，`role1`）及尾端萬用字元模式（例如，`role*`）。只有在網域上啟用 Security 外掛程式時，才能使用此屬性。                                     |
| `index_pattern`      | 清單      | 傳入查詢的目標索引清單。支援完全相符（例如，`logs-2025`）及尾端萬用字元模式（例如，`logs*`）。                                |

## 參數

`workload_group` 功能類型包含下列參數。

| 參數        | 資料類型 | 說明                                                                                             |
|:-----------------|:----------|:--------------------------------------------------------------------------------------------------------|
| attribute        | 物件    | 規則必須至少包含一個屬性（`index_pattern`、`principal.username` 或 `principal.role`）。 |
| `description`    | 字串    | 規則的說明。                                                                              |
| `workload_group` | 字串    | 要套用至符合此規則之請求的工作負載群組 ID。                                      |

## 規則比對與優先順序

單一請求可能符合多個規則。OpenSearch 會將每個規則與請求進行比對，再使用優先順序邏輯決定要指派哪個工作負載群組。 
如果沒有符合的規則，請求會在未指派工作負載群組的情況下執行。

### 單一規則內的比對

只有當規則中的每個屬性都符合時，該規則才會符合請求，因此同一規則中的多個屬性會形成邏輯 `AND`。在單一屬性內，列出的值會形成邏輯 `OR`：只要請求符合其中任一個值，該屬性就會符合。例如，包含 `"principal": { "role": ["role1", "role2"] }` 的規則會符合使用者具有 `role1` 或 `role2` 的請求。

若要僅在請求包含特定值組合時才符合請求（單一屬性內的邏輯 `AND`），請為每個必要值建立個別規則。在同一屬性下列出多個值時，一律會套用 `OR` 語意。
{: .note}

由於 `principal.username` 和 `principal.role` 是單一 `principal` 屬性的子欄位，因此其所有值都會使用 `OR`（而非 `AND`）合併。下列範例顯示同時具有 `principal` 和 `index_pattern` 屬性的規則：

```json
{
  "principal": {
    "username": ["user1", "user2"],
    "role": ["role1", "role2", "role3"]
  },
  "index_pattern": ["index-1", "index-2", "logs-*"],
  "workload_group": "<id>"
}
```

此規則會符合包含至少一個 `principal` 值（使用者名稱或角色）及至少一個 `index_pattern` 值的請求：

```
(user1 OR user2 OR role1 OR role2 OR role3) AND (index-1 OR index-2 OR logs-*)
```

### 在多個符合的規則之間選擇

當請求符合多個規則，而這些規則對應至不同的工作負載群組時，OpenSearch 會依下列順序選取單一群組：

1. **屬性優先順序**：優先選擇透過最高優先順序屬性比對成功的工作負載群組。優先順序固定不變，並依照[屬性](#attributes)表中所示的順序（先 `principal.username`，再 `principal.role`，最後是 `index_pattern`）。
1. **比對分數**：如果仍無法明確選擇，OpenSearch 會比較比對分數。完全相符的分數高於較短的前綴（萬用字元）相符，而符合請求中更多值的工作負載群組會獲得較高的累計分數。例如，如果請求包含三個角色，且一個群組的規則符合全部三個角色，另一個群組的規則只符合兩個角色，則會選取符合三個角色的群組。
1. **無法判定平手時不指派**：如果比較所有屬性後，仍有兩個以上的工作負載群組平手（例如，兩個規則各自透過單一且具體程度相同的角色符合請求），OpenSearch 就不會指派任何工作負載群組。請求會在未指派工作負載群組的情況下執行，而不是任意選擇一個群組。

## 更新規則

若要更新規則，請在路徑參數中提供其 ID，並在請求本文中提供更新後的欄位。更新規則時，只會變更您指定的參數；其餘參數皆維持不變。下列請求會更新 ID 為 `176fd554-43e7-39eb-92cc-56615d287eae` 之規則的說明與索引模式：

```json
PUT _rules/workload_group/176fd554-43e7-39eb-92cc-56615d287eae
{
  "description": "updated description for rule",
  "index_pattern": ["log*", "event*"]
}
```
{% include copy-curl.html %}

回應顯示更新後的欄位：

```json
{
  "id": "176fd554-43e7-39eb-92cc-56615d287eae",
  "description": "updated description for rule",
  "index_pattern": [
    "log*",
    "event*"
  ],
  "workload_group": "wfbdJoDAS0mYiLbEAjd1sA",
  "updated_at": "2025-08-06T15:14:09.935879339Z"
}
```

## 擷取規則

您可以依規則 ID 或屬性篩選條件擷取規則。您可以分頁瀏覽傳回的規則清單。

下列請求會擷取 `workload_group` 功能類型的所有規則：

```json
GET /_rules/workload_group
```
{% include copy-curl.html %}

下列請求會依 ID 擷取 `workload_group` 功能類型的規則：

```json
GET /_rules/workload_group/{rule_id}
```
{% include copy-curl.html %}

下列請求會擷取符合指定 `index_pattern` 和 `principal.username` 的所有 `workload_group` 規則：

```json
GET /_rules/workload_group?index_pattern=log*,event*&principal.username=admin
```
{% include copy-curl.html %}

如果回應包含的結果超過單一頁面可容納的數量，OpenSearch 會將結果分頁，並在回應中包含 `search_after` 值：

```json
{
  "rules": [
    {
      "id": "z1MJApUB0zgMcDmz-UQq",
      "description": "Rule for tagging workload_group_id to index123",
      "index_pattern": ["index123"],
      "workload_group": "workload_group_id",
      "updated_at": "2025-02-14T01:19:22.589Z"
    },
    ...
  ],
  "search_after": ["z1MJApUB0zgMcDmz-UQq"]
}
```

若要擷取下一頁，請使用相同的篩選條件，向同一端點傳送另一個請求，並將前一個回應中的 `search_after` 值納入查詢參數。

下列請求會提供同一工作負載群組的下一頁規則：

```json
GET /_rules/workload_group?index_pattern=log*,event*&search_after=z1MJApUB0zgMcDmz-UQq
```
{% include copy-curl.html %}

## 刪除規則

若要刪除規則，請提供規則的 ID：

```json
DELETE /_rules/workload_group/{rule_id}
```
{% include copy-curl.html %}

