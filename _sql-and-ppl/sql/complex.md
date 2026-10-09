---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "複雜查詢"
parent: SQL
nav_order: 6
redirect_from:
  - /search-plugins/sql/complex/
  - /search-plugins/sql/sql/complex/
---

# 複雜 SQL 查詢

除了簡單的 SFW (`SELECT-FROM-WHERE`) 查詢之外，SQL 外掛程式也支援複雜查詢，例如子查詢、join、union 和 minus。這些查詢會在多個 OpenSearch 索引上運作。若要檢視這些查詢在幕後的執行方式，請使用 `explain` 操作。


## 聯結

OpenSearch SQL 支援 inner join、cross join 和 left outer join。

### 限制

Join 有若干限制：

1. 您只能 join 兩個索引。
1. 您必須為索引使用別名（例如 `people p`）。
1. 在 ON 子句中，您只能使用 AND 條件。
1. 在 WHERE 陳述式中，請勿合併包含多個索引的樹狀結構。例如，下列陳述式可運作：

   ```
   WHERE (a.type1 > 3 OR a.type1 < 0) AND (b.type2 > 4 OR b.type2 < -1)
   ```

   下列陳述式則不行：

   ```
   WHERE (a.type1 > 3 OR b.type2 < 0) AND (a.type1 > 4 OR b.type2 < -1)
   ```

1. 您無法對結果使用 GROUP BY 或 ORDER BY。
1. 不支援搭配 OFFSET 的 LIMIT（例如 `LIMIT 25 OFFSET 25`）。

### 說明

`JOIN` 子句會使用各索引共通的値，合併來自一或多個索引的欄位。

### 語法

規則 `tableSource`：

![tableSource 規則]({{site.url}}{{site.baseurl}}/images/tableSource.png)

規則 `joinPart`：

![joinPart 規則]({{site.url}}{{site.baseurl}}/images/joinPart.png)

### 範例 1：內部聯結

Inner join 會根據您的 join 述詞，合併兩個索引的欄位來建立新的結果集。它會逐一查看兩個索引並比較每份文件，以找出符合 join 述詞的文件。您可以選擇在 `JOIN` 子句前面加上 `INNER` 關鍵字。

Join 述詞由 ON 子句指定。

SQL 查詢：

```sql
SELECT
  a.account_number, a.firstname, a.lastname,
  e.id, e.name
FROM accounts a
JOIN employees_nested e
 ON a.account_number = e.id
```
{% include copy.html %}


說明：

`explain` 輸出很複雜，因為 `JOIN` 子句會與兩個在不同查詢規劃架構中執行的 OpenSearch DSL 查詢相關聯。您可以檢查 `Physical Plan` 和 `Logical Plan` 物件來解讀它。

```json
{
  "Physical Plan" : {
    "Project [ columns=[a.account_number, a.firstname, a.lastname, e.name, e.id] ]" : {
      "Top [ count=200 ]" : {
        "BlockHashJoin[ conditions=( a.account_number = e.id ), type=JOIN, blockSize=[FixedBlockSize with size=10000] ]" : {
          "Scroll [ employees_nested as e, pageSize=10000 ]" : {
            "request" : {
              "size" : 200,
              "from" : 0,
              "_source" : {
                "excludes" : [ ],
                "includes" : [
                  "id",
                  "name"
                ]
              }
            }
          },
          "Scroll [ accounts as a, pageSize=10000 ]" : {
            "request" : {
              "size" : 200,
              "from" : 0,
              "_source" : {
                "excludes" : [ ],
                "includes" : [
                  "account_number",
                  "firstname",
                  "lastname"
                ]
              }
            }
          },
          "useTermsFilterOptimization" : false
        }
      }
    }
  },
  "description" : "Hash Join algorithm builds hash table based on result of first query, and then probes hash table to find matched rows for each row returned by second query",
  "Logical Plan" : {
    "Project [ columns=[a.account_number, a.firstname, a.lastname, e.name, e.id] ]" : {
      "Top [ count=200 ]" : {
        "Join [ conditions=( a.account_number = e.id ) type=JOIN ]" : {
          "Group" : [
            {
              "Project [ columns=[a.account_number, a.firstname, a.lastname] ]" : {
                "TableScan" : {
                  "tableAlias" : "a",
                  "tableName" : "accounts"
                }
              }
            },
            {
              "Project [ columns=[e.name, e.id] ]" : {
                "TableScan" : {
                  "tableAlias" : "e",
                  "tableName" : "employees_nested"
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

查詢會傳回下列結果：

<!-- vale off -->

| a.account_number | a.firstname | a.lastname | e.id | e.name |
| :--- | :--- | :--- | :--- | :--- |
| 6 | Hattie | Bond | 6 | Jane Smith |

<!-- vale on -->

### 範例 2：交叉聯結

Cross join 又稱為 Cartesian join，會將第一個索引中的每份文件與第二個索引中的每份文件合併。
結果集是兩個索引中所有文件的笛卡兒積。
此操作類似於沒有用來指定聯結條件的 `ON` 子句的 inner join。

對兩個大型甚至中型索引執行 cross join 有風險。它可能會觸發斷路器來終止查詢，以避免記憶體耗盡。
{: .warning }

SQL 查詢：

```sql
SELECT
  a.account_number, a.firstname, a.lastname,
  e.id, e.name
FROM accounts a
JOIN employees_nested e
```
{% include copy.html %}


查詢會傳回下列結果：

<!-- vale off -->

| a.account_number | a.firstname | a.lastname | e.id | e.name |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Amber | Duke | 3 | Bob Smith |
| 1 | Amber | Duke | 4 | Susan Smith |
| 1 | Amber | Duke | 6 | Jane Smith |
| 6 | Hattie | Bond | 3 | Bob Smith |
| 6 | Hattie | Bond | 4 | Susan Smith |
| 6 | Hattie | Bond | 6 | Jane Smith |
| 13 | Nanette | Bates | 3 | Bob Smith |
| 13 | Nanette | Bates | 4 | Susan Smith |
| 13 | Nanette | Bates | 6 | Jane Smith |
| 18 | Dale | Adams | 3 | Bob Smith |
| 18 | Dale | Adams | 4 | Susan Smith |
| 18 | Dale | Adams | 6 | Jane Smith |

<!-- vale on -->

### 範例 3：左外部聯結

使用 left outer join 可保留第一個索引中不符合 join 述詞的資料列。關鍵字 `OUTER` 為選用。

SQL 查詢：

```sql
SELECT
  a.account_number, a.firstname, a.lastname,
  e.id, e.name
FROM accounts a
LEFT JOIN employees_nested e
 ON a.account_number = e.id
```
{% include copy.html %}


查詢會傳回下列結果：

<!-- vale off -->

| a.account_number | a.firstname | a.lastname | e.id | e.name |
| :--- | :--- | :--- | :--- | :--- |
| 1 | Amber | Duke | null | null |
| 6 | Hattie | Bond | 6 | Jane Smith |
| 13 | Nanette | Bates | null | null |
| 18 | Dale | Adams | null | null |

<!-- vale on -->

## 子查詢

子查詢是完整的 `SELECT` 陳述式，用於另一個陳述式內並以括號括住。
從 explain 輸出中，您可以看到某些子查詢實際上會轉換為等效的 join 查詢來執行。

### 範例 1：資料表子查詢

SQL 查詢：

```sql
SELECT a1.firstname, a1.lastname, a1.balance
FROM accounts a1
WHERE a1.account_number IN (
  SELECT a2.account_number
  FROM accounts a2
  WHERE a2.balance > 10000
)
```
{% include copy.html %}


說明：

```json
{
  "Physical Plan" : {
    "Project [ columns=[a1.balance, a1.firstname, a1.lastname] ]" : {
      "Top [ count=200 ]" : {
        "BlockHashJoin[ conditions=( a1.account_number = a2.account_number ), type=JOIN, blockSize=[FixedBlockSize with size=10000] ]" : {
          "Scroll [ accounts as a2, pageSize=10000 ]" : {
            "request" : {
              "size" : 200,
              "query" : {
                "bool" : {
                  "filter" : [
                    {
                      "bool" : {
                        "adjust_pure_negative" : true,
                        "must" : [
                          {
                            "bool" : {
                              "adjust_pure_negative" : true,
                              "must" : [
                                {
                                  "bool" : {
                                    "adjust_pure_negative" : true,
                                    "must_not" : [
                                      {
                                        "bool" : {
                                          "adjust_pure_negative" : true,
                                          "must_not" : [
                                            {
                                              "exists" : {
                                                "field" : "account_number",
                                                "boost" : 1
                                              }
                                            }
                                          ],
                                          "boost" : 1
                                        }
                                      }
                                    ],
                                    "boost" : 1
                                  }
                                },
                                {
                                  "range" : {
                                    "balance" : {
                                      "include_lower" : false,
                                      "include_upper" : true,
                                      "from" : 10000,
                                      "boost" : 1,
                                      "to" : null
                                    }
                                  }
                                }
                              ],
                              "boost" : 1
                            }
                          }
                        ],
                        "boost" : 1
                      }
                    }
                  ],
                  "adjust_pure_negative" : true,
                  "boost" : 1
                }
              },
              "from" : 0
            }
          },
          "Scroll [ accounts as a1, pageSize=10000 ]" : {
            "request" : {
              "size" : 200,
              "from" : 0,
              "_source" : {
                "excludes" : [ ],
                "includes" : [
                  "firstname",
                  "lastname",
                  "balance",
                  "account_number"
                ]
              }
            }
          },
          "useTermsFilterOptimization" : false
        }
      }
    }
  },
  "description" : "Hash Join algorithm builds hash table based on result of first query, and then probes hash table to find matched rows for each row returned by second query",
  "Logical Plan" : {
    "Project [ columns=[a1.balance, a1.firstname, a1.lastname] ]" : {
      "Top [ count=200 ]" : {
        "Join [ conditions=( a1.account_number = a2.account_number ) type=JOIN ]" : {
          "Group" : [
            {
              "Project [ columns=[a1.balance, a1.firstname, a1.lastname, a1.account_number] ]" : {
                "TableScan" : {
                  "tableAlias" : "a1",
                  "tableName" : "accounts"
                }
              }
            },
            {
              "Project [ columns=[a2.account_number] ]" : {
                "Filter [ conditions=[AND ( AND account_number ISN null, AND balance GT 10000 ) ] ]" : {
                  "TableScan" : {
                    "tableAlias" : "a2",
                    "tableName" : "accounts"
                  }
                }
              }
            }
          ]
        }
      }
    }
  }
}
```

查詢會傳回下列結果：

<!-- vale off -->

| a1.firstname | a1.lastname | a1.balance |
| :--- | :--- | :--- |
| Amber | Duke | 39225 |
| Nanette | Bates | 32838 |

<!-- vale on -->

### 範例 2：FROM 子句中的子查詢

SQL 查詢：

```sql
SELECT a.f, a.l, a.a
FROM (
  SELECT firstname AS f, lastname AS l, age AS a
  FROM accounts
  WHERE age > 30
) AS a
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
        }
      ],
      "adjust_pure_negative" : true,
      "boost" : 1.0
    }
  },
  "_source" : {
    "includes" : [
      "firstname",
      "lastname",
      "age"
    ],
    "excludes" : [ ]
  }
}
```

查詢會傳回下列結果：

<!-- vale off -->

| f | l | a |
| :--- | :--- | :--- |
| Amber | Duke | 32 |
| Dale | Adams | 33 |
| Hattie | Bond | 36 |

<!-- vale on -->