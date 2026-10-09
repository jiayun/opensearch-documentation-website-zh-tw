---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "刪除"
parent: SQL
nav_order: 12
redirect_from:
  - /search-plugins/sql/delete/
  - /search-plugins/sql/sql/delete/
---


# SQL DELETE 陳述式

`DELETE` 陳述式會刪除符合 `WHERE` 子句中述詞的文件。
如果您未指定 `WHERE` 子句，則會刪除所有文件。

### 設定

`DELETE` 陳述式預設為停用。若要在 SQL 中啟用 `DELETE` 功能，您需要傳送下列請求來更新組態：

```json
PUT _plugins/_query/settings
{
  "transient": {
    "plugins.sql.delete.enabled": "true"
  }
}
```
{% include copy-curl.html %}

### 語法

規則 `singleDeleteStatement`：

![singleDeleteStatement]({{site.url}}{{site.baseurl}}/images/singleDeleteStatement.png)

### 範例

SQL 查詢：

```sql
DELETE FROM accounts
WHERE age > 30
```
{% include copy.html %}


說明：

```json
{
  "size" : 1000,
  "query" : {
    "bool" : {
      "must" : [
        {
          "range" : {
            "age" : {
              "from" : 30,
              "to" : null,
              "include_lower" : false,
              "include_upper" : true,
              "boost" : 1.0
            }
          }
        }
      ],
      "adjust_pure_negative" : true,
      "boost" : 1.0
    }
  },
  "_source" : false
}
```

查詢會傳回下列結果：

```json
{
  "schema" : [
    {
      "name" : "deleted_rows",
      "type" : "long"
    }
  ],
  "total" : 1,
  "datarows" : [
    [
      3
    ]
  ],
  "size" : 1,
  "status" : 200
}
```

`datarows` 欄位會顯示已刪除的文件數。
