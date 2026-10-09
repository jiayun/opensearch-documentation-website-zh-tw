---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "規則式自動標記"
nav_order: 80
parent: Availability and recovery
has_children: true
---

# 規則式自動標記

規則式自動標記會自動將功能專屬的值指派給傳入的請求，並透過比對請求屬性，依據一組預先定義的規則評估這些請求。
例如，工作負載管理功能會使用索引模式作為屬性，並指派工作負載群組 ID。

規則式自動標記提供下列優點：

* 彈性的屬性比對
* 支援功能專屬的比對邏輯
* 一致的政策套用
* 自動化的請求分類
* 降低管理負擔
* 集中化的規則管理
* 輕鬆更新政策

規則式自動標記提供彈性的架構，可實作功能專屬的請求處理。雖然本主題以工作負載管理為例，但以屬性為基礎的比對系統可調整用於其他 OpenSearch 功能與使用案例。
{: .tip }

## 重要概念

在檢閱規則組態與行為之前，請務必先了解規則式自動標記的下列重要元件：

* **規則**：定義比對條件 (屬性) 以及要指派的值。
* **屬性**：用於比對規則的索引鍵-值配對 (例如索引模式、使用者名稱、使用者角色或請求類型)。
* **功能專屬的值**：規則相符時所指派的值。
* **模式比對**：屬性值的比對行為 (完全相符或以模式為基礎)。

## 規則結構與管理

妥善的規則結構與管理對於有效的自動標記至關重要。本節說明規則結構描述以及如何管理規則。

### 規則結構描述

下列規則結構描述包含比對屬性與功能專屬的值：

```json
{
  "_id": "fwehf8302582mglfio349==",  
  "index_pattern": ["logs-prod-*"],
  "principal": {
    "username": ["admin"],
    "role": ["all_access"]
  },
  "other_attribute": ["value1", "value2"],
  "workload_group": "production_workload_id",
  "updated_at": 1683256789000
}
```

### 管理規則

使用 [Rules API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/rule-lifecycle-api/) 來管理規則。

## 屬性比對

屬性比對系統會決定哪些規則適用於指定的請求。每種屬性類型可依據下列屬性類型支援不同的比對行為：

1. **完全相符**：屬性值必須完全相符。
2. **模式比對**：支援萬用字元 (例如索引模式)。
3. **清單比對**：比對清單中的任何項目。
4. **範圍比對**：比對定義範圍內的值。

例如，在工作負載管理中，索引模式支援：

* 完全相符：`logs-2025-04`
* 前置字元模式：`logs-2025-*`

請注意，比對行為取決於功能與屬性類型。

### 規則優先順序

當多個規則符合某個請求時，OpenSearch 會使用下列優先順序規則：

1. 屬性比對較為明確的規則會優先處理。
2. 套用功能專屬的決勝邏輯。

例如，以索引模式來說：

* `logs-prod-2025-*` 優先於 `logs-prod-*`。
* `logs-prod-*` 優先於 `logs-*`。

### 評估流程

OpenSearch 會使用下列流程評估傳入的請求：

1. OpenSearch 收到請求。
2. 系統會依據定義的規則評估請求屬性。
3. 指派最明確的相符規則的值。
4. 如果沒有規則相符，則不指派任何值。

如果在套用所有決勝邏輯後，仍有兩個或多個規則並列，也就是它們的相符程度同樣明確且產生相同的相符分數，則不指派任何值。OpenSearch 不會任意在並列的規則之間做選擇。
{: .note}

### 規則比對範例

下列範例示範 OpenSearch 如何比對屬性以及解決規則之間的並列情況。

在這些範例中，`username` 屬性的優先順序高於 `index_pattern` 屬性 (優先順序取決於功能與功能類型)。

1. **範例 1**
   某個請求符合三個規則：

   * 規則 1：`index_pattern = log*`
   * 規則 2：`username = admin`
   * 規則 3：`index_pattern = log123*`

   **結果**：套用規則 2，因為 `username` 屬性的優先順序較高。

2. **範例 2**
   某個請求符合兩個規則：

   * 規則 1：`index_pattern = logs-prod-*`
   * 規則 2：`index_pattern = logs-*`

   **結果**：套用規則 1，因為 `logs-prod-*` 比 `logs-*` 更明確。

3. **範例 3**
   某個請求符合兩個規則：

   * 規則 1：`index_pattern = log*` 與 `username = admin`
   * 規則 2：`username = admin`

   **結果**：套用規則 1，因為它同時包含 `index_pattern` 與 `username` 屬性，使其成為更明確的相符項。

## 工作負載管理範例

這些範例示範規則式自動標記在工作負載管理中的運作方式，該功能使用索引模式作為其主要屬性。

### 多屬性比對

```json
{
  "index_pattern": ["logs-prod-*"],
  "request_type": ["search", "count"],
  "workload_group": "production_search_workload_id"
}

{
  "index_pattern": ["logs-prod-*"],
  "workload_group": "production_workload_id"
}
```

### 屬性明確性

```json
{
  "index_pattern": ["logs-*"],
  "workload_group": "general_workload_id"
}

{
  "index_pattern": ["logs-prod-service-*"],
  "workload_group": "prod_service_workload_id"
}
```

## 最佳實務

設計與操作規則式自動標記時，請遵循下列最佳實務。

### 設計規則

建立規則時，請專注於建構合乎邏輯且明確的組態，以支援您的工作負載與存取模式。請考量下列準則：

* 找出最符合您使用案例的屬性。
* 使用明確的屬性值以進行精確控制。
* 在適當情況下合併多個屬性。
* 使用一致的命名慣例。
* 記錄屬性比對行為。

### 管理屬性

屬性的選擇與組態會大幅影響規則的成效。若要成功管理屬性，請執行下列動作：

* 了解每個屬性的比對行為。
* 從所需的最明確條件開始。
* 除非刻意為之，否則避免規則重疊。
* 為未來的屬性值模式做好規劃。

### 作業

持續的作業與監控有助於長期維持規則品質。請使用下列最佳實務，確保您的功能規則可靠且有效：

* 在開發環境中測試新規則。
* 在系統記錄檔中監控規則相符情況。
* 記錄規則組態。
* 定期檢閱規則成效。
* 移除未使用的規則。

## 疑難排解

建立規則時，可能發生下列問題：

* **未指派任何值**：此問題通常發生在請求屬性不符合任何現有規則時。  
  例如，假設 `index_pattern` 是有效的允許屬性。如果對 `logs_q1_2025` 發出搜尋請求，但該值沒有任何規則存在，則該請求不會符合任何規則，因而導致缺少指派。

* **非預期的值**：當定義了多個具有重疊或衝突條件的規則時，就可能發生此情況。  
  例如，請考量下列規則：
  1. `{ principal: {"username": ["dev*"]}, "index_pattern": ["logs*"] }`
  2. `{ "index_pattern": ["logs*", "events*"] }`

  如果使用者名稱 `dev_john` 的使用者對 `logs_q1_25` 傳送搜尋請求，該請求會依據 `username` 與 `index_pattern` 屬性符合第一個規則。即使 `index_pattern` 也符合資格，該請求仍不會符合第二個規則。

您可以使用下列其中一種技術驗證組態，以解決這兩個問題：

- **使用範例請求測試規則**：首先，使用 REST API 建立規則，然後傳送符合該規則屬性的請求。例如，對於具有 `"index_pattern": ["logs*", "events*"]` 的規則，您可以對 `logs` 或 `events` 索引傳送請求。然後查詢 [Workload Management Stats API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/workload-management/wlm-feature-overview/#workload-management-stats-api) 來驗證工作負載管理統計資料。

- **使用 [Get Rule API]({{site.url}}{{site.baseurl}}/tuning-your-cluster/availability-and-recovery/rule-based-autotagging/rule-lifecycle-api/#get-a-rule)** 來確認規則定義。
