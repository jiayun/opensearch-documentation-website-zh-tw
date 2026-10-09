---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換類型對應"
nav_order: 1
parent: Migrate metadata
grand_parent: Migration workflows
permalink: /migration-assistant/migration-phases/migrate-metadata/handling-type-mapping-deprecation/
redirect_from:
  - /migration-assistant/migration-phases/assessment/handling-type-mapping-deprecation/
  - /migration-assistant/migration-phases/planning-your-migration/handling-type-mapping-deprecation/
---

# 轉換類型對應

較舊的 Elasticsearch 資料集可能每個索引包含多個對應類型，如下列範例所示：

```json
{
  "mappings": {
    "book": {
      "properties": {
        "title": { "type": "text" }
      }
    },
    "movie": {
      "properties": {
        "title": { "type": "text" }
      }
    }
  }
}
```

現代 OpenSearch 不支援此結構。如果您的快照包含多類型定義，`metadataMigrationConfig.multiTypeBehavior` 參數會控制 Migration Assistant 如何處理它們。下表說明有效的值。

| 選項 | 行為 | 使用時機 |
|:-------|:---------|:---------|
| `NONE` | 遇到多類型對應時，讓遷移失敗。 | 您想要在繼續之前明確處理多類型問題。 |
| `UNION` | 將所有類型合併成單一目標索引中的一個對應。 | 這些類型足夠相容，可以在一個合併的對應下共存。 |
| `SPLIT` | 將每個類型路由到個別的目標索引。 | 不同類型應該成為不同的索引，或合併它們會產生欄位衝突。 |

## 設定多類型行為

在工作流程組態中將 `multiTypeBehavior` 設為適當的值，然後執行試驗性遷移，並在遷移完整資料集之前驗證產生的目標對應和索引配置。若要編輯工作流程組態，請執行下列命令：

```bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

## 自訂類型轉換器

如果內建的 `multiTypeBehavior` 選項不夠用，您可以透過中繼資料遷移設定提供自訂轉換器組態。

那是一條專家的路徑。請在下列情況使用它：

- 目標索引命名必須遵循特定模式。
- 只有選取的類型應該遷移。
- 您需要與內建工作流程選項不同的路由邏輯。

## 驗證結果

在試驗性中繼資料執行之後，請驗證下列項目：

- 產生的目標索引名稱
- 合併所引入的欄位衝突
- 別名和範本行為
- 假設特定索引配置的應用程式查詢。

如果此轉換變更了索引名稱或欄位語意，您的用戶端組態可能也需要變更。
