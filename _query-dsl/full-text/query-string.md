---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "查詢字串"
parent: Full-text queries
nav_order: 80
redirect_from:
  - /opensearch/query-dsl/full-text/query-string/
  - /query-dsl/query-dsl/full-text/query-string/
---

# 查詢字串查詢

`query_string` 查詢會根據[查詢字串語法](#query-string-syntax)剖析查詢字串。它可用於建立功能強大卻精簡的查詢，這些查詢可以納入萬用字元並搜尋多個欄位。

使用 `query_string` 查詢進行搜尋不會傳回巢狀文件。若要搜尋巢狀欄位，請使用 [`nested` 查詢]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/)。
{: .note}

查詢字串查詢具有嚴格的語法，若語法無效會傳回錯誤。因此，它不適合用於搜尋方塊應用程式。若需要較寬鬆的替代方案，請考慮使用 [`simple_query_string` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/simple-query-string/)。如果您不需要查詢語法支援，請使用 [`match` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match/)。
{: .important}

## 查詢字串語法

查詢字串語法是以 [Apache Lucene 查詢語法](https://lucene.apache.org/core/{{site.lucene_version}}/queryparser/org/apache/lucene/queryparser/classic/package-summary.html#package.description)為基礎。

您可以在下列情況使用查詢字串語法：

1. 在 `query_string` 查詢中，例如：
    ```json
    GET _search
    {
      "query": {
        "query_string": {
          "query": "the wind AND (rises OR rising)"
        }
      }
    }
    ```
    {% include copy-curl.html %}

1. 在 OpenSearch Dashboards 的 Discover 或 Dashboard 應用程式中，如果您關閉 DQL，如下圖所示。
  ![在 OpenSearch Dashboards Discover 中使用查詢字串語法]({{site.url}}{{site.baseurl}}/images/discover-lucene-syntax.png)
  
    DQL 與查詢字串查詢 (Lucene) 語言是 Discover 和 Dashboards 中兩個搜尋列語言選項。若要比較這些語言選項，請參閱 [DQL 與查詢字串查詢快速參考]({{site.url}}{{site.baseurl}}/dashboards/dql/#dql-and-query-string-query-quick-reference)。 
    {: .tip}

1. 如果您使用 HTTP 請求查詢參數進行搜尋，例如： 
  ```json
    GET _search?q=wind
  ```

查詢字串是由_詞彙_和_運算子_組成。詞彙是單一單字 (例如，在查詢 `wind rises` 中，詞彙是 `wind` 和 `rises`)。如果多個詞彙被引號包圍，它們會被視為一個詞組，其中的單字會依出現順序進行比對 (例如，`"wind rises"`)。運算子 (例如 `OR`、`AND` 和 `NOT`) 會指定用於解譯查詢字串中文字的布林邏輯。 

本節的範例使用包含下列對應和文件的索引：

```json
PUT /testindex
{
  "mappings": {
    "properties": {
      "title": { 
        "type": "text",
        "fields": {
          "english": { 
            "type": "text",
            "analyzer": "english"
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/1
{
  "title": "The wind rises"
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/2
{
  "title": "Gone with the wind",
  "description": "A 1939 American epic historical film"
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/3
{
  "title": "Windy city"
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/4
{
  "article title": "Wind turbines"
}
```
{% include copy-curl.html %}

## 保留字元

以下是查詢字串查詢的保留字元清單： 

`+`、`-`、`=`、`&&`、`||`、`>`、`<`、`!`、`(`、`)`、`{`、`}`、`[`、`]`、`^`、`"`、`~`、`*`、`?`、`:`、`\`、`/`

使用反斜線 (`\`) 逸出保留字元。傳送 JSON 請求時，請使用雙反斜線 (`\\`) 來逸出保留字元 (因為反斜線字元本身即為保留字元，您必須使用另一個反斜線來逸出反斜線)。 
{: .tip}

例如，若要搜尋運算式 `2*3`，請指定查詢字串：`2\\*3`：

```json
GET /testindex/_search
{
 "query": {
    "query_string": {
      "query": "title: 2\\*3"
    }
  }
}
```
{% include copy-curl.html %}

`>` 和 `<` 符號無法逸出。它們會被解譯為範圍查詢。 
{: .important}

## 空白字元和空查詢

空白字元不會被視為運算子。如果查詢字串為空或僅包含空白字元，查詢不會傳回結果。

## 欄位名稱

在冒號前指定欄位名稱。下表包含帶有欄位名稱的範例查詢。

`query_string` 查詢中的查詢 | Discover 中的查詢 | 文件相符的準則 | `testindex` 索引中的相符文件
:--- | :--- | :--- | :---
`title: wind` | `title: wind` | `title` 欄位包含單字 `wind`。 | 1、2
`title: (wind OR windy)` | `title: (wind OR windy)` | `title` 欄位包含單字 `wind` 或單字 `windy`。 | 1、2、3
`title: \"wind rises\"` | `title: "wind rises"` | `title` 欄位包含詞組 `wind rises`。使用反斜線逸出引號。 | 1
`article\\ title: wind` | `article\ title: wind` | `article title` 欄位包含單字 `wind`。使用反斜線逸出空格字元。 | 4
`title.\\*: rise` | `title.\*: rise` | 每個以 `title.` 開頭的欄位 (在此範例中為 `title.english`) 都包含單字 `rise`。使用反斜線逸出萬用字元。 | 1
`_exists_: description` | `_exists_: description` | 欄位 `description` 存在。 | 2

## 萬用字元運算式

您可以使用特殊字元指定萬用字元運算式：`?` 會取代單一字元，而 `*` 會取代零個或多個字元。

#### 範例

下列查詢會搜尋標題包含單字 `gone` 且描述包含以 `hist` 開頭之單字的文件：

```json
GET /testindex/_search
{
 "query": {
    "query_string": {
      "query": "title: gone AND description: hist*"
    }
  }
}
```
{% include copy-curl.html %}

萬用字元查詢可能會使用大量記憶體，進而降低效能。位於單字開頭的萬用字元 (例如 `*cal`) 成本最高，因為在該類萬用字元上比對文件需要檢查索引中的所有詞彙。若要停用前置萬用字元，請將 `allow_leading_wildcard` 設為 `false`。
{: .warning}

為了提升效率，`*` 這類純萬用字元會改寫為 `exists` 查詢。因此，`description: *` 萬用字元會比對 `description` 欄位中包含空字串值的文件，但不會比對 `description` 欄位遺漏或具有 `null` 值的文件。

如果您將 `analyze_wildcard` 設為 `true`，OpenSearch 會分析以 `*` 結尾的查詢 (例如 `hist*`)。因此，OpenSearch 會建立一個布林查詢，其中包含對前 n-1 個詞元進行完全相符，以及對最後一個詞元進行前置字元相符所產生的詞元。

## 正規表示式

若要在查詢字串中指定正規表示式模式，請以正斜線 (`/`) 包圍它們，例如 `title: /w[a-z]nd/`。

`allow_leading_wildcard` 參數不適用於正規表示式。例如，`/.*d/` 這類查詢字串會檢查索引中的所有詞彙。 
{: .important}

## 模糊比對

您可以使用 `~` 運算子執行模糊查詢，例如 `title: rise~`。

此查詢會搜尋包含與搜尋詞彙在允許的最大編輯距離內相似之詞彙的文件。編輯距離定義為 [Damerau-Levenshtein 距離](https://en.wikipedia.org/wiki/Damerau%E2%80%93Levenshtein_distance)，用於衡量將一個詞彙變更為另一個詞彙所需的單一字元變更次數 (插入、刪除、取代或調換)。

預設編輯距離 2 應可涵蓋 80% 的拼字錯誤。若要變更預設編輯距離，請在 `~` 運算子後指定新的編輯距離。例如，若要將編輯距離設為 `1`，請使用查詢 `title: rise~1`。

請勿混用模糊和萬用字元運算子。如果您同時指定模糊和萬用字元運算子，其中一個運算子將不會套用。例如，如果您可以搜尋 `wnid*~1`，則會套用萬用字元運算子 `*`，但不會套用模糊運算子 `~1`。
{: .important}

## 鄰近查詢

鄰近查詢不要求搜尋片語必須依照指定的順序排列。它允許片語中的詞以不同的順序出現，或由其他詞分隔。鄰近查詢會指定片語中詞的最大編輯距離。例如，下列查詢在比對指定片語中的詞時，允許編輯距離為 4：

```json
GET /testindex/_search
{
 "query": {
    "query_string": {
      "query": "title: \"wind gone\"~4"
    }
  }
}
```
{% include copy-curl.html %}

當 OpenSearch 比對文件時，文件中的詞愈接近查詢中指定的詞序（編輯距離愈小），文件的相關性分數就愈高。  

## 範圍

若要為數值、字串或日期欄位指定範圍，請使用方括號 (`[min TO max]`) 表示包含範圍，並使用大括號 (`{min TO max}`) 表示排除範圍。您也可以混用方括號與大括號，以包含或排除下限與上限（例如 `{min TO max]`）。 

日期範圍的日期必須以您對應包含該日期的欄位時所使用的格式提供。如需支援的日期格式詳細資訊，請參閱[格式]({{site.url}}{{site.baseurl}}/opensearch/supported-field-types/date/#formats)。

下表提供範圍語法的範例。

資料類型 | 查詢 | 查詢字串
:--- | :--- | :---
數值 | 帳號從 1 到 15（含）的文件。 | `account_number: [1 TO 15]` 或 <br> `account_number: (>=1 AND <=15)` 或 <br> `account_number: (+>=1 +<=15)`
| 帳號為 15 及以上的文件。 | `account_number: [15 TO *]` 或 <br> `account_number: >=15`（請注意 `>=` 符號後沒有空格）
字串 | 姓氏從 Bates（含）到 Duke（不含）的文件。 | `lastname: [Bates TO Duke}` 或 <br> `lastname: (>=Bates AND <Duke)`
| 姓氏依字母順序排在 Bates 之前的文件。 | `lastname: {* TO Bates}` 或 <br> `lastname: <Bates`（請注意 `<` 符號後沒有空格）
日期 | 發行日期介於 03/21/2023 與 09/25/2023 之間（含）的文件。 | `release_date: [03/21/2023 TO 09/25/2023]`

除了在查詢字串中指定範圍之外，您也可以使用[範圍查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/range/)，它提供更可靠的語法。
{: .tip}

## 提升

使用插入號 (`^`) 提升運算子，以乘數提升文件的相關性分數。[0, 1) 範圍內的值會降低相關性，而大於 1 的值會提高相關性。預設值為 `1`。 

下表提供提升的範例。

類型 | 說明 | 查詢字串
:--- | :--- | :---
詞提升 | 尋找所有包含詞 `street` 的地址，並提升包含詞 `Madison` 的地址。 | `address: Madison^2 street`
片語提升 | 尋找標題包含片語 `wind rises` 的文件，並提升 2 倍。 | `title: \"wind rises\"^2` 
| 尋找標題包含詞 `wind rises` 的文件，並將包含片語 `wind rises` 的文件提升 2 倍。 | `title: (wind rises)^2`

## 布林運算子

當您在查詢中提供搜尋詞時，依預設，查詢會傳回至少包含其中一個所提供詞的文件。您可以使用 `default_operator` 參數為所有詞指定運算子。因此，如果您將 `default_operator` 設為 `AND`，則所有詞都是必要的；而如果您將它設為 `OR`，則所有詞都是選用的。 

### `+` 與 `-` 運算子

如果您想要更精細地控制必要與選用的詞，可以使用 `+` 與 `-` 運算子。`+` 運算子會使其後的詞成為必要，而 `-` 運算子則會排除其後的詞。

例如，在查詢字串 `title: (gone +wind -turbines)` 中，指定詞 `gone` 為選用、詞 `wind` 必須存在，且詞 `turbines` 不得存在於相符文件的標題中：

```json
GET /testindex/_search
{
 "query": {
    "query_string": {
      "query": "title: (gone +wind -turbines)"
    }
  }
}
```
{% include copy-curl.html %}

此查詢會傳回兩份相符的文件：

```json
{
  "_index": "testindex",
  "_id": "2",
  "_score": 1.3159468,
  "_source": {
    "title": "Gone with the wind",
    "description": "A 1939 American epic historical film"
  }
},
{
  "_index": "testindex",
  "_id": "1",
  "_score": 0.3438858,
  "_source": {
    "title": "The wind rises"
  }
}
```

上述查詢等同於下列布林查詢：

```json
GET testindex/_search
{
  "query": {
    "bool": {
      "must": {
        "match": {
          "title": "wind"
        }
      },
      "should": {
        "match": {
          "title": "gone"
        }
      },
      "must_not": {
        "match": {
          "title": "turbines"
        }
      }
    }
  }
}
```

### 傳統布林運算子

或者，您可以使用下列布林運算子：`AND`、`&&`、`OR`、`||`、`NOT`、`!`。不過，這些運算子不遵循優先順序規則，因此當您使用多個布林運算子時，必須使用括號來指定優先順序。例如，查詢字串 `title: (gone +wind -turbines)` 可以使用布林運算子改寫如下：

`title: ((gone AND wind) OR wind) AND NOT turbines`

執行下列包含改寫後查詢字串的查詢：

```json
GET testindex/_search
{
 "query": {
    "query_string": {
      "query": "title: ((gone AND wind) OR wind) AND NOT turbines"
    }
  }
}
```
{% include copy-curl.html %}

此查詢傳回的結果與使用 `+` 與 `-` 運算子的查詢相同。不過請注意，相符文件的相關性分數與先前的結果不同：

```json
{
  "_index": "testindex",
  "_id": "2",
  "_score": 1.6166971,
  "_source": {
    "title": "Gone with the wind",
    "description": "A 1939 American epic historical film"
  }
},
{
  "_index": "testindex",
  "_id": "1",
  "_score": 0.3438858,
  "_source": {
    "title": "The wind rises"
  }
}
```
{% include copy-curl.html %}

### 分組

使用括號將多個子句或詞分組為子查詢。例如，下列查詢會搜尋標題中包含詞 `gone` 或 `rises`，且必須包含詞 `wind` 的文件：

```json
GET testindex/_search
{
 "query": {
    "query_string": {
      "query": "title: (gone OR rises) AND wind"
    }
  }
}
```

結果包含兩份相符的文件：

```json
{
  "_index": "testindex",
  "_id": "1",
  "_score": 1.5046883,
  "_source": {
    "title": "The wind rises"
  }
},
{
  "_index": "testindex",
  "_id": "2",
  "_score": 1.3159468,
  "_source": {
    "title": "Gone with the wind",
    "description": "A 1939 American epic historical film"
  }
}
```

您也可以使用分組來提升子查詢結果，或指定目標欄位，例如 `title:(gone AND wind) description:(historical film)^2`。

## 搜尋多個欄位

若要搜尋多個欄位，請使用 `fields` 參數。當您提供 `fields` 參數時，查詢會改寫為 `field_1: query OR field_2: query ...`。 

例如，下列查詢會在 `title` 與 `description` 欄位中搜尋詞 `wind` 或 `film`：

```json
GET testindex/_search
{
  "query": {
    "query_string": {
      "fields": [ "title", "description" ],
      "query": "wind AND film"
    }
  }
}
```
{% include copy-curl.html %}

上述查詢等同於下列未提供 `fields` 參數的查詢：

```json
GET testindex/_search
{
  "query": {
    "query_string": {
      "query": "(title:wind OR description:wind) AND (title:film OR description:film)"
    }
  }
}
```

### 搜尋欄位的多個子欄位

若要搜尋欄位的所有內部欄位，您可以使用萬用字元。例如，若要搜尋 `address` 欄位內的所有子欄位，請使用下列查詢：

```json
GET /testindex/_search
{
  "query": {
    "query_string" : {
      "fields" : ["address.*"],
      "query" : "New AND (York OR Jersey)"
    }
  }
}
```
{% include copy-curl.html %}

上述查詢等同於下列未提供 `fields` 參數的查詢 (請注意，`*` 已使用 `\\` 逸出)：

```json
GET /testindex/_search
{
  "query": {
    "query_string" : {
      "query" : "address.\\*: New AND (York OR Jersey)"
    }
  }
}
```

### 加權 (Boosting)

由每個搜尋詞彙產生的子查詢會使用帶有 `tie_breaker` 的 [`dis_max` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/) 來合併。若要對個別欄位加權，請使用 `^` 運算子。例如，下列查詢將 `title` 欄位加權 2 倍：

```json
GET testindex/_search
{
  "query": {
    "query_string": {
      "fields": [ "title^2", "description" ],
      "query": "wind AND film"
    }
  }
}
```
{% include copy-curl.html %}

若要對欄位的所有子欄位加權，請在萬用字元之後指定加權運算子：

```json
GET /testindex/_search
{
  "query": {
    "query_string" : {
      "fields" : ["work_address", "address.*^2"],
      "query" : "New AND (York OR Jersey)"
    }
  }
}
```

### 多欄位搜尋的參數

搜尋多個欄位時，您可以將額外的選用參數 `type` 傳遞給 `query_string` 查詢。

參數 | 資料類型 | 說明
:--- | :--- | :---
`type` | 字串 | 決定 OpenSearch 如何執行查詢並為結果評分。有效值為 `best_fields`、`bool_prefix`、`most_fields`、`cross_fields`、`phrase` 和 `phrase_prefix`。預設值為 `best_fields`。有效值的說明請參閱 [多重比對查詢類型]({{site.url}}{{site.baseurl}}/query-dsl/full-text/multi-match/#multi-match-query-types)。

## `query_string` 查詢中的同義詞

`query_string` 查詢支援使用 `synonym_graph` 詞元篩選器進行多詞彙同義詞擴展。如果您使用 `synonym_graph` 詞元篩選器，OpenSearch 會為每個同義詞建立 [片語比對查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。

`auto_generate_synonyms_phrase_query` 參數指定是否自動為多詞彙同義詞建立片語比對查詢。預設情況下，`auto_generate_synonyms_phrase_query` 為 `true`，因此如果您指定 `ml, machine learning` 作為同義詞並搜尋 `ml`，OpenSearch 會搜尋 `ml OR "machine learning"`。

或者，您可以使用連接詞來比對多詞彙同義詞。如果您將 `auto_generate_synonyms_phrase_query` 設定為 `false`，OpenSearch 會搜尋 `ml OR (machine AND learning)`。

例如，下列查詢搜尋文字 `ml models`，並指定不為每個同義詞自動產生片語比對查詢：

```json
GET /testindex/_search
{
  "query": {
    "query_string": {
      "default_field": "title",
      "query": "ml models",
      "auto_generate_synonyms_phrase_query": false
    }
  }
}
```
{% include copy-curl.html %}

對於此查詢，OpenSearch 會建立下列布林查詢：`(ml OR (machine AND learning)) models`。

## 最低相符數量

`query_string` 查詢會在每個運算子周圍分割查詢，並為整個輸入建立布林查詢。[`minimum_should_match` 參數]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/) 指定文件必須比對的最少詞彙數量，才會出現在搜尋結果中。例如，下列查詢要求每份傳回的文件，其 `description` 欄位都必須至少符合兩個詞彙：

```json
GET /testindex/_search
{
  "query": {
    "query_string": {
      "fields": [
        "description"
      ],
      "query": "historical epic film",
      "minimum_should_match": 2
    }
  }
}
```
{% include copy-curl.html %}

對於此查詢，OpenSearch 會建立下列布林查詢：`(description:historical description:epic description:film)~2`。

### 搭配多個欄位使用最低相符數量

如果您在 `query_string` 查詢中指定多個欄位，OpenSearch 會為指定的欄位建立 [`dis_max` 查詢]({{site.url}}{{site.baseurl}}/query-dsl/compound/disjunction-max/)。如果您未明確為查詢詞彙指定運算子，整個查詢文字會被視為一個子句。OpenSearch 會使用此單一子句為每個欄位建立查詢。最終的布林查詢包含一個對應於所有欄位之 `dis_max` 查詢的單一子句，因此不會套用 `minimum_should_match` 參數。

例如，在下列查詢中，`historical epic heroic` 被視為單一子句：

```json
GET /testindex/_search
{
  "query": {
    "query_string": {
      "fields": [
        "title",
        "description"
      ],
      "query": "historical epic heroic",
      "minimum_should_match": 2
    }
  }
}
```
{% include copy-curl.html %}

對於此查詢，OpenSearch 會建立下列布林查詢：`((title:historical title:epic title:heroic) | (description:historical description:epic description:heroic))`。

如果您在查詢詞彙中加入明確的運算子 (`AND` 或 `OR`)，每個詞彙都會被視為獨立的子句，並可對其套用 `minimum_should_match` 參數。例如，在下列查詢中，`historical`、`epic` 和 `heroic` 被視為獨立的子句：

```json
GET /testindex/_search
{
  "query": {
    "query_string": {
      "fields": [
        "title",
        "description"
      ],
      "query": "historical OR epic OR heroic",
      "minimum_should_match": 2
    }
  }
}
```
{% include copy-curl.html %}

對於此查詢，OpenSearch 會建立下列布林查詢：`((title:historical | description:historical) (description:epic | title:epic) (description:heroic | title:heroic))~2`。此查詢至少比對三個子句中的兩個。每個子句代表針對每個詞彙，在 `title` 和 `description` 兩個欄位上執行的 `dis_max` 查詢。

或者，若要確保可以套用 `minimum_should_match`，您可以將 `type` 參數設定為 `cross_fields`。這表示在分析輸入文字時，使用相同分析器的欄位應分為同一組：

```json
GET /testindex/_search
{
  "query": {
    "query_string": {
      "fields": [
        "title",
        "description"
      ],
      "query": "historical epic heroic",
      "type": "cross_fields",
      "minimum_should_match": 2
    }
  }
}
```
{% include copy-curl.html %}

對於此查詢，OpenSearch 會建立下列布林查詢：`((title:historical | description:historical) (description:epic | title:epic) (description:heroic | title:heroic))~2`。

不過，如果您使用不同的分析器，則必須在查詢中使用明確的運算子，以確保 `minimum_should_match` 參數套用至每個詞彙。

## 參數

下表列出 `query_string` 查詢支援的參數。除了 `query` 以外，所有參數皆為選用。

參數 | 資料類型 | 說明
:--- | :--- | :---
`query` | 字串 | 可能包含 [查詢字串語法](#query-string-syntax) 中用於搜尋之運算式的文字。必要。
`allow_leading_wildcard` | 布林值 | 指定是否允許 `*` 和 `?` 作為搜尋詞彙的第一個字元。預設為 `true`。
`analyze_wildcard` | 布林值 | 指定 OpenSearch 是否應嘗試分析萬用字元詞彙。預設為 `false`。
`analyzer` | 字串 | 用來對查詢字串文字進行斷詞的[分析器]({{site.url}}{{site.baseurl}}/analyzers/index/)。預設為為 `default_field` 指定的索引時分析器。如果未為 `default_field` 指定分析器，則 `analyzer` 是索引的預設分析器。有關 `index.query.default_field` 的更多資訊，請參閱 [動態索引設定]({{site.url}}{{site.baseurl}}/install-and-configure/configuring-opensearch/index-settings/#dynamic-index-settings)。
`auto_generate_synonyms_phrase_query` | 布林值 | 指定是否為多詞彙同義詞自動建立 [片語比對查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/match-phrase/)。例如，如果您指定 `ba, batting average` 作為同義詞並搜尋 `ba`，則 OpenSearch 會搜尋 `ba OR "batting average"` (若此選項為 `true`) 或 `ba OR (batting AND average)` (若此選項為 `false`)。預設為 `true`。
`boost` | 浮點數 | 以給定的倍數提升子句的權重。適合用於在複合查詢中為子句加權。[0, 1) 範圍內的值會降低相關性，大於 1 的值會提高相關性。預設為 `1`。
`default_field` | 字串 | 當查詢字串中未指定欄位時要搜尋的欄位。支援萬用字元。預設為 `index.query. Default_field` 索引設定中指定的值。預設情況下，`index.query. Default_field` 為 `*`，表示擷取所有適合詞彙查詢的欄位並篩除中繼資料欄位。如果未指定 `prefix`，擷取的欄位會合併成一個查詢。適用欄位不包含巢狀文件。搜尋所有適用欄位可能是耗用大量資源的作業。`indices.query.bool.max_clause_count` 搜尋設定定義了一次可查詢的欄位數與詞彙數乘積的最大值。`indices.query.bool.max_clause_count` 的預設值為 1,024。
`default_operator`| 字串 | 如果查詢字串包含多個搜尋詞彙，指定文件被視為符合時，是所有詞彙都必須符合 (`AND`) 還是只需一個詞彙符合 (`OR`)。有效值為：<br>- `OR`：字串 `to be` 會被解譯為 `to OR be`<br>- `AND`：字串 `to be` 會被解譯為 `to AND be`<br> 預設為 `OR`。
`enable_position_increments` | 布林值 | 當為 `true` 時，產生的查詢會感知位置增量。當移除停用詞後在詞彙之間留下不想要的「間隙」時，此設定很有用。預設為 `true`。
`fields` | 字串陣列 | 要搜尋的欄位清單 (例如 `"fields": ["title^4", "description"]`)。支援萬用字元。若未指定，預設為 `index.query. Default_field` 設定，其預設值為 `["*"]`。
`fuzziness` | 字串 | 在判斷詞彙是否符合某個值時，將一個單字變更為另一個單字所需的字元編輯次數 (插入、刪除、替換)。例如，`wined` 與 `wind` 之間的距離為 1。有效值為非負整數或 `AUTO`。預設值 `AUTO` 會根據搜尋詞彙的長度動態選擇編輯距離。您可以使用 `AUTO:[low],[high]` 語法自訂門檻，其中 `low` 和 `high` 定義字元長度邊界。若省略，OpenSearch 會使用 `AUTO:3,6` 作為預設值，套用下列規則：<br>- 包含 0--2 個字元的詞彙：需要完全符合 (0 次編輯)。<br>- 包含 3--5 個字元的詞彙：最多允許 1 次編輯。<br>- 包含 6 個以上字元的詞彙：最多允許 2 次編輯。<br>例如，`AUTO:4,7` 要求包含 0--3 個字元的詞彙完全符合，包含 4--6 個字元的詞彙最多允許 1 次編輯，包含 7 個以上字元的詞彙最多允許 2 次編輯。大多數情況建議使用 `AUTO`。
`fuzzy_max_expansions` | 正整數 | 查詢可展開的最大詞彙數。模糊查詢會「展開至」`fuzziness` 指定距離內的多個符合詞彙，然後 OpenSearch 會嘗試比對這些詞彙。預設為 `50`。
`fuzzy_transpositions` | 布林值 | 將 `fuzzy_transpositions` 設為 `true` (預設) 會在 `fuzziness` 選項的插入、刪除和替換作業中加入相鄰字元交換。例如，若 `fuzzy_transpositions` 為 true (交換 "n" 和 "i")，`wind` 與 `wnid` 之間的距離為 1；若為 false (刪除 "n"、插入 "n")，則距離為 2。若 `fuzzy_transpositions` 為 false，`rewind` 和 `wnid` 與 `wind` 的距離相同 (2)，儘管從以人為本的角度來看 `wnid` 顯然是拼字錯誤。預設值適合大多數使用情境。
`lenient` | 布林值 | 將 `lenient` 設為 `true` 會忽略查詢與文件欄位之間的資料類型不符。例如，查詢字串 `"8.2"` 可以符合 `float` 類型的欄位。預設為 `false`。
`max_determinized_states` | 正整數 | Lucene 可為包含正規表示式的查詢字串 (例如 `"query": "/wind.+?/"`) 建立的「[狀態](https://lucene.apache.org/core/{{site.lucene_version}}/core/org/apache/lucene/util/automaton/Operations.html#DEFAULT_MAX_DETERMINIZED_STATES)」數上限 (複雜度的度量)。數字越大，允許的查詢會使用越多記憶體。預設為 10,000。
`minimum_should_match` | 正或負整數、正或負百分比、組合 | 如果查詢字串包含多個搜尋詞彙且您使用 `or` 運算子，此為文件被視為符合時需要符合的詞彙數。例如，若 `minimum_should_match` 為 2，`wind often rising` 不符合 `The Wind Rises.`；若 `minimum_should_match` 為 `1`，則符合。詳細資訊請參閱 [最低相符數量]({{site.url}}{{site.baseurl}}/query-dsl/minimum-should-match/)。
`phrase_slop` | 整數 | 符合單字之間允許的最大單字數。若 `phrase_slop` 為 2，片語中符合單字之間最多允許兩個單字。調換順序的單字其 slop 為 2。預設為 `0` (完全片語符合，符合的單字必須相鄰)。
`quote_analyzer` | 字串 | 用來對查詢字串中引號內文字進行斷詞的分析器。會針對引號內文字覆寫 `analyzer` 參數。預設為為 `default_field` 指定的 `search_quote_analyzer`。
`quote_field_suffix` | 字串 | 此選項支援使用與非精確符合不同的分析方法來搜尋精確符合 (以引號包圍)。例如，若 `quote_field_suffix` 為 `.exact`，且您在 `title` 欄位中搜尋 `\"lightly\"`，OpenSearch 會在 `title.exact` 欄位中搜尋單字 `lightly`。此第二個欄位可能使用不同的類型 (例如 `keyword` 而非 `text`) 或不同的分析器。
`rewrite` | 字串 | 決定 OpenSearch 如何改寫與評分多詞彙查詢。有效值為 `constant_score`、`scoring_boolean`、`constant_score_boolean`、`top_terms_N`、`top_terms_boost_N` 和 `top_terms_blended_freqs_N`。預設為 `constant_score`。
`time_zone` | 字串 | 指定所需時區相對於 `UTC` 的偏移時數。如果查詢字串包含日期範圍，您需要指定時區偏移數。例如，對於包含 `"query": "wind rises release_date[2012-01-01 TO 2014-01-01]"` 之類日期範圍的查詢，請設定 `time_zone": "-08:00"`。用於指定偏移時數的預設時區格式為 `UTC`。

查詢字串查詢可能會在內部轉換為 [前綴查詢]({{site.url}}{{site.baseurl}}/query-dsl/term/prefix/)。如果 [`search.allow_expensive_queries`]({{site.url}}{{site.baseurl}}/query-dsl/index/#expensive-queries) 設為 `false`，則不會執行前綴查詢。如果啟用 `index_prefixes`，則會忽略 `search.allow_expensive_queries` 設定，並建立並執行最佳化的查詢。
{: .important}
