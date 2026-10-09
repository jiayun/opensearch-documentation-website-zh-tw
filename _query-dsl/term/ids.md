---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: IDs
parent: Term-level queries
nav_order: 40
---

# IDs 查詢

使用 `ids` 查詢，在 `_id` 欄位中搜尋具有一個或多個特定文件 ID 值的文件。例如，下列查詢會請求 ID 為 `34229` 和 `91296` 的文件：

```json
GET shakespeare/_search
{
  "query": {
    "ids": {
      "values": [
        34229,
        91296
      ]
    }
  }
}
```
{% include copy-curl.html %}

## 參數

此查詢接受下列參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`values` | 字串陣列 | 要搜尋的文件 ID。必要。
`boost` | 浮點數 | 浮點值，用來指定此欄位對相關性分數的權重。大於 1.0 的值會提高欄位的相關性。介於 0.0 和 1.0 之間的值會降低欄位的相關性。預設值為 1.0。
