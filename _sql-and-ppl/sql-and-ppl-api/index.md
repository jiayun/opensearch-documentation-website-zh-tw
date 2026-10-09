---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "SQL 與 PPL API"
nav_order: 1
has_children: true
redirect_from:
  - /search-plugins/sql/sql-ppl-api/
  - /sql-and-ppl/sql-ppl-api/
  - /sql-and-ppl/sql-and-ppl-api/
---

# SQL 與 PPL API

使用 SQL 與 PPL API 將查詢傳送至 SQL 外掛程式。使用 `_sql` 端點以 SQL 傳送查詢，並使用 `_ppl` 端點以 PPL 傳送查詢。對於這兩者，您也可以使用 `_explain` 端點將查詢轉譯為 [OpenSearch 領域特定語言]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/) (DSL)，或對錯誤進行疑難排解。

## Query API

將 SQL/PPL 查詢傳送至 SQL 外掛程式。您可以透過查詢參數傳遞回應的格式。

### 查詢參數

參數 | 資料類型 | 說明
:--- | :--- | :---
[format]({{site.url}}{{site.baseurl}}/search-plugins/sql/response-formats/) | 字串 | 回應的格式。`_sql` 端點支援 `jdbc`、`csv`、`raw` 與 `json` 格式。`_ppl` 端點支援 `jdbc`、`csv` 與 `raw` 格式。預設為 `jdbc`。
`sanitize` | 布林值 | 指定是否在結果中逸出特殊字元。如需更多資訊，請參閱[回應格式]({{site.url}}{{site.baseurl}}/search-plugins/sql/response-formats/)。預設為 `true`。

### 請求本文欄位

欄位 | 資料類型 | 說明  
:--- | :--- | :---
`query` | 字串 | 要執行的查詢。必要。
[filter](#filtering-results) | JSON 物件 | 結果的篩選條件。選用。
[fetch_size](#paginating-results) | 整數 | 單一回應中要傳回的結果數量。用於結果分頁。預設為 1,000。選用。SQL 支援 `fetch_size`，且需要使用 `jdbc` 回應格式。

#### 範例請求

```json
POST /_plugins/_sql
{
  "query" : "SELECT * FROM accounts"
}
```
{% include copy-curl.html %}

#### 範例回應

回應包含結構描述與結果：

```json
{
  "schema": [
    {
      "name": "account_number",
      "type": "long"
    },
    {
      "name": "firstname",
      "type": "text"
    },
    {
      "name": "address",
      "type": "text"
    },
    {
      "name": "balance",
      "type": "long"
    },
    {
      "name": "gender",
      "type": "text"
    },
    {
      "name": "city",
      "type": "text"
    },
    {
      "name": "employer",
      "type": "text"
    },
    {
      "name": "state",
      "type": "text"
    },
    {
      "name": "age",
      "type": "long"
    },
    {
      "name": "email",
      "type": "text"
    },
    {
      "name": "lastname",
      "type": "text"
    }
  ],
  "datarows": [
    [
      1,
      "Amber",
      "880 Holmes Lane",
      39225,
      "M",
      "Brogan",
      "Pyrami",
      "IL",
      32,
      "amberduke@pyrami.com",
      "Duke"
    ],
    [
      6,
      "Hattie",
      "671 Bristol Street",
      5686,
      "M",
      "Dante",
      "Netagy",
      "TN",
      36,
      "hattiebond@netagy.com",
      "Bond"
    ],
    [
      13,
      "Nanette",
      "789 Madison Street",
      32838,
      "F",
      "Nogal",
      "Quility",
      "VA",
      28,
      "nanettebates@quility.com",
      "Bates"
    ],
    [
      18,
      "Dale",
      "467 Hutchinson Court",
      4180,
      "M",
      "Orick",
      null,
      "MD",
      33,
      "daleadams@boink.com",
      "Adams"
    ]
  ],
  "total": 4,
  "size": 4,
  "status": 200
}
```

### 回應本文欄位

欄位 | 資料類型 | 說明  
:--- | :--- | :---
`schema` | 陣列 | 指定所有欄位的名稱與類型。
`data_rows` | 二維陣列 | 結果的陣列。每個結果代表一個符合的資料列 (文件)。
`total` | 整數 | 索引中的資料列 (文件) 總數。
`size` | 整數 | 單一回應中要傳回的結果數量。
`status` | 字串 | OpenSearch 在執行查詢後傳回的 HTTP 回應狀態。

## Explain API

SQL 外掛程式的 `explain` 功能會顯示查詢如何在 OpenSearch 上執行，這對偵錯與開發非常有用。向 `_plugins/_sql/_explain` 或 `_plugins/_ppl/_explain` 端點傳送 POST 請求，會以 JSON 格式傳回 [OpenSearch 領域特定語言]({{site.url}}{{site.baseurl}}/opensearch/query-dsl/) (DSL)。

從 OpenSearch 3.0.0 開始，當您將 `plugins.calcite.enabled` 設定為 `true` 時，`explain` 回應會提供有關查詢執行計畫的增強資訊。此 API 支援四種輸出格式：

- `standard`：顯示邏輯與實體計畫 (未指定時的預設值)
- `simple`：顯示不含屬性的邏輯計畫
- `cost`：顯示邏輯與實體計畫及其成本
- `extended`：顯示邏輯與實體計畫及產生的程式碼

### 範例

下列範例示範不同的 `explain` 查詢。

#### 基本 SQL 查詢

下列請求顯示基本的 SQL `explain` 查詢：

```json
POST _plugins/_sql/_explain
{
  "query": "SELECT firstname, lastname FROM accounts WHERE age > 20"
}
```
{% include copy.html %}


回應顯示查詢執行計畫：

```json
{
  "root": {
    "name": "ProjectOperator",
    "description": {
      "fields": "[firstname, lastname]"
    },
    "children": [
      {
        "name": "OpenSearchIndexScan",
        "description": {
          "request": """OpenSearchQueryRequest(indexName=accounts, sourceBuilder={"from":0,"size":200,"timeout":"1m","query":{"range":{"age":{"from":20,"to":null,"include_lower":false,"include_upper":true,"boost":1.0}}},"_source":{"includes":["firstname","lastname"],"excludes":[]},"sort":[{"_doc":{"order":"asc"}}]}, searchDone=false)"""
        },
        "children": []
      }
    ]
  }
}
```

#### 使用 Calcite 引擎的進階查詢

下列請求示範使用 Calcite 引擎的更複雜查詢：

```json
POST _plugins/_ppl/_explain
{
  "query" : "source=state_country | where country = 'USA' OR country = 'England' | stats count() by country"
}
```
{% include copy.html %}


回應以標準格式顯示邏輯與實體計畫：

```json
{
  "calcite": {
    "logical": """LogicalProject(count()=[$1], country=[$0])
  LogicalAggregate(group=[{1}], count()=[COUNT()])
    LogicalFilter(condition=[SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7))])
      CalciteLogicalIndexScan(table=[[OpenSearch, state_country]])
""",
    "physical": """EnumerableCalc(expr#0..1=[{inputs}], count()=[$t1], country=[$t0])
  CalciteEnumerableIndexScan(table=[[OpenSearch, state_country]], PushDownContext=[[FILTER->SEARCH($1, Sarg['England', 'USA':CHAR(7)]:CHAR(7)), AGGREGATION->rel#53:LogicalAggregate.NONE.[](input=RelSubset#43,group={1},count()=COUNT())], OpenSearchRequestBuilder(sourceBuilder={"from":0,"size":0,"timeout":"1m","query":{"terms":{"country":["England","USA"],"boost":1.0}},"sort":[{"_doc":{"order":"asc"}}],"aggregations":{"composite_buckets":{"composite":{"size":1000,"sources":[{"country":{"terms":{"field":"country","missing_bucket":true,"missing_order":"first","order":"asc"}}}]},"aggregations":{"count()":{"value_count":{"field":"_index"}}}}}}, requestedTotalSize=10000, pageSize=null, startFrom=0)])
"""
  }
}
```

若要取得查詢計畫的簡化檢視，您可以使用 `simple` 格式：

```json
POST _plugins/_ppl/_explain?format=simple
{
  "query" : "source=state_country | where country = 'USA' OR country = 'England' | stats count() by country"
}
```
{% include copy-curl.html %}

回應顯示精簡的邏輯計畫：

```json
{
  "calcite": {
    "logical": """LogicalProject
  LogicalAggregate
    LogicalFilter
      CalciteLogicalIndexScan
"""
  }
}
```

對於需要後續處理的查詢，`explain` 回應除了 OpenSearch DSL 之外還會包含查詢計畫。對於不需要後續處理的查詢，您只會看到完整的 DSL。

## 分頁結果

若要取得分頁回應，請使用 `fetch_size` 參數。`fetch_size` 的值應大於 0。預設值為 1,000。值為 0 會退回非分頁回應。

`fetch_size` 參數僅支援 `jdbc` 回應格式。
{: .note }

### 範例

下列請求包含 SQL 查詢，並指定一次傳回五筆結果：

```json
POST _plugins/_sql/
{
  "fetch_size" : 5,
  "query" : "SELECT firstname, lastname FROM accounts WHERE age > 20 ORDER BY state ASC"
}
```
{% include copy-curl.html %}

回應包含不含 `fetch_size` 的查詢會包含的所有欄位，以及一個用於擷取後續結果頁面的 `cursor` 欄位：

```json
{
  "schema": [
    {
      "name": "firstname",
      "type": "text"
    },
    {
      "name": "lastname",
      "type": "text"
    }
  ],
  "cursor": "d:eyJhIjp7fSwicyI6IkRYRjFaWEo1UVc1a1JtVjBZMmdCQUFBQUFBQUFBQU1XZWpkdFRFRkZUMlpTZEZkeFdsWnJkRlZoYnpaeVVRPT0iLCJjIjpbeyJuYW1lIjoiZmlyc3RuYW1lIiwidHlwZSI6InRleHQifSx7Im5hbWUiOiJsYXN0bmFtZSIsInR5cGUiOiJ0ZXh0In1dLCJmIjo1LCJpIjoiYWNjb3VudHMiLCJsIjo5NTF9",
  "total": 956,
  "datarows": [
    [
      "Cherry",
      "Carey"
    ],
    [
      "Lindsey",
      "Hawkins"
    ],
    [
      "Sargent",
      "Powers"
    ],
    [
      "Campos",
      "Olsen"
    ],
    [
      "Savannah",
      "Kirby"
    ]
  ],
  "size": 5,
  "status": 200
}
```

若要擷取後續頁面，請使用上一個回應中的 `cursor`：

```json
POST /_plugins/_sql
{
   "cursor": "d:eyJhIjp7fSwicyI6IkRYRjFaWEo1UVc1a1JtVjBZMmdCQUFBQUFBQUFBQU1XZWpkdFRFRkZUMlpTZEZkeFdsWnJkRlZoYnpaeVVRPT0iLCJjIjpbeyJuYW1lIjoiZmlyc3RuYW1lIiwidHlwZSI6InRleHQifSx7Im5hbWUiOiJsYXN0bmFtZSIsInR5cGUiOiJ0ZXh0In1dLCJmIjo1LCJpIjoiYWNjb3VudHMiLCJsIjo5NTF9"
}
```
{% include copy-curl.html %}

下一個回應只包含結果的 `datarows` 以及新的 `cursor`。

```json
{
  "cursor": "d:eyJhIjp7fSwicyI6IkRYRjFaWEo1UVc1a1JtVjBZMmdCQUFBQUFBQUFBQU1XZWpkdFRFRkZUMlpTZEZkeFdsWnJkRlZoYnpaeVVRPT0iLCJjIjpbeyJuYW1lIjoiZmlyc3RuYW1lIiwidHlwZSI6InRleHQifSx7Im5hbWUiOiJsYXN0bmFtZSIsInR5cGUiOiJ0ZXh0In1dLCJmIjo1LCJpIjoiYWNjb3VudHMabcde12345",
  "datarows": [
    [
      "Abbey",
      "Karen"
    ],
    [
      "Chen",
      "Ken"
    ],
    [
      "Ani",
      "Jade"
    ],
    [
      "Peng",
      "Hu"
    ],
    [
      "John",
      "Doe"
    ]
  ]
}
```

若巢狀欄位被扁平化，`datarows` 可能會有超過 `fetch_size` 筆記錄。
{: .note }

最後一頁結果只有 `datarows`，沒有 `cursor`。`cursor` 內容會在最後一頁自動清除。

若要明確清除游標內容，請使用 `_plugins/_sql/close` 端點操作：

```json
POST /_plugins/_sql/close
{
   "cursor": "d:eyJhIjp7fSwicyI6IkRYRjFaWEo1UVc1a1JtVjBZMmdCQUFBQUFBQUFBQU1XZWpkdFRFRkZUMlpTZEZkeFdsWnJkRlZoYnpaeVVRPT0iLCJjIjpbeyJuYW1lIjoiZmlyc3RuYW1lIiwidHlwZSI6InRleHQifSx7Im5hbWUiOiJsYXN0bmFtZSIsInR5cGUiOiJ0ZXh0In1kLCJmIjo1LCJpIjoiYWNjb3VudHMiLCJsIjo5NTF9"
}
```
{% include copy-curl.html %}

回應是來自 OpenSearch 的確認：

```json
{"succeeded":true}
```

## 篩選結果

您可以使用 `filter` 參數，直接將更多條件新增至 OpenSearch DSL。

下列 SQL 查詢會傳回所有客戶的名稱與帳戶餘額。接著會篩選結果，只包含餘額低於 $10,000 的客戶。

```json
POST /_plugins/_sql/
{
  "query" : "SELECT firstname, lastname, balance FROM accounts",
  "filter" : {
    "range" : {
      "balance" : {
        "lt" : 10000
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含相符的結果：

```json
{
  "schema": [
    {
      "name": "firstname",
      "type": "text"
    },
    {
      "name": "lastname",
      "type": "text"
    },
    {
      "name": "balance",
      "type": "long"
    }
  ],
  "total": 2,
  "datarows": [
    [
      "Hattie",
      "Bond",
      5686
    ],
    [
      "Dale",
      "Adams",
      4180
    ]
  ],
  "size": 2,
  "status": 200
}
```

您可以使用 Explain API 查看此查詢如何對 OpenSearch 執行：

```json
POST /_plugins/_sql/_explain
{
  "query" : "SELECT firstname, lastname, balance FROM accounts",
  "filter" : {
    "range" : {
      "balance" : {
        "lt" : 10000
      }
    }
  }
}
```
{% include copy-curl.html %}

回應包含 OpenSearch DSL 中對應前述查詢的布林值查詢：

```json
{
  "from": 0,
  "size": 200,
  "query": {
    "bool": {
      "filter": [{
        "bool": {
          "filter": [{
            "range": {
              "balance": {
                "from": null,
                "to": 10000,
                "include_lower": true,
                "include_upper": false,
                "boost": 1.0
              }
            }
          }],
          "adjust_pure_negative": true,
          "boost": 1.0
        }
      }],
      "adjust_pure_negative": true,
      "boost": 1.0
    }
  },
  "_source": {
    "includes": [
      "firstname",
      "lastname",
      "balance"
    ],
    "excludes": []
  }
}
```

## 使用參數

您可以使用 `parameters` 欄位，將參數值傳遞至已備妥的 SQL 查詢。

下列 explain 操作使用帶有 `age` 參數的 SQL 查詢：

```json
POST /_plugins/_sql/_explain
{
  "query": "SELECT * FROM accounts WHERE age = ?",
  "parameters": [{
    "type": "integer",
    "value": 30
  }]
}
```
{% include copy-curl.html %}

回應包含 OpenSearch DSL 中對應前述 SQL 查詢的布林值查詢：

```json
{
  "from": 0,
  "size": 200,
  "query": {
    "bool": {
      "filter": [{
        "bool": {
          "must": [{
            "term": {
              "age": {
                "value": 30,
                "boost": 1.0
              }
            }
          }],
          "adjust_pure_negative": true,
          "boost": 1.0
        }
      }],
      "adjust_pure_negative": true,
      "boost": 1.0
    }
  }
}

```