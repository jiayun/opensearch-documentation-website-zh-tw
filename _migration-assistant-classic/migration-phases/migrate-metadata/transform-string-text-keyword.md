---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "將 string 欄位轉換為 text/keyword"
nav_order: 4
parent: Migrate metadata
grand_parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/migrate-metadata/transform-string-text-keyword/
---

# 將 string 欄位轉換為 text/keyword


本指南說明 Migration Assistant 在從較早版本的 Elasticsearch 遷移時，如何自動處理已淘汰的 `string` 欄位類型。

## 概觀

`string` 欄位類型是 Elasticsearch 早期版本的主要文字欄位類型，但在 Elasticsearch 5.x 中已被淘汰，並在 Elasticsearch 6.0 中完全移除。在 Elasticsearch 5.x 中，它僅在向後相容模式下可用。

當從 Elasticsearch 1.x 至 5.x 遷移到較新版本時，Migration Assistant 會自動將 `string` 欄位類型轉換為其現代等效類型：已分析的欄位轉換為 `text`，未分析的欄位轉換為 `keyword`。

若要判斷 Elasticsearch 叢集是否使用 `string` 欄位類型，請呼叫來源叢集的 `GET /_mapping` API。在 Migration Console 中執行 `console clusters curl source_cluster "/_mapping"`。如果您看到 `"type":"string"`，表示此轉換適用，且這些欄位將在遷移期間自動轉換。

## 相容性

`string` 轉換為 `text`/`keyword` 的欄位類型轉換適用於：
- **來源叢集**：Elasticsearch 1.x--5.x
- **目標叢集**：Elasticsearch 5.x+ 或 OpenSearch 1.x+
- **自動轉換**：中繼資料遷移期間不需要任何組態。

## 自動轉換邏輯

Migration Assistant 會根據欄位的 `index` 屬性，決定是否將 `string` 欄位轉換為 `text` 或 `keyword`。

### 轉換為 `keyword`
在下列情況下，欄位會轉換為 `keyword`：
- `index: "not_analyzed"`
- `index: "no"`
- `index: false`

### 轉換為 `text`
在下列情況下，欄位會轉換為 `text`：
- `index: "analyzed"`
- `index` 未定義

### 屬性清理

在轉換期間，Migration Assistant 也會清理與目標欄位類型不相容的屬性。

**對於 `keyword` 欄位**，會移除下列屬性：
- `analyzer`
- `search_analyzer`
- `position_increment_gap`
- `term_vector`
- `fielddata`

**對於 `text` 欄位**，會移除下列屬性：
- `doc_values`
- `null_value` (如果存在)

此外，舊版的 `index` 值會被正規化：
- `index: "analyzed"` 和 `index: "not_analyzed"` 會被移除 (Elasticsearch 5.x 的預設值為 `true`)。
- `index: "no"` 會變成 `index: false`。

## 遷移輸出

在遷移過程中，您會在輸出中看到此轉換：

```
Transformations:
   string to text/keyword:
      Convert field type string to text/keyword based on field data mappings
```

## 轉換行為

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
    "status": {
      "type": "string",
      "index": "not_analyzed",
      "doc_values": true
    },
    "category": {
      "type": "string",
      "index": "no"
    }
  }
}</code></pre>
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <pre><code>{
  "properties": {
    "status": {
      "type": "keyword",
      "doc_values": true
    },
    "category": {
      "type": "keyword",
      "index": false
    }
  }
}</code></pre>
      </td>
    </tr>
    <tr>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <pre><code>{
  "properties": {
    "title": {
      "type": "string",
      "analyzer": "standard",
      "fielddata": true
    },
    "description": {
      "type": "string",
      "index": "analyzed",
      "term_vector": "with_positions"
    }
  }
}</code></pre>
      </td>
      <td style="border: 1px solid #ddd; padding: 8px;">
        <pre><code>{
  "properties": {
    "title": {
      "type": "text",
      "analyzer": "standard",
      "fielddata": true
    },
    "description": {
      "type": "text",
      "term_vector": "with_positions"
    }
  }
}</code></pre>
      </td>
    </tr>
  </tbody>
</table>

## 行為差異

Migration Assistant 會在中繼資料遷移期間自動轉換所有 `string` 欄位，不需要額外的組態。

### 混合欄位類型

如果您的來源叢集已包含 `string`、`text` 和 `keyword` 欄位的混合 (在還原了 Elasticsearch 2.x 索引的 Elasticsearch 5.x 中很常見)，則只會轉換 `string` 欄位。現有的 `text` 和 `keyword` 欄位保持不變。

### 查詢與彙總的影響

遷移之後，請注意下列主要差異：

- **詞彙查詢**在 `text` (已分析) 和 `keyword` (精確比對) 欄位上的運作方式不同。
- **彙總**：`text` 欄位無法用於彙總，除非啟用 `fielddata`；`keyword` 欄位則可直接用於彙總。
- **排序**：`text` 欄位預設無法用於排序；`keyword` 欄位支援排序。
- **大小寫敏感度**：`keyword` 欄位區分大小寫；`text` 欄位則取決於分析器。

### 應用程式相容性

請檢查您的應用程式程式碼中是否有：
- 預期舊 `string` 欄位行為的查詢。
- 對已轉換為 `text` 之欄位的彙總或排序。
- 對現在使用 `keyword` 之欄位的區分大小寫搜尋。

對於同時需要已分析和精確比對功能的欄位，請考慮在遷移後使用同時包含 `text` 和 `keyword` 對應的多欄位 (multi-fields)。

## 疑難排解

如果您在 string 欄位轉換時遇到問題：

1. **驗證來源版本** -- 確認您的來源叢集執行的是 Elasticsearch 1.x 至 5.x。

2. **檢查遷移記錄檔** -- 檢閱詳細的遷移記錄檔，查看是否有任何警告或錯誤：
   ```bash
   tail /shared-logs-output/migration-console-default/*/metadata/*.log
   ```

3. **驗證對應** -- 遷移之後，確認欄位類型已正確轉換：
   ```bash
   GET /your-index/_mapping
   ```

4. **檢視欄位使用情況** -- 確認您的應用程式查詢與新的欄位類型相容。原本適用於 `string` 欄位的查詢應該仍可搭配 `text` 和 `keyword` 欄位運作，但某些進階功能的行為可能不同。

## 相關文件

- [Transform field types 文件]({{site.url}}{{site.baseurl}}/classic/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/) -- 設定自訂欄位類型轉換。
- [keyword 欄位類型文件]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/) -- 瞭解 keyword 欄位類型。
- [text 欄位類型文件]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) -- 瞭解 text 欄位類型。
