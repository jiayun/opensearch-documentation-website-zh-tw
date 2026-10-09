---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "全部相符查詢"
nav_order: 20
---

# 全部相符查詢

`match_all` 查詢會傳回所有文件。如果您需要傳回整組文件，此查詢在測試大型文件集時可能很實用。

```json
GET _search
{
  "query": {
    "match_all": {}
  }
}
```
{% include copy-curl.html %}

`match_all` 查詢有 `match_none` 對應版本，但很少派上用場：

```json
GET _search
{
  "query": {
    "match_none": {}
  }
}
```
{% include copy-curl.html %}


## 參數

`match_all` 和 `match_none` 查詢都接受下列參數。所有參數都是選用的。

參數 | 資料類型 | 說明
:--- | :--- | :---
`boost` | 浮點數 | 指定此欄位對相關性分數之權重的浮點值。大於 1.0 的值會提高欄位的相關性。介於 0.0 和 1.0 之間的值會降低欄位的相關性。預設值為 1.0。
`_name` | 字串 | 用於查詢標記的查詢名稱。選用。
