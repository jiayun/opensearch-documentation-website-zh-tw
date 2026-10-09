---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 flattened 欄位轉換為 flat_object"
nav_order: 3
parent: Migrate metadata
grand_parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/migrate-metadata/transform-flattened-flat-object/
---

# 將 flattened 欄位轉換為 flat_object

本指南說明 Migration Assistant 在遷移至 OpenSearch 期間如何自動轉換 `flattened` 欄位類型。

## 概觀

`flattened` 欄位類型是在 Elasticsearch 7.3 中以 X-Pack 功能的形式推出。它可讓您將整個 JSON 物件儲存為單一欄位值，這對於具有大量或未知數量唯一鍵的物件很有用。

遷移至 OpenSearch 2.7 或更新版本時，Migration Assistant 會自動將 `flattened` 欄位類型轉換為 OpenSearch 的對等類型 `flat_object`。此轉換不需要任何組態或使用者介入。

若要判斷 Elasticsearch 叢集是否使用 `flattened` 欄位類型，請呼叫來源叢集的 `GET /_mapping` API。在 Migration Console 中，執行 `console clusters curl source_cluster "/_mapping"`。如果您看到 `"type":"flattened"`，表示此轉換適用，且這些欄位將在遷移期間自動轉換。

## 相容性

`flattened` 至 `flat_object` 欄位類型轉換適用於：
- **來源叢集**：Elasticsearch 7.3+
- **目標叢集**：OpenSearch 2.7+
- **自動轉換**：中繼資料期間不需要任何組態

## 自動遷移

遷移至 OpenSearch 2.7 或更新版本時，Migration Assistant 會自動偵測 `flattened` 欄位類型，並將其轉換為 `flat_object` 欄位。在遷移過程中，您會在輸出中看到此轉換：

```
Transformations:
   flattened to flat_object:
      Convert field data type flattened to OpenSearch flat_object
```

### 轉換範例

<table style="border-collapse: collapse; border: 1px solid #ddd;">
  <thead>
    <tr>
      <th style="border: 1px solid #ddd; padding: 8px;">來源欄位類型</th>
      <th style="border: 1px solid #ddd; padding: 8px;">目標欄位類型</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <pre><code>{
  "properties": {
    "labels": {
      "type": "flattened"
    },
    "title": {
      "type": "text"
    }
  }
}</code></pre>
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <pre><code>{
  "properties": {
    "labels": {
      "type": "flat_object"
    },
    "title": {
      "type": "text"
    }
  }
}</code></pre>
      </td>
    </tr>
  </tbody>
</table>

## 各版本的轉換行為

Migration Assistant 會自動將所有 `flattened` 欄位轉換為 `flat_object` 欄位。不需要任何額外的組態。

如果您要遷移至早於 2.7 的 OpenSearch 版本，包含 `flattened` 欄位類型的索引將無法遷移。您有幾個選項：

1. **升級目標叢集**：將您的目標 OpenSearch 叢集升級至 2.7 或更新版本，以支援自動轉換。

2. **自訂轉換**：使用[欄位類型轉換架構]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/)將 `flattened` 轉換為其他支援的類型（例如 `object` 或 `nested`）。

## flattened 與 flat_object 的差異

雖然 OpenSearch 中的 `flat_object` 提供與 Elasticsearch 的 `flattened` 類型類似的功能，但仍有若干細微差異：

- **查詢語法**：兩者都支援使用點標記法存取巢狀欄位。
- **效能**：編製索引與搜尋的效能特性類似。
- **儲存空間**：兩者都將整個物件儲存為單一 Lucene 欄位。
- **限制**：兩者在彙總與排序方面有類似的限制。

## 疑難排解

如果您在 `flattened` 欄位遷移時遇到問題：

1. **確認目標版本** -- 確保您的目標 OpenSearch 叢集執行的是 2.7 或更新版本。

2. **檢查遷移記錄檔** -- 檢閱詳細的遷移記錄檔，查看是否有任何警告或錯誤：
   ```bash
   cat /shared-logs-output/migration-console-default/*/metadata/*.log
   ```

3. **驗證對應** -- 遷移後，確認欄位類型已正確轉換：
   ```bash
   GET /your-index/_mapping
   ```

## 相關文件

- [轉換欄位類型文件]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/) -- 設定自訂欄位類型轉換。
- [flat_object 欄位類型文件]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/flat-object/) -- 了解 flat_object 欄位類型。