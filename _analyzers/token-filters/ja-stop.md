---
# Modified by the jiayun zh-TW fork: Taiwan Traditional Chinese translation and website adaptations.
layout: default
title: "日文停用詞"
parent: Token filters
nav_order: 178
---

# 日文停用詞詞元篩選器

`ja_stop` 詞元篩選器會從詞元串流中移除日文停用詞。它會將詞元與字詞清單比對，該清單可以是內建的日文停用詞集，也可以是您提供的自訂清單。若要改為依文法類別移除詞元，請使用 [`kuromoji_part_of_speech`]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-part-of-speech/)。

此篩選器也支援適用於建議功能的模式（`remove_trailing: false`），在此模式下會保留結尾的停用詞。這對自動完成的使用情境很重要，因為使用者可能正在輸入一個以停用詞或助詞結尾的片語。

## 安裝

`ja_stop` 詞元篩選器需要 `analysis-kuromoji` 外掛程式。如需安裝說明，請參閱 [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)。

## 參數

下表列出 `ja_stop` 詞元篩選器的參數。

參數 | 資料類型 | 說明
:--- | :--- | :---
`stopwords` | 字串或字串陣列 | 要使用的停用詞。可接受 `_japanese_` 以使用內建的日文停用詞集、明確列出停用詞的陣列，或是指向每行包含一個停用詞之檔案的路徑。預設為 `_japanese_`（與內建 `kuromoji` 分析器所使用的停用詞集相同）。
`ignore_case` | 布林值 | 設為 `true` 時，停用詞比對不區分大小寫。預設為 `false`。
`remove_trailing` | 布林值 | 設為 `true`（預設）時，會移除詞元串流結尾的停用詞。設為 `false` 時，會保留結尾的停用詞，讓前綴比對的自動完成查詢能在部分輸入的內容上正確運作。

如需內建停用詞集中的完整停用詞清單，請參閱 Lucene 儲存庫中的 [stopwords.txt](https://github.com/apache/lucene/blob/main/lucene/analysis/kuromoji/src/resources/org/apache/lucene/analysis/ja/stopwords.txt)。

## 範例：最簡用法

下列範例單獨使用 `ja_stop`，以顯示此篩選器本身會移除哪些內容：

```json
PUT /ja-stop-minimal-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ja_stop_minimal_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["ja_stop"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用句子 `新聞を読んでいるばかりだ`（「我只讀報紙，什麼也不做」）測試分析器，斷詞器會將其切分為 `新聞`、`を`、`読ん`、`で`、`いる`、`ばかり` 和 `だ`：

```json
POST /ja-stop-minimal-index/_analyze
{
  "analyzer": "ja_stop_minimal_analyzer",
  "text": "新聞を読んでいるばかりだ"
}
```
{% include copy-curl.html %}

此篩選器會移除 `を`、`で`、`いる` 和 `だ`，因為它們位於 `_japanese_` 停用詞集中。屈折詞幹 `読ん` 和副助詞 `ばかり` 不在停用詞集中，因此它們會與內容詞元 `新聞` 一同保持不變，因為 `ja_stop` 不會將屈折變化正規化，也不會依文法類別進行篩選：

```json
{
  "tokens": [
    {
      "token": "新聞",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "読ん",
      "start_offset": 3,
      "end_offset": 5,
      "type": "word",
      "position": 2
    },
    {
      "token": "ばかり",
      "start_offset": 8,
      "end_offset": 11,
      "type": "word",
      "position": 5
    }
  ]
}
```

請將此結果與下列[完整管線範例](#example-full-analysis-pipeline)比較。加入 `kuromoji_baseform` 會將 `読ん` 正規化為其辭典形式 `読む`。加入 `kuromoji_part_of_speech` 會移除副助詞 `ばかり`，該助詞不在 `_japanese_` 停用詞清單中，因此無法僅靠 `ja_stop` 移除。

## 範例：完整分析管線

此範例使用相同的句子 `新聞を読んでいるばかりだ`（「我只讀報紙，什麼也不做」），以顯示三個篩選器結合使用時各自負責的不同工作：

- `kuromoji_baseform` 會將屈折動詞詞幹 `読ん` 正規化為其辭典形式 `読む`。
- `kuromoji_part_of_speech` 會移除 `ja_stop` 無法處理的副助詞 `ばかり`，以及 `ja_stop` 也會移除的助詞 `を`、`で` 和 `だ`。
- `ja_stop` 會移除剩餘的 `いる`，該詞列於內建的日文停用詞集中。

建立一個索引，並使用串接這三個篩選器的分析器：

```json
PUT /ja-stop-index
{
  "settings": {
    "analysis": {
      "analyzer": {
        "ja_stop_analyzer": {
          "type": "custom",
          "tokenizer": "kuromoji_tokenizer",
          "filter": ["kuromoji_baseform", "kuromoji_part_of_speech", "ja_stop"]
        }
      }
    }
  }
}
```
{% include copy-curl.html %}

使用相同的句子測試分析器：

```json
POST /ja-stop-index/_analyze
{
  "analyzer": "ja_stop_analyzer",
  "text": "新聞を読んでいるばかりだ"
}
```
{% include copy-curl.html %}

回應中僅包含兩個內容詞元，且動詞為其基本形式：

```json
{
  "tokens": [
    {
      "token": "新聞",
      "start_offset": 0,
      "end_offset": 2,
      "type": "word",
      "position": 0
    },
    {
      "token": "読む",
      "start_offset": 3,
      "end_offset": 5,
      "type": "word",
      "position": 2
    }
  ]
}
```

## 相關文件

- [Kuromoji 分析器]({{site.url}}{{site.baseurl}}/analyzers/language-analyzers/kuromoji/)
- [Kuromoji 斷詞器]({{site.url}}{{site.baseurl}}/analyzers/tokenizers/kuromoji/)
- [Kuromoji 基本形式詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-baseform/)
- [Kuromoji 詞性詞元篩選器]({{site.url}}{{site.baseurl}}/analyzers/token-filters/kuromoji-part-of-speech/)
