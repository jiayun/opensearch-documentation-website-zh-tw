---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "正規表示式語法"
nav_order: 95
---

# 正規表示式語法

[正規表示式](https://en.wikipedia.org/wiki/Regular_expression) (regex) 是一種使用特殊符號與運算子定義搜尋模式的方式。這些模式可讓您比對字串中的字元序列。

在 OpenSearch 中，您可以在下列查詢類型中使用正規表示式：

* [`regexp`]({{site.url}}{{site.baseurl}}/query-dsl/term/regexp/)
* [`query_string`]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)

OpenSearch 使用 [Apache Lucene](https://lucene.apache.org/core/) regex 引擎，該引擎有其專屬的語法與限制。它**不**使用 [Perl Compatible Regular Expressions (PCRE)](https://en.wikipedia.org/wiki/Perl_Compatible_Regular_Expressions)，因此某些您熟悉的 regex 功能可能行為不同或不受支援。
{: .note}

## 在 regexp 與 query_string 查詢之間做選擇

`regexp` 與 `query_string` 查詢都支援正規表示式，但它們的行為不同，且適用於不同的使用情境。

| 功能                   | `regexp` 查詢                                     | `query_string` 查詢                                |
| ------------------------- | -------------------------------------------------- | --------------------------------------------------- |
| 模式比對   | Regex 模式必須符合整個欄位值            | Regex 模式可以符合欄位的任何部分                  |
| `flags` 支援           | `flags` 會啟用選用的 regex 運算子                 | `flags` 不支援                        |
| 查詢類型                   | 詞彙層級查詢 (不計分)       | 全文查詢 (計分並剖析)           |
| 最佳使用情境             | 對 keyword 或精確欄位進行嚴格的模式比對 | 使用支援 regex 模式的彈性查詢字串，在已分析的欄位內搜尋       |
| 複雜查詢組合 | 僅限於 regex 模式                         | 支援 `AND`、`OR`、萬用字元、欄位、加權及其他功能。請參閱 [查詢字串查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。 |


## 保留字元

Lucene 的 regex 引擎支援所有 Unicode 字元。不過，下列字元會被視為特殊運算子：

```
. ? + * | { } [ ] ( ) " \
```

視啟用的 `flags` (其指定了[選用運算子](#optional-operators)) 而定，下列字元也可能會被保留：

```
@ & ~ < >
```

若要依字面比對這些字元，請使用反斜線 (`\`) 將其逸出，或將整個字串以雙引號括住：

- `\&`：比對字面上的 `&`
- `\\`：比對字面上的反斜線 (`\`)
- `"hello@world"`：比對完整字串 `hello@world`


## 標準 regex 運算子

Lucene 支援一組核心的 regex 運算子：

- `.` – 比對任何單一字元。**範例**：`f.n` 比對 `f` 後接任何字元，再接 `n` (例如 `fan` 或 `fin`)。

- `?` – 比對前置字元的零個或一個。**範例**：`colou?r` 比對 `color` 與 `colour`。

- `+` – 比對前置字元的一個或多個。**範例**：`go+` 比對 `g` 後接一個或多個 `o` (`go`、`goo`、`gooo` 等)。

- `*` – 比對前置字元的零個或多個。**範例**：`lo*se` 比對 `l` 後接零個或多個 `o`，再接 `se` (`lse`、`lose`、`loose`、`loooose` 等)。

- `{min,max}` – 比對特定範圍的重複次數。若省略 `max`，則比對的字元數沒有上限。**範例**：`x{3}` 比對恰好 3 個 `x` (`xxx`)；`x{2,4}` 比對 2 到 4 個 `x` (`xx`、`xxx` 或 `xxxx`)；`x{3,}` 比對 3 個或更多 `x` (`xxx`、`xxxx`、`xxxxx` 等)。

- `|` – 做為邏輯 `OR`。**範例**：`apple|orange` 比對 `apple` 或 `orange`。

- `( )` – 將字元分組為子模式。**範例**：`ab(cd)?` 比對 `ab` 與 `abcd`。

- `[ ]` – 從一組字元或範圍中比對一個字元。**範例**：`[aeiou]` 比對任何母音。
    - `-` – 在方括號內提供時，表示一個範圍，除非被逸出或是方括號內的第一個字元。**範例**：`[a-z]` 比對任何小寫字母；`[-az]` 比對 `-`、`a` 或 `z`；`[a\\-z]` 比對 `a`、`-` 或 `z`。
    - `^` – 在方括號內提供時，做為邏輯 `NOT`，將字元範圍或集合中的任何字元取反。**範例**：`[^az]` 比對除了 `a` 或 `z` 以外的任何字元；`[^a-z]` 比對除了小寫字母以外的任何字元；`[^-az]` 比對除了 `-`、`a` 與 `z` 以外的任何字元；`[^a\\-z]` 比對除了 `a`、`-` 與 `z` 以外的任何字元。


## 選用運算子

您可以使用 `flags` 參數啟用其他 regex 運算子。請以 `|` 分隔多個旗標。

以下是可用的旗標：

- `ALL` (預設) – 啟用所有選用運算子。

{% comment %}
<!-- COMPLEMENT is deprecated and doesn't work. Leaving it here until https://github.com/opensearch-project/OpenSearch/issues/18397 is resolved. -->
{% endcomment %}

- `COMPLEMENT` – 啟用 `~`，其會將最短的後續表達式取反。**範例**：`d~ef` 比對 `dgf`、`dxf`，但不比對 `def`。

- `INTERSECTION` – 啟用 `&` 做為 `AND` 邏輯運算子。**範例**：`ab.+&.+cd` 比對開頭為 `ab` 且結尾為 `cd` 的字串。

- `INTERVAL` – 啟用 `<min-max>` 語法以比對數值範圍。**範例**：`id<10-12>` 比對 `id10`、`id11` 與 `id12`。

- `ANYSTRING` – 啟用 `@` 以比對任何字串。您可以將其與 `~` 及 `&` 結合以進行排除。**範例**：`@&.*error.*&.*[0-9]{3}.*` 比對同時包含「error」一詞與三個數字序列的字串。

## 不支援的功能

Lucene 的引擎不支援下列常用的 regex 錨點：

- `^` – 行開頭
- `$` – 行結尾

取而代之的是，您的模式必須符合整個字串才能產生比對。

## 範例

若要試用正規表示式，請將下列文件編製索引至 `logs` 索引：

```json
PUT /logs/_doc/1
{
  "message": "error404"
}
```
{% include copy-curl.html %}

```json
PUT /logs/_doc/2
{
  "message": "error500"
}
```
{% include copy-curl.html %}

```json
PUT /logs/_doc/3
{
  "message": "error1a"
}
```
{% include copy-curl.html %}

### 範例：包含正規表示式的基本查詢

下列 `regexp` 查詢會傳回 `message` 欄位的整個值符合「error」後接一個或多個數字之模式的文件。若某個值僅以子字串形式包含該模式，則不符合：

```json
GET /logs/_search
{
  "query": {
    "regexp": {
      "message": {
        "value": "error[0-9]+"
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢比對 `error404` 與 `error500`：


```json
{
  "took": 28,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 1,
        "_source": {
          "message": "error404"
        }
      },
      {
        "_index": "logs",
        "_id": "2",
        "_score": 1,
        "_source": {
          "message": "error500"
        }
      }
    ]
  }
}
```

### 範例：使用選用運算子

下列查詢會比對 `message` 欄位完全符合以「error」開頭、後接 400 到 500 (含) 之間數字的字串之文件。`INTERVAL` 旗標會啟用 `<min-max>` 語法以表示數值範圍：

```json
GET /logs/_search
{
  "query": {
    "regexp": {
      "message": {
        "value": "error<400-500>",
        "flags": "INTERVAL"
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢比對 `error404` 與 `error500`：

```json
{
  "took": 22,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 1,
        "_source": {
          "message": "error404"
        }
      },
      {
        "_index": "logs",
        "_id": "2",
        "_score": 1,
        "_source": {
          "message": "error500"
        }
      }
    ]
  }
}
```

### 範例：使用 ANYSTRING

啟用 `ANYSTRING` 旗標時，`@` 運算子會比對整個字串。這與交集 (`&`) 結合時很有用，因為它可讓您建構在特定條件下比對完整字串的查詢。

下列查詢會比對同時包含「error」一詞與三個數字序列的訊息。使用 `ANYSTRING` 來斷言整個欄位必須符合兩個模式的交集：

```json
GET /logs/_search
{
  "query": {
    "regexp": {
      "message.keyword": {
        "value": "@&.*error.*&.*[0-9]{3}.*",
        "flags": "ANYSTRING|INTERSECTION"
      }
    }
  }
}
```
{% include copy-curl.html %}

此查詢比對 `error404` 與 `error500`：

```json
{
  "took": 20,
  "timed_out": false,
  "_shards": {
    "total": 1,
    "successful": 1,
    "skipped": 0,
    "failed": 0
  },
  "hits": {
    "total": {
      "value": 2,
      "relation": "eq"
    },
    "max_score": 1,
    "hits": [
      {
        "_index": "logs",
        "_id": "1",
        "_score": 1,
        "_source": {
          "message": "error404"
        }
      },
      {
        "_index": "logs",
        "_id": "2",
        "_score": 1,
        "_source": {
          "message": "error500"
        }
      }
    ]
  }
}
```

請注意，此查詢也會比對 `xerror500`、`error500x` 與 `errorxx500`。