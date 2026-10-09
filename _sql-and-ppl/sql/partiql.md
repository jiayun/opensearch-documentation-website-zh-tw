---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "JSON 支援"
parent: SQL
nav_order: 8
redirect_from:
  - /search-plugins/sql/partiql/
  - /search-plugins/sql/sql/partiql/
---

# SQL JSON 支援

SQL 外掛程式依照 [PartiQL](https://partiql.org/) 規格支援 JSON，PartiQL 是一種相容於 SQL 的查詢語言，可讓您查詢任何資料格式的半結構化與巢狀資料。SQL 外掛程式僅支援 PartiQL 規格的子集。

## 查詢巢狀集合

PartiQL 擴充了 SQL，讓您可以查詢並扁平化巢狀集合。在 OpenSearch 中，這對查詢含有巢狀物件或欄位的 JSON 索引非常有用。

若要跟著操作，請使用 `bulk` 操作將一些範例資料編製索引：

```json
POST employees_nested/_bulk?refresh
{"index":{"_id":"1"}}
{"id":3,"name":"Bob Smith","title":null,"projects":[{"name":"SQL Spectrum querying","started_year":1990},{"name":"SQL security","started_year":1999},{"name":"OpenSearch security","started_year":2015}]}
{"index":{"_id":"2"}}
{"id":4,"name":"Susan Smith","title":"Dev Mgr","projects":[]}
{"index":{"_id":"3"}}
{"id":6,"name":"Jane Smith","title":"Software Eng 2","projects":[{"name":"SQL security","started_year":1998},{"name":"Hello security","started_year":2015,"address":[{"city":"Dallas","state":"TX"}]}]}
```
{% include copy-curl.html %}

### 範例 1：扁平化巢狀集合

此範例會找出欄位值 (`name`) 符合述詞 (包含 `security`) 的巢狀文件 (`projects`)。由於每個父文件可能有多個巢狀文件，符合條件的巢狀文件會被扁平化。換句話說，最終結果是父文件與巢狀文件之間的笛卡兒積。

```sql
SELECT e.name AS employeeName,
       p.name AS projectName
FROM employees_nested AS e,
       e.projects AS p
WHERE p.name LIKE '%security%'
```
{% include copy.html %}


說明：

```json
{
  "from" : 0,
  "size" : 200,
  "query" : {
    "bool" : {
      "filter" : [
        {
          "bool" : {
            "must" : [
              {
                "nested" : {
                  "query" : {
                    "wildcard" : {
                      "projects.name" : {
                        "wildcard" : "*security*",
                        "boost" : 1.0
                      }
                    }
                  },
                  "path" : "projects",
                  "ignore_unmapped" : false,
                  "score_mode" : "none",
                  "boost" : 1.0,
                  "inner_hits" : {
                    "ignore_unmapped" : false,
                    "from" : 0,
                    "size" : 3,
                    "version" : false,
                    "seq_no_primary_term" : false,
                    "explain" : false,
                    "track_scores" : false,
                    "_source" : {
                      "includes" : [
                        "projects.name"
                      ],
                      "excludes" : [ ]
                    }
                  }
                }
              }
            ],
            "adjust_pure_negative" : true,
            "boost" : 1.0
          }
        }
      ],
      "adjust_pure_negative" : true,
      "boost" : 1.0
    }
  },
  "_source" : {
    "includes" : [
      "name"
    ],
    "excludes" : [ ]
  }
}
```

查詢會傳回以下結果：

<!-- vale off -->

| employeeName | projectName
:--- | :---
Bob Smith | OpenSearch Security
Bob Smith | SQL security
Jane Smith | Hello security
Jane Smith | SQL security

<!-- vale on -->

### 範例 2：存在子查詢中的扁平化

若要在子查詢中扁平化巢狀集合，以檢查它是否符合某個條件：

```sql
SELECT e.name AS employeeName
FROM employees_nested AS e
WHERE EXISTS (
    SELECT *
    FROM e.projects AS p
    WHERE p.name LIKE '%security%'
)
```
{% include copy.html %}


說明：

```json
{
  "from" : 0,
  "size" : 200,
  "query" : {
    "bool" : {
      "filter" : [
        {
          "bool" : {
            "must" : [
              {
                "nested" : {
                  "query" : {
                    "bool" : {
                      "must" : [
                        {
                          "bool" : {
                            "must" : [
                              {
                                "bool" : {
                                  "must_not" : [
                                    {
                                      "bool" : {
                                        "must_not" : [
                                          {
                                            "exists" : {
                                              "field" : "projects",
                                              "boost" : 1.0
                                            }
                                          }
                                        ],
                                        "adjust_pure_negative" : true,
                                        "boost" : 1.0
                                      }
                                    }
                                  ],
                                  "adjust_pure_negative" : true,
                                  "boost" : 1.0
                                }
                              },
                              {
                                "wildcard" : {
                                  "projects.name" : {
                                    "wildcard" : "*security*",
                                    "boost" : 1.0
                                  }
                                }
                              }
                            ],
                            "adjust_pure_negative" : true,
                            "boost" : 1.0
                          }
                        }
                      ],
                      "adjust_pure_negative" : true,
                      "boost" : 1.0
                    }
                  },
                  "path" : "projects",
                  "ignore_unmapped" : false,
                  "score_mode" : "none",
                  "boost" : 1.0
                }
              }
            ],
            "adjust_pure_negative" : true,
            "boost" : 1.0
          }
        }
      ],
      "adjust_pure_negative" : true,
      "boost" : 1.0
    }
  },
  "_source" : {
    "includes" : [
      "name"
    ],
    "excludes" : [ ]
  }
}
```

查詢會傳回以下結果：

<!-- vale off -->

| employeeName |
:--- | :---
Bob Smith |
Jane Smith |

<!-- vale on -->