---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "遷移中繼資料"
nav_order: 50
parent: Migration workflows
has_children: true
has_toc: true
permalink: /migration-assistant/migration-phases/migrate-metadata/
redirect_from:
  - /migration-assistant/migration-phases/migrating-metadata/
  - /migration-phases/migrating-metadata/
  - /migration-assistant/deploying-migration-assistant/getting-started-data-migration/
---

# 遷移中繼資料

中繼資料遷移會將目標叢集調整為能夠接收即將到來的資料與流量的形態。它會在文件回填或重播變得有意義之前，處理對應、範本、別名以及其他索引層級的定義。

在工作流程模型中，中繼資料遷移是遷移工作流程內一個已設定的階段。

## 中繼資料工作流程步驟

當 `metadataMigrationConfig` 存在時，工作流程會執行兩個邏輯步驟：

1. `evaluateMetadata`
2. `migrateMetadata`

第一個步驟評估將套用哪些內容。第二個步驟將這些變更寫入目標。如果已啟用核准機制，工作流程可以在這兩個步驟之間暫停，讓您在繼續之前檢查結果。

## 中繼資料遷移範圍

中繼資料遷移可以處理：

- 索引設定
- 索引對應
- 舊式與可組合範本
- 元件範本
- 別名

它不會自動遷移叢集周邊的所有內容。請為安全性組態、ISM 或 ILM 政策、資料匯入管線、儀表板或 Kibana 物件，以及其他環境專屬資產規劃個別的工作。

## 內建轉換

目前的中繼資料遷移路徑已包含針對數個常見相容性問題的內建轉換，包括：

- `string` 轉換為 `text` 與 `keyword`
- `flattened` 轉換為 `flat_object`
- `dense_vector` 轉換為 `knn_vector`
- 針對較新的 OpenSearch 與 Serverless NextGen 目標的額外向量相容性轉換。

如果您的遷移需求超出內建功能，您也可以透過 `transformerConfig`、`transformerConfigBase64` 或 `transformerConfigFile` 提供自訂中繼資料轉換器。

## 重要的組態欄位

實用的中繼資料設定包括：

- `indexAllowlist`
- `indexTemplateAllowlist`
- `componentTemplateAllowlist`
- `multiTypeBehavior`
- `allowLooseVersionMatching`
- `transformerConfig*`

請使用主控台中與版本相符的範例，查看您所安裝版本的確切結構。(*Version-matched* (版本相符) 表示結構描述對應於您主控台 pod 中安裝的 Migration Assistant 版本——`workflow configure sample --load` 會從該 pod 上的 `/root/.workflowUser.schema.json` 讀取結構描述，因此載入的範例一律包含該版本支援的欄位。) 若要載入並編輯範例，請執行下列命令：

```bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

## 索引篩選行為

中繼資料 `indexAllowlist` 是在快照已經建立之後才會評估。它支援：

- 精確的索引名稱
- 以 `regex:` 為前置詞的 Regex 模式

這與快照建立的允許清單不同，後者使用來源叢集自身的快照多索引運算式語法。

## 多類型行為

如果您的遷移涉及具有多類型對應的較舊 Elasticsearch 資料集，請審慎設定 `multiTypeBehavior`：

- `NONE` 在遇到多類型資料時失敗
- `UNION` 將類型合併為一個對應
- `SPLIT` 將類型路由至個別的索引。

請勿在此任意猜測。如果多類型行為對您的應用程式很重要，請先在一小部分資料上進行試驗。

## 繼續之前驗證中繼資料

中繼資料遷移執行完畢後，請在進入完整回填或切換之前驗證目標：

```bash
console clusters curl target /_cat/indices?v
console clusters curl target /_cat/templates?v
console clusters curl target /_cat/aliases?v
console clusters curl target /my-index/_mapping
```
{% include copy.html %}

## 監控與疑難排解

請盡可能使用工作流程工具，而非原始的 pod 路徑：

```bash
workflow manage
workflow status
workflow log all
```
{% include copy.html %}

如果中繼資料遷移失敗，常見原因如下：

- 不相容的對應或設定
- 缺少轉換
- 目標端不支援的功能
- 目標端的驗證或連線問題。

{% include migration-phase-navigation.html %}
