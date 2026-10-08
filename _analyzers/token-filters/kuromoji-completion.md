---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji 自動完成"
parent: Token filters
nav_order: 231
---

# Kuromoji 自動完成詞元篩選器

`kuromoji_completion` 詞元篩選器會為日文詞元產生羅馬字讀音變體。在索引分析器中使用時，它會在相同位置同時輸出原始詞元以及一個或多個羅馬字替代形式。如此一來，使用者輸入日文字元或其對應的讀音拼寫，都能搜尋到日文內容。

此篩選器的設計用途是搭配 `kuromoji_completion` 分析器使用，或用於支援自動完成或建議欄位的自訂分析器中。由於此篩選器在索引時與查詢時的套用方式不同，因此提供了 `mode` 參數。

## 安裝

`kuromoji_completion` 詞元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝說明，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

下表列出 `kuromoji_completion` 詞元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`mode` | 字串 | 控制詞元的產生方式。有效值為 `index`（預設）和 `query`。兩種模式都會將片假名詞元展開為其原始形式以及所有羅馬字變體。`query` 模式另外套用兩項規則，以處理來自輸入法編輯器 (IME) 的部分輸入：它會先將連續的假名詞元串接成單一詞元再進行羅馬字轉換，並且會將假名詞元與其後代表 IME 部分輸入按鍵的小寫英文字母詞元合併（例如，`サッ` 後接 `k` 會變成 `サッk`）。

請在搜尋分析器中使用 `query` 模式，讓使用者輸入的部分 IME 內容能在羅馬字轉換之前正確組合。
{: .tip}

## 範例

下列範例會建立名為 `kuromoji_completion_example` 的索引，其中包含索引時分析器（使用 `mode: index`）和搜尋時分析器（使用 `mode: query`），並將 `suggest` 欄位對應為使用這兩個分析器：

```json
PUT /kuromoji_completion_example
{
  "settings": {
    "analysis": {
      "filter": {
        "completion_index_filter": {
          "type": "kuromoji_completion",
          "mode": "index"
        },
        "completion_query_filter": {
          "type": "kuromoji_completion",
          "mode": "query"
        }
      },
      "analyzer": {
        "completion_index_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["completion_index_filter"]
        },
        "completion_query_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["completion_query_filter"]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "completion_index_analyzer",
        "search_analyzer": "completion_query_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用此組態時，包含 `konpyu` 或 `コンピュ` 的查詢都會比對到以 `コンピューター` 編製索引的文件。

### 索引時詞元

使用下列請求，以意為「使用電腦」的文字檢視索引時產生的詞元：

```json
POST /kuromoji_completion_example/_analyze
{
  "analyzer": "completion_index_analyzer",
  "text": "コンピューターを使う"
}
```
{% include copy-curl.html %}

回應包含產生的詞元。每個來源詞元都會在相同位置產生原始形式以及一個或多個羅馬字變體。對於 `コンピューター`（電腦），篩選器會輸出原始片假名詞元和兩個羅馬字變體（`konpyuーtaー` 和 `konnpyuーtaー`）。對於助詞 `を`，它會輸出原始形式和兩個羅馬字形式（`wo` 和 `o`）。對於動詞 `使う`（使用），它會輸出原始形式和兩個羅馬字形式（`tukau` 和 `tsukau`）：

```json
{
  "tokens": [
    {
      "token": "コンピューター",
      "start_offset": 0,
      "end_offset": 7,
      "type": "word",
      "position": 0
    },
    {
      "token": "konpyuーtaー",
      "start_offset": 0,
      "end_offset": 7,
      "type": "word",
      "position": 0
    },
    {
      "token": "konnpyuーtaー",
      "start_offset": 0,
      "end_offset": 7,
      "type": "word",
      "position": 0
    },
    {
      "token": "を",
      "start_offset": 7,
      "end_offset": 8,
      "type": "word",
      "position": 1
    },
    {
      "token": "wo",
      "start_offset": 7,
      "end_offset": 8,
      "type": "word",
      "position": 1
    },
    {
      "token": "o",
      "start_offset": 7,
      "end_offset": 8,
      "type": "word",
      "position": 1
    },
    {
      "token": "使う",
      "start_offset": 8,
      "end_offset": 10,
      "type": "word",
      "position": 2
    },
    {
      "token": "tukau",
      "start_offset": 8,
      "end_offset": 10,
      "type": "word",
      "position": 2
    },
    {
      "token": "tsukau",
      "start_offset": 8,
      "end_offset": 10,
      "type": "word",
      "position": 2
    }
  ]
}
```

### 查詢時詞元

兩種模式都會將片假名詞元展開為原始形式以及所有羅馬字變體。`query` 模式的主要差異在於它對部分 IME 輸入的處理方式：當片假名詞元後接一個代表 IME 輸入中按鍵的小寫英文字母字元時，`query` 模式會先將它們串接成單一詞元再進行羅馬字轉換。若沒有這項處理，部分按鍵會被當作獨立的詞元處理，而羅馬字轉換結果將無法比對到任何已編製索引的變體。

下列範例以輸入 `コンピュt` 示範此行為，此輸入代表使用者已輸入片假名 `コンピュ`，且仍在使用 IME 組字輸入下一個字元 `t`：

```json
POST /kuromoji_completion_example/_analyze
{
  "analyzer": "completion_query_analyzer",
  "text": "コンピュt"
}
```
{% include copy-curl.html %}

`query` 模式會將 `t` 辨識為部分 IME 按鍵，並在羅馬字轉換之前將其與前面的片假名詞元合併，為合併後的形式 `コンピュt` 產生三個詞元：合併後的片假名加按鍵詞元，以及其兩個羅馬字變體（`konpyut` 和 `konnpyut`）：

```json
{
  "tokens": [
    {
      "token": "コンピュt",
      "start_offset": 0,
      "end_offset": 5,
      "type": "word",
      "position": 0
    },
    {
      "token": "konpyut",
      "start_offset": 0,
      "end_offset": 5,
      "type": "word",
      "position": 0
    },
    {
      "token": "konnpyut",
      "start_offset": 0,
      "end_offset": 5,
      "type": "word",
      "position": 0
    }
  ]
}
```

若使用 `index` 模式，`コンピュ` 和 `t` 會在不同位置以兩個獨立的詞元輸出，因此永遠不會產生羅馬字形式 `konpyut`，搜尋 `konpyut` 也不會有相符結果。

### 使用前綴查詢進行搜尋

由於索引會儲存原始片假名詞元及其所有羅馬字變體，您可以直接對已編製索引的羅馬字詞元使用 `prefix` 查詢來實作自動完成。`prefix` 查詢會略過分析器，並比對任何以指定值開頭的已編製索引詞元。

首先，將範例文件編製索引：

```json
POST /kuromoji_completion_example/_doc/1
{
  "content": "コンピューターを使う"
}
```
{% include copy-curl.html %}

下列 `prefix` 查詢會比對到該文件，因為 `konnp` 是已編製索引的羅馬字詞元 `konnpyuーtaー` 的前綴：

```json
GET /kuromoji_completion_example/_search
{
  "query": {
    "prefix": {
      "content": {
        "value": "konnp"
      }
    }
  }
}
```
{% include copy-curl.html %}

下列 `prefix` 查詢使用片假名前綴 `コンピュ` 比對到該文件，因為它是已編製索引的片假名詞元 `コンピューター` 的前綴：

```json
GET /kuromoji_completion_example/_search
{
  "query": {
    "prefix": {
      "content": {
        "value": "コンピュ"
      }
    }
  }
}
```
{% include copy-curl.html %}

若要採用更高層級的做法，在分析器層級而非篩選器層級設定 `mode`，請使用內建的 [`kuromoji_completion` 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/#kuromoji-completion-analyzer)。
{: .tip}

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
- [Kuromoji 讀音形式詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-readingform/)
- [日文停用詞詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/ja-stop/)
