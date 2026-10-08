---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "Kuromoji（日文）"
parent: Language analyzers
grand_parent: Analyzers
nav_order: 225
---

# Kuromoji 分析器

`kuromoji` 分析器使用以 IPAdic 字典為基礎的 Kuromoji 程式庫，為日文文字提供詞素分析。它會將日文句子切分為有意義的詞元，移除常見的停用詞與文法助詞，並以字典基本形式傳回詞元。

若要使用 `kuromoji` 分析器或任何 Kuromoji 元件，您必須先安裝 `analysis-kuromoji` 外掛程式。

## 安裝外掛程式

在所有節點上安裝外掛程式，然後重新啟動叢集：

```bash
bin/opensearch-plugin install analysis-kuromoji
```
{% include copy.html %}

如需安裝外掛程式的詳細資訊，請參閱[管理 OpenSearch 外掛程式]({{site.url}}{{site.baseurl}}/install-and-configure/plugins/)。

## Kuromoji 外掛程式元件

`analysis-kuromoji` 外掛程式提供下列元件，您可以單獨使用這些元件，或在自訂分析器中組合使用。

### 分析器

| 分析器 | 說明 |
|:---------|:------------|
| [`kuromoji`](#analysis-pipeline) | 內建的日文分析器。切分文字、移除停用詞，並將詞元正規化為其基本形式。 |
| [`kuromoji_completion`](#kuromoji-completion-analyzer) | 專為日文文字自動完成而設計的分析器。產生原始日文詞元及其羅馬字讀音變體。 |

### 斷詞器

| 斷詞器 | 說明 |
|:----------|:------------|
| [`kuromoji_tokenizer`]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/) | 以字典為基礎的日文斷詞器，具有可設定的切分模式。 |

### 字元篩選器

| 字元篩選器 | 說明 |
|:----------------|:------------|
| [`kuromoji_iteration_mark`]({{site.url}}{{site.baseurl}}/analyzers/character-filters/kuromoji-iteration-mark/) | 將日文疊字記號（々、ゝ、ゞ、ヽ 和 ヾ）展開為其所重複的字元，以進行正規化。 |

### 詞元篩選器

| 詞元篩選器 | 說明 |
|:------------|:------------|
| [`kuromoji_baseform`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-baseform/) | 將詞形變化的詞元替換為其字典基本形式。 |
| [`kuromoji_part_of_speech`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-part-of-speech/) | 移除詞性標記位於已設定之停用標記清單中的詞元。 |
| [`kuromoji_readingform`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-readingform/) | 將每個詞元替換為其片假名或羅馬字讀音。 |
| [`kuromoji_stemmer`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-stemmer/) | 移除片假名單字結尾的長音符號（ー）。 |
| [`ja_stop`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/ja-stop/) | 從詞元串流中移除日文停用詞。 |
| [`kuromoji_number`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-number/) | 將日文數字表示式轉換為標準阿拉伯數字。 |
| [`kuromoji_completion`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-completion/) | 為片假名詞元產生羅馬字讀音變體，以支援自動完成。 |

## 分析管線

`kuromoji` 分析器會依序對輸入文字套用下列元件：

1. `cjk_width` 字元篩選器會在斷詞之前，將全形 ASCII 變體轉換為對應的標準 ASCII 字元，並將半形片假名變體轉換為全形片假名。
2. 採用 `search` 模式的 `kuromoji_tokenizer` 會使用 IPAdic 字典切分文字，將較長的複合詞拆分為其子詞元。
3. `kuromoji_baseform` 詞元篩選器會將動詞和形容詞的變化形式替換為其字典形式（例如，食べた 會變成 食べる）。
4. `kuromoji_part_of_speech` 詞元篩選器會移除助詞（助詞）、助動詞（助動詞）、標點符號（記号）及其他停用標記。
5. `ja_stop` 詞元篩選器會移除常見的日文停用詞。
6. `kuromoji_stemmer` 詞元篩選器會移除四個字元以上之片假名單字結尾的長音符號（ー）（例如，コンピューター 會變成 コンピュータ）。
7. `lowercase` 詞元篩選器會將所有拉丁字元轉換為小寫。

## 參數

下表列出 `kuromoji` 分析器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`mode` | 字串 | 斷詞模式。有效值為 `normal`、`search`（預設）和 `extended`。詳細資訊請參閱[斷詞模式](#tokenization-modes)。
`user_dictionary` | 字串 | 放置於 OpenSearch config 目錄中的自訂使用者字典檔案（CSV 格式）路徑。選用。
`user_dictionary_rules` | 字串陣列 | CSV 格式的內嵌自訂字典規則。每個項目為 `<text>,<subtokens>,<readings>,<part of speech>`。選用。不能與 `user_dictionary` 同時使用。
`stopwords` | 字串或字串陣列 | 要使用的停用詞。可接受 `_japanese_`（內建的日文停用詞集）、明確停用詞的陣列，或停用詞檔案的路徑。預設為 `_japanese_`。

如需內建停用詞集中的完整停用詞清單，請參閱 Lucene 儲存庫中的 [stopwords.txt](https://github.com/apache/lucene/blob/main/lucene/analysis/kuromoji/src/resources/org/apache/lucene/analysis/ja/stopwords.txt)。

## 斷詞模式

斷詞器模式控制複合詞與未知詞的切分方式。

| 模式 | 效果 |
|:-----|:-------|
| `normal` | 標準的字典式切分。複合詞會保留為單一詞元。未知詞會保留為單一詞元。 |
| `search`（預設） | 與 `normal` 類似，但複合詞（例如地名）也會拆分為其子元件，以提高搜尋查詢的召回率。 |
| `extended` | 與 `normal` 類似，但未知詞會拆分為單字元（unigram，即個別字元），確保每個字元都會編製索引。 |

## 範例：基本用法

以下範例會建立使用內建 `kuromoji` 分析器的索引：

```json
PUT /japanese-index
{
  "mappings": {
    "properties": {
      "content": {
        "type": "text",
        "analyzer": "kuromoji"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用一個意思為「我在東京的圖書館讀書」的日文句子測試分析器：

```json
POST /_analyze
{
  "analyzer": "kuromoji",
  "text": "東京の図書館で勉強しました"
}
```
{% include copy-curl.html %}

分析器會傳回基本形式的詞元，並移除助詞與助動詞：

```json
{
  "tokens": [
    {
      "token": "東京",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "図書館",
      "start_offset": 3,
      "end_offset": 6,
      "type": "word",
      "position": 2
    },
    {
      "token": "勉強",
      "start_offset": 7,
      "end_offset": 9,
      "type": "word",
      "position": 4
    }
  ]
}
```

## 範例：自訂 Kuromoji 分析器

以下範例會建立自訂 `kuromoji` 分析器，並使用 `user_dictionary_rules` 註冊內嵌自訂詞彙：

```json
PUT /japanese-custom-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "my_kuromoji": {
          "type": "kuromoji",
          "mode": "search",
          "user_dictionary_rules": [
            "東京スカイツリー,東京 スカイツリー,トウキョウ スカイツリー,カスタム名詞"
          ]
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "title": {
        "type": "text",
        "analyzer": "my_kuromoji"
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含已註冊詞彙的句子（「我去了東京晴空塔」）測試自訂分析器：

```json
POST /japanese-custom-index/_analyze
{
  "analyzer": "my_kuromoji",
  "text": "東京スカイツリーに行きました"
}
```
{% include copy-curl.html %}

分析器會使用自訂字典規則，將 `東京スカイツリー` 切分為 `東京` 和 `スカイツリー`。預設的片假名詞幹提取器（`kuromoji_stemmer`）會移除 `スカイツリー` 結尾的長音符號，產生 `スカイツリ`。`kuromoji_part_of_speech` 篩選器會移除助詞 `に` 以及助動詞 `まし` 和 `た`，而 `kuromoji_baseform` 會將 `行き` 正規化為其基本形式 `行く`：

```json
{
  "tokens": [
    {
      "token": "東京",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "スカイツリ",
      "start_offset": 2,
      "end_offset": 8,
      "type": "word",
      "position": 1
    },
    {
      "token": "行く",
      "start_offset": 9,
      "end_offset": 11,
      "type": "word",
      "position": 3
    }
  ]
}
```

## Kuromoji 自動完成分析器

`kuromoji_completion` 分析器專為自動完成使用案例而設計。它會同時產生原始的日文詞元及其羅馬字（拉丁字母）讀音變體，讓使用者可以輸入日文字元或其羅馬拼音來搜尋日文內容。在 `query` 模式下，分析器還會先將輸入法編輯器（IME）的部分輸入組合成單一詞元，再進行羅馬字轉換。

下表列出 `kuromoji_completion` 分析器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`mode` | 字串 | 控制詞元的產生方式。有效值為 `index`（預設）和 `query`。兩種模式都會將片假名詞元展開為其原始形式以及所有羅馬字變體。`query` 模式會套用兩項額外規則來處理 IME 的部分輸入：在進行羅馬字轉換前，將連續的假名詞元串接成單一詞元；並將假名詞元與其後代表 IME 部分按鍵輸入的小寫英文字母詞元合併（例如，`サッ` 後接 `k` 會變成 `サッk`）。
`user_dictionary` | 字串 | 自訂使用者字典檔案的路徑。選用。
`user_dictionary_rules` | 字串陣列 | 內嵌的自訂字典規則。選用。

請在搜尋分析器中使用 `query` 模式，讓使用者輸入的 IME 部分輸入能在羅馬字轉換前正確組合。
{: .tip}

### 範例：使用 Kuromoji 自動完成分析器進行自動完成

下列範例設定一個索引，在編製索引時和搜尋時分別使用不同的自動完成分析器：

```json
PUT /autocomplete-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "kuromoji_index_analyzer": {
          "type": "kuromoji_completion",
          "mode": "index"
        },
        "kuromoji_search_analyzer": {
          "type": "kuromoji_completion",
          "mode": "query"
        }
      }
    }
  },
  "mappings": {
    "properties": {
      "suggest": {
        "type": "text",
        "analyzer": "kuromoji_index_analyzer",
        "search_analyzer": "kuromoji_search_analyzer"
      }
    }
  }
}
```
{% include copy-curl.html %}

如需自動完成詞元篩選器的詳細資訊，請參閱 [Kuromoji 自動完成詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-completion/)。

## 搭配使用 Kuromoji 和 ICU 外掛程式

若要進行最完整的日文文字分析，請結合 `analysis-kuromoji` 和 `analysis-icu` 外掛程式。ICU 提供全形與半形字元的 Unicode 正規化，以及完整的字元摺疊功能，這些是單靠 Kuromoji 元件無法提供的。

在建立使用這兩個外掛程式元件的索引之前，必須先安裝 `analysis-kuromoji` 和 `analysis-icu`。
{: .note}

下列範例建立一個結合這兩個外掛程式的自訂分析器。`icu_normalizer` 字元篩選器會在斷詞前將全形字元轉換為對應的 ASCII 字元（例如，`３００` 會變成 `300`），使數字序列保持為單一詞元。`kuromoji_iteration_mark` 字元篩選器會展開日文的疊字記號（例如，`時々` 會變成 `時時`），讓斷詞器能在字典中正確查詢：

```json
PUT /japanese-icu-index
{
  "settings": {
    "index": {
      "analysis": {
        "analyzer": {
          "japanese_icu_analyzer": {
            "char_filter": [
              "icu_normalizer",
              "kuromoji_iteration_mark"
            ],
            "tokenizer": "kuromoji_tokenizer",
            "filter": [
              "kuromoji_baseform",
              "kuromoji_part_of_speech",
              "ja_stop",
              "kuromoji_stemmer",
              "lowercase"
            ]
          }
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用包含全形數字和長音符號的句子（「電腦處理 300 份文件」）測試此組合分析器：

```json
POST /japanese-icu-index/_analyze
{
  "analyzer": "japanese_icu_analyzer",
  "text": "コンピューターは３００件の文書を処理します"
}
```
{% include copy-curl.html %}

分析器會套用下列轉換：

- `icu_normalizer` 會在斷詞前將全形數字 `３００` 轉換為 `300`。
- `kuromoji_stemmer` 會移除結尾的長音符號，將 `コンピューター` 轉換為 `コンピュータ`。
- `kuromoji_part_of_speech` 會移除助詞 `は`、`の` 和 `を`，以及助動詞 `ます`。
- `ja_stop` 會移除 `し`，因為它出現在 `_japanese_` 停用詞集中。
- `300` 會保持為單一詞元，而 `文書` 和 `処理` 會以基本形式傳回。

回應如下所示：

```json
{
  "tokens": [
    {
      "token": "コンピュータ",
      "start_offset": 0,
      "end_offset": 7,
      "type": "word",
      "position": 0
    },
    {
      "token": "300",
      "start_offset": 8,
      "end_offset": 11,
      "type": "word",
      "position": 2
    },
    {
      "token": "件",
      "start_offset": 11,
      "end_offset": 12,
      "type": "word",
      "position": 3
    },
    {
      "token": "文書",
      "start_offset": 13,
      "end_offset": 15,
      "type": "word",
      "position": 5
    },
    {
      "token": "処理",
      "start_offset": 16,
      "end_offset": 18,
      "type": "word",
      "position": 7
    }
  ]
}
```

## 相關文件

- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
- [Kuromoji 疊字記號字元篩選器]({{site.url}}{{site.baseurl}}/analyzers/character-filters/kuromoji-iteration-mark/)
- [ICU 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/icu/)
- [CJK 寬度詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/cjk-width/)
