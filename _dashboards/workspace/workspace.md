---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "工作區"
nav_order: 120
has_children: true
---

# 工作區
**於 2.18 版推出**
{: .label .label-purple }

工作區可讓您透過特定使用案例的組態來調整您的環境。例如，您可以為可觀測性情境建立專用的工作區，讓您專注於相關功能。此外，您可以在具有隔離儲存空間的工作區中整理視覺資產，例如儀表板和視覺化。

## 工作區資料模型

工作區資料模型由以下結構定義：

```typescript
interface Workspace {
  id: string;
  name: string;
  description?: string;
  features?: string[];
  color: string;
  uiSettings: Record<string, unknown>;
}
```
{% include copy.html %}

工作區資料模型由以下主要屬性組成：

- `id`：字串類型；每個工作區的唯一 ID。
- `name`：字串類型；指定工作區的名稱。
- `description`：選用的字串類型；提供工作區的背景資訊。
- `features`：選用的字串陣列；包含與工作區連結的使用案例 ID。

---

#### 工作區物件範例

以下物件顯示典型的工作區組態：

```typescript
{
  id: "M5NqCu",
  name: "Analytics team",
  description: "Analytics team workspace",
  features: ["use-case-analytics"],
}
```
{% include copy.html %}

此組態使用 `use-case-observability` 功能集建立 `Analytics team`。使用案例會對應至特定的功能群組，將每個工作區中的功能限制在所定義的功能集內。

以下為預先定義的使用案例選項：

- `use-case-observability`
- `use-case-security-analytics`
- `use-case-search`
- `use-case-essentials`
- `use-case-all`

---

## 將已儲存物件與工作區建立關聯

OpenSearch Dashboards 中的已儲存物件（例如儀表板、視覺化和索引模式）可以與特定工作區建立關聯，隨著物件數量增加，能提升組織性與可存取性。

`workspaces` 屬性是一個字串陣列，會新增至已儲存物件，以將其與一個或多個工作區連結。因此，儀表板和視覺化等已儲存物件只能在其指定的工作區中存取。

以下已儲存物件顯示與工作區 `M5NqCu` 建立關聯的儀表板物件：

```typescript
{
  type: "dashboard",
  id: "da123f20-6680-11ee-93fa-df944ec23359",
  workspaces: ["M5NqCu"]
}
```
{% include copy.html %}

已儲存物件支援與多個工作區建立關聯，有助於跨團隊協作與資源共用。當某個物件與多個團隊、專案或使用案例相關時，此功能非常實用。

以下範例顯示連結至多個工作區的資料來源物件：

```typescript
{
  type: "data-source",
  id: "da123f20-6680-11ee-93fa-df944ec23359",
  workspaces: ["M5NqCu", "<TeamA-workspace-id>", "<Analytics-workspace-id>"]
}
```
{% include copy.html %}

## 非工作區已儲存物件

並非 OpenSearch Dashboards 中的所有已儲存物件都與工作區相關聯。有些物件獨立於工作區架構之外運作。這些物件沒有 `workspace` 屬性，並提供全系統的功能。例如，全域使用者介面設定物件會管理影響整個 OpenSearch Dashboards 介面的組態，以便在所有工作區中維持一致的功能。

這種雙重方式讓 OpenSearch Dashboards 能在細緻、因應情境的自訂與整體系統一致性之間取得平衡。

## 啟用工作區

在您的 `opensearch_dashboards.yml` 檔案中，設定以下選項：

```yaml
workspace.enabled: true
uiSettings:
  overrides:
    "home:useNewHomePage": true
```
{% include copy.html %}

如果您的叢集已安裝 Security 外掛程式，則必須停用多租用戶功能，以避免與類似的工作區發生衝突：

```yaml
opensearch_security.multitenancy.enabled: false
```
{% include copy.html %}

更新組態檔案後，請重新啟動 OpenSearch Dashboards 以使變更生效。
