---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Dashboards 查詢語言（DQL）"
nav_order: 50
redirect_from:
  - /dashboards/discover/dql/
---

<!-- vale off -->
# Dashboards 查詢語言（DQL）
<!-- vale on -->

Dashboards 查詢語言（DQL）是一種簡單的文字式查詢語言，用於在 OpenSearch Dashboards 中篩選資料。 

DQL 和 [query string 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)（Lucene）語言是 Discover 和 Dashboards 搜尋列中的兩種語言選項。本頁提供 DQL 語法參考。如需 Lucene 語法，請參閱 [Query string 查詢]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/)。如需比較語法，請參閱[命令快速參考](#dql-and-query-string-query-quick-reference)。

OpenSearch Dashboards 預設使用 DQL 語法。若要切換至 query string 查詢（Lucene），請選取搜尋方塊旁的 **DQL** 按鈕，然後切換 **On** 開關，如下圖所示。 

![在 Dashboard 中使用 DQL 工具列搜尋詞彙]({{site.url}}{{site.baseurl}}/images/dashboards/dql-interface.png)

語法會變更為 **Lucene**。若要切換回 DQL，請選取 **Lucene** 按鈕，然後切換 **Off** 開關。

## 對經過分析的文字進行查詢

執行查詢時，了解您的欄位是經過分析（[`text`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 類型）還是未經分析（[`keyword`]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/keyword/) 類型）至關重要，因為這會大幅影響搜尋行為。在經過分析的欄位中，文字會經過斷詞和篩選，而未經分析的欄位則儲存精確值。對於 `wind` 這類簡單的欄位查詢，搜尋經過分析的欄位時，會比對含有 `wind` 的文件，不區分大小寫；但對 keyword 欄位執行相同查詢時，則需要精確比對完整字串。如需經過分析的欄位的詳細資訊，請參閱[文字分析]({{site.url}}{{site.baseurl}}/analyzers/)。

## 設定

若要在 OpenSearch Dashboards 中依照本教學操作，請展開下列設定步驟。

<details markdown="block">
<summary>
    設定
</summary>
{: .text-delta}

使用下列步驟準備範例資料以供查詢。

**步驟 1：設定索引的對應**

在主選單中，選取 **Management** > **Dev Tools**，以開啟 [Dev Tools]({{site.url}}{{site.baseurl}}/dashboards/dev-tools/run-queries/)。傳送下列請求以建立索引對應：

```json
PUT testindex
{
  "mappings" : {
    "properties" :  {
      "date" : {
        "type" : "date",
        "format" : "yyyy-MM-dd"
      }
    }
  }
}
```
{% include copy-curl.html %}

**步驟 2：將文件匯入索引**

在 **Dev Tools** 中，將下列文件匯入索引：

```json
PUT /testindex/_doc/1
{
  "title": "The wind rises",
  "description": "A biographical film",
  "media_type": "film",
  "date": "2013-07-20",
  "page_views": 100
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/2
{
  "title": "Gone with the wind",
  "description": "A well-known 1939 American epic historical film",
  "media_type": "film",
  "date": "1939-09-09",
  "page_views": 200
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/3
{
  "title": "Chicago: the historical windy city",
  "media_type": "article",
  "date": "2023-07-29",
  "page_views": 300
}
```
{% include copy-curl.html %}

```json
PUT /testindex/_doc/4
{
  "article title": "Wind turbines",
  "media_type": "article",
  "format": "2*3"
}
```
{% include copy-curl.html %}

**步驟 3：建立索引模式**

依照下列步驟為您的索引建立索引模式：

1. 在主選單中，選取 **Management** > **Dashboards Management**。 
1. 選取 **Index patterns**，然後選取 **Create index pattern**。
1. 在 **Index pattern name** 中，輸入 `testindex*`。選取 **Next step**。
1. 在 **Time field** 中，選取 `I don't want to use the time filter`。
1. 選取 **Create index pattern**。

如需索引模式的詳細資訊，請參閱[索引模式]({{site.url}}{{site.baseurl}}/dashboards/management/index-patterns/)。

**步驟 4：前往 Discover 並選取索引模式**

在主選單中，選取 **Discover**。在左上角，從 **Index patterns** 下拉式清單中選取 `testindex*`。主要面板會顯示索引中的文件，您現在可以試用本頁所述的 DQL 查詢。

[物件欄位](#object-fields)和[巢狀欄位](#nested-fields)章節提供連結，說明試用這些章節中的查詢所需的額外設定。
{: .note}
</details>

## DQL 和 query string 查詢快速參考

下表提供這兩種查詢語言命令的快速參考。 

| 功能 | DQL | Query string 查詢（Lucene）|
|:---|:---|:---|
| 基本詞彙搜尋 | `wind` | `wind` |
| 多個詞彙 | `wind gone`（尋找含有 `wind` 或 `gone` 的文件） | `wind gone`（尋找含有 `wind` 或 `gone` 的文件） |
| 精確片語搜尋 | `"wind rises"` | `"wind rises"` |
| 特定欄位搜尋 | `title: wind` | `title:wind` |
| 欄位是否存在 | `description:*` | `_exists_:description` |
| 欄位中的多個詞彙 | `title: (wind OR rises)` <br><br> | `title:(wind OR rises)` |
| 含有空格的欄位 | `article*title: wind` | `article\ title:wind` |
| 跳脫特殊字元 | `format: 2\*3` | `format:2\*3` |
| 多欄位搜尋 | `title: wind OR description: film` | `title:wind OR description:film` |
| 巢狀欄位搜尋 | 請參閱[巢狀欄位](#nested-fields) | 不支援 |
| 數值範圍 | `page_views >= 100 and page_views <= 300` <br><br> `not page_views: 100`（結果包含不含 `page_views` 欄位的文件） <br><br>   請參閱[範圍](#ranges)| `page_views:[100 TO 300]` <br><br>  `page_views:(>=100 AND <=300)` <br><br>  `page_views:(+>=100 +<=300)` <br><br>  `page_views:[100 TO *]` <br><br>  `page_views:>=100` <br><br>  `NOT page_views:100`（結果包含不含 `page_views` 欄位的文件） <br><br> 請參閱[範圍]({{site.url}}{{site.baseurl}}/query-dsl/full-text/query-string/#ranges)|
| 日期範圍 | `date >= "1939-01-01" and date <= "2013-12-31"` <br><br> `not date: "1939-09-08"` | `date:[1939-01-01 TO 2013-12-31]` <br><br> `NOT date:1939-09-08` <br><br> 支援所有數值範圍語法結構|
| 不含邊界值的範圍 | 不支援 | `page_views: {100 TO 300}`（傳回 `page_views` 介於 `100` 和 `300` 之間的文件，不含 `100` 和 `300`） |
| 布林值 `AND` | `media_type: film AND page_views: 100` <br><br> `media_type: film and page_views: 100`| `media_type:film AND page_views:100` <br><br> `+media_type:film +page_views:100`|
| 布林值 `NOT` | `NOT media_type: article` <br><br> `not media_type: article` | `NOT media_type:article` <br><br> `-media_type:article`  |
| 布林值 `OR` | `title: wind OR description: film` <br><br> `title: wind or description: film` | `title: wind OR description: film` |
| 必須包含／禁止包含運算子 | 不支援 | 同時支援 `+`（必須包含運算子）和 `-`（禁止包含運算子） <br><br> `+title:wind -media_type:article`（傳回 `title` 含有 `wind`，但 `media_type` 不含 `article` 的文件）  |
| 萬用字元 | `title: wind*`<br><br> `titl*: wind` <br><br> 不支援在片語搜尋（引號內）中使用萬用字元 <br><br> 僅支援 `*`（多個字元）  | `title:wind*` 或 `title:w?nd` <br><br> 不支援在欄位名稱中使用萬用字元 <br><br> 不支援在片語搜尋（引號內）中使用萬用字元 <br><br> 支援 `*`（多個字元）和 `?`（單一字元） |
| 正規表示式 | 不支援 | `title:/w[a-z]nd/` |
| 模糊搜尋 | 不支援 | `title:wind~2` |
| 鄰近搜尋 | 不支援 | `"wind rises"~2` |
| 提高詞彙權重 | 不支援 | `title:wind^2` |
| 保留字元 | `\ ( ) : < > " *` | `+ - = && || > < ! ( ) { } [ ] ^ " ~ * ? : \ /` |

## 搜尋詞彙

預設情況下，DQL 會在索引中設為預設欄位的欄位內搜尋。若未設定預設欄位，DQL 會搜尋所有欄位。例如，下列查詢會搜尋任何欄位中包含 `rises` 或 `wind` 字詞的文件：

```python
rises wind
```
{% include copy.html %}

上述查詢會比對任何搜尋詞彙出現的文件，不論順序為何。預設情況下，DQL 使用 `or` 結合搜尋詞彙。若要瞭解如何建立包含搜尋詞彙的布林運算式，請參閱 [布林運算子](#boolean-operators)。

若要搜尋片語（依序排列的字詞序列），請使用引號包住文字。例如，下列查詢會搜尋確切文字 "wind rises"：

```python
"wind rises"
```
{% include copy.html %}

連字號是 Lucene 的保留字元，因此若您的搜尋詞彙包含連字號，DQL 可能會提示您切換至 Lucene 語法。若要避免這種情況，請在片語搜尋中使用引號包住搜尋詞彙，或在一般搜尋中省略連字號。
{: .tip}

## 保留字元

以下是 DQL 中的保留字元清單：

`\`, `(`, `)`, `:`, `<`, `>`, `"`, `*`

使用反斜線（`\`）來跳脫保留字元。例如，若要搜尋運算式 `2*3`，請將查詢指定為 `2\*3`：

```plaintext
2\*3
```
{% include copy.html %}

## 在欄位中搜尋

若要在特定欄位中搜尋文字，請在冒號前指定欄位名稱：

```python
title: rises wind
```
{% include copy.html %}

您所搜尋欄位的分析器會將查詢文字解析成詞元，並比對任何詞元出現的文件。

DQL 會忽略空白字元，因此 `title:rises wind` 與 `title: rises wind` 相同。
{: .tip}

使用萬用字元來參照包含空格的欄位名稱。例如，`article*title` 會比對 `article title` 欄位。
{: .tip}

## 欄位名稱

請在冒號前指定欄位名稱。下表包含使用欄位名稱的範例查詢。

查詢 | 文件比對條件 | 來自 `testindex` 索引的比對文件
:--- | :--- | :---
`title: wind` | `title` 欄位包含字詞 `wind`。 | 1, 2
`title: (wind OR windy)` | `title` 欄位包含字詞 `wind` 或字詞 `windy`。 | 1, 2, 3
`title: "wind rises"` | `title` 欄位包含片語 `wind rises`。 | 1
`title.keyword: The wind rises` | `title.keyword` 欄位完全符合 `The wind rises`。 | 1
`title*: wind` | 任何以 `title` 開頭的欄位（例如 `title` 與 `title.keyword`）包含字詞 `wind` | 1, 2
`article*title: wind` | 以 `article` 開頭且以 `title` 結尾的欄位包含字詞 `wind`。符合欄位 `article title`。 | 4
`description:*` | 欄位 `description` 存在的文件。 | 1, 2

## 萬用字元

DQL 在搜尋詞彙與欄位名稱中都支援萬用字元（僅 `*`），例如：

```python
t*le: *wind and rise*
```
{% include copy.html %}

## 範圍

DQL 支援使用 `>`、`<`、`>=` 與 `<=` 運算子的數值不等式，例如：

```python
page_views > 100 and page_views <= 300
```
{% include copy.html %}

您可以對日期使用範圍運算子。例如，下列查詢會搜尋包含 2013 至 2023 年（含端點）範圍內日期的文件：

```python
date >= "2013-01-01" and date < "2024-01-01"
```
{% include copy.html %}

您可以使用 `not` 與欄位名稱來查詢「不等於」，例如：

```python
not page_views: 100
```
{% include copy.html %}

請注意，上述查詢會傳回 `page_views` 欄位不包含 `100`，或該欄位不存在的文件。若要篩選出包含欄位 `page_views` 的文件，請使用下列查詢：

```python
page_views:* and not page_views: 100
```
{% include copy.html %}

## 布林運算子

DQL 支援 `and`、`or` 與 `not` 布林運算子。DQL 不區分大小寫，因此 `AND` 與 `and` 相同。例如，下列查詢是兩個布林子句的合取：

```python
title: wind and description: epic
```
{% include copy.html %}

布林運算子遵循 `not`、`and` 與 `or` 的邏輯優先順序，因此在下列範例中，`title: wind and description: epic` 會先被求值：

```python
media_type: article or title: wind and description: epic
```
{% include copy.html %}

若要指定求值順序，請將布林子句以括號分組。例如，在下列查詢中，括號內的運算式會先被求值：

```python
(media_type: article or title: wind) and description: epic
```
{% include copy.html %}

欄位前綴會參照緊接在冒號之後的詞元。例如，下列查詢會搜尋 `title` 欄位包含 `windy` 的文件，或任何欄位中包含字詞 `historical` 的文件：

```python
title: windy or historical
```
{% include copy.html %}

若要搜尋 `title` 欄位包含 `windy` 或 `historical` 的文件，請將詞彙以括號分組：

```python
title: (windy or historical)
```
{% include copy.html %}

上述查詢等同於 `title: windy or title: historical`。

若要否定查詢，請使用 `not` 運算子。例如，下列查詢會搜尋 `title` 欄位包含字詞 `wind`、不是 `article` 類型的 `media_type`，且 `description` 欄位不包含 `epic` 的文件：

```python
title: wind and not (media_type: article or description: epic)
```
{% include copy.html %}

查詢可以包含多個分組層級，例如：

```python
title: ((wind or windy) and not rises)
```
{% include copy.html %}

## 物件欄位

若要參照物件的內部欄位，請列出該欄位的點路徑。

若要為包含物件的文件編製索引，請依照 [物件欄位類型範例]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/object/#example) 中的步驟。若要搜尋 `patient` 物件的 `name` 欄位，請使用下列語法：

```python
patient.name: john
```
{% include copy.html %}

## 巢狀欄位

若要參照巢狀物件，請列出該欄位的 JSON 路徑。

若要為包含物件的文件編製索引，請依照 [巢狀欄位類型範例]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/nested/#mapping-objects-as-nested) 中的步驟。

若要搜尋 `patients` 物件的 `name` 欄位，請使用下列語法：

```python
patients: {name: john}
```
{% include copy.html %}

若要擷取符合多個欄位的文件，請指定所有欄位。例如，假設下列文件中有額外的 `status` 欄位：

```json
{ 
  "status": "Discharged",
  "patients": [ 
    {"name" : "John Doe", "age" : 56, "smoker" : true},
    {"name" : "Mary Major", "age" : 85, "smoker" : false}
  ] 
}
```

若要搜尋名為 John 的已出院病患，請在查詢中指定 `name` 與 `status`：

```python
patients: {name: john} and status: discharged
```
{% include copy.html %}

您可以結合多個布林與範圍查詢來建立更精細的查詢，例如：

```python
patients: {name: john and smoker: true and age < 57} 
```
{% include copy.html %}

## 雙重巢狀欄位 

請考慮一份具有雙重巢狀欄位的文件。在這份文件中，`patients` 與 `names` 欄位皆為 `nested` 類型：

```json
{
  "patients": [
    {
      "names": [
        { "name": "John Doe", "age": 56, "smoker": true },
        { "name": "Mary Major", "age": 85, "smoker": false}
      ]
    }
  ]
}
```

若要搜尋 `patients` 物件的 `name` 欄位，請使用下列語法：

```python
patients: {names: {name: john}}
```
{% include copy.html %}

相對地，請考慮一份文件中 `patients` 欄位為 `object` 類型，但 `names` 欄位為 `nested` 類型：

```json
{
  "patients": 
  {
    "names": [
      { "name": "John Doe", "age": 56, "smoker": true },
      { "name": "Mary Major", "age": 85, "smoker": false}
    ]
  }
}
```

若要搜尋 `patients` 物件的 `name` 欄位，請使用下列語法：

```python
patients.names: {name: john}
```
{% include copy.html %}
