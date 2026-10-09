---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "疑難排解"
nav_order: 88
redirect_from:
  - /search-plugins/sql/troubleshoot/
---

# SQL 與 PPL 疑難排解

SQL 外掛程式是無狀態的，因此疑難排解大多著重於特定查詢失敗的原因。

最常見的錯誤是令人聞之色變的空指標例外，這可能發生在剖析錯誤期間，或使用錯誤的 HTTP 方法時（POST 與 GET，以及相反情況）。POST 方法與 HTTP 請求本文能提供最一致的結果：

```json
POST _plugins/_sql
{
  "query": "SELECT * FROM my-index WHERE ['name.firstname']='saanvi' LIMIT 5"
}
```
{% include copy-curl.html %}

如果查詢的行為不如預期，請使用 `_explain` API 查看轉譯後的查詢，然後據以進行疑難排解。對大多數操作而言，`_explain` 會傳回 OpenSearch query DSL。對於 `UNION`、`MINUS` 和 `JOIN`，它會傳回更類似 SQL 執行計畫的內容。

#### 範例請求

```json
POST _plugins/_sql/_explain
{
  "query": "SELECT * FROM my-index LIMIT  50"
}
```
{% include copy-curl.html %}


#### 範例回應

```json
{
  "from": 0,
  "size": 50
}
```

## 索引對應驗證例外

如果您看到下列驗證例外，請確認查詢中的索引不是索引模式，且沒有多個類型：

```json
{
  "error": {
    "reason": "There was internal problem at backend",
    "details": "When using multiple indices, the mappings must be identical.",
    "type": "VerificationException"
  },
  "status": 503
}
```

如果這些步驟無效，請提交 [GitHub 議題](https://github.com/opensearch-project/sql/issues)。
