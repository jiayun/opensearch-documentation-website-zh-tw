---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "轉換欄位類型"
nav_order: 2
parent: Migrate metadata
grand_parent: Migration phases
permalink: /classic/migration-assistant/migration-phases/migrate-metadata/handling-field-type-breaking-changes/
---

# 轉換欄位類型

{: .note }
這些轉換可能不適用於您的使用情境，但建立轉換的框架旨在處理變更工作負載或將其移至新目標時的突變、資料充實及其他修改。

本指南說明如何在遷移至 OpenSearch 的過程中，使用 Migration Assistant 轉換已淘汰或不相容的欄位類型。

欄位類型定義資料在索引中的儲存與查詢方式。文件中的每個欄位都對應到一個資料類型，該類型決定其索引方式以及可對其執行哪些操作。

例如，下列圖書館藏書的索引對應定義了三個欄位，每個欄位各有不同的類型：

```json
GET /library-books/_mappings
{
  "library-books": {
    "mappings": {
      "properties": {
        "title":          { "type": "text" },
        "publishedDate":  { "type": "date" },
        "pageCount":      { "type": "integer" }
      }
    }
  }
}
```

如需更多資訊，請參閱[對應與欄位類型]({{site.url}}{{site.baseurl}}/mappings/)。

## 設定項目轉換

您可以提供轉換組態檔，自訂中繼資料與資料遷移期間欄位類型的轉換方式，步驟如下：

1. 開啟 Migration Assistant 主控台。
2. 使用下列命令建立 JavaScript 檔案來定義您的轉換邏輯：

   ```bash
   vim /shared-logs-output/field-type-converter.js
   ```
   {% include copy.html %}

3. 撰寫任何執行所需欄位類型轉換的 JavaScript 規則。如需規則實作方式的範例，請參閱[`field-type-converter.js` 實作範例](#example-field-type-converterjs-implementation)。
4. 使用下列命令建立轉換描述檔：

   ```bash
   vim /shared-logs-output/transformation.json
   ```
   {% include copy.html %}

5. 在 `transformation.json` 中加入對您 JavaScript 檔案的參照。
6. 執行中繼資料遷移，並使用類似下列的命令提供轉換組態：

   ```bash
   console metadata migrate \
     --transformer-config-file /shared-logs-output/transformation.json
   ```
   {% include copy.html %}

### `field-type-converter.js` 實作範例

下列指令碼示範如何執行常見的欄位類型轉換，包括：

* 將已淘汰的 `string` 類型替換為 `text`。
* 將 `flattened` 轉換為 `flat_object`，並在存在時移除 `index` 屬性。


```javascript
function main(context) {
  const rules = [
    {
      when: { type: "string" },
      set: { type: "text" }
    },
    {
      when: { type: "flattened" },
      set: { type: "flat_object" },
      remove: ["index"]
    }
  ];

  function applyRules(node, rules) {
    if (Array.isArray(node)) {
      node.forEach((child) => applyRules(child, rules));
    } else if (node instanceof Map) {
      for (const { when, set, remove = [] } of rules) {
        const matches = Object.entries(when).every(([k, v]) => node.get(k) === v);
        if (matches) {
          Object.entries(set).every(([k, v]) => node.set(k, v));
          remove.forEach((key) => node.delete(key));
        }
      }
      for (const child of node.values()) {
        applyRules(child, rules);
      }
    } else if (node && typeof node === "object") {
      for (const { when, set, remove = [] } of rules) {
        const matches = Object.entries(when).every(([k, v]) => node[k] === v);
        if (matches) {
          Object.assign(node, set);
          remove.forEach((key) => delete node[key]);
        }
      }
      Object.values(node).forEach((child) => applyRules(child, rules));
    }
  }

  return (doc) => {
    if (doc && doc.type && doc.name && doc.body) {
      applyRules(doc, rules);
    }
    return doc;
  };
}
(() => main)();
```
{% include copy.html %}

該指令碼包含下列元素：

1. `rules` 陣列定義轉換邏輯：

   * `when`：用於比對節點的鍵值條件
   * `set`：當 `when` 子句符合時要套用的鍵值對
   * `remove` (選用)：符合時要從節點刪除的鍵

2. `applyRules` 函式會遞迴走訪輸入：

   * 陣列會逐元素遞迴處理。
   * `Map` 物件會使用定義的規則進行比對與修改。
   * 一般物件會檢查是否符合並據以轉換。

3. `main` 函式會回傳一個轉換函式，該函式會：

   * 將規則套用至每份文件。
   * 回傳修改後的文件，供遷移或重新播放使用。

### `transformation.json` 範例

下列 JSON 檔案會參照您的轉換指令碼，並使用您的自訂規則初始化 JavaScript 引擎：

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

## 摘要

透過使用轉換組態，您可以在中繼資料遷移或資料重新播放期間改寫已淘汰或不相容的欄位類型。這可確保目標 OpenSearch 叢集只會收到相容的對應——即使來源叢集包含 `string` 等過時類型，或需要轉換的 `flattened` 等功能。
