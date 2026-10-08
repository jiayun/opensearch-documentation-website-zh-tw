---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: indices
parent: Anatomy of a workload
nav_order: 10
redirect_from:
  - /benchmark/workloads/indices/
---

<!-- vale off -->
# indices 元素
<!-- vale on -->

`indices` 元素包含工作負載中使用的所有索引清單。

## 範例

若要建立索引，請指定其名稱。若要為索引新增定義，請使用 `body` 選項並將其指向包含索引定義的 JSON 檔案：

```json
"indices": [
    {
      "name": "geonames",
      "body": "geonames-index.json",
    }
]
```

## 組態選項

請搭配 `indices` 使用下列選項：

參數 | 必要 | 類型 | 說明
:--- | :--- | :--- | :---
`name` | 是 | 字串 | 索引範本的名稱。
`body` | 否 | 字串 | 對應至 Create Index API 請求本文中所使用索引定義的檔案名稱。 
