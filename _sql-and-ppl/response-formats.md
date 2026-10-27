---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "回應格式"
nav_order: 2
redirect_from:
  - /search-plugins/sql/response-formats/
---

# SQL 和 PPL 查詢回應格式

OpenSearch 為 SQL 和 PPL 查詢提供 `jdbc`、`csv` 和 `raw` 回應格式，各自適用於不同用途。`jdbc` 格式廣泛使用，因為它提供結構描述資訊，並新增分頁等更多功能。除了 JDBC 驅動程式之外，各種用戶端也能受益於詳細且格式良好的回應。

## JDBC 格式

預設情況下，SQL 外掛程式會以標準 JDBC 格式傳回回應。此格式是為 JDBC 驅動程式以及需要結構描述與結果集都格式良好的用戶端所提供。

#### 範例請求

下列查詢未指定回應格式，因此格式設定為 `jdbc`：

```json
POST _plugins/_sql
{
  "query" : "SELECT firstname, lastname, age FROM accounts ORDER BY age LIMIT 2"
}
```
{% include copy-curl.html %}

#### 範例回應

在回應中，`schema` 包含欄位名稱與類型，`datarows` 欄位則包含結果集：

```json
{
  "schema": [{
      "name": "firstname",
      "type": "text"
    },
    {
      "name": "lastname",
      "type": "text"
    },
    {
      "name": "age",
      "type": "long"
    }
  ],
  "total": 4,
  "datarows": [
    [
      "Nanette",
      "Bates",
      28
    ],
    [
      "Amber",
      "Duke",
      32
    ]
  ],
  "size": 2,
  "status": 200
}
```

如果發生任何類型的錯誤，OpenSearch 會傳回錯誤訊息。

下列查詢搜尋不存在的欄位 `unknown`：

```json
POST /_plugins/_sql
{
  "query" : "SELECT unknown FROM accounts"
}
```
{% include copy-curl.html %}

回應包含錯誤訊息與錯誤原因：

```json
{
  "error": {
    "reason": "Invalid SQL query",
    "details": "Field [unknown] cannot be found or used here.",
    "type": "SemanticAnalysisException"
  },
  "status": 400
}
```

## CSV 格式

您也可以指定以 CSV 格式傳回結果。

#### 範例請求

```json
POST /_plugins/_sql?format=csv
{
  "query" : "SELECT firstname, lastname, age FROM accounts ORDER BY age"
}
```
{% include copy-curl.html %}

#### 範例回應

```text
firstname,lastname,age
Nanette,Bates,28
Amber,Duke,32
Dale,Adams,33
Hattie,Bond,36
```
### 清理 CSV 格式的結果

預設情況下，OpenSearch 會依據下列規則清理標題儲存格 (欄位名稱) 與資料儲存格 (欄位內容)：

- 如果儲存格以 `+`、`-`、`=` 或 `@` 開頭，清理器會在儲存格開頭插入單引號 (`'`)。
- 如果儲存格包含一或多個逗號 (`,`)，清理器會以雙引號 (`"`) 包圍該儲存格。

### 範例

下列查詢將一份文件編製索引，其儲存格以特殊字元開頭或包含逗號：

```json
PUT /userdata/_doc/1?refresh=true
{
  "+firstname": "-Hattie",
  "=lastname": "@Bond",
  "address": "671 Bristol Street, Dente, TN"
}
```
{% include copy-curl.html %}

您可以使用下列查詢以 CSV 格式請求結果：

```json
POST /_plugins/_sql?format=csv
{
  "query" : "SELECT * FROM userdata"
}
```
{% include copy-curl.html %}

在回應中，以特殊字元開頭的儲存格會加上 `'` 前綴。包含逗號的儲存格會以引號包圍：

```text
'+firstname,'=lastname,address
'Hattie,'@Bond,"671 Bristol Street, Dente, TN"
```

若要略過清理，請將 `sanitize` 查詢參數設定為 false：

```json
POST /_plugins/_sql?format=csvandsanitize=false
{
  "query" : "SELECT * FROM userdata"
}
```
{% include copy-curl.html %}

回應包含原始 CSV 格式的結果：

```text
=lastname,address,+firstname
@Bond,"671 Bristol Street, Dente, TN",-Hattie
```

## Raw 格式

您可以使用 raw 格式將結果導向其他命令列工具進行後續處理。

#### 範例請求

```json
POST /_plugins/_sql?format=raw
{
  "query" : "SELECT firstname, lastname, age FROM accounts ORDER BY age"
}
```
{% include copy-curl.html %}

#### 範例回應

```text
Nanette|Bates|28
Amber|Duke|32
Dale|Adams|33
Hattie|Bond|36
```

預設情況下，OpenSearch 會依據下列規則清理 `raw` 格式的結果：

- 如果資料儲存格包含一或多個直立線字元 (`|`)，清理器會以雙引號包圍該儲存格。

### 範例

下列查詢將欄位中包含直立線字元 (`|`) 的文件編製索引：

```json
PUT /userdata/_doc/1?refresh=true
{
  "+firstname": "|Hattie",
  "=lastname": "Bond|",
  "|address": "671 Bristol Street| Dente| TN"
}
```
{% include copy-curl.html %}

您可以使用下列查詢以 `raw` 格式請求結果：

```json
POST /_plugins/_sql?format=raw
{
  "query" : "SELECT * FROM userdata"
}
```
{% include copy-curl.html %}

查詢傳回含有 `|` 字元的儲存格，並以雙引號包圍整個儲存格：

```text
"|address"|=lastname|+firstname
"671 Bristol Street| Dente| TN"|"Bond|"|"|Hattie"
```