---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "文字分析"
has_children: true
nav_order: 5
nav_exclude: true
has_toc: false
permalink: /analyzers/
redirect_from: 
  - /opensearch/query-dsl/text-analyzers/
  - /query-dsl/analyzers/text-analyzers/
  - /analyzers/text-analyzers/
  - /analyzers/index/
---

# 文字分析

當您使用全文搜尋來搜尋文件時，您會希望取得所有相關的結果。如果您要找「walk」，您會對包含該字任何形式的結果感興趣，例如「Walk」、「walked」或「walking」。為了協助全文搜尋，OpenSearch 使用文字分析。

文字分析的目的是將來源文件中非結構化的自由文字內容分割成一連串的詞彙 (term)，接著將這些詞彙儲存在反向索引中。之後，當對使用者的查詢套用類似的文字分析時，所產生的詞彙序列便有助於比對相關的來源文件。

從技術角度來看，文字分析流程包含數個步驟，其中部分步驟為選用：

1. 在將自由文字內容分割成個別單字之前，先在字元層級精煉文字可能會有所幫助。此選用步驟的主要目的是協助斷詞器（分析流程的下一個階段）產生更好的詞元。這可能包括移除標記標籤（例如 HTML），或處理特定的字元模式（例如將 &#x1F642; 表情符號取代為文字 `:slightly_smiling_face:`）。

2. 下一步是將自由文字分割成個別單字---_詞元_。這是由 _斷詞器_ 執行。例如，經過斷詞後，句子 `Actions speak louder than words` 會被分割成詞元 `Actions`、`speak`、`louder`、`than` 和 `words`。

3. 最後一步是套用一系列詞元篩選器來處理個別詞元。目的是將每個詞元轉換成可預測的形式並直接儲存在索引中，例如將詞元轉換成小寫，或執行詞幹提取（將單字還原為其字根）。例如，詞元 `Actions` 會變成 `action`，`louder` 會變成 `loud`，而 `words` 會變成 `word`。

儘管 ***token***（詞元）與 ***term***（詞彙）這兩個術語聽起來相似，有時也會交替使用，但了解兩者之間的差異會很有幫助。在 Apache Lucene 的語境中，兩者各自扮演不同的角色。***詞元*** 是斷詞器在文字分析期間建立的，在通過詞元篩選器鏈時，通常會經過多次額外的修改。每個詞元都與中繼資料相關聯，這些中繼資料可在文字分析流程中進一步使用。***詞彙*** 是直接儲存在反向索引中的資料值，關聯的中繼資料少得多。在搜尋期間，比對是在詞彙層級進行。
{: .note}

## 分析器

在 OpenSearch 中，涵蓋文字分析的抽象概念稱為 _分析器_。每個分析器都包含下列依序套用的元件：

1. **字元篩選器**：首先，字元篩選器會以字元串流的形式接收原始文字，並在文字中新增、移除或修改字元。例如，字元篩選器可以從字串中移除 HTML 字元，使文字 `<p><b>Actions</b> speak louder than <em>words</em></p>` 變成 `\nActions speak louder than words\n`。字元篩選器的輸出是字元串流。

1. **斷詞器**：接著，斷詞器會接收經字元篩選器處理過的字元串流，並將文字分割成個別的 _詞元_（通常是單字）。例如，斷詞器可以依空白分割文字，使上述文字變成 [`Actions`, `speak`, `louder`, `than`, `words`]。斷詞器也會維護詞元的中繼資料，例如詞元在文字中的起始與結束位置。斷詞器的輸出是詞元串流。

1. **詞元篩選器**：最後，詞元篩選器會接收來自斷詞器的詞元串流，並新增、移除或修改詞元。例如，詞元篩選器可以將詞元轉換為小寫，使 `Actions` 變成 `action`；移除如 `than` 的停用詞；或為單字 `speak` 新增如 `talk` 的同義詞。

分析器必須只包含一個斷詞器，並且可以包含零個或多個字元篩選器，以及零個或多個詞元篩選器。
{: .note}

另外還有一種特殊類型的分析器，稱為 ***正規化器***。正規化器與分析器類似，差別在於它不包含斷詞器，且只能包含特定類型的字元篩選器與詞元篩選器。這些篩選器只能執行字元層級的操作，例如字元或模式取代，無法對整個詞元執行操作。這表示不支援將詞元取代為同義詞或詞幹提取。如需更多詳細資訊，請參閱[正規化器]({{site.url}}{{site.baseurl}}/analyzers/normalizers/)。

## 支援的分析器

如需支援的分析器清單，請參閱[分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/index/)。

## 自訂分析器

如有需要，您可以組合斷詞器、詞元篩選器與字元篩選器來建立自訂分析器。如需更多資訊，請參閱[建立自訂分析器]({{site.url}}{{site.baseurl}}/analyzers/custom-analyzer/)。

## 編製索引時與查詢時的文字分析

OpenSearch 會在您將文件編製索引時以及傳送搜尋請求時，對文字欄位執行文字分析。依據文字分析的時機，所使用的分析器分類如下：

- _索引分析器_ 在編製索引時執行分析：當您為 [text]({{site.url}}{{site.baseurl}}/mappings/supported-field-types/text/) 欄位編製索引時，OpenSearch 會在編製索引之前先分析該欄位。如需有關指定索引分析器方式的更多資訊，請參閱[索引分析器]({{site.url}}{{site.baseurl}}/analyzers/index-analyzers/)。

- _搜尋分析器_ 在查詢時執行分析：當您對文字欄位執行全文查詢時，OpenSearch 會分析查詢字串。如需有關指定搜尋分析器方式的更多資訊，請參閱[搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)。

在大多數情況下，您應該在編製索引與搜尋時使用相同的分析器，因為這樣文字欄位與查詢字串會以相同方式進行分析，所產生的詞元也會如預期般相符。
{: .tip}

### 範例

當您將包含文字欄位且其文字為 `Actions speak louder than words` 的文件編製索引時，OpenSearch 會分析該文字並產生下列詞元清單：

文字欄位詞元 = [`action`, `speak`, `loud`, `than`, `word`]

當您搜尋符合查詢 `speaking loudly` 的文件時，OpenSearch 會分析查詢字串並產生下列詞元清單：

查詢字串詞元 = [`speak`, `loud`]

接著，OpenSearch 會將查詢字串中的每個詞元與文字欄位詞元清單進行比較，發現兩份清單都包含詞元 `speak` 與 `loud`，因此 OpenSearch 會將此文件作為符合查詢的搜尋結果之一傳回。

## 測試分析器

若要測試內建分析器，並檢視將文件編製索引時其產生的詞元清單，您可以使用 [Analyze API]({{site.url}}{{site.baseurl}}/api-reference/analyze-apis/#apply-a-built-in-analyzer)。

在請求中指定分析器與要分析的文字：

```json
GET /_analyze
{
  "analyzer" : "standard",
  "text" : "Let’s contribute to OpenSearch!"
}
```
{% include copy-curl.html %}

下圖顯示查詢字串。

![含索引位置的查詢字串]({{site.url}}{{site.baseurl}}/images/string-indices.png)

回應包含每個詞元及其起始與結束位移，分別對應原始字串中的起始索引（包含）與結束索引（不包含）：

```json
{
  "tokens": [
    {
      "token": "let’s",
      "start_offset": 0,
      "end_offset": 5,
      "type": "<ALPHANUM>",
      "position": 0
    },
    {
      "token": "contribute",
      "start_offset": 6,
      "end_offset": 16,
      "type": "<ALPHANUM>",
      "position": 1
    },
    {
      "token": "to",
      "start_offset": 17,
      "end_offset": 19,
      "type": "<ALPHANUM>",
      "position": 2
    },
    {
      "token": "opensearch",
      "start_offset": 20,
      "end_offset": 30,
      "type": "<ALPHANUM>",
      "position": 3
    }
  ]
}
```

## 驗證分析器設定

若要驗證哪個分析器與哪個欄位相關聯，您可以使用 get mapping API 操作：

```json
GET /testindex/_mapping
```
{% include copy-curl.html %}

回應會提供每個欄位的分析器資訊：

```json
{
  "testindex": {
    "mappings": {
      "properties": {
        "text_entry": {
          "type": "text",
          "analyzer": "simple",
          "search_analyzer": "whitespace"
        }
      }
    }
  }
}
```

## 正規化器

斷詞會將文字分割成個別詞彙，但無法處理詞元形式的變化。正規化會將詞元轉換為標準格式來解決這些問題。這可確保相似的詞彙能適當地相符，即使它們並不完全相同。

### 正規化技術

下列正規化技術有助於處理詞元形式的變化：

1. **大小寫正規化**：將所有詞元轉換為小寫，以確保不區分大小寫的比對。例如，「Hello」會正規化為「hello」。

2. **詞幹提取**：將單字還原為其字根形式。例如，「cars」會提取詞幹為「car」，而「running」會正規化為「run」。

3. **同義詞處理：**將同義詞視為相等。例如，「jogging」與「running」可以在共同的詞彙（例如「run」）下編製索引。

### 正規化

由於大小寫正規化，搜尋 `Hello` 會比對到包含 `hello` 的文件。

由於詞幹提取，搜尋 `cars` 也會比對到包含 `car` 的文件。

透過同義詞處理，查詢 `running` 可以擷取包含 `jogging` 的文件。

正規化可確保搜尋不受限於完全相符的詞彙，從而取得更相關的結果。例如，搜尋 `Cars running` 可以正規化以比對 `car run`。

## 後續步驟

- 進一步了解如何指定[索引分析器]({{site.url}}{{site.baseurl}}/analyzers/index-analyzers/)與[搜尋分析器]({{site.url}}{{site.baseurl}}/analyzers/search-analyzers/)。
- 請參閱[支援的分析器]({{site.url}}{{site.baseurl}}/analyzers/supported-analyzers/index/)清單。