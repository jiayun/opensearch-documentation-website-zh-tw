---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換欄位類型"
nav_order: 2
parent: Migrate metadata
grand_parent: Migration workflows
permalink: /migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/
redirect_from:
  - /migration-assistant/migration-phases/assessment/handling-field-type-breaking-changes/
  - /migration-assistant/migration-phases/planning-your-migration/handling-field-type-breaking-changes/
---

# 轉換欄位類型

Migration Assistant 會在中繼資料遷移期間自動解決數種常見的欄位類型相容性問題。下列章節說明內建轉換何時已足夠，以及何時需要自訂轉換器。

## 內建轉換

在建立自訂邏輯之前，請先確認遷移是否已由內建的中繼資料轉換涵蓋：

- `string` 至 `text` 與 `keyword`
- `flattened` 至 `flat_object`
- `dense_vector` 至 `knn_vector`
- 針對較新的 OpenSearch 與 Serverless NextGen 目標的額外向量相容性調整。

## 自訂欄位類型轉換器

只有在下列情況才使用自訂轉換器：

- 內建規則不符合您的目標行為。
- 您的應用程式需要特定的欄位重寫。
- 您需要以預設值未涵蓋的方式移除或調整對應屬性。

自訂中繼資料轉換可透過下列中繼資料遷移設定進行設定：

- `transformerConfig`
- `transformerConfigBase64`
- `transformerConfigFile`

若要設定自訂轉換器，請載入範例組態並編輯工作流程：

```bash
workflow configure sample --load
workflow configure edit
```
{% include copy.html %}

設定 `transformerConfigFile` 需要額外的設定，適用於進階使用情境：該檔案必須可供 Migration Console 容器存取。您可以將它掛載為 Kubernetes 磁碟區，或將它包含在自訂容器映像中。

### JavaScript 型轉換器

您可以透過 `JsonJSTransformerProvider` 提供 JavaScript 型的中繼資料轉換器。常見的使用情境包括：

- 取代已淘汰的欄位類型
- 移除不相容的對應屬性
- 在欄位定義抵達目標之前予以正規化。

### 範例組態

下列範例顯示參照 JavaScript 檔案的轉換器描述項：

```json
[
  {
    "JsonJSTransformerProvider": {
      "initializationScriptFile": "/shared-logs-output/field-type-converter.js",
      "bindingsObject": "{}"
    }
  }
]
```
{% include copy.html %}

## 建議的順序

只有在確認內建轉換無法涵蓋您的需求之後，才使用自訂轉換器。請遵循以下順序：

1. 執行評估。
2. 檢視內建轉換頁面。
3. 設定試驗工作流程。
4. 只有在試驗工作流程的結果需要時，才新增自訂轉換器。

## 驗證轉換後的中繼資料

在中繼資料階段執行完畢後，請驗證目標對應：

```bash
console clusters curl target /my-index/_mapping
workflow show
```
{% include copy.html %}

如果自訂轉換器變更了欄位名稱或語意，請在進行完整回填或切換之前，先驗證應用程式查詢。
